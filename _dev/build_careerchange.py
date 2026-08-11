#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Becoming a therapist in California, for somebody arriving from another job.

WHY THIS PAGE EXISTS

The site's coverage audit found 73 pages aimed at people already inside the
profession and none at all aimed at the person deciding whether to enter it.
That person is asking four questions nobody answers with numbers:

  How many people are doing this, and is the field filling up?
  Which of the three licenses should I aim at, and does it matter?
  How long does it really take, counted honestly?
  What does it cost me, and what does it pay?

Every one of those is answerable from data this site already holds, plus one
federal series it did not: IPEDS completions, which says how many California
master's degrees a year feed the pipeline.

THE FOUR FINDINGS

1. THE PIPELINE GREW 66% IN EIGHT YEARS while California's master's output
   overall grew 14%. Nobody is publishing that. It is the single most
   decision-relevant fact for a person choosing this in 2026, and it points
   the opposite way from every "shortage" headline.

2. ONLY THE MFT LICENSE BANKS PRE-DEGREE HOURS. Section 4980.43(c)(4) allows
   1,300 of the 3,000 to be earned before the degree is awarded. Section
   4999.46(c)(1) requires the LPCC's to be postdegree and section 4996.23(a)
   requires the LCSW's to be post-master's. Same practicum, same work, and
   two of the three throw it away.

3. THE THREE LICENSES ARE AT COMPLETELY DIFFERENT POINTS OF THEIR LIVES.
   There are 0.33 MFT associates per licensed MFT, 0.47 social work
   associates per LCSW, and 1.25 counselor associates per LPCC. The LPCC is
   still mostly a register of people who have not finished.

4. ATTRITION IS VISIBLE IN THE BOARD'S OWN NUMBERS and nobody puts them
   together: 29.74% of applications arrive deficient, the clinical exams pass
   in the sixties and seventies, and 26.7% of counselor associate
   registrations are delinquent against 6.4% of licensed MFTs.

WHAT THIS PAGE MUST NOT DO

It must not tell anybody whether to do it. The whole value is that the
numbers are assembled honestly in one place and the reader decides. Every
encouraging sentence and every discouraging one has to be a figure with a
source next to it. A guard below fails the build if the page ever tells the
reader what to choose.

THE TUITION CAVEAT IS LOAD-BEARING

Only 33 of the 78 programs publish a per-unit price or a total, and the
California State University campuses are largely not among them because they
publish a per-semester full-time rate instead. So the range printed is the
range across the programs that publish - it is not the range across
California, and the cheapest option in the state is probably not on it. That
sentence ships beside the number, and a guard checks it is still there.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import bbs_stats as B
import dca_stats as D
import degree_pipeline as G
import practicum_data as P
import county_pay_data as CP

SITE = pk.SITE
PAGE = "becoming-a-therapist-california-career-change.html"
DONOR = "practicum-california-mft-trainee.html"

PRACTICUM = "practicum-california-mft-trainee.html"
PROGRAMS = "mft-programs-california.html"
BECOME = "become-an-mft-california.html"
HIRED = "getting-hired-as-a-california-associate.html"
CALC = "amft-3000-hours-california.html"
EXAMS = "bbs-exam-pass-rates-california.html"
TIMES = "bbs-processing-times-california.html"
FEES = "bbs-fees-california-2026.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"
COUNTY = "county-therapist-pay-california.html"
RATES = "rates.html"
ATLAS = "therapists-by-county-california.html"
FORGIVE = "loan-forgiveness-employers-california.html"
COL = "therapist-cost-of-living-california.html"
UNPAID = "associate-unpaid-hours-california.html"

LEG = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
       "?lawCode=BPC&sectionNum=%s.")

JUMPS = [("pipeline", "How many are coming"),
         ("license", "Which of the three"),
         ("clock", "How long, honestly"),
         ("cost", "What it costs"),
         ("pay", "What it pays"),
         ("attrition", "Where people stop"),
         ("questions", "Before you apply"),
         ("sources", "Sources")]

FIRST, LAST = G.YEARS[0], G.YEARS[-1]
WIDE_GROWTH = 100.0 * (G.WIDE_LATEST - G.WIDE_FIRST) / G.WIDE_FIRST
ALL_GROWTH = (100.0 * (G.STATE_TOTAL[LAST] - G.STATE_TOTAL[FIRST])
              / G.STATE_TOTAL[FIRST])

AMFT = D.BY_TYPE["Associate Marriage & Family Therapist"]
LMFT = D.BY_TYPE["Licensed Marriage and Family Therapist"]
ASW = D.BY_TYPE["Associate Clinical Social Worker"]
LCSW = D.BY_TYPE["Licensed Clinical Social Worker"]
APCC = D.BY_TYPE["Assoc. Professional Clinical Counselor"]
LPCC = D.BY_TYPE["Licensed Professional Clinical Counselor"]

TUI = P.TUITION
TUI_LO, TUI_HI = TUI[0], TUI[-1]
TUI_MED = TUI[len(TUI) // 2]

TUITION_CAVEAT = (
    "Only %d of the %d programs publish a per-unit price or a total, and the "
    "California State University campuses are largely not among them because "
    "they publish a per-semester full-time rate instead. <b>This is the range "
    "across the programs that publish it, not the range across California</b>, "
    "and the cheapest degree in the state is probably not on it."
    % (P.TUITION_N, P.N))


def n(x):
    return format(int(x), ",d")


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Changing career &middot; California &middot; the numbers, checked %s"
        % G.CHECKED,
        "California graduates %s people a year into this, and it is growing "
        "%.0f times faster than graduate education is." % (n(G.WIDE_LATEST),
                                                           WIDE_GROWTH / ALL_GROWTH),
        "Not encouragement and not a warning &mdash; the figures somebody "
        "deciding whether to retrain deserves to see first. How many are "
        "coming, which of the three licenses is which, how long it takes "
        "counted honestly, what it costs and what it pays.",
        [(n(G.WIDE_LATEST), "clinical master's a year"),
         ("+%.0f%%" % WIDE_GROWTH, "growth since %d" % FIRST),
         (n(AMFT + ASW + APCC), "associates in the queue"),
         ("104", "weeks minimum after the degree")],
        JUMPS))

    # -------------------------------------------------------------- pipeline
    o.append('<section class="pk-sec" id="pipeline">')
    o.append(pk.quote(
        "The question underneath the question",
        ["People asking whether to retrain into therapy almost always ask it "
         "as &ldquo;is there demand?&rdquo;. There is. That is not the "
         "binding constraint and it never was.",
         "The binding constraint is <em>supply of the thing you need next</em> "
         "&mdash; a practicum seat, then a job that will employ someone who "
         "cannot yet bill commercial insurance, then a supervisor. Every one "
         "of those is rationed, and the number of people competing for them "
         "is the number below."]))

    o.append('<p class="pk-k">How many are coming</p>')
    o.append('<h2 class="pk-h">The pipeline grew %.0f%% while all California '
             "master's degrees grew %.0f%%.</h2>" % (WIDE_GROWTH, ALL_GROWTH))
    o.append('<p class="pk-d">Master&rsquo;s degrees awarded by California '
             "institutions, from the federal completions survey every "
             "accredited school must file. The clinical pipeline is the four "
             "fields a California LMFT or LPCC degree actually files under "
             "&mdash; the Board approves a degree by its content, not by its "
             "federal subject code, so counting only &ldquo;marriage and "
             "family therapy&rdquo; undercounts badly.</p>")

    labels = {c: l for c, l, _ in G.CIP}
    show = ["511505", "422803", "511508", "422801", "440701", "131101"]
    rows = []
    for c in show:
        cells = [labels[c] + (" <b>&bull;</b>" if c in G.WIDE else "")]
        cells += [(n(G.SERIES[y][c]), "f") for y in G.YEARS]
        rows.append(cells)
    rows.append((["<b>The clinical pipeline &mdash; the four marked</b>"]
                 + [("<b>%s</b>" % n(sum(G.SERIES[y][c] for c in G.WIDE)), "f")
                    for y in G.YEARS], "hi"))
    rows.append(["Every master's degree in California"]
                + [(n(G.STATE_TOTAL[y]), "m") for y in G.YEARS])
    o.append(pk.table(
        ["Field of study"] + [str(y) for y in G.YEARS], rows,
        caption="%d is absent because the data mirror returns it "
                "byte-identical to %d for every California institution, which "
                "is not what a real year looks like. Social work and school "
                "counseling are shown for scale and are not counted in the "
                "clinical pipeline &mdash; social work leads to the LCSW by a "
                "different route, and a school counseling credential is not a "
                "Board license at all." % (G.EXCLUDED_YEAR, FIRST),
        minw=860))

    o.append('<p class="pk-p">Two things worth sitting with. The clinical '
             "pipeline is up <b>%.0f%%</b> in eight years against <b>%.0f%%</b> "
             "for graduate education in California generally &mdash; so this "
             "is not a field growing with everything else, it is a field "
             "people are actively moving into. And <b>social work is flat</b>: "
             "%s in %d, %s in %d. The growth is entirely on the therapy and "
             "counseling side.</p>"
             % (WIDE_GROWTH, ALL_GROWTH, n(G.SERIES[FIRST]["440701"]), FIRST,
                n(G.SERIES[LAST]["440701"]), LAST))

    o.append(pk.callout(
        "What that looks like from inside the queue",
        ["There are <b>%s</b> people currently registered as associates in "
         "California across the three licenses, against <b>%s</b> licensed. "
         "Those associates are all looking for the same finite things: "
         "supervised hours, a supervisor with capacity, and an employer that "
         "can bill for them."
         % (n(AMFT + ASW + APCC), n(LMFT + LCSW + LPCC)),
         'Which counties are already crowded is <a href="%s">the county '
         "atlas</a>, and why an employer can bill for a pre-licensed "
         'clinician in some settings and not others is <a href="%s">a rule '
         "about Medi-Cal</a> rather than anything about you."
         % (ATLAS, HIRED)],
        big=n(AMFT + ASW + APCC)))
    o.append("</section>")

    # --------------------------------------------------------------- license
    o.append('<section class="pk-sec" id="license">')
    o.append('<p class="pk-k">Which of the three</p>')
    o.append('<h2 class="pk-h">Only one of them lets your practicum count.</h2>')
    o.append('<p class="pk-d">California licenses three kinds of master&rsquo;s'
             "-level therapist. People treat the choice as a matter of "
             "temperament. It is also a matter of statute, and the statutes "
             "are not the same.</p>")

    o.append(pk.table(
        ["", "LMFT", "LCSW", "LPCC"],
        [(["<b>Hours you may bank before the degree</b>",
           "<b>Up to 1,300 of the 3,000</b>", "None", "None"], "hi"),
         ["Where that is written",
          ("&sect;&thinsp;4980.43(c)(4)", "m"),
          ("&sect;&thinsp;4996.23(a)", "m"),
          ("&sect;&thinsp;4999.46(c)(1)", "m")],
         ["Practicum hours the degree statute requires",
          ("150 + 75", "f"), "Set by the accreditor, not this code",
          ("280", "f")],
         ["Licensed in California now", (n(LMFT), "f"), (n(LCSW), "f"),
          (n(LPCC), "f")],
         ["Associates registered now", (n(AMFT), "f"), (n(ASW), "f"),
          (n(APCC), "f")],
         (["<b>Associates per licensee</b>",
           ("<b>%.2f</b>" % (AMFT / float(LMFT)), "f"),
           ("<b>%.2f</b>" % (ASW / float(LCSW)), "f"),
           ("<b>%.2f</b>" % (APCC / float(LPCC)), "f")], "hi"),
         ["Registrations currently delinquent",
          ("%.1f%%" % D.DELINQUENCY["AMFT"]["pct"], "m"),
          ("%.1f%%" % D.DELINQUENCY["ASW"]["pct"], "m"),
          ("%.1f%%" % D.DELINQUENCY["APCC"]["pct"], "m")],
         ["California master's degrees a year in the matching field",
          (n(G.SERIES[LAST]["511505"]), "m"),
          (n(G.SERIES[LAST]["440701"]), "m"),
          (n(G.SERIES[LAST]["511508"] + G.SERIES[LAST]["422803"]), "m")]],
        caption="Counts are from the state&rsquo;s own licensee register as "
                "at %s. The degree-per-year row is indicative rather than "
                "exact: California programs file under several federal "
                "subject codes and a single one does not map cleanly onto a "
                "single license." % D.AS_AT,
        minw=760))

    o.append('<p class="pk-p">Read the last-but-one row. There are '
             "<b>%.2f</b> counselor associates for every licensed LPCC, "
             "against <b>%.2f</b> MFT associates per licensed MFT. The LPCC "
             "is California&rsquo;s newest license &mdash; it is still mostly "
             "a register of people who have not finished yet, which is also "
             "why <b>%.1f%%</b> of those registrations are delinquent against "
             "<b>%.1f%%</b> of licensed MFTs.</p>"
             % (APCC / float(LPCC), AMFT / float(LMFT),
                D.DELINQUENCY["APCC"]["pct"], D.DELINQUENCY["LMFT"]["pct"]))

    o.append(pk.numbered([
        ("1", "The 1,300 hours are the largest single difference.",
         'A California MFT student can accrue up to 1,300 of the 3,000 hours '
         "before the degree is awarded, of which no more than 750 may be "
         "counseling plus direct supervisor contact. "
         '<a href="%s" rel="nofollow noopener" target="_blank">'
         "&sect;&thinsp;4980.43(c)(4) and (5)</a>. The LPCC statute says "
         "&ldquo;3,000 postdegree hours&rdquo; and the LCSW statute says "
         "&ldquo;post-master&rsquo;s degree&rdquo;. Same practicum, same "
         'chair, same clients &mdash; <a href="%s">two of the three throw it '
         "away</a>." % (LEG % "4980.43", PRACTICUM)),
        ("2", "All three still need 104 weeks.",
         "Banking hours early shortens the hour count, not the calendar. "
         "Every one of the three requires the experience to span at least two "
         "years. What the 1,300 buys is slack in the period when you are also "
         "job hunting, not an earlier license."),
        ("3", "Employability is a billing rule, not a preference.",
         'Which settings can bill for a pre-licensed clinician at all is set '
         'by Medi-Cal, and it names associates by category. That is why '
         '<a href="%s">so many first jobs are county and county-contracted</a>, '
         "across all three licenses." % HIRED),
        ("4", "The LCSW is a different degree, not a different exam.",
         "It requires an MSW. If you are choosing between an MFT-track "
         "master's and an MSW you are choosing between two curricula and two "
         "job markets at the point of application, not at the point of "
         "licensure."),
    ]))
    o.append("</section>")

    # ----------------------------------------------------------------- clock
    o.append('<section class="pk-sec" id="clock">')
    o.append('<p class="pk-k">How long, honestly</p>')
    o.append('<h2 class="pk-h">Nobody does it in the advertised time.</h2>')
    o.append('<p class="pk-d">The programs quote the degree. The Board quotes '
             "the hours. Neither quotes the joins, and the joins are where "
             "the year goes.</p>")

    lmft_le = B.latest("lmft_le")
    lmft_cl = B.latest("lmft_cl")
    o.append(pk.table(
        ["Stage", "What it is", "What it actually takes"],
        [["The degree", "60&ndash;90 graduate units, six of them practicum",
          "2 to 3 years. One program on the list reports an average time to "
          "degree of 2.9 years against a published two-year roadmap."],
         ["Practicum inside it",
          "150 face-to-face hours plus 75, minimum, at an approved site",
          "12 to 18 months at 12&ndash;20 hours a week, alongside classes"],
         (["<b>Degree to registration</b>",
           "The Board must <b>receive</b> the associate application within 90 "
           "days of the degree date",
           "<b>%d days</b> to process an associate registration in the most "
           "recent published quarter &mdash; and it has been as long as %d"
           % (min(B.OLD_TIMES[0][1][-1], 999), max(B.OLD_TIMES[0][1]))], "hi"),
         ["The 3,000 hours", "At least 104 weeks, 40 hours a week maximum",
          "Two years is the floor and assumes full-time clinical work from "
          "week one. Part-time or unpaid stretches it."],
         ["Two exams",
          "Law and Ethics during the first registration, then the clinical "
          "exam at the end",
          "%d%% of first-time candidates passed the law and ethics exam and "
          "%d%% passed the clinical exam in the most recent quarter"
          % (lmft_le[3], lmft_cl[3])],
         ["Registration to license", "The license application itself",
          "%d days in the most recent published quarter for the LMFT"
          % B.OLD_TIMES[3][1][-1]]],
        caption="Processing times are the Board&rsquo;s own published "
                "figures. It changed how it measures them at Q2 FY 2025/26, "
                "so the two series are not spliced here &mdash; "
                "<a href=\"%s\">the processing-time page</a> keeps them "
                "apart and explains why." % TIMES,
        minw=760))

    o.append('<p class="pk-p">Added up, a realistic figure from first class to '
             "license is <b>five to six years</b> for somebody moving at a "
             "steady pace, and that assumes the practicum seat, the job and "
             "the supervisor all arrive when needed. The statutory floor is "
             "about four. The gap between the two is the part nobody "
             "advertises.</p>")
    o.append("</section>")

    # ------------------------------------------------------------------ cost
    o.append('<section class="pk-sec" id="cost">')
    o.append('<p class="pk-k">What it costs</p>')
    o.append('<h2 class="pk-h">%s to %s for the same license.</h2>'
             % (pk.money(TUI_LO["cost"]), pk.money(TUI_HI["cost"])))
    o.append('<p class="pk-d">Tuition for the degree, computed from each '
             "program&rsquo;s own published per-unit price and unit count, or "
             "from a total where the program states one. %s</p>"
             % TUITION_CAVEAT)

    rows = []
    for t in TUI[:5]:
        rows.append([pk.esc(t["inst"]), (pk.money(t["cost"]), "f"),
                     (str(t["units"] or "&mdash;"), "m"),
                     (pk.money(t["per_unit"]) if t["per_unit"] else "&mdash;", "m")])
    rows.append(((["&hellip; %d programs between &hellip;" % (len(TUI) - 10),
                   "", "", ""]), "mid"))
    for t in TUI[-5:]:
        rows.append([pk.esc(t["inst"]), (pk.money(t["cost"]), "f"),
                     (str(t["units"] or "&mdash;"), "m"),
                     (pk.money(t["per_unit"]) if t["per_unit"] else "&mdash;", "m")])
    o.append(pk.table(
        ["Program", "Tuition for the degree", "Units", "Per unit"], rows,
        caption="Tuition only. Fees, books, liability insurance, "
                "transportation to a placement and the Live Scan are on top, "
                "and none of them is trivial. The median of the %d is %s. "
                "Every figure links back to the program&rsquo;s own page on "
                "<a href=\"%s\">the program comparison</a>, where the source "
                "is recorded." % (len(TUI), pk.money(TUI_MED["cost"]), PROGRAMS),
        minw=680))

    o.append(pk.numbered([
        ("$0", "what the practicum year pays",
         "A trainee may not take money from a client and in most placements "
         "is not paid at all. It is also the year with the least room for "
         "other work, because the site wants 12 to 20 hours a week at fixed "
         "times."),
        ("3,000", "hours at whatever the associate job pays",
         'What those jobs pay in Los Angeles and the Bay Area is <a '
         'href="%s">on the associate pay page</a>; what a county job pays '
         'across all 58 counties is <a href="%s">from the State '
         "Controller&rsquo;s own file</a>. If any of those hours are asked of "
         'you unpaid, <a href="%s">the wage claim is a real one</a>.'
         % (PAY, COUNTY, UNPAID)),
        ("2", "exams, plus the registration and the license",
         'Board fees fell in July 2026 and <a href="%s">the fee page</a> '
         "carries the current schedule. They are the small number on this "
         "page, which is worth saying plainly &mdash; the cost of this path "
         "is tuition and forgone earnings, not paperwork." % FEES),
        ("?", "supervision, if your employer does not provide it",
         "An employer that supplies supervision is supplying something with a "
         "real market price. Two otherwise identical offers where one "
         "includes supervision and one does not are not the same offer, and "
         "that is worth pricing before signing."),
    ]))

    o.append(pk.callout(
        "The one that offsets it",
        ["Public service loan forgiveness asks only whether your employer is "
         "a government or qualifying nonprofit entity. It does not ask about "
         "your license, which means an associate at a county agency can be "
         "accruing qualifying payments from the first month &mdash; and "
         "California runs a loan repayment program that names registered "
         'associates directly. <a href="%s">Which employers qualify, on which '
         "test</a> is the whole of that page." % FORGIVE,
         'What a therapist&rsquo;s money looks like once licensed is <a '
         'href="%s">the cost-of-living page</a> and <a href="%s">the rate '
         "research</a>." % (COL, RATES)]))
    o.append("</section>")

    # ------------------------------------------------------------------- pay
    o.append('<section class="pk-sec" id="pay">')
    o.append('<p class="pk-k">What it pays</p>')
    o.append('<h2 class="pk-h">The same job pays %.1f times more in one '
             "California county than another.</h2>"
             % (CP.COUNTIES[0]["max_med"] / float(CP.COUNTIES[-1]["max_med"])))
    o.append('<p class="pk-d">County employment is where a large share of '
             "first jobs are, for the billing reason above, and it is the one "
             "part of this market with real published numbers rather than "
             "self-reported ones. These are what counties told the State "
             "Controller they paid.</p>")

    o.append(pk.table(
        ["", "Top of the published range", "County"],
        [(["<b>Highest</b>", (pk.money(CP.COUNTIES[0]["max_med"]), "f"),
           CP.COUNTIES[0]["county"]], "hi"),
         ["Median across the state",
          (pk.money(CP.YEAR_TOTALS[CP.YEARS[-1]]["max_med"]), "f"),
          "%d counties reporting" % CP.YEAR_TOTALS[CP.YEARS[-1]]["counties"]],
         ["Lowest", (pk.money(CP.COUNTIES[-1]["max_med"]), "f"),
          CP.COUNTIES[-1]["county"]]],
        caption="%s data. A published range is not an offer and not what any "
                "individual earns. The full table of every county, three "
                "years of movement, and the one county in California that "
                "publishes what it pays a pre-licensed clinician, is on "
                "<a href=\"%s\">the county pay page</a>."
                % (CP.YEARS[-1], COUNTY),
        minw=620))

    o.append('<p class="pk-p">Private practice is the other end and it is a '
             "different business rather than a better salary: you are "
             'buying your own insurance, chasing your own claims and '
             'carrying your own empty hours. <a href="%s">What insurers '
             "actually pay per session in California, against what private "
             'pay charges</a>, is the research that answers it.</p>' % RATES)
    o.append("</section>")

    # ------------------------------------------------------------- attrition
    o.append('<section class="pk-sec" id="attrition">')
    o.append('<p class="pk-k">Where people stop</p>')
    o.append('<h2 class="pk-h">Three places the Board can see people leaving.</h2>')
    o.append('<p class="pk-d">None of these is published as an attrition '
             "figure. They are the Board&rsquo;s own operational numbers, and "
             "read together they are the closest thing that exists to one.</p>")

    le_lo, le_hi = B.spread("lmft_le", 3)
    cl_lo, cl_hi = B.spread("lmft_cl", 3)
    o.append(pk.table(
        ["Signal", "The number", "What it means"],
        [["Applications that arrive deficient",
          ("%.1f%%" % B.DEFICIENCY_RATE, "f"),
          "Up from %.0f%% the previous quarter. A deficient application is "
          "not a rejection &mdash; it is weeks or months added while "
          "something is corrected, at the exact moment somebody is trying to "
          "start a job." % B.DEFICIENCY_RATE_PRIOR],
         ["First-time pass rate, LMFT law and ethics",
          ("%d&ndash;%d%%" % (le_lo, le_hi), "f"),
          "Across the seven quarters published. Roughly a quarter of "
          "first-time candidates do not pass on the first sitting."],
         (["<b>First-time pass rate, LMFT clinical exam</b>",
           ("<b>%d&ndash;%d%%</b>" % (cl_lo, cl_hi), "f"),
           "<b>The last gate, taken after the 3,000 hours are already "
           "done.</b> Failing it does not end anything, but it is the "
           "furthest anybody has to travel to hit a wall."], "hi"),
         ["Associate registrations currently delinquent",
          ("%.1f%% / %.1f%% / %.1f%%"
           % (D.DELINQUENCY["AMFT"]["pct"], D.DELINQUENCY["ASW"]["pct"],
              D.DELINQUENCY["APCC"]["pct"]), "m"),
          "MFT, social work and counselor associates respectively. A lapsed "
          "registration is not proof somebody quit &mdash; but against "
          "%.1f%% for licensed MFTs it is the clearest signal in the register "
          "that the associate years are where people fall out."
          % D.DELINQUENCY["LMFT"]["pct"]]],
        caption="Deficiency and exam figures are transcribed from Board "
                "meeting packets and are on <a href=\"%s\">the exam page</a> "
                "and <a href=\"%s\">the processing-time page</a> in full. "
                "Delinquency is counted from the state&rsquo;s licensee "
                "register as at %s." % (EXAMS, TIMES, D.AS_AT),
        minw=760))
    o.append("</section>")

    # ------------------------------------------------------------- questions
    o.append('<section class="pk-sec" id="questions">')
    o.append('<p class="pk-k">Before you apply</p>')
    o.append('<h2 class="pk-h">Eight questions with checkable answers.</h2>')
    o.append('<p class="pk-d">Not a readiness quiz. These are the ones where '
             "an admissions conversation either produces a specific answer or "
             "does not, and the difference tells you a great deal.</p>")

    o.append(pk.checklist("Ask the program, and write the answer down", [
        "<b>Who finds my practicum site?</b> %d of the %d programs on this "
        "site publish nothing about it. <a href=\"%s\">The comparison is "
        "here</a> &mdash; go in already knowing what they have said in public."
        % (P.COUNTS["not published"], P.N, PRACTICUM),
        "<b>Do you run your own clinic, and does every student get a seat in "
        "it?</b> %d of the %d have one. Owning a clinic and guaranteeing a "
        "seat are different claims." % (P.OWN_CLINIC, P.N),
        "<b>How many direct client contact hours before you will graduate "
        "me?</b> The published minimums run from %d to %d, and the state's "
        "floor for the MFT is 225." % (P.DCC_MIN, P.DCC_MAX),
        "<b>Is this degree Board-approved for the license I want, and for the "
        "second one?</b> A program built for both the LMFT and the LPCC asks "
        "for 280 practicum hours rather than 225, because the counselor "
        "statute does.",
        "<b>What is the total tuition, in dollars, for the whole degree?</b> "
        "Per-unit prices and unit counts are both published; the product is "
        "the number that matters and it ranges from %s to %s."
        % (pk.money(TUI_LO["cost"]), pk.money(TUI_HI["cost"])),
        "<b>What is your average time to degree, not your published "
        "roadmap?</b> At least one California program publishes both, and "
        "they differ by most of a year.",
        "<b>Where did last year's graduating cohort get their first jobs?</b> "
        "If the answer is general rather than specific, the program is not "
        "tracking it.",
        "<b>Can I do this part time while working?</b> The practicum is the "
        "constraint, not the classes &mdash; 12 to 20 hours a week at a site "
        "that sets the times.",
    ]))

    o.append(pk.callout(
        "What this page is not",
        ["It does not say whether to do this. Everything above is a figure "
         "with a source beside it, assembled because nobody had assembled it, "
         "and the decision belongs to the person reading.",
         'If the answer is yes, the next two pages are <a href="%s">how the '
         'practicum year actually works</a> and <a href="%s">the route to the '
         "license end to end</a>." % (PRACTICUM, BECOME)]))
    o.append("</section>")

    # --------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("How many are coming", [
            ("IPEDS Completions, California master's degrees by field, %d to "
             "%d, read through the Urban Institute Education Data API"
             % (FIRST, LAST), G.SOURCE),
            ("IPEDS at the National Center for Education Statistics, the "
             "underlying federal survey", G.NCES),
        ]),
        ("Who is already here", [
            ("The California licensee register, all %s records as at %s"
             % (n(D.TOTAL), D.AS_AT), D.SOURCE),
            ("The same register counted by county",
             "https://therapistsupport.org/%s" % ATLAS),
        ]),
        ("The Board's own operating numbers", [
            ("Board of Behavioral Sciences meeting packets, %d quarters of "
             "licensing and examination reporting" % len(B.QUARTERS),
             B.MEETINGS_INDEX),
            ("Seven quarters of pass rates for all seven exams",
             "https://therapistsupport.org/%s" % EXAMS),
            ("How long each application type is taking",
             "https://therapistsupport.org/%s" % TIMES),
        ]),
        ("The statute", [
            ("&sect;&thinsp;4980.43 &mdash; the LMFT's 3,000 hours and the "
             "1,300 that may precede the degree", LEG % "4980.43"),
            ("&sect;&thinsp;4996.23 &mdash; the LCSW's post-master's hours",
             LEG % "4996.23"),
            ("&sect;&thinsp;4999.46 &mdash; the LPCC's postdegree hours",
             LEG % "4999.46"),
        ]),
        ("Programs, pay and cost", [
            ("The %d California MFT programs, with tuition and practicum "
             "sources for each" % P.N,
             "https://therapistsupport.org/%s" % PROGRAMS),
            ("The practicum year, and who finds your site",
             "https://therapistsupport.org/%s" % PRACTICUM),
            ("What county jobs pay, from the State Controller's file",
             "https://therapistsupport.org/%s" % COUNTY),
            ("What associate jobs pay in Los Angeles and the Bay Area",
             "https://therapistsupport.org/%s" % PAY),
        ]),
    ], note="%s Degree counts are master's degrees awarded by institutions "
            "located in California and include people who then leave the "
            "state, so they overstate the number entering the California "
            "workforce &mdash; by how much is not published. Licensee counts "
            "are a snapshot of a register, not a flow. Board figures are "
            "transcribed from published meeting packets. <b>Nothing here is "
            "career, legal or financial advice</b>, and no figure on this "
            "page is a prediction about any individual." % TUITION_CAVEAT)
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Becoming a therapist in California: the numbers before you decide",
    "How many people California graduates into therapy each year, which of "
    "the three licenses banks your practicum hours, what the degree costs, "
    "what the jobs pay, and where the Board can see people stopping.",
    "licensure", "reference",
    "Should I retrain as a therapist in California?",
    "The pipeline, the three licenses compared on statute rather than "
    "temperament, an honest clock, the real cost and the visible attrition",
    "%s clinical master's a year, up %.0f%% since %d"
    % (n(G.WIDE_LATEST), WIDE_GROWTH, FIRST),
    weight=4)


def main():
    print("becoming a therapist, from another career")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources" % (PAGE, n(len(html)), nsrc))

    bad = pk.check_page(p, [
        ("the pipeline growth finding", "grew %.0f%%" % WIDE_GROWTH),
        ("the pre-degree hours finding", "Up to 1,300 of the 3,000"),
        ("the tuition caveat", "not the range across California"),
        ("the not-advice statement", "It does not say whether to do this"),
        ("the published-range caveat", "not what any individual earns"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # The page exists to hand somebody figures, not a verdict. Anything that
    # reads as a recommendation is the one failure mode that would matter.
    for phrase in ("you should become", "you should not become",
                   "we recommend", "the right choice for you",
                   "is a great career", "is a bad career",
                   "do not do this", "you will succeed"):
        if phrase in art.lower():
            print("GUARD: the page tells the reader what to choose: %r" % phrase)
            bad += 1

    # Every year in the series must be printed, or the growth claim is being
    # made over a table the reader cannot check.
    for y in G.YEARS:
        if str(y) not in art:
            print("GUARD: %d is missing from the pipeline table" % y)
            bad += 1
    if str(G.EXCLUDED_YEAR) not in art:
        print("GUARD: the excluded year is not disclosed")
        bad += 1

    # The three statutory citations are the spine of the license comparison.
    for needle in ("4980.43(c)(4)", "4996.23(a)", "4999.46(c)(1)"):
        if needle not in art:
            print("GUARD: %s is not cited" % needle)
            bad += 1

    # The tuition caveat has to sit near the tuition figure, not in a footnote
    # a thousand words away.
    i_num = art.find(pk.money(TUI_HI["cost"]))
    i_cav = art.find("not the range across California")
    if i_num < 0 or i_cav < 0 or abs(i_num - i_cav) > 3000:
        print("GUARD: the tuition caveat has drifted away from the figure")
        bad += 1

    for w in pk.spelling(s):
        print("GUARD: British spelling %r" % w)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
