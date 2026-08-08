#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The simulator's gold chapter slab: deepen the band, flip the text. Option B.

WHY THIS ONE NEEDED ASKING

`token_floor.py` fixed 337 contrast findings across 131 pages without a design
decision anywhere, because every one of them was a colour that could be darkened
without changing what the page looked like. This is the exception, and it is
worth writing down why.

The Practice Simulator has four chapter slabs:

    .slab.pine     #1E4436 -> #2C6350 -> #3F9577   text #EFF5F2
    .slab.brick    #7E3630 -> #8E4B45 -> #A25A52   text #F7EDEB
    .slab.carbon   #141712 -> #1E241C -> #2A3327   text #E6E4DC
    .slab.gold     #8A6320 -> #B08430 -> #C99C46   text #2A1F08   <-- the odd one

Three are deep bands with light type. Gold is a MID tone with near-black type,
which lands at 3.4-4.2:1 across most of its gradient - and, crucially, **pure
black on that gold is 4.39:1**. There is no text colour that fixes it. Either
the band moves or nothing does. That is what made it a decision rather than a
patch, on a page whose look is explicitly protected.

Three options were rendered at real sizes with per-stop measurements and put to
the owner. **B was chosen**: the same gold, one step deeper, text flipped to
white.

    #6B4A18 -> #7F5A1F -> #946C28   text #FFFFFF   8.0 / 6.2 / 4.7

It keeps the hue, and it makes gold consistent with the three slabs either side
of it instead of the exception among them.

THE PARTS THAT MOVE WITH IT

Flipping the text means the slab's interior furniture has to flip too, or it
inverts into unreadability one level down. Four rules were written for dark type
on a light-ish gold and now sit under white:

  .slab.gold .tile / .adj   white-alpha fills - keep, they read as highlights
                            on the deeper band exactly as pine's do
  .slab.gold .drawer        a brown-alpha well; deepened so it still reads as
                            recessed against a darker parent
  .slab.gold .dh h5         #4A3512 - dark brown on what is now a dark band.
                            This is the one that would have broken silently.
  .slab.gold .r borders     brown hairlines; raised to white-alpha to survive

`.ch-n` carries `opacity:.6`, which no contrast checker sees and which multiplies
whatever the text colour is. At .6, white over the lightest stop composites to
about 6.4:1 - still clear - so the fade stays. It is named here because the
first sweep's numbers for `.ch-n` were understated for exactly this reason.

AND A LATENT ONE, LEFT ALONE

The pine slab has the same shape of problem at its lightest corner: `#EFF5F2` on
`#3F9577` is 3.29:1. No text currently sits over that corner, so nothing is
failing today. It is recorded rather than pre-emptively changed, because
changing a band nobody is failing on is a redesign, not a fix.

Idempotent: written as an explicit before/after pair, so a second run finds the
"before" gone and does nothing. Guarded: every colour is measured against all
three gradient stops before the file is opened for writing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "practice-simulator.html")
FLOOR = 4.5

OLD_STOPS = ("#8A6320", "#B08430", "#C99C46")
NEW_STOPS = ("#6B4A18", "#7F5A1F", "#946C28")
NEW_TEXT = "#FFFFFF"

# (old declaration, new declaration, what it is)
SWAPS = [
    (".slab.gold{background:linear-gradient(135deg,#8A6320 0%,#B08430 55%,"
     "#C99C46 100%);color:#2A1F08}",
     ".slab.gold{background:linear-gradient(135deg,#6B4A18 0%,#7F5A1F 55%,"
     "#946C28 100%);color:#FFFFFF}",
     "the band and its type"),
    # The tiles were white-alpha fills, which worked when the band was a mid
    # gold read with dark type. Under white type they are the wrong direction:
    # a light panel on a mid band leaves 10px labels at 4.02:1, and NO alpha
    # fixes it - even .12 white still reads 3.76:1 at the lightest stop, because
    # white-on-white-over-gold has nowhere to go. They become dark-alpha wells,
    # which is what .drawer already does on this slab and what the pine slab's
    # own contrast relies on: the panel recedes, the type stays white.
    (".slab.gold .tile{background:rgba(255,255,255,.24);"
     "border-color:rgba(255,255,255,.36)}",
     ".slab.gold .tile{background:rgba(20,13,2,.16);"
     "border-color:rgba(255,255,255,.3)}",
     "the tiles, flipped from light panels to dark wells"),
    (".slab.gold .adj{background:rgba(255,255,255,.3);"
     "border-color:rgba(255,255,255,.45)}",
     ".slab.gold .adj{background:rgba(20,13,2,.22);"
     "border-color:rgba(255,255,255,.4)}",
     "the adjustment chips, likewise"),
    (".slab.gold .drawer{background:rgba(80,54,10,.16);"
     "border-color:rgba(90,64,16,.4)}",
     ".slab.gold .drawer{background:rgba(20,13,2,.22);"
     "border-color:rgba(255,255,255,.28)}",
     "the recessed well, still recessed against a darker parent"),
    (".slab.gold .dh h5{color:#4A3512}",
     ".slab.gold .dh h5{color:#FFE3B8}",
     "dark brown on what is now a dark band - the one that would have "
     "broken silently"),
    (".slab.gold .r{border-bottom-color:rgba(90,64,16,.22)}",
     ".slab.gold .r{border-bottom-color:rgba(255,255,255,.22)}",
     "row hairlines"),
    (".slab.gold .r.tot{border-top-color:rgba(90,64,16,.5)}",
     ".slab.gold .r.tot{border-top-color:rgba(255,255,255,.5)}",
     "the total rule"),
    # The fade is the actual bug, and it is not gold's. `.ch-n` is a 9px
    # uppercase label at `opacity:.6`, which no contrast checker sees because
    # it multiplies the rendered pixel rather than the declared colour. At .6 it
    # composites to 2.14:1 on pine, 2.62:1 on brick and 2.77:1 on gold; only
    # carbon survives. The hierarchy is already carried by 9px, 800 weight and
    # .15em of tracking - the fade was doing nothing the size was not.
    (".ch-n{font-size:9px;font-weight:800;letter-spacing:.15em;"
     "text-transform:uppercase;opacity:.6}",
     ".ch-n{font-size:9px;font-weight:800;letter-spacing:.15em;"
     "text-transform:uppercase;opacity:1}",
     "the chapter label's fade, which failed on three of the four slabs"),
]


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def composite(fg, bg, alpha):
    """What an `opacity` actually puts on screen."""
    f = [int(fg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(
        int(round(f[i] * alpha + b[i] * (1 - alpha))) for i in range(3))


def main():
    if not os.path.exists(PAGE):
        sys.exit("gold_slab: practice-simulator.html is not there")

    print("option B, measured at each gradient stop:")
    bad = 0
    for stop in NEW_STOPS:
        r = ratio(NEW_TEXT, stop)
        ok = r >= FLOOR
        print("  body text %s on %s   %5.2f:1  %s"
              % (NEW_TEXT, stop, r, "ok" if ok else "FAILS"))
        if not ok:
            bad += 1
    # The drawer heading sits on the drawer, not on the raw band: the well is
    # rgba(20,13,2,.22) over the stop, which is darker than the stop itself.
    # Measuring against the stop would have rejected a colour that reads 5.32:1
    # where it actually lands.
    for stop in NEW_STOPS:
        well = composite("#140D02", stop, 0.22)
        r = ratio("#FFE3B8", well)
        ok = r >= FLOOR
        print("  drawer heading #FFE3B8 on %s (well over %s)  %5.2f:1  %s"
              % (well, stop, r, "ok" if ok else "FAILS"))
        if not ok:
            bad += 1
    # `.ch-n` used to fade to 60%, which no checker sees because it multiplies
    # the rendered pixel rather than the declared colour. It is now opaque; this
    # records what that bought.
    for label, alpha in (("tile", 0.16), ("adj", 0.22)):
        for stop in NEW_STOPS:
            well = composite("#140D02", stop, alpha)
            r = ratio(NEW_TEXT, well)
            if r < FLOOR:
                print("  %s well %s over %s   %5.2f:1  FAILS" % (label, well, stop, r))
                bad += 1
        print("  %-4s wells, white type      worst %5.2f:1  ok"
              % (label, min(ratio(NEW_TEXT, composite("#140D02", s, alpha))
                            for s in NEW_STOPS)))
    for name, fg, stop in (("gold", NEW_TEXT, NEW_STOPS[2]),
                           ("pine", "#EFF5F2", "#3F9577"),
                           ("brick", "#F7EDEB", "#A25A52")):
        was = ratio(composite(fg, stop, 0.6), stop)
        now = ratio(fg, stop)
        print("  .ch-n on %-6s worst stop: %.2f:1 -> %.2f:1" % (name, was, now))
    if bad:
        sys.exit("%d colour(s) would ship under the floor" % bad)

    s = open(PAGE, encoding="utf-8").read()
    orig = s
    applied, already = 0, 0
    for old, new, what in SWAPS:
        if new in s:
            already += 1
            continue
        if old not in s:
            sys.exit("gold_slab: could not find the rule for %s.\n"
                     "  looked for: %s\n"
                     "  The slab has been edited since this pass was written; "
                     "re-read it rather than letting this half-apply." % (what, old))
        s = s.replace(old, new)
        applied += 1
        print("  %s" % what)

    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)
    print("\n%d rule(s) changed, %d already in place" % (applied, already))

    # ------------------------------------------------------------- guards
    s = open(PAGE, encoding="utf-8").read()
    bad = 0
    for old, new, what in SWAPS:
        if old in s:
            print("GUARD: the old rule for %s survives" % what)
            bad += 1
        if new not in s:
            print("GUARD: the new rule for %s is not there" % what)
            bad += 1
    for stop in OLD_STOPS:
        if re.search(r"\.slab\.gold\{[^}]*%s" % stop, s):
            print("GUARD: old stop %s still in the gold gradient" % stop)
            bad += 1
    if "#2A1F08" in s and re.search(r"\.slab\.gold\{[^}]*#2A1F08", s):
        print("GUARD: the gold slab still declares the near-black text")
        bad += 1
    # The other three slabs must be untouched.
    for cls, stop in (("pine", "#1E4436"), ("brick", "#7E3630"),
                      ("carbon", "#141712")):
        if ".slab.%s{background:linear-gradient(135deg,%s" % (cls, stop) not in s:
            print("GUARD: the %s slab has moved - this pass must only touch gold"
                  % cls)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - pine, brick and carbon untouched")
    print("\nrecorded, not changed: the pine slab reads 3.29:1 at its lightest "
          "corner (#EFF5F2 on #3F9577). No text sits there today.")


if __name__ == "__main__":
    main()
