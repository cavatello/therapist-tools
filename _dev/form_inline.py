#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One Formspree handler per page, and only one.

WHAT THIS FILE WAS, AND WHAT HAPPENED

It was written to answer this:

  "can the footer email just reply with confirmation and results within the
   page? I don't like it going to formspring, looks bad"

That work was **already done**, in an earlier session, and done better. The
existing handler - injected with the signup band itself - echoes the address
back to the reader, gives a message and a mailing-list signup different
answers ("you're on the list" after reporting a bug reads as though the report
went nowhere), and reports a valueless `gtag` event. It is the one that should
be running.

The duplicate shipped for one deploy and was caught in a real browser rather
than by a syntax check: submitting the contact form fired **two** POSTs to
Formspree, the two handlers raced to replace the same `<form>` node, and the
confirmation box never appeared. In the failure path the second handler
captured "Sending…" as the button's original label and restored it to that, so
the button stayed stuck. A duplicate that works is invisible; a duplicate that
races is a bug report.

WHAT IT DOES NOW

Strips its own former output wherever it still exists, and then asserts the
invariant that made the bug possible in the first place:

  **exactly one script on any page may handle a Formspree submit.**

Nothing else. It writes only to remove itself.

THE LESSON, WHICH IS THE POINT OF KEEPING THIS FILE

Before writing a pass, read the page for the behaviour you are about to add.
`_dev/` has ~40 passes now and no index of what each one injects; "does this
already exist?" is not answerable from the file names. Fifteen seconds of
`grep 'submit' contact.html` would have replaced an hour.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/form_inline.py */"
JSMARK = "// _dev/form_inline.py"

# A script counts as a Formspree handler if it binds a submit listener AND
# posts somewhere itself. `analytics_events.py` also listens for submit, and
# it is not a handler - it counts an event and lets the form proceed.
def is_handler(code):
    return ("submit" in code
            and re.search(r"addEventListener\(\s*['\"]submit", code)
            and ("fetch(" in code or "XMLHttpRequest" in code))


def main():
    print("one Formspree handler per page:")
    removed = 0
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        s = re.sub(r"\n?<script>" + re.escape(JSMARK) + r"[\s\S]*?</script>\n?",
                   "", s)
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            removed += 1
    if removed:
        print("  removed the duplicate handler from %d page(s)" % removed)
    else:
        print("  nothing to remove")

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
        handlers = [m.group(1) for m in
                    re.finditer(r"<script[^>]*>([\s\S]*?)</script>", s)
                    if is_handler(m.group(1))]
        if len(handlers) != 1:
            print("GUARD %s: %d scripts handle a Formspree submit. Two "
                  "handlers race to replace the same <form> node and fire two "
                  "POSTs for one click." % (rel, len(handlers)))
            bad += 1
        # The form must still be a real POST, so a reader with JavaScript off
        # reaches a working endpoint rather than a button that does nothing.
        for tag in re.findall(r"<form[^>]*formspree\.io[^>]*>", s):
            if 'method="post"' not in tag.lower():
                print("GUARD %s: a Formspree form lost its method=post" % rel)
                bad += 1
        if MARK in s or JSMARK in s:
            print("GUARD %s: the duplicate handler is still here" % rel)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d page(s) with a form, each with exactly one "
          "handler, each still posting without JavaScript" % checked)


if __name__ == "__main__":
    main()
