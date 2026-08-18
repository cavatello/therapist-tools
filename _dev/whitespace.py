#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every build leaked blank lines, and that is why a deploy touched 250 files.

WHAT WAS HAPPENING

Several passes maintain a block in a shared file by removing their old one and
appending a fresh copy:

    new = re.sub(MARK ... END, "", sheet).rstrip()
    new += "\\n\\n" + CSS.strip() + "\\n"

The `rstrip()` cleans up only when the block happened to be last. Three passes
write `css/house-chrome.css` this way - `ask_surface.py`, `footer_index.py`
and `stage_shell.py` - so on any given run at most one of them is last and the
other two cut their block out of the MIDDLE, leaving the newlines that were on
either side of it. A few more every build, forever.

`css/house-chrome.css` had reached runs of **253 consecutive blank lines**.

WHY IT MATTERED, WHICH IS NOT THE BYTES

63 KB of blank lines across a 46 MB site is nothing. The cost is that changing
one byte of a stylesheet changes its sha1, and the family passes stamp that
sha1 into `href="css/house-chrome.css?v=<hash>"` on every page that links it.
So **six blank lines nobody could see repointed 239 pages**, and a deploy that
should have been forty files was two hundred and fifty.

That is not a cosmetic problem. It buries the real change among two hundred
that say nothing, and it makes a byte-comparison against live useless as a
verification.

WHAT THIS DOES

    python3 _dev/whitespace.py --css     collapse runs in the hand-authored
                                         sheets, BEFORE anything hashes them
    python3 _dev/whitespace.py --html    the same for published pages, last
    python3 _dev/whitespace.py --check   verify only; writes nothing

Runs of three or more newlines become two - one blank line, which is a
paragraph break and is worth keeping. Only the hand-authored `css/house*.css`
are touched: the content-addressed sheets are GENERATED from page style blocks
by `extract_css.py`, and rewriting one after it has been named would break the
relationship between a sheet's name and its contents, which is the trap
`type_census.py` already documents.

In HTML, `<pre>`, `<textarea>`, `<script>` and `<style>` are held out. The
first two because whitespace there is content; the second two because
`extract_css.py` hoists style blocks by exact match and `css_dedupe.py`
collapses byte-identical copies - reformatting one would quietly defeat both.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

RUN = re.compile(r"\n{3,}")
PROTECT = re.compile(r"<(pre|textarea|script|style)\b[\s\S]*?</\1>", re.I)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f)
                    for f in sorted(os.listdir(p)) if f.endswith(".html")]
    return out


def sheets():
    d = os.path.join(SITE, "css")
    if not os.path.isdir(d):
        return []
    return ["css/" + f for f in sorted(os.listdir(d))
            if f.startswith("house") and f.endswith(".css")]


def squeeze_html(s):
    held = []

    def hold(m):
        held.append(m.group(0))
        return "\x01%d\x01" % (len(held) - 1)

    s = PROTECT.sub(hold, s)
    s = RUN.sub("\n\n", s)
    for i, v in enumerate(held):
        s = s.replace("\x01%d\x01" % i, v)
    return s


def runs_in(s, html):
    if html:
        held = PROTECT.sub("", s)
        return [len(m.group(0)) - 1 for m in RUN.finditer(held)]
    return [len(m.group(0)) - 1 for m in RUN.finditer(s)]


def main(what, check_only=False):
    targets = []
    if what in ("css", "all"):
        targets += [(f, False) for f in sheets()]
    if what in ("html", "all"):
        targets += [(f, True) for f in pages()]

    changed, saved, worst = 0, 0, 0
    for rel, html in targets:
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        before = runs_in(s, html)
        if before:
            worst = max(worst, max(before))
        out = squeeze_html(s) if html else RUN.sub("\n\n", s)
        if out != s:
            saved += len(s) - len(out)
            changed += 1
            if not check_only:
                open(p, "w", encoding="utf-8").write(out)

    if check_only:
        if changed:
            print("GUARD: %d file(s) still carry a run of 3+ newlines, the "
                  "longest %d blank lines - %d bytes that repoint every "
                  "`?v=` hash for nothing" % (changed, worst - 1, saved))
            sys.exit("%d file(s) not normalised" % changed)
        print("no file carries more than one consecutive blank line, so a "
              "stylesheet's hash only moves when its rules do")
        return

    print("%s: %d file(s) normalised, %d byte(s) of blank line removed"
          % (what, changed, saved))


if __name__ == "__main__":
    what = "html" if "--html" in sys.argv else ("css" if "--css" in sys.argv
                                                else "all")
    main(what, "--check" in sys.argv)
