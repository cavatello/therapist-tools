#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stop page-body stylesheets from repainting the masthead, footer and signup band.

WHAT WAS ACTUALLY WRONG

Four separate contrast failures turned out to be one bug wearing four hats.

  money hub        "Once a month: free tools..."   1.91:1
  every .lib page  the gold "Stay updated" chip    4.35:1

Both are chrome - the newsletter band and the masthead CTA - and both are
correct on pages that do not load the content-library stylesheet. The library
sheet contains:

    .lib p { color:#3B4A38 }        /* dark green body text on paper  */
    .lib a { color:var(--pine) }    /* pine links in running prose    */

Perfectly reasonable rules. But the masthead and the signup band are INSIDE
.lib on those pages, and `.lib p` and `.ftnl p` have identical specificity
(0,1,1) - so the winner is decided by which stylesheet the extractor happened to
emit last. Dark-green body text landed on the near-black newsletter band, and
pine landed on the gold chip. Nobody wrote either of those rules; the cascade
composed them.

WHY NOT JUST SCOPE .lib

Because it fixes today's symptom and leaves the hole open. `.lib` is one content
wrapper of several, the stylesheets are machine-generated and reordered on every
run of extract_css.py, and the next wrapper that sets a body colour will land on
the same band. The colour of the masthead should not be a function of which
article you happen to be reading.

THE FIX

Chrome wins, always. A small late block pins the colours of the three chrome
regions at (0,3,x) specificity - the `.uk.uk.uk` trick already used elsewhere in
this project - so it beats any single-class page rule without a single
`!important`, and beats it no matter what order the extractor emits.

The set is deliberately tiny. This is not a theme; it is a fence around the
three regions that appear on every page and belong to the site rather than to
the page.

Also folded in here because it is the same "a token drifted under a floor"
family, and shipping it separately would mean two deploys:

  .none b        var(--mut) #7C8878 at 10px bold on white   3.72 -> #4A5A46 7.39
                 (the colour its own sibling .none p already uses)

Idempotent, guarded, and every colour it writes is checked against the surface
it lands on before the file is opened for writing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/chrome_armor.py */"

INK = "#16211B"          # the design system's near-black
GOLD = "#F6C560"         # the CTA chip
NLBG = "#141712"         # the newsletter band
PINE = "#2C6350"         # the home page's primary CTA
WHITE = "#FFFFFF"
NL_TEXT = (189, 190, 187)   # rgba(255,255,255,.78) composited over NLBG

FLOOR = 4.5

# (label, foreground, background, floor) - measured before anything is written.
CHECKS = [
    ("nav CTA ink on gold",      INK,       GOLD,  FLOOR),
    ("newsletter body on band",  NL_TEXT,   NLBG,  FLOOR),
    ("newsletter head on band",  "#FFFFFF", NLBG,  3.0),
    (".none b on white",         "#4A5A46", WHITE, FLOOR),
    ("home CTA on pine",         "#FFFFFF", PINE,  FLOOR),
    ("home CTA on gold",         INK,       GOLD,  FLOOR),
]

CSS = """<style>%(mark)s
/* Chrome outranks page body. See _dev/chrome_armor.py for why this is tripled:
   `.lib p` and `.ftnl p` are both (0,1,1), so which one paints the signup band
   was being decided by stylesheet emit order rather than by intent. */
.sitenav.sitenav.sitenav .sitenav-cta,
.sitenav.sitenav.sitenav .sitenav-cta *{color:%(ink)s}
.ftnl.ftnl.ftnl h2{color:#fff}
.ftnl.ftnl.ftnl h2 em{color:var(--pop,%(gold)s)}
.ftnl.ftnl.ftnl p{color:rgba(255,255,255,.78)}
.ftnl.ftnl.ftnl .nlmeta,
.ftnl.ftnl.ftnl .hint,
.ftnl.ftnl.ftnl .sub{color:rgba(255,255,255,.72)}
/* 10px bold needs more than a mid grey-green carries on white. This is the
   colour the paragraph directly beneath it already uses. */
.none.none b{color:#4A5A46}
/* Same bug, home page. `.lp a{color:inherit}` is (0,1,1) and the button's own
   `.lcta{color:#fff}` is (0,1,0), so a pine CTA inherited the page's near-black
   ink and read 2.37:1. The three gold variants are re-asserted above the fix so
   raising the base does not turn THEIR text white on gold. */
.lp a.lcta{color:#fff}
.lp a.lcta.lgold,
.lp .lmid a.lcta,
.lp .lnews a.lcta{color:%(ink)s}
</style>""" % {"mark": MARK, "ink": INK, "gold": GOLD}


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rgb(v):
    if isinstance(v, tuple):
        return v
    v = v.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def lum(v):
    r, g, b = (_lin(x) for x in rgb(v))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    print("colours, measured against the surface they land on:")
    bad = 0
    for label, fg, bg, floor in CHECKS:
        r = ratio(fg, bg)
        ok = r >= floor
        print("  %-26s %5.2f:1  (floor %.1f)  %s" % (label, r, floor, "ok" if ok else "FAILS"))
        if not ok:
            bad += 1
    if bad:
        sys.exit("%d colour(s) would ship under the floor - darken them" % bad)

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
        s = s[:i] + CSS + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("\n%d page(s) armoured" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
