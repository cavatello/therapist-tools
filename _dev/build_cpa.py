#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The accountant meeting: what to settle first, and what to ask.

TIER 3 EDITORIAL #1e, and the cheapest of the five in the brief because it
depends on nothing external - no legislature, no vendor, no dated dataset.

WHAT THIS PAGE IS FOR, AND WHY IT IS NOT ANOTHER TAX PAGE

This site already carries ten pages of California therapist tax content:
the entity question, the incorporation floor, S-corp salary and its Social
Security cost, California payroll on top of it, the estimated-tax shape,
deductions, the home office, the three retirement plans, the backdoor Roth
pro-rata trap, and the whole strategy priced end to end. All of it is
already written and all of it is already sourced.

So the gap is not another explanation. It is the HOUR ITSELF. A therapist
books an accountant, and spends the first half of a billed hour being told
what is on those ten pages. This page is the preparation that stops that
happening: what to know before you sit down, what to ask, and the answers
that tell you the person across the table has never had a California
licensed therapist as a client.

THE NO-NEW-NUMBERS RULE, INHERITED FROM build_viable.py

Every figure carried from this site is credited to the page that computes
it, and a guard reads that page to confirm it is still there. This page
introduces NO figures of its own about tax outcomes. The only new numbers
here are about PREPARERS - the bond, the training hours, the representation
rights - and each of those comes from the FTB, CTEC or the IRS, cited.

THE ONE THING THIS PAGE ASSERTS THAT THE OTHERS DO NOT

That the credential matters, and that most people do not know there is a
credential to check. In California, anyone who prepares returns for a fee
must register with CTEC unless they are a CPA, an enrolled agent, a State
Bar attorney or a specified banking or trust official. And in an audit,
only the first three of those can represent you without limit. A preparer
holding nothing but a PTIN cannot represent you at all. That is a real,
checkable, consequential difference and no therapy-facing page states it.

NO PRICES. Fee ranges for accountants could not be sourced to anything
primary, and a made-up range on a page whose whole promise is traceability
would be the worst kind of small lie. The page says what drives the fee and
what to ask about it instead. A guard fails the build if a dollar-an-hour
figure ever appears.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "questions-to-ask-a-cpa-california-therapist.html"
DONOR = "bbs-advertising-rules-2026.html"

READ = "18 August 2026"

# ------------------------------------------------ pages this one stands on
LLC = "therapist-llc-california.html"
INC = "cost-of-incorporating-california-therapist.html"
SALARY = "s-corp-salary-social-security-therapist.html"
SDI = "s-corp-sdi-california-therapist.html"
EST = "quarterly-estimated-taxes-california-therapist.html"
DEDUCT = "therapist-tax-deductions-california.html"
HOME = "home-office-deduction-california-therapist.html"
RETIRE = "solo-401k-sep-simple-california-therapist.html"
ROTH = "backdoor-roth-pro-rata-therapist.html"
STRAT = "therapist-tax-strategy-california.html"
HIRE = "hiring-first-associate-california-therapist.html"
BILLS = "superbills-good-faith-estimate-california-therapist.html"

# Every figure below is CARRIED, not computed here. The guard in main()
# opens each source page and fails the build if the figure has gone.
FIGURES = [("$800", INC), ("30/40/0/30", EST), ("1.3%", SDI),
           ("17701.04", LLC), ("$1,041", SALARY),
           ("$5 a square foot", HOME), ("14 sessions", HIRE)]

# Preparer credentials - the only facts this page introduces, read 18 Aug 2026.
FTB_CTEC = ("https://www.ftb.ca.gov/tax-pros/"
            "california-tax-education-council.html")
CTEC_FIND = "https://ctec.org/taxpayers/find-verify-preparer/"
IRS_CRED = ("https://www.irs.gov/tax-professionals/"
            "understanding-tax-return-preparer-credentials-and-qualifications")
IRS_PTIN = ("https://www.irs.gov/tax-professionals/"
            "ptin-requirements-for-tax-return-preparers")
IRS_DIR = ("https://www.irs.gov/tax-professionals/"
           "faqs-directory-of-federal-tax-return-preparers-with-credentials-"
           "and-select-qualifications")
DCA = "https://search.dca.ca.gov/"

JUMPS = [("credential", "Check the credential"),
         ("know", "Know this first"),
         ("ask", "What to ask"),
         ("wrong", "Wrong answers"),
         ("bring", "What to bring"),
         ("sources", "Sources")]


def plain(u, t):
    return '<a href="' + u + '">' + t + "</a>"


def sec(anchor, kicker, head):
    return ('<section class="pk-sec" id="' + anchor + '">'
            '<p class="pk-k">' + kicker + "</p>"
            '<h2 class="pk-h">' + head + "</h2>")


def p(html):
    return '<p class="pk-p">' + html + "</p>"


def h3(t):
    return '<h3 class="pk-h3">' + t + "</h3>"


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Before the meter starts &middot; checked " + READ,
        "Everything on this site that an accountant would otherwise "
        "charge you an hour to explain.",
        "A first meeting with an accountant goes one of two ways. Either "
        "you spend the first half of it being taught what is already "
        "written down, or you arrive knowing it and spend the whole hour "
        "on the parts that are actually about you. This page is the "
        "second version: what to settle before you book, what to ask, "
        "and the answers that mean this person has never had a "
        "California licensed therapist as a client.",
        [("3", "credentials that can represent you in an audit"),
         ("$5,000", "the bond a registered preparer must carry"),
         ("60", "hours of training before they may charge a fee"),
         ("1", "wrong answer that should end the interview")],
        JUMPS))

    # -------------------------------------------------------- credential
    o.append(sec("credential", "Start here, because almost nobody does",
                 "Not everyone who prepares tax returns for money is a "
                 "CPA, and the difference shows up in an audit."))
    o.append(p(
        "In California, anyone who prepares or assists in preparing tax "
        "returns <b>for a fee</b> has to register with the California "
        "Tax Education Council unless they are exempt. The exempt list "
        "is short: California CPAs, enrolled agents, attorneys who are "
        "members of the State Bar, and specified banking or trust "
        "officials. Everyone else must complete a <b>60-hour</b> "
        "qualifying course, carry a <b>$5,000</b> tax preparer bond, and "
        "renew each year with <b>20 hours</b> of continuing education "
        "&mdash; ten of federal tax law, three of federal update, two of "
        "ethics and <b>five of California tax law</b>."))
    o.append(p(
        "Separately, the IRS requires that &ldquo;anyone who prepares or "
        "assists in preparing federal tax returns for compensation must "
        "have a valid&rdquo; preparer tax identification number for the "
        "year. A PTIN is not a credential. It is a registration number, "
        "and on its own it carries almost no authority."))
    o.append(h3("What each one can do if the IRS comes back to you"))
    o.append(pk.table(
        ["Who they are", "What they can do for you before the IRS"],
        [[("Attorney, CPA, or enrolled agent", "f"),
          "<b>Unlimited representation.</b> Any matter &mdash; audits, "
          "payment and collection, appeals &mdash; whether or not they "
          "prepared the return."],
         [("Annual Filing Season Program", "f"),
          "<b>Limited.</b> Only returns they prepared and signed, and "
          "only before revenue agents, customer service representatives "
          "and similar staff. Not appeals. Not collection."],
         [("PTIN only, no credential", "f"),
          "<b>Effectively none.</b> They may prepare your return and "
          "cannot represent you on it, other than for returns prepared "
          "before 1 January 2016."]],
        caption="From the IRS&rsquo;s own description of preparer "
                "credentials, read " + READ + ". The distinction costs "
                "nothing on a quiet year and everything on a bad one."))
    o.append(pk.callout(
        "Two searches, four minutes, before you send anyone your books",
        ["A CPA license is on the same California license search you use "
         "for your own &mdash; the Department of Consumer Affairs covers "
         "Accountancy and Behavioral Sciences in one place, and shows "
         "whether a license is current, expired, suspended or revoked. "
         "A registered preparer who is not a CPA is on the Council&rsquo;s "
         "own register instead, and the IRS publishes a directory of "
         "credentialed preparers.",
         "Both links are in the sources below. Registrations expire and "
         "licenses get suspended, and neither event sends you a letter."]))
    o.append("</section>")

    # -------------------------------------------------------------- know
    o.append(sec("know", "Do not pay to be taught these",
                 "Nine things this site already answers, so you are not "
                 "buying them by the hour."))
    o.append(p(
        "None of this is advice about your situation, and an accountant "
        "who knows your numbers may tell you something different about "
        "any of it. The point is narrower: walk in already knowing the "
        "shape of the question, so the hour goes on your answer rather "
        "than on the background."))
    o.append(pk.numbered([
        ("1", "You cannot put a California therapy practice in an LLC.",
         "Not a preference &mdash; a statute. The choice is sole "
         "proprietorship or a California professional corporation, "
         "which may then elect S-corp treatment. "
         + plain(LLC, "The subsection that forbids it &rarr;")),
        ("2", "A professional corporation has an annual floor.",
         "It costs something every year whether or not it earns "
         "anything, and there is a first-year rule. Below a certain "
         "profit the structure costs more than it saves. "
         + plain(INC, "The floor, and where it starts paying &rarr;")),
        ("3", "A low S-corp salary is not free money.",
         "It buys a tax saving now and sells future Social Security to "
         "pay for it, and the trade can be priced rather than argued "
         "about. " + plain(SALARY, "What the trade actually costs "
                           "&rarr;")),
        ("4", "California payroll takes back part of the S-corp saving.",
         "The pitch is usually made in federal terms only. State "
         "employer costs are real and one of them has no wage cap. "
         + plain(SDI, "The costs the pitch omits &rarr;")),
        ("5", "California&rsquo;s estimated-tax year is not four equal "
         "quarters.",
         "The state schedule is front-loaded and does not match the "
         "federal one, which is the single most common way a first "
         "year in practice goes wrong. "
         + plain(EST, "Both schedules, and the safe harbour &rarr;")),
        ("6", "A deduction is worth your marginal rate, not its face "
         "value.",
         "Which is why &ldquo;write it off&rdquo; is not a plan. "
         + plain(DEDUCT, "What qualifies, and what it is worth &rarr;")
         + " &middot; " + plain(HOME, "The home office, both methods "
                                "&rarr;")),
        ("7", "There are three retirement plans and they are not close.",
         "At a given profit one of them takes far more than the others, "
         "and the right answer changes as the practice grows. "
         + plain(RETIRE, "The three, at three profit levels &rarr;")),
        ("8", "A backdoor Roth can be mostly taxable by accident.",
         "The pro-rata rule looks at every one of your traditional IRA "
         "balances, and the deadline is the end of December, not April. "
         + plain(ROTH, "Why yours was taxable &rarr;")),
        ("9", "Hiring an associate is a classification question before "
         "it is a cost question.",
         "And the cost question has a break-even caseload. "
         + plain(HIRE, "The loaded cost and the rule &rarr;")),
    ]))
    o.append(p(
        "If you want the whole thing priced end to end before you go in, "
        "that is " + plain(STRAT, "the tax strategy page") + ", which "
        "puts a number on how much of the bill is actually optional."))
    o.append("</section>")

    # --------------------------------------------------------------- ask
    o.append(sec("ask", "The hour itself",
                 "Questions worth an accountant&rsquo;s time, because "
                 "the answers depend on facts only they will have."))
    o.append(h3("Structure, and whether to change it"))
    o.append(pk.checklist("", [
        "At my profit, does a professional corporation clear its own "
        "annual cost, and by how much &mdash; after California payroll, "
        "not just the federal saving?",
        "If we incorporate, what does the first year cost in filings and "
        "fees that the second year does not?",
        "What salary would you set, how did you arrive at it, and what "
        "would you show if that figure were ever questioned?",
        "What happens to this if my income drops for a year &mdash; what "
        "does the structure cost me then, and how hard is it to undo?",
    ]))
    o.append(h3("The rhythm of the year"))
    o.append(pk.checklist("", [
        "What am I sending, to whom, and on what dates &mdash; federal "
        "and California, which are not the same schedule?",
        "Which safe harbour are you aiming me at, and what happens if I "
        "have a much better year than last year?",
        "Who actually presses send: you, or me? Say it out loud now, "
        "because this is the thing that gets assumed in both directions.",
        "If a notice arrives, what do you do and what does it cost? "
        "Their answer here is where the credential above stops being "
        "theoretical.",
    ]))
    o.append(h3("Retirement, which is where the real money is"))
    o.append(pk.checklist("", [
        "Given my profit and whether I have employees, which plan takes "
        "the most &mdash; and what is the deadline to open it, as "
        "opposed to the deadline to fund it?",
        "Do I have any traditional IRA balance anywhere that would make "
        "a backdoor Roth partly taxable, and what would you do about it "
        "before December?",
        "If I hire someone, which of these plans forces me to cover them "
        "too, and what does that cost per employee?",
    ]))
    o.append(h3("Records, and the part that is specific to this work"))
    o.append(pk.checklist("", [
        "What are you going to need from me that identifies my clients "
        "&mdash; and can we do this with figures rather than names?",
        "How do you receive and store documents? A superbill carries a "
        "client&rsquo;s name and a diagnosis code, and email is where "
        "that usually goes wrong.",
        "Who else at your firm sees my file, and are they bound the same "
        "way you are?",
        "If I am ever audited, what of mine gets handed over, and do I "
        "get to see it first?",
    ]))
    o.append(p(
        "That last group is not a tax question and a general accountant "
        "may never have been asked it. It is worth asking anyway: what "
        "you hand over is client material, and "
        + plain(BILLS, "what a superbill has to contain")
        + " is why. An accountant who takes the question seriously is "
        "telling you something useful about the rest of the "
        "relationship."))
    o.append("</section>")

    # ------------------------------------------------------------- wrong
    o.append(sec("wrong", "How to tell in ten minutes",
                 "Four answers that mean this person has not done this "
                 "for a California therapist."))
    o.append(pk.numbered([
        ("1", "&ldquo;Set up an LLC.&rdquo;",
         "This is the one that should end the interview, and it is the "
         "most common advice a therapist gets. A California-licensed "
         "marriage and family therapist, clinical social worker, "
         "professional clinical counselor or psychologist "
         "<b>cannot</b> form one to deliver licensed services. Someone "
         "who opens with it has confused your profession with a "
         "consultancy, and everything downstream of that assumption is "
         "also wrong. " + plain(LLC, "The statute &rarr;")),
        ("2", "A salary number with no reasoning attached.",
         "The figure matters less than whether they can say how they "
         "got there and what they would show if it were challenged. "
         "&ldquo;Everyone uses this&rdquo; is not a method."),
        ("3", "Four equal quarterly payments.",
         "That is the federal shape. California&rsquo;s is not, and a "
         "practice that pays evenly into the state has underpaid twice "
         "by June. " + plain(EST, "The two schedules &rarr;")),
        ("4", "An S-corp saving quoted in federal terms only.",
         "If the pitch has not mentioned California employer payroll, "
         "the number is bigger than the reality. Ask them to redo it "
         "with the state costs in. " + plain(SDI, "What they are "
                                             "&rarr;")),
    ]))
    o.append(pk.callout(
        "None of this makes a generalist a bad accountant",
        ["Most accountants have never had a licensed therapist as a "
         "client, and the entity rule genuinely is unusual &mdash; it "
         "surprises lawyers too. The point of the four above is not to "
         "catch anyone out. It is that you can find out in the first ten "
         "minutes whether you are the one who is going to have to teach "
         "them, and decide knowingly whether you mind."]))
    o.append("</section>")

    # ------------------------------------------------------------- bring
    o.append(sec("bring", "The practical part",
                 "What to have with you, and what to settle about the "
                 "fee."))
    o.append(pk.checklist("What to bring", [
        "Last year&rsquo;s returns, federal and California, and any "
        "notice you have received since.",
        "A profit figure for this year so far, and an honest guess at "
        "the full year. Everything above depends on it and nothing can "
        "be answered without it.",
        "Whether you have employees or contractors, and whether any of "
        "them is pre-licensed.",
        "Every retirement account you hold, including old ones you have "
        "stopped thinking about &mdash; that is what the pro-rata "
        "question turns on.",
        "Your license type and status, because the entity question "
        "depends on it.",
    ]))
    o.append(p(
        "On fees, ask how they charge and what changes the number "
        "&mdash; a return, payroll for a corporation, and answering a "
        "notice are three different pieces of work and are often priced "
        "separately. This page deliberately quotes no fee range: what "
        "accountants charge could not be traced to a primary source, and "
        "a plausible-looking made-up range would be worse than nothing "
        "on a page whose whole promise is that every figure comes from "
        "somewhere. Ask two or three, and compare what they said about "
        "the entity question while you are at it."))
    o.append("</section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("Who may prepare a return for a fee, and what they may do", [
            ("California Franchise Tax Board on the California Tax "
             "Education Council - who must register, who is exempt, the "
             "$5,000 bond, the 60-hour course and the 20 hours of "
             "continuing education", FTB_CTEC),
            ("The IRS on preparer credentials - unlimited representation "
             "for attorneys, CPAs and enrolled agents; limited for the "
             "Annual Filing Season Program; effectively none for a "
             "PTIN-only preparer", IRS_CRED),
            ("The IRS on who needs a PTIN", IRS_PTIN),
        ]),
        ("Where to check somebody before you hire them", [
            ("California Department of Consumer Affairs license search - "
             "Accountancy and Behavioral Sciences in one place, with "
             "license status and discipline", DCA),
            ("The Council's own register, for a preparer who is not a "
             "CPA, an enrolled agent or an attorney", CTEC_FIND),
            ("The IRS directory of federal tax return preparers with "
             "credentials and select qualifications", IRS_DIR),
        ]),
        ("The figures above, each on the page that computes it", [
            ("Why a California therapist cannot use an LLC, and the two "
             "structures left", LLC),
            ("What a professional corporation costs to run every year",
             INC),
            ("What a low S-corp salary costs in Social Security later",
             SALARY),
            ("The California employer payroll costs the S-corp pitch "
             "leaves out", SDI),
            ("The two estimated-tax schedules and the safe harbour",
             EST),
            ("What is deductible, and what a deduction is worth",
             DEDUCT),
            ("The home office, both methods", HOME),
            ("Solo 401(k), SEP and SIMPLE at three profit levels",
             RETIRE),
            ("The backdoor Roth pro-rata rule and the December "
             "deadline", ROTH),
            ("The whole tax bill priced, and how much of it is "
             "optional", STRAT),
            ("Hiring an associate: classification, loaded cost and "
             "break-even", HIRE),
            ("What a superbill and a Good Faith Estimate have to "
             "contain", BILLS),
        ]),
    ], note="The preparer rules above were read on " + READ + " from the "
            "Franchise Tax Board, the California Tax Education Council "
            "and the IRS, and the link beside each is the authority "
            "rather than this page. Every other figure on this page is "
            "carried from the page on this site that computes it, and "
            "introduces nothing new. This site earns nothing from any "
            "link here and does not recommend or receive anything from "
            "any accountant, firm or directory. Nothing here is tax or "
            "legal advice, and a question is not an answer - the whole "
            "point of the page is that the answers depend on facts only "
            "you and your accountant have.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Questions to ask a CPA: California therapists",
    "What to know before you meet an accountant, what to ask, and the "
    "answers that mean they have never had a California licensed "
    "therapist as a client.",
    "money", "guide",
    "What should I ask an accountant, and what should I already know?",
    "Nine things to settle before the meeting, the questions worth the "
    "hour, and four answers that should end the interview",
    "3 credentials that can represent you in an audit",
    weight=4)


def main():
    print("the accountant-meeting page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    path = os.path.join(SITE, PAGE)
    open(path, "w", encoding="utf-8").write(html)
    print("  wrote " + PAGE + ", " + format(len(html), ",d")
          + " bytes, " + str(nsrc) + " sources")

    bad = 0
    # ---- NO NEW NUMBERS. Every carried figure must still be on its page.
    for fig, src_page in FIGURES:
        s = re.sub(r"\s+", " ",
                   open(os.path.join(SITE, src_page),
                        encoding="utf-8").read())
        if fig not in s:
            print("GUARD: \"" + fig + "\" is credited to " + src_page
                  + ", which no longer contains it")
            bad += 1

    n = pk.check_page(path, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        # The credential facts, which are the only ones this page owns.
        ("the CTEC bond", "$5,000"),
        ("the qualifying course", "60-hour"),
        ("the continuing education", "20 hours"),
        ("the California tax law hours", "five of California tax law"),
        ("the unlimited-representation tier", "Unlimited representation"),
        ("the PTIN limit", "1 January 2016"),
        ("the FTB source", "california-tax-education-council"),
        ("the IRS credentials source", "understanding-tax-return-preparer"),
        ("the license search", "search.dca.ca.gov"),
        # Every page it stands on must actually be linked.
        ("the LLC page", LLC),
        ("the incorporation page", INC),
        ("the salary page", SALARY),
        ("the SDI page", SDI),
        ("the estimated-tax page", EST),
        ("the deductions page", DEDUCT),
        ("the home-office page", HOME),
        ("the retirement page", RETIRE),
        ("the backdoor-Roth page", ROTH),
        ("the strategy page", STRAT),
        ("the hiring page", HIRE),
        ("the superbill page", BILLS),
        # The screening question that gives the page its point.
        ("the LLC wrong answer", "Set up an LLC"),
    ], [h for h, _ in JUMPS])

    s = open(path, encoding="utf-8").read()
    art = pk.article(s)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # ---- NO INVENTED FEES. The page says why it quotes none; if a rate
    # ever appears, either it has a source or this guard is doing its job.
    for pattern, why in ((r"\$\s?\d[\d,]*\s*(?:an|per|/)\s*hour",
                          "an hourly rate"),
                         (r"\$\s?\d[\d,]*\s*(?:to|-|&ndash;)\s*\$\s?\d",
                          "a fee range")):
        m = re.search(pattern, flat)
        if m and "$5,000" not in m.group(0):
            print("GUARD: " + why + " (\"" + m.group(0).strip()
                  + "\") appeared on a page that states it quotes none. "
                  "Either cite a primary source for it and update this "
                  "guard, or take it out.")
            bad += 1

    # ---- The LLC rule is the page's screening question and the site's
    # standing legal correction. It must survive as a PROHIBITION.
    if "cannot form one" not in flat:
        print("GUARD: the page no longer says a California licensee "
              "cannot form an LLC - which is the one answer it exists to "
              "tell a reader to walk away from")
        bad += 1

    # ---- the standing site guards
    for track in ("?ref=", "&ref=", "?aff", "&aff", "utm_", "?tap_",
                  "impact.com", "shareasale", "partnerize", "?a_aid",
                  "clickbank", "?pa=", "avantlink"):
        if track in art:
            print("GUARD: links must stay plain - found \"" + track + "\"")
            bad += 1
    if "earns nothing" not in flat:
        print("GUARD: the page no longer states that the site earns "
              "nothing from these links")
        bad += 1
    for wrong in ("we found that", "our testing shows", "the best course",
                  "we recommend buying"):
        if wrong in flat:
            print("GUARD: \"" + wrong + "\" reads as an endorsement")
            bad += 1
    for phrase in ("is hiring", "has openings", "guaranteed",
                   "accepting new"):
        if phrase in flat:
            print("GUARD: banned phrase \"" + phrase + "\" in the article")
            bad += 1

    # ---- the meta description ceiling in seo_rules
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    dlen = len(desc.group(1)) if desc else 0
    if not 70 <= dlen <= 168:
        print("GUARD: the meta description is " + str(dlen)
              + " characters; seo_rules wants 70 to 168")
        bad += 1

    if n or bad:
        sys.exit(str(n + bad) + " check failure(s)")
    print("  checks passed - " + str(len(FIGURES)) + " carried figures "
          "verified on their own pages, 12 pages linked, no fee quoted, "
          "description " + str(dlen) + " chars, " + str(nsrc) + " sources")


if __name__ == "__main__":
    main()
