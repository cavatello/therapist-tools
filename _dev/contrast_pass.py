#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Raise the muted label colour sitewide, measured rather than eyeballed.

WHAT THE SWEEP FOUND

A headless pass over the live site, measuring every text node's computed colour
against its computed background, found one defect repeated everywhere: the
small-caps meta labels are too light. Not one class — a whole family, because
they were all set from the same idea of "muted":

    .chk    2.66:1     "Checked Aug 2026" on a library card
    .uk     2.96:1     "MORE ON THIS" on the up-link
    .cun    3.24:1     the unit count on a course card
    .yr     3.53:1     the year beside a tuition figure
    .vmeta  3.53:1     the source line under a video
    .sn     3.56:1     the sentiment tag on a quote
    .tm     3.56:1     the thread meta on a forum link
    .np     3.72:1     "not published"
    .tn     3.72:1     the numbers in the on-this-page rail

The floor for text this size is 4.5:1. Every one of them is under it, and the
worst — "Checked Aug 2026" — is the site's own freshness stamp.

None of these are decorative. "Not published" is a substantive answer on this
site, and the check date is the thing the whole two-clocks pattern exists to
surface. A label you have to lean in to read is a label that is not doing its
job.

WHY THIS IS AN OVERRIDE AND NOT AN EDIT TO THE SOURCE

The colours are spread across generated stylesheets in css/ and across
_dev/restyle.css, which is on the do-not-edit list. So this is a last-loaded,
scoped override the pipeline re-emits — the same shape as _dev/footer_fix.py.

WHAT IS DELIBERATELY LEFT ALONE

.hint, .sub, .nlmeta, .long and .pr-kick also came back low, and they are NOT in
the list below. Each of them appears on a dark band as well as a light one, and
a blanket colour would fix one context by breaking the other. Some were also
false positives in the sweep itself: the dark bands are gradients, so a
background-COLOUR walk sails past them and compares white hero text against
cream. Those need per-context rules and a per-context measurement, and guessing
at them here would be exactly the mistake this pass exists to correct.

Every value below is verified against the four light surfaces the site actually
uses, and the pass exits non-zero if any of them lands under the floor.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/contrast_pass.py */"

# The light surfaces in the palette. The DARKEST of these is the hardest case
# for a grey label, so all four are checked and the worst is what counts.
SURFACES = {
    "white":  (0xFF, 0xFF, 0xFF),
    "cream":  (0xFB, 0xF9, 0xF3),
    "paper":  (0xF4, 0xF0, 0xE6),
    "sand":   (0xF0, 0xEA, 0xDA),
}

MUTED = (0x63, 0x5D, 0x4E)      # replaces #9A8F76 / #A79E88 / #B0A896
FLOOR = 4.5

# Classes that only ever sit on a light surface. Verified by reading where each
# one is emitted, not assumed from the name.
LIGHT_ONLY = [
    "uk", "chk", "cun", "yr", "vmeta", "sn", "tm", "tn", "np", "ig-k",
    "ocl", "disc", "nx-k", "nx-f", "org", "mods", "sb", "cred", "meth",
    "tvnote", "rgmore", "lname", "ud", "uall", "pdcity", "pdyr",
]


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(rgb):
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def css():
    sel = ",".join(".%s" % c for c in LIGHT_ONLY)
    hexv = "#%02X%02X%02X" % MUTED
    return ("<style>%s\n"
            "/* One muted label colour, verified against every light surface in\n"
            "   the palette. Replaces #9A8F76, #A79E88 and #B0A896, all of which\n"
            "   measured under 4.5:1. */\n"
            "%s{color:%s}\n"
            "</style>" % (MARK, sel, hexv))


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    print("muted label #%02X%02X%02X against every light surface:" % MUTED)
    worst = 99.0
    for name, bg in sorted(SURFACES.items()):
        r = ratio(MUTED, bg)
        worst = min(worst, r)
        print("  %-7s %5.2f:1  %s" % (name, r, "ok" if r >= FLOOR else "FAILS"))
    if worst < FLOOR:
        sys.exit("the replacement colour does not clear %.1f:1 on every "
                 "surface - darken it, do not lower the floor" % FLOOR)

    n = 0
    block = css()
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + block + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("%d page(s) given the label override" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d class(es) raised to at least %.2f:1"
          % (len(LIGHT_ONLY), worst))


if __name__ == "__main__":
    main()
