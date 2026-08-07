#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give the heroes a palette instead of a monotony and one outlier.

The state this replaces, measured across the site:

  index, practice-simulator, associate, 3,000-hours   pine green, near identical
  tax, grow                                           near-black into the same green
  working-remotely                                    the same green again
  cost-of-living                                      DEEP PURPLE

That is not a system in either direction. Six pages were indistinguishable
from one another and from the site header, which is itself a green gradient,
so a reader could not tell from the top of the screen which tool they were on.
And the seventh was violet under a green header - the user's words on seeing it
were "this green and purple color system awful".

The system this installs. Every hero is a dark gradient whose hue sits on a
single arc from moss through pine to deep sea, 105 degrees to 205 degrees. The
site header is green at roughly 163 degrees and sits in the middle of that arc,
so every hero is a relative of the chrome above it rather than a competitor.
Amber (#F6C560, about 42 degrees) is the only warm colour anywhere and stays
the sole accent, which is what makes a call to action read as one.

  practice-simulator, associate, 3,000-hours   pine    the house colour
  tax, grow                                    ink     near-black into pine
  cost-of-living                               teal    184 degrees
  working-remotely                             sea     205 degrees, the one blue

Two pages change. Cost-of-living loses the purple; working-remotely picks up
the coolest end of the arc, because it is the page about practising from
somewhere else and it was previously impossible to tell apart from three other
green pages.

How the purple is removed matters. Not repainted by hand - HUE-ROTATED. Each
of the six violet values on that page is converted to HLS, its hue moved from
about 251 degrees to 184, and its lightness and saturation left exactly as they
were. Every contrast relationship the page already had is preserved by
construction: the pale lilac stays as pale against white as it was, the deep
one stays as deep. Choosing six new colours by eye would have meant re-checking
six contrast pairs and getting one of them wrong.

Idempotent: after one run there are no source colours left to match.
"""
import os, re, sys, colorsys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

# hue window that counts as "violet" for the guard below
VIOLET = (230.0, 310.0)
TEAL_HUE = 184.0


def rot(hexstr, target_hue):
    """Move a colour's hue, keeping its lightness and saturation."""
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    _, light, sat = colorsys.rgb_to_hls(r, g, b)
    r2, g2, b2 = colorsys.hls_to_rgb(target_hue / 360.0, light, sat)
    return "#%02x%02x%02x" % tuple(round(v * 255) for v in (r2, g2, b2))


def hue_of(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, _, s = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, s


# ---- page 1: cost-of-living, violet -> teal, by rotation
COLA = "therapist-cost-of-living-california.html"

# ---- page 2: working-remotely, house green -> deep sea, the one blue hero
RW = "therapist-working-remotely-california.html"
RW_OLD = "linear-gradient(160deg,#2C6350 0%,#1F4C3C 70%,#1A4234 100%)"
RW_NEW = "linear-gradient(160deg,#1F5573 0%,#173F5A 70%,#13324A 100%)"


def do_cola():
    path = os.path.join(SITE, COLA)
    s = open(path, encoding="utf-8").read()
    styles = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    targets = {}
    for m in re.finditer(r"#([0-9A-Fa-f]{6})\b", styles):
        val = "#" + m.group(1).lower()
        hue, sat = hue_of(val)
        if VIOLET[0] <= hue <= VIOLET[1] and sat > 0.06:
            targets[val] = rot(val, TEAL_HUE)
    if not targets:
        print("%-44s no violet left" % COLA)
        return 0
    n = 0
    for old, new in targets.items():
        # case-insensitive, because the file mixes #4B3B93 and #4b3b93
        s, k = re.subn(re.escape(old), new, s, flags=re.I)
        n += k
        print("    %s -> %s   x%d" % (old, new, k))
    open(path, "w", encoding="utf-8").write(s)
    print("%-44s %d violet value(s), %d occurrence(s) rotated to teal"
          % (COLA, len(targets), n))
    return 1


def do_rw():
    path = os.path.join(SITE, RW)
    s = open(path, encoding="utf-8").read()
    if RW_NEW in s:
        print("%-44s already deep sea" % RW)
        return 0
    if s.count(RW_OLD) != 1:
        print("%-44s hero gradient matched %d times, skipped"
              % (RW, s.count(RW_OLD)))
        return 0
    open(path, "w", encoding="utf-8").write(s.replace(RW_OLD, RW_NEW, 1))
    print("%-44s hero -> deep sea" % RW)
    return 1


def main():
    changed = do_cola() + do_rw()

    # ---- guards
    bad = 0
    s = open(os.path.join(SITE, COLA), encoding="utf-8").read()
    styles = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    left = set()
    for m in re.finditer(r"#([0-9A-Fa-f]{6})\b", styles):
        v = "#" + m.group(1).lower()
        hue, sat = hue_of(v)
        if VIOLET[0] <= hue <= VIOLET[1] and sat > 0.06:
            left.add(v)
    if left:
        print("GUARD %s: violet survives: %s" % (COLA, ", ".join(sorted(left))))
        bad += 1

    # every hero hue must land on the arc, so no page fights the header
    for f, sel in ((COLA, r"\.clhero"), (RW, r"\.rwhero")):
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        st = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
        m = re.search(sel + r"\s*\{([^}]*)\}", st)
        if not m:
            print("GUARD %s: hero rule not found" % f); bad += 1; continue
        hues = [hue_of("#" + h)[0] for h in re.findall(r"#([0-9A-Fa-f]{6})", m.group(1))]
        # Amber is deliberately exempt. It is the site's single warm accent and
        # appears inside hero rules as a highlight; the first version of this
        # guard flagged working-remotely for a hue of 45 degrees, which was the
        # accent doing exactly its job. The rule is about the BACKGROUND arc,
        # not about banning warmth.
        off = [h for h in hues
               if not (100.0 <= h <= 210.0) and not (28.0 <= h <= 58.0)]
        if off:
            print("GUARD %s: hero hue(s) off the arc: %s"
                  % (f, ", ".join("%.0f" % h for h in off))); bad += 1

    for f in (COLA, RW):
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if s.count("<h1") != 1:
            print("GUARD %s: %d h1" % (f, s.count("<h1"))); bad += 1

    if bad:
        sys.exit("hero_palette: %d guard failure(s)" % bad)
    print("%d page(s) recoloured · guards clean" % changed)


if __name__ == "__main__":
    main()
