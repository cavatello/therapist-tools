#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The site footer was legible on some pages and not on others.

WHAT WAS HAPPENING

`.ftcols a{color:rgba(255,255,255,.72)}` - the rule that makes the footer links
readable on the near-black band - lives in ONE extracted stylesheet, and not
every page links that stylesheet. `extract_css.py` only hoists a block that four
or more pages share, and it links each page to the blocks that page actually
had; a template that never carried the footer block never gets the file.

On the pages that do link it, the footer reads cream on ink. On the pages that
do not, the links fall back to the site's default link colour - pine #2C6350 -
on a #16211B band. That is a contrast ratio of about 1.6:1. The links are
effectively invisible, which is what "the footers are not matching" was.

WHY THIS IS A LAST-LOADED OVERRIDE AND NOT AN EDIT TO THE SHARED FILE

The shared file is generated. Editing css/*.css by hand is reverted by the next
`extract_css.py` run - that is written on the tin - so the correction has to be
something the pipeline re-emits. It is scoped `.sitefoot .ftcols a` rather than
`.ftcols a` so it outranks any page-local `a{}` rule regardless of load order,
and it is appended last on every page so it cannot be a race.

The footer is chrome. Chrome that renders differently depending on which
stylesheet a page happened to inherit is not chrome, it is an accident.

Idempotent, and guarded against the numbers rather than the rules: the contrast
ratio of every declared colour against the footer band is computed here, and the
pass fails if any of them lands under 4.5:1.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

MARK = "/* _dev/footer_fix.py */"
BAND = (0x16, 0x21, 0x1B)          # .sitefoot background

CSS = """<style>%s
/* The footer is chrome and must not depend on which stylesheet a page
   inherited. Scoped to .sitefoot so it outranks a page-local a{} rule, and
   appended last so it cannot lose a load-order race. */
.sitefoot .ftcols a{color:rgba(255,255,255,.78)}
.sitefoot .ftcols a:hover{color:#fff;text-decoration:underline}
.sitefoot .ftcols h5{color:#16211B;background:#F6C560}
.sitefoot .ftcols p{color:rgba(255,255,255,.62)}
.sitefoot .ftby{color:rgba(255,255,255,.62)}
.sitefoot .ftby b{color:rgba(255,255,255,.88)}
.sitefoot .ftby a,.sitefoot .ftcols a:focus-visible{color:#F6C560}
""" % MARK + "</style>"

# (label, colour, alpha) as declared above, for the contrast guard.
DECLARED = [
    (".ftcols a", (255, 255, 255), 0.78),
    (".ftcols p", (255, 255, 255), 0.62),
    (".ftby", (255, 255, 255), 0.62),
    (".ftby b", (255, 255, 255), 0.88),
    (".ftby a", (0xF6, 0xC5, 0x60), 1.0),
]


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(rgb):
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def over(fg, a, bg):
    """What the eye actually sees: the declared colour composited onto the band
    at its alpha. Checking the declared colour alone would pass a 20%-opacity
    white that is unreadable."""
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))


def ratio(fg, a, bg):
    l1, l2 = lum(over(fg, a, bg)), lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    print("contrast against the footer band #16211B:")
    worst = 99.0
    for label, rgb, a in DECLARED:
        r = ratio(rgb, a, BAND)
        worst = min(worst, r)
        print("  %-12s %5.2f:1 %s" % (label, r, "ok" if r >= 4.5 else "FAILS"))
    if worst < 4.5:
        sys.exit("a declared footer colour is under 4.5:1 - fix the CSS, not "
                 "the guard")

    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitefoot" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?",
                   "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + CSS + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("%d page(s) given the footer override" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitefoot" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies of the override" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
