#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""547 hours and nobody will hire you. The reason is not your hours.

THE QUESTION THIS ANSWERS

The two highest comment counts found anywhere in the Facebook research, from
the California associate group:

    "I am an AMFT / APCC and I'm having a horrible time finding employment.
     Everywhere I apply I hear they are looking for someone with almost totally
     completed hours. I only have 547. How do I get hours if everyone expects
     me to have a..."                                        - 23 / 87

    "After months of applying for jobs without being selected, I have started
     considering filing for bankruptcy because, without a job, I can no longer
     keep up with my loan payments."                          - 26 / 114

And: "My last interview had 60 peop[le]..."

THE CORRECTION THIS PAGE MAKES

Every answer in those threads is about the applicant - your resume, your
interviewing, your hours, network harder. Not one of them names the structural
fact underneath, which is a billing rule:

  * Medi-Cal Specialty Mental Health Services authorises registered associates
    to deliver billable services BY NAME. So do the 90-day-rule candidates who
    have applied but have no number yet, and so do clinical trainees still in
    a degree program.

  * Commercial payers largely do not. A group private practice whose revenue is
    commercial insurance cannot bill for your work at all, which is why its
    only economic use for an associate is private-pay clients it does not have
    enough of.

So it is not one job market with a high bar. It is two markets, and only one of
them is legally able to employ you. Someone applying to both and hearing
nothing from half of them concludes the bar is their hour count. It is not.

THE FACT NOBODY IN THOSE THREADS MENTIONED

California's Medi-Cal Behavioral Health Student Loan Repayment Program pays
non-prescribing licensed AND ASSOCIATE-LEVEL PRE-LICENSURE practitioners up to
$180,000 against student loans, for a four-year service obligation in a
Medi-Cal safety-net setting. The 114-comment thread was written by someone
considering bankruptcy over their loans. Nobody replied with this.

That is not a coincidence - it is what happens when the only people answering
are other associates.

WHAT THIS PAGE DOES NOT DO

It does not tell anyone to take the county job. The four-year arithmetic is on
the page as a calculator precisely because the answer depends on numbers only
the reader has, and because a page that concluded for them would be doing the
thing the threads already do badly.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "getting-hired-as-a-california-associate.html"
DONOR = "associate-unpaid-hours-california.html"

PAY = "associate-therapist-pay-los-angeles-bay-area.html"
ADVISOR = "associate-mft-job-advisor.html"
HOURS = "amft-3000-hours-california.html"
UNPAID = "associate-unpaid-hours-california.html"
OOS = "out-of-state-to-california-licensure.html"
COUNTY = "therapists-by-county-california.html"

# The loan repayment program, from HCAI's own program page.
MBH_ASSOCIATE = 180000
MBH_PRESCRIBER = 240000
MBH_UNLICENSED = 120000
MBH_YEARS = 4
MBH_NEXT = "1 May 2027"
MEDICAID_SHARE = 40
RURAL_SHARE = 30

LMH_AWARD = 15000
LMH_MONTHS = 24
LMH_TIMES = 3

TOTAL_HOURS = 3000
WEEKS = 104

JUMPS = [("why", "Why nobody replies"),
         ("who", "Who can hire you"),
         ("money", "The $180,000"),
         ("compare", "Compare two offers"),
         ("signal", "What the ad means"),
         ("timing", "The calendar"),
         ("sources", "Sources")]


# ------------------------------------------------------------- the staff types
#
# Transcribed from the DHCS State Plan Amendment that lists who may deliver
# billable Specialty Mental Health Services. The pre-licensed rows are the
# point of the table: they are named in the same document as the licensed ones.
SMHS_STAFF = [
    ("Registered associate &mdash; AMFT, ASW, APCC", "Yes, by name",
     "Listed as an authorized staff type in the same State Plan Amendment as "
     "the licensed professions. Your registration is the credential."),
    ("Candidate who has applied but has no number yet", "Yes, with a condition",
     "Named for people who &ldquo;submitted their applications for Associate "
     "registration to BBS within 90 days of their degree award date and are "
     "completing supervised experience toward licensure&rdquo;. The 90-day "
     "rule is not only about whether hours count &mdash; it is also about "
     "whether you are employable at all."),
    ("Clinical trainee, still enrolled", "Yes",
     "An unlicensed individual enrolled in a California degree program "
     "required for licensure, in an approved practicum or internship."),
    ("Registered psychological associate", "Not listed",
     "Absent from the authorized staff types. A real asymmetry, and worth "
     "knowing before assuming the doctoral route is the easier one for "
     "employment."),
]

# Who actually employs pre-licensed clinicians, and why. The `bill` column is
# the whole explanation; `hours` is what it means for how fast you accrue.
SETTINGS = [
    ("County behavioral health, and its contracted agencies",
     "Medi-Cal specialty mental health",
     "Your work is billable from day one, so hiring you is a revenue decision "
     "rather than a favor. This is where volume hiring happens."),
    ("Federally qualified health centers and community mental health centers",
     "Medi-Cal, and the safety-net grant programs",
     "The same billing logic, plus these are the settings that unlock the "
     "loan repayment below."),
    ("Non-profit community agencies",
     "County contracts, grants, sliding scale",
     "Pay is the lowest of any setting and the caseload is the heaviest, "
     "which is the trade that makes the hours arrive fastest."),
    ("Schools and school-based programs",
     "Medi-Cal, county contracts, district budgets",
     "Often overlooked. The academic calendar means hiring windows are "
     "sharp and early."),
    ("Group private practice",
     "Commercial insurance and private pay",
     "Cannot bill your work to most commercial payers, so it can only use "
     "you for private-pay clients. That is why these posts ask for people "
     "who are nearly licensed &mdash; they are hiring for the license, not "
     "for the associate."),
]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Getting hired &middot; the associate job market &middot; checked %s"
        % pk.CHECKED,
        "It is not one job market with a high bar.",
        "It is two markets, and only one of them is legally able to bill for "
        "your work. That, and not your hour count, is why half your "
        "applications never get a reply &mdash; and the market that can hire "
        "you carries <b>up to $180,000</b> of loan repayment almost nobody "
        "mentions.",
        [("$%s" % format(MBH_ASSOCIATE, ",d"), "loan repayment, associate tier"),
         ("%d yrs" % MBH_YEARS, "service obligation for it"),
         ("90 days", "to stay employable after graduating"),
         ("%s" % MBH_NEXT.split()[-1], "when the next window opens")],
        JUMPS))

    # ------------------------------------------------------------ the question
    o.append('<section class="pk-sec">')
    o.append(pk.quote(
        "Two posts, 87 and 114 comments, and not one structural answer",
        ["I am an AMFT / APCC and I&rsquo;m having a horrible time finding "
         "employment. Everywhere I apply I hear they are looking for someone "
         "with almost totally completed hours. <b>I only have 547.</b> How do "
         "I get hours if everyone expects me to have a&hellip;",
         "After months of applying for jobs without being selected, I have "
         "started considering filing for bankruptcy because, without a job, I "
         "can no longer keep up with my loan payments."]))

    o.append('<p class="pk-k">The short version</p>')
    o.append('<h2 class="pk-h">The bar is not your hours. It is who is allowed '
             "to bill for you.</h2>")
    o.append('<p class="pk-d">Every reply in those threads is about the '
             "applicant &mdash; the resume, the interview, the networking. "
             "The fact underneath is a billing rule, and once you can see it "
             "the pattern in your own rejections stops looking like a "
             "judgment on you.</p>")

    o.append(pk.numbered([
        ("1", "Medi-Cal names you as an authorized provider.",
         "The State Plan Amendment that governs Specialty Mental Health "
         "Services lists registered associates as a staff type whose services "
         "are billable &mdash; alongside licensed psychologists, LCSWs, LMFTs "
         "and LPCCs. Not as an exception. As a category."),
        ("2", "Most commercial payers do not.",
         "A practice whose revenue is commercial insurance generally cannot "
         "bill an associate&rsquo;s session to that payer at all. Its only "
         "economic use for you is private-pay clients, and a practice with a "
         "surplus of those is not a common thing."),
        ("3", "So the two halves of your application list behave differently.",
         "The half that can bill you is reading your application as a revenue "
         "question. The half that cannot is waiting for someone who is nearly "
         "licensed. Applying equally to both, and hearing back from one, "
         "reads as &ldquo;everyone wants completed hours&rdquo;."),
    ]))
    o.append("</section>")

    # --------------------------------------------------------------- why
    o.append('<section class="pk-sec" id="why">')
    o.append('<p class="pk-k">The staff-type list</p>')
    o.append('<h2 class="pk-h">You are on the list. So is the person who has '
             "not got a number yet.</h2>")
    o.append('<p class="pk-d">This is the document that decides whether a '
             "Medi-Cal setting can pay you, and it is more generous than the "
             "job ads suggest.</p>")
    o.append(pk.table(
        ["Who you are", "Billable under Medi-Cal SMHS?", "What it means"],
        [[a, (b, "m"), c] for a, b, c in SMHS_STAFF],
        caption="Transcribed from the DHCS State Plan Amendment listing "
                "authorized SMHS and DMC-ODS staff types. A county or its "
                "contracted agency still applies its own credentialing "
                "procedure on top of this; the State Plan sets the floor, not "
                "the ceiling.",
        minw=640))

    o.append(pk.callout(
        "The 90-day rule is an employment rule as well as an hours rule",
        ["Most people meet the 90-day rule as the thing that decides whether "
         "post-degree hours count. It does a second job nobody advertises: it "
         "is what keeps you inside the authorized staff-type list during the "
         "months between your degree and your registration number.",
         "Which means the window in which a Medi-Cal setting can put you on "
         "payroll opens at your degree award date, not at the arrival of your "
         "number &mdash; and closes if the application is late."]))
    o.append("</section>")

    # --------------------------------------------------------------- who
    o.append('<section class="pk-sec" id="who">')
    o.append('<p class="pk-k">By setting</p>')
    o.append('<h2 class="pk-h">Where the hiring actually is.</h2>')
    o.append('<p class="pk-d">Ordered by how structurally able each setting '
             "is to employ a pre-licensed clinician, which is not the order "
             "most job searches run in.</p>")
    o.append(pk.table(
        ["Setting", "What pays for you there", "Why it hires associates, or does not"],
        [[a, (b, "m"), c] for a, b, c in SETTINGS],
        minw=680))
    o.append('<p class="pk-p">None of this says the county job is the right '
             "one. It says the rejection pattern has a cause that is not "
             "about you, and that a search weighted toward the settings that "
             "can bill for your work is a different search. What each setting "
             'actually pays is on <a href="%s">the associate pay page</a>, '
             'and whether a specific offer is any good is what <a href="%s">'
             "the job advisor</a> is for.</p>" % (PAY, ADVISOR))
    o.append("</section>")

    # ------------------------------------------------------------- the money
    o.append('<section class="pk-sec" id="money">')
    o.append('<p class="pk-k">Loan repayment</p>')
    o.append('<h2 class="pk-h">The $%s an associate can be paid against '
             "student loans.</h2>" % format(MBH_ASSOCIATE, ",d"))
    o.append('<p class="pk-d">The 114-comment thread was written by somebody '
             "weighing bankruptcy over their loan payments. Nobody replied "
             "with this, and it is a state program that names associates "
             "explicitly.</p>")

    o.append(pk.table(
        ["Tier", "Award", "Service obligation"],
        [["Licensed, prescribing", ("$%s" % format(MBH_PRESCRIBER, ",d"), "f"),
          "%d years" % MBH_YEARS],
         (["<b>Non-prescribing licensed, or associate-level pre-licensure</b>",
           ("$%s" % format(MBH_ASSOCIATE, ",d"), "f"),
           "%d years" % MBH_YEARS], "hi"),
         ["Non-licensed, non-prescribing &mdash; SUD counselors, community "
          "health workers, peer support specialists, wellness coaches",
          ("$%s" % format(MBH_UNLICENSED, ",d"), "f"),
          "Two to four years, by award size"]],
        caption="The Medi-Cal Behavioral Health Student Loan Repayment "
                "Program, run by HCAI. Awards are stated as maximums &mdash; "
                "&ldquo;up to&rdquo; &mdash; not as the amount everybody "
                "receives.",
        minw=600))

    o.append('<h3 class="pk-h3">The condition, which is also the point</h3>')
    o.append('<p class="pk-p">The service obligation has to be completed in a '
             "Medi-Cal safety-net setting: a federally qualified health "
             "center, a community mental health center, a rural health "
             "clinic, or a setting where at least <b>%d%%</b> of the "
             "population is on Medicaid or uninsured &mdash; %d%% for rural "
             "hospitals. Which is the same list as the settings that can bill "
             "for your work in the first place.</p>"
             % (MEDICAID_SHARE, RURAL_SHARE))
    o.append('<p class="pk-p">So the setting people describe as the one that '
             "pays worst is also the only one that opens this. That does not "
             "make it the right choice &mdash; it makes it a choice with a "
             "second number attached, and the comparison below is the "
             "arithmetic nobody in those threads ran.</p>")

    o.append(pk.checklist(
        "The other program, and what is not known about it",
        ["The Licensed Mental Health Services Provider Education Program pays "
         "up to $%s for a %d-month commitment at an eligible site in a "
         "shortage area, and can be awarded up to %d times in a career."
         % (format(LMH_AWARD, ",d"), LMH_MONTHS, LMH_TIMES),
         "Its program page does <b>not</b> state whether pre-licensed "
         "registrants qualify, and this page will not guess. The grant guide "
         "and the program mailbox are both linked in the sources.",
         "Both programs run on an annual cycle rather than rolling intake. "
         "The next window opens <b>%s</b>." % MBH_NEXT]))
    o.append("</section>")

    # ---------------------------------------------------------- the calculator
    o.append('<section class="pk-sec" id="compare">')
    o.append('<p class="pk-k">The comparison</p>')
    o.append('<h2 class="pk-h">What the worse offer is actually worth.</h2>')
    o.append('<p class="pk-d">Four years, because that is the service '
             "obligation and roughly the length of an associateship. Put in "
             "two real offers. Everything runs in this browser and nothing is "
             "stored or sent anywhere.</p>")
    o.append(CALC_HTML)
    o.append('<p class="pk-p">Two things the arithmetic cannot weigh, and you '
             "have to. A caseload heavy enough to close %s hours quickly is "
             "also a caseload heavy enough to burn you out before it does. "
             "And an award is a maximum applied for on a cycle, not a "
             "salary &mdash; a plan that only works if the award lands is not "
             "a plan.</p>" % format(TOTAL_HOURS, ",d"))
    o.append("</section>")

    # ---------------------------------------------------------- reading the ad
    o.append('<section class="pk-sec" id="signal">')
    o.append('<p class="pk-k">Reading the posting</p>')
    o.append('<h2 class="pk-h">What &ldquo;must have substantial hours&rdquo; '
             "is really telling you.</h2>")
    o.append(pk.table(
        ["What the ad says", "What it usually means"],
        [["&ldquo;Nearly licensed preferred&rdquo;, from a group private practice",
          "The revenue is commercial insurance and they are waiting for a "
          "license they can bill. Your hour count is not the variable; there "
          "is no number that makes an associate billable to that payer."],
         ["&ldquo;2,000+ hours required&rdquo;",
          "Sometimes a real caseload-independence requirement. Often a filter "
          "written to reduce an applicant pool the poster could not otherwise "
          "read &mdash; the 60-person interview problem, solved with a number."],
         ["&ldquo;Supervision provided&rdquo; with no pay figure",
          "Supervision is not compensation, and unpaid non-clinical time is "
          "its own problem with its own remedy. See the wage-claim page."],
         ["&ldquo;Fee-for-service, per billable hour&rdquo;",
          "Your no-shows, notes, and the supervision the Board requires may "
          "be unpaid under this. That is the single biggest gap between a "
          "headline rate and take-home."],
         ["&ldquo;Medi-Cal&rdquo;, &ldquo;FQHC&rdquo;, &ldquo;county "
          "contract&rdquo;, &ldquo;community mental health&rdquo;",
          "This employer can bill for you, and is plausibly a qualifying "
          "site for the loan repayment above. Worth asking about in the "
          "interview, because the employer often has not thought of it "
          "either."]],
        minw=620))
    o.append('<p class="pk-p">If an offer is on the table rather than '
             'hypothetical, <a href="%s">the job advisor</a> takes the actual '
             "numbers and tells you what the year looks like. If you are "
             'already in one that is not paying you properly, <a href="%s">'
             "the wage-claim page</a> is the remedy the Board cannot give "
             "you.</p>" % (ADVISOR, UNPAID))
    o.append("</section>")

    # ------------------------------------------------------------- the calendar
    o.append('<section class="pk-sec" id="timing">')
    o.append('<p class="pk-k">The calendar</p>')
    o.append('<h2 class="pk-h">Three clocks, and only one of them is '
             "yours.</h2>")
    o.append(pk.numbered([
        ("1", "The 90-day clock, from your degree award date.",
         "It decides whether the months before your number arrives count "
         "&mdash; and whether a Medi-Cal setting can employ you during them. "
         "It starts whether or not you have a job lined up."),
        ("2", "The loan repayment cycle, once a year.",
         "Not rolling. The next window opens %s, which means an employment "
         "decision made in the autumn is a decision about which cycle you are "
         "eligible for." % MBH_NEXT),
        ("3", "The %s-week floor on your own hours.",
         "The %s hours cannot be completed in under %d weeks whatever your "
         "caseload, so the fastest possible associateship is two years. An "
         "offer that starts four months sooner moves your license date by "
         "four months &mdash; and that is the number the comparison above "
         "puts against the pay difference."
         % (format(TOTAL_HOURS, ",d"), WEEKS)),
    ]))
    o.append('<p class="pk-p">How the %s hours actually project from the week '
             'you work is on <a href="%s">the hours page</a>. If your hours '
             'or your license come from another state, <a href="%s">that is a '
             "different route</a> with its own conditions.</p>"
             % (format(TOTAL_HOURS, ",d"), HOURS, OOS))
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, n = pk.sources([
        ("Who may deliver billable services", [
            ("DHCS State Plan Amendment 23-0026 &mdash; authorized staff "
             "types for Specialty Mental Health Services and DMC-ODS, "
             "including registered associates, 90-day candidates and clinical "
             "trainees",
             "https://bhcsproviders.acgov.org/providers/QA/docs/qa_manual/"
             "SPA-23-0026%20SMHS%20DMC-ODS%20Staff%20Types.pdf"),
        ]),
        ("Loan repayment", [
            ("Medi-Cal Behavioral Health Student Loan Repayment Program "
             "&mdash; award tiers, service obligation and qualifying settings",
             "https://hcai.ca.gov/workforce/initiatives/"
             "behavioral-health-bh-connect/mbhslrp/"),
            ("Licensed Mental Health Services Provider Education Program "
             "&mdash; the $%s award, and the page that does not state whether "
             "pre-licensed registrants qualify" % format(LMH_AWARD, ",d"),
             "https://hcai.ca.gov/workforce/financial-assistance/"
             "loan-repayment/lmhspep/"),
            ("California State Loan Repayment Program &mdash; the separate, "
             "federally matched program, for comparison",
             "https://hcai.ca.gov/workforce/financial-assistance/"
             "loan-repayment/slrp/"),
        ]),
        ("The 90-day rule", [
            ("Board of Behavioral Sciences &mdash; 90-day rule frequently "
             "asked questions",
             "https://www.bbs.ca.gov/pdf/90day_rule_faq.pdf"),
        ]),
        ("Where the questions came from", [
            ("Three California therapist Facebook groups, 22,800 members, "
             "read directly in August 2026. Quotes are verbatim and "
             "de-identified; engagement is given as reactions / comments "
             "because the ratio is the finding", None),
        ]),
    ], note="Award figures are the maximums the program publishes, not the "
            "amount every grantee receives, and every program here runs on "
            "an annual cycle that can change. Check the current grant guide "
            "before making an employment decision that depends on one. "
            "Nothing here is legal, financial or career advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


# ------------------------------------------------------------ the comparison
#
# Nothing typed here leaves the page: no URL state, no storage, no analytics
# call, no network. Somebody comparing two real job offers is entering their
# own salary, and the site's printed promise is that nothing typed is sent
# anywhere.
CALC_HTML = """<div class="pk-calc" id="gh-calc">
<div class="pk-cg">
<div class="pk-cc">
<h3>The offer on the table</h3>
<label class="pk-fl" for="gh-a-pay">Annual pay ($)</label>
<input type="number" id="gh-a-pay" min="0" max="300000" step="1000" placeholder="0">
<label class="pk-fl" for="gh-a-hrs">Hours toward licensure per week</label>
<input type="number" id="gh-a-hrs" min="0" max="60" step="1" placeholder="0">
<label class="pk-fl" for="gh-a-slrp">Medi-Cal safety-net setting?</label>
<select id="gh-a-slrp">
<option value="">Choose</option>
<option value="y">Yes &mdash; loan repayment may apply</option>
<option value="n">No, or not sure</option>
</select>
</div>
<div class="pk-cc">
<h3>The one you are holding out for</h3>
<label class="pk-fl" for="gh-b-pay">Annual pay ($)</label>
<input type="number" id="gh-b-pay" min="0" max="300000" step="1000" placeholder="0">
<label class="pk-fl" for="gh-b-hrs">Hours toward licensure per week</label>
<input type="number" id="gh-b-hrs" min="0" max="60" step="1" placeholder="0">
<label class="pk-fl" for="gh-b-wait">Months you would wait for it</label>
<input type="number" id="gh-b-wait" min="0" max="36" step="1" placeholder="0">
<label class="pk-fl" for="gh-award">Loan repayment you would realistically apply for ($)</label>
<input type="number" id="gh-award" min="0" max="180000" step="5000" placeholder="0">
</div>
</div>
<div class="pk-out">
<div class="r hd"><span>Over four years</span><span>Difference</span></div>
<div class="r"><span class="lbl">Pay &mdash; the offer on the table</span><span class="va" id="gh-o-apay">&mdash;</span></div>
<div class="r"><span class="lbl">Pay &mdash; the one you are waiting for</span><span class="va" id="gh-o-bpay">&mdash;</span></div>
<div class="r"><span class="lbl">Loan repayment, if the award lands</span><span class="va" id="gh-o-award">&mdash;</span></div>
<div class="r"><span class="lbl">Weeks to 3,000 hours &mdash; on the table</span><span class="va" id="gh-o-awk">&mdash;</span></div>
<div class="r"><span class="lbl">Weeks to 3,000 hours &mdash; waiting</span><span class="va" id="gh-o-bwk">&mdash;</span></div>
<div class="r tot"><span class="lbl"><b>Four-year gap, taking it now</b></span><span class="va" id="gh-o-tot">&mdash;</span></div>
</div>
<p class="pk-note" id="gh-warn">Put in both offers. Everything is computed in
your browser, nothing is stored, and nothing is sent anywhere.</p>
</div>"""

CALC_JS = """<script>
(function(){
  var EM = '\\u2014';
  function el(id){ return document.getElementById(id); }
  function num(id){
    var e = el(id); if(!e) return 0;
    var v = parseFloat(e.value);
    return (isFinite(v) && v > 0) ? v : 0;
  }
  function val(id){ var e = el(id); return e ? e.value : ''; }
  function money(n){
    return (n < 0 ? '-$' : '$') + Math.round(Math.abs(n)).toLocaleString('en-US');
  }
  function set(id, t){ var e = el(id); if(e) e.textContent = t; }
  function run(){
    var apay = num('gh-a-pay'), ahrs = num('gh-a-hrs');
    var bpay = num('gh-b-pay'), bhrs = num('gh-b-hrs');
    var wait = num('gh-b-wait'), award = num('gh-award');
    var slrp = val('gh-a-slrp');
    var warn = el('gh-warn');

    if(!apay || !bpay){
      ['gh-o-apay','gh-o-bpay','gh-o-award','gh-o-awk','gh-o-bwk','gh-o-tot']
        .forEach(function(id){ set(id, EM); });
      if(warn) warn.innerHTML = 'Put in both offers. Everything is computed ' +
        'in your browser, nothing is stored, and nothing is sent anywhere.';
      return;
    }

    /* Four years of pay. The offer you are waiting for pays nothing during
       the wait, which is the cost the threads never count. */
    var months = 48;
    var aTotal = apay * (months / 12);
    var bTotal = bpay * ((months - Math.min(wait, months)) / 12);

    /* The award only attaches to the safety-net offer, and only if the reader
       said the setting qualifies. An unanswered dropdown is not a yes. */
    var awardCredit = (slrp === 'y') ? award : 0;

    /* The 104-week floor is statutory: 3,000 hours cannot be completed in
       fewer weeks however heavy the caseload. */
    var awk = ahrs ? Math.max(104, Math.ceil(3000 / ahrs)) : 0;
    var bwk = bhrs ? Math.max(104, Math.ceil(3000 / bhrs)) + Math.round(wait * 4.35) : 0;

    set('gh-o-apay', money(aTotal));
    set('gh-o-bpay', money(bTotal));
    set('gh-o-award', awardCredit ? money(awardCredit) :
        (slrp === 'y' ? EM : 'Not available'));
    set('gh-o-awk', awk ? awk + ' wks' : EM);
    set('gh-o-bwk', bwk ? bwk + ' wks' : EM);

    var gap = (aTotal + awardCredit) - bTotal;
    set('gh-o-tot', money(gap));

    var bits = [];
    if(gap > 0){
      bits.push('<b>Taking the offer on the table is ahead by ' + money(gap) +
        ' over four years</b>');
    } else if(gap < 0){
      bits.push('<b>Waiting is ahead by ' + money(-gap) + ' over four years</b>');
    } else {
      bits.push('<b>The two come out level over four years</b>');
    }
    if(wait){
      bits.push('counting ' + wait + ' month' + (wait === 1 ? '' : 's') +
        ' of no pay while you wait');
    }
    if(awardCredit){
      bits.push('and a loan repayment award that is applied for on an annual ' +
        'cycle, not guaranteed');
    } else if(slrp !== 'y' && award){
      bits.push('the award is not counted, because the offer on the table was ' +
        'not marked as a Medi-Cal safety-net setting');
    }
    if(awk && bwk && awk !== bwk){
      bits.push((awk < bwk ? 'and it also licenses you ' + (bwk - awk) :
                 'though it licenses you ' + (awk - bwk)) + ' weeks ' +
                (awk < bwk ? 'sooner' : 'later'));
    }
    if(warn){
      warn.innerHTML = bits.join(', ') + '. Nothing here is stored or sent ' +
        'anywhere.';
    }
  }
  ['gh-a-pay','gh-a-hrs','gh-a-slrp','gh-b-pay','gh-b-hrs','gh-b-wait','gh-award']
    .forEach(function(id){
      var e = el(id);
      if(e){ e.addEventListener('input', run); e.addEventListener('change', run); }
    });
  run();
})();
</script>"""


META = pk.meta_block(
    PAGE,
    "Getting hired as a California associate: why half your applications "
    "never reply",
    "547 hours and nobody will hire you. The reason is a billing rule, not "
    "your hour count - and the settings that can employ you carry "
    "$180,000 of loan repayment.",
    "licensure", "guide",
    "I have 547 hours and everyone wants someone almost done &mdash; how do "
    "I get hired?",
    "Which settings can legally bill for a pre-licensed clinician, the "
    "$180,000 associate loan-repayment tier, and what a worse offer taken "
    "sooner is actually worth",
    "$%s, associate tier" % format(MBH_ASSOCIATE, ",d"),
    weight=5)


def main():
    print("getting hired as a California associate")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=CALC_JS)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the structural thesis", "who is allowed to bill for you"),
        ("the staff-type finding", "Registered associate"),
        ("the 90-day employment consequence", "within 90 days of their degree"),
        ("the award tier", "$%s" % format(MBH_ASSOCIATE, ",d")),
        ("the safety-net condition", "%d%%" % 40),
        ("the comparison", 'id="gh-calc"'),
        ("the comparison script", "gh-o-tot"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # The page turns on associates being NAMED rather than tolerated. If the
    # table loses a row the thesis is unsupported and the hero still asserts it.
    for who, _, _ in SMHS_STAFF:
        if who.split("&mdash;")[0].strip()[:26] not in art:
            print("GUARD: the staff type %r is not on the page" % who[:40])
            bad += 1
    for setting, _, _ in SETTINGS:
        if setting.split(",")[0][:30] not in art:
            print("GUARD: the setting %r is not on the page" % setting[:40])
            bad += 1

    # The 104-week floor is statutory and the calculator enforces it. If the
    # script stops doing so it will print licensure dates that cannot happen.
    if "Math.max(104," not in s:
        print("GUARD: the calculator no longer enforces the 104-week floor")
        bad += 1

    # An award is a maximum applied for on a cycle. Presenting it as certain is
    # the single way this page could do real harm.
    for hedge in ("not as the amount everybody", "not guaranteed",
                  "is not a plan"):
        if hedge not in s:
            print("GUARD: the hedge %r has gone" % hedge)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
