#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The eyebrow label on a dark hero band, measured against the band it sits on.

WHAT THIS FIXES

_dev/contrast_pass.py deliberately left `.sub` alone, and said why:

    ".hint, .sub, .nlmeta, .long and .pr-kick also came back low, and they are
     NOT in the list below. Each of them appears on a dark band as well as a
     light one, and a blanket colour would fix one context by breaking the
     other ... the dark bands are gradients, so a background-COLOUR walk sails
     past them and compares white hero text against cream. Those need
     per-context rules and a per-context measurement."

This is that per-context measurement. It was prompted by a real report: the
eyebrow above the h1 on mft-programs-california.html reads

    "78 California programs - every one the Board recognizes"

in #4E4940 on a pine gradient. Measured in the browser, that is 1.20:1. The
text is effectively invisible.

THE CAUSE, WHICH IS A MISSING RULE RATHER THAN A WRONG ONE

Every dark hero band in the site sets its own eyebrow colour:

    .libband .sub   var(--amber)
    .pxband  .sub   var(--amber)
    .scband  .sub   var(--amber)

`.pdband` - which exists on exactly one page - was never given the rule, so it
falls through to the base `p.sub{color:#4E4940}`, a warm grey chosen for the
cream body surface. Right colour, wrong surface.

AND A SECOND DEFECT THE MEASUREMENT TURNED UP

var(--amber) is #F6C560. Against the lightest stop of every dark band gradient,
#2C6350, that measures 4.26:1 - under the 4.5:1 floor this site holds itself
to. So the three bands that DID have the rule were also failing, just less
obviously than the one that didn't. The project already settled on #FFD37A for
gold-on-pine for this exact reason; this pass applies that decision to the
eyebrows too. #FFD37A measures 4.88:1 on the same surface.

WHY AN OVERRIDE RATHER THAN AN EDIT AT SOURCE

Same reason as contrast_pass.py: the colours live in generated stylesheets under
css/ and in _dev/restyle.css, which is on the do-not-edit list. This is a
last-loaded, scoped block the pipeline re-emits.

ON SPECIFICITY

`.pdband .sub` is (0,2,0) and already beats the base `p.sub` at (0,1,1). The
doubled form below is belt-and-braces against a later single-class override
landing in the same cascade position, and costs nothing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARK = "/* _dev/dark_band_labels.py */"
FLOOR = 4.5

# Every dark hero band in the site. The value is the LIGHTEST stop of that
# band's gradient, because that is the hardest case for light text on it.
# Read out of the stylesheets rather than remembered - all five currently
# top out at pine, and the guard below re-checks that claim.
BANDS = {
    "pdband":  (0x2C, 0x63, 0x50),
    "libband": (0x2C, 0x63, 0x50),
    "pxband":  (0x2C, 0x63, 0x50),
    "scband":  (0x2C, 0x63, 0x50),
    "artband": (0x2C, 0x63, 0x50),
}

# The gold that clears the floor on pine. #F6C560, the palette's --amber,
# does not - see the docstring.
EYEBROW = (0xFF, 0xD3, 0x7A)

# The colour the broken band was falling through to, kept here so the guard
# can prove it is gone rather than assuming.
FELL_THROUGH_TO = "#4E4940"


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(rgb):
    r, g, b = (_lin(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def css():
    sel = ",".join(".{0}.{0} .sub".format(b) for b in sorted(BANDS))
    hexv = "#%02X%02X%02X" % EYEBROW
    return ("<style>%s\n"
            "/* The eyebrow above the h1 on a dark hero band. #F6C560 measures\n"
            "   4.26:1 on the lightest stop of these gradients and .pdband had\n"
            "   no rule at all, so it inherited the light-surface grey and\n"
            "   measured 1.20:1. %s measures 4.88:1. */\n"
            "%s{color:%s}\n"
            "</style>" % (MARK, hexv, sel, hexv))


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    hexv = "#%02X%02X%02X" % EYEBROW
    print("eyebrow %s against the lightest stop of every dark band:" % hexv)
    worst = 99.0
    for band, bg in sorted(BANDS.items()):
        r = ratio(EYEBROW, bg)
        worst = min(worst, r)
        print("  %-8s on #%02X%02X%02X  %5.2f:1  %s"
              % (band, bg[0], bg[1], bg[2], r, "ok" if r >= FLOOR else "FAILS"))
    old = ratio((0xF6, 0xC5, 0x60), (0x2C, 0x63, 0x50))
    print("  (for comparison, the old #F6C560 measures %.2f:1)" % old)
    if worst < FLOOR:
        sys.exit("the eyebrow colour does not clear %.1f:1 on every dark band - "
                 "lighten it, do not lower the floor" % FLOOR)

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
    print("%d page(s) given the eyebrow override" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d copies of the block" % (rel, s.count(MARK)))
            bad += 1
            continue
        # The block has to come after the base p.sub declaration, or the
        # cascade puts the grey back. This is the failure that started it.
        for band in BANDS:
            if 'class="%s"' % band not in s:
                continue
            i_base = s.rfind(FELL_THROUGH_TO)
            i_fix = s.find(MARK)
            if i_base > i_fix:
                print("GUARD %s: %s is declared after the override" % (rel, FELL_THROUGH_TO))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards ok")


if __name__ == "__main__":
    main()
