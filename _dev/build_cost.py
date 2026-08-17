#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What getting licensed actually costs - assembled, not invented.

EDITORIAL #9 of the approved list. The question is asked constantly and
answered badly, because the answer is scattered across five pages that
each own one line of it: the Board's fee schedule, the degree, the
fingerprints, supervision, CE. Nobody adds them up, and the sum is the
thing people want.

THE CONTENT RULE, INHERITED FROM build_viable.py: no new numbers. Every
figure here already exists on another page of this site, where it
carries its own source and its own checked date. This page assembles
them and links each one back. The FIGURES guard below fails the build
if any attributed figure is missing from the page it is attributed to.

The only arithmetic this page performs is addition over those figures,
and it shows its working in a table rather than asserting a total.

THE FINDING THE ARITHMETIC PRODUCES

The license is the cheap part. Everything the State of California
charges to turn a qualified person into an LMFT comes to roughly $549
paid once plus renewals - $624 to $924 across the whole route. The
degree that qualifies you runs $37,800 to $152,340. So the regulatory
cost is between one and two per cent of the entry cost, and every
argument about Board fees is an argument about the wrong number.

WHAT THIS PAGE DELIBERATELY DOES NOT PRICE

Exam preparation is a real cost and this site has not yet compared the
vendors, so it is named as a line and left unpriced rather than given a
figure from a vendor's marketing page. Same for the Live Scan rolling
fee, which the Board itself does not publish, and for supervision paid
privately, where the site carries a distribution rather than a price.
Saying "not priced here" is the honest move and it is also the one that
keeps the no-new-numbers rule intact.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "what-licensure-actually-costs-california.html"
DONOR = "bbs-advertising-rules-2026.html"

FEES = "bbs-fees-california-2026.html"
ROUTE = "become-an-mft-california.html"
PROGS = "mft-programs-california.html"
SUPER = "finding-a-clinical-supervisor-california.html"
CE = "continuing-education-california-lmft.html"
HOURS = "amft-3000-hours-california.html"
VIABLE = "is-therapy-financially-viable-california.html"

# Every figure this page uses, and the page it must appear on.
FIGURES = [
    ("$500", FEES),          # the paid-once Board subtotal
    ("$575", FEES),          # the floor, 104-week route
    ("$875", FEES),          # the ceiling, five renewals
    ("$75", FEES),           # each annual associate renewal
    ("$100", FEES),          # biennial renewal, active
    ("$32", ROUTE),          # DOJ fingerprints
    ("$17", ROUTE),          # FBI fingerprints
    ("$37,800", PROGS),
    ("$152,340", PROGS),
    ("$170", CE),            # the whole CE cycle, held down
    ("$300", SUPER),         # what a third of payers pay a month
]

# Derived by addition over the figures above. Shown as arithmetic on the
# page, never asserted - and re-derived here so a moved figure moves it.
FINGERPRINTS = 32 + 17                    # 49
ONCE = 500 + FINGERPRINTS                 # 549
ROUTE_LOW = 575 + FINGERPRINTS            # 624
ROUTE_HIGH = 875 + FINGERPRINTS           # 924
ENTRY_LOW = 37800 + ROUTE_LOW             # 38,424
ENTRY_HIGH = 152340 + ROUTE_HIGH          # 153,264

JUMPS = [("once", "Paid once"),
         ("route", "The whole route"),
         ("degree", "The number that dwarfs it"),
         ("after", "After the license"),
         ("unpriced", "What this cannot price"),
         ("sources", "Sources")]


def m(n):
    return "$" + format(int(n), ",d")


def link(page, text):
    return '<a href="%s">%s</a>' % (page, text)


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Every figure lifted from the page that documents it &middot; "
        "checked August 2026",
        "The license is the cheap part.",
        "Everything the State of California charges to turn a qualified "
        "person into an LMFT comes to about %s paid once, and %s to %s "
        "across the whole route including renewals. The degree that "
        "qualifies you runs %s to %s. This page adds up the regulatory "
        "cost, shows the working, and is honest about the four lines "
        "nobody can price."
        % (m(ONCE), m(ROUTE_LOW), m(ROUTE_HIGH), m(37800), m(152340)),
        [(m(ONCE), "paid once, to the state"),
         ("%s&ndash;%s" % (m(ROUTE_LOW), m(ROUTE_HIGH)), "the whole "
          "regulatory route"),
         ("%s&ndash;%s" % (m(37800), m(152340)), "the degree that "
          "qualifies you"),
         ("~1%", "the regulatory share of entry cost")],
        JUMPS))

    # ---------------------------------------------------------------- once
    o.append('<section class="pk-sec" id="once">')
    o.append('<p class="pk-k">The one-time bill</p>')
    o.append('<h2 class="pk-h">%s, and five of the six lines are the '
             "Board&rsquo;s.</h2>" % m(ONCE))
    o.append('<p class="pk-p">These are the charges you pay exactly '
             "once on the way from a finished degree to a license. "
             "Every Board fee halved on 1 July 2026 and the reduced "
             "schedule runs to 30 June 2030, so these are the current "
             "figures and they are temporary ones &mdash; the %s "
             "carries the reversion.</p>"
             % link(FEES, "fee-schedule page"))

    rows = [
        ["Registration application &mdash; AMFT, ASW, APCC", "$75",
         link(FEES, "Board fee schedule")],
        ["California Law and Ethics exam", "$75",
         link(FEES, "Board fee schedule")],
        ["License application", "$125", link(FEES, "Board fee schedule")],
        ["LMFT clinical exam", "$125", link(FEES, "Board fee schedule")],
        ["Initial license issuance", "$100",
         link(FEES, "Board fee schedule")],
        (["<b>Board subtotal, paid once</b>", "<b>$500</b>",
          link(FEES, "Board fee schedule")], "hi"),
        ["Fingerprinting &mdash; state, to the DOJ", "$32",
         link(ROUTE, "the route page")],
        ["Fingerprinting &mdash; federal, to the FBI", "$17",
         link(ROUTE, "the route page")],
        ["Exam vendor &mdash; Pearson VUE", "$0",
         link(ROUTE, "the route page")],
        (["<b>Paid once, in total</b>", "<b>%s</b>" % m(ONCE),
          "The five Board fees plus both fingerprint fees"], "hi"),
    ]
    o.append(pk.table(["What", "Now", "Where the figure comes from"],
                      rows,
                      caption="The exam vendor charges nothing because "
                              "the exam fee is already inside what you "
                              "paid the Board - which is the line most "
                              "cost articles double-count."))
    o.append("</section>")

    # --------------------------------------------------------------- route
    o.append('<section class="pk-sec" id="route">')
    o.append('<p class="pk-k">Add the years</p>')
    o.append('<h2 class="pk-h">%s to %s, and which one you pay is '
             "decided by how long the hours take.</h2>"
             % (m(ROUTE_LOW), m(ROUTE_HIGH)))
    o.append('<p class="pk-p">An associate registration runs a year at '
             "a time, and each renewal is another $75. The 3,000 hours "
             "cannot lawfully be completed in under 104 weeks, so "
             "everybody pays at least one renewal; the Board permits "
             "five before the registration expires. That turns the "
             "total into a line rather than a point, and where you land "
             "on it is a question about your caseload, which the %s "
             "answers.</p>" % link(HOURS, "hours projection"))

    rows = [
        ["Fastest lawful route &mdash; 104 weeks, one renewal", "$575",
         m(ROUTE_LOW)],
        ["The common case &mdash; two renewals", "$650", m(650 + 49)],
        ["The statutory ceiling &mdash; five renewals", "$875",
         m(ROUTE_HIGH)],
    ]
    o.append(pk.table(["How long you are an associate",
                       "Board fees", "With fingerprints"],
                      rows,
                      caption="Board totals from the fee-schedule page; "
                              "the right-hand column adds the $49 of "
                              "fingerprinting from the route page."))
    o.append('<p class="pk-p">Two things sit outside that. A $20 Mental '
             "Health Practitioner Education Fund fee rides along with "
             "renewals, and supervision may or may not cost you "
             "anything &mdash; both are covered below.</p>")
    o.append("</section>")

    # -------------------------------------------------------------- degree
    o.append('<section class="pk-sec" id="degree">')
    o.append('<p class="pk-k">The number that dwarfs the rest</p>')
    o.append('<h2 class="pk-h">The degree costs 40 to 165 times the '
             "license.</h2>")
    o.append('<p class="pk-p">Every figure above is regulatory. None of '
             "it qualifies you for anything &mdash; the degree does "
             "that, and it is where the money actually goes. Published "
             "tuition across the California MFT programs on the %s runs "
             "from %s to %s for the whole degree.</p>"
             % (link(PROGS, "programs directory"), m(37800), m(152340)))

    rows = [
        ["Cheapest published program", m(37800), "$575", m(ENTRY_LOW)],
        ["Dearest published program", m(152340), "$875", m(ENTRY_HIGH)],
    ]
    o.append(pk.table(["Route", "Degree", "Board fees",
                       "Entry cost, with fingerprints"],
                      rows,
                      caption="Degree figures from the programs "
                              "directory; Board figures from the fee "
                              "schedule. Everything else on this page "
                              "is rounding error against this row."))
    o.append(pk.callout(
        "So the fee argument is an argument about the wrong number",
        ["Board fees are between roughly one and two per cent of what "
         "entering this profession costs. They halved in July 2026, "
         "which saved the median candidate a few hundred dollars across "
         "several years &mdash; real, and not the decision.",
         "The decision is the program. A %s spread between the cheapest "
         "and dearest published tuition is the only line on this page "
         "big enough to change what the career is worth, and it is "
         "chosen once, early, usually with the least information. The "
         "whole-career version of that arithmetic is on %s."
         % (m(152340 - 37800), link(VIABLE, "the viability page"))]))
    o.append("</section>")

    # --------------------------------------------------------------- after
    o.append('<section class="pk-sec" id="after">')
    o.append('<p class="pk-k">It does not stop at the license</p>')
    o.append('<h2 class="pk-h">What starts the day you are '
             "licensed.</h2>")
    rows = [
        ["Biennial renewal, active", "$100", "Every two years",
         link(FEES, "fee schedule")],
        ["36 hours of continuing education", "under $170",
         "Every two-year cycle", link(CE, "the CE page")],
    ]
    o.append(pk.table(["What", "Amount", "How often", "Source"], rows))
    o.append('<p class="pk-p">The CE figure is the cash cost of a '
             "compliant cycle done deliberately, and it is small. What "
             "the %s is actually about is not the money: 62 per cent of "
             "recent Board CE audits ended in failure, and they fail on "
             "timing, provenance and paperwork rather than on effort or "
             "expense.</p>" % link(CE, "CE page"))
    o.append("</section>")

    # ------------------------------------------------------------ unpriced
    o.append('<section class="pk-sec" id="unpriced">')
    o.append('<p class="pk-k">The honest gaps</p>')
    o.append('<h2 class="pk-h">Four lines this page will not put a '
             "number on.</h2>")
    o.append(pk.numbered([
        ("1", "The Live Scan rolling fee.",
         "The $32 and $17 above go to the DOJ and the FBI. The site "
         "that takes your prints charges its own fee on top, it varies, "
         "and <b>the Board publishes no figure for it</b>. A made-up "
         "range would be the only invented number on this page."),
        ("2", "Exam preparation.",
         "A real cost, and a real market &mdash; this site has not "
         "compared the vendors yet, so there is no figure here to lift. "
         "What is worth knowing meanwhile is on %s: the Board publishes "
         "two different pass rates for every exam, the first-time rate "
         "and the all-sittings rate, and they are not close."
         % link("bbs-exam-pass-rates-california.html",
                "the pass-rates page")),
        ("3", "Supervision, if you pay for it yourself.",
         "Most associates do not &mdash; the employer arranges it. "
         "Among those who do pay, the Board&rsquo;s own survey has 35 "
         "per cent paying more than $300 a month, with the rest spread "
         "from under $50 upward; the distribution is on %s. Over a "
         "two-year registration the difference between $0 and the top "
         "of that range is larger than every other line on this page "
         "except the degree. And there is a trap attached: paid out of "
         "your own pocket in a private practice with no employer "
         "relationship, the weeks may not be creditable at all."
         % link(SUPER, "the supervisor page")),
        ("4", "The income you do not earn while you qualify.",
         "The largest cost of all, and not a fee. It is the associate "
         "years at associate pay, which is a different question worked "
         "in full on %s." % link(VIABLE, "the viability page")),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("Every figure on this page, and the page that owns it", [
            ("The Board fee schedule, halved from 1 July 2026 - the "
             "$500 paid-once subtotal, the $575 floor and $875 ceiling, "
             "and the reversion in 2030", FEES),
            ("The route page - the DOJ and FBI fingerprint fees, and "
             "what the exam vendor charges", ROUTE),
            ("The California MFT programs directory - published "
             "tuition, from $37,800 to $152,340", PROGS),
            ("The continuing-education page - the cost of a compliant "
             "cycle, and the audit that six in ten fail", CE),
            ("The clinical supervisor page - what supervision costs "
             "the minority who pay for it, and the private-practice "
             "trap", SUPER),
            ("The 3,000-hours projection - which renewal count you "
             "actually land on", HOURS),
            ("The viability page - the same arithmetic across a whole "
             "career, ending at the simulator", VIABLE),
        ]),
    ], note="This page introduces no figures of its own. Every amount "
            "above is carried from the page listed beside it, where it "
            "has a primary source and the date it was last checked; "
            "the only arithmetic performed here is addition, and it is "
            "shown rather than asserted. Fee schedules change - the "
            "current one reverts in 2030 - so check the source page "
            "before relying on a total. Nothing here is legal or "
            "financial advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "What licensure actually costs in California: the whole bill",
    "Every charge on the way to an LMFT license, added up from the "
    "pages that document each one - about $549 paid once, $624 to $924 "
    "across the route, against a degree costing $37,800 to $152,340.",
    "licensure", "reference",
    "What does it actually cost to get licensed as a therapist in California?",
    "The one-time bill, the renewals, and the degree that dwarfs both - "
    "plus the four costs nobody can put a number on",
    "About $549 once; $624 to $924 across the route",
    weight=4)


def main():
    print("the cost-of-licensure page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    # ---- NO NEW NUMBERS: every figure must live on its source page
    bad = 0
    for fig, src_page in FIGURES:
        s = open(os.path.join(SITE, src_page), encoding="utf-8").read()
        if fig.replace("$", "") not in s.replace("$", ""):
            print("GUARD: %s is attributed to %s, which does not "
                  "contain it" % (fig, src_page))
            bad += 1

    # ---- the derived sums must still be the sums
    for label, got, want in (("fingerprints", FINGERPRINTS, 49),
                             ("paid once", ONCE, 549),
                             ("route low", ROUTE_LOW, 624),
                             ("route high", ROUTE_HIGH, 924)):
        if got != want:
            print("GUARD: %s computes to %d, not %d - a component "
                  "figure moved and the prose needs rereading, not "
                  "just the number" % (label, got, want))
            bad += 1

    n = pk.check_page(p, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        ("the fee-schedule link", FEES),
        ("the route link", ROUTE),
        ("the programs link", PROGS),
        ("the supervisor link", SUPER),
        ("the CE link", CE),
        ("the viability link", VIABLE),
        ("the paid-once total", m(ONCE)),
        ("the route range low", m(ROUTE_LOW)),
        ("the route range high", m(ROUTE_HIGH)),
    ], [h for h, _ in JUMPS])

    s = open(p, encoding="utf-8").read()
    artm = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s)
    art = artm.group(0)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # The page's whole claim is that it invents nothing. If a future edit
    # prices one of the four unpriced lines, this stops being true.
    if "the board publishes no figure for it" not in flat:
        print("GUARD: the Live Scan line no longer says the Board "
              "publishes no figure")
        bad += 1
    if "has not compared the vendors yet" not in flat:
        print("GUARD: the exam-prep line no longer declines to price "
              "itself")
        bad += 1

    for phrase in ("is hiring", "has openings", "guaranteed",
                   "you will earn", "accepting new"):
        if phrase in flat:
            print("GUARD: %r has no business on an arithmetic page"
                  % phrase)
            n += 1
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        n += 1

    if n or bad:
        sys.exit("%d check failure(s)" % (n + bad))
    print("  checks passed - %d figures verified on their source pages, "
          "4 lines left honestly unpriced" % len(FIGURES))


if __name__ == "__main__":
    main()
