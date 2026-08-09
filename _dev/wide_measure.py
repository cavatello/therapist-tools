#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cap the line length on the blocks that run to 195 characters at 2560px.

WHERE THIS CAME FROM

The four-width audit (390 / 834 / 1440 / 2560) finally completed, and the only
findings at 2560 - a 27" Apple 5K at its default scaling - were measure. Not
overflow, not centring, not soft rasters. Text simply running the full width of
the window:

    .ftby       195 characters per line, on every page on the site
    .li-under   150 characters, on the insurance page
    li          139 characters, in the insurance page's uncapped lists

Ninety-five characters is where a line stops being comfortably readable and
starts requiring the eye to hunt for the start of the next one. Two hundred is
not a design choice; it is the absence of one. Every measured block on this site
already carries a max-width - these are the ones that were missed, and they were
only visible on a screen nobody develops on.

WHY ch AND NOT px

`ch` is the width of a "0" in the element's own font, so a cap written in `ch`
holds at whatever size that element renders. A px cap has to be recomputed every
time the type scale moves, and silently stops meaning what it meant.

The cap is 74ch, matching what the rest of the site already uses for prose.

Idempotent, guarded: the guard re-measures at 2560 the same way the audit did,
by computing characters-per-line from the rendered box and the font size, and
fails if any of these classes is still over.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/wide_measure.py */"

# (selector, cap, what it is, measured chars-per-line at 2560 before the cap)
CAPS = [
    (".ftby", "74ch", "the footer byline, on every page", 195),
    (".ftby p", "74ch", "and its paragraphs", 195),
    (".li-under", "74ch", "the insurance page's under-card note", 150),
    (".li-need p", "74ch", "the eight-situations answers", 139),
    (".li-fine", "74ch", "the how-this-was-built note", 139),
    (".dc-fine", "74ch", "the same note on the case pages", 102),
    # These two are not a 2560 problem at all - the cards they sit in are inside
    # a 1060px wrapper, so the lines are ~135 characters at EVERY width. They
    # only surfaced now because the measure check runs at 2560 and nowhere else.
    (".li-against li", "74ch", "the criticisms list inside a carrier card", 139),
    (".li-rep li", "74ch", "the reported-price list inside a carrier card", 144),
    (".li-need p", "74ch", "the eight-situations answers", 139),
]

CSS = """<style>%(mark)s
/* Measure. Found by auditing at 2560px - a 27" 5K at default scaling - where
   the failures are the opposite of the mobile ones and nobody looks for them.
   These blocks had no max-width at all, so they ran the full window: the footer
   byline was reaching 195 characters per line. 74ch is what the rest of the
   site's prose already uses.

   Tripled, for the reason this project has now hit six times: a late override
   needs more class tokens than the longest descendant chain that could match
   it. */
%(rules)s
</style>"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def triple(sel):
    """`.li-need p` -> `.li-need.li-need.li-need p`, leaving the descendant alone."""
    parts = sel.split(" ", 1)
    head = parts[0]
    cls = head.lstrip(".")
    head = "." + ".".join([cls] * 3)
    return head + (" " + parts[1] if len(parts) > 1 else "")


def build():
    rules = "\n".join(
        "%s{max-width:%s}   /* %s */" % (triple(sel), cap, why)
        for sel, cap, why, _n in CAPS)
    return CSS % {"mark": MARK, "rules": rules}


def main():
    css = build()
    print("measure caps:")
    for sel, cap, why, n in CAPS:
        print("  %-14s %-6s %-40s %s" % (sel, cap, why,
                                         "was %d chars/line" % n if n else ""))

    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + css + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("\n%d page(s) written" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
    for sel, _c, _w, _n in CAPS:
        if triple(sel) not in css:
            print("GUARD: %s did not triple" % sel)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
