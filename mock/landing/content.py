# -*- coding: utf-8 -*-
"""Copy for the landing page.

The brief, verbatim: "It must be an actual landing page, home page to help MFT
in California understand the website, tools and support for MFTs. So should not
jump into things, do a good job making sure well communicated purpose of site,
then go into various tools."

So the order is: who this is for -> why it exists -> what you can do here ->
how it works -> who made it. The calculator does not appear until the reader has
been told what they are looking at, and it is a link rather than a live field.

Every figure below is engine output on the site's own worked example
($200/hr, 25 sessions, 50 weeks, the twelve STARTER running costs, filing
single): gross $250,000, running costs $42,574, profit $213,906, tax $69,061,
take-home $138,365.
"""

SIM = "practice-simulator.html"
TAX = "therapist-tax-strategy-california.html"
GROW = "grow-your-therapy-practice.html"
AMFT = "associate-mft-job-advisor.html"
HRS = "amft-3000-hours-california.html"
COLA = "therapist-cost-of-living-california.html"
RATES = "rates.html"
TOOLS = "tools.html"
ABOUT = "about.html"
NEWS = "newsletter.html"
CONTACT = "contact.html"

SITE_NAME = "Therapist Support"

# --- the hero -------------------------------------------------------------
HERO = dict(
    eyebrow="For California-licensed therapists",
    h1="The money side of a therapy practice, worked out in the open.",
    lede="Free tools and plain-language research for California LMFTs, LCSWs, "
         "LPCCs and psychologists — built by someone doing the same work, for "
         "the questions nobody covers in graduate school.",
    cta="See what the tools do",
    cta2="Start with the simulator",
)

# --- why this exists: the ANSWER GRID -------------------------------------
# Was three paragraphs about the author's motive. The reader does not arrive
# caring who made this; they arrive with a question. So the slot now carries
# four of the real ones, each routed to the tool that answers it. Only the one
# genuinely useful sentence of the old prose survives, as the lede.
WHY_H = "Four questions nobody covered in grad school."
WHY_LEDE = ("The answers exist. They are scattered across accountants who charge by the "
            "hour, forum threads written by people guessing, and blog posts that stop "
            "exactly where the arithmetic starts &mdash; and almost none of it is "
            "specific to California, which is where most of the difference is.")
ANSWERS = [
    ("Should I incorporate, or stay a sole proprietor?",
     "A California therapist may not form an LLC. The real choice is sole proprietor or "
     "a professional corporation with an S-corp election, and it is worth a five-figure "
     "swing either way.",
     "Tax &amp; retirement strategy", TAX),
    ("What is this associate job actually paying me?",
     "Flat rate, share of the fee, or salary &mdash; priced against the unpaid admin and "
     "the supervision you have to sit in either way.",
     "AMFT job advisor", AMFT),
    ("How long until I am licensed?",
     "Four requirements close at different speeds, and the 3,000 hours is almost never "
     "the one that decides your date.",
     "3,000 hours calculator", HRS),
    ("Can I afford to live here on this?",
     "Housing, transport and food by area, your student loan on RAP or the standard "
     "plan, and what is left over for savings.",
     "Cost of living", COLA),
]

# --- the three promises ---------------------------------------------------
PROMISES = [
    dict(k="compute", title="It computes, it doesn't opine",
         body="Every dollar on this site is the output of a calculation you can "
              "follow, run on numbers you typed in. There are no illustrative "
              "figures and no worked examples standing in for your practice."),
    dict(k="ca", title="California specifically",
         body="Not a national calculator with a state dropdown. California has "
              "its own income tax schedule, its own franchise tax, and its own "
              "rule that a licensed therapist may not form an LLC — all of which "
              "change the answer."),
    dict(k="open", title="Nothing saved, nothing sold",
         body="No account, no email required, nothing stored on a server. Your "
              "numbers live in the page and in a link you can copy. There is no "
              "paid tier and nothing here is trying to sell you a service."),
]

# --- who it's for ---------------------------------------------------------
AUDIENCE_H = "Who this is for"
AUDIENCE = [
    dict(k="assoc", label="Registered associates",
         body="AMFTs, ASWs and APCCs weighing up a placement and counting toward "
              "3,000 hours.",
         href=AMFT, cta="Start with the Job Advisor"),
    dict(k="solo", label="Solo private practice",
         body="Licensed, seeing your own clients, and trying to work out what the "
              "practice actually pays you.",
         href=SIM, cta="Start with the simulator"),
    dict(k="growing", label="Practices with room to grow",
         body="Deciding whether to incorporate, employ associates, raise rates, or "
              "fill the week.",
         href=TAX, cta="Start with tax strategy"),
]

# --- the tools ------------------------------------------------------------
TOOLS_H = "What you can do here"
TOOLS_LEDE = ("Four tools and a research library. Each one answers a single "
              "question, and each one shows its working.")

TOOL_BLOCKS = [
    dict(k="sim", href=SIM, tag="The main tool",
         q="What does my practice actually pay me?",
         title="Practice Simulator",
         body="Your session rate and caseload, twelve categories of running cost, "
              "self-employment tax and California income tax — ending in one "
              "number: what reaches your bank account.",
         stat=("$138,365", "take-home on a $250,000 practice"),
         bullets=["Twelve expense categories, itemised",
                  "Self-employment tax worked, not estimated",
                  "Employing associates, with employer payroll tax split six ways",
                  "Shareable by link, nothing saved"]),
    dict(k="tax", href=TAX, tag="Once a year",
         q="Sole proprietor, or a professional corporation?",
         title="Tax & Retirement Strategy",
         body="How much of your tax bill is optional. Solo 401(k), SEP and SIMPLE "
              "priced against your own profit, then both entity structures side "
              "by side with the Social Security cost included.",
         stat=("$69,061", "tax on that same practice"),
         bullets=[]),
    dict(k="amft", href=AMFT, tag="Pre-licensed",
         q="Is this associate job worth taking?",
         title="Associate Job Advisor",
         body="Flat rate per clinical hour, a share of the fee, or salary — what "
              "one placement really pays once unpaid admin and supervision are "
              "counted, and how long 3,000 hours takes at that caseload.",
         stat=("3,000", "hours, priced in weeks"),
         bullets=[]),
    dict(k="grow", href=GROW, tag="When you have room",
         q="Where do my next ten clients come from?",
         title="Grow Your Practice",
         body="What one client is worth over their whole time with you, which "
              "channels actually convert, and how many enquiries a month you need "
              "just to stand still against churn.",
         stat=("24", "clients, and what each is worth"),
         bullets=[]),
]

READING_H = "And things worth reading once"
READING = [
    dict(href=RATES, title="The California Therapy Rate Gap",
         body="What insurance panels reimburse against what private pay supports, "
              "region by region, and the size of the gap between them."),
    dict(href=TAX + "#remote", title="Curious about working remotely?",
         body="The same practice run from eight places — and the Board's own "
              "answer on whether you may see California clients from abroad."),
]

# --- how it works ---------------------------------------------------------
HOW_H = "How it works"
HOW = [
    ("Nothing is saved", "No account, no sign-up, no server. What you type stays "
     "in the page. Close the tab and it is gone."),
    ("Your numbers travel in a link", "Every tool writes your setup into the URL, "
     "so you can send it to your accountant, your supervisor, or yourself later."),
    ("The tools hand off to each other", "Fill in your practice once and the tax "
     "page picks up the same figures — expense category by expense category."),
    ("Every claim is cited", "Statutes, IRS schedules and Board publications are "
     "linked to the source, not paraphrased. Where something is a convention "
     "rather than a rule, it says so."),
]

# --- about ----------------------------------------------------------------
ABOUT_H = "Who makes this"
ABOUT_BODY = ("One person, working in California, building the tools they wanted "
              "and could not find. It is free because the arithmetic should be, "
              "and because the alternative — guessing — is expensive.")
ABOUT_NOTE = ("None of this is tax, legal or financial advice, and it is not a "
              "substitute for an accountant who knows your situation. It is the "
              "arithmetic, done properly, so that the conversation with them "
              "starts further along.")

# ==========================================================================
# What Help Scout actually does, and what is worth taking
#
# Fetched and read rather than recalled. Five patterns worth stealing:
#
# 1. NO SECTION IS A DEAD END. Every block routes somewhere deeper. They have
#    no "here are our features" list - they have feature sections that each
#    hand you to a page.
# 2. A NAMED HUB WITH A PROMISE. "Support Toolkit — explore our collection of
#    free templates, guides, courses, and resources." The name makes it a
#    destination; the sentence tells you the whole shape of it in one line.
# 3. A CATEGORY LABEL ON EVERY CARD. Cheap metadata that makes a grid scannable
#    and tells you what KIND of thing it is before you click.
# 4. THE BINARY CTA, REPEATED. Primary plus secondary, in the hero, again
#    mid-page, again in the prefooter. Same pair, three times.
# 5. MIXED FORMATS IN ONE HUB. Calculators next to guides next to templates,
#    grouped by type rather than by topic.
#
# What NOT to take: their whole page is a funnel toward a trial, and every
# escalation serves that. This site is not selling anything, so the escalation
# runs use a tool -> read the thinking -> stay updated. Copying their urgency
# without their business model just makes a free site look like it wants
# something.
# ==========================================================================

# Category labels. One word wherever possible - the point is scanning.
KIND = {"tool": "Tool", "notes": "Field notes", "ref": "Reference", "guide": "Guide"}

# Every tool block ends by promoting the piece of reading that pairs with it.
# This is pattern 1: a reader who finishes a tool is the most likely person in
# the world to read the article about the same subject.
PAIRS = {
    "sim":  ("notes", "The California Therapy Rate Gap",
             "What insurance panels pay against what private pay supports.", RATES),
    "tax":  ("notes", "Curious about working remotely?",
             "The same practice run from eight places, and the Board&rsquo;s own answer "
             "on seeing California clients from abroad.", TAX + "#remote"),
    "amft": ("ref", "What the Board actually requires",
             "Units of supervision, the four gates, and the one that usually binds.",
             AMFT + "#rules"),
    "grow": ("tool", "Practice Simulator",
             "Growth only matters if the practice pays you. Start from the profit.", SIM),
}

# Section kickers - the "all of it" link beside every heading.
KICKERS = {
    "audience": ("All free tools", TOOLS),
    "tools": ("The whole toolkit", TOOLS),
    "reading": ("Everything written here", RATES),
}

# The mid-page band. Help Scout repeats the same binary CTA three times; this is
# the second of the three.
MID = dict(
    eyebrow="Not sure where to start",
    h="Most people start with one number: what the practice actually pays them.",
    body="Everything else on this site is downstream of it. Put a rate and a caseload "
         "in, and the tax page, the growth page and the eight-location comparison all "
         "pick up the same figures.",
    cta="Open the practice simulator", cta2="Or see all four tools",
)

# The named hub, taken straight from the Support Toolkit pattern. The resources
# page does not exist yet - this block is what it will be introduced by, and
# until it ships the link points at the tools index.
TOOLKIT = dict(
    name="The California Therapist Toolkit",
    promise="A growing collection of free calculators, research and plain-English "
            "reference \u2014 for practicum students, registered associates and "
            "licensed therapists working in California.",
    items=[("Calculators", "Four, all free, none of them ask for an email"),
           ("Research", "Rates, reimbursement and what the market actually pays"),
           ("Reference", "Board rules, statutes and tax schedules, linked to source"),
           ("Templates", "Coming: the sheets and letters people keep asking for")],
    href=TOOLS,
)
