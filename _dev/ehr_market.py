#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn a two-product comparison into the whole market, with every price.

THE REPORT

  "this page should actually be an entire comparison of all options for EHR
   systems like simple practice, and instead show all the optoins and prices
   and comparisons as landing page. and all this info seems useles here"

and, separately, that the page opened with a paragraph about being "somewhere
in a 30-day trial", which is a guess about the reader dressed as a fact.

WHAT IS KEPT, AND WHY THIS IS A PASS AND NOT A REBUILD

The existing page is ~200KB of checked research: supervisor co-signature
mechanics for associates, Good Faith Estimates under the No Surprises Act,
&sect;2290.5 telehealth consent including the fact that it covers associates,
BAA handling, what a couples call over video actually needs, and what happens
to your records for the seven years after you stop practising. None of that
gets better by being rewritten, and all of it would be lost by rebuilding the
page from a data file.

So: the head, the hero and the opening section are replaced, a full-market
section is inserted, and everything from "If you are an associate" onward is
left exactly as it is. `mock/articles/build_articles.py` cannot run - its
`_chrome.html` input is gone - so a pass is the only instrument available
here anyway.

WHAT THE RESEARCH FOUND, BEYOND THE PRICES

Three things worth knowing before reading the table:

  - **Power Diary is now Zanda.** powerdiary.com/pricing 302s to
    zandahealth.com/pricing. This is the third rebrand this site has had to
    absorb in a month, after CAQH -> DataSpring and TheraNest -> Ensora.
  - **One of the fifteen publishes no price at all.** Valant's plans-and-pricing
    page is a quote request. On this site that gets recorded as a fact about
    Valant rather than left as a blank cell.
  - **The sticker price is not the ranking.** TherapyNotes is $69 and meters
    the plumbing at 14 cents a unit; SimplePractice is $49 and includes it.
    Almost every "cheapest" claim in this market survives only until somebody
    bills a claim.

EVERY FIGURE IS THE VENDOR'S OWN, READ FROM ITS OWN PRICING PAGE IN AUGUST
2026. Promotional rates are noted as promotional and never used as the price.

Idempotent - it recognises its own output and removes it before re-inserting.
Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = "therapynotes-vs-simplepractice-california.html"
MARK = "<!-- _dev/ehr_market.py -->"
END = "<!-- /ehr_market -->"
CHECKED = "August 2026"

# name, url, solo price, what that buys, per extra clinician, telehealth,
# claims, free trial, note
# Sorted by the lowest price at which the product is usable by one clinician,
# because that is the column a reader scans.
SYSTEMS = [
    ("Carepatron", "https://www.carepatron.com/pricing",
     "$0", "free tier, unlimited clients, 1GB", "$31/user (Plus)",
     "included", "&mdash;", "free tier",
     "The only genuinely free tier here that includes telehealth and an AI "
     "scribe. 1GB of storage is the catch."),
    ("Zanda", "https://zandahealth.com/pricing",
     "$19", "Starter, 1,000 appointments a year", "$19 (Growth, $49 base)",
     "$9/clinician", "&mdash;", "14 days",
     "<b>Formerly Power Diary</b> &mdash; powerdiary.com now redirects here."),
    ("Healthie", "https://www.gethealthie.com/pricing",
     "$19", "Core, capped at 10 active clients", "$50 (Group, $149 base)",
     "included", "ClaimMD from $30/mo", "14 days",
     "$49 Essentials is the first realistic tier &mdash; 250 clients and "
     "CMS-1500s."),
    ("TheraNest", "https://ensorahealth.com/pricing/theranest-mental-health/",
     "$29", "Essentials, per therapist", "$29+ per therapist",
     "add-on; unlimited on Premier", "30 free/mo on Advanced", "21 days",
     "Now <b>Ensora Mental Health</b>. Insurance billing automation is the "
     "$89 Premier tier."),
    ("Practice Better", "https://www.practicebetter.io/pricing",
     "$35", "Starter, capped at 10 clients", "$50 (Team, $155 base)",
     "included", "&mdash;", "14 days",
     "Built for nutrition and coaching first. $69 Professional is the first "
     "tier that holds a caseload."),
    ("Sessions Health", "https://sessionshealth.com/pricing",
     "$39", "unlimited clients, everything core", "$29",
     "$10/clinician", "from $0.25/claim", "30 days",
     "Free up to 3 clients. The cheapest uncapped solo plan in this table."),
    ("TheraPlatform", "https://www.theraplatform.com/pricing",
     "$39", "Basic, one provider only", "$39&ndash;$49 (Pro tiers)",
     "unlimited, included", "$0.25/claim", "30 days",
     "Basic does not allow a second provider at all."),
    ("SimplePractice", "https://www.simplepractice.com/pricing/",
     "$49", "Starter", "$74 (Plus group)",
     "included", "35 free/mo on Plus", "30 days",
     "$79 Essential is where template customisation starts, which matters "
     "for a California telehealth consent."),
    ("CarePaths", "https://www.carepaths.com/pricing",
     "$49", "EHR plus measurement-based care", "$5.75&ndash;$49",
     "&mdash;", "&mdash;", "30 days",
     "$5.75 a head for students is the lowest training-clinic rate found."),
    ("Jane", "https://jane.app/pricing",
     "$54", "Balance, capped at 20 appointments a month", "$39 PT / $79 FT",
     "$15/clinician for group", "$20 + $5/FT clinician", "&mdash;",
     "$79 Practice is the first uncapped tier. Insurance billing is a "
     "separate line."),
    ("ICANotes", "https://www.icanotes.com/pricing/",
     "$55", "notes only, non-prescriber", "per clinician",
     "$20/user", "contact sales", "30 days",
     "$75 for scheduling and billing. <b>Three-month minimum commitment.</b>"),
    ("TherapyAppointment", "https://www.therapyappointment.com/pricing",
     "$59", "standard, over 40 sessions a month", "$39",
     "$15/provider, or $5 with your own Zoom", "$0.15/claim", "30 days",
     "$10 and $39 intro tiers while your caseload is still small."),
    ("TherapyNotes", "https://www.therapynotes.com/pricing/",
     "$69", "solo, single user", "$50 (group, $79 base)",
     "basic free; Premium $15", "14&cent;/claim", "30 days",
     "Meters the plumbing: 14&cent; a claim, a reminder or an eligibility "
     "check. ePrescribe is $65."),
    ("IntakeQ / Practice Q", "https://intakeq.com/pricing",
     "$84.90", "practice management, telehealth included", "$30",
     "included", "&mdash;", "14 days",
     "$59.90 low-volume tier caps you at 25 appointments a month. Forms-first "
     "by design."),
    ("Valant", "https://www.valant.io/plans-pricing/",
     "not published", "quote only", "not published",
     "not published", "not published", "&mdash;",
     "The pricing page is a quote request. &ldquo;Flexible pricing that is "
     "customized&rdquo; is the whole of it."),
]

CATEGORIES = [
    ("A full EHR",
     "Scheduling, notes, a client portal, billing and claims in one system. "
     "SimplePractice, TherapyNotes, TheraNest, Sessions Health, "
     "TherapyAppointment, TheraPlatform, CarePaths, Jane, Valant.",
     "What a solo California practice that bills insurance needs."),
    ("Notes first",
     "Documentation and little else, priced accordingly. ICANotes at $55 is "
     "the clearest example.",
     "Only if something else already does your scheduling and billing."),
    ("Forms first",
     "Intake, consent and questionnaires as the centre of the product, with "
     "practice management bolted on. IntakeQ / Practice Q.",
     "Strong if your intake paperwork is the part that hurts."),
    ("Wellness platforms",
     "Built for nutrition, coaching and allied health, sold to therapists "
     "too. Practice Better, Healthie, Carepatron, Zanda.",
     "Cheaper, and thinner on the mental-health specifics &mdash; treatment "
     "plans, CPT sets, superbill formatting."),
    ("A network that includes one",
     "Alma, Headway and Grow Therapy give you scheduling, notes and billing "
     "as part of the network rather than as a subscription.",
     "You are not paying for software; you are paying a share of every "
     "session. Priced on <a href=\"alma-for-california-therapists.html\">the "
     "network pages</a>."),
]


def block():
    o = [MARK]
    o.append('<h2 id="every-system-and-what-it-publishes">Every system, and '
             'what it actually publishes</h2>')
    o.append("<p>Fifteen practice-management systems a California therapist "
             "can buy today. Fourteen publish a price; one does not, and that "
             "is recorded here as a fact about the vendor rather than left as "
             "an empty cell. Every figure below was read from the vendor's own "
             "pricing page in %s, and the link on each name goes to the page "
             "it came from.</p>" % CHECKED)
    o.append("<p><b>Promotional rates are not prices.</b> Six of these were "
             "running a half-off introductory offer on the day they were "
             "checked. None of those numbers is in the table. What is in the "
             "table is what you pay in month seven.</p>")

    o.append('<div class="tw"><table class="tbl"><thead><tr>'
             "<th>System</th><th>Cheapest solo plan</th><th>What that buys</th>"
             "<th>Each extra clinician</th><th>Telehealth</th>"
             "<th>Claims</th><th>Trial</th></tr></thead><tbody>")
    for name, url, solo, buys, extra, tele, claims, trial, _note in SYSTEMS:
        o.append("<tr><td><a href=\"%s\" target=\"_blank\" rel=\"noopener\">"
                 "%s</a></td><td><b>%s</b></td><td>%s</td><td>%s</td>"
                 "<td>%s</td><td>%s</td><td>%s</td></tr>"
                 % (url, name, solo, buys, extra, tele, claims, trial))
    o.append("</tbody></table></div>")
    o.append('<p class="cap">Monthly, in US dollars, billed monthly. Annual '
             'billing takes roughly 10&ndash;15%% off at most of them. Checked '
             '%s.</p>' % CHECKED)

    o.append("<h3>What the sticker price leaves out</h3>")
    o.append("<p>The column that decides your bill is not the first one. Two "
             "systems four dollars apart on the pricing page can be forty "
             "dollars apart in practice, and it runs in both directions:</p>")
    o.append("<ul>")
    o.append("<li><b>Claims.</b> 14&cent; at TherapyNotes, 15&cent; at "
             "TherapyAppointment, 25&cent; at Sessions Health and "
             "TheraPlatform, bundled at SimplePractice and IntakeQ. At 80 "
             "claims a month that is a range of $0 to $20.</li>")
    o.append("<li><b>Reminders.</b> 14&cent; a text at TherapyNotes, 5&cent; "
             "at Practice Better, 9&cent; at Zanda, bundled at several "
             "others. Email reminders are free everywhere.</li>")
    o.append("<li><b>Telehealth.</b> Free at some, $9&ndash;$20 a clinician a "
             "month at others. If you see couples who join from two "
             "addresses, check the participant cap before you check the "
             "price &mdash; TherapyNotes' free tier stops at two.</li>")
    o.append("<li><b>Card processing.</b> 2.9% + 30&cent; at most, "
             "<b>3.1% + 30&cent;</b> at TherapyNotes. On $120,000 of card "
             "revenue those two tenths of a percent are $240 a year, which is "
             "more than the entire headline gap between most of these "
             "systems.</li>")
    o.append("<li><b>The AMA CPT licence.</b> A separate December line at "
             "several vendors &mdash; $19.50 a therapist at TheraNest. It is "
             "not on any pricing page.</li>")
    o.append("<li><b>AI notes.</b> $30&ndash;$49 a clinician a month almost "
             "everywhere, or 59&cent; a note at TherapyAppointment. If you "
             "will use it, it is the largest single add-on in this market and "
             "it can double a $39 subscription.</li>")
    o.append("</ul>")

    o.append("<h3>Five kinds of product, sold as one category</h3>")
    o.append("<p>A list of fifteen prices implies fifteen comparable things. "
             "They are not comparable, and the cheapest row is usually cheap "
             "because it is a different product:</p>")
    o.append('<div class="tw"><table class="tbl"><thead><tr><th>Kind</th>'
             "<th>Which ones</th><th>When it is the right answer</th>"
             "</tr></thead><tbody>")
    for kind, which, when in CATEGORIES:
        o.append("<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>"
                 % (kind, which, when))
    o.append("</tbody></table></div>")

    o.append("<h3>The notes worth reading before you shortlist</h3>")
    o.append("<ul>")
    for name, url, _s, _b, _e, _t, _c, _tr, note in SYSTEMS:
        o.append('<li><b><a href="%s" target="_blank" rel="noopener">%s</a>'
                 "</b> &mdash; %s</li>" % (url, name, note))
    o.append("</ul>")

    o.append("<p><b>Two of the fifteen changed identity this year.</b> "
             "Power&nbsp;Diary is now Zanda and powerdiary.com redirects; "
             "TheraNest is now Ensora Mental Health. If a comparison you read "
             "elsewhere still calls them by the old names, it has not been "
             "checked since at least 2025 &mdash; and neither, probably, have "
             "its prices.</p>")

    o.append("<p>The rest of this page is the part a price table cannot do: "
             "what two of these actually feel like to run a California "
             "practice on. TherapyNotes and SimplePractice are the two most "
             "California therapists end up choosing between, so they are the "
             "two taken apart in detail below &mdash; supervisor "
             "co-signature, Good Faith Estimates, "
             "&sect;&thinsp;2290.5 telehealth consent, and what happens to "
             "your records for the seven years after you stop.</p>")
    o.append(END)
    return "".join(o)


NAV = (
    '<nav class="artnav"><b>On this page</b>'
    '<a href="#every-system-and-what-it-publishes"><i class="tsn">1</i>'
    "Every system, and what it publishes</a>"
    '<a href="#what-each-one-charges-and-what-that-works-out-to">'
    '<i class="tsn">2</i>What TherapyNotes and SimplePractice charge</a>'
    '<a href="#if-you-are-an-associate-or-you-supervise-one">'
    '<i class="tsn">3</i>If you are an associate, or you supervise one</a>'
    '<a href="#the-california-questions"><i class="tsn">4</i>'
    "The California questions</a>"
    '<a href="#seven-years-after-your-last-session-and-how-to-get-out">'
    '<i class="tsn">5</i>Seven years after your last session, and how to get '
    "out</a>"
    '<a href="#what-is-wrong-with-each-of-them"><i class="tsn">6</i>'
    "What is wrong with each of them</a>"
    '<a href="#the-verdict"><i class="tsn">7</i>The verdict</a>'
    '<a href="#what-to-do-on-monday"><i class="tsn">8</i>'
    "What to do on Monday</a></nav>")

H1 = ("Every practice-management system a California therapist can buy, "
      "<em>with the price each one publishes</em>")
DEK = ("Fifteen systems, from $0 to $99 a month for one clinician &mdash; and "
       "one that publishes nothing at all. Then the two most California "
       "therapists actually choose between, taken apart on the things a "
       "feature grid never covers: supervisor co-signature, Good Faith "
       "Estimates, &sect;&thinsp;2290.5 telehealth consent, and what happens "
       "to your records for the seven years after you stop.")
KICK = "California &middot; practice software"
FIG = ("$0&ndash;$99", "the published solo price, before a single add-on")
TITLE = ("Every therapy EHR compared, priced &mdash; California, 2026 "
         "| Therapist Support")
DESC = ("Fifteen practice-management systems for California therapists with "
        "every published price, what each add-on actually costs, and a "
        "detailed TherapyNotes vs SimplePractice comparison. Checked "
        "August 2026.")


def main():
    p = os.path.join(SITE, PAGE)
    if not os.path.exists(p):
        sys.exit("ehr_market: %s is missing" % PAGE)
    s = open(p, encoding="utf-8").read()
    orig = s
    print("the whole market, on %s" % PAGE)

    # ------------------------------------------------------- remove our own
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)

    # ------------------------------------------------- the opening section
    # Anchored on the id, not the heading text, because the heading text also
    # appears in the on-this-page nav a few hundred characters earlier - the
    # exact pattern that has bitten this project eight times.
    # Our own block has already been stripped above, so this always inserts
    # exactly once. On the first run the preamble is still there and gets
    # replaced; on every run after that it is gone and the block goes at the
    # top of the body. There is no third branch, because a branch that leaves
    # the block out is how an idempotent pass silently empties a page.
    start = s.find('<h2 id="where-you-probably-are-right-now">')
    if start > 0:
        nxt = s.find('<h2 id="what-each-one-charges', start + 1)
        if nxt < start:
            sys.exit("ehr_market: found the preamble but not the section "
                     "after it - refusing to guess where it ends")
        n = nxt - start
        if not (900 < n < 4000):
            sys.exit("ehr_market: the preamble measures %d chars, expected "
                     "900-4000. Refusing to cut - a match that ran away takes "
                     "the page with it." % n)
        s = s[:start] + block() + s[nxt:]
        print("  ok       replaced the 30-day-trial preamble (%d chars) with "
              "the market section" % n)
    else:
        m = re.search(r'<div class="artbody">', s)
        if not m:
            sys.exit("ehr_market: no .artbody to insert into")
        s = s[:m.end()] + block() + s[m.end():]
        print("  ok       market section inserted at the top of the body")

    # ------------------------------------------------------------- the nav
    s = re.sub(r'<nav class="artnav">[\s\S]*?</nav>', NAV, s, count=1)

    # ------------------------------------------------------------ the hero
    s = re.sub(r'<p class="kick">[\s\S]*?</p>', '<p class="kick">%s</p>' % KICK,
               s, count=1)
    s = re.sub(r"<h1[^>]*>[\s\S]*?</h1>", "<h1>%s</h1>" % H1, s, count=1)
    s = re.sub(r'<p class="dek">[\s\S]*?</p>', '<p class="dek">%s</p>' % DEK,
               s, count=1)
    s = re.sub(r'(<div class="artfig">\s*<b>)[\s\S]*?(</span>)',
               r"\g<1>%s</b><span>%s\g<2>" % FIG, s, count=1)

    # ------------------------------------------------------------- the head
    # ts:number feeds the In-short card in pixel_concepts.py. Leaving it stale
    # would put the old $31 headline back on the page in a different box.
    s = re.sub(r"<title>[\s\S]*?</title>", "<title>%s</title>" % TITLE, s,
               count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               r"\g<1>%s\g<2>" % DESC, s, count=1)
    for key, val in (("ts:number", "$0&ndash;$99 a month"),
                     ("ts:question",
                      "Which practice-management system should a California "
                      "therapist use?"),
                     ("ts:answer",
                      "Fifteen compared on what each one actually publishes")):
        if re.search(r'<meta name="%s" content="' % key, s):
            s = re.sub(r'(<meta name="%s" content=")[^"]*(")' % key,
                       lambda m, v=val: m.group(1) + v + m.group(2), s, count=1)

    if s != orig:
        open(p, "w", encoding="utf-8").write(s)

    # ---------------------------------------------------------------- guards
    bad = 0
    s = open(p, encoding="utf-8").read()

    if s.count(MARK) != 1:
        print("GUARD: %d market blocks" % s.count(MARK)); bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1

    # Every system must appear with its price AND a link to the page the price
    # came from. A row whose source link went missing is a number nobody can
    # check, which on this site is worse than no number.
    for name, url, solo, *_rest in SYSTEMS:
        if url not in s:
            print("GUARD: %s has no source link on the page" % name); bad += 1
        if solo not in s:
            print("GUARD: %s's price %r is not on the page intact"
                  % (name, solo)); bad += 1

    # The research below the fold must survive. This pass replaces the top of
    # an article whose builder cannot run; if it ever eats the body, there is
    # no way to regenerate it.
    for keep in ('id="if-you-are-an-associate-or-you-supervise-one"',
                 'id="the-california-questions"',
                 'id="seven-years-after-your-last-session-and-how-to-get-out"',
                 'id="the-verdict"', "Good Faith Estimate", "2290.5"):
        if keep not in s:
            print("GUARD: %r is gone. The pass has eaten research it cannot "
                  "rebuild." % keep)
            bad += 1

    # The preamble it was asked to remove must actually be gone.
    if "somewhere in a 30-day trial" in s:
        print("GUARD: the 30-day-trial preamble survived"); bad += 1

    # Every nav entry must point at a heading that exists.
    for href in re.findall(r'<a href="#([a-z0-9-]+)"><i class="tsn">', s):
        if 'id="%s"' % href not in s:
            print("GUARD: the nav links #%s, which is not on the page" % href)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("\n%d systems, %d with a published price. guards clean - every "
          "figure carries a link to the page it came from, and the California "
          "research below the fold is intact"
          % (len(SYSTEMS),
             len([x for x in SYSTEMS if x[2] != "not published"])))


if __name__ == "__main__":
    main()
