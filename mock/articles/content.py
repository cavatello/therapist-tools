# -*- coding: utf-8 -*-
"""Three articles. Every figure traces to a source verified on 5 August 2026.

Chosen because the research is already done and cited, not because of search
volume. Francis's rule was to pick where you have headroom and then be more
thorough than anyone else; here the headroom is that almost nobody writing for
therapists does the arithmetic.
"""

ARTICLES = [

# ---------------------------------------------------------------- 1. entity
dict(
 slug="therapist-llc-california",
 category="Money",
 stage="run",
 minutes=8,
 updated="2026-08-05",
 title=("Can a California therapist form an LLC? No — and here is what to do instead"),
 h1="You cannot form an LLC in California. <em>Here is what to do instead.</em>",
 h1_plain="You cannot form an LLC in California. Here is what to do instead.",
 kicker="California &middot; entity structure",
 dek=("Every small-business guide points you at the same door and calls it the obvious one. For a "
      "licensed therapist in California that door is locked, and it is one sentence in the "
      "Corporations Code that locks it. Let us go and read the sentence."),
 dek_plain=("Every small-business guide points you at the same door and calls it the obvious one. "
            "For a licensed therapist in California that door is locked, and it is one sentence "
            "in the Corporations Code that locks it. Let us go and read the sentence."),
 figure=("&sect;17701.04", "the subsection that ends the argument"),
 tool=("therapist-tax-strategy-california.html",
       "Work out which structure is actually cheaper on your numbers",
       "The tax page runs the whole engine twice &mdash; once as a sole proprietor, once as "
       "a professional corporation with an S election &mdash; and itemises what the "
       "structure costs against what it saves. It uses your own profit, not an example."),
 sections=[
  ("The sentence that closes the door", [
   ("p", "Picture the search you have almost certainly already run. How to structure a therapy "
         "practice. The answers come back confident and unanimous: form an LLC. It is what nearly "
         "every small business in this country does, it is what your accountant friend in another "
         "state did, and it is what the first four results will tell you."),
   ("p", "It is also not available to you. That is the kind of claim that deserves the source "
         "rather than a summary of the source, so here it is, whole:"),
   ("quote", "&ldquo;Nothing in this title shall be construed to permit a domestic or "
             "foreign limited liability company to render professional services, as "
             "defined in subdivision (a) of Section 13401 and in Section 13401.3, in this "
             "state.&rdquo;",
    "Cal. Corp. Code &sect;17701.04(e) &mdash; see source [1]"),
   ("p", "&ldquo;Professional services&rdquo; means services requiring a licence. Marriage "
         "and family therapy, clinical social work, professional clinical counselling and "
         "psychology are all in that category. So the LLC is out &mdash; not disfavoured, "
         "not risky, <b>unavailable</b>.<sup><a href=\"#s1\">[1]</a></sup>"),
   ("p", "This matters more than a technicality, because people do form them. A therapist "
         "who registers an LLC and practises through it has an entity that cannot lawfully "
         "render the service it exists to render, which is a problem you would rather find "
         "out about now than during a Board complaint or a malpractice claim."),
  ]),
  ("What is actually on the menu", [
   ("p", "Two things."),
   ("ul", ["<b>A sole proprietorship.</b> No filing, no separate return, no annual minimum "
           "tax. You and the practice are the same legal person for tax purposes, and your "
           "income lands on a Schedule C.",
           "<b>A California professional corporation</b>, which for an MFT is specifically a "
           "marriage and family therapy corporation. It is a real corporation, it files its "
           "own return, and it can then elect S-corp treatment with the IRS &mdash; which is "
           "the thing people are usually reaching for when they say &ldquo;LLC&rdquo;."]),
   ("p", "The second one has its own statute. A marriage and family therapy corporation "
         "must comply with the Moscone-Knox Professional Corporation Act, and the Business "
         "and Professions Code says so in terms.<sup><a href=\"#s2\">[2]</a></sup>"),
  ]),
  ("Who is allowed to own it", [
   ("p", "This is where a widely repeated figure is slightly wrong in a way worth "
         "correcting. You will read that a therapy corporation must be &ldquo;51% "
         "therapist-owned&rdquo;. The statute does not say that. It sets a ceiling on "
         "everyone else:"),
   ("quote", "&ldquo;&hellip;so long as the sum of all shares owned by those licensed "
             "persons does not exceed 49 percent of the total number of shares of the "
             "professional corporation&hellip;&rdquo;",
    "Cal. Corp. Code &sect;13401.5 &mdash; see source [3]"),
   ("p", "The 51% is the arithmetic complement, not a quoted figure. In practice it comes "
         "to the same place, but if you are drafting a cap table with a psychologist or an "
         "LCSW co-owner, the number the statute actually constrains is theirs, not "
         "yours.<sup><a href=\"#s3\">[3]</a></sup>"),
   ("p", "One more oddity worth knowing before a lawyer corrects you: &sect;13401.5 labels "
         "it a <b>marriage and family therapist corporation</b>, while the Business and "
         "Professions Code calls it a <b>marriage and family therapy corporation</b>. Both "
         "are correct in their own code. Do not let a copy editor &ldquo;fix&rdquo; one "
         "into the other."),
  ]),
  ("The name is constrained too", [
   ("p", "You cannot call it whatever you like, and this is where filings get rejected at "
         "the Secretary of State:"),
   ("quote", "&ldquo;The name of a marriage and family therapy corporation shall contain "
             "one or more of the words &lsquo;marriage,&rsquo; &lsquo;family,&rsquo; or "
             "&lsquo;child&rsquo; together with one or more of the words "
             "&lsquo;counseling,&rsquo; &lsquo;counselor,&rsquo; &lsquo;therapy,&rsquo; or "
             "&lsquo;therapist,&rsquo; and wording or abbreviations denoting corporate "
             "existence.&rdquo;",
    "B&amp;P Code &sect;4987.7 &mdash; see source [4]"),
   ("p", "So &ldquo;Jordan Reyes, Inc.&rdquo; will not do. &ldquo;Reyes Family Therapy "
         "Corporation&rdquo; will.<sup><a href=\"#s4\">[4]</a></sup>"),
  ]),
  ("So which one should you choose", [
   ("p", "Here the question stops being legal and becomes arithmetic. And the honest answer turns "
         "on one number you have most likely never written down: your practice profit after "
         "expenses. Not your gross. Not what the panels pay. What is left."),
   ("p", "The corporation is not free. California charges every corporation a <b>minimum "
         "franchise tax of $800 a year whether or not it made a profit</b>, waived only in "
         "the first year.<sup><a href=\"#s5\">[5]</a></sup> On top of that the state does "
         "not honour the S election the way the IRS does &mdash; it still taxes the entity "
         "<b>1.5% of California source income</b>.<sup><a href=\"#s6\">[6]</a></sup> Then "
         "there is payroll, a corporate return, a Statement of Information, and the "
         "California payroll taxes on your own wage that most comparisons quietly omit."),
   ("pull", "$800", "owed every year whether or not the practice made a profit &mdash; the "
                    "single biggest reason a low-revenue practice should stay a sole "
                    "proprietorship"),
   ("p", "Against that sits the self-employment tax you stop paying on the distribution. "
         "Whether the saving clears the cost depends entirely on your profit and the salary "
         "you pay yourself, and near the break-even point the answer flips."),
   ("p", "There is no rule of thumb worth trusting here. Anyone who offers you one is guessing at "
         "your numbers, which is why the calculator below runs the whole engine twice on yours, "
         "and shows you the lines rather than handing down a verdict."),
  ]),
 ],
 sources=[
  (1, "Cal. Corporations Code &sect;17701.04",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17701.04.&lawCode=CORP",
   "subdivision (e) prohibits an LLC from rendering professional services in California"),
  (2, "Cal. Business &amp; Professions Code &sect;4987.5",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4987.5.&lawCode=BPC",
   "defines a marriage and family therapy corporation and requires Moscone-Knox compliance"),
  (3, "Cal. Corporations Code &sect;13401.5",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=13401.5.&lawCode=CORP",
   "caps other licensed shareholders at 49%; subdivision (g) is the MFT corporation"),
  (4, "Cal. Business &amp; Professions Code &sect;4987.7",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4987.7.&lawCode=BPC",
   "the naming requirement"),
  (5, "California Franchise Tax Board &mdash; Corporations",
   "https://www.ftb.ca.gov/file/business/types/corporations/index.html",
   "the $800 minimum franchise tax, and the first-year exemption"),
  (6, "California Franchise Tax Board &mdash; S corporations",
   "https://www.ftb.ca.gov/file/business/types/corporations/s-corporations.html",
   "California taxes S corporations 1.5% of California source income"),
 ]),

# ------------------------------------------------------------------- 2. SDI
dict(
 slug="s-corp-sdi-california-therapist",
 category="Money",
 stage="run",
 minutes=6,
 updated="2026-08-05",
 title="California SDI and the S-corp: the $1,248 the pitch forgets",
 h1="The <em>$1,248</em> the S-corp pitch forgets.",
 h1_plain="The $1,248 the S-corp pitch forgets.",
 kicker="California &middot; payroll tax",
 dek=("Every comparison of sole proprietor against S-corp counts the self-employment tax you stop "
      "paying. Almost none of them notice what you become on the day your corporation first pays "
      "you a wage. You become an employer. California has a great deal to say about employers."),
 dek_plain=("Every comparison of sole proprietor against S-corp counts the self-employment tax "
            "you stop paying. Almost none of them notice what you become on the day your "
            "corporation first pays you a wage. You become an employer. California has a great "
            "deal to say about employers."),
 figure=("$1,248", "State Disability, on a $96,000 salary, that a sole proprietor never pays"),
 tool=("therapist-tax-strategy-california.html",
       "See it in the itemised comparison",
       "The tax page now charges California payroll tax on your own wage as its own line, "
       "against the self-employment tax you stop paying, the franchise tax, the filings and "
       "the QBI deduction you give up. On your profit, not an example."),
 sections=[
  ("What the pitch counts, and what it leaves out", [
   ("p", "Let us begin with the pitch as it is usually made, because it is a good pitch and most "
         "of it is true. As a sole proprietor you pay self-employment tax on all of your net "
         "earnings. As an S-corp you pay yourself a salary, pay payroll tax on that, and take the "
         "rest as a distribution which is not subject to it. The gap is the saving, and the "
         "saving is real."),
   ("p", "Set against that saving, most comparisons count California's $800 minimum "
         "franchise tax, the 1.5% state tax on S-corp income, a payroll service, a "
         "corporate return, and the qualified business income deduction that shrinks when "
         "you pay yourself a wage."),
   ("p", "What almost none of them count is the thing that happened quietly on the day the salary "
         "started. <b>A corporation that pays you is an employer.</b> You are now standing on "
         "both sides of that sentence &mdash; the one issuing the wage and the one receiving it "
         "&mdash; and California taxes both."),
  ]),
  ("The two lines that go missing", [
   ("p", "There are two, and one of them is much larger than the other."),
   ("table", ["What", "Rate", "On", "A $96,000 salary"], [
     ["State Disability Insurance", "1.3%", "the whole salary, no cap", "$1,248"],
     ["UI, ETT and FUTA", "4.1% combined", "the first $7,000 only", "$287"],
     ["Total", "", "", "$1,535"]]),
   ("p", "The second line is small and flat &mdash; those taxes stop at the $7,000 wage "
         "base, so they are about $287 at any realistic salary. The first is the one that "
         "matters, because <b>California removed the SDI wage cap on 1 January 2024</b>. It "
         "is now 1.3% of the entire salary with no ceiling, so it scales with every raise "
         "you give yourself.<sup><a href=\"#s1\">[1]</a></sup>"),
   ("p", "A sole proprietor pays none of this. Self-employment tax does not include state "
         "disability, and a self-employed person is only covered if they opt in separately."),
   ("pull", "$1,535", "a year that belongs on the corporation's side of the ledger and is "
                      "usually missing from it"),
  ]),
  ("What it does to the answer", [
   ("p", "Adding the missing line to our own engine moved the numbers more than we "
         "expected. At 50% salary, on the site's worked example:"),
   ("table", ["Practice profit", "S-corp advantage before", "After"], [
     ["$192,000", "$3,237 a year better", "$1,702 a year better"],
     ["$151,200", "$2,411 better", "$1,142 better"],
     ["$122,880", "$1,655 better", "$570 better"],
     ["$108,000", "$1,258 better", "$269 better"],
     ["$94,080", "$887 better", "$12 a year <b>worse</b>"]]),
   ("p", "At the bottom of that table the verdict flips. A practice clearing about $94,000 "
         "was being told to incorporate and should not bother &mdash; which is exactly the "
         "margin where someone actually needs the answer, and exactly where a rule of thumb "
         "is least useful."),
  ]),
  ("You can escape the SDI, but not for free", [
   ("p", "There is a way out of the larger line, and it is worth knowing precisely because "
         "it is opt-in. A corporate officer who is the sole shareholder &mdash; or the only "
         "shareholder besides a spouse &mdash; may file <b>form DE 459</b> and be excluded "
         "from State Disability coverage, under section 637.1 of the Unemployment Insurance "
         "Code.<sup><a href=\"#s2\">[2]</a></sup>"),
   ("p", "Three things follow, and they are why our engine models the default rather than "
         "the exception."),
   ("ul", ["<b>Nothing happens automatically.</b> A therapist who incorporates and files "
           "nothing pays SDI.",
           "<b>It is not free money.</b> The exclusion gives up State Disability and Paid "
           "Family Leave cover. For a solo practitioner with no sick pay and no employer "
           "behind them, that is a real trade, not a loophole.",
           "<b>It covers SDI only.</b> The form says so itself: the corporation must still "
           "report your wages and pay Unemployment Insurance and Employment Training Tax. "
           "The $287 is not escapable."]),
   ("p", "So the honest framing is not &ldquo;you can avoid this&rdquo;. It is: this costs "
         "$1,248 a year unless you deliberately give up your disability cover, in which "
         "case it costs you that cover instead."),
  ]),
  ("Why this is easy to miss", [
   ("p", "Worth saying plainly, because we missed it ourselves for months. Our engine "
         "already charged Unemployment Insurance, ETT and FUTA correctly &mdash; on "
         "<b>associate</b> wages, a few functions away in the same file. It simply never "
         "charged them on the owner's own salary, and never modelled SDI at all."),
   ("p", "There was also a variable in that engine named <code>SDI</code>. It holds 0.124 "
         "&mdash; the Social Security rate, not California State Disability. Searching the "
         "code for &ldquo;SDI&rdquo; found it, and it looked handled."),
   ("p", "If you are checking your own accountant's spreadsheet, or anyone else's "
         "calculator, that is the line to look for: <b>does the corporation's side charge "
         "anything at all for California payroll on your own wage?</b> If it does not, the "
         "comparison is flattering the corporation by roughly $1,500 a year."),
  ]),
 ],
 sources=[
  (1, "California EDD &mdash; Payroll tax rates and withholding",
   "https://edd.ca.gov/en/payroll_taxes/rates_and_withholding/",
   "&ldquo;The SDI withholding rate for 2026 is 1.3 percent&rdquo;; &ldquo;Effective January "
   "1, 2024, all wages are subject to SDI contributions&rdquo;; ETT 0.1%; UI and ETT wage "
   "limit $7,000"),
  (2, "California EDD form DE 459 &mdash; Sole Shareholder/Corporate Officer Exclusion",
   "https://edd.ca.gov/siteassets/files/pdf_pub_ctr/de459.pdf",
   "excludes SDI only, under CUIC &sect;637.1; &ldquo;The corporation must report your wages "
   "and pay contributions for Unemployment Insurance (UI) and Employment Training Tax "
   "(ETT)&rdquo;"),
 ]),

# ------------------------------------------------------------------ 3. fees
dict(
 slug="bbs-fees-california-2026",
 category="Licensure",
 stage="pre",
 minutes=5,
 updated="2026-08-05",
 title="BBS fees halved in July 2026: what the route to licensure actually costs",
 h1="BBS fees halved in July. <em>The route now costs $575 to $875.</em>",
 h1_plain="BBS fees halved in July. The route now costs $575 to $875.",
 kicker="California &middot; Board of Behavioral Sciences",
 dek=("Every Board fee halved on 1 July 2026. What the whole route costs still depends on one "
      "thing nobody writes down &mdash; how many years you spend as an associate. Here is the "
      "arithmetic, and the reversion date that ends it."),
 dek_plain=("Every Board fee halved on 1 July 2026. What the whole route costs still depends on "
            "one thing nobody writes down - how many years you spend as an associate. Here is "
            "the arithmetic, and the reversion date that ends it."),
 figure=("$575&ndash;$875", "the whole route, depending on your years as an associate"),
 tool=("amft-3000-hours-california.html",
       "Put it against your actual timeline",
       "The 3,000-hours page projects all four BBS requirements from the week you actually "
       "work, and names the one you are waiting on. The fee schedule below is built into it."),
 sections=[
  ("What changed", [
   ("p", "If you have looked up the cost of getting licensed in California in the past few weeks, "
         "there is a fair chance you were quoted a number that is no longer true. The Board of "
         "Behavioral Sciences reduced almost every fee it charges, effective <b>1 July 2026</b>. "
         "The reduction is temporary and runs to <b>30 June 2030</b>.<sup><a "
         "href=\"#s1\">[1]</a></sup>"),
   ("table", ["Fee", "Was", "Now"], [
     ["Registration application &mdash; AMFT, ASW, APCC", "$150", "$75"],
     ["Annual renewal &mdash; AMFT, ASW, APCC", "$150", "$75"],
     ["California Law &amp; Ethics exam", "$150", "$75"],
     ["Licence application", "$250", "$125"],
     ["LMFT clinical exam", "$250", "$125"],
     ["Initial licence issuance", "$200", "$100"],
     ["Biennial renewal, active", "$200", "$100"],
     ["Biennial renewal, inactive", "$100", "$50"]]),
   ("p", "Now the part every version of this article gets wrong, including an earlier "
         "version of this one. There is no single number, because <b>the fees you pay "
         "once are not the whole bill</b>. Five of them you pay exactly once:"),
   ("table", ["Paid once", "Amount"], [
     ["Registration application", "$75"],
     ["California Law &amp; Ethics exam", "$75"],
     ["Licence application", "$125"],
     ["LMFT clinical exam", "$125"],
     ["Initial licence issuance", "$100"],
     ["<b>Subtotal</b>", "<b>$500</b>"]]),
   ("p", "Your registration then runs for one year from the last day of the month it was "
         "issued &mdash; that first year is already inside the $75 you just paid. Every "
         "year after it is another $75, and you may renew five times before the "
         "registration cancels at six years.<sup><a href=\"#s3\">[3]</a></sup> So the "
         "answer is a line, not a point:"),
   ("table", ["Time as an associate", "Renewals", "Total Board fees"], [
     ["Under a year", "0", "$500"],
     ["1&ndash;2 years &mdash; the 104-week statutory minimum", "1", "$575"],
     ["2&ndash;3 years", "2", "$650"],
     ["3&ndash;4 years", "3", "$725"],
     ["4&ndash;5 years", "4", "$800"],
     ["5&ndash;6 years &mdash; the statutory ceiling", "5", "$875"]]),
   ("p", "The 3,000 hours cannot be completed in under 104 weeks, so <b>$575 is the "
         "floor</b> for anyone who finishes as fast as the law allows. <b>$875 is the "
         "ceiling</b>, and it is what you pay if you use the full six years. Most people "
         "land between. Every one of those totals is exactly half of what the same route "
         "cost before July."),
   ("pull", "$650", "two renewals &mdash; the middle of the range, and the most common "
                    "answer"),
  ]),
  ("Two things the headline number leaves out", [
   ("p", "First, a <b>$20 Mental Health Practitioner Education Fund fee</b> is not part of "
         "the reduction. It attaches to licence renewal-related applications, which means "
         "it touches nothing on the road from registration to your first licence &mdash; "
         "but it does make a real LMFT biennial renewal <b>$120, not $100</b>.<sup><a "
         "href=\"#s1\">[1]</a></sup>"),
   ("p", "Second, this is temporary. On 1 July 2030 the old schedule returns. If you are "
         "budgeting a licensure timeline that runs past that date, the back half costs "
         "double the front half."),
   ("p", "And the law and ethics exam fee can recur: associates must take it "
         "<b>annually until they pass</b> in order to renew a registration, so the $75 is "
         "not necessarily a one-off.<sup><a href=\"#s2\">[2]</a></sup>"),
  ]),
  ("The Board contradicts itself, and that is worth knowing", [
   ("p", "If you go looking for these numbers you will find two different answers on "
         "bbs.ca.gov. The fee reduction FAQ carries the reduced schedule. The Board's own "
         "<b>Manage License/Registration</b> page still displays the pre-reduction table, "
         "with $150 annual renewals and $220 active renewals."),
   ("p", "We cite the FAQ, because it is the more specific and more recent document and it "
         "states its own effective dates. But if you land on the renewal page first and see "
         "the old figures, that is why. Do not assume you have been quoted wrongly."),
  ]),
  ("What is not included at all", [
   ("p", "Board fees are a small part of what pre-licensure actually costs. Not in any of "
         "the numbers above:"),
   ("ul", ["<b>Supervision, if you pay for it.</b> Group private practice often bills it "
           "back at roughly $450 a month, which is about $5,400 a year out of your "
           "take-home &mdash; several times the entire Board fee for the year.",
           "<b>Professional liability insurance.</b>",
           "<b>Continuing education.</b> Associates need 3 hours of California law and "
           "ethics each one-year renewal period.",
           "<b>Fingerprinting and duplicate documents</b>, which the FAQ excludes from the "
           "reduction explicitly. If you are applying from outside California you also pay "
           "the Board a $49 hard-card fingerprint fee, which was not reduced.",
           "<b>The clinical exam for LCSWs and LPCCs</b>, which is administered by ASWB and "
           "NBCC respectively and priced by them, not by the Board."]),
   ("p", "One more thing worth knowing before you budget: the clinical exam fee is not "
         "billed to you later. It is collected <b>with the licence application</b>, as a "
         "single $250 payment, so that is one bill and not two."),
   ("p", "The fee cut is real and it is welcome. It is also, for most associates, a smaller "
         "line than one month of supervision."),
  ]),
 ],
 sources=[
  (1, "BBS Temporary Fee Reduction FAQ",
   "https://www.bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf",
   "effective 1 July 2026 through 30 June 2030; the full reduced schedule; the $20 Mental "
   "Health Practitioner Education Fund fee is not reduced; fingerprint and duplicate "
   "document fees excluded"),
  (2, "BBS &mdash; California Law and Ethics Exam",
   "https://www.bbs.ca.gov/exams/calaw_ethics.html",
   "&ldquo;Exam must be TAKEN annually, until passed, to renew an Associate "
   "Registration&rdquo;"),
  (3, "Cal. Bus. &amp; Prof. Code &sect;4984.01",
   "https://law.justia.com/codes/california/code-bpc/division-2/chapter-13/article-4/section-4984-01/",
   "a registration expires one year from the last day of the month in which it was issued, "
   "and may be renewed a maximum of five times &mdash; six years in total"),
 ]),


# ------------------------------------------------------ 4. cost of incorporating
dict(
 slug="cost-of-incorporating-california-therapist",
 category="Money",
 stage="run",
 minutes=7,
 updated="2026-08-06",
 title=("What incorporating actually costs a California therapist, "
        "before you earn a dollar"),
 h1="The corporation costs <em>$800 before you see a client</em>.",
 h1_plain="The corporation costs $800 before you see a client.",
 kicker="California &middot; entity structure",
 dek=("Everyone quotes the self-employment tax an S election saves. Far fewer "
      "quote what the corporation charges you for the privilege &mdash; a floor "
      "that arrives whether or not you made anything, and a first-year rule that "
      "almost every guide states backwards."),
 dek_plain=("Everyone quotes the self-employment tax an S election saves. Far fewer "
            "quote what the corporation charges you for the privilege - a floor that "
            "arrives whether or not you made anything, and a first-year rule that "
            "almost every guide states backwards."),
 figure=("$800", "the minimum, owed on a year you earned nothing"),
 tool=("therapist-tax-strategy-california.html",
       "Price the corporation against staying a sole proprietor, on your profit",
       "The tax page runs the whole engine twice and itemises every cost on this "
       "page against the self-employment tax the election saves. It uses your own "
       "profit rather than an example, which is the only way this question has an "
       "answer."),
 sections=[
  ("The floor", [
   ("p", "Picture the worst year you can plausibly have. A referral source dries "
         "up, you take three months off, the practice makes almost nothing. As a "
         "sole proprietor that year costs you nothing in entity tax, because there "
         "is no entity."),
   ("p", "As a corporation it costs <b>$800</b>."),
   ("quote", "&ldquo;Every corporation that is incorporated, registered, or doing "
             "business in California must pay the $800 minimum franchise tax.&rdquo;",
    "Franchise Tax Board &mdash; see source [1]"),
   ("p", "That is the whole of it. Not a tax on profit, not a fee scaled to "
         "revenue &mdash; a floor. The franchise tax is <b>the greater of 1.5% of "
         "net income or $800</b>, so the $800 is what you pay in every year the "
         "1.5% comes to less.<sup><a href=\"#s2\">[2]</a></sup>"),
   ("pull", "$800", "owed on a year the practice made nothing at all"),
   ("p", "At what profit does the 1.5% overtake the floor? Divide: <b>$53,333</b>. "
         "Below that the corporation charges you $800; above it, 1.5% of everything."),
  ]),

  ("The first-year rule everyone states backwards", [
   ("p", "You will read that your first year is free. It is half true, and the "
         "half that is wrong is the half that costs money."),
   ("p", "The exemption is real: <b>&ldquo;newly incorporated or qualified "
         "corporations are not required to pay the minimum franchise tax in their "
         "first taxable year&rdquo;</b>.<sup><a href=\"#s1\">[1]</a></sup> But it "
         "exempts you from the <b>minimum</b> only &mdash; not from the tax itself."),
   ("quote", "&ldquo;New corporations&hellip; are exempt from the minimum franchise "
             "tax for its first return, but must compute their tax by multiplying "
             "their net income for the year by 1.5%.&rdquo;",
    "California Tax Service Center &mdash; see source [2]"),
   ("p", "So a first-year corporation that made $90,000 does not pay $0. It pays "
         "<b>$1,350</b>, and it pays it on time. What the exemption saves is the "
         "$800 you would have owed if you had made nothing."),
   ("p", "There is a second half to this that catches people harder. Estimated tax "
         "payments are required from the first year, not from the second &mdash; "
         "the Board expects corporations to pay in as they go, whatever their "
         "history.<sup><a href=\"#s3\">[3]</a></sup> A first year spent assuming "
         "nothing is due arrives at April with a bill and a penalty."),
  ]),

  ("A note on why the LLC rule does not apply to you", [
   ("p", "Much of the confusion here is imported from a different entity. "
         "California waived the LLC annual tax for first-year LLCs under Assembly "
         "Bill 85 &mdash; and that waiver expired. Articles written in 2022 said "
         "&ldquo;first year free&rdquo;, articles written in 2024 said the "
         "opposite, and both were about LLCs."),
   ("p", "None of it is about you. A California therapist <b>cannot form an LLC "
         "for licensed practice at all</b>,<sup><a href=\"#s4\">[4]</a></sup> so "
         "the only first-year rule that applies is the corporation one above, "
         "which is not scheduled to expire. "
         "<a href=\"therapist-llc-california.html\">Why the LLC is closed to you "
         "&rarr;</a>"),
  ]),

  ("The costs that are not the franchise tax", [
   ("p", "The $800 is the visible one. Three more arrive with it, and only one of "
         "them is usually counted."),
   ("ul", ["<b>Payroll on your own wage.</b> A corporation that pays you is an "
           "employer. California charges State Disability Insurance at 1.3% of the "
           "<b>whole</b> salary with no cap since 2024, plus Unemployment "
           "Insurance, ETT and FUTA on the first $7,000. On a $96,000 salary that "
           "is $1,248 and $287. A sole proprietor pays none of it. "
           "<a href=\"s-corp-sdi-california-therapist.html\">The $1,248 in full "
           "&rarr;</a>",
           "<b>A corporate return.</b> Form 100S is not a Schedule C, and it is "
           "not the sort of thing most therapists file themselves.",
           "<b>A payroll service.</b> Running one employee through payroll monthly "
           "is a subscription you did not previously have, and doing it by hand is "
           "how reasonable-compensation problems start."]),
   ("p", "The one figure I have seen put on the whole running cost comes from "
         "Heard, an accounting firm working only with therapists: roughly "
         "<b>$4,400 a year</b>, with a floor of <b>$100,000</b> of annual net "
         "income before the election is worth making at all. That is one firm's "
         "number rather than a rule, and it is quoted here as such."),
  ]),

  ("So when does it pay", [
   ("p", "The honest answer is that it depends on a number this page does not "
         "have, and neither does any other page written for a general audience: "
         "your profit after expenses, and the salary you would actually pay "
         "yourself."),
   ("p", "What can be said without your numbers is the shape. The saving grows "
         "with the distribution you take. The cost is mostly <b>fixed</b> &mdash; "
         "$800, a return, a payroll service &mdash; with one part that scales, the "
         "1.5%. Fixed costs against a growing saving is a curve with a crossing "
         "point, and below that point incorporating loses money with perfect "
         "reliability."),
   ("p", "Which is why there is a calculator below rather than a verdict here."),
  ]),
 ],
 sources=[
  (1, "Franchise Tax Board &mdash; Corporations",
   "https://www.ftb.ca.gov/file/business/types/corporations/index.html",
   "the $800 minimum franchise tax, and the first-year exemption from the minimum "
   "for newly incorporated corporations"),
  (2, "California Tax Service Center &mdash; S corporations",
   "https://taxes.ca.gov/s-corporations/",
   "&ldquo;the greater of 1.5% of the corporation&rsquo;s net income or $800&rdquo;, "
   "and the rule that a first-year corporation still computes the 1.5%"),
  (3, "FTB Publication 1060 &mdash; Guide for corporations starting business in "
      "California", "https://www.ftb.ca.gov/forms/misc/1060.html",
   "the estimated-payment requirement from the first year, and the 1.5% S "
   "corporation rate"),
  (4, "Cal. Corporations Code &sect;17701.04",
   "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17701.04.&lawCode=CORP",
   "subdivision (e) &mdash; why an LLC, and therefore the LLC first-year rules, are "
   "not available for licensed practice"),
 ],
),

# --------------------------------------------------------- 5. estimated taxes
dict(
 slug="quarterly-estimated-taxes-california-therapist",
 category="Money",
 stage="run",
 minutes=6,
 updated="2026-08-06",
 title=("Quarterly estimated taxes for a California therapist: four dates, "
        "and one of them is zero"),
 h1="California asks for <em>30, 40, 0 and 30</em>. In that order.",
 h1_plain="California asks for 30, 40, 0 and 30. In that order.",
 kicker="California &middot; paying as you go",
 dek=("The federal instalments are four roughly equal payments. California&rsquo;s "
      "are not equal, are not in the order you would guess, and the September one "
      "is nothing at all. Budgeting them as quarters is how a practice ends up "
      "short in June."),
 dek_plain=("The federal instalments are four roughly equal payments. California's are "
            "not equal, are not in the order you would guess, and the September one is "
            "nothing at all. Budgeting them as quarters is how a practice ends up short "
            "in June."),
 figure=("30/40/0/30", "California&rsquo;s four instalments, as percentages"),
 tool=("therapist-tax-strategy-california.html",
       "Work out what the year owes before you divide it up",
       "Every instalment on this page is a share of one annual figure, so the "
       "instalment is only as good as that figure. The tax page computes the year "
       "&mdash; federal, California, self-employment &mdash; on your own profit."),
 sections=[
  ("Two schedules, not one", [
   ("p", "A private practice has no employer withholding anything, so the tax "
         "arrives in instalments you send yourself. There are two sets of them, "
         "they share three of their four dates, and they divide the year "
         "completely differently."),
   ("p", "The federal instalments are what you would expect &mdash; four payments, "
         "one per quarter, 15 April, 15 June, 15 September and 15 January."
         "<sup><a href=\"#s2\">[2]</a></sup>"),
   ("p", "California&rsquo;s are not:"),
   ("table", ["Instalment", "Due", "Share of the year"],
    [["First", "15 April 2026", "30%"],
     ["Second", "15 June 2026", "40%"],
     ["Third", "15 September 2026", "0%"],
     ["Fourth", "15 January 2027", "30%"]]),
   ("p", "That third line is not a typo and it is the thing worth knowing. "
         "<b>California asks for nothing in September.</b> It has already asked "
         "for 70% of the year by 15 June.<sup><a href=\"#s1\">[1]</a></sup>"),
   ("pull", "70%", "of the California year, due by 15 June"),
  ]),

  ("Why the shape matters more than the dates", [
   ("p", "A therapist who budgets &ldquo;a quarter each quarter&rdquo; is fine "
         "federally and 40% short in June. The California year is front-loaded: "
         "seventy per cent of it lands in the first two months of the tax "
         "calendar, before most practices have had a chance to earn it."),
   ("p", "In a growing practice this is uncomfortable but survivable. In a "
         "practice with a seasonal shape &mdash; and therapy has one, with the "
         "summer dip most private practices know &mdash; a 40% payment due on 15 "
         "June, computed on last year, arrives at close to the worst possible "
         "moment."),
   ("p", "The September zero is not a gift. It is the reason June is 40%."),
  ]),

  ("The safe harbour, which is the part that actually protects you", [
   ("p", "You are not required to guess this year correctly. Both systems let you "
         "pay by reference to <b>last</b> year instead, and a year you have already "
         "filed is a number rather than a forecast."),
   ("ul", ["<b>Federal.</b> Pay the lesser of 90% of the current year&rsquo;s tax, "
           "or 100% of last year&rsquo;s. If last year&rsquo;s adjusted gross "
           "income was above <b>$150,000</b> ($75,000 married filing separately), "
           "the prior-year figure rises to <b>110%</b>."
           "<sup><a href=\"#s2\">[2]</a></sup>",
           "<b>California.</b> The same structure and the same threshold: 100% of "
           "last year, or <b>110%</b> if last year&rsquo;s California AGI was above "
           "<b>$150,000</b> ($75,000 married filing separately)."
           "<sup><a href=\"#s1\">[1]</a></sup>",
           "<b>And one more California rule</b> that will not apply to most "
           "readers but is absolute when it does: at a current-year California AGI "
           "of <b>$1,000,000</b> or more, the prior-year safe harbour disappears "
           "entirely and you must pay on <b>90% of the current year</b>."
           "<sup><a href=\"#s1\">[1]</a></sup>"]),
   ("p", "The practical consequence is worth stating plainly. In a year your "
         "income is <b>rising</b>, paying on last year is the cheaper "
         "arrangement &mdash; you keep the difference until April and owe no "
         "penalty. In a year your income is <b>falling</b>, paying on last year "
         "means lending the state money you did not have to."),
  ]),

  ("What this does not decide", [
   ("p", "Nothing on this page tells you the amount. It tells you the fractions "
         "and the dates the fractions attach to, which is only useful once you "
         "have a year&rsquo;s tax to divide."),
   ("p", "And a caution about the safe harbour specifically: it protects you from "
         "the <b>penalty</b>, not from the bill. Paying 100% of a small prior year "
         "through a large current one is entirely legal and leaves the whole "
         "difference due in April. That is a cash-flow decision rather than a tax "
         "one, and it is the one people regret."),
  ]),
 ],
 sources=[
  (1, "Franchise Tax Board &mdash; Estimated tax payments",
   "https://www.ftb.ca.gov/pay/estimated-tax-payments.html",
   "the 30/40/0/30 instalment percentages and their due dates; the 100% and 110% "
   "prior-year safe harbours and the $150,000 threshold; the 90% current-year "
   "requirement above $1,000,000 of California AGI"),
  (2, "IRS &mdash; Estimated tax, frequently asked questions",
   "https://www.irs.gov/faqs/estimated-tax",
   "the four federal payment periods and due dates; 90% of the current year or "
   "100% of the prior year, rising to 110% above $150,000 of prior-year AGI"),
 ],
),


# ------------------------------------------------------------ 6. backdoor Roth
dict(
 slug="backdoor-roth-pro-rata-therapist",
 category="Money",
 stage="run",
 minutes=7,
 updated="2026-08-06",
 title=("The backdoor Roth, and the one account balance that ruins it"),
 h1="The backdoor Roth is simple. <em>One old account makes it expensive.</em>",
 h1_plain="The backdoor Roth is simple. One old account makes it expensive.",
 kicker="California &middot; retirement",
 dek=("Two steps, both legal, both easy. Then a rule almost nobody mentions "
      "reaches back across every traditional, SEP and SIMPLE IRA you own and "
      "makes most of the conversion taxable &mdash; and it measures on a date you "
      "will not think about."),
 dek_plain=("Two steps, both legal, both easy. Then a rule almost nobody mentions "
            "reaches back across every traditional, SEP and SIMPLE IRA you own and "
            "makes most of the conversion taxable - and it measures on a date you will "
            "not think about."),
 figure=("11%", "of one therapist&rsquo;s conversion that came out tax-free"),
 tool=("therapist-tax-strategy-california.html",
       "See what the conversion actually costs you, with your own balances",
       "The tax page asks for your pre-tax IRA balance and prorates the conversion "
       "properly rather than assuming the balance is zero. That one field is the "
       "difference between a tax-free move and a four-figure bill."),
 sections=[
  ("Why the back door exists at all", [
   ("p", "A Roth IRA is the account most therapists want and many are not allowed "
         "to have. You put in money already taxed, it grows, and nothing is taxed "
         "on the way out. The catch is an income limit, and a private practice "
         "that is going well crosses it."),
   ("p", "For 2026 the ability to contribute directly phases out between "
         "<b>$153,000 and $168,000</b> of modified adjusted gross income if you "
         "file single or head of household, and between <b>$242,000 and "
         "$252,000</b> filing jointly. Filing separately it phases out between $0 "
         "and $10,000, which is a polite way of saying no."
         "<sup><a href=\"#s1\">[1]</a></sup>"),
   ("p", "The back door is the workaround, and it is two steps:"),
   ("ul", ["Contribute to a <b>traditional</b> IRA and take no deduction. There is "
           "no income limit on a non-deductible contribution. For 2026 that is "
           "<b>$7,500</b>, or $8,600 from age 50."
           "<sup><a href=\"#s1\">[1]</a></sup>",
           "<b>Convert</b> it to a Roth. There is no income limit on a conversion "
           "either."]),
   ("p", "Money you were not allowed to put in the front door is now inside. "
         "Nothing about this is aggressive or obscure; it is the ordinary "
         "interaction of two rules."),
  ]),

  ("The rule that reaches back", [
   ("p", "Here is where it goes wrong, and it goes wrong quietly, months later, "
         "on a form."),
   ("p", "The tax code does not see your IRAs as separate accounts. For working "
         "out what a distribution or conversion costs, <b>every traditional, SEP "
         "and SIMPLE IRA you own is treated as one pot</b>. You cannot convert the "
         "clean $7,500 and leave the old money alone, because as far as the "
         "arithmetic is concerned there is no clean $7,500 &mdash; there is one "
         "balance, part after-tax and part before, and anything you take out comes "
         "out in that proportion.<sup><a href=\"#s3\">[3]</a></sup>"),
   ("p", "Form 8606 is where this becomes concrete. Line 6 asks for:"),
   ("quote", "&ldquo;the total value of all your traditional IRAs as of December "
             "31&hellip;, plus any outstanding rollovers.&rdquo;",
    "Instructions for Form 8606 &mdash; see source [2]"),
   ("p", "Two things in that sentence cost money.<sup><a href=\"#s2\">[2]</a></sup> "
         "<b>All</b> &mdash; traditional, "
         "SEP and SIMPLE together. And <b>December 31</b> &mdash; not the day you "
         "converted, not the day you contributed. The year&rsquo;s closing balance "
         "is the denominator, whatever the account looked like in March."),
  ]),

  ("What it costs, on real numbers", [
   ("p", "A therapist contributes <b>$7,500</b> non-deductible and converts it the "
         "same week. Clean, textbook, no tax expected. She also has a "
         "<b>$60,000</b> traditional IRA from a job she left in 2014 and has not "
         "thought about since."),
   ("p", "The tax-free share of the conversion is her after-tax basis over "
         "everything: $7,500 &divide; ($60,000 + $7,500)."),
   ("pull", "11%", "of the conversion came out tax-free. The rest was taxable."),
   ("p", "So <b>$6,667</b> of the $7,500 is taxable income. At a 24% federal and "
         "9.3% California marginal rate that is about <b>$2,220</b> in tax on a "
         "move she was told was tax-free."),
   ("p", "The remaining <b>$833</b> of basis does not vanish &mdash; it carries "
         "forward on Form 8606 and comes out tax-free eventually. But &ldquo;you "
         "get it back over the next twenty years&rdquo; is a poor answer to a "
         "bill due in April."),
  ]),

  ("The escape hatch, and its deadline", [
   ("p", "The denominator counts IRAs. It does <b>not</b> count employer plans. A "
         "401(k) balance is invisible to line 6."),
   ("p", "Which gives the fix its shape: if you have a solo 401(k) &mdash; and a "
         "therapist with self-employment income can open one &mdash; and the plan "
         "accepts incoming rollovers, moving the old pre-tax IRA into it empties "
         "the pot. Denominator zero, conversion fully tax-free."),
   ("p", "The deadline is the part people miss. It is not &ldquo;before you "
         "convert&rdquo;. It is <b>before 31 December of the year you convert</b>, "
         "because that is the date line 6 measures. A conversion in March and a "
         "rollover in November still work. A conversion in March and a rollover "
         "next February do not."),
   ("p", "The same date runs in the other direction, which is the trap nobody "
         "warns about. Do a clean backdoor Roth in March with no IRA balance at "
         "all, then open a <b>SEP-IRA</b> in November because an accountant "
         "suggested it, and you have retroactively made March taxable. The SEP "
         "counts. It was not there when you converted and it does not matter."),
  ]),

  ("What this page is not telling you", [
   ("p", "Whether to do it at all. The back door is worth the trouble when you "
         "expect your retirement tax rate to be at or above today&rsquo;s, and it "
         "is a wash or worse when you do not &mdash; and that is a forecast rather "
         "than a calculation."),
   ("p", "Nor is it the biggest lever available to a self-employed therapist. "
         "$7,500 into a Roth is a good habit; a solo 401(k) takes "
         "<b>$24,500</b> of salary deferral in 2026 before any employer "
         "contribution, and it is the account that actually moves a tax bill."
         "<sup><a href=\"#s1\">[1]</a></sup> The back door is a supplement to "
         "that, not a substitute for it."),
   ("p", "And this is the point in an article where you would normally be told to "
         "consult a professional. Do &mdash; but go in knowing the one question "
         "that decides your answer: <b>what is the total balance of every "
         "traditional, SEP and SIMPLE IRA in your name?</b> If it is not zero, the "
         "clean version of this manoeuvre is not available to you until it is."),
  ]),
 ],
 sources=[
  (1, "IRS &mdash; 401(k) limit increases to $24,500 for 2026, IRA limit "
      "increases to $7,500",
   "https://www.irs.gov/newsroom/401k-limit-increases-to-24500-for-2026-ira-limit-increases-to-7500",
   "the 2026 IRA limit and catch-up, the 401(k) deferral limit, and the Roth "
   "phase-out ranges for each filing status"),
  (2, "IRS &mdash; Instructions for Form 8606, Nondeductible IRAs",
   "https://www.irs.gov/instructions/i8606",
   "line 6: the total value of all traditional IRAs as of 31 December plus "
   "outstanding rollovers, with SEP and SIMPLE IRAs included and employer plans "
   "excluded"),
  (3, "26 U.S. Code &sect;408(d)(2) &mdash; special rules applying section 72",
   "https://www.law.cornell.edu/uscode/text/26/408",
   "the aggregation rule itself: all individual retirement plans treated as one "
   "contract and all distributions in a year as one distribution"),
 ],
),

]
