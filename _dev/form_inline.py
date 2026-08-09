#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The signup band answers on the page. On all 158 pages, not on five.

THE REPORT

  "can the footer email just reply with confirmation and results within the
   page? I don't like it going to formspring, looks bad"

WHAT WAS ACTUALLY WRONG, WHICH WAS NOT WHAT IT LOOKED LIKE

The handler that does this already existed and is good. It posts in the
background, echoes the address back so the reader can see they did not typo
it, and - the part that matters - gives a message and a mailing-list signup
different answers, because being told "you're on the list" after reporting a
bug reads as though the report went nowhere.

It lives in `mock/amft/_chrome_js.txt`, a builder chrome fragment, and it
therefore reached **five pages**: about, contact, index, newsletter and rates.
The signup band itself is injected by `_dev/footer_band.py` onto all 158. So
on 153 pages the form was still a plain POST that navigated the reader to
Formspree's own confirmation page - exactly the thing that was reported.

The first attempt at this file wrote a *second* handler and put it everywhere,
which fixed 153 pages and broke 5: two handlers raced to replace the same
`<form>` node and fired two POSTs for one click, and in the failure path the
second one captured "Sending…" as the button's original label and restored it
to that, so the button stuck. Caught in a real browser, not by a syntax check.
A duplicate that works is invisible; a duplicate that races is a bug report.

WHAT THIS DOES NOW

Lifts that same handler, verbatim, out of `_chrome_js.txt` and injects it on
every page that has a Formspree form and no handler yet. One implementation,
in one place, reaching every page it should have reached to begin with. If
somebody improves the copy in `_chrome_js.txt`, this pass carries the
improvement everywhere on the next run.

  - **Pages that already have it are skipped**, so the five keep exactly the
    handler their builder gave them and nothing races.
  - **The form still works with JavaScript off.** The handler's only structural
    act is `preventDefault` inside a submit listener. No script, no listener,
    and the browser posts the form the old way - off-site, but working.
  - **The `.nlok` and `.nlerr` styles are already site-wide**, so nothing new
    is needed for it to render; that was checked rather than assumed.

Idempotent. Guarded on the invariant that made the first attempt a bug:
exactly one script per page may handle a Formspree submit.

THE LESSON, WHICH IS WHY THE HISTORY IS WRITTEN DOWN HERE

Before adding a behaviour, read a built page for it. `_dev/` is ~40 passes and
some behaviour comes from `mock/` builders instead; "does this already exist?"
is not answerable from the file names. Fifteen seconds of `grep submit
contact.html` would have replaced an hour.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SOURCE = os.path.join(SITE, "mock", "amft", "_chrome_js.txt")
JSMARK = "// _dev/form_inline.py - lifted from mock/amft/_chrome_js.txt"
# the sentence that identifies the block inside that file
SIGIL = "Post the signup in the background"
# left behind by the first, duplicated attempt
LEGACY_CSS = "/* _dev/form_inline.py */"
LEGACY_JS = "// _dev/form_inline.py\n"


def is_handler(code):
    """Binds a submit listener AND posts by itself.

    `_dev/analytics_events.py` also listens for submit and is deliberately not
    counted: it records an event and lets the form proceed. Counting it would
    make this pass refuse to run on every page on the site."""
    return bool(re.search(r"addEventListener\(\s*['\"]submit", code)
                and ("fetch(" in code or "XMLHttpRequest" in code))


def handler():
    """The signup IIFE, exactly as the builder writes it.

    Taken by locating the sentence and walking back to the `(function(){` that
    opens its block, rather than by slicing at a fixed offset - the file has
    several IIFEs and they get reordered."""
    if not os.path.exists(SOURCE):
        sys.exit("form_inline: %s is gone. That file is the single copy of "
                 "this handler; this pass cannot invent a replacement, and "
                 "writing a second implementation is what broke it last time."
                 % SOURCE)
    js = open(SOURCE, encoding="utf-8").read()
    i = js.find(SIGIL)
    if i < 0:
        sys.exit("form_inline: %r is no longer in %s - the handler was renamed "
                 "or removed" % (SIGIL, SOURCE))
    start = js.rfind("(function(){", 0, i)
    if start < 0:
        sys.exit("form_inline: found the handler but not the function that "
                 "opens it")
    # walk to the matching close, counting braces outside strings and comments
    depth = 0
    end = -1
    k = start
    while k < len(js):
        c = js[k]
        if c in "'\"":
            q = c
            k += 1
            while k < len(js) and js[k] != q:
                k += 2 if js[k] == "\\" else 1
        elif js.startswith("//", k):
            k = js.find("\n", k)
            if k < 0:
                break
        elif js.startswith("/*", k):
            k = js.find("*/", k) + 1
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = js.find(";", k)
                break
        k += 1
    if end < 0:
        sys.exit("form_inline: could not find the end of the handler")
    return js[start:end + 1]


def main():
    code = handler()
    block = "<script>%s\n%s\n</script>" % (JSMARK, code)
    print("the signup band answers on the page, everywhere:")
    print("  handler lifted from mock/amft/_chrome_js.txt, %d chars" % len(code))

    added = skipped = cleaned = 0
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s

        # remove our own, including the first attempt's separate stylesheet
        s = re.sub(r"\n?<style>" + re.escape(LEGACY_CSS) + r"[\s\S]*?</style>\n?",
                   "", s)
        s = re.sub(r"\n?<script>" + re.escape(JSMARK) + r"[\s\S]*?</script>\n?",
                   "", s)
        s = re.sub(r"\n?<script>" + re.escape(LEGACY_JS) + r"[\s\S]*?</script>\n?",
                   "", s)
        if s != orig:
            cleaned += 1

        if "formspree.io" in s:
            has = any(is_handler(m.group(1)) for m in
                      re.finditer(r"<script[^>]*>([\s\S]*?)</script>", s))
            if has:
                skipped += 1
            else:
                e = s.lower().rfind("</body>")
                if e < 0:
                    print("  MISSING  %s has no </body>" % rel)
                    continue
                s = s[:e] + block + "\n" + s[e:]
                added += 1

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)

    print("  %d page(s) given the handler, %d already had it from their "
          "builder" % (added, skipped))

    # --------------------------------------------------------------- guards
    bad = 0
    checked = 0
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s or "formspree.io" not in s:
            continue
        checked += 1
        n = sum(1 for m in re.finditer(r"<script[^>]*>([\s\S]*?)</script>", s)
                if is_handler(m.group(1)))
        if n != 1:
            print("GUARD %s: %d scripts handle a Formspree submit. Two "
                  "handlers race to replace the same <form> node and fire two "
                  "POSTs for one click." % (rel, n))
            bad += 1
        # A reader with JavaScript off must still reach a working endpoint.
        for tag in re.findall(r"<form[^>]*formspree\.io[^>]*>", s):
            if 'method="post"' not in tag.lower():
                print("GUARD %s: a Formspree form lost its method=post, so it "
                      "does nothing without JavaScript" % rel)
                bad += 1
        # The confirmation has to be able to render. These styles come from
        # elsewhere on the site, so this is a real dependency and not a
        # formality.
        if ".nlok" not in s and not re.search(r'href="css/', s):
            print("GUARD %s: no .nlok styles and no stylesheet link" % rel)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d page(s) with a form, each with exactly one "
          "handler, each still posting without JavaScript" % checked)


if __name__ == "__main__":
    main()
