#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rates.html joins the grid, and keeps its own voice.

THE QUESTION THAT WAS ASKED AND NEVER ANSWERED

  "IS THIS PAGE USING NEW DESIGN TEMPLATE FROM PIXEL AND CONCEPTS? SEEMS TO BE
   ITS OWN DESIGN STYLE https://therapistsupport.org/rates.html"

The honest answer is: partly. It takes the shared masthead, the shared footer,
the CSS floors and the In-short card, and then lays its body out on its own
900px measure with a serif display face and a red accent. That was deliberate -
it is a research dossier, and reading it should feel different from using a
calculator.

WHAT IS ACTUALLY WRONG, WHICH IS NOT THE TYPOGRAPHY

Measured at 1440, before this pass:

    the masthead              x = 156
    .drwrap, the article body x = 156   (brought on by _dev/one_grid.py)
    the hero, the gap bar,
    the colophon, the footer  x = 270

So the page disagrees with **itself**. The headline sits 114px to the right of
the article that follows it, and the signature gap bar sits 114px right of the
on-this-page rail directly beneath it. Nobody chose that; it is what happens
when some blocks are centred at 900 and the ones around them are centred at
1180.

WHAT THIS CHANGES

The four stray blocks move onto the same grid as everything else - 1180px, 26px
of padding, and the same two widening steps `_dev/widen.py` gives the masthead.
The reading measure is preserved where it matters by capping the display
headline in `ch` rather than by shrinking its container, which is the same
argument `one_grid.py` makes: the page has one grid, and columns sit inside it.

WHAT THIS DELIBERATELY DOES NOT CHANGE

Not one typographic value. Not the serif display face, not the red accent, not
the gap-bar device, not the colophon's voice. The distinct look is the point of
the page and it survives; what it loses is a misalignment it never meant to
have.

WHY IT NEEDS A BODY CLASS

`.hero` is not unique to this page - `practice-simulator.html` has a `.hero`
too, and there it is a full-bleed band with its own inner container. A bare
`.hero{max-width:1180px}` would have collapsed that band. So this pass adds
`class="ratespage"` to the body and scopes everything to it. The alternative -
guessing which `.hero` was which - is the recurring bug on this project written
into a stylesheet.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = "rates.html"
MARK = "/* _dev/rates_grid.py */"
BODYCLASS = "ratespage"

CANON = 1180
PAD = 26
# must match _dev/widen.py STEP1/STEP2 and _dev/one_grid.py STEPS
STEPS = [(1500, 1320), (1900, 1560)]

# the blocks that were centred at 900 while the page around them was on 1180
# `.sitefoot-in` looked like a fifth. It is a rule with no element - the page
# uses the shared `.ftin` footer, which `_dev/one_grid.py` already handles - and
# the guard below caught it rather than letting a dead selector ship.
STRAYS = [".hero", ".gapbar-wrap", ".colophon"]


def sheet():
    # `.ratespage.ratespage .hero` - doubled, because the 900px rules are in
    # this page's own inline stylesheet and a single class would otherwise tie
    # on specificity and lose on source order.
    sel = ",".join(".%s.%s %s" % (BODYCLASS, BODYCLASS, s) for s in STRAYS)
    o = ["<style>%s" % MARK,
         "/* The four blocks that were centred at 900 while the masthead, the",
         "   footer and the article body were on the 1180 grid. Geometry only -",
         "   this pass changes no typographic value on this page, because the",
         "   serif display face and the red accent are the point of it. */",
         "%s{max-width:%dpx;padding-left:%dpx;padding-right:%dpx;"
         "margin-left:auto;margin-right:auto}" % (sel, CANON, PAD, PAD),
         "/* The measure moves onto the headline itself rather than staying in",
         "   its container - same argument as _dev/one_grid.py. 24ch, not 19:",
         "   19 held the headline to 555px inside a 1128px grid and broke it",
         "   over three lines with 570px of white beside it. */",
         ".%s.%s .hero h1{max-width:24ch}" % (BODYCLASS, BODYCLASS),
         ".%s.%s .gapbar-wrap .gapbar{max-width:none}" % (BODYCLASS, BODYCLASS),
         "/* The gap bar and the on-this-page rail used to be 114px apart",
         "   horizontally, which hid the fact that they are zero pixels apart",
         "   vertically. Aligning them exposed it. */",
         ".%s.%s .gapbar-wrap{margin-bottom:30px}" % (BODYCLASS, BODYCLASS)]
    for at, w in STEPS:
        o.append("@media (min-width:%dpx){%s{max-width:%dpx}}" % (at, sel, w))
    o.append("@media (max-width:640px){%s{padding-left:18px;"
             "padding-right:18px}}" % sel)
    o.append("</style>")
    return "\n".join(o)


def main():
    p = os.path.join(SITE, PAGE)
    if not os.path.exists(p):
        sys.exit("rates_grid: %s is missing" % PAGE)
    s = open(p, encoding="utf-8").read()
    orig = s

    s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)

    # ------------------------------------------------------- the body class
    m = re.search(r"<body([^>]*)>", s)
    if not m:
        sys.exit("rates_grid: no <body> tag")
    attrs = m.group(1)
    if BODYCLASS not in attrs:
        if 'class="' in attrs:
            new = attrs.replace('class="', 'class="%s ' % BODYCLASS, 1)
        else:
            new = attrs + ' class="%s"' % BODYCLASS
        s = s[:m.start()] + "<body%s>" % new + s[m.end():]
        print("  ok       added class=%r to <body>" % BODYCLASS)
    else:
        print("  already  <body> carries class=%r" % BODYCLASS)

    e = s.lower().rfind("</body>")
    if e < 0:
        sys.exit("rates_grid: no </body>")
    s = s[:e] + sheet() + "\n" + s[e:]

    if s != orig:
        open(p, "w", encoding="utf-8").write(s)
    print("  ok       %d block(s) brought onto the grid: %s"
          % (len(STRAYS), ", ".join(STRAYS)))

    # --------------------------------------------------------------- guards
    bad = 0
    s = open(p, encoding="utf-8").read()

    if s.count(MARK) != 1:
        print("GUARD: %d stylesheets" % s.count(MARK)); bad += 1
    if len(re.findall(r'<body[^>]*\b%s\b' % BODYCLASS, s)) != 1:
        print("GUARD: the body class is not on the page exactly once"); bad += 1

    # Every block this pass claims to move must actually be on the page. A
    # renamed block would leave the page half on the grid and half off it,
    # which is the state this pass exists to end.
    for stray in STRAYS:
        if 'class="%s' % stray.lstrip(".") not in s:
            print("GUARD: %s is not on the page. Either it was renamed - "
                  "update STRAYS - or the block is gone." % stray)
            bad += 1

    # The page's own voice must survive. This pass is geometry; if it ever
    # starts changing type, these are the things that would go first.
    for what, needle in (("the serif display face", "Newsreader"),
                         ("the gap-bar device", "gapbar"),
                         ("the colophon", "colophon"),
                         ("the In-short card", "tsshort")):
        if needle not in s:
            print("GUARD: %s is gone from rates.html. This pass changes "
                  "geometry, never typography." % what)
            bad += 1

    # And the body must still be on the grid, or the hero would now be aligned
    # with nothing. `.drwrap` is _dev/one_grid.py's, not this pass's.
    if ".drwrap" not in "".join(re.findall(r"<style>([\s\S]*?)</style>", s)) \
            and not re.search(r'href="css/', s):
        print("GUARD: cannot confirm .drwrap is still styled"); bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - geometry only, and every typographic signature of "
          "the page is still there")


if __name__ == "__main__":
    main()
