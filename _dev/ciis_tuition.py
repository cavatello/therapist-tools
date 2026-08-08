#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIIS publishes its tuition. This page said it did not.

WHAT WAS WRONG. california-institute-of-integral-studies-mft.html carried
"Published tuition: not published" and a whole section headed "This programme
does not publish a tuition figure anywhere I could find it." CIIS publishes it
plainly, on the page this site was already linking to as the programme's own
page:

    Master's Division Students, per unit
      2025-26   $1,374
      2026-27   $1,449
    -- https://www.ciis.edu/admissions-and-financial-aid/costs-and-aid/tuition-and-fees

so the gap was a collection failure, not an absence. On a site whose whole
proposition is that a missing figure means nobody published it, a wrong "not
published" is the most expensive kind of error there is: it is a claim about
the school, and it is false.

A NOTE ON THE SOURCE. Google's AI Overview gives $1,028 a unit for 2026-27 for
this school. It is wrong - it appears to be quoting a different division's rate.
The figure used here is read off CIIS's own tuition table. This is exactly why
the rule on this project is to verify a number against the institution's page
rather than a summary of it.

WHAT THIS CHANGES.

  programs.json   per_unit, tyear and turl, so every future rebuild is right.
  the school page the tuition row, the headline figure and the "what it costs"
                  section, edited in place - because the rendered page has since
                  been through restyle, nav_rebuild, uplinks, breadcrumbs and
                  analytics, and rebuilding it from build_schools.py would drop
                  all of that chrome on the floor.
  the depth JSON  drops "Tuition and total cost of attendance were not
                  collected" from the gaps list, and the page's rendered copy
                  of it.
  32 other pages  the sentence "45 of the 78 on the Board's list are the same"
                  is a COUNT. One school moving from not-published to published
                  makes it 44, everywhere it appears. A derived number left
                  stale on 32 pages is the same bug in a different place.

Idempotent: a second run reports nothing to do.
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
GUIDE = os.path.join(SITE, "mock", "mftguide")
SLUG = "california-institute-of-integral-studies-mft"
PAGE = os.path.join(SITE, SLUG + ".html")

PER_UNIT = 1449.0
TYEAR = "2026-27"
TURL = "https://www.ciis.edu/admissions-and-financial-aid/costs-and-aid/tuition-and-fees"
TU = "$1,449 a unit"
YR = ' <span class="yr">%s</span>' % TYEAR

GAP = "Tuition and total cost of attendance were not collected."

NP = '<span class="np">not published</span>'


def rewrite(path, pairs, required=True):
    s = open(path, encoding="utf-8").read()
    orig = s
    for old, new in pairs:
        if old not in s:
            if required and new not in s:
                sys.exit("%s: could not find\n  %r" % (os.path.basename(path), old[:120]))
            continue
        s = s.replace(old, new)
    if s != orig:
        open(path, "w", encoding="utf-8").write(s)
        return True
    return False


def main():
    # ---- 1. the data, so a rebuild does not undo this
    dp = os.path.join(GUIDE, "programs.json")
    progs = json.load(open(dp, encoding="utf-8"))
    hit = [p for p in progs if p["institution"] == "California Institute of Integral Studies"]
    if not hit:
        sys.exit("programs.json: CIIS not found")
    r = hit[0]
    if r.get("per_unit") != PER_UNIT or r.get("tyear") != TYEAR:
        r["per_unit"] = PER_UNIT
        r["tyear"] = TYEAR
        r["turl"] = TURL
        open(dp, "w", encoding="utf-8").write(
            json.dumps(progs, indent=1, ensure_ascii=False) + "\n")
        print("programs.json: per_unit=%s tyear=%s" % (PER_UNIT, TYEAR))
    else:
        print("programs.json: already correct")

    published = sum(1 for p in progs if p.get("per_unit") or p.get("total"))
    n_all = len(progs)
    silent = n_all - published
    print("%d of %d now publish a figure; %d do not" % (published, n_all, silent))

    # ---- 2. the depth record
    dj = os.path.join(GUIDE, "depth", SLUG + ".json")
    if os.path.exists(dj):
        d = json.load(open(dj, encoding="utf-8"))
        gaps = [g for g in d.get("gaps", []) if GAP not in g]
        if len(gaps) != len(d.get("gaps", [])):
            d["gaps"] = gaps
            open(dj, "w", encoding="utf-8").write(
                json.dumps(d, indent=1, ensure_ascii=False) + "\n")
            print("depth JSON: tuition gap removed")

    # ---- 3. the rendered page
    src = ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s'
           % (TURL, TU, YR))
    pairs = [
        # the on-paper table row
        ('<div class="r"><span>Published tuition</span><b>%s</b></div>' % NP,
         '<div class="r"><span>Published tuition</span><b>%s</b></div>' % src),
        # the headline figure, which falls back to the unit count only when
        # there is no tuition to show
        ('<b>60 units (LMFT track); 70 units (LPCC track)</b>'
         '<span>to complete the degree</span>',
         '<b>%s</b><span>published tuition, %s</span>' % (TU, TYEAR)),
        # the section that asserted the absence
        ("<p><b>This programme does not publish a tuition figure</b> anywhere I "
         "could find it. 45 of the 78 on the Board&rsquo;s list are the same. "
         "That is a fair thing to ask admissions directly, and the speed and "
         "specificity of the answer tells you something on its own.</p>",
         "<p>The figure below is the institution&rsquo;s own, from its own page, "
         "with the year it applies to. Multiply the per-unit rate by the actual "
         "unit count and add campus fees before comparing it with anything. At "
         "this rate the 60-unit LMFT track is about <b>$86,940</b> of tuition "
         "and the 70-unit LPCC track about <b>$101,430</b>, before fees.</p>"
         '<p style="font-size:15.2px"><b>%s</b>%s &mdash; '
         '<a href="%s" target="_blank" rel="noopener noreferrer">source</a></p>'
         % (TU, YR, TURL)),
    ]
    if rewrite(PAGE, pairs):
        print("%s.html rewritten" % SLUG)

    # the gap bullet as rendered
    s = open(PAGE, encoding="utf-8").read()
    out = re.sub(r"<li>[^<]*Tuition and total cost of attendance were not "
                 r"collected\.[^<]*</li>", "", s)
    if out != s:
        open(PAGE, "w", encoding="utf-8").write(out)
        print("%s.html: rendered gap bullet removed" % SLUG)

    # ---- 4. the count, on every page that quotes it
    old_n = "45 of the 78 on the Board&rsquo;s list are the same"
    new_n = "%d of the %d on the Board&rsquo;s list are the same" % (silent, n_all)
    n = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        p = os.path.join(SITE, f)
        s = open(p, encoding="utf-8").read()
        if old_n in s:
            open(p, "w", encoding="utf-8").write(s.replace(old_n, new_n))
            n += 1
    print("%d page(s) recounted -> %s" % (n, new_n))

    # ---- guards
    bad = 0
    s = open(PAGE, encoding="utf-8").read()
    for phrase in ["does not publish a tuition figure", GAP,
                   "Published tuition</span><b>%s" % NP]:
        if phrase in s:
            print("GUARD %s.html: %r survives" % (SLUG, phrase[:60]))
            bad += 1
    if TU not in s:
        print("GUARD %s.html: the figure is not on the page" % SLUG)
        bad += 1
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html") and old_n in open(
                os.path.join(SITE, f), encoding="utf-8").read():
            print("GUARD %s: stale count" % f)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
