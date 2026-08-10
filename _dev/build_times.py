#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""You passed. Now how long? - the Board's own processing times, as a series.

THE QUESTION THIS ANSWERS

"I passed my clinical exam - how long until the license actually shows up?"
The answers in support groups are anecdotes: somebody's took three weeks,
somebody's took five months, and the thread ends without anyone knowing which
is typical. The Board publishes the answer quarterly, in a licensing report
inside a board meeting packet.

THE FINDING

Registration got faster and licensure got much slower, in the same year.

An AMFT registration for a clean application was processed in 15 calendar days
in the most recent published quarter, down from 18 a year earlier. Over the
same year an LMFT license went from 54 days to 96, and an LCSW license from 48
to 88. Those are the Board's own figures, printed side by side in its own
report, and nobody has written them down where a licensee would find them.

THE TRAP THIS PAGE IS BUILT AROUND

The Board changed how it measures at Q2 FY 2025/26. Before that it published
one number covering every application processed; from Q2 it splits approved
from deficient. The Feb 2026 packet backfills the year-ago quarter on the new
basis and gets AMFT 29 where the older packets published 45 for that same
quarter. Both are correct - they measure different things.

Any page that draws one line through those two series shows a dramatic
improvement that did not happen. This one prints them as two tables with the
break stated between them, which is less satisfying and is what the data
supports.

WHAT IS DELIBERATELY NOT HERE

A prediction of how long yours will take. A quarterly mean is not a promise,
and the single biggest determinant is not in the Board's control or this
page's: whether the application goes in complete. That is why the deficient
column is on the page at all.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk
import bbs_stats as B

PAGE = "bbs-processing-times-california.html"
DONOR = "hiring-first-associate-california-therapist.html"

EXAMS_PAGE = "bbs-exam-pass-rates-california.html"
HOURS = "amft-3000-hours-california.html"
FEES = "bbs-fees-california-2026.html"

JUMPS = [
    ("now", "The current numbers"),
    ("shift", "What changed this year"),
    ("deficient", "The cost of a gap"),
    ("break", "Why the old figures differ"),
    ("volume", "How much work it is"),
]


def approved(label):
    for row in B.NEW_APPROVED:
        if row[0] == label:
            return row
    raise KeyError(label)


def deficient(label):
    for row in B.DEFICIENT:
        if row[0] == label:
            return row
    raise KeyError(label)


def pct_change(old, new):
    return int(round(100.0 * (new - old) / old))


def body():
    o = ['<article class="pk-wrap">']

    lmft = approved("LMFT license")
    lcsw = approved("LCSW license")
    amft = approved("AMFT registration")
    asw = approved("ASW registration")

    o.append(pk.hero(
        "Processing times &middot; %s &middot; checked %s"
        % (B.LATEST, pk.CHECKED),
        "You passed. Now how long?",
        "The Board publishes this every quarter and nobody reads it. In the "
        "last year <b>getting registered got faster and getting licensed got "
        "much slower</b> &mdash; an LMFT license went from %d days to %d."
        % (lmft[3], lmft[4]),
        [("%d days" % lmft[4], "LMFT license, clean application"),
         ("%d days" % lcsw[4], "LCSW license, clean application"),
         ("%d days" % amft[4], "AMFT registration"),
         ("%s%%" % pct_change(lmft[3], lmft[4]), "change in an LMFT license, "
          "year over year")],
        JUMPS))

    # ---------------------------------------------------------------- current
    o.append('<section class="pk-sec" id="now">')
    o.append('<p class="pk-k">%s, against the same quarter a year earlier</p>'
             % B.LATEST)
    o.append('<h2 class="pk-h">Calendar days, for an application with nothing '
             "wrong with it.</h2>")
    o.append('<p class="pk-d">These are the Board&rsquo;s figures for '
             "<b>approved applications with no deficiencies</b> &mdash; the "
             "best case. Both columns come from the same report, which prints "
             "the year-ago quarter beside the current one, so the comparison "
             "is the Board&rsquo;s own and not this page&rsquo;s "
             "arithmetic.</p>")
    rows = []
    for label, q2a, q2b, q3a, q3b in B.NEW_APPROVED:
        ch = pct_change(q3a, q3b)
        cls = "bad" if ch >= 25 else ("good" if ch <= -25 else "")
        rows.append(([label, ("%d" % q3a, "n"), ("%d" % q3b, "f"),
                      ("%s%d%%" % ("+" if ch > 0 else "", ch), "m")], cls))
    o.append(pk.table(
        ["Application", "A year earlier", B.LATEST, "Change"],
        rows,
        "Registrations are moving in one direction and licenses in the "
        "other. The Board attributes the licensing side to staffing "
        "constraints and cross-training. Read these as the shape of the "
        "queue in a quarter, not as a promise about your file &mdash; a mean "
        "of several hundred applications says nothing about any one of "
        "them.", minw=560))
    o.append("</section>")

    # ----------------------------------------------------------------- shift
    o.append('<section class="pk-sec" id="shift">')
    o.append('<p class="pk-k">The thing worth knowing</p>')
    o.append('<h2 class="pk-h">Registration sped up. Licensure did the '
             "opposite.</h2>")
    o.append(pk.numbered([
        ("1", "Getting registered is now quick",
         "An <b>ASW registration went from %d days to %d</b> and an APCC "
         "registration from %d to %d over the year. If you are a new "
         "graduate waiting to start accruing hours, that wait is a fraction "
         "of what it was, and it is now short enough that the binding "
         "constraint is your transcript, not the Board."
         % (asw[3], asw[4], approved("APCC registration")[3],
            approved("APCC registration")[4])),
        ("2", "Getting licensed is not",
         "An <b>LMFT license went from %d days to %d</b>, and an LCSW "
         "license from %d to %d. That is roughly three months of waiting "
         "after you have passed the exam, paid the fee and submitted a "
         "complete application. Plan the gap between the last supervised "
         "session and the first independent one around three months, not "
         "three weeks." % (lmft[3], lmft[4], lcsw[3], lcsw[4])),
        ("3", "LPCC and LEP are a different queue",
         "An LPCC license was processed in %d days and an LEP license in "
         "%d, both broadly stable. The volumes are far smaller, which is "
         "the likeliest explanation and is not one the Board has given."
         % (approved("LPCC license")[4], approved("LEP license")[4])),
    ]))
    o.append("</section>")

    # -------------------------------------------------------------- deficient
    o.append('<section class="pk-sec" id="deficient">')
    o.append('<p class="pk-k">The one variable you control</p>')
    o.append('<h2 class="pk-h">What a missing document costs you.</h2>')
    o.append('<p class="pk-d">A &ldquo;deficient&rdquo; application is one '
             "the Board had to come back to you about &mdash; a missing "
             "transcript, an unsigned verification, a gap in the hours. It "
             "is not a rejection. It is a letter, a wait for your reply, and "
             "a return to the back of somebody&rsquo;s queue.</p>")
    rows = []
    for label, q2a, q2b in B.DEFICIENT:
        app = approved(label)
        mult = q2b / float(app[2]) if app[2] else 0
        cls = "bad" if mult >= 3 else ""
        rows.append(([label, ("%d" % app[2], "n"), ("%d" % q2b, "f"),
                      ("%.1f&times;" % mult, "m")], cls))
    o.append(pk.table(
        ["Application", "Approved, clean", "Deficient", "Multiple"],
        rows,
        "Both columns are Q2 FY 2025/26, the only quarter for which the "
        "Board published both. <b>The May 2026 report dropped the deficient "
        "table entirely</b>, so there is no more recent figure and this page "
        "will not invent one. The LEP figure of %d days is an artifact the "
        "Board explains itself: %s."
        % (deficient("LEP license")[2], B.LEP_OUTLIER), minw=560))

    o.append(pk.callout(
        "How often it happens",
        ["In Q1 FY 2025/26 the Board put the licensing deficiency rate at "
         "<b>%s%%</b>, up from about %d%% the quarter before. Roughly three "
         "applications in ten come back."
         % (format(B.DEFICIENCY_RATE, ".2f"), int(B.DEFICIENCY_RATE_PRIOR)),
         "Which makes the deficient column above the more honest planning "
         "number for a lot of people, and makes the checklist below worth "
         "more than any amount of refreshing BreEZe."]))

    o.append(pk.checklist(
        "The things that most often send an application back",
        ["<b>Transcripts that have not arrived yet.</b> The Board&rsquo;s "
         "own explanation for a spike in deficient registrations was "
         "graduation-season timing &mdash; degrees conferred after the "
         "application went in.",
         "<b>An experience verification the supervisor has not signed</b>, "
         "or has signed in a way the form does not accept. The Board does "
         "accept an electronic signature; it does not accept a typed name.",
         "<b>Hours that do not reconcile</b> between the weekly logs and the "
         "verification total.",
         "<b>A registration that lapsed mid-associateship</b>, leaving a gap "
         "the hours cannot cross.",
         "<b>Paper rather than BreEZe.</b> The Board says online filing "
         "saves weeks against a paper application, and does not quantify it "
         "further &mdash; so treat that as a direction, not a number."]))
    o.append("</section>")

    # ------------------------------------------------------------- the break
    o.append('<section class="pk-sec" id="break">')
    o.append('<p class="pk-k">If you have seen different figures</p>')
    o.append('<h2 class="pk-h">The Board changed how it measures, and the two '
             "series do not join.</h2>")
    o.append('<p class="pk-d">Through Q1 FY 2025/26 the Board published a '
             "single processing time per application type, covering every "
             "application it processed. From Q2 FY 2025/26 it publishes "
             "approved and deficient separately. Those measure different "
             "things, and the older numbers are still in circulation.</p>")
    hdr = ["Application"] + [q.replace("FY ", "") for q in B.OLD_QUARTERS]
    rows = [[label] + [("%d" % v, "n") for v in series]
            for label, series in B.OLD_TIMES]
    o.append(pk.table(hdr, rows,
                      "The old basis: all applications processed, in calendar "
                      "days, Q1 FY 2024/25 to Q1 FY 2025/26.", minw=620))

    q2 = "Q2 FY 24/25"
    o.append(pk.callout(
        "The same quarter, measured two ways",
        ["For <b>%s</b>, the packets published in 2025 reported an AMFT "
         "registration at <b>%d days</b> on the old basis. The February 2026 "
         "packet, backfilling the same quarter on the new basis, reports "
         "<b>%d days</b>."
         % (q2, dict(B.OLD_TIMES)["AMFT registration"][1],
            approved("AMFT registration")[1]),
         "Neither figure is wrong. One includes the applications that had "
         "something missing and one does not. <b>Draw a single line through "
         "them and you get a fifteen-day improvement that never "
         "happened</b> &mdash; which is why this page prints two tables and "
         "a paragraph instead of one chart."]))
    o.append("</section>")

    # ------------------------------------------------------------- the volume
    o.append('<section class="pk-sec" id="volume">')
    o.append('<p class="pk-k">Context for the queue</p>')
    o.append('<h2 class="pk-h">How much of this there is.</h2>')
    v = B.VOLUMES
    o.append(pk.table(
        ["In %s" % B.LATEST, "Received", "Processed", "A year earlier, "
         "received"],
        [["Registrations &mdash; AMFT, ASW, APCC",
          (format(v["reg_received"], ",d"), "n"),
          (format(v["reg_processed"], ",d"), "n"),
          (format(v["reg_received_prior"], ",d"), "n")],
         ["Licenses &mdash; LMFT, LCSW, LPCC, LEP",
          (format(v["lic_received"], ",d"), "n"),
          (format(v["lic_processed"], ",d"), "n"),
          (format(v["lic_received_prior"], ",d"), "n")]],
        "Licensing applications processed rose %s%% year over year while the "
        "time each one took nearly doubled, which is the shape of a queue "
        "clearing faster than it is growing but from further behind."
        % format(100.0 * (v["lic_processed"] - v["lic_processed_prior"])
                 / v["lic_processed_prior"], ".1f"), minw=560))

    rows = []
    for name, count, growth in B.POPULATION:
        rows.append([name, (format(count, ",d"), "f"),
                     ("+%s%%" % format(growth, ".2f"), "m") if growth
                     else ("&mdash;", "m")])
    o.append(pk.table(
        ["Who is on the register", "Number", "Year on year"],
        rows,
        "<b>%s people</b> hold a California behavioral sciences license or "
        "registration, up %s%% on a year earlier. LPCC is growing at nearly "
        "%d%% a year from a small base; the registration populations are "
        "reported without a growth figure."
        % (format(B.POPULATION_TOTAL, ",d"),
           format(B.POPULATION_GROWTH, ".2f"), int(B.POPULATION[2][2])),
        minw=460))

    o.append('<p class="pk-fine">Everything on this page is transcribed from '
             "the board meeting packets listed below and nothing is derived "
             "except the percentage changes, which are computed from the two "
             "figures printed either side of them. If you are still counting "
             'hours rather than waiting on a license, <a href="%s">the hours '
             "calculator</a> works from your own numbers; if you are waiting "
             'on a result rather than a license, <a href="%s">the exam '
             "statistics are here</a>.</p>" % (HOURS, EXAMS_PAGE))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    lic = [(l + " &mdash; " + w, u) for l, w, u in B.PACKETS
           if "icens" in w or "egistration" in w]
    src, n = pk.sources(
        [("The board packets every figure was read from", lic),
         ("Finding them yourself",
          [("BBS board meeting agendas and materials", B.MEETINGS_INDEX),
           ("BreEZe, where an application is filed and its status shown",
            "https://www.breeze.ca.gov/")])],
        note="The Board reports a quarter roughly two months after it ends, "
             "so the most recent published figure is always a quarter or so "
             "old. Where a table was discontinued &mdash; as the deficient "
             "one was after Q2 FY 2025/26 &mdash; this page says so rather "
             "than carrying the last figure forward as though it were "
             "current.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "How long the BBS takes: California licence and registration times",
    "The Board's own quarterly processing times for AMFT, ASW and APCC "
    "registrations and LMFT, LCSW, LPCC and LEP licences, with the year-ago "
    "comparison and what a deficient application costs.",
    "licensure", "reference",
    "I passed the exam &mdash; how long until the licence actually arrives?",
    "The Board's published processing times, the year-over-year shift, and "
    "the cost of an application that comes back",
    "%d days for an LMFT licence" % approved("LMFT license")[4],
    weight=5)

# The title and description above are the two places on this page where the
# word appears without a Labor Code section beside it, and both are read by
# people rather than by the spelling guard's American-English rule. Keep them
# consistent with the rest of the site: American spelling, everywhere.
META = META.replace("licence", "license").replace("Licence", "License")


def main():
    print("BBS processing times")
    problems = B.check()
    for x in problems:
        print("GUARD:", x)
    if problems:
        sys.exit("the transcribed data is inconsistent; nothing was written")

    lmft = approved("LMFT license")
    print("  LMFT license, clean application: %d days a year ago, %d now (%s%%)"
          % (lmft[3], lmft[4],
             ("+%d" % pct_change(lmft[3], lmft[4]))
             if pct_change(lmft[3], lmft[4]) > 0
             else pct_change(lmft[3], lmft[4])))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the methodology break", "do not join"),
        ("the deficiency rate", format(B.DEFICIENCY_RATE, ".2f")),
        ("the old series", "all applications processed"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # The break between the two series is the whole reason this page is
    # careful. If the section explaining it is ever cut, the two tables above
    # it become a single misleading series.
    if 'id="break"' not in art:
        print("GUARD: the methodology-break section is gone, and the two "
              "tables above it are now uncaptioned")
        bad += 1

    # Both figures of the headline comparison must appear as written.
    for want in ("%d days" % lmft[3], "%d days" % lmft[4]):
        if want not in art:
            print("GUARD: %s is not on the page" % want)
            bad += 1

    if nsrc < 6:
        print("GUARD: %d sources for a page that is nothing but transcribed "
              "figures" % nsrc)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - two series kept apart, %d sources" % nsrc)


if __name__ == "__main__":
    main()
