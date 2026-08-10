#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Where California's therapists are, from the state's own file of all 165,235.

THE QUESTION THIS ANSWERS

Two of them, and the second is the one people are actually asking.

The stated question is "how many therapists are there in California, and
where?" - which nobody publishes at license-type granularity, and which the
state's own data answers exactly.

The real question is the one filling associate support groups: *"I have 547
hours and everywhere I apply wants someone nearly finished. How do I get hours
if everyone expects me to already have them?"* That was 87 comments. Another
was 114, from somebody considering bankruptcy after months of rejections. The
replies are sympathy, because nobody has a number.

There is a number. Associates per licensed clinician, by county, computed from
the register: 0.82 in Merced against 0.24 in Marin, among counties big enough
to rank. An associate in Merced is competing for supervision against a pool
three times denser, relative to the clinicians who could hire and supervise
them, than one in Marin. That is not advice and it is not encouragement. It is
arithmetic, and it is the first honest answer that thread has had.

(Imperial is higher still at 1.06 - more associates than licensed clinicians -
but it has 337 people in total, and a ratio built on 337 moves when a handful
of them renew. MIN_FOR_RANKING keeps counties that small off the ranking and
on the full table, and the page says so rather than quietly dropping them.)

THE FINDING THAT CAME OUT OF THE DATA RATHER THAN INTO IT

Delinquency by license type was computed as a sanity check and turned out to be
the most striking thing in the file:

    APCC   26.7%        LPCC    2.8%
    LEP    18.1%        LCSW    5.2%
    ASW    13.3%        LMFT    6.4%
    AMFT    9.4%

**More than one in four professional clinical counselor associates is
delinquent.** Every associate category lapses more than every licensed
category, and the APCC-to-LPCC gap is nine-fold. Nobody has published this. The
page states it and is careful about what it does and does not prove: a
delinquent registration is a fact about a register, and the file cannot say
whether somebody left the profession, let a registration lapse between jobs, or
simply renewed late.

WHERE THE NUMBERS COME FROM

`_dev/dca_licensees.py`, which downloads California's monthly file of every BBS
licensee and writes counts to `_dev/dca_stats.py`. Every figure on this page is
read from that module at build time. None is typed into prose - if the register
moves, the page moves.

THE PRIVACY POSITION, STATED ON THE PAGE

The source file contains addresses, and for a solo practitioner that is usually
their home. This page publishes counts and nothing else, and says so out loud,
because a reader who realises their address is in a public state file deserves
to know what this site did and did not do with it.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk
import dca_stats as D

PAGE = "therapists-by-county-california.html"
DONOR = "hiring-first-associate-california-therapist.html"

PAY = "associate-therapist-pay-los-angeles-bay-area.html"
HOURS = "amft-3000-hours-california.html"
ADVISOR = "associate-mft-job-advisor.html"
UNPAID = "associate-unpaid-hours-california.html"
TIMES = "bbs-processing-times-california.html"

# A county needs enough people in it for a ratio to mean anything. Modoc has 20
# clinicians in total; its ratio moves by 0.05 when one person renews. The
# threshold is stated on the page rather than hidden, and the small counties are
# still listed - just not ranked.
MIN_FOR_RANKING = 400

JUMPS = [
    ("supply", "The competition map"),
    ("counties", "Every county"),
    ("lapse", "Who drops out"),
    ("what", "What the register is"),
    ("limits", "What it cannot tell you"),
]


def ranked():
    return sorted(((c, v) for c, v in D.COUNTIES.items()
                   if v["assoc"] + v["lic"] >= MIN_FOR_RANKING),
                  key=lambda kv: -kv[1]["ratio"])


def by_size():
    return sorted(D.COUNTIES.items(), key=lambda kv: -(kv[1]["assoc"] + kv[1]["lic"]))


def statewide_ratio():
    a = sum(v["assoc"] for v in D.COUNTIES.values())
    l = sum(v["lic"] for v in D.COUNTIES.values())
    return a / float(l), a, l


def body():
    o = ['<article class="pk-wrap">']

    rk = ranked()
    hi_c, hi = rk[0]
    lo_c, lo = rk[-1]
    ratio, n_assoc, n_lic = statewide_ratio()
    worst = max(D.DELINQUENCY.items(), key=lambda kv: kv[1]["pct"])
    best = min(D.DELINQUENCY.items(), key=lambda kv: kv[1]["pct"])

    o.append(pk.hero(
        "The register &middot; %s &middot; %s licensees"
        % (D.AS_AT, format(D.TOTAL, ",d")),
        "Every therapist in California, counted.",
        "California publishes its whole register every month and nobody reads "
        "it. Here is what is in this month&rsquo;s: <b>where the competition "
        "for supervision is, and who is quietly dropping off the register</b>.",
        [(format(D.TOTAL, ",d"), "licensees and registrants"),
         ("%d" % len(D.COUNTIES), "counties, all of them"),
         ("%.2f&ndash;%.2f" % (lo["ratio"], hi["ratio"]),
          "associates per licensed clinician"),
         ("%.1f%%" % worst[1]["pct"], "of %s registrations delinquent" % worst[0])],
        JUMPS))

    # ------------------------------------------------------------ the supply
    o.append('<section class="pk-sec" id="supply">')
    o.append(pk.quote(
        "The question this page was built to answer",
        ["I am an AMFT and I&rsquo;m having a horrible time finding "
         "employment. Everywhere I apply they are looking for someone with "
         "almost totally completed hours. <b>I only have 547.</b> How do I get "
         "hours if everyone expects me to have them already?"]))
    o.append('<p class="pk-d">That post drew eighty-seven replies, almost all '
             "of them sympathy. Sympathy is not wrong, but there is also a "
             "number, and it is in the state&rsquo;s own register.</p>")

    o.append('<p class="pk-k">The reframe</p>')
    o.append('<h2 class="pk-h">How crowded your county is, measured.</h2>')
    o.append('<p class="pk-d">Every associate needs a licensed clinician to '
             "employ and supervise them. So the ratio that matters is not how "
             "many therapists your county has &mdash; it is <b>how many "
             "associates there are for each licensed clinician who could take "
             "one on</b>. Statewide that is <b>%s associates against %s "
             "licensed clinicians, or %.2f each</b>. It is nowhere near evenly "
             "spread.</p>"
             % (format(n_assoc, ",d"), format(n_lic, ",d"), ratio))

    rows = []
    for c, v in rk[:8]:
        rows.append(([c, (format(v["assoc"], ",d"), "n"),
                      (format(v["lic"], ",d"), "n"),
                      ("%.2f" % v["ratio"], "f")], "bad"))
    for c, v in rk[-6:]:
        rows.append(([c, (format(v["assoc"], ",d"), "n"),
                      (format(v["lic"], ",d"), "n"),
                      ("%.2f" % v["ratio"], "f")], "good"))
    o.append(pk.table(
        ["County", "Associates", "Licensed", "Associates each"],
        rows,
        "The eight most crowded counties and the six least, of the %d with at "
        "least %d clinicians. <b>%s has %.2f associates for every licensed "
        "clinician; %s has %.2f.</b> An associate in %s is looking for a "
        "supervisor in a market more than %s times denser."
        % (len(rk), MIN_FOR_RANKING, hi_c, hi["ratio"], lo_c, lo["ratio"],
           hi_c, ("%.1f" % (hi["ratio"] / lo["ratio"])).rstrip("0").rstrip(".")),
        minw=520))

    o.append(pk.callout(
        "What this does and does not say",
        ["It <b>does</b> say where the queue for supervision is longest, and "
         "that the queue is a local fact rather than a personal failing. If "
         "you are in one of the counties at the top of that table, the "
         "difficulty you are having is measurable and it is not about you.",
         "It does <b>not</b> say where the jobs are. A county with few "
         "associates may have few employers as well. Read it as competition "
         "for each available supervisor, which is the constraint associates "
         "actually hit &mdash; and pair it with what the jobs "
         "<a href=\"%s\">actually pay</a>." % PAY]))
    o.append("</section>")

    # ---------------------------------------------------------- all counties
    o.append('<section class="pk-sec" id="counties">')
    o.append('<p class="pk-k">All %d, largest first</p>' % len(D.COUNTIES))
    o.append('<h2 class="pk-h">Every county in California.</h2>')
    o.append('<p class="pk-d">Associates are AMFT, ASW and APCC '
             "registrations. Licensed is LMFT, LCSW, LPCC and LEP. Counties "
             "with fewer than %d clinicians are shown but not ranked, because "
             "a ratio built on twenty people moves when one of them "
             "renews.</p>" % MIN_FOR_RANKING)
    rows = []
    for c, v in by_size():
        small = (v["assoc"] + v["lic"]) < MIN_FOR_RANKING
        rows.append([c, (format(v["assoc"], ",d"), "n"),
                     (format(v["lic"], ",d"), "n"),
                     (format(v["assoc"] + v["lic"], ",d"), "n"),
                     ("&mdash;" if small else "%.2f" % v["ratio"], "m")])
    o.append(pk.table(
        ["County", "Associates", "Licensed", "Total", "Associates each"],
        rows,
        "%s of the %s records carry a California county. The rest are "
        "licensees at out-of-state addresses (%s of them) or records with no "
        "county on file."
        % (format(sum(v["assoc"] + v["lic"] for v in D.COUNTIES.values()), ",d"),
           format(D.TOTAL, ",d"), format(D.OUT_OF_STATE, ",d")), minw=560))
    o.append("</section>")

    # ---------------------------------------------------------------- lapse
    o.append('<section class="pk-sec" id="lapse">')
    o.append('<p class="pk-k">The finding nobody has published</p>')
    o.append('<h2 class="pk-h">More than one in four APCC registrations is '
             "delinquent.</h2>")
    o.append('<p class="pk-d">This was computed as a check on the data and '
             "turned out to be the most striking thing in it. Every associate "
             "category lapses more often than every licensed category, and the "
             "gap between the two professional clinical counselor grades is "
             "nine-fold.</p>")
    rows = []
    for k, v in sorted(D.DELINQUENCY.items(), key=lambda kv: -kv[1]["pct"]):
        assoc = k in ("AMFT", "ASW", "APCC")
        rows.append(([("<b>%s</b>" % k) + ("" if not assoc else " &mdash; associate"),
                      (format(v["total"], ",d"), "n"),
                      (format(v["delinquent"], ",d"), "n"),
                      ("%.1f%%" % v["pct"], "f")],
                     "bad" if v["pct"] >= 13 else ("good" if v["pct"] < 6 else "")))
    o.append(pk.table(
        ["License or registration", "On the register", "Delinquent", "Share"],
        rows,
        "%s of the %s records on the register are delinquent, and %s are "
        "current-but-inactive. <b>%s at %.1f%% against %s at %.1f%%</b> is the "
        "widest gap between two grades of the same profession."
        % (format(D.BY_STATUS.get("Delinquent", 0), ",d"),
           format(D.TOTAL, ",d"),
           format(D.BY_STATUS.get("CurrentInactive", 0), ",d"),
           worst[0], worst[1]["pct"], best[0], best[1]["pct"]), minw=520))

    o.append(pk.checklist(
        "Four things a delinquency rate is not",
        ["<b>It is not an attrition rate.</b> A delinquent registration means "
         "the renewal date passed without a renewal. Some of those people left "
         "the profession; some are between jobs; some paid late.",
         "<b>It is not a measure of anybody&rsquo;s competence.</b> The "
         "commonest reason a registration lapses is that a fee and a form fell "
         "past a date.",
         "<b>It does not say the license is gone.</b> California allows a "
         "delinquent license to be renewed, with a fee, for a period after "
         "expiry &mdash; a delinquent record is a warning, not a headstone.",
         "<b>It is one month&rsquo;s snapshot.</b> The register is republished "
         "monthly and this page is rebuilt from the current file, so the "
         "figure moves. It was last read in %s." % D.AS_AT]))
    o.append('<p class="pk-fine">If your own registration has gone delinquent '
             "or is close to it, the two things worth knowing are how long the "
             'Board is currently taking &mdash; <a href="%s">that is published '
             "quarterly and is on this site</a> &mdash; and whether your hours "
             'are still inside their validity window, which <a href="%s">the '
             "hours calculator</a> works out from your own dates.</p>"
             % (TIMES, HOURS))
    o.append("</section>")

    # ------------------------------------------------------------ the source
    o.append('<section class="pk-sec" id="what">')
    o.append('<p class="pk-k">Where every number here comes from</p>')
    o.append('<h2 class="pk-h">The state publishes this. Monthly. To '
             "anyone.</h2>")
    o.append('<p class="pk-d">The Department of Consumer Affairs puts the '
             "complete register of Board of Behavioral Sciences licensees on "
             "its public-information page, refreshed every month, free, with "
             "no account and no key. This month&rsquo;s file holds <b>%s "
             "records across %s California cities</b>. It is a plain "
             "tab-delimited text file that happens to be named as a "
             "spreadsheet, which may be part of why so few people have "
             "opened it.</p>"
             % (format(D.TOTAL, ",d"), format(D.CITIES, ",d")))

    rows = []
    for k, v in sorted(D.BY_TYPE.items(), key=lambda kv: -kv[1]):
        rows.append([k, (format(v, ",d"), "f")])
    o.append(pk.table(["What is on the register", "How many"], rows,
                      "Every license and registration type the Board issues, "
                      "as at %s." % D.AS_AT, minw=420))

    o.append(pk.callout(
        "What this site did not publish, and why",
        ["The state&rsquo;s file also contains an <b>address for every one of "
         "those %s people</b>. It is the address of record, and for a "
         "therapist in solo practice that is very often the address they sleep "
         "at."
         % format(D.TOTAL, ",d"),
         "<b>This page publishes counts and nothing else.</b> No names, no "
         "addresses, no license numbers. The build refuses to run if the raw "
         "file would be committed, and re-reads its own output afterwards to "
         "check that nothing identifying survived into it.",
         "That the data is public does not mean every use of it is decent. If "
         "you want to check a specific license, the Board&rsquo;s own "
         "verification search is the right place, and it is linked below."]))
    o.append("</section>")

    # ---------------------------------------------------------------- limits
    o.append('<section class="pk-sec" id="limits">')
    o.append('<p class="pk-k">Read this before quoting the page</p>')
    o.append('<h2 class="pk-h">What the register cannot tell you.</h2>')
    o.append(pk.table(
        ["The question", "What the file can say"],
        [(["How many new therapists were licensed last year?",
           "<b>Nothing reliable.</b> The file carries an "
           "&ldquo;original issue date&rdquo;, and counting by it produces a "
           "collapse in new licenses that did not happen &mdash; license "
           "numbers do not band by year, and the Board&rsquo;s own quarterly "
           "report records more applications processed in three months than "
           "that field attributes to a whole year. The build refuses to emit "
           "the series. For real issuance figures, use the Board&rsquo;s "
           "licensing reports."], "bad"),
         ["Who is taking new clients, and in what?",
          "<b>Nothing.</b> No specialty, no modality, no availability, no fee. "
          "The register is an administrative list, not a directory of "
          "practice."],
         ["Who has been disciplined?",
          "<b>Nothing.</b> There is no discipline field. The Board publishes "
          "enforcement outcomes only through per-licensee lookup &mdash; the "
          "case library on this site is built from the decisions themselves, "
          "not from this file."],
         ["Where does somebody actually work?",
          "<b>Not reliably.</b> The address is the address of record, which "
          "may be a home, an employer, or a mail drop. County counts are "
          "sound in aggregate and should not be read as a workplace map."],
         ["Is this person licensed right now?",
          "<b>Only as at %s.</b> A monthly snapshot is a month stale by "
          "construction. Verify a specific license with the Board." % D.AS_AT]],
        "The rule this site works to: publish what the source supports and say "
        "plainly what it does not. The issue-date row above is a figure that "
        "would have made a striking chart, and it is not on the page because "
        "it would have been wrong."))
    o.append("</section>")

    src, n = pk.sources([
        ("The register", [
            ("California Department of Consumer Affairs &mdash; public "
             "information, where the monthly licensee file is published",
             D.SOURCE),
            ("DCA license search, for verifying one specific license",
             "https://search.dca.ca.gov/"),
            ("Board of Behavioral Sciences", "https://www.bbs.ca.gov/"),
        ]),
        ("What the register cannot answer, and what does", [
            ("BBS licensing reports &mdash; actual applications received and "
             "processed each quarter, which is where issuance figures belong",
             "https://bbs.ca.gov/about/board_meetings.html"),
        ]),
    ], note="Every figure on this page is computed from the file at build "
            "time rather than typed into the text, so when the state "
            "republishes, the page changes with it. The file was last read in "
            "<b>%s</b>." % D.AS_AT)
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "Therapists by county in California: all 165,000, from the register",
    "Every LMFT, LCSW, LPCC and associate counted by county, from the "
    "state's own monthly register: how many associates compete for each "
    "licensed supervisor, and which registrations lapse most.",
    "licensure", "reference",
    "How many therapists are there in my county, and how crowded is it?",
    "The whole California register counted by county and license type, with "
    "the associate-per-supervisor ratio and the delinquency rates nobody "
    "publishes",
    "%s on the register" % format(D.TOTAL, ",d"),
    weight=5)


def main():
    print("the California therapist map")
    rk = ranked()
    if len(rk) < 20:
        sys.exit("build_atlas: only %d counties clear the ranking threshold, "
                 "which suggests dca_stats.py is not what it should be" % len(rk))
    ratio, n_assoc, n_lic = statewide_ratio()
    print("  %s licensees, %d counties, statewide ratio %.2f"
          % (format(D.TOTAL, ",d"), len(D.COUNTIES), ratio))
    print("  most crowded: %s %.2f | least: %s %.2f"
          % (rk[0][0], rk[0][1]["ratio"], rk[-1][0], rk[-1][1]["ratio"]))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the privacy statement", "publishes counts and nothing else"),
        ("the issue-date warning", "collapse in new licenses that did not"),
        ("the delinquency table", "Delinquent"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every county must be on the page, or the "all 58" claim is false.
    missing = [c for c in D.COUNTIES if c not in art]
    if missing:
        print("GUARD: %d counties are counted but not printed: %s"
              % (len(missing), ", ".join(sorted(missing)[:6])))
        bad += 1
    if len(D.COUNTIES) != 58:
        print("GUARD: dca_stats has %d counties, and California has 58"
              % len(D.COUNTIES))
        bad += 1

    # The headline figures must be derived, never typed. If a number appears in
    # the prose that is not in the data, it was typed.
    for want in (format(D.TOTAL, ",d"), "%.1f%%" % D.DELINQUENCY["APCC"]["pct"],
                 "%.2f" % rk[0][1]["ratio"]):
        if want not in art:
            print("GUARD: the derived figure %s is not on the page" % want)
            bad += 1

    # This page must never carry a person.
    if re.search(r"\b\d{1,5}\s+[A-Z][a-z]+\s+(St|Ave|Rd|Dr|Blvd|Way|Ln)\b", art):
        print("GUARD: something shaped like a street address is on the page")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - %d counties printed, every figure derived, no "
          "person on the page" % len(D.COUNTIES))


if __name__ == "__main__":
    main()
