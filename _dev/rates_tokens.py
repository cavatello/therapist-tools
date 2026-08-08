#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two colours on rates.html that a later :root block quietly redefined.

rates.html carries its own palette, and the pixel restyle pass appended a SECOND
`:root` block to it - the design-system tokens, copied rather than imported so
the page stays standalone. Copying them was right. The collision was not
noticed: both blocks define `--amber`, and the second one wins.

    :root{ ... --amber:#C98B4B }   the page's own accent, for cream surfaces
    :root{ ... --amber:#FFE3B8 }   the design system's amber, for DARK bands

`.part-num` - the roman numerals that mark each part of the essay - is written
`color:var(--amber)` and sits on cream. It was authored against the first value
and is now painted with the second, so the section markers render at 1.18:1:
pale apricot on off-white, effectively invisible. Nothing failed; a token moved
underneath a rule that was already correct.

The fix is not to unpick the two :root blocks - the design tokens belong there,
and the next pass would put them back. It is to stop `.part-num` depending on a
name whose meaning is contested on this page, and give it a literal that clears
the floor on cream. #8A6023 is not invented for this: it is already in the
page's own pixel artwork, as the dark amber in the SVG.

Second value, unrelated cause, same shape: #9C968A at 13px - the part deks and
the italic disclaimer - reads 2.79:1. The earlier rates_contrast.py pass caught
three near-neighbours (#9C8F72, #8C8471, #7C766A) and missed this one. It goes
to #635E53, the muted grey the rest of the site already standardised on.

Idempotent - both replacements are already-passing values, so a second run has
nothing left to find.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "rates.html")
FLOOR = 4.5

SURFACES = {
    "card white": "#FFFFFF",
    "cream":      "#FBF9F3",
    "paper":      "#FCFAF2",
}

# The literal that replaces var(--amber) for the part numerals, and the muted
# grey that the rest of the site uses.
AMBER_INK = "#8A6023"
MUTED = "#635E53"


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


def main():
    if not os.path.exists(PAGE):
        sys.exit("rates_tokens: rates.html is not there")

    print("replacements, measured:")
    worst = 99.0
    for name, colour in (("part numeral", AMBER_INK), ("muted", MUTED)):
        for s, bg in SURFACES.items():
            r = ratio(colour, bg)
            worst = min(worst, r)
            print("  %-13s %s on %-10s %5.2f:1  %s"
                  % (name, colour, s, r, "ok" if r >= FLOOR else "FAILS"))
    if worst < FLOOR:
        sys.exit("a replacement does not clear %.1f:1" % FLOOR)

    s = open(PAGE, encoding="utf-8").read()
    orig = s
    counts = {}

    # .part-num: replace the token reference inside its own rule only. Other
    # users of var(--amber) on this page sit on dark bands, where #FFE3B8 is
    # the right answer and must stay.
    def fix_partnum(m):
        block = m.group(0)
        if "var(--amber)" not in block:
            return block
        counts["part-num"] = counts.get("part-num", 0) + 1
        return block.replace("var(--amber)", AMBER_INK)

    s2 = re.sub(r"\.part-num\s*\{[^}]*\}", fix_partnum, s)
    s = s2

    n = len(re.findall(r"#9C968A", s, re.I))
    if n:
        s = re.sub(r"#9C968A", MUTED, s, flags=re.I)
        counts["#9C968A"] = n

    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)
    print("\n%s" % (", ".join("%s x%d" % kv for kv in counts.items())
                    or "nothing to change"))

    s = open(PAGE, encoding="utf-8").read()
    bad = 0
    m = re.search(r"\.part-num\s*\{[^}]*\}", s)
    if not m:
        print("GUARD: .part-num rule has gone missing")
        bad += 1
    elif "var(--amber)" in m.group(0):
        print("GUARD: .part-num still resolves through --amber")
        bad += 1
    if re.search(r"#9C968A", s, re.I):
        print("GUARD: #9C968A survives")
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
