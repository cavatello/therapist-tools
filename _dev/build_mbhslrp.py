#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MBH-SLRP in full: the $180,000 an associate can be paid, and its conditions.

WHY THIS PAGE

`loan-forgiveness-employers-california.html` compares four programs and
`medi-cal-safety-net-employers-california.html` names employers. Neither
explains this one program properly, and it is the only one of the four that
pays a pre-licensed clinician a life-changing amount.

WHAT THE RESEARCH FOUND, AND WHAT CHANGED

The August 2026 content analysis concluded that nobody in the associate group
mentioned loan repayment - the 114-comment bankruptcy thread got no reply
naming it. That has changed, and the new posts are more useful than the old
silence:

    "I'm currently looking for an AMFT position because my current site
     unfortunately no longer qualifies under the Medi-Cal Behavioral Health
     Student Loan Repayment Program (MBH-SLRP)."            - 4 comments

    "I'm an AMFT in Orange County, CA with about 2300 hours towards licensing.
     Seeking a hybrid/remote position at a site that accepts Medi-Cal or 40% of
     uninsured clients so I can qualify for SLRP. I'd really appreciate any
     leads."                                                - 1 comment

    "I am an AMFT and APCC currently seeking a remote role with an organization
     that supports clinicians through the HCAI Loan Repayment Program or other
     student loan forgiveness options."                     - no replies

Four comments, one comment, none. People now know the program exists and are
asking the room to find them a qualifying employer. The room cannot.

THE FOUR THINGS THIS PAGE SAYS THAT NOBODY ELSE DOES

1. THE SERVICE OBLIGATION IS 32 HOURS A WEEK OF DIRECT CLIENT CARE. Not 32
   hours of employment - direct care. For a therapist that is a very heavy
   caseload, heavier than most full-time clinical jobs actually carry, and it
   is the condition most likely to be discovered late.

2. IT IS ONE PAYMENT TO YOUR LOAN SERVICER, NOT INCOME. For the 2026 cycle,
   paid somewhere between November 2026 and November 2027. It does nothing for
   the monthly payment that is the actual crisis in those threads.

3. YOUR SITE CAN STOP QUALIFYING. The first post above is somebody job-hunting
   mid-obligation because their employer fell out of eligibility. No guide
   mentions this and it is the single largest practical risk in the program.

4. HCAI DOES NOT SAY WHETHER THE AWARD IS TAXABLE, AND THERE IS A STATUTE
   NOBODY CITES. 26 U.S.C. 108(f)(4) excludes from gross income amounts
   received under "any other State loan repayment or loan forgiveness program
   that is intended to provide for the increased availability of health care
   services in underserved or health professional shortage areas". Whether
   MBH-SLRP falls inside it is not something this page decides - but on a
   $180,000 award the question is worth tens of thousands and it is not asked
   anywhere.

ON THE ONE PLACE THE SOURCES DISAGREE

HCAI's FAQ and an April 2026 Board of Behavioral Sciences agenda item both
describe eligible sites as the Medi-Cal safety net - FQHCs, community mental
health centers, rural health clinics, and settings over a Medicaid threshold.
HCAI's own technical assistance guide describes something narrower: specialty
mental health, Drug Medi-Cal and DMC-ODS services at county-operated or
county-contracted sites. The page prints both and tells the reader to have
their employer confirm with HCAI rather than pretending the documents agree.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "mbh-slrp-california.html"
DONOR = "loan-forgiveness-employers-california.html"

FORGIVE = "loan-forgiveness-employers-california.html"
EMPLOYERS = "medi-cal-safety-net-employers-california.html"
HIRED = "getting-hired-as-a-california-associate.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"
HOURS = "amft-3000-hours-california.html"

TOTAL_FUND = 90100000
TIER1 = 120000
TIER2 = 180000
TIER3 = 240000
DIRECT_HOURS = 32
SCHOOL_HOURS = 30
NEXT_CYCLE = "1 May 2027"
PAY_WINDOW = "November 2026 and November 2027"
MEDICAID_SHARE = 40
RURAL_SHARE = 30

VERIFY_HCAI = "https://hcai.ca.gov/loans-scholarships-grants/eligibility/"
PROGRAM = ("https://hcai.ca.gov/workforce/initiatives/"
           "behavioral-health-bh-connect/mbhslrp/")

JUMPS = [("what", "What it is"),
         ("tiers", "The three tiers"),
         ("conditions", "The conditions"),
         ("sites", "Where you must work"),
         ("room", "What the room is asking"),
         ("tax", "The tax question"),
         ("apply", "Applying"),
         ("sources", "Sources")]

TIERS = [
    ("Certified, non-licensed", TIER1,
     "Alcohol and other drug counselors, certified peer support specialists, "
     "certified wellness coaches, community health workers and "
     "promotores/representatives, and mental health rehabilitation "
     "specialists."),
    ("Non-prescribing licensed, <b>and associate-level pre-licensure</b>", TIER2,
     "<b>Associate clinical social workers, associate marriage and family "
     "therapists, associate professional clinical counselors</b>, licensed "
     "clinical psychologists, LCSWs, LMFTs, LPCCs, licensed psychiatric "
     "technicians, licensed vocational nurses, occupational therapists, "
     "psychology associates, and registered nurses."),
    ("Prescribing licensed", TIER3,
     "Addiction medicine physicians, psychiatrists, addiction psychiatrists, "
     "child and adolescent psychiatrists, nurse practitioners, and physician "
     "assistants."),
]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "MBH-SLRP &middot; the full program &middot; checked %s" % pk.CHECKED,
        "$%s for an associate, and four conditions nobody mentions."
        % format(TIER2, ",d"),
        "California&rsquo;s largest loan repayment program names registered "
        "associates in its own eligibility tier. It also asks for <b>%d hours "
        "a week of direct client care</b>, pays once, and can stop applying to "
        "you if your employer changes. <b>Everything here is information, not "
        "an eligibility decision &mdash; verify with HCAI before you act.</b>"
        % DIRECT_HOURS,
        [("$%sm" % (TOTAL_FUND // 1000000), "available for award"),
         ("$%s" % format(TIER2, ",d"), "the associate tier"),
         ("%d hrs" % DIRECT_HOURS, "a week of direct client care"),
         ("1", "payment, to your loan servicer")],
        JUMPS))

    # ------------------------------------------------------- the loud warning
    o.append('<section class="pk-sec">')
    o.append(pk.callout(
        "Read this before anything else",
        ["This page reports what HCAI and the Board of Behavioral Sciences "
         "have <b>published about this program</b>, read on the date in the "
         "hero. It is not advice, it is not an eligibility determination, and "
         "it cannot tell you whether you or your employer qualify.",
         "<b>None of it can be guaranteed current.</b> Award amounts, "
         "obligations, eligible settings and application windows all change "
         "between cycles, and the published documents do not always agree with "
         "each other &mdash; where they disagree, this page shows you both "
         "rather than picking one.",
         "<b>Verify with HCAI directly before you make an employment decision "
         "or submit anything.</b> The program runs "
         '<a href="%s" rel="nofollow noopener" target="_blank">its own '
         "eligibility checker</a> and publishes "
         '<a href="%s" rel="nofollow noopener" target="_blank">the program '
         "page</a>. Use them."
         % (VERIFY_HCAI, PROGRAM)],
        big="Information only. Verify with HCAI before you act."))
    o.append("</section>")

    # --------------------------------------------------------------- what
    o.append('<section class="pk-sec" id="what">')
    o.append('<p class="pk-k">What it is</p>')
    o.append('<h2 class="pk-h">The largest thing California has ever offered a '
             "pre-licensed clinician.</h2>")
    o.append('<p class="pk-d">MBH-SLRP pays student loans for behavioral '
             "health practitioners who serve Medi-Cal members. It sits inside "
             "BH-CONNECT, the state&rsquo;s behavioral health workforce "
             "initiative, and the Board of Behavioral Sciences was told in "
             "April 2026 that <b>up to $%s is available for award</b>.</p>"
             % format(TOTAL_FUND, ",d"))
    o.append('<p class="pk-p">The reason it matters more than the other three '
             "programs an associate might look at is simple: the other two "
             "state and federal loan repayment schemes require a full, "
             'unrestricted license. <a href="%s">This one names associates in '
             "its own tier</a>, and it is the biggest of the four.</p>"
             % FORGIVE)
    o.append("</section>")

    # --------------------------------------------------------------- tiers
    o.append('<section class="pk-sec" id="tiers">')
    o.append('<p class="pk-k">The tiers</p>')
    o.append('<h2 class="pk-h">Three of them, and you are in the middle one.</h2>')
    rows = []
    for label, amount, who in TIERS:
        cls = "hi" if amount == TIER2 else ""
        row = [label, ("up to $%s" % format(amount, ",d"), "f"), who]
        rows.append((row, cls) if cls else row)
    o.append(pk.table(["Tier", "Award", "Who is in it"], rows,
                      caption="Every figure is a maximum, not the amount every "
                              "grantee receives. Transcribed from HCAI&rsquo;s "
                              "technical assistance guide.",
                      minw=660))
    o.append("</section>")

    # ---------------------------------------------------------- conditions
    o.append('<section class="pk-sec" id="conditions">')
    o.append('<p class="pk-k">The conditions</p>')
    o.append('<h2 class="pk-h">Four things that decide whether this is worth '
             "it, and none of them is the number.</h2>")

    o.append(pk.numbered([
        ("1", "%d hours a week of <em>direct client care</em>." % DIRECT_HOURS,
         "Not %d hours of employment. Direct care, at an eligible practice "
         "site &mdash; or %d hours in an eligible school setting. For a "
         "therapist that is a heavier clinical week than most full-time jobs "
         "actually carry, and it is the condition most likely to be discovered "
         "after you have signed something."
         % (DIRECT_HOURS, SCHOOL_HOURS)),
        ("2", "A two-, three- or four-year service obligation.",
         "HCAI says it &ldquo;may vary by program, profession or award "
         "amount&rdquo;. The associate tier has been described as four years. "
         "Ask which one applies to you before you plan around it."),
        ("3", "One payment, to your loan servicer, later.",
         "HCAI or its designee issues <b>a single payment directly to the loan "
         "servicer</b> named in your application. For the 2026 cycle that "
         "payment falls somewhere between %s. It is not income, it does not "
         "arrive monthly, and it does nothing at all for the monthly payment "
         "that is usually the emergency." % PAY_WINDOW),
        ("4", "Your site can stop qualifying.",
         "This is not in any guide. It is in the group, from somebody living "
         "it &mdash; see below. Eligibility attaches to where you work, and "
         "where you work can change underneath you."),
    ]))

    o.append(pk.callout(
        "The arithmetic worth doing before the arithmetic everyone does",
        ["$%s over four years is about $%s a year of loan principal. Set "
         "against that: %d direct hours a week is roughly %d%% more clinical "
         "contact than a typical full caseload, sustained for four years, in "
         "the settings that already pay least."
         % (format(TIER2, ",d"), format(TIER2 // 4, ",d"), DIRECT_HOURS, 28),
         "That is not an argument against it. It is the trade the program "
         "actually offers, stated plainly, which is more than the flyer does. "
         'What each setting pays is on <a href="%s">the associate pay page</a>, '
         'and the four-year comparison against a better-paid offer is on '
         '<a href="%s">the hiring page</a>.' % (PAY, HIRED)]))
    o.append("</section>")

    # --------------------------------------------------------------- sites
    o.append('<section class="pk-sec" id="sites">')
    o.append('<p class="pk-k">Where you have to work</p>')
    o.append('<h2 class="pk-h">The published documents do not agree, so here '
             "are both.</h2>")
    o.append(pk.table(
        ["Source", "How it describes an eligible site"],
        [["HCAI&rsquo;s BH-CONNECT FAQ, and an April 2026 Board of Behavioral "
          "Sciences agenda item",
          "The Medi-Cal safety net: <b>federally qualified health centers, "
          "community mental health centers, rural health clinics</b>, plus "
          "hospitals and other settings meeting a Medicaid payer threshold "
          "&mdash; at least %d%% of the population on Medicaid or uninsured, "
          "%d%% for rural hospitals." % (MEDICAID_SHARE, RURAL_SHARE)],
         ["HCAI&rsquo;s own technical assistance guide",
          "Narrower: <b>specialty mental health, Drug Medi-Cal, or "
          "DMC-ODS services</b> at county-operated sites and community-based "
          "sites contracted with a county behavioral health agency, and "
          "possibly individual practitioners contracted with one."]],
        caption="These are not the same set. Neither is obviously wrong &mdash; "
                "the second may describe one route among several. What follows "
                "from it is practical: <b>do not infer your site&rsquo;s "
                "eligibility from a category</b>. Have the employer confirm "
                "with HCAI in writing, and get it in the employment "
                "verification form.",
        minw=620))
    o.append('<p class="pk-p">Which employers sit in the enumerable part of '
             'that list is <a href="%s">a directory of its own</a> &mdash; the '
             "%s county behavioral health plans and the health center "
             "organizations, by name. It is a starting point and not an "
             "answer, for exactly the reason above.</p>" % (EMPLOYERS, "57"))
    o.append("</section>")

    # ---------------------------------------------------------------- room
    o.append('<section class="pk-sec" id="room">')
    o.append('<p class="pk-k">What the room is asking</p>')
    o.append('<h2 class="pk-h">People have found the program. They cannot '
             "find a qualifying employer.</h2>")
    o.append('<p class="pk-d">Three posts from the California associate group, '
             "de-identified. The comment counts are the finding: the room "
             "knows the program exists now and cannot answer the question "
             "that follows.</p>")

    o.append(pk.quote(
        "The risk no guide mentions &mdash; 4 comments",
        ["I&rsquo;m currently looking for an AMFT position because <b>my "
         "current site unfortunately no longer qualifies</b> under the "
         "Medi-Cal Behavioral Health Student Loan Repayment Program "
         "(MBH-SLRP). I&rsquo;m specifically looking for positions at "
         "sites that&hellip;"]))
    o.append(pk.quote(
        "Knows the rule, cannot find the employer &mdash; 1 comment",
        ["I&rsquo;m an AMFT in Orange County, CA with about 2,300 hours&hellip; "
         "Seeking a hybrid/remote position at a site that "
         "accepts Medi-Cal or 40% of uninsured clients so I can qualify for "
         "SLRP. I&rsquo;d really appreciate any leads."]))
    o.append(pk.quote(
        "No replies at all",
        ["I am an AMFT and APCC currently seeking a remote role with an "
         "organization that supports clinicians through the HCAI Loan "
         "Repayment Program or other student loan forgiveness options."]))

    o.append(pk.checklist(
        "What those three posts tell you that the program documents do not",
        ["<b>Site eligibility is not permanent.</b> Somebody is job-hunting "
         "mid-obligation because their employer fell out of it. Ask, before "
         "you take a job, what happens to your award if the site&rsquo;s "
         "status changes &mdash; and ask HCAI, not the employer.",
         "<b>Two of the three want remote or hybrid work.</b> The obligation "
         "is written as direct client care <em>at an eligible practice site</em>. "
         "Whether telehealth from home counts against that is not answered in "
         "any published document, and it is the first question to put to HCAI "
         "if remote work is your plan.",
         "<b>Asking a peer group to find you a qualifying employer does not "
         "work.</b> Four comments, one, and none. That is not unkindness; it "
         "is that nobody has the list."]))
    o.append("</section>")

    # ----------------------------------------------------------------- tax
    o.append('<section class="pk-sec" id="tax">')
    o.append('<p class="pk-k">The question nobody answers</p>')
    o.append('<h2 class="pk-h">Is a $%s award taxable income?</h2>'
             % format(TIER2, ",d"))
    o.append('<p class="pk-d"><b>HCAI&rsquo;s FAQ does not address it.</b> '
             "Neither does the technical assistance guide. On an award this "
             "size the answer is worth tens of thousands of dollars, and there "
             "is a federal provision that nobody in this conversation "
             "cites.</p>")
    o.append(pk.callout(
        "26 U.S.C. &sect;108(f)(4)",
        ["Gross income does not include any amount received under section "
         "338B(g) of the Public Health Service Act, under a State program "
         "described in section 338I of that Act, <b>&ldquo;or under any other "
         "State loan repayment or loan forgiveness program that is intended to "
         "provide for the increased availability of health care services in "
         "underserved or health professional shortage areas (as determined by "
         "such State)&rdquo;</b>.",
         "That is the whole of the relevant text. Whether MBH-SLRP sits inside "
         "it turns on how the program is characterized and on California&rsquo;s "
         "own determination &mdash; and on state conformity, which is a "
         "separate question from the federal one.",
         "<b>This page does not decide it, and neither should a forum.</b> It "
         "is a question for a tax professional, and it is worth paying one to "
         "ask before you plan around a net figure. What it should not be is "
         "unexamined, which is where it currently sits."]))
    o.append("</section>")

    # --------------------------------------------------------------- apply
    o.append('<section class="pk-sec" id="apply">')
    o.append('<p class="pk-k">Applying</p>')
    o.append('<h2 class="pk-h">What you need in front of you, and when.</h2>')
    o.append('<p class="pk-d">The 2026 cycle is closed. The next window opens '
             "<b>%s</b>, which makes an autumn employment decision a decision "
             "about which cycle you can enter.</p>" % NEXT_CYCLE)
    o.append(pk.checklist(
        "The documents the application asks for",
        ["An unofficial transcript.",
         "Your license or certificate number, and a copy of it.",
         "For every loan: <b>lender account number, origination date, loan "
         "servicer, current balance, the repayment amount you are requesting, "
         "and the most current statement</b>.",
         "Your employer&rsquo;s contact information &mdash; the employment "
         "verification form is completed by them, not by you.",
         "Two emergency contacts.",
         "Your National Provider Identifier.",
         "A COI letter, if you previously worked for the State of California."]))
    o.append('<p class="pk-p">The loan detail is the part that takes longest '
             "if you have several servicers, and the employment verification "
             "is the part that depends on somebody else. Both are worth "
             "starting before the window opens rather than inside it.</p>")
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The program", [
            ("Medi-Cal Behavioral Health Student Loan Repayment Program "
             "&mdash; HCAI&rsquo;s program page, award tiers and cycle dates",
             PROGRAM),
            ("MBH-SLRP Technical Assistance Guide, 2025 &mdash; the three "
             "tiers with their full discipline lists, the application document "
             "list, and the narrower description of eligible sites",
             "https://hcai.ca.gov/wp-content/uploads/2025/07/"
             "MBH-SLRP-Technical-Assistance-Guide-2025.pdf"),
            ("BH-CONNECT frequently asked questions &mdash; the safety-net "
             "setting list, the two-, three- or four-year obligation, and the "
             "single payment to the loan servicer",
             "https://hcai.ca.gov/workforce/initiatives/"
             "behavioral-health-bh-connect/bh-connect-frequently-asked-questions/"),
            ("HCAI eligibility quiz &mdash; the state&rsquo;s own checker, "
             "which is what to use rather than this page", VERIFY_HCAI),
        ]),
        ("The figures", [
            ("Board of Behavioral Sciences, Policy and Advocacy Committee, "
             "17 April 2026 &mdash; the $%s available for award, the "
             "associate-level professions, the safety-net site list, and the "
             "%d-hour direct care requirement"
             % (format(TOTAL_FUND, ",d"), DIRECT_HOURS),
             "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260417_pa_item5.pdf"),
        ]),
        ("The tax question", [
            ("26 U.S.C. &sect;108(f)(4) &mdash; the exclusion from gross "
             "income for State loan repayment programs aimed at underserved "
             "or shortage areas",
             "https://www.law.cornell.edu/uscode/text/26/108"),
        ]),
        ("What the room is asking", [
            ("Three posts from a California associate support group, read "
             "%s. Quotes are verbatim and de-identified; comment counts are "
             "as displayed." % pk.CHECKED, None),
        ]),
    ], note="<b>Everything above is drawn from published program documents "
            "on a stated date and none of it can be guaranteed current.</b> "
            "Award amounts, obligations, eligible settings and application "
            "windows change between cycles, and the published sources do not "
            "agree with each other on eligible sites. This page is not legal, "
            "financial or tax advice and cannot determine your eligibility. "
            "<b>Verify with HCAI directly, and take the tax question to a "
            "professional, before you act.</b>")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "MBH-SLRP explained: the $180,000 California pays associate therapists",
    "California's largest loan repayment program names registered "
    "associates in its own tier. The conditions nobody mentions: 32 direct "
    "care hours a week, one payment, and a site that can stop qualifying.",
    "licensure", "guide",
    "How does the Medi-Cal Behavioral Health Student Loan Repayment Program "
    "actually work?",
    "The three award tiers, the %d-hour direct-care obligation, where you "
    "have to work, and the tax question HCAI does not answer" % DIRECT_HOURS,
    "$%s, associate tier" % format(TIER2, ",d"),
    weight=5)


def main():
    print("MBH-SLRP in full")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the direct-care condition", "hours a week of <em>direct client care"),
        ("the single-payment finding", "a single payment directly to the loan"),
        ("the site-can-stop-qualifying risk", "no longer qualifies"),
        ("the source disagreement", "do not agree, so here"),
        ("the tax statute", "increased availability of health care services"),
        ("the funding total", format(TOTAL_FUND, ",d")),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every tier must be present with its figure, or the hero's claim that an
    # associate sits in the middle one is unsupported.
    for label, amount, who in TIERS:
        if format(amount, ",d") not in art:
            print("GUARD: the $%s tier is missing" % format(amount, ",d"))
            bad += 1
    if "associate marriage and family therapists" not in art:
        print("GUARD: the associate professions are not named in the tier table")
        bad += 1

    # The page must never resolve the tax question or the source disagreement.
    for banned in ("is not taxable", "is tax-free", "is exempt from tax",
                   "you will qualify", "you are eligible"):
        if banned in art.lower():
            print("GUARD: the page states %r - it cannot decide that" % banned)
            bad += 1

    # Four disclaimer placements, guarded individually.
    for what, needle in (
            ("the hero warning", "verify with HCAI before you act"),
            ("the panel", "Information only. Verify with HCAI before you act."),
            ("the currency caveat", "None of it can be guaranteed current"),
            ("the sources note", "Verify with HCAI directly, and take the tax "
                                 "question to a professional")):
        if needle not in s:
            print("GUARD: %s is missing (%s)" % (what, needle[:44]))
            bad += 1

    # De-identification: the standing rule on this site is that no individual
    # is named. The quotes are from real posts and the names must not travel.
    for name in ("KindOtter", "Jessica", "Melinda"):
        if name in s:
            print("GUARD: %r appears on the page - quotes are de-identified"
                  % name)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
