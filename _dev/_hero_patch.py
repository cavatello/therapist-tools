import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()

# ---------------------------------------------------------------- docstring
s = s.replace('''WHY THIS DESIGN AND NOT THE OTHER TWO''',
'''WHO ACTUALLY ARRIVES HERE, WHICH THE FIRST VERSION GOT WRONG

The first build opened with "One bar. Four gates. Nothing you type here leaves
this browser." That headline describes a widget. It was written for somebody
arriving from a link posted in a group - already oriented, wanting the tool -
and that is not who mostly arrives. Most arrive cold, from a search for one
specific question, and a cold arrival needs to learn three things in the first
screen:

    am I in the right place, is this the whole thing, and where do I start

The old hero answered none of them. Two of its four blocks were about privacy,
which is a trust signal and not a reason to stay, and its four figures were the
statute - 3,000, 1,750, 500, 104 - numbers a registered associate already
knows. Nothing said "everything for this stage, in one place", so the page read
as a single calculator rather than a hub over twenty pages.

So the order is now: what this is and how much of it there is, then the four
places most people start, then the tool, then the shelf grouped by subject.
The privacy promise sits with the tool, where it is the answer to an actual
question, rather than in the headline where it displaced the offer.

WHY THIS DESIGN AND NOT THE OTHER TWO''')

# ------------------------------------------------------------------- jumps
s = s.replace('''JUMPS = [("ledger", "Where you are"),
         ("asking", "What this room asks"),
         ("shelf", "Everything for this stage"),
         ("sources", "The rules behind it")]''',
'''JUMPS = [("start", "Start here"),
         ("ledger", "Where you are"),
         ("asking", "What this room asks"),
         ("shelf", "All %d guides"),
         ("sources", "The rules behind it")]

# The four things most people arrive wanting. Ordered by how often the
# question turns up, not by how good the page is.
START = [
    ("amft-3000-hours-california.html", "When do I actually finish?",
     "Your date, from the hours you are really logging"),
    ("getting-hired-as-a-california-associate.html",
     "Why is nobody hiring me?",
     "It is a billing rule, and it is not about your hour count"),
    ("associate-therapist-pay-los-angeles-bay-area.html",
     "What should this job pay?",
     "Salary against per-session, and what counties actually pay"),
    ("associate-unpaid-hours-california.html", "Do I have to work unpaid?",
     "No, and there is a wage claim with a deadline"),
]

# The shelf, grouped. Twenty ungrouped cards is a wall; five headed groups is
# a table of contents, and a cold arrival can see the shape of the whole thing
# without reading any of it.
GROUPS = [
    ("Your hours, and what counts toward them",
     ["amft-3000-hours-california.html",
      "practicum-california-mft-trainee.html",
      "associate-hours-telehealth-out-of-state.html",
      "associate-hours-trackers-compared.html",
      "out-of-state-to-california-licensure.html"]),
    ("Getting hired, and what it pays",
     ["getting-hired-as-a-california-associate.html",
      "associate-mft-job-advisor.html",
      "associate-therapist-pay-los-angeles-bay-area.html",
      "county-therapist-pay-california.html",
      "county-job-portals-california.html",
      "medi-cal-safety-net-employers-california.html",
      "associate-unpaid-hours-california.html"]),
    ("Money back on your loans",
     ["loan-forgiveness-employers-california.html",
      "mbh-slrp-california.html"]),
    ("The Board: exams, fees and waiting",
     ["bbs-exam-pass-rates-california.html",
      "bbs-processing-times-california.html",
      "bbs-fees-california-2026.html",
      "continuing-education-california-lmft.html",
      "therapist-discipline-cases-california.html"]),
    ("The market you are qualifying into",
     ["therapists-by-county-california.html"]),
]''')
open(p, "w", encoding="utf-8").write(s)
print("docstring + jumps + START + GROUPS")

s = open(p, encoding="utf-8").read()

# ------------------------------------------------------------------- hero
old_hero = s[s.index("    o.append(pk.hero("):s.index("    # ---------------------------------------------------------------- ledger")]
new_hero = '''    o.append(pk.hero(
        "For California associates &middot; AMFT, ASW and APCC",
        "Everything a California associate needs, in one place.",
        "%d guides for the years between registration and your license "
        "&mdash; the hours and what counts toward them, why employers can or "
        "cannot hire you, what the work pays county by county, the loan "
        "repayment nobody mentions, and the Board&rsquo;s own numbers on "
        "exams and waiting times. Every figure comes from a named source, and "
        "the whole site is free."
        % len(shelf),
        [(str(len(shelf)), "guides for this stage"),
         ("58", "county job portals, checked"),
         ("165,000", "licensees in the register"),
         ("$0", "and no account, ever")],
        JUMPS))

    # ----------------------------------------------------------------- start
    o.append('<section class="pk-sec" id="start">')
    o.append('<p class="pk-k">Start here</p>')
    o.append('<h2 class="pk-h">Four questions bring most people to this '
             "page.</h2>")
    o.append('<p class="pk-d">Written for AMFTs. Where a rule differs for an '
             "ASW or an APCC, the page says so and links to the difference.</p>")
    o.append('<div class="start">')
    for href, q, sub in START:
        o.append('<a href="%s%s"><span class="q">%s</span>'
                 '<span class="s">%s</span></a>' % (UP, href, q, sub))
    o.append("</div>")
    o.append("</section>")

'''
s = s.replace(old_hero, new_hero)

# JUMPS carries a %d for the shelf count; fill it where the hero is built.
s = s.replace("        JUMPS))\n\n    # ----------------------------------------------------------------- start",
              "        [(h, l % len(shelf) if '%d' in l else l)\n"
              "         for h, l in JUMPS]))\n\n"
              "    # ----------------------------------------------------------------- start")
open(p, "w", encoding="utf-8").write(s)
print("hero + start section")

s = open(p, encoding="utf-8").read()

# --------------------------------------------- plain words, not "gates"
s = s.replace('''THE GATE THAT LEADS

Of the four sub-totals inside the 3,000, the one people miss is the 500
relational hours - counselling couples, families and children. Somebody can
reach 3,000 total and 1,750 direct and still not be finished. So the
relational gate is the highest-contrast element on the page, not a footnote in
the fourth tile.''',
'''THE WORD "GATE" IS GONE, AND THE REASON IS NOT ONLY THE JARGON

This page used to call the four requirements "gates". Two things were wrong
with that. Nobody outside the person who wrote it knows what a gate is meant
to be. And it framed the 3,000 as the thing you are working toward, when the
3,000 is almost never what decides anybody's date - a caseload of adult
individuals closes the total long before it produces 500 relational hours, and
the 104 weeks bind anyone moving quickly.

So they are requirements, they are named that, and the page says plainly which
one usually runs out last rather than implying it is the big number at the
top.''')

s = s.replace('''        "One bar. Four gates. Nothing you type here leaves this browser.",''',
              '''        "Everything a California associate needs, in one place.",''')
s = s.replace('"500 relational hours is the gate people reach 3,000 without"',
              '"The 3,000 is almost never what decides your date"')
s = s.replace('''        [("3,000", "hours in total"),
         ("1,750", "direct clinical"),
         ("500", "relational &mdash; the gate"),
         ("104", "weeks minimum")],''',
              '''        [(str(len(shelf)), "guides for this stage"),
         ("58", "county job portals, checked"),
         ("165,000", "licensees in the register"),
         ("$0", "and no account, ever")],''')
s = s.replace('("500", "relational &mdash; the gate")', '("500", "relational hours")')
s = s.replace("The whole requirement, in one line.",
              "Which requirement is actually holding you up?")
s = s.replace('''"Four numbers off your own log. The bar is the 3,000; the tiles are the "
             "sub-totals underneath it, and one of them stops more people than "
             "the rest.</p>")''',
              '''"Four numbers off your own log. There are four requirements and "
             "they fill at different speeds &mdash; the total is almost never "
             "the one you are actually waiting on.</p>")''')
s = s.replace('''"The relational gate is "
             "marked because it is the one people reach 3,000 without: 500 "
             "hours with couples, families and children, inside the 1,750. "''',
              '''"Relational hours are "
             "highlighted because they are what people reach 3,000 without: "
             "500 hours with couples, families and children, inside the "
             "1,750, and an all-adult caseload never produces them. "''')
s = s.replace('("gRel", "Relational"),', '("gRel", "Relational hours"),')
s = s.replace('("gWeeks", "Weeks"), ("gWhen", "Weeks still to go")',
              '("gWeeks", "Weeks elapsed"), ("gWhen", "Weeks still to go")')
s = s.replace('"the relational gate", "reach 3,000 without"',
              '"the relational finding", "almost never what decides your date"')
s = s.replace('("the relational gate", "reach 3,000 without"),',
              '("the plain-language finding", "almost never what decides your date"),')
s = s.replace('''        "The four numbers, and where they come from",''',
              '''        "The four requirements, and where they come from",''')
s = s.replace("relational gate", "relational requirement")
s = s.replace("Four gates", "Four requirements")
s = s.replace("four gates", "four requirements")
open(p, "w", encoding="utf-8").write(s)
print("gate language removed from the builder")
