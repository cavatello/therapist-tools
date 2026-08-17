#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Typography, counted: every face, every size, every radius, every gradient.

WHY THIS EXISTS

`palette_census.py` counted colour and found 346 of them where the house
style names eight. The same question had never been asked of type, and the
answer is the same shape:

    5 typefaces          Fraunces, Inter, IBM Plex Mono and Bricolage
                         Grotesque on 241 pages each, plus Archivo as a
                         fallback in every pagekit stack - and ten custom
                         properties pointing at four faces, including a
                         duplicated `--hs-*` set
    92 font sizes        from 7.5px to 66px, in 0.1px steps in places. Forty
                         two of them are not a whole or half pixel.
                         `16.5px`, the house body metric, appears 23 times;
                         `15px` appears 112 and `14px` 96
    20 radii             including `999px` seventy times, against a house
                         style that says "no pill buttons"
    123 gradients        over 28 sources, against a house style that says
                         "no gradients from anywhere"

None of that is a bug on its own. All of it together is why a reader moving
between two pages of the same site can see that something changed and not be
able to say what.

WHAT IT REPORTS, AND WHICH PART IS A REAL FAULT

Three of the four are drift: a backlog to be conformed deliberately, with a
baseline so it cannot grow while that happens. The fourth is a live defect
and it is worth stating separately:

    USED BUT NOT LOADED   a page whose CSS asks for a face the page never
                          links. The browser silently renders the fallback,
                          so the page ships in a face nobody chose. This is
                          invisible to every check that reads CSS without
                          also reading the <link>s.
    LOADED BUT NOT USED   the reverse: a webfont downloaded on a page that
                          never sets it. Costs a request and a render delay
                          on every visit and changes nothing on screen.

Both need the *pair* - what a page loads AND what its own sheets and inline
blocks declare - which is why this walks per page rather than over `css/`.

SCOPE

Published pages, `ops/`, `mock/` and `_dev/` excluded, and the two
visual-direction mockups (`tycoon.html`, `concepts.html`) excluded from the
face rules for the same reason `palette_conform.py` leaves their colours
alone: a mockup exists to be different. Their sizes and radii still count -
a mockup is allowed its own face, not its own arbitrary 0.1px steps.

USAGE

    python3 _dev/type_census.py                 report
    python3 _dev/type_census.py --check         exit non-zero on NEW drift
    python3 _dev/type_census.py --write-baseline

Baseline pattern, as in `seo_rules.py`, `family_coverage.py` and
`palette_census.py`: the known set is recorded so the build fails on a new
typeface, a new size, a new radius or a new gradient rather than on the
whole backlog at once.
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
BASELINE = os.path.join(HERE, "type_baseline.json")

SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
NOFACE = {"tycoon.html", "concepts.html"}

# Faces the house style and the built site actually use. Anything else is a
# fifth face, which is a decision, not a default.
#   Inter    the body face P8 names
#   Fraunces the display serif every family except pagekit sets headings in
#   Bricolage Grotesque   pagekit's display face - the OTHER display face,
#            recorded here because it is on all 242 pages and in every
#            pagekit hero, and unpicking that is a design decision rather
#            than a cleanup
#   IBM Plex Mono   figures, labels, kickers
HOUSE_FACES = {"inter", "fraunces", "bricolage grotesque", "ibm plex mono"}
# Generic families and stack fallbacks are not faces.
GENERIC = {"system-ui", "sans-serif", "serif", "monospace", "ui-monospace",
           "ui-sans-serif", "ui-serif", "cursive", "fantasy", "inherit",
           "initial", "unset", "georgia", "arial", "helvetica",
           "helvetica neue", "times", "times new roman", "courier",
           "courier new", "segoe ui", "roboto", "menlo", "monaco",
           "consolas", "liberation mono", "sf mono", "apple color emoji",
           "-apple-system", "blinkmacsystemfont", "emoji", "noto color emoji",
           "segoe ui emoji", "segoe ui symbol", "arial narrow",
           "sfmono-regular", "dejavu sans mono", "lucida console",
           "andale mono", "cambria", "palatino", "book antiqua",
           "trebuchet ms", "verdana", "tahoma", "impact", "charter",
           "iowan old style", "seravek", "optima", "avenir",
           "avenir next", "gill sans", "futura"}

FACE = re.compile(r"font-family\s*:\s*([^;}]+)")
SIZE = re.compile(r"font-size\s*:\s*([0-9.]+)px")
RAD = re.compile(r"border-radius\s*:\s*([0-9.]+)px")
GRAD = re.compile(r"(?:linear|radial|conic)-gradient\s*\(")
GFONT = re.compile(r"fonts\.googleapis\.com/css2\?([^\"']+)")
FAMPARAM = re.compile(r"family=([^&:]+)")


def bucket(fn):
    """A stable identity for a stylesheet. See the note at its use."""
    return ("css/<content-addressed>" if re.fullmatch(r"[0-9a-f]{12}", fn[:-4])
            else "css/" + fn)


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


def _names(decl):
    """The stack, cleaned, in order. Escaped quotes and !important out."""
    out = []
    for part in decl.split(","):
        name = re.sub(r'[\\"\']', "", part)
        name = re.sub(r"!\s*important", "", name).strip().lower()
        if not name or name.startswith("var("):
            continue
        out.append(name)
    return out


def declared(text):
    """Every real face named anywhere in a font-family declaration."""
    out = set()
    for m in FACE.finditer(text):
        for name in _names(m.group(1)):
            if name not in GENERIC:
                out.add(name)
    return out


def primary(text):
    """Only the FIRST real face of each stack.

    This distinction is the whole value of the loaded/used pair. `Archivo`
    is declared on 240 pages and loaded on almost none of them - and that
    is not a fault, because every one of those declarations reads
    `'Bricolage Grotesque','Archivo',Inter,...`, so Archivo is a fallback
    behind a face that DOES load and will never render. Only a face at the
    head of its stack is a face the page has actually asked for.
    """
    out = set()
    for m in FACE.finditer(text):
        for name in _names(m.group(1)):
            if name not in GENERIC:
                out.add(name)
            break
    return out


def main():
    sheet = {}
    for fn in sorted(os.listdir(CSSDIR)):
        if fn.endswith(".css"):
            sheet[fn] = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()

    faces = Counter()
    sizes = Counter()
    radii = Counter()
    grads = Counter()
    used_unloaded = defaultdict(set)
    loaded_unused = defaultdict(set)
    outside = defaultdict(set)          # a face that is not a house face

    # Sizes, radii and gradients are counted once per SOURCE - each
    # stylesheet once, each page's own inline blocks once - not once per
    # page that happens to link a shared sheet. Otherwise one declaration
    # in house.css reads as 242 of them.
    for fn, body in sheet.items():
        for m in SIZE.finditer(body):
            sizes[float(m.group(1))] += 1
        for m in RAD.finditer(body):
            radii[float(m.group(1))] += 1
        for _m in GRAD.finditer(body):
            # Content-addressed sheets are RENAMED whenever their bytes
            # change - palette_conform.py rewrites one and its filename
            # becomes the sha1 of the new contents - so keying a baseline on
            # `css/<hash>.css` records a name that is guaranteed to be wrong
            # by the next build. This cost a red build: the check reported
            # "new gradient on css/126048de4cb8.css" when nothing had
            # gained a gradient, only a name. Hashed sheets collapse to one
            # bucket; a hand-authored sheet keeps its name, because that
            # name is stable.
            grads[bucket(fn)] += 1

    for rel in pages():
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()
        base = os.path.basename(rel)
        own = "\n".join(m.group(1) for m in
                        re.finditer(r"<style\b[^>]*>([\s\S]*?)</style>", html))
        own += "\n".join(m.group(1) for m in
                         re.finditer(r'style="([^"]*)"', html))
        for m in SIZE.finditer(own):
            sizes[float(m.group(1))] += 1
        for m in RAD.finditer(own):
            radii[float(m.group(1))] += 1
        for _m in GRAD.finditer(own):
            grads[rel] += 1
        links = [n for n in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)',
                                       html)]
        # Everything CSS that this page can see: its own inline blocks, its
        # style attributes, and every sheet it links.
        seen = [html] + [sheet[n] for n in links if n in sheet]
        blob = "\n".join(seen)

        for f in declared(blob):
            faces[f] += 1
            if f not in HOUSE_FACES and base not in NOFACE:
                outside[f].add(rel)

        # loaded vs used, which needs both halves
        loaded = set()
        for m in GFONT.finditer(html):
            for fam in FAMPARAM.findall(m.group(1)):
                loaded.add(fam.replace("+", " ").strip().lower())
        want = primary(blob)
        if base not in NOFACE:
            for f in sorted(want - loaded):
                used_unloaded[f].add(rel)
            for f in sorted(loaded - declared(blob)):
                loaded_unused[f].add(rel)

    report = {
        "faces": {k: v for k, v in sorted(faces.items())},
        "sizes": sorted(sizes),
        "radii": sorted(radii),
        "gradient_pages": sorted(grads),
        "outside_house_faces": {k: sorted(v) for k, v in sorted(outside.items())},
        "used_but_not_loaded": {k: sorted(v)
                                for k, v in sorted(used_unloaded.items())},
        "loaded_but_not_used": {k: sorted(v)
                                for k, v in sorted(loaded_unused.items())},
    }

    if "--write-baseline" in sys.argv:
        json.dump(report, open(BASELINE, "w", encoding="utf-8"), indent=1,
                  sort_keys=True)
        print("baseline written: %d face(s), %d size(s), %d radius value(s), "
              "%d page(s) with a gradient"
              % (len(report["faces"]), len(report["sizes"]),
                 len(report["radii"]), len(report["gradient_pages"])))
        return

    print("%d page(s)" % len(pages()))
    print("\nFACES, by pages declaring them:")
    for f, n in faces.most_common():
        tag = "" if f in HOUSE_FACES else "   <- not a house face"
        print("  %4d  %s%s" % (n, f, tag))

    print("\n%d distinct font-size value(s). The house style names two type "
          "sizes." % len(sizes))
    odd = sorted(s for s in sizes if abs(s * 2 - round(s * 2)) > 1e-9)
    print("  %d of them are not a whole or half pixel: %s"
          % (len(odd), ", ".join("%gpx" % s for s in odd[:14])))
    print("  16.5px (the house body metric): %d use(s).  15px: %d.  14px: %d."
          % (sizes.get(16.5, 0), sizes.get(15.0, 0), sizes.get(14.0, 0)))

    print("\n%d distinct border-radius value(s). 999px (a pill, which the "
          "house style rules out): %d use(s)." % (len(radii),
                                                  radii.get(999.0, 0)))

    print("\n%d gradient(s) over %d page(s). The house style says none."
          % (sum(grads.values()), len(grads)))

    if used_unloaded:
        print("\nUSED BUT NOT LOADED - these render in a fallback face:")
        for f, ps in sorted(used_unloaded.items()):
            print("  %-24s %3d page(s)  e.g. %s" % (f, len(ps),
                                                    sorted(ps)[0]))
    if loaded_unused:
        print("\nLOADED BUT NOT USED - a webfont downloaded for nothing:")
        for f, ps in sorted(loaded_unused.items()):
            print("  %-24s %3d page(s)  e.g. %s" % (f, len(ps),
                                                    sorted(ps)[0]))

    if "--check" in sys.argv:
        if not os.path.exists(BASELINE):
            sys.exit("no baseline - run --write-baseline first")
        old = json.load(open(BASELINE, encoding="utf-8"))
        bad = []
        for f in sorted(set(report["faces"]) - set(old["faces"])):
            bad.append("new typeface: %s" % f)
        for s in sorted(set(report["sizes"]) - set(old["sizes"])):
            bad.append("new font-size: %gpx" % s)
        for r in sorted(set(report["radii"]) - set(old["radii"])):
            bad.append("new border-radius: %gpx" % r)
        for p in sorted(set(report["gradient_pages"])
                        - set(old["gradient_pages"])):
            bad.append("new gradient on: %s" % p)
        for f in sorted(set(report["used_but_not_loaded"])
                        - set(old["used_but_not_loaded"])):
            bad.append("face used but not loaded: %s" % f)
        if bad:
            print()
            for b in bad:
                print("  NEW  %s" % b)
            sys.exit("%d new typography drift(s) - conform them, or run "
                     "--write-baseline if deliberate" % len(bad))
        print("\nagainst the baseline: 0 new faces, sizes, radii, gradients "
              "or unloaded faces.")


if __name__ == "__main__":
    main()
