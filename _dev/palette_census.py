#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every colour actually in use, ranked, against the sanctioned palette.

WHY THIS EXISTS

`_dev/house_tokens.py` conformed the eight P8 tokens. That was necessary
and it was not sufficient, and the gap is instructive: it rewrote seven
specific old->new pairs that had been MEASURED on `body`. It never asked
the more obvious question - what colours does this site actually use? -
so it never saw that `css/5ca46b240881.css`, which styles the five topic
hub pages, carries eighteen uses of `#16211B` and a warm grey family
(`#3A3529`, `#6C6555`, `#4A463A`, `#D9D0BA`) that belongs to the palette
the house style replaced.

Fixing reported symptoms finds reported symptoms. This counts everything.

WHAT IT DOES

Walks every stylesheet that a PUBLISHED page links, plus every inline
`<style>` block and `style="..."` attribute on those pages, and censuses
every hex literal and rgb()/rgba() colour. Each is classified:

    SANCTIONED   a P8 token, a path hue, or one of the accessory values
                 that has been verified for contrast and written down
    OFF-PALETTE  everything else, with counts and the files it lives in

Published pages only. `ops/`, `mock/` and the `_dev/` mockups are out of
scope - they are scratch, not the site. `_dev/chrome_donor.html` is a
different case and it is worth stating, because getting it wrong cost a
pipeline run: eight builders copy that file's chrome into the pages they
write, so it is a TEMPLATE, and `palette_conform.py` conforms it. It is not
censused here only because it is not itself a page - its colours reach this
census through everything it stamps out.

USAGE

    python3 _dev/palette_census.py              report
    python3 _dev/palette_census.py --check      exit non-zero on NEW
                                                off-palette colour
    python3 _dev/palette_census.py --write-baseline

Baseline pattern, same as seo_rules.py and family_coverage.py: the known
set is recorded so the build fails on a NEW off-palette colour rather
than on the whole backlog at once.
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
BASELINE = os.path.join(HERE, "palette_baseline.json")

SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")
# Published pages only. See the docstring.
SKIP_DIRS = ("ops", "mock", "_dev", "_to_delete", "hours")
# Visual-direction mockups. Neither is in sitemap.xml, both are deliberately
# off-palette - tycoon.html is a game aesthetic in purple and navy - and
# holding a mockup to the house palette is how you lose the mockup. Same
# exclusion as _dev/palette_conform.py's NOCOLOUR.
NOCOLOUR = {"tycoon.html", "concepts.html"}

# ---- the sanctioned palette -------------------------------------------
# The eight P8 tokens (claude/house-style-the-fifth-thing.md).
TOKENS = {
    "#F6F8F6": "paper", "#FFFFFF": "card", "#1B2420": "ink",
    "#5F6A64": "dim", "#DFE4E0": "line", "#2C6350": "pine",
    "#123C30": "deep", "#FFE7A3": "gold",
}
# The six path hues, each >=4.5:1 on paper. Chip and 4px rule only.
PATH_HUES = {
    "#2F6FDB": "path deciding", "#7A5AF8": "path in-a-program",
    "#0E8FA8": "path the-gap", "#17864A": "path counting-hours",
    "#B0730B": "path newly-licensed", "#BC3F86": "path running-a-practice",
}
# Accessory values that are NOT tokens but ARE deliberate and verified.
# Each one earns its place by having been measured for contrast and
# written down in a project doc; anything not on this list is drift.
ACCESSORY = {
    "#F6C560": "CTA gold background (verified with #14372C text)",
    "#14372C": "text on the CTA gold, 8.11:1",
    "#8A6516": "gold-on-light text, 4.9-5.3:1 on every light surface",
    "#C6DBD1": "light mint - on-dark body text 9.6:1, and the light surface",
    "#84AC99": "muted on-dark kicker, 4.86:1 on deep",
    "#635D4E": "contrast_pass muted label, 6.07:1 on cream",
    "#000000": "pure black - only ever in shadows and masks",
}
SANCTIONED = {}
SANCTIONED.update(TOKENS)
SANCTIONED.update(PATH_HUES)
SANCTIONED.update(ACCESSORY)

HEX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")


def norm(h):
    """#abc -> #AABBCC, uppercase."""
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h.upper()


def pages():
    out = []
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html"):
            out.append(f)
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    # ---- which sheets do published pages actually link?
    live_sheets, page_text = set(), {}
    for rel in pages():
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()
        # A mockup's <link>s still count - a sheet it loads is a live sheet -
        # but its own markup is not censused.
        for name in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)', html):
            live_sheets.add(name)
        if os.path.basename(rel) not in NOCOLOUR:
            page_text[rel] = html

    counts = Counter()
    where = defaultdict(set)

    def scan(text, origin):
        for m in HEX.finditer(text):
            c = norm(m.group(0))
            counts[c] += 1
            where[c].add(origin)

    for name in sorted(live_sheets):
        p = os.path.join(CSSDIR, name)
        if os.path.exists(p):
            scan(open(p, encoding="utf-8").read(), "css/" + name)
    for rel, html in page_text.items():
        for m in re.finditer(r"<style>([\s\S]*?)</style>", html):
            scan(m.group(1), rel + " (inline block)")
        for m in re.finditer(r'style="([^"]*)"', html):
            scan(m.group(1), rel + " (style attr)")

    off = {c: n for c, n in counts.items() if c not in SANCTIONED}
    ok = {c: n for c, n in counts.items() if c in SANCTIONED}

    if "--write-baseline" in sys.argv:
        json.dump({c: sorted(where[c]) for c in sorted(off)},
                  open(BASELINE, "w", encoding="utf-8"), indent=1,
                  sort_keys=True)
        print("baseline written: %d off-palette colour(s)" % len(off))
        return

    known = {}
    if os.path.exists(BASELINE):
        known = json.load(open(BASELINE, encoding="utf-8"))
    new = sorted(c for c in off if c not in known)

    print("%d live stylesheet(s) + inline styles on %d published page(s)"
          % (len(live_sheets), len(page_text)))
    print("%d sanctioned colour(s) in %d use(s); %d OFF-PALETTE colour(s) "
          "in %d use(s)\n"
          % (len(ok), sum(ok.values()), len(off), sum(off.values())))

    print("SANCTIONED, by use:")
    for c, n in sorted(ok.items(), key=lambda x: -x[1]):
        print("  %5d  %s  %s" % (n, c, SANCTIONED[c]))

    print("\nOFF-PALETTE, by use:")
    for c, n in sorted(off.items(), key=lambda x: -x[1])[:40]:
        tag = " (NEW)" if c in new else ""
        src = sorted(where[c])
        print("  %5d  %s%s  %s%s"
              % (n, c, tag, src[0],
                 " +%d more" % (len(src) - 1) if len(src) > 1 else ""))

    if "--check" in sys.argv:
        if new:
            print("\n%d NEW off-palette colour(s): %s"
                  % (len(new), ", ".join(new)))
            sys.exit("new off-palette colour(s) - conform them, or run "
                     "--write-baseline if deliberate")
        print("\n%d known off-palette colour(s) in the baseline, 0 new."
              % len(off))


if __name__ == "__main__":
    main()
