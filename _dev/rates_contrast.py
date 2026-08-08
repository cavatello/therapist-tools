#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Raise four colours in the rates.html palette until they clear 4.5:1.

rates.html is a standalone editorial page with its own palette, so the sitewide
label override in _dev/contrast_pass.py does not reach it. A headless pass over
the page measured fifteen text nodes under the floor, and they came down to
exactly four hex values:

    --muted   #7C766A   4.28:1   the deck, the part deks, table headers
              #9C8F72   3.03:1   table cells and the figures inside them
              #8C8471   3.55:1   small print
    --pine    #3F9577   3.14:1   the accent, used as TEXT on a tinted chip

The last one is the interesting case. #3F9577 is a fine colour for a bar, a rule
or a border — a large block of it against paper is perfectly visible, and the
gap bars on this page use it exactly that way. It fails only where it is used
for TEXT, and it fails hardest at 10px on the pale green chip, which is where
the ratio drops to 3.14:1. So the fix is not "change the green": it is to use
the site's darker pine, #2C6350, wherever the green carries words. The bars keep
the colour they were designed with.

Every replacement is checked here against the surfaces the page actually uses,
and the pass exits non-zero rather than shipping one that does not clear.

Idempotent: the replacements are already-passing colours, so a second run finds
nothing left to change.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "rates.html")
FLOOR = 4.5

# The surfaces these colours actually sit on, read off the rendered page.
SURFACES = {
    "card white": (0xFF, 0xFF, 0xFF),
    "cream":      (0xFB, 0xF9, 0xF3),
    "paper":      (0xFC, 0xFA, 0xF2),
    "pine chip":  (0xE6, 0xF1, 0xEB),
}

SWAPS = [
    # (old, new, the surfaces it must clear)
    ("#7C766A", "#635E53", ("card white", "cream", "paper")),
    ("#9C8F72", "#6E6553", ("card white", "cream", "paper")),
    ("#8C8471", "#67604F", ("card white", "cream", "paper")),
    # Text only. The gap bars keep #3F9577 - see the module docstring.
    ("#3F9577", "#2C6350", ("card white", "cream", "paper", "pine chip")),
]

# Where the green must NOT be swapped, because it is a block of colour rather
# than a letterform. Matched on the declaration, not the value.
KEEP_GREEN = re.compile(
    r"(background|border|fill|stroke|box-shadow|outline)[^;:]*:[^;]*#3F9577",
    re.I)


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(rgb):
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def main():
    if not os.path.exists(PAGE):
        sys.exit("rates_contrast: rates.html is not there")

    print("replacements, measured:")
    worst = 99.0
    for old, new, surfaces in SWAPS:
        for s in surfaces:
            r = ratio(hx(new), SURFACES[s])
            worst = min(worst, r)
            flag = "ok" if r >= FLOOR else "FAILS"
            print("  %s -> %s  on %-10s %5.2f:1  %s" % (old, new, s, r, flag))
    if worst < FLOOR:
        sys.exit("a replacement does not clear %.1f:1 - darken it" % FLOOR)

    s = open(PAGE, encoding="utf-8").read()
    orig = s
    counts = {}
    for old, new, _sf in SWAPS:
        if old != "#3F9577":
            n = len(re.findall(re.escape(old), s, re.I))
            if n:
                s = re.sub(re.escape(old), new, s, flags=re.I)
                counts[old] = n
            continue
        # The green: swap only where it is not painting a surface.
        out, last, n = [], 0, 0
        for m in re.finditer(r"#3F9577", s, re.I):
            line_start = s.rfind(";", 0, m.start()) + 1
            line_start = max(line_start, s.rfind("{", 0, m.start()) + 1)
            decl = s[line_start:m.end() + 1]
            out.append(s[last:m.start()])
            if KEEP_GREEN.search(decl):
                out.append(m.group(0))
            else:
                out.append(new)
                n += 1
            last = m.end()
        out.append(s[last:])
        s = "".join(out)
        if n:
            counts[old] = n

    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)
    print("\n%s" % (", ".join("%s x%d" % (k, v) for k, v in counts.items())
                    or "nothing to change"))

    bad = 0
    s = open(PAGE, encoding="utf-8").read()
    for old, _new, _sf in SWAPS:
        if old == "#3F9577":
            continue
        if re.search(re.escape(old), s, re.I):
            print("GUARD: %s survives" % old)
            bad += 1
    # the green may survive, but only on a surface declaration
    for m in re.finditer(r"#3F9577", s, re.I):
        a = max(s.rfind(";", 0, m.start()), s.rfind("{", 0, m.start())) + 1
        if not KEEP_GREEN.search(s[a:m.end() + 1]):
            print("GUARD: #3F9577 still used for text near %r"
                  % s[max(0, m.start() - 60):m.end()][-60:])
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - nothing under %.1f:1 left in this palette" % FLOOR)


if __name__ == "__main__":
    main()
