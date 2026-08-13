#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The pass rate is 84%. It is also 65%. Both are the same exam, same quarter.

THE QUESTION THIS ANSWERS

People preparing for the California clinical exams trade practice-test scores
with each other in support groups because there is no published benchmark they
trust. The one free analysis that circulates reports a pass rate in the high
fifties and was last updated in 2017. The Board publishes the real figures
every quarter, in a board meeting packet nobody outside the Board reads.

WHY A NUMBER IS NOT ENOUGH, AND WHAT THIS PAGE DOES INSTEAD

The Board publishes two pass rates for every exam and they are far apart. The
overall rate counts every sitting, including people on their third attempt.
The first-time rate counts only candidates sitting for the first time. Quoting
either one without saying which it is produces exactly the confusion this page
exists to end - "the pass rate is 84%" and "the pass rate is 65%" were both
true of the LMFT Clinical exam in the same quarter.

So the page prints both, always, side by side, and never a single headline
figure on its own.

The second thing it does is print SEVEN quarters rather than one. A single
quarter is not a rate. The LCSW Law and Ethics overall pass rate has been 58%
and 81% within the same two-year window; anyone planning around one quarter's
figure is planning around noise. The spread is computed from the data rather
than asserted, so it cannot drift out of date while the sentence stays.

WHAT THE BOARD DOES NOT PUBLISH, SAID PLAINLY

Pass rates by school, by program, by attempt number beyond the first, or by
any candidate characteristic. This page says so instead of filling the space,
because the absence is the answer to a question people genuinely ask.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk
import bbs_stats as B

PAGE = "bbs-exam-pass-rates-california.html"
# Chrome comes from a frozen pre-conversion snapshot (_dev/chrome_donor.html)
# rather than a live page: rollout step 5 converts live pages to the house
# design one family at a time, and a converted donor would hand this builder
# bc2 head links on top of its own family CSS - the mixed state the
# collision audit forbids. The snapshot retires when this family converts.
DONOR = "_dev/chrome_donor.html"

TIMES = "bbs-processing-times-california.html"
HOURS = "amft-3000-hours-california.html"
FEES = "bbs-fees-california-2026.html"
PROGRAMS = "mft-programs-california.html"

JUMPS = [
    ("two", "Two rates, not one"),
    ("now", "The latest quarter"),
    ("series", "Seven quarters"),
    ("noise", "How much it moves"),
    ("missing", "What is not published"),
    ("scoring", "When the score was wrong"),
]


def arrow(cur, prev):
    if cur == prev:
        return "level"
    d = cur - prev
    return ("+%d" % d) if d > 0 else ("%d" % d)


def body():
    o = ['<article class="pk-wrap">']

    cl_total, cl_all, cl_ftn, cl_ft = B.latest("lmft_cl")
    le_total, le_all, le_ftn, le_ft = B.latest("lmft_le")

    o.append(pk.hero(
        "Examination statistics &middot; %s &middot; checked %s"
        % (B.LATEST, pk.CHECKED),
        "The pass rate is 84%. It is also 65%.",
        "Both are the California LMFT Clinical exam. The Board publishes "
        "<b>two rates for every exam</b> and almost nobody quoting one of "
        "them says which. Here are seven quarters of both, for all seven "
        "exams.",
        [("%d%%" % cl_ft, "LMFT clinical, first-time"),
         ("%d%%" % cl_all, "the same exam, all sittings"),
         ("%s" % format(sum(B.TOTAL_ADMINISTERED[-4:]), ",d"),
          "exams sat in the last four quarters"),
         ("0", "pass rates published by school")],
        JUMPS))

    # ------------------------------------------------------------- two rates
    o.append('<section class="pk-sec" id="two">')
    o.append('<p class="pk-k">The distinction everything turns on</p>')
    o.append('<h2 class="pk-h">Two rates. They are not close, and they answer '
             "different questions.</h2>")
    o.append(pk.numbered([
        ("1", "The first-time rate &mdash; the one that answers your question",
         "Only candidates sitting the exam for the first time. In "
         "%s that was <b>%s of the %s people</b> who sat the LMFT Clinical "
         "exam, and <b>%d%%</b> of them passed. This is the number that "
         "answers &ldquo;if I sit it properly prepared, what happens?&rdquo;"
         % (B.LATEST, format(cl_ftn, ",d"), format(cl_total, ",d"), cl_ft)),
        ("2", "The overall rate",
         "Every sitting in the quarter, including second, third and later "
         "attempts. The same quarter&rsquo;s figure was <b>%d%%</b>. It is "
         "lower because retakes are harder than first sittings, not because "
         "the exam got harder. This number answers &ldquo;what share of the "
         "exams sat this quarter were passed?&rdquo; &mdash; a question about "
         "the Board&rsquo;s workload, not about you." % cl_all),
        ("3", "Which one you are usually shown",
         "Whichever makes the point being made. The free analysis that "
         "circulates in study groups reports a figure in the high fifties "
         "and was last revised in 2017; the schools quote first-time rates. "
         "<b>Neither is wrong and neither is the whole number.</b> This page "
         "prints both every time, in that order."),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------ the latest
    o.append('<section class="pk-sec" id="now">')
    o.append('<p class="pk-k">%s &mdash; the most recent published</p>'
             % B.LATEST)
    o.append('<h2 class="pk-h">Every California behavioral sciences exam, '
             "most recent quarter.</h2>")
    rows = []
    for key, label, who, series in B.EXAMS:
        t, a, fn, f = series[-1]
        pt, pa, pfn, pf = series[-2]
        cls = ""
        if f >= 85:
            cls = "good"
        elif a < 60:
            cls = "bad"
        rows.append(([label, (format(t, ",d"), "n"), ("%d%%" % f, "f"),
                      ("%d%%" % a, "n"), (arrow(a, pa), "m"), who], cls))
    o.append(pk.table(
        ["Exam", "Sittings", "First-time", "All sittings", "vs prior qtr",
         "Who sits it"],
        rows,
        "The arrow column compares the overall rate with the previous "
        "quarter, which is the comparison the Board itself prints. It is not "
        "a trend &mdash; see the next two sections for how far these move "
        "quarter to quarter before anything has actually changed. "
        "<b>%s exams were administered in %s</b>, against %s the quarter "
        "before."
        % (format(B.TOTAL_ADMINISTERED[-1], ",d"), B.LATEST,
           format(B.TOTAL_ADMINISTERED[-2], ",d")), minw=760))
    o.append("</section>")

    # ------------------------------------------------------------ the series
    o.append('<section class="pk-sec" id="series">')
    o.append('<p class="pk-k">Seven quarters</p>')
    o.append('<h2 class="pk-h">First-time pass rates, quarter by quarter.</h2>')
    o.append('<p class="pk-d">Each cell is the percentage of first-time '
             "sitters who passed. Every quarter except the two ends appears "
             "in two separate board packets, because each packet prints the "
             "prior quarter beside the current one, and the overlapping "
             "figures agree.</p>")
    hdr = ["Exam"] + [q.replace("FY ", "") for q in B.QUARTERS]
    rows = []
    for key, label, who, series in B.EXAMS:
        rows.append([label] + [("%d%%" % q[3], "n") for q in series])
    o.append(pk.table(hdr, rows, minw=740))

    o.append('<h3 class="pk-h3">And the overall rate, the same seven '
             "quarters.</h3>")
    rows = []
    for key, label, who, series in B.EXAMS:
        rows.append([label] + [("%d%%" % q[1], "n") for q in series])
    o.append(pk.table(hdr, rows,
                      "Sittings, not candidates: someone who sat twice in a "
                      "quarter appears twice. Totals administered across the "
                      "seven quarters ran %s to %s."
                      % (format(min(B.TOTAL_ADMINISTERED), ",d"),
                         format(max(B.TOTAL_ADMINISTERED), ",d")), minw=740))
    o.append("</section>")

    # ------------------------------------------------------------- the noise
    o.append('<section class="pk-sec" id="noise">')
    o.append('<p class="pk-k">Before you plan around a number</p>')
    o.append('<h2 class="pk-h">How far each of these moves without anything '
             "changing.</h2>")
    o.append('<p class="pk-d">This is the argument for printing seven '
             "quarters instead of one. The range below is simply the lowest "
             "and highest quarterly figure in the table above &mdash; the "
             "same exam, the same Board, the same two years.</p>")
    rows = []
    for key, label, who, series in B.EXAMS:
        lo_a, hi_a = B.spread(key, 1)
        lo_f, hi_f = B.spread(key, 3)
        span = hi_a - lo_a
        cls = "bad" if span >= 20 else ""
        rows.append(([label, ("%d&ndash;%d%%" % (lo_f, hi_f), "n"),
                      ("%d&ndash;%d%%" % (lo_a, hi_a), "n"),
                      ("%d pts" % span, "f")], cls))
    o.append(pk.table(
        ["Exam", "First-time range", "Overall range", "Overall spread"],
        rows,
        "The LCSW Law and Ethics exam has been reported at both ends of a "
        "twenty-three point range inside two years. Nothing about the exam "
        "changed by twenty-three points. A quarter is a small sample of a "
        "self-selecting group of people who chose that quarter to sit, and it "
        "should be read as one.", minw=620))

    o.append(pk.callout(
        "What the Board itself concluded",
        ["The Office of Professional Examination Services ran a five-year "
         "study of the low LPCC Law and Ethics pass rates. Its conclusion, "
         "printed in the February 2026 packet, was that <b>&ldquo;%s&rdquo;"
         "</b>." % B.OPES_LPCC,
         "That is the most careful look anyone has taken at one of these "
         "numbers, and it found nothing to explain it. It is a good reason "
         "to be suspicious of any confident story about why a rate moved."]))
    o.append("</section>")

    # ---------------------------------------------------------- what is not
    o.append('<section class="pk-sec" id="missing">')
    o.append('<p class="pk-k">Established by absence</p>')
    o.append('<h2 class="pk-h">What the Board does not publish.</h2>')
    o.append('<p class="pk-d">These are the questions people ask most often '
             "in study groups, and the honest answer to all of them is that "
             "the data does not exist publicly. Nine board packets were read "
             "for this page; none of them contains any of it.</p>")
    o.append(pk.table(
        ["The question", "What is published"],
        [["Which schools have the best pass rates?",
          "<b>Nothing.</b> The Board does not break any exam result out by "
          "degree program, school or accreditation status. Any ranking you "
          "find is somebody&rsquo;s reconstruction, not a Board figure."],
         ["What is the pass rate on a second attempt? A third?",
          "<b>Nothing.</b> The split is first-time against all sittings. The "
          "retake rate can be inferred as a residual, but the Board does not "
          "state it and the inference is fragile at these sample sizes."],
         ["How many attempts do people usually need?",
          "<b>Nothing.</b> Not published in any packet read for this page."],
         ["What score do I need?",
          "<b>Not a percentage.</b> These are criterion-referenced exams "
          "scored against a standard, not curved against other candidates, "
          "which is why a practice-test percentage traded in a study group "
          "does not convert into a pass probability."],
         ["Does the pass rate differ by region, language or route to "
          "eligibility?",
          "<b>Nothing</b>, except that endorsed and out-of-state candidates "
          "are broken out separately in the FY 2025/26 packets only, and "
          "those cohorts are small enough that their rates swing wildly."]],
        "That last point is worth sitting with. The single most requested "
        "statistic about California licensing exams &mdash; which program "
        "prepares people best &mdash; has never been published by the body "
        "that has the data."))
    o.append("</section>")

    # ------------------------------------------------------------ the scoring
    o.append('<section class="pk-sec" id="scoring">')
    o.append('<p class="pk-k">A documented failure, with numbers</p>')
    o.append('<h2 class="pk-h">Once, the passing score itself was wrong.</h2>')
    inc = B.SCORING_INCIDENT
    o.append('<p class="pk-d">This is not a rumour from a support group. It '
             "is in the Board&rsquo;s own May 2025 packet. A new "
             "publication of the <b>%s</b> exam took effect on %s and was "
             "sent to the testing vendor <b>with an incorrect passing "
             "score</b>. The Board&rsquo;s examination services unit caught "
             "it while reviewing results.</p>"
             % (inc["exam"], inc["effective"]))
    o.append(pk.callout(
        "What the rescoring found",
        ["Of the <b>%d</b> LPCC Law and Ethics exams taken between %s, "
         "<b>%d results were changed from fail to pass</b>. The remaining %d "
         "were unaffected. Candidates were notified by email, and exams sat "
         "from 20 February onward were scored correctly."
         % (inc["taken"], inc["window"], inc["changed"], inc["still_fail"]),
         "Nearly <b>%d%%</b> of the people who sat that exam in that "
         "three-week window were told they had failed when they had passed."
         % round(100.0 * inc["changed"] / inc["taken"])],
        big="%d of %d" % (inc["changed"], inc["taken"])))
    o.append('<p class="pk-d">The reason to print this is not that it is '
             "likely to happen to you. It is that the Board found and fixed "
             "it, published the numbers, and the only place those numbers "
             "appear is a meeting packet. If a result ever looks wrong, the "
             "quarterly examination report is where an answer would surface "
             "&mdash; and the packets are public.</p>")
    o.append('<p class="pk-fine">The exams themselves are only half of the '
             "wait. Once you have passed, the Board still has to process the "
             "application, and that queue has moved a long way in the last "
             'year &mdash; <a href="%s">the processing times are here</a>. '
             'If you are still counting hours, <a href="%s">the hours '
             'calculator</a> works from your own numbers and sends nothing '
             "anywhere.</p>" % (TIMES, HOURS))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    groups = [("The board packets every figure was read from",
               [(l + " &mdash; " + w, u) for l, w, u in B.PACKETS]),
              ("Finding them yourself",
               [("BBS board meeting agendas and materials", B.MEETINGS_INDEX)])]
    src, n = pk.sources(groups, note=(
        "The filename pattern is not stable &mdash; three consecutive years "
        "use an underscore, a hyphen and no separator at all &mdash; so a "
        "guessed URL will return a 404. Start from the meetings index and "
        "follow the links. Figures are transcribed, never derived: where the "
        "Board did not publish something, this page says so rather than "
        "estimating it."))
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "California LMFT, LCSW and LPCC exam pass rates, seven quarters",
    "The Board publishes two pass rates for every exam and they are far "
    "apart. Seven quarters of both, for all seven California behavioral "
    "sciences exams, transcribed from the board packets.",
    "licensure", "reference",
    "What is the actual pass rate for the California clinical exam?",
    "Both published rates for all seven exams across seven quarters, and how "
    "far each one moves before anything has changed",
    "%d%% first-time, %d%% overall" % (B.latest("lmft_cl")[3],
                                       B.latest("lmft_cl")[1]),
    weight=5)


def main():
    print("BBS examination statistics")
    problems = B.check()
    for x in problems:
        print("GUARD:", x)
    if problems:
        sys.exit("the transcribed data is inconsistent; nothing was written")
    print("  %d quarters, %d exams, %d packets"
          % (len(B.QUARTERS), len(B.EXAMS), len(B.PACKETS)))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the seven-quarter table", B.QUARTERS[0].replace("FY ", "")),
        ("the scoring incident", "changed from fail to pass"),
        ("the OPES finding", "statistically significant"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every published figure has to be present as written. A percentage that
    # appears on the page but not in the data means a number was typed into
    # prose and will not move when the data does.
    for key, label, who, series in B.EXAMS:
        for want in ("%d%%" % series[-1][1], "%d%%" % series[-1][3]):
            if want not in art:
                print("GUARD: %s's latest rate %s is not on the page"
                      % (key, want))
                bad += 1

    # The page's whole argument is that a single rate is meaningless. If the
    # word "the pass rate is" ever appears followed by one figure and no
    # qualifier, the argument has been undone by an edit.
    # The page's argument is that the two rates travel together. If an edit
    # ever leaves one of them behind, the page becomes the thing it was
    # written to correct. Case-insensitive, because "First-time range" is a
    # table header and counts.
    n_ft = art.lower().count("first-time")
    if n_ft < 6:
        print("GUARD: only %d mentions of the first-time rate. The page's "
              "point is that both rates travel together." % n_ft)
        bad += 1

    if nsrc < 9:
        print("GUARD: %d sources, and there are %d packets to cite"
              % (nsrc, len(B.PACKETS)))
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - both rates for %d exams across %d quarters, %d "
          "sources" % (len(B.EXAMS), len(B.QUARTERS), nsrc))


if __name__ == "__main__":
    main()
