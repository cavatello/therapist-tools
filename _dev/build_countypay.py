#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What a California county job actually pays, from the employers' own returns.

WHY THIS PAGE EXISTS

Every other figure on this site about county pay is self-reported or inferred
from a job advert. The State Controller publishes what each county actually
told the state it paid, by position, every year. Nobody has turned it on this
audience.

It also lands in the middle of three things already published here. The hiring
page says the settings that can legally bill for a pre-licensed clinician are
mostly county and county-contracted. The loan-forgiveness page says a county is
a government employer, so PSLF asks nothing further. The MBH-SLRP page says a
county behavioral health site scores 20 of the 70 points. All three point at
the county job, and none of them says what it pays.

THE FINDING

Median top of the published salary range, 2025, by county: San Mateo $140,483,
Imperial $50,855. Two point eight times, for comparable work, inside one state.
That is not a cost-of-living adjustment; San Mateo is expensive but it is not
2.8 times Imperial.

THE THREE METHOD DECISIONS THE PAGE HAS TO DEFEND

1. THE PUBLISHED RANGE LEADS, NOT ACTUAL PAY. Actual pay includes people who
   started in November, went on leave, or left in March, so its median sits
   below the range and answers a different question. A person comparing two
   counties wants the range. Both are printed and the difference is explained.

2. THE COUNT IS A FLOOR. 795 distinct job titles matched across three years and
   county naming is wildly inconsistent - Psychiatric Social Worker, Behavioral
   Health Clinician, Clinical Therapist, Mental Health Specialist all describe
   overlapping work. Anything named unusually is missed. The page says so.

3. THE PRE-LICENSED ROW IS ONE COUNTY. Exactly one county publishes an
   explicitly pre-licensed clinical title. It gives a clean licensure premium
   and it is a sample of one, and the page states that in the same breath as
   the number rather than in a footnote.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import county_pay_data as cp
import sf_pay_data as sf

SITE = pk.SITE
PAGE = "county-therapist-pay-california.html"
DONOR = "medi-cal-safety-net-employers-california.html"

HIRED = "getting-hired-as-a-california-associate.html"
FORGIVE = "loan-forgiveness-employers-california.html"
MBH = "mbh-slrp-california.html"
EMPLOYERS = "medi-cal-safety-net-employers-california.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"
ATLAS = "therapists-by-county-california.html"

JUMPS = [("spread", "The spread"),
         ("trend", "Three years"),
         ("table", "Every county"),
         ("prelicensed", "Pre-licensed"),
         ("sanfrancisco", "San Francisco"),
         ("method", "How it was counted"),
         ("sources", "Sources")]

Y = cp.YEARS
LATEST = Y[-1]
TOP = cp.COUNTIES[0]
BOTTOM = cp.COUNTIES[-1]
RATIO = TOP["max_med"] / float(BOTTOM["max_med"])


def money(n):
    return "$%s" % format(int(n), ",d")


def body():
    o = ['<article class="pk-wrap">']
    t = cp.YEAR_TOTALS

    o.append(pk.hero(
        "County pay &middot; the State Controller&rsquo;s own file &middot; "
        "read %s" % cp.CHECKED,
        "The same job pays %.1f times more in one California county than "
        "another." % RATIO,
        "Not a survey and not a job advert &mdash; this is what every county "
        "told the state it paid, for every position, three years running. "
        "<b>%s</b> clinical mental health positions across <b>%d</b> counties."
        % (format(t[LATEST]["matched"], ",d"), t[LATEST]["counties"]),
        [(money(TOP["max_med"]), "top of range, %s" % TOP["county"]),
         (money(BOTTOM["max_med"]), "top of range, %s" % BOTTOM["county"]),
         (format(t[LATEST]["matched"], ",d"), "positions counted"),
         ("%d" % len(cp.COUNTIES), "counties with enough to rank")],
        JUMPS))

    # ---------------------------------------------------------------- spread
    o.append('<section class="pk-sec" id="spread">')
    o.append(pk.quote(
        "Why this page is here",
        ["Three pages on this site already point at the county job. The hiring "
         "page, because Medi-Cal is what lets an employer bill for a "
         "pre-licensed clinician at all. The loan-forgiveness page, because a "
         "county is a government employer and PSLF asks nothing further. The "
         "MBH-SLRP page, because a county behavioral health site is worth 20 "
         "of the 70 points.",
         "None of them says what it pays. This one does, from the employers&rsquo; "
         "own returns rather than from anybody&rsquo;s memory of a job advert."]))

    o.append('<p class="pk-k">The finding</p>')
    o.append('<h2 class="pk-h">%s to %s, for the same work.</h2>'
             % (money(BOTTOM["max_med"]), money(TOP["max_med"])))
    o.append('<p class="pk-d">Median top of the published salary range in %s, '
             "across the clinical mental health positions each county reported. "
             "The gap is <b>%.1f&times;</b>, and cost of living does not explain "
             "it &mdash; %s is expensive, but it is not %.1f times %s.</p>"
             % (LATEST, RATIO, TOP["county"], RATIO, BOTTOM["county"]))

    rows = []
    for r in cp.COUNTIES[:6]:
        rows.append([r["county"], (money(r["max_med"]), "f"),
                     (money(r["min_med"]), "f"), (format(r["n"], ",d"), "m")])
    rows.append((["&hellip; %d counties between &hellip;"
                  % (len(cp.COUNTIES) - 12), "", "", ""], "mid"))
    for r in cp.COUNTIES[-6:]:
        rows.append([r["county"], (money(r["max_med"]), "f"),
                     (money(r["min_med"]), "f"), (format(r["n"], ",d"), "m")])
    o.append(pk.table(
        ["County", "Top of range", "Floor of range", "Positions"], rows,
        caption="The full table of all %d is further down. A county needs at "
                "least five reported positions to appear at all, so the very "
                "smallest are absent rather than shown on a sample of one."
                % len(cp.COUNTIES),
        minw=560))
    o.append("</section>")

    # ----------------------------------------------------------------- trend
    o.append('<section class="pk-sec" id="trend">')
    o.append('<p class="pk-k">Three years</p>')
    o.append('<h2 class="pk-h">The range moved %s in two years.</h2>'
             % money(t[LATEST]["max_med"] - t[Y[0]]["max_med"]))
    pct = 100.0 * (t[LATEST]["max_med"] - t[Y[0]]["max_med"]) / t[Y[0]]["max_med"]
    o.append('<p class="pk-d">Statewide medians across every county that '
             "reported. The top of the published range rose <b>%.1f%%</b> "
             "between %s and %s.</p>" % (pct, Y[0], LATEST))

    o.append(pk.table(
        ["Statewide median"] + [str(y) for y in Y],
        [["Positions counted"] + [(format(t[y]["matched"], ",d"), "m") for y in Y],
         ["Counties reporting"] + [(str(t[y]["counties"]), "m") for y in Y],
         ["Floor of the published range"] + [(money(t[y]["min_med"]), "f") for y in Y],
         (["<b>Top of the published range</b>"]
          + [(money(t[y]["max_med"]), "f") for y in Y], "hi"),
         ["Actual total wages"] + [(money(t[y]["wages_med"]), "f") for y in Y]],
        caption="Actual wages sit below the range because they include people "
                "who started in November, took leave, or left in March. The "
                "range is what a person comparing two counties is actually "
                "choosing between.",
        minw=560))

    o.append(pk.callout(
        "What this is worth next to the loan repayment",
        ["A county job at the median top of range is %s. Put that beside the "
         "two programs a county unlocks and the picture changes: <b>PSLF</b> "
         "asks only that the employer is a government entity, and "
         "<b>MBH-SLRP</b> scores a county behavioral health site at 20 of its "
         "70 points."
         % money(t[LATEST]["max_med"]),
         "So the county job is not simply the low-paying option people describe "
         "in the groups. It is the middle of the pay distribution attached to "
         "the two largest loan repayment routes an associate can reach &mdash; "
         'which is the arithmetic <a href="%s">the hiring page</a> runs, and '
         '<a href="%s">the loan-forgiveness page</a> explains.'
         % (HIRED, FORGIVE)]))
    o.append("</section>")

    # ----------------------------------------------------------------- table
    o.append('<section class="pk-sec" id="table">')
    o.append('<p class="pk-k">Every county</p>')
    o.append('<h2 class="pk-h">All %d, ordered by the top of the range.</h2>'
             % len(cp.COUNTIES))
    rows = []
    for r in cp.COUNTIES:
        then = r.get("max_med_2023")
        if then:
            delta = r["max_med"] - then
            move = ("%s%s" % ("+" if delta >= 0 else "&minus;",
                              money(abs(delta)).lstrip("$")), "m")
        else:
            move = ("&mdash;", "m")
        rows.append([r["county"], (money(r["max_med"]), "f"),
                     (money(r["min_med"]), "f"),
                     (money(r["wages_med"]) if r["wages_med"] else "&mdash;", "f"),
                     (format(r["n"], ",d"), "m"), move])
    o.append(pk.table(
        ["County", "Top of range", "Floor of range", "Actual wages, median",
         "Positions", "Change since %s" % Y[0]],
        rows,
        caption="%s data, from the State Controller&rsquo;s county file read "
                "%s. &ldquo;Change since %s&rdquo; compares the median top of "
                "range and is blank where the county did not report comparable "
                "positions that year. A dollar figure here is what the county "
                "published or paid &mdash; it is not an offer, and it is not "
                "what any individual earns."
                % (LATEST, cp.CHECKED, Y[0]),
        minw=720))
    o.append('<p class="pk-p">How crowded each county already is with '
             'therapists is <a href="%s">the county atlas</a>, and which of '
             'them run the Medi-Cal plans is <a href="%s">the employer '
             "directory</a>.</p>" % (ATLAS, EMPLOYERS))
    o.append("</section>")

    # ----------------------------------------------------------- pre-licensed
    p = cp.PRE_LICENSED
    o.append('<section class="pk-sec" id="prelicensed">')
    o.append('<p class="pk-k">The pre-licensed row</p>')
    o.append('<h2 class="pk-h">One county in the state publishes what it pays '
             "an associate.</h2>")
    o.append('<p class="pk-d">Of %s distinct job titles across three years, '
             "exactly one names the pre-licensed grade explicitly: <b>%s</b>, "
             "&ldquo;Clinical Therapist Pre-License&rdquo;. That makes a clean "
             "comparison possible against its own licensed grade &mdash; and "
             "makes it a sample of one county, which is said here rather than "
             "in a footnote.</p>" % (format(cp.DISTINCT_TITLES, ",d"), p["county"]))

    o.append(pk.table(
        ["Grade", "Floor of range", "Top of range", "People"],
        [["Clinical Therapist <b>Pre-License</b> &mdash; %s" % p["county"],
          (money(p["min"]), "f"), (money(p["max"]), "f"),
          (format(p["n"], ",d"), "m")],
         (["Clinical Therapist I&ndash;III, licensed &mdash; %s"
           % " and ".join(p["peer_counties"]),
           (money(p["peer_min"]), "f"), (money(p["peer_max"]), "f"),
           (format(p["peer_n"], ",d"), "m")], "hi")],
        caption="The licensed grade spans two counties because Riverside uses "
                "the same title; the pre-licensed grade exists in one.",
        minw=560))

    o.append('<p class="pk-p">The gap at the top of the range is <b>%s</b>, or '
             "about <b>%.0f%%</b>. That is what this one county has decided the "
             "license is worth, and it is the only county in California that "
             "publishes the comparison at all. Everywhere else the pre-licensed "
             "clinician is inside a grade that does not name them, which is its "
             "own finding about how visible associates are in public payroll "
             "data.</p>"
             % (money(p["peer_max"] - p["max"]),
                100.0 * (p["peer_max"] - p["max"]) / p["max"]))
    o.append("</section>")

    # --------------------------------------------------------- san francisco
    L = sf.YEARS[-1]
    T = sf.YEAR_TOTALS[L]
    o.append('<section class="pk-sec" id="sanfrancisco">')
    o.append('<p class="pk-k">The county that is not in the file</p>')
    o.append('<h2 class="pk-h">San Francisco is missing from every table '
             "above, and it is one of the best payers in the state.</h2>")
    o.append('<p class="pk-d">Not under-counted &mdash; <b>absent</b>. There is '
             "no employer named San Francisco anywhere in the State "
             "Controller&rsquo;s county file, because San Francisco is a "
             "consolidated city and county and files in the "
             "<em>cities</em> dataset instead. The table above reports %d of "
             "California&rsquo;s 58 counties and this is one of the three it "
             "cannot see.</p>" % cp.YEAR_TOTALS[LATEST]["counties"])

    o.append(pk.quote(
        "Read this before comparing the numbers",
        ["San Francisco publishes what it <em>paid</em>. It does not publish a "
         "salary range at all, so the figures below are <b>actual base salary "
         "for full-time staff</b> &mdash; a different measure from the "
         "published range that leads every table above, and one that normally "
         "sits <em>below</em> the top of a range rather than at it.",
         "That is why San Francisco gets its own section rather than a row. "
         "Putting a derived range into a table of published ones would make "
         "every other number on this page harder to trust, which is a bad "
         "trade for one more line."]))

    o.append(pk.table(
        ["San Francisco, full-time"] + list(sf.YEARS),
        [["People in these titles"]
         + [(format(sf.YEAR_TOTALS[y]["n_all"], ",d"), "m") for y in sf.YEARS],
         ["Of those, full-time"]
         + [(format(sf.YEAR_TOTALS[y]["n_ft"], ",d"), "m") for y in sf.YEARS],
         (["<b>Median base salary</b>"]
          + [("<b>%s</b>" % money(sf.YEAR_TOTALS[y]["median"]), "f")
             for y in sf.YEARS], "hi"),
         ["Tenth percentile"]
         + [(money(sf.YEAR_TOTALS[y]["p10"]), "f") for y in sf.YEARS],
         ["Ninetieth percentile"]
         + [(money(sf.YEAR_TOTALS[y]["p90"]), "f") for y in sf.YEARS]],
        caption="Base salary only &mdash; overtime and other pay excluded, "
                "benefits excluded. Full-time means the city recorded at least "
                "%d paid hours, which removes people who started late, left "
                "early or took leave. The county table above does <b>not</b> "
                "filter that way, which is one more reason these sit apart."
                % sf.FT_HOURS,
        minw=620))

    rows = []
    for t in sf.BY_TITLE:
        rows.append([pk.esc(t["job"]), (format(t["n"], ",d"), "m"),
                     (money(t["median"]), "f"), (money(t["p10"]), "f"),
                     (money(t["p90"]), "f")])
    o.append(pk.table(
        ["Classification, %s" % L, "Full-time people", "Median base",
         "Tenth percentile", "Ninetieth percentile"], rows,
        caption="The city&rsquo;s own classification titles. Five more that a "
                "keyword search catches were left out by hand &mdash; juvenile "
                "hall and family court counselors, an environmental health "
                "inspector, and two single-person administrative roles &mdash; "
                "because none of them is a clinical classification.",
        minw=680))

    o.append(pk.callout(
        "What the comparison is actually worth",
        ["A San Francisco <b>Behavioral Health Clinician</b> was paid a median "
         "base of <b>%s</b>, and the senior grade <b>%s</b>. Against the "
         "statewide county median of <b>%s</b> in <em>actual total wages</em> "
         "&mdash; the nearest like-for-like column on this page &mdash; that "
         "is a different market."
         % (money(sf.BY_TITLE[0]["median"]), money(sf.BY_TITLE[1]["median"]),
            money(cp.YEAR_TOTALS[LATEST]["wages_med"])),
         "Two cautions in the same breath. The statewide figure includes "
         "part-year staff and this one does not, so some of the gap is "
         "measurement. And <b>%s of the %s full-time posts sit in one "
         "department</b>, %s &mdash; this is one large employer, not a city-wide "
         "average."
         % (format(sf.TOP_DEPARTMENT[1], ",d"), format(T["n_ft"], ",d"),
            sf.TOP_DEPARTMENT[0])],
        big=money(sf.BY_TITLE[0]["median"])))

    o.append('<p class="pk-p">Headcount is the other half of it. <b>%s</b> '
             "people held these titles in %s, which would place San Francisco "
             "among the largest public behavioral health employers in the Bay "
             "Area &mdash; and the page said nothing about it until now. How "
             'crowded the county already is with therapists is <a href="%s">the '
             "county atlas</a>.</p>"
             % (format(T["n_all"], ",d"), L, ATLAS))
    o.append("</section>")

    # ---------------------------------------------------------------- method
    o.append('<section class="pk-sec" id="method">')
    o.append('<p class="pk-k">How it was counted</p>')
    o.append('<h2 class="pk-h">Three decisions, and what each of them costs.</h2>')
    o.append(pk.numbered([
        ("1", "The published range leads, not actual pay.",
         "Every row carries the position&rsquo;s published salary range "
         "alongside what the person was actually paid. Actual pay includes "
         "part-year staff, leave and mid-year starters, so its median sits "
         "below the range and answers a different question. Both are printed."),
        ("2", "The count is a floor, not a census.",
         "%s distinct titles matched across three years, and county naming is "
         "wildly inconsistent &mdash; psychiatric social worker, behavioral "
         "health clinician, clinical therapist and mental health specialist "
         "all describe overlapping work. Anything a county names unusually is "
         "missed. Physical and occupational therapists, environmental health "
         "specialists and employment counselors are excluded deliberately, "
         "because a keyword match catches all of them."
         % format(cp.DISTINCT_TITLES, ",d")),
        ("3", "A figure here is not an offer.",
         "It is what a county published as a range, or reported as paid, for a "
         "grade. What you are offered depends on the grade you are hired into, "
         "your step within it, and whether the posting is full time. Treat this "
         "as the shape of the market rather than as a number to quote in a "
         "negotiation."),
    ]))
    o.append('<p class="pk-p">The underlying files are public and bulk '
             "downloadable, so anything here can be checked against the source "
             "rather than taken on trust. What each setting pays an associate "
             'specifically, from job adverts rather than payroll, is on <a '
             'href="%s">the associate pay page</a>.</p>' % PAY)
    o.append("</section>")

    # --------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The data", [
            ("Government Compensation in California &mdash; the State "
             "Controller&rsquo;s bulk county files for %s, read %s"
             % (", ".join(str(y) for y in Y), cp.CHECKED),
             cp.SOURCE),
            ("San Francisco Employee Compensation, the city&rsquo;s own file "
             "over DataSF, read %s &mdash; San Francisco is a consolidated "
             "city and county and is not in the Controller&rsquo;s county "
             "download at all" % sf.CHECKED, sf.PAGE),
        ]),
        ("Where the county job comes up elsewhere on this site", [
            ("Which settings can legally bill for a pre-licensed clinician",
             "https://therapistsupport.org/%s" % HIRED),
            ("Which employers unlock loan forgiveness, and on what test",
             "https://therapistsupport.org/%s" % FORGIVE),
            ("MBH-SLRP, where a county behavioral health site scores 20 of 70",
             "https://therapistsupport.org/%s" % MBH),
        ]),
    ], note="Figures are what counties reported to the State Controller for "
            "the years shown, reduced to medians by <b>_dev/county_pay.py</b>. "
            "The Controller states that information is posted as submitted by "
            "each employer and that it is not responsible for the accuracy of "
            "it. <b>A figure here is a published range or a reported payment, "
            "not an offer</b>, and not what any individual earns. Nothing here "
            "is career or financial advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "What California county jobs pay therapists, from the state's own file",
    "The same clinical role pays %.1f times more in one California county than "
    "another. %s positions across %d counties, from what employers reported to "
    "the State Controller." % (RATIO, format(cp.YEAR_TOTALS[LATEST]["matched"], ",d"),
                               cp.YEAR_TOTALS[LATEST]["counties"]),
    "getting-paid", "reference",
    "What does a California county job actually pay a therapist?",
    "Every county ranked by published salary range, three years of movement, "
    "and the one county that publishes what it pays a pre-licensed clinician",
    "%.1f&times; between the top and bottom county" % RATIO,
    weight=4)


def main():
    print("county pay")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d counties, %d sources"
          % (PAGE, format(len(html), ",d"), len(cp.COUNTIES), nsrc))

    bad = pk.check_page(p, [
        ("the San Francisco absence", "consolidated city and county"),
        ("the different-measure caveat", "different measure from the"),
        ("the spread finding", "for the same work"),
        ("the range-not-actual decision", "answers a different question"),
        ("the floor-not-census caveat", "not a census"),
        ("the not-an-offer caveat", "is not an offer"),
        ("the one-county caveat", "sample of one county"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every ranked county must appear. A county missing from a pay table reads
    # as "your county pays nothing", which is never what it means.
    for r in cp.COUNTIES:
        if r["county"] not in art:
            print("GUARD: %s is missing from the table" % r["county"])
            bad += 1

    # The headline ratio and the two endpoints have to agree with the data.
    if "%.1f" % RATIO not in art:
        print("GUARD: the headline ratio is not on the page")
        bad += 1
    for v in (TOP["max_med"], BOTTOM["max_med"]):
        if money(v) not in art:
            print("GUARD: %s is not on the page" % money(v))
            bad += 1

    # The pre-licensed section must keep its sample-size caveat attached to the
    # number, not floating elsewhere.
    i_num = art.find(money(cp.PRE_LICENSED["max"]))
    i_caveat = art.find("sample of one county")
    if i_num < 0 or i_caveat < 0 or abs(i_num - i_caveat) > 4000:
        print("GUARD: the one-county caveat has drifted away from the figure")
        bad += 1

    # San Francisco's figures must never migrate into the county table, which
    # is a table of published ranges. If the median base salary ever appears
    # above the San Francisco section, something has merged them.
    i_sf = art.find('id="sanfrancisco"')
    i_med = art.find(money(sf.YEAR_TOTALS[sf.YEARS[-1]]["median"]))
    if i_sf < 0:
        print("GUARD: the San Francisco section is missing")
        bad += 1
    elif 0 <= i_med < i_sf:
        print("GUARD: a San Francisco figure appears above its own section - "
              "actual pay and published ranges have been mixed")
        bad += 1

    # And the basis caveat has to sit with the figures, not drift.
    i_cav = art.find("different measure from the", i_sf if i_sf > 0 else 0)
    if i_cav < 0 or abs(i_cav - i_sf) > 3000:
        print("GUARD: the basis caveat has drifted away from the section")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
