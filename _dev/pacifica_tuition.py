#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pacifica publishes its cost of attendance. This page said it did not.

WHAT PACIFICA ACTUALLY PUBLISHES, 2025-26
(https://www.pacifica.edu/financial-aid/cost-of-attendance/2025-2026-cost-of-attendance-m-a-counseling-psychology/)

  Tuition        $7,467 per quarter for Fall, Winter and Spring
                 $5,599 for Summer
                 = $28,000 a year
  Residential    $2,328 per quarter Fall-Spring, $2,032 Summer = $9,016 a year
  Non-residential  $1,332 per quarter Fall-Spring, $1,036 Summer = $5,032 a year

  Annual direct total: $37,016 residential / $33,032 non-residential.

WHY THE PROGRAM FIGURE IS COMPUTED AND SAYS SO

Pacifica publishes an ANNUAL cost and does not publish a program total. The
program is 2.5 years (10 quarters), which the school does publish. So
$28,000 x 2.5 = $70,000 of tuition is arithmetic on the institution's own two
published numbers - which is exactly what this site means by "computed" - and
it goes on the chart as a hatched bar, not a solid one. Calling it "published"
would claim Pacifica had stated a number it has not stated.

The residential fee is NOT rolled into that figure. It is a real, compulsory,
published charge - the program is low-residency and the retreats are not
optional - but it pays for accommodation and meals, so folding it into a
tuition comparison would make Pacifica look expensive against schools whose
students pay rent to a landlord instead. It is named separately on the page,
which is the only honest way to show it.

GOOGLE'S AI OVERVIEW SAYS $62,500-$75,000 for this program. It is a summary of
summaries; the figures here are read off Pacifica's own table. Same rule as
CIIS: verify against the institution, not against a description of it.

Idempotent, guarded.
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
GUIDE = os.path.join(SITE, "mock", "mftguide")
SLUG = "pacifica-graduate-institute-mft"
PAGE = os.path.join(SITE, SLUG + ".html")
DIRECTORY = os.path.join(SITE, "mft-programs-california.html")

TURL = ("https://www.pacifica.edu/financial-aid/cost-of-attendance/"
        "2025-2026-cost-of-attendance-m-a-counseling-psychology/")
TYEAR = "2025-26"
ANNUAL = 28000
YEARS = 2.5
TOTAL = int(ANNUAL * YEARS)             # 70,000
RES = 9016
NONRES = 5032
TU = "$%s total" % "{:,}".format(TOTAL)
NP = '<span class="np">not published</span>'

COST = (
    "<p>Pacifica publishes a cost of attendance per year rather than per "
    "program. Tuition is <b>$7,467</b> a quarter for Fall, Winter and Spring "
    "and <b>$5,599</b> for Summer &mdash; <b>$28,000</b> a year. The program "
    "runs 2.5 years, so the tuition for the whole degree is <b>$70,000</b>. "
    "That multiplication is mine; both numbers in it are Pacifica&rsquo;s.</p>"
    "<p>On top of tuition there is a compulsory session fee, because this is a "
    "low-residency program and the retreats are not optional: <b>$9,016</b> a "
    "year residential (room and meals on campus) or <b>$5,032</b> a year "
    "non-residential. It is listed separately here rather than added in, "
    "because it buys accommodation &mdash; rolling it into a tuition "
    "comparison would price Pacifica against schools whose students pay a "
    "landlord instead.</p>"
    '<p style="font-size:15.2px"><b>%s</b> <span class="yr">%s</span> &mdash; '
    '<a href="%s" target="_blank" rel="noopener noreferrer">source</a></p>'
    % (TU, TYEAR, TURL))


def main():
    # ---- the data
    dp = os.path.join(GUIDE, "programs.json")
    progs = json.load(open(dp, encoding="utf-8"))
    hit = [p for p in progs if p["institution"] == "Pacifica Graduate Institute"]
    if not hit:
        sys.exit("programs.json: Pacifica not found")
    r = hit[0]
    if r.get("total") != TOTAL:
        r["total"] = TOTAL
        r["tyear"] = TYEAR
        r["turl"] = TURL
        open(dp, "w", encoding="utf-8").write(
            json.dumps(progs, indent=1, ensure_ascii=False) + "\n")
        print("programs.json: total=%s tyear=%s" % (TOTAL, TYEAR))
    else:
        print("programs.json: already correct")

    published = sum(1 for p in progs if p.get("per_unit") or p.get("total"))
    n_all = len(progs)
    silent = n_all - published
    print("%d of %d publish a figure; %d do not" % (published, n_all, silent))

    # ---- the school page
    if os.path.exists(PAGE):
        s = open(PAGE, encoding="utf-8").read()
        orig = s
        src = ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
               ' <span class="yr">%s</span>' % (TURL, TU, TYEAR))
        s = s.replace(
            '<div class="r"><span>Published tuition</span><b>%s</b></div>' % NP,
            '<div class="r"><span>Published tuition</span><b>%s</b></div>' % src)
        s = re.sub(
            r"<p><b>This program does not publish a tuition figure</b>"
            r"[\s\S]*?</p>", COST, s, count=1)
        s = re.sub(r"<li>[^<]*[Tt]uition[^<]*not (?:collected|published)[^<]*</li>",
                   "", s)
        if s != orig:
            open(PAGE, "w", encoding="utf-8").write(s)
            print("%s.html rewritten" % SLUG)

    # ---- the count sentence, wherever it is quoted
    old = None
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        p = os.path.join(SITE, f)
        t = open(p, encoding="utf-8").read()
        m = re.search(r"(\d+) of the (\d+) on the Board&rsquo;s list are the same", t)
        if m and int(m.group(1)) != silent:
            old = m.group(0)
            break
    n = 0
    if old:
        new = ("%d of the %d on the Board&rsquo;s list are the same"
               % (silent, n_all))
        for f in sorted(os.listdir(SITE)):
            if not f.endswith(".html"):
                continue
            p = os.path.join(SITE, f)
            t = open(p, encoding="utf-8").read()
            if old in t:
                open(p, "w", encoding="utf-8").write(t.replace(old, new))
                n += 1
        print("%d page(s) recounted -> %s" % (n, new))

    # ---- the directory chart: a COMPUTED bar, hatched, in rank order
    d = open(DIRECTORY, encoding="utf-8").read()
    orig = d
    top = 152340.0
    bar = ('<div class="ig-b cmp"><span class="ig-l">'
           '<a href="%s.html">Pacifica Graduate Institute</a></span>'
           '<span class="ig-t"><i style="width:%.4f%%"></i></span>'
           '<span class="ig-v">$%s</span></div>'
           % (SLUG, 100.0 * TOTAL / top, "{:,}".format(TOTAL)))
    if "Pacifica Graduate Institute</a></span><span class=\"ig-t\"" not in d:
        # immediately below the next figure up, so the chart stays sorted
        m = re.search(r'<div class="ig-b [a-z]+"><span class="ig-l">'
                      r'(?:<a[^>]*>)?Meridian University', d)
        if not m:
            print("  chart: could not find the insertion point, bar not added")
        else:
            d = d[:m.start()] + bar + d[m.start():]
            print("directory: computed bar inserted at $%s"
                  % "{:,}".format(TOTAL))
    dot = ('<span class="ig-d" title="Pacifica Graduate Institute"></span>')
    if dot in d:
        d = d.replace(dot, "", 1)
        print("directory: removed from the no-figure list")
    d = re.sub(r"<b>\d+ of the \d+ publish neither</b>",
               "<b>%d of the %d publish neither</b>" % (silent, n_all), d)
    if d != orig:
        open(DIRECTORY, "w", encoding="utf-8").write(d)

    # ---- guards
    bad = 0
    if os.path.exists(PAGE):
        s = open(PAGE, encoding="utf-8").read()
        if "does not publish a tuition figure" in s:
            print("GUARD %s.html: still claims no figure" % SLUG)
            bad += 1
        if TU not in s:
            print("GUARD %s.html: the figure is not on the page" % SLUG)
            bad += 1
    d = open(DIRECTORY, encoding="utf-8").read()
    if "Pacifica Graduate Institute</a>" not in d:
        print("GUARD directory: Pacifica is not on the chart")
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
