#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What it costs to RUN the payroll, on the page that already prices the hire.

WHY THIS IS A SECTION AND NOT A SIXTH NEW PAGE

The Facebook sweep found two threads worth a page each. The first became
`_dev/build_unpaid.py`. The second - "can I 1099 my associate, and what does a
W-2 actually cost" - already had a page: `hiring-first-associate-california-
therapist.html` answers the classification question at length and prices the
employer taxes to the dollar. Publishing a second page on the same question
would have split the topic across two URLs competing with each other, which is
the opposite of what the site's internal linking is for.

What that page was missing is the operational half, and it is the half nobody
writes: the employer taxes are only part of the cost, and the practice still
has to actually run a payroll. That is a monthly subscription, a registration
with the EDD triggered at a threshold most people have never heard of, and a
workers' compensation quote whose real number depends on a class code the page
did not name.

THE THREE THINGS THIS ADDS

1. **The EDD registration trigger is $100 of wages in a calendar quarter, and
   the deadline is 15 days.** Not a salary threshold, not an annual one. One
   month of a part-time associate crosses it.
2. **Published payroll prices for exactly one employee**, from each vendor's
   own pricing page. ADP publishes no price at all, and this section says so
   rather than quoting a figure from a review site.
3. **The workers' compensation class code.** The page already carries the
   statewide advisory average of $1.65 per $100 of payroll and says an
   office-based practice classifies below it. This puts a number on "below":
   the median filed rate for class 8834 is $1.25 and for clerical 8810 it is
   $0.40.

WHAT IT DOES NOT TOUCH

The existing cost table, the FUTA footnote or the SDI correction, all of which
are right. This inserts one section between "What an employee actually costs"
and "What an associate earns you", in the page's own markup idiom - h2, p,
div.tw > table.tbl - so no new CSS ships for it.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

PAGE = os.path.join(SITE, "hiring-first-associate-california-therapist.html")
ANCHOR = '<h2 id="what-an-associate-earns-you">'
SECT_ID = "what-it-costs-to-run-the-payroll"

EDD_TRIGGER = 100
EDD_DAYS = 15

# Base monthly price + per-employee fee, from each vendor's own pricing page,
# checked August 2026. A vendor that does not publish a price is None, and the
# table prints that rather than a figure borrowed from somewhere else.
PAYROLL = [
    ("Patriot Software, Basic", 17, 4,
     "You file and deposit the taxes yourself."),
    ("Patriot Software, Full Service", 37, 5,
     "Patriot files and deposits."),
    ("Wave Payroll", 40, 6,
     "The $40 base applies to accounts opened after April 2025."),
    ("Gusto Simple", 49, 6, "The entry tier; benefits administration costs more."),
    ("OnPay", 49, 6, "One tier, everything included."),
    ("QuickBooks", None, None,
     "No standalone payroll price is published any more. The cheapest listed "
     "bundle is payroll plus accounting at $88 a month plus $6.50 per "
     "employee."),
    ("ADP RUN", None, None,
     "<b>No price published anywhere.</b> Both the pricing page and the "
     "package comparison show a quote request and a telephone number."),
]

# California Department of Insurance rate comparison, September 2024 edition -
# the most recent published. Median of the filed manual base rates per $100 of
# payroll, across 79 filings.
COMP = [("8834", "Physicians &amp; clerical: outpatient clinic", 1.25,
         0.53, 1.98),
        ("8810", "Clerical office employees", 0.40, 0.16, 1.21)]
COMP_N = 79
COMP_EDITION = "September 2024"


def money(n):
    return "$" + format(int(round(n)), ",d")


def section():
    o = ['<h2 id="%s">What it costs to run the payroll</h2>' % SECT_ID]
    o.append("<p>The table above is what the <i>employee</i> costs. Running a "
             "payroll is a separate line, and it is the one that surprises "
             "people, because it is a subscription that starts the month you "
             "hire and does not scale down for a single part-time associate. "
             "Three things have to happen before the first payslip.</p>")

    o.append("<p><b>Register with the EDD.</b> The trigger is not a salary "
             "and it is not annual: you must register once you pay more than "
             "<b>%s in wages in a calendar quarter</b>, and you have "
             "<b>%d days</b> from crossing it. An associate working two days "
             "a week crosses it in the first fortnight. Registration is free "
             "and is done through e-Services for Business.</p>"
             % (money(EDD_TRIGGER), EDD_DAYS))

    o.append("<p><b>Buy a payroll service, or do it by hand.</b> Doing it by "
             "hand means quarterly DE 9 and DE 9C filings, federal 941s, "
             "deposits on a schedule the IRS assigns you, and a W-2 in "
             "January &mdash; which your associate needs for the Board, not "
             "just for their taxes. Every published price below is for "
             "<b>one employee</b>, taken from the vendor's own pricing page "
             "in August 2026.</p>")

    rows = []
    for name, base, per, note in PAYROLL:
        if base is None:
            total = "Not published"
            detail = "&mdash;"
        else:
            total = money(base + per)
            detail = "%s + %s per employee" % (money(base), money(per))
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                    % (name, total, detail, note))
    o.append('<div class="tw"><table class="tbl"><tr><th>Service</th>'
             "<th>One employee, a month</th><th>How it is built</th>"
             "<th>Note</th></tr>" + "".join(rows) + "</table></div>")

    o.append("<p>So the realistic range is <b>%s to %s a month</b> &mdash; "
             "<b>%s to %s a year</b> &mdash; for the mechanics of paying one "
             "person. That is roughly one to two per cent on top of a %s "
             "salary, and it is the line most \"what does an employee cost\" "
             "calculations leave out entirely because it is not a tax."
             % (money(21), money(55), money(21 * 12), money(55 * 12),
                money(70000)))

    o.append("<p><b>Get the workers' compensation class code right.</b> The "
             "section above uses the statewide advisory average of $1.65 per "
             "$100 of payroll as a ceiling, and notes that an office-based "
             "mental health practice classifies well below it. Here is how far "
             "below. These are median filed manual base rates across %d "
             "carrier filings, from the California Department of Insurance's "
             "own rate comparison, %s edition &mdash; which is the most recent "
             "one published.</p>" % (COMP_N, COMP_EDITION))

    rows = []
    for code, label, med, lo, hi in COMP:
        rows.append("<tr><td>%s</td><td>%s</td><td>$%.2f</td><td>$%.2f "
                    "&ndash; $%.2f</td><td>%s on a %s payroll</td></tr>"
                    % (code, label, med, lo, hi, money(70000 * med / 100.0),
                       money(70000)))
    o.append('<div class="tw"><table class="tbl"><tr><th>Class code</th>'
             "<th>What it covers</th><th>Median rate per $100</th>"
             "<th>Range filed</th><th>On a $70,000 salary</th></tr>"
             + "".join(rows) + "</table></div>")

    o.append("<p>The spread between the cheapest and dearest filing for the "
             "same class code is nearly four to one, which is the argument "
             "for getting more than one quote. Two cautions carry over from "
             "the section above: carriers apply a minimum annual premium, so "
             "a single-employee policy may not scale down proportionally, and "
             "these are manual base rates that each insurer then modifies "
             "through its own rating plan. Treat the median as the middle of "
             "a real market, not as a quote.</p>")

    o.append("<p>Put together with the employer taxes above, the honest "
             "planning figure for a first associate on a $70,000 salary is a "
             "<b>multiplier of about 1.10 on the wage, plus $250 to $660 a "
             "year for the payroll service itself</b>. The percentage load is "
             "heaviest on a part-time hire, because the unemployment taxes "
             "stop at the first $7,000 of wages and the payroll subscription "
             "does not care how many hours anybody works.</p>")
    return "".join(o)


NAV_TITLE = "What it costs to run the payroll"


def renumber_nav(html):
    """Put the new heading into the page's own "On this page" rail.

    The rail is authored markup, not generated: a numbered list of anchors
    written into the page long before this pass existed. Adding an h2 without
    touching it produces a section the page's own navigation does not know
    about - which is exactly the class of silent, valid-markup failure this
    project keeps relearning, and it was how this pass shipped the first time.

    So the rail is rebuilt from the h2 ids that actually exist, in document
    order, with the numbers derived rather than typed. If the rail is ever
    regenerated by another pass, this becomes a no-op instead of a conflict.
    """
    m = re.search(r'<nav class="artnav">[\s\S]*?</nav>', html)
    if not m:
        return html
    nav = m.group(0)
    if "#%s" % SECT_ID in nav:
        pass  # already there; still renumber, in case an id moved

    heads = re.findall(r'<h2 id="([a-z0-9-]+)">(.*?)</h2>', html)
    if not heads:
        return html
    items = []
    for i, (hid, title) in enumerate(heads, 1):
        title = re.sub(r"<[^>]+>", "", title)
        items.append('<a href="#%s"><i class="tsn">%d</i>%s</a>'
                     % (hid, i, title))
    rebuilt = '<nav class="artnav"><b>On this page</b>%s</nav>' % "".join(items)
    return html.replace(nav, rebuilt, 1)


def main():
    if not os.path.exists(PAGE):
        sys.exit("payroll_ops: the hiring page is missing")
    s = open(PAGE, encoding="utf-8").read()
    orig = s

    # Remove any previous copy before re-inserting, so a changed price
    # replaces the old section rather than joining it.
    s = re.sub(r'<h2 id="%s">[\s\S]*?(?=<h2 id="what-an-associate-earns-you">)'
               % re.escape(SECT_ID), "", s)

    if s.count(ANCHOR) != 1:
        sys.exit("payroll_ops: the anchor heading matched %d times, expected "
                 "1. The page's structure has changed; do not guess a new "
                 "insertion point." % s.count(ANCHOR))
    s = s.replace(ANCHOR, section() + ANCHOR, 1)

    s = renumber_nav(s)

    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)
        print("hiring page: the payroll-operations section inserted, %d bytes"
              % len(section()))
    else:
        print("hiring page: already current")

    # --------------------------------------------------------------- guards
    bad = 0
    s = open(PAGE, encoding="utf-8").read()

    if s.count('id="%s"' % SECT_ID) != 1:
        print("GUARD: %d sections with id=%r"
              % (s.count('id="%s"' % SECT_ID), SECT_ID))
        bad += 1

    # The section must land between the cost table and the revenue section,
    # or it reads as part of the wrong argument.
    a = s.find('id="what-an-employee-actually-costs-in-california"')
    b = s.find('id="%s"' % SECT_ID)
    c = s.find('id="what-an-associate-earns-you"')
    if not (a < b < c) or -1 in (a, b, c):
        print("GUARD: the section is at %d, between %d and %d - it is not "
              "where it was meant to go" % (b, a, c))
        bad += 1

    if s.count("<h1") != 1:
        print("GUARD: %d h1 on the page" % s.count("<h1"))
        bad += 1

    for tag in ("table", "div", "tr", "td", "th"):
        o = len(re.findall(r"<%s\b" % tag, s))
        cl = len(re.findall(r"</%s>" % tag, s))
        if o != cl:
            print("GUARD: %d <%s> against %d </%s>" % (o, tag, cl, tag))
            bad += 1

    # No new CSS: the section reuses the page's own idiom. A class that is not
    # already styled on this page would ship an unstyled table.
    for cls in ("tw", "tbl"):
        if 'class="%s"' % cls not in orig:
            print("GUARD: the page has no .%s to borrow, so the new table "
                  "would render unstyled" % cls)
            bad += 1

    # Every price in the data must be on the page, or a vendor was dropped.
    for name, base, per, note in PAYROLL:
        if name not in s:
            print("GUARD: %s is not on the page" % name)
            bad += 1
        if base is not None and money(base + per) not in s:
            print("GUARD: %s's one-employee total is not on the page" % name)
            bad += 1

    # The rail has to list the new section, and its numbering has to match
    # the headings that exist. A section the page's own navigation does not
    # know about is the failure this pass shipped once already.
    nav = re.search(r'<nav class="artnav">[\s\S]*?</nav>', s)
    if not nav:
        print("GUARD: the page has no On-this-page rail to update")
        bad += 1
    else:
        nav = nav.group(0)
        heads = [h for h, t in re.findall(r'<h2 id="([a-z0-9-]+)">(.*?)</h2>', s)]
        listed = re.findall(r'<a href="#([a-z0-9-]+)"><i class="tsn">(\d+)</i>',
                            nav)
        if [h for h, n in listed] != heads:
            print("GUARD: the rail lists %s, the page has %s"
                  % ([h for h, n in listed], heads))
            bad += 1
        if [int(n) for h, n in listed] != list(range(1, len(heads) + 1)):
            print("GUARD: the rail's numbers are %s"
                  % [n for h, n in listed])
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - one section, in place, %d services and %d class "
          "codes, no new CSS" % (len(PAYROLL), len(COMP)))


if __name__ == "__main__":
    main()
