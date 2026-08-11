#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Which employers unlock loan forgiveness for a California therapist.

THE QUESTION THIS ANSWERS

It came out of the hiring page. A person in the associate group was weighing
bankruptcy over student loans, in a thread with 114 comments, and nobody
mentioned that California pays associate-level practitioners up to $180,000
against those loans. The obvious follow-up is: so which employers?

THE STRUCTURE NOBODY PUBLISHES, AND THE REASON IT MATTERS

Four programs are in play and they qualify you on three completely different
axes. Everybody conflates them:

    PSLF        asks WHO YOUR EMPLOYER IS   - government or 501(c)(3)
    MBH-SLRP    asks WHO YOU SERVE          - a Medi-Cal safety-net setting
    NHSC LRP    asks WHERE THE SITE IS      - approved site in a mental
    CA SLRP                                   health shortage area

The same job can qualify under one and not the others, and the two findings
that fall out of that are the page:

  1. PSLF asks nothing about your license. An associate working for a county
     behavioral health agency is very likely accruing qualifying payments
     right now, and on income-driven repayment at associate pay those payments
     are small - which makes the forgiveness large relative to what is paid.

  2. An associate at a FOR-PROFIT group practice serving Medi-Cal clients
     qualifies for none of them, because PSLF is about employer type and not
     about who you serve. That is the opposite of what people assume.

And the negative finding, which is worth as much as the positive one: NHSC and
CA SLRP both require full licensure in terms. Only PSLF and MBH-SLRP reach an
associate.

WHY THE DISCLAIMER IS LOUD AND REPEATED

Because getting this wrong is expensive in a way most pages on this site are
not. Somebody who believes an employer qualifies for PSLF and is wrong can lose
years of payments before finding out. So: the page reports what the published
sources say on a stated date, links the official verification tool for every
program, and never concludes that a particular employer or job qualifies. The
warning is in the hero, in a panel before any content, inside the checker, and
in the sources note - four times, deliberately.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import hrsa_stats as hs

SITE = pk.SITE
PAGE = "loan-forgiveness-employers-california.html"
DONOR = "getting-hired-as-a-california-associate.html"

HIRED = "getting-hired-as-a-california-associate.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"
ATLAS = "therapists-by-county-california.html"
HOURS = "amft-3000-hours-california.html"

PSLF_PAYMENTS = 120
PSLF_HOURS = 30
PSLF_RULE_DATE = "1 July 2026"

MBH_ASSOCIATE = 180000
MBH_PRESCRIBER = 240000
MBH_UNLICENSED = 120000
MBH_YEARS = 4
MBH_NEXT = "1 May 2027"
MEDICAID_SHARE = 40
RURAL_SHARE = 30

NHSC_FULL = 50000
NHSC_HALF = 30000
NHSC_YEARS = 2

SLRP_FULL = 50000
SLRP_HALF = 25000
SLRP_EXT_1 = 20000
SLRP_EXT_3 = 10000

LMH_AWARD = 15000
LMH_MONTHS = 24
LMH_TIMES = 3

JUMPS = [("axes", "Three questions"),
         ("pslf", "PSLF"),
         ("state", "The state programs"),
         ("where", "Where the shortage areas are"),
         ("counties", "By county"),
         ("check", "Check a job"),
         ("sources", "Sources")]

VERIFY_PSLF = "https://studentaid.gov/pslf/"
VERIFY_HPSA = "https://data.hrsa.gov/tools/shortage-area/hpsa-find"
VERIFY_HCAI = "https://hcai.ca.gov/loans-scholarships-grants/eligibility/"
VERIFY_NHSC = "https://nhsc.hrsa.gov/loan-repayment/nhsc-loan-repayment-program"


def top_counties(n=58):
    """All 58, ordered by designated mental-health shortage areas.

    Zeroes are printed rather than dropped. A county missing from a table is
    read as an oversight; a county showing zero is information.
    """
    out = []
    for c in hs.CA_COUNTIES:
        out.append((c, hs.CA_MH_HPSA_BY_COUNTY.get(c, 0),
                    hs.CA_HEALTH_CENTER_BY_COUNTY.get(c, 0)))
    out.sort(key=lambda r: (-r[1], -r[2], r[0]))
    return out[:n]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Loan forgiveness &middot; who qualifies you &middot; federal and "
        "state data read %s" % hs.CHECKED,
        "Four programs. Three different questions. One of them ignores your "
        "license entirely.",
        "Which employer you take decides which of these you can ever claim "
        "&mdash; and two of the four reach an associate. <b>Everything here is "
        "information, not an eligibility decision: verify with the program "
        "itself before you act on any of it.</b>",
        [("2 of 4", "programs an associate can reach"),
         ("$%s" % format(MBH_ASSOCIATE, ",d"), "the largest, and it names associates"),
         (format(hs.CA_MH_HPSA_DESIGNATED, ",d"), "designated mental health shortage areas"),
         ("57 of 58", "counties with at least one")],
        JUMPS))

    # ------------------------------------------------------- the loud warning
    o.append('<section class="pk-sec">')
    o.append(pk.callout(
        "Read this before anything else on the page",
        ["This page reports what four public programs have <b>published about "
         "themselves</b>, read on the date in the hero. It is not advice, it "
         "is not an eligibility determination, and it cannot tell you whether "
         "a particular employer or job qualifies. Only the program can do "
         "that.",
         "<b>None of it can be guaranteed current.</b> Program rules change, "
         "award amounts change, application cycles open and close, and "
         "shortage-area designations are added and withdrawn continuously "
         "&mdash; of the %s California mental health designations on file "
         "right now, %s are already withdrawn or proposed for withdrawal. A "
         "figure that was right the day it was read can be wrong the day you "
         "read it."
         % (format(hs.CA_MH_HPSA_TOTAL_ROWS, ",d"),
            format(hs.CA_MH_HPSA_BY_STATUS.get("Withdrawn", 0)
                   + hs.CA_MH_HPSA_BY_STATUS.get("Proposed For Withdrawal", 0),
                   ",d")),
         "<b>Verify directly with the government before you make an "
         "employment decision, sign anything, or change a repayment plan.</b> "
         'Every program below links to its own official checker: '
         '<a href="%s" rel="nofollow noopener" target="_blank">the federal '
         "PSLF employer search</a>, "
         '<a href="%s" rel="nofollow noopener" target="_blank">HRSA&rsquo;s '
         "shortage-area finder</a>, and "
         '<a href="%s" rel="nofollow noopener" target="_blank">HCAI&rsquo;s '
         "eligibility quiz</a>. Use them. Getting this wrong can cost years of "
         "qualifying payments, and no page can carry that risk for you."
         % (VERIFY_PSLF, VERIFY_HPSA, VERIFY_HCAI)],
        big="Information only. Verify with the program before you act."))
    o.append("</section>")

    # --------------------------------------------------------------- the axes
    o.append('<section class="pk-sec" id="axes">')
    o.append('<p class="pk-k">The comparison</p>')
    o.append('<h2 class="pk-h">They are not four versions of the same test.</h2>')
    o.append('<p class="pk-d">Each program asks a different question, which is '
             "why the same job can qualify under one and be ruled out by "
             "another. The column people never see is the third one.</p>")

    o.append(pk.table(
        ["Program", "What it asks", "Reaches an associate?", "What it pays"],
        [(["<b>PSLF</b> &mdash; federal",
           "Who is your <b>employer</b>? Government at any level, or a "
           "501(c)(3).",
           ("Yes", "m"),
           "Whatever is left after %d qualifying payments"
           % PSLF_PAYMENTS], "hi"),
         (["<b>MBH-SLRP</b> &mdash; California",
           "Who do you <b>serve</b>? A Medi-Cal safety-net setting.",
           ("Yes, a named tier", "m"),
           "Up to $%s over %d years" % (format(MBH_ASSOCIATE, ",d"), MBH_YEARS)],
          "hi"),
         ["<b>NHSC LRP</b> &mdash; federal",
          "Where is the <b>site</b>? NHSC-approved, in a mental health "
          "shortage area.",
          ("No &mdash; full license", "m"),
          "Up to $%s over %d years, full time"
          % (format(NHSC_FULL, ",d"), NHSC_YEARS)],
         ["<b>CA SLRP</b> &mdash; California",
          "Where is the <b>site</b>? In a designated shortage area, "
          "non-profit, sliding fee, and willing to match the award.",
          ("No &mdash; full license", "m"),
          "$%s over %d years, full time, then extensions"
          % (format(SLRP_FULL, ",d"), NHSC_YEARS)]],
        caption="A fifth, the Licensed Mental Health Services Provider "
                "Education Program, pays up to $%s for a %d-month commitment "
                "and can be awarded %d times in a career. Its program page "
                "does not state whether pre-licensed registrants qualify, so "
                "this page does not say either way."
                % (format(LMH_AWARD, ",d"), LMH_MONTHS, LMH_TIMES),
        minw=720))

    o.append(pk.numbered([
        ("1", "The two that reach an associate are the two biggest.",
         "PSLF has no cap at all &mdash; it forgives the remaining balance "
         "&mdash; and MBH-SLRP is the largest fixed award of the four. The "
         "programs that rule you out are the smaller ones."),
        ("2", "The two that rule you out say so in terms.",
         "NHSC requires you to be &ldquo;fully trained and licensed to "
         "practice&rdquo; in the discipline and state. California&rsquo;s "
         "SLRP requires you to &ldquo;possess a valid and unrestricted "
         "license&rdquo;. Neither has an associate tier, and no amount of "
         "supervised experience substitutes."),
        ("3", "Which means the question to ask an employer changes with your "
         "status.",
         "Pre-licensed, you are asking whether they are a government body or "
         "a 501(c)(3), and whether they are a Medi-Cal safety-net setting. "
         "Licensed, the site&rsquo;s shortage-area designation opens up as "
         "well &mdash; and for CA SLRP, whether the site will put up matching "
         "funds, which is the condition that quietly disqualifies most of "
         "them."),
    ]))
    o.append("</section>")

    # ---------------------------------------------------------------- PSLF
    o.append('<section class="pk-sec" id="pslf">')
    o.append('<p class="pk-k">PSLF</p>')
    o.append('<h2 class="pk-h">The federal one does not care what your license '
             "says.</h2>")
    o.append('<p class="pk-d">The regulation defines a qualifying employer by '
             "what the organization is, not by what you do inside it. There "
             "is no discipline list, no license requirement and no job title "
             "in the definition.</p>")

    o.append(pk.table(
        ["The test", "What the regulation requires"],
        [["Qualifying employer",
          "A United States-based <b>federal, state, local or tribal</b> "
          "government organization, agency or entity, including the Armed "
          "Forces and National Guard; a public child or family service "
          "agency; or an organization exempt under <b>section 501(c)(3)</b>. "
          "Business entities, labor unions and partisan political "
          "organizations are excluded."],
         ["Full time",
          "A minimum average of <b>%d hours a week</b> across one or more "
          "qualifying jobs during the certified period." % PSLF_HOURS],
         ["Payments",
          "<b>%d</b> monthly payments made after 1 October 2007. They do not "
          "have to be consecutive." % PSLF_PAYMENTS],
         ["Loans and plans",
          "Direct Subsidized, Unsubsidized, PLUS and Consolidation loans, on "
          "an income-driven plan, the 10-year standard plan, or a plan whose "
          "payment meets or exceeds the 10-year standard amount."],
         ["Since %s" % PSLF_RULE_DATE,
          "A final rule adds an <b>excluded employer</b> category for "
          "organizations the Secretary determines engage in activities with a "
          "substantial illegal purpose. The Department&rsquo;s own analysis "
          "projects fewer than ten employers affected a year, but payments "
          "made after a disqualification do not count."]],
        caption="34 CFR &sect;685.219. Read the definition of qualifying "
                "employer twice: nothing in it is about you.",
        minw=640))

    o.append(pk.callout(
        "Two consequences almost nobody draws",
        ["<b>An associate at a county behavioral health agency is very likely "
         "accruing qualifying payments right now.</b> The county is a local "
         "government entity, which is the whole test. And on income-driven "
         "repayment at associate pay the monthly payment is small &mdash; so "
         "the balance forgiven at the end is large relative to what was "
         "actually paid. Nobody tells you this at induction.",
         "<b>An associate at a for-profit group practice serving Medi-Cal "
         "clients qualifies for none of the four.</b> Serving the right "
         "population does not help: PSLF asks about the employer, and a "
         "for-profit practice is a business entity. This is the opposite of "
         "what most people assume, and it is the single most expensive "
         "assumption on this page."]))
    o.append('<p class="pk-p">If you think this may already apply to you, the '
             "thing to do is not to read more about it &mdash; it is to run "
             'your employer through <a href="%s" rel="nofollow noopener" '
             'target="_blank">the federal employer search</a> and file the '
             "employer certification. Certifying early is how you find out "
             "you were wrong while it is still cheap.</p>" % VERIFY_PSLF)
    o.append("</section>")

    # ------------------------------------------------------- state programs
    o.append('<section class="pk-sec" id="state">')
    o.append('<p class="pk-k">The California programs</p>')
    o.append('<h2 class="pk-h">One names associates. The other requires a '
             "license and a willing employer.</h2>")

    o.append('<h3 class="pk-h3">Medi-Cal Behavioral Health Student Loan '
             "Repayment &mdash; the one that reaches you</h3>")
    o.append(pk.table(
        ["Tier", "Award", "Service"],
        [["Licensed, prescribing", ("$%s" % format(MBH_PRESCRIBER, ",d"), "f"),
          "%d years" % MBH_YEARS],
         (["<b>Non-prescribing licensed, or associate-level pre-licensure</b>",
           ("$%s" % format(MBH_ASSOCIATE, ",d"), "f"),
           "%d years" % MBH_YEARS], "hi"),
         ["Non-licensed, non-prescribing", ("$%s" % format(MBH_UNLICENSED, ",d"), "f"),
          "Two to four years, by award size"]],
        caption="Awards are stated as maximums. The service obligation must "
                "be completed in a Medi-Cal safety-net setting: a federally "
                "qualified health center, community mental health center, "
                "rural health clinic, or a setting where at least %d%% of the "
                "population is on Medicaid or uninsured &mdash; %d%% for "
                "rural hospitals. The next application window opens <b>%s</b>."
                % (MEDICAID_SHARE, RURAL_SHARE, MBH_NEXT),
        minw=560))

    o.append('<h3 class="pk-h3">California SLRP &mdash; licensed only, and the '
             "match is the catch</h3>")
    o.append('<p class="pk-p">$%s for a two-year full-time obligation, $%s '
             "half-time, then extensions of $%s a year and later $%s. "
             "Eligible disciplines include LMFT, LCSW, LPCC and health "
             "service psychologist. The applicant must <b>&ldquo;possess a "
             "valid and unrestricted license&rdquo;</b>, so an associate "
             "cannot apply.</p>"
             % (format(SLRP_FULL, ",d"), format(SLRP_HALF, ",d"),
                format(SLRP_EXT_1, ",d"), format(SLRP_EXT_3, ",d")))
    o.append('<p class="pk-p">The site condition is the one that decides most '
             "cases. It must sit in a federally designated shortage area, be "
             "a public or private not-for-profit outpatient facility open to "
             "the general public, offer a sliding fee schedule, and "
             "<b>match the award dollar for dollar</b>. That last requirement "
             "is why a designated shortage area near you is not the same "
             "thing as a participating employer near you, and why this is a "
             "question to ask the employer rather than to infer from a "
             "map.</p>")
    o.append("</section>")

    # --------------------------------------------------------------- where
    o.append('<section class="pk-sec" id="where">')
    o.append('<p class="pk-k">The shortage-area layer</p>')
    o.append('<h2 class="pk-h">%s live designations, and five times that many '
             "dead ones.</h2>" % format(hs.CA_MH_HPSA_DESIGNATED, ",d"))
    o.append('<p class="pk-d">HRSA publishes every mental health shortage-area '
             "designation it has ever recorded. Most of California&rsquo;s "
             "are no longer in force, and reading the file without filtering "
             "on status overstates the state by about six times.</p>")

    st = hs.CA_MH_HPSA_BY_STATUS
    o.append(pk.table(
        ["Status", "California mental health designations"],
        [(["<b>Designated</b> &mdash; in force",
           (format(st.get("Designated", 0), ",d"), "f")], "hi"),
         ["Proposed for withdrawal",
          (format(st.get("Proposed For Withdrawal", 0), ",d"), "f")],
         ["Withdrawn", (format(st.get("Withdrawn", 0), ",d"), "f")]],
        caption="Which is also why nothing on this page can be treated as "
                "current without checking: the withdrawal column moves.",
        minw=480))

    types = sorted(hs.CA_MH_HPSA_BY_TYPE.items(), key=lambda x: -x[1])
    o.append('<h3 class="pk-h3">What kind of designation they are</h3>')
    o.append(pk.table(
        ["Designation type", "Count"],
        [[k, (format(v, ",d"), "f")] for k, v in types],
        caption="A facility-type designation &mdash; health center, rural "
                "health clinic, tribal health &mdash; attaches to a named "
                "site. A population or geographic designation attaches to an "
                "area, and a job inside that area is not automatically at an "
                "approved site.",
        minw=520))

    o.append('<p class="pk-p">The shortage <b>score</b> runs from %g to %g '
             "across California&rsquo;s live designations, averaging %.1f. It "
             "matters because NHSC funds applications from the highest scores "
             "down, so two approved sites are not equally likely to get you "
             "an award.</p>"
             % (hs.HPSA_SCORE_MIN, hs.HPSA_SCORE_MAX, hs.HPSA_SCORE_MEAN))
    o.append("</section>")

    # ------------------------------------------------------------- counties
    o.append('<section class="pk-sec" id="counties">')
    o.append('<p class="pk-k">By county</p>')
    o.append('<h2 class="pk-h">Every county but one has a designated shortage '
             "area.</h2>")
    o.append('<p class="pk-d">The only California county with no designated '
             "mental health shortage area is <b>%s</b> &mdash; also the "
             "state&rsquo;s least populous. Health center sites are counted "
             "separately because they are named facilities rather than areas, "
             "and they are the clearest overlap between the federal and state "
             "programs.</p>" % (hs.COUNTIES_WITH_NONE[0]
                                if hs.COUNTIES_WITH_NONE else "none"))

    rows = []
    for county, hpsa, hc in top_counties():
        rows.append([county, (format(hpsa, ",d"), "f"), (format(hc, ",d"), "f")])
    o.append(pk.table(
        ["County", "Designated mental health shortage areas",
         "Active health center sites"],
        rows,
        caption="Designations from HRSA&rsquo;s mental health shortage-area "
                "file, health centers from its service delivery and "
                "look-alike site file, both read %s. A count in this table "
                "says a county contains designated areas or health center "
                "sites. It does <b>not</b> say any of them is hiring, is "
                "NHSC-approved, or would qualify you for anything."
                % hs.CHECKED,
        minw=560))
    o.append('<p class="pk-p">How crowded each county already is with '
             'therapists is a different question, answered on <a href="%s">the '
             "county atlas</a>.</p>" % ATLAS)
    o.append("</section>")

    # -------------------------------------------------------------- checker
    o.append('<section class="pk-sec" id="check">')
    o.append('<p class="pk-k">The checker</p>')
    o.append('<h2 class="pk-h">Which of the four a job could reach.</h2>')
    o.append('<p class="pk-d">Describe the job. This reads the published rules '
             "and tells you which programs are <b>worth verifying</b> and "
             "which are ruled out on their face. It runs in your browser, "
             "nothing is stored and nothing is sent anywhere &mdash; and it "
             "is not an eligibility decision.</p>")
    o.append(CALC_HTML)
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The federal program, in the regulation", [
            ("34 CFR &sect;685.219 &mdash; Public Service Loan Forgiveness: "
             "the definitions of qualifying employer, full-time employment "
             "and qualifying payment",
             "https://www.ecfr.gov/current/title-34/subtitle-B/chapter-VI/"
             "part-685/subpart-B/section-685.219"),
            ("Federal Student Aid &mdash; PSLF, and the employer search tool "
             "to verify with",
             VERIFY_PSLF),
            ("The final rule adding an excluded-employer category, effective "
             "%s" % PSLF_RULE_DATE,
             "https://www.acenet.edu/News-Room/Pages/ED-Finalizes-PSLF-Rule.aspx"),
        ]),
        ("The other three programs", [
            ("Medi-Cal Behavioral Health Student Loan Repayment Program "
             "&mdash; the award tiers, including the associate-level tier",
             "https://hcai.ca.gov/workforce/initiatives/"
             "behavioral-health-bh-connect/mbhslrp/"),
            ("NHSC Loan Repayment Program &mdash; &ldquo;fully trained and "
             "licensed&rdquo;, and the shortage-area site requirement",
             VERIFY_NHSC),
            ("California State Loan Repayment Program",
             "https://hcai.ca.gov/workforce/financial-assistance/"
             "loan-repayment/slrp/"),
            ("2026 California SLRP grant guide &mdash; the licensure wording, "
             "award amounts and the matching-funds condition",
             "https://hcai.ca.gov/document/2026-slrp-grant-guide/"),
            ("Licensed Mental Health Services Provider Education Program",
             "https://hcai.ca.gov/workforce/financial-assistance/"
             "loan-repayment/lmhspep/"),
            ("HCAI eligibility quiz &mdash; the state&rsquo;s own checker",
             VERIFY_HCAI),
        ]),
        ("The counts on this page", [
            ("HRSA Data Downloads &mdash; the mental health shortage-area "
             "file and the health center service delivery and look-alike site "
             "file, both read %s and reduced to counts by "
             "_dev/hrsa_sites.py" % hs.CHECKED,
             "https://data.hrsa.gov/data/download"),
            ("HRSA shortage-area finder &mdash; check a specific address "
             "rather than a county",
             VERIFY_HPSA),
        ]),
    ], note="<b>Everything above is information drawn from public program "
            "documents on a stated date, and none of it can be guaranteed "
            "current.</b> Program rules, award amounts, application windows "
            "and shortage-area designations all change without notice, and "
            "this page is not connected to any of them. It is not legal, "
            "financial or tax advice, and it cannot determine your "
            "eligibility for anything. <b>Verify with the program directly "
            "before making an employment decision, submitting an "
            "application, or changing a repayment plan.</b>")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


# ---------------------------------------------------------------- the checker
#
# Nothing typed here leaves the page: no URL state, no storage, no analytics
# call, no network. And the output vocabulary is deliberate - "worth verifying"
# and "ruled out on its face", never "eligible". The page cannot determine
# eligibility and must not sound as though it has.
CALC_HTML = """<div class="pk-calc" id="lf-calc">
<div class="pk-cg">
<div class="pk-cc">
<h3>The job</h3>
<label class="pk-fl" for="lf-emp">Who is the employer?</label>
<select id="lf-emp">
<option value="">Choose</option>
<option value="gov">Government &mdash; federal, state, county, city or tribal</option>
<option value="np">A 501(c)(3) non-profit</option>
<option value="fp">A for-profit business</option>
<option value="self">Self-employed or my own practice</option>
</select>
<label class="pk-fl" for="lf-set">What kind of setting is it?</label>
<select id="lf-set">
<option value="">Choose</option>
<option value="safety">Health center, community mental health center, rural health clinic, or mostly Medi-Cal and uninsured</option>
<option value="county">County behavioral health, or an agency contracted to it</option>
<option value="other">Something else</option>
</select>
</div>
<div class="pk-cc">
<h3>And you</h3>
<label class="pk-fl" for="lf-lic">Your status</label>
<select id="lf-lic">
<option value="">Choose</option>
<option value="assoc">Registered associate &mdash; AMFT, ASW or APCC</option>
<option value="lic">Licensed &mdash; LMFT, LCSW, LPCC or psychologist</option>
</select>
<label class="pk-fl" for="lf-ft">Is it full time, 30 hours a week or more?</label>
<select id="lf-ft">
<option value="">Choose</option>
<option value="y">Yes</option>
<option value="n">No</option>
</select>
<label class="pk-fl" for="lf-hpsa">Is the site in a designated shortage area?</label>
<select id="lf-hpsa">
<option value="">Choose</option>
<option value="y">Yes</option>
<option value="n">No</option>
<option value="?">Don't know</option>
</select>
</div>
</div>
<div class="pk-out">
<div class="r hd"><span>Program</span><span>On the published rules</span></div>
<div class="r"><span class="lbl">PSLF &mdash; federal</span><span class="va" id="lf-o-pslf">&mdash;</span></div>
<div class="r"><span class="lbl">MBH-SLRP &mdash; California, up to $180,000</span><span class="va" id="lf-o-mbh">&mdash;</span></div>
<div class="r"><span class="lbl">NHSC Loan Repayment &mdash; federal</span><span class="va" id="lf-o-nhsc">&mdash;</span></div>
<div class="r"><span class="lbl">California SLRP</span><span class="va" id="lf-o-slrp">&mdash;</span></div>
<div class="r tot"><span class="lbl"><b>Worth verifying</b></span><span class="va" id="lf-o-count">&mdash;</span></div>
</div>
<p class="pk-note" id="lf-warn"><b>This is not an eligibility decision.</b>
Describe the job and this will tell you which programs are worth checking and
which are ruled out on their face. Verify every one of them with the program
itself before acting &mdash; nothing here is stored or sent anywhere.</p>
</div>"""

CALC_JS = """<script>
(function(){
  var EM = '\\u2014';
  var YES = 'Worth verifying', NO = 'Ruled out', MAYBE = 'Check the site';
  function el(id){ return document.getElementById(id); }
  function v(id){ var e = el(id); return e ? e.value : ''; }
  function set(id, t){ var e = el(id); if(e) e.textContent = t; }
  function run(){
    var emp = v('lf-emp'), set_ = v('lf-set'), lic = v('lf-lic');
    var ft = v('lf-ft'), hpsa = v('lf-hpsa');
    var warn = el('lf-warn');
    var ids = ['lf-o-pslf','lf-o-mbh','lf-o-nhsc','lf-o-slrp','lf-o-count'];

    if(!emp || !lic){
      ids.forEach(function(id){ set(id, EM); });
      if(warn) warn.innerHTML = '<b>This is not an eligibility decision.</b> ' +
        'Describe the job and this will tell you which programs are worth ' +
        'checking and which are ruled out on their face. Verify every one of ' +
        'them with the program itself before acting \\u2014 nothing here is ' +
        'stored or sent anywhere.';
      return;
    }

    var reasons = [];

    /* PSLF turns on the employer and on full-time hours. It asks nothing
       about the license, which is the point of the page. */
    var pslf;
    if(emp === 'gov' || emp === 'np'){
      pslf = (ft === 'n') ? 'Not full time' : YES;
      if(ft === 'n'){ reasons.push('PSLF needs an average of 30 hours a week'); }
    } else {
      pslf = NO;
      reasons.push(emp === 'self'
        ? 'PSLF does not reach self-employment'
        : 'PSLF excludes for-profit business entities, whoever the clients are');
    }

    /* MBH-SLRP reaches associates by name, and turns on the setting. */
    var mbh;
    if(emp === 'fp' || emp === 'self'){
      mbh = MAYBE;
    } else if(set_ === 'safety' || set_ === 'county'){
      mbh = YES;
    } else if(set_){
      mbh = MAYBE;
    } else {
      mbh = MAYBE;
    }

    /* Both site-based programs require full licensure in terms. */
    var nhsc, slrp;
    if(lic === 'assoc'){
      nhsc = NO; slrp = NO;
      reasons.push('NHSC and California SLRP both require a full, unrestricted license');
    } else {
      nhsc = (hpsa === 'n') ? NO : (hpsa === 'y' ? YES : MAYBE);
      slrp = (hpsa === 'n') ? NO : (hpsa === 'y' ? MAYBE : MAYBE);
      if(hpsa === 'n'){
        reasons.push('both site-based programs need a designated shortage area');
      }
    }

    set('lf-o-pslf', pslf);
    set('lf-o-mbh', mbh);
    set('lf-o-nhsc', nhsc);
    set('lf-o-slrp', slrp);
    var n = [pslf, mbh, nhsc, slrp].filter(function(x){ return x === YES; }).length;
    set('lf-o-count', n + ' of 4');

    var lead;
    if(n === 0){
      lead = '<b>Nothing here is ruled in on the answers given</b>';
    } else {
      lead = '<b>' + n + ' of the four look worth verifying</b>';
    }
    var tail = reasons.length ? ' \\u2014 ' + reasons.join('; ') + '.' : '.';
    if(warn){
      warn.innerHTML = lead + tail + ' <b>This is not an eligibility ' +
        'decision and it is not guaranteed current.</b> &ldquo;Worth ' +
        'verifying&rdquo; means exactly that: take it to the program\\u2019s ' +
        'own checker before you act on it. Nothing here is stored or sent ' +
        'anywhere.';
    }
  }
  ['lf-emp','lf-set','lf-lic','lf-ft','lf-hpsa'].forEach(function(id){
    var e = el(id);
    if(e){ e.addEventListener('change', run); e.addEventListener('input', run); }
  });
  run();
})();
</script>"""


META = pk.meta_block(
    PAGE,
    "Loan forgiveness for California therapists: which employers qualify",
    "Four programs, three different tests. PSLF ignores your license and "
    "asks who employs you. Two of the four reach an associate. Information "
    "only - verify with each program.",
    "licensure", "guide",
    "Which California employers qualify me for student loan forgiveness?",
    "What each of the four programs actually asks, which two reach an "
    "associate, and where California&rsquo;s designated shortage areas are",
    "2 of 4 reach an associate",
    weight=5)


def main():
    print("loan forgiveness employers in California")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=CALC_JS)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources, %d counties"
          % (PAGE, format(len(html), ",d"), nsrc, len(hs.CA_COUNTIES)))

    bad = pk.check_page(p, [
        ("the employer-not-license finding", "nothing in it is about you"),
        ("the for-profit correction", "a for-profit practice is a business"),
        ("the full-licensure bar", "possess a valid and unrestricted"),
        ("the matching-funds catch", "match the award dollar for dollar"),
        ("the checker", 'id="lf-calc"'),
        ("the checker script", "lf-o-pslf"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every county must be in the table. A county silently dropped reads as
    # "no shortage areas here" to somebody deciding where to work.
    for c in hs.CA_COUNTIES:
        if c not in art:
            print("GUARD: %s is missing from the county table" % c)
            bad += 1

    # The verification warning is the point of the page and the thing most
    # likely to be softened by a later editing pass. Four placements, checked.
    warnings = [
        ("the hero warning", "verify with the program itself before"),
        ("the panel before the content", "Information only. Verify with the "
                                         "program before you act."),
        ("the cannot-be-current line", "None of it can be guaranteed "
                                       "current"),
        ("the checker warning", "not an eligibility decision"),
        ("the sources note", "Verify with the program directly before making"),
    ]
    for what, needle in warnings:
        if needle not in s:
            print("GUARD: %s is missing - the disclaimer must appear in all "
                  "four places (%s)" % (what, needle[:40]))
            bad += 1

    # "Eligible" as a verdict is the word this page must never print at the
    # reader. The checker says "Worth verifying" instead, on purpose.
    for banned in (">Eligible<", ">You qualify<", ">Qualifies<"):
        if banned in art:
            print("GUARD: the page states %r as a verdict - it cannot "
                  "determine eligibility" % banned)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
