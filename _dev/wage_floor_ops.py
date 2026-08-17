#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""How you may lawfully pay an associate, on the page that already hires one.

WHY THIS IS A SECTION AND NOT A TENTH NEW PAGE

The ranked editorial list has `paying-your-associates-california.html` at
#7: "clinical rate versus administrative rate, what the market actually
pays at each stage, overhead, and the ethical-employer question." Checked
against what is already live, most of that is BUILT:

  associate-therapist-pay-los-angeles-bay-area.html  the $70,304 exempt
      floor, the local minimum wages, published scales from 19 named
      employers, and the compliant shape stated outright - piece rate for
      sessions, hourly for everything else
  associate-unpaid-hours-california.html             LAB 226.2 as the
      argument that wins a claim, and which agency hears it
  county-therapist-pay-california.html               what the market pays
  hiring-first-associate-california-therapist.html   the classification
      question, the loaded cost, the break-even caseload

So a #7 page would be a fourth URL on facts three pages already carry,
competing with all of them - the exact failure `payroll_ops.py` was
written to avoid, and this file follows its precedent deliberately.

WHAT IS ACTUALLY MISSING, AND IS REAL

The hiring page is the site's only EMPLOYER-side page, and it is the one
page that does not carry this material. Its "Salary or a percentage
split" section raises every issue and resolves none of them: it says
commission-style wages "still have to clear the minimum wage for every
hour worked", it names $16.90, and then it says "do not assume an
associate is exempt from overtime ... ask an employment lawyer". It never
names the salary floor, and it never names section 226.2 - the statute
that decides the question - though two other pages on this site do.

THE FOUR THINGS THIS ADDS

1. **The exempt salary floor, $70,304**, with the arithmetic shown, and
   the point that it tracks the STATE minimum wage - so a Los Angeles
   employer does not use the city figure. $70,000, the round number the
   page's own worked example uses for COST, is $304 under it.
2. **The enumerated professional exemption is closed.** Wage Order 4-2001
   section 1(A)(3) names eight professions - law, medicine, dentistry,
   optometry, architecture, engineering, teaching, accounting. None of
   them is psychotherapy. Salary alone never makes anyone exempt; the
   duties test is separate, and "primarily engaged" means more than half
   the employee's work time.
3. **Per-session pay is piece-rate pay, and LAB 226.2 governs it.**
   Separate compensation for rest and recovery periods and for other
   nonproductive time - which the statute defines - at stated rates. The
   session rate may not be averaged across that time.
4. **What the pay stub has to itemize**, which is where a practice that
   pays correctly still loses a claim.

SOURCING RULE: every figure is from a primary source read 16 August 2026
- 8 CCR 11040 (Wage Order 4-2001) for the exemption and the overtime
rates, LAB 226.2 for piece rate, the DIR minimum wage FAQ for $16.90,
LAB 515(c) for the full-time definition. The one derived number is
$70,304, and the section shows its arithmetic rather than asserting it.

Inserts one section between "Salary or a percentage split" and "What
supervision requires of you", in the page's own markup idiom - h2, p,
div.tw > table.tbl - so no new CSS ships for it.

Idempotent, guarded. Run after payroll_ops.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

PAGE = os.path.join(SITE, "hiring-first-associate-california-therapist.html")
ANCHOR = '<h2 id="what-supervision-requires-of-you">'
SECT_ID = "how-you-may-lawfully-pay-them"

MIN_WAGE = 16.90          # DIR, MW-2026, from 1 January 2026
FULL_TIME_HOURS = 2080    # LAB 515(c): 40 hours a week
EXEMPT_FLOOR = MIN_WAGE * 2 * FULL_TIME_HOURS       # 70,304
EXEMPT_MONTH = EXEMPT_FLOOR / 12.0                  # 5,858.67

# 8 CCR 11040 section 1(A)(3) - the professions named in the professional
# exemption. Psychotherapy is not among them, which is the finding.
ENUMERATED = ("law", "medicine", "dentistry", "optometry", "architecture",
              "engineering", "teaching", "accounting")

# What "other nonproductive time" means in a therapy practice. LAB 226.2
# defines it as time under the employer's control that is not directly
# related to the activity being paid by the piece; these are that time.
NONPRODUCTIVE = [
    ("Progress notes and treatment plans",
     "The writing attached to a session is not the session, and a "
     "per-session rate does not reach it."),
    ("The supervision hour the registration requires",
     "Required, scheduled, and under your control - it is working time "
     "however useful the associate finds it."),
    ("Case consultation, staff meetings and training",
     "Anything the practice calls the associate to."),
    ("No-shows and late cancellations",
     "Where the associate held the hour, the hour was under your "
     "control. No session was billed, so no piece was earned - which is "
     "precisely the case the statute is about."),
    ("Records requests, insurance calls and intake screening",
     "Administrative work for the practice, paid at an hourly rate."),
]


def money(n):
    return "$" + format(int(round(n)), ",d")


def money2(n):
    return "$" + format(n, ",.2f")


def section():
    o = ['<h2 id="%s">How you may lawfully pay them</h2>' % SECT_ID]

    o.append("<p>The section above sets out the two shapes an offer takes "
             "&mdash; a salary, or a share of what they bill. Both are "
             "lawful. Neither is lawful in every form, and the rules that "
             "decide it are not in the Board&rsquo;s statute at all: they "
             "are wage and hour law, they are enforced by a different "
             "agency, and an associate who brings a claim under them does "
             "not need the Board&rsquo;s permission to do it. Three "
             "questions settle almost every case.</p>")

    # --------------------------------------------------------- 1. exempt?
    o.append("<p><b>First: is the associate exempt? Almost certainly "
             "not.</b> Exemption is two tests and an employer has to pass "
             "both. The salary test is a floor. The duties test is a "
             "separate question about the work, and paying somebody well "
             "does not answer it &mdash; under Wage Order 4-2001 an exempt "
             "employee must be <i>primarily engaged</i> in exempt duties, "
             "and &ldquo;primarily&rdquo; is defined as more than one-half "
             "of their working time.</p>")

    o.append("<p>The duties test is where this usually ends. The wage "
             "order&rsquo;s professional exemption names its professions "
             "&mdash; %s and %s. That list is closed, and psychotherapy is "
             "not on it. Anyone claiming the exemption for a therapist is "
             "arguing the separate &ldquo;learned or artistic "
             "profession&rdquo; branch, which turns on advanced knowledge "
             "and on the customary and regular exercise of discretion and "
             "independent judgment &mdash; a real question for a registrant "
             "whose work is, by the definition in the Board&rsquo;s own "
             "statute, under another clinician&rsquo;s responsibility and "
             "control. This page does not tell you the answer for your "
             "practice. It tells you that the easy route is closed and the "
             "remaining one is a question for an employment lawyer, asked "
             "before the first payslip rather than after a claim.</p>"
             % (", ".join(ENUMERATED[:-1]), ENUMERATED[-1]))

    # ---------------------------------------------------------- 2. floor
    o.append("<p><b>Second: the salary floor, and it is not %s.</b> An "
             "exempt employee in California must earn a monthly salary of "
             "no less than two times the state minimum wage for full-time "
             "employment, which Labor Code &sect;&thinsp;515(c) fixes at 40 "
             "hours a week. In 2026 that arithmetic is fixed:</p>"
             % money(70000))

    o.append('<div class="tw"><table class="tbl">'
             "<tr><th>Step</th><th>Figure</th><th>Where it comes from</th></tr>"
             "<tr><td>State minimum wage, from 1 January 2026</td>"
             "<td>%s an hour</td><td>DIR, official notice MW-2026</td></tr>"
             "<tr><td>Twice the state minimum wage</td><td>%s an hour</td>"
             "<td>Wage Order 4-2001, &sect;&thinsp;1(A)</td></tr>"
             "<tr><td>Full-time year</td><td>%s hours</td>"
             "<td>Labor Code &sect;&thinsp;515(c), 40 hours a week</td></tr>"
             "<tr><td><b>The exempt salary floor</b></td><td><b>%s a "
             "year</b></td><td><b>%s a month</b></td></tr>"
             "</table></div>"
             % (money2(MIN_WAGE), money2(MIN_WAGE * 2),
                format(FULL_TIME_HOURS, ",d"), money(EXEMPT_FLOOR),
                money2(EXEMPT_MONTH)))

    o.append("<p>Two things follow that catch people out. The floor tracks "
             "the <b>state</b> minimum wage, so it is the same figure "
             "everywhere in California &mdash; a Los Angeles employer does "
             "not compute it from the city rate. And %s, the round number "
             "this page prices the hire on and the round number most first "
             "offers reach for, is <b>%s under it</b>. A salary below the "
             "floor is not an exempt salary no matter what the contract "
             "calls it, and the consequence is not a shortfall of %s: it is "
             "that the associate was non-exempt all along, with every hour "
             "over eight in a day owed at time and a half.</p>"
             % (money(70000), money(EXEMPT_FLOOR - 70000),
                money(EXEMPT_FLOOR - 70000)))

    o.append("<p>Which is the practical reading of all of this: for a first "
             "associate, budget as non-exempt, pay hourly or pay the "
             "overtime, and keep the timekeeping records that prove it. "
             "That is the cheap version of this problem.</p>")

    # ------------------------------------------------------ 3. piece rate
    o.append("<p><b>Third: a per-session rate is piece-rate pay, and it has "
             "its own statute.</b> This is the one that turns a good-faith "
             "split into a wage claim. Labor Code &sect;&thinsp;226.2 "
             "requires that an employee paid by the piece be compensated "
             "for rest and recovery periods and for <i>other nonproductive "
             "time</i> <b>separately from</b> the piece-rate compensation. "
             "The statute defines that time as time under the "
             "employer&rsquo;s control which is not directly related to the "
             "activity being paid by the piece. The session rate may not be "
             "spread across it, however generous the rate is.</p>")

    o.append("<p>Two rates, and they are not the same rate. Rest and "
             "recovery periods are paid at no less than the higher of the "
             "employee&rsquo;s average hourly rate or the applicable "
             "minimum wage. Other nonproductive time is paid at no less "
             "than the applicable minimum wage &mdash; and "
             "&ldquo;applicable&rdquo; is where a local ordinance bites, "
             "because that one <i>is</i> the city&rsquo;s figure, not the "
             "state&rsquo;s. In a therapy practice, the nonproductive time "
             "is not an edge case. It is most of the week that is not a "
             "session:</p>")

    rows = []
    for what, why in NONPRODUCTIVE:
        rows.append("<tr><td><b>%s</b></td><td>%s</td></tr>" % (what, why))
    o.append('<div class="tw"><table class="tbl">'
             "<tr><th>Paid separately, at an hourly rate</th>"
             "<th>Why the session rate does not reach it</th></tr>"
             + "".join(rows) + "</table></div>")

    o.append("<p>So the compliant shape of a per-session offer is not one "
             "number. It is two: a rate per completed session, and an "
             "hourly rate for everything else, tracked and paid as its own "
             "line. A practice that pays a single per-session figure and "
             "nothing for the notes is not driving a hard bargain &mdash; "
             "it is running the arrangement &sect;&thinsp;226.2 was "
             "written about.</p>")

    # ---------------------------------------------------------- the stub
    o.append("<p><b>And the pay stub has to show it.</b> Section 226.2 is "
             "also an itemization rule, which is how a practice that pays "
             "the right total still loses. The wage statement must "
             "separately state the total hours of compensable rest and "
             "recovery periods, the rate, and the gross wages paid for "
             "them; and the total hours of other nonproductive time, the "
             "rate, and the gross wages paid for that. A lump sum labelled "
             "&ldquo;admin&rdquo; does not satisfy it. Whatever payroll "
             "service you chose two sections up has to be set up to carry "
             "those lines, and the default configuration will not.</p>")

    o.append("<p>None of this is the Board&rsquo;s jurisdiction, which is "
             "why it does not appear in the supervision rules below and why "
             "asking the Board about it produces an answer that sounds like "
             "a shrug. It is the Labor Commissioner&rsquo;s. The "
             "associate&rsquo;s side of the same question &mdash; what to "
             "do when this has already gone wrong &mdash; is worked in full "
             "on <a href=\"associate-unpaid-hours-california.html\">the "
             "unpaid-hours page</a>, and the offer-by-offer version, with "
             "published scales from named employers, is on <a "
             "href=\"associate-therapist-pay-los-angeles-bay-area.html\">the "
             "associate pay page</a>. Nothing here is legal advice, and the "
             "duties test in particular is fact-specific: this section "
             "tells you which questions decide it and where the floors "
             "are.</p>")

    return "".join(o)


def renumber_nav(html):
    """Rebuild the page's authored On-this-page rail from the h2s that exist.

    Same reasoning as payroll_ops.renumber_nav: the rail is authored markup,
    so an h2 added without touching it produces a section the page's own
    navigation does not know about. Rebuilt from document order, numbers
    derived rather than typed, so the two passes cannot disagree.
    """
    m = re.search(r'<nav class="artnav">[\s\S]*?</nav>', html)
    if not m:
        return html
    heads = re.findall(r'<h2 id="([a-z0-9-]+)">(.*?)</h2>', html)
    if not heads:
        return html
    items = []
    for i, (hid, title) in enumerate(heads, 1):
        title = re.sub(r"<[^>]+>", "", title)
        items.append('<a href="#%s"><i class="tsn">%d</i>%s</a>'
                     % (hid, i, title))
    rebuilt = '<nav class="artnav"><b>On this page</b>%s</nav>' % "".join(items)
    return html.replace(m.group(0), rebuilt, 1)


def main():
    if not os.path.exists(PAGE):
        sys.exit("wage_floor_ops: the hiring page is missing")
    s = open(PAGE, encoding="utf-8").read()
    orig = s

    # Drop any previous copy before re-inserting, so a changed figure
    # replaces the old section rather than joining it.
    s = re.sub(r'<h2 id="%s">[\s\S]*?(?=%s)'
               % (re.escape(SECT_ID), re.escape(ANCHOR)), "", s)

    if s.count(ANCHOR) != 1:
        sys.exit("wage_floor_ops: the anchor heading matched %d times, "
                 "expected 1. The page's structure has changed; do not "
                 "guess a new insertion point." % s.count(ANCHOR))
    s = s.replace(ANCHOR, section() + ANCHOR, 1)
    s = renumber_nav(s)

    if s != orig:
        open(PAGE, "w", encoding="utf-8").write(s)
        print("hiring page: the lawful-pay section inserted, %d bytes"
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

    # It has to land between the split section and the supervision section,
    # or it is answering a question the page has not asked yet.
    a = s.find('id="salary-or-a-percentage-split"')
    b = s.find('id="%s"' % SECT_ID)
    c = s.find('id="what-supervision-requires-of-you"')
    if -1 in (a, b, c) or not (a < b < c):
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

    # No new CSS: the section borrows the page's own table idiom.
    for cls in ("tw", "tbl"):
        if 'class="%s"' % cls not in orig:
            print("GUARD: the page has no .%s to borrow, so the new table "
                  "would render unstyled" % cls)
            bad += 1

    # THE ARITHMETIC. $70,304 is the only derived figure on the section and
    # it is the one a stale minimum wage would silently falsify.
    if abs(EXEMPT_FLOOR - 70304) > 0.5:
        print("GUARD: the exempt floor computes to %s, not $70,304 - the "
              "minimum wage constant has moved and the prose around it "
              "needs rewriting, not just the number" % money(EXEMPT_FLOOR))
        bad += 1
    for must in (money(EXEMPT_FLOOR), money2(MIN_WAGE), money2(MIN_WAGE * 2),
                 money2(EXEMPT_MONTH)):
        if must not in s:
            print("GUARD: %s is not on the page" % must)
            bad += 1

    # The claim the section turns on: the enumerated list, in full. If a
    # profession is dropped the sentence stops being checkable.
    for prof in ENUMERATED:
        if prof not in s:
            print("GUARD: %r is missing from the enumerated exemption list"
                  % prof)
            bad += 1
    if "psychotherapy is not on it" not in s:
        print("GUARD: the page no longer states that psychotherapy is "
              "absent from the enumerated list")
        bad += 1

    # Cross-links, so this section stays a section and does not drift into
    # being a fourth page on the same facts.
    for href in ("associate-unpaid-hours-california.html",
                 "associate-therapist-pay-los-angeles-bay-area.html"):
        if href not in s:
            print("GUARD: the cross-link to %s is missing" % href)
            bad += 1

    # House rules.
    art = s
    if "guaranteed" in section().lower():
        print("GUARD: banned phrase 'guaranteed' in the new section")
        bad += 1
    if "LLC" in section():
        print("GUARD: 'LLC' in the new section")
        bad += 1

    # The rail has to list every section, in document order.
    nav = re.search(r'<nav class="artnav">[\s\S]*?</nav>', art)
    if not nav:
        print("GUARD: the page has no On-this-page rail to update")
        bad += 1
    else:
        heads = [h for h, t in re.findall(r'<h2 id="([a-z0-9-]+)">(.*?)</h2>',
                                          art)]
        listed = [h for h, n in
                  re.findall(r'<a href="#([a-z0-9-]+)"><i class="tsn">(\d+)</i>',
                             nav.group(0))]
        if listed != heads:
            print("GUARD: the rail lists %s, the page has %s"
                  % (listed, heads))
            bad += 1

    if bad:
        sys.exit("%d guard failure(s)" % bad)
    print("  guards clean - exempt floor %s, %d nonproductive rows, rail "
          "renumbered" % (money(EXEMPT_FLOOR), len(NONPRODUCTIVE)))


if __name__ == "__main__":
    main()
