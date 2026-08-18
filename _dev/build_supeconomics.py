#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What it costs and pays to BE a supervisor, which is two different questions.

TIER 3 EDITORIAL #1b, and the last of the five. This site already has
`finding-a-clinical-supervisor-california.html` - the SUPERVISEE's side of
the arrangement. Nothing existed on the other side of the table.

THE FRAME, WHICH IS THE POINT OF THE PAGE

"Should I supervise?" is not one question, it is two, and they have almost
nothing in common:

  A. Supervising somebody else's employee, for a fee. An hourly
     arrangement, with a training bill in front of it and real liability
     attached to it. The economics are the economics of a side income.
  B. Employing an associate inside your own practice. Not a side income
     at all - a hiring decision, because section 4980.43.3 says an
     associate "shall only perform mental health and related services as
     an employee or volunteer, and not as an independent contractor."
     Payroll, workers' compensation, a caseload to fill.

Most writing on this subject silently mixes the two, quotes an hourly rate
that belongs to (A), and leaves the reader with a number that means
nothing for the thing they were actually considering. This site already
prices (B) properly on the hiring page, with a loaded cost and a
break-even caseload. So this page's job is to separate the two, price what
can be priced, and hand each half to the page that already answers it.

WHAT IT DELIBERATELY DOES NOT DO: QUOTE A GOING RATE

No primary source publishes what California supervisors charge. There are
survey figures and forum numbers and none of them is traceable, and this
site's whole promise is that every figure traces to a source page. So the
page states the costs that ARE knowable - fifteen hours of training before
you start, six every renewal period after - explains what drives a fee,
and refuses to invent the fee itself. A guard fails the build if an hourly
rate for supervision ever appears.

WHAT WAS ALREADY BANKED, AND WHAT IS NEW

The two parallel two-year eligibility tests were established in
`claude/trainee-tier-design-and-university-channel.md` section 5 and are
used here. The training hours (16 CCR 1821.3) and the employment rule
(BPC 4980.43.3) were verified for this page.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "becoming-a-clinical-supervisor-california.html"
DONOR = "bbs-advertising-rules-2026.html"

READ = "18 August 2026"

FINDSUP = "finding-a-clinical-supervisor-california.html"
HIRE = "hiring-first-associate-california-therapist.html"
GETHIRED = "getting-hired-as-a-california-associate.html"
UNPAID = "associate-unpaid-hours-california.html"
INS = "therapy-liability-insurance-california.html"
CASES = "therapist-discipline-cases-california.html"
HOURS = "amft-3000-hours-california.html"
CE = "continuing-education-california-lmft.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"

FIGURES = [("14 sessions", HIRE), ("most commonly reported use", INS)]


def leg(code, section):
    return ("https://leginfo.legislature.ca.gov/faces/"
            "codes_displaySection.xhtml?lawCode=" + code
            + "&sectionNum=" + section + ".")


BPC4980_03 = leg("BPC", "4980.03")
BPC4980_43_3 = leg("BPC", "4980.43.3")
CCR1821_3 = "https://www.law.cornell.edu/regulations/california/16-CCR-1821.3"
F4980_43_3 = ("https://codes.findlaw.com/ca/business-and-professions-code/"
              "bpc-sect-4980-43-3/")
BBSSUP = "https://www.bbs.ca.gov/pdf/forms/supervision_agreement.pdf"

JUMPS = [("two", "Two different questions"),
         ("qualify", "Whether you qualify"),
         ("cost", "What it costs to start"),
         ("liability", "What you take on"),
         ("fee", "What it pays"),
         ("sources", "Sources")]


def plain(u, t):
    return '<a href="' + u + '">' + t + "</a>"


def sec(anchor, kicker, head):
    return ('<section class="pk-sec" id="' + anchor + '">'
            '<p class="pk-k">' + kicker + "</p>"
            '<h2 class="pk-h">' + head + "</h2>")


def p(html):
    return '<p class="pk-p">' + html + "</p>"


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "The other side of the table &middot; checked " + READ,
        "Supervising for a fee and employing an associate are not the "
        "same decision.",
        "This site has always covered how to find a supervisor. This is "
        "the reverse: what it takes to become one, what it costs before "
        "you earn anything, what you are on the hook for afterwards, and "
        "why the two versions of this arrangement have completely "
        "different economics. One is an hourly side income. The other is "
        "payroll.",
        [("15", "hours of training before you supervise at all"),
         ("6", "more hours every renewal period after that"),
         ("2", "separate two-year tests, and people check one"),
         ("0", "published rates this page is willing to quote")],
        JUMPS))

    # --------------------------------------------------------------- two
    o.append(sec("two", "Start here or the numbers are meaningless",
                 "&ldquo;Should I supervise?&rdquo; is two questions "
                 "wearing one coat."))
    o.append(pk.table(
        ["", "Supervising for a fee",
         "Employing an associate in your practice"],
        [["What it is", "An hourly arrangement with somebody else&rsquo;s "
          "employee or volunteer",
          "A hiring decision, with payroll attached"],
         ["Who pays whom", "The supervisee, or their employer, pays you",
          "You pay them"],
         ["The employment rule", "Their employer&rsquo;s problem",
          ("Yours &mdash; an associate must be an employee, never a "
           "contractor", "f")],
         ["What decides whether it works",
          "Your hourly fee against your time and risk",
          "Whether the caseload fills"],
         ["Where this site prices it",
          "Below, as far as anything can be priced",
          "On the hiring page, with a break-even at 14 sessions a week"]],
        caption="The two are routinely written about as one subject, "
                "which is how people end up applying an hourly rate to a "
                "payroll decision.", minw=620))
    o.append(p(
        "If what you are considering is the second one &mdash; taking on "
        "an associate inside your own practice &mdash; the arithmetic "
        "already exists on "
        + plain(HIRE, "the hiring page") + ": the loaded cost, the "
        "break-even caseload, and the classification rule. Read that "
        "one. This page is mostly about the first, plus everything both "
        "have in common."))
    o.append("</section>")

    # ------------------------------------------------------------ qualify
    o.append(sec("qualify", "Eligibility",
                 "Two separate two-year tests, and almost everybody "
                 "checks only the first."))
    o.append(p(
        "Section 4980.03(g) sets out who may supervise. The part worth "
        "slowing down on is that the first two conditions look like one "
        "condition and are not:"))
    o.append(pk.numbered([
        ("1", "An active license for at least two of the last five years",
         "The one everybody knows, and the one a directory listing "
         "implies."),
        ("2", "And, separately: two of the last five years actually "
         "practicing psychotherapy or providing clinical supervision",
         "A second, independent test. A licensee who has held the "
         "license continuously but spent the last three years teaching, "
         "administering or on leave can satisfy the first and fail this "
         "one. It is almost never checked, by either side."),
        ("3", "Supervision training",
         "Covered in full below &mdash; it is the real entry cost."),
        ("4", "Never the supervisee&rsquo;s own therapist",
         "Not now and not previously."),
        ("5", "Not suspended, and not on probation",
         "For a period specified by the Board."),
        ("6", "Not a relative, spouse, partner or in a business "
         "relationship with the supervisee",
         "The conflict rules are broader than people assume."),
    ]))
    o.append(pk.callout(
        "The test nobody runs, in both directions",
        ["A supervisee whose supervisor turns out not to have qualified "
         "does not get those hours back. That risk sits on the person "
         "with the least power in the arrangement and the least ability "
         "to check &mdash; which is why the supervisee&rsquo;s side of "
         "this is written up separately on "
         + plain(FINDSUP, "the finding-a-supervisor page") + ", and why "
         "the second test above is worth being able to answer about "
         "yourself before anyone asks."]))
    o.append("</section>")

    # -------------------------------------------------------------- cost
    o.append(sec("cost", "What it costs before you earn anything",
                 "Fifteen hours, then six more every renewal period, "
                 "for as long as you keep supervising."))
    o.append(p(
        "The training requirement is in regulation rather than statute "
        "&mdash; 16 CCR section 1821.3. &ldquo;Licensees who commence "
        "supervision for the first time in California shall obtain "
        "<b>fifteen (15) hours</b> in supervision training or "
        "coursework&rdquo;, and thereafter &ldquo;supervisors shall "
        "complete a minimum of <b>six (6) hours</b> of continuing "
        "professional development in supervision during each subsequent "
        "renewal period while providing supervision&rdquo;."))
    o.append(p(
        "The content is specified too: competencies for new supervisors, "
        "goal setting and evaluation, the supervisor and supervisee "
        "relationship, California law and ethics, cultural and "
        "contextual variables, supervision theories, and documentation. "
        "The six ongoing hours can be met in more ways than a course "
        "&mdash; teaching a supervision course, publishing research on "
        "supervision, mentoring with other supervisors, or attending a "
        "peer discussion group all count."))
    o.append(p(
        "Two things follow. The fifteen hours are a real barrier to "
        "entry, paid before the first hour is billed. And the six hours "
        "are an <b>ongoing</b> cost that runs for as long as you "
        "supervise, alongside the continuing education you already owe "
        "for the license itself &mdash; that separate obligation is on "
        + plain(CE, "the continuing education page") + ". This page "
        "does not price either, because course prices come from vendors "
        "rather than from any authority, and are not the same thing as "
        "a rule."))
    o.append(p(
        "There is paperwork as well. The supervision relationship is "
        "documented on the Board&rsquo;s own Supervision Agreement, and "
        "the deadline for it is short &mdash; the requirements for the "
        "supervisee&rsquo;s side of that, including which logs have to "
        "be kept separately, are on "
        + plain(HOURS, "the 3,000-hours page") + "."))
    o.append("</section>")

    # --------------------------------------------------------- liability
    o.append(sec("liability", "What you are actually taking on",
                 "The clinical work becomes yours to answer for."))
    o.append(p(
        "This is the part that does not appear in any fee calculation "
        "and should dominate it. When you supervise, another "
        "clinician&rsquo;s decisions about real clients sit under your "
        "license. The Board&rsquo;s interest in a case does not stop at "
        "the person who saw the client, and this site&rsquo;s "
        + plain(CASES, "discipline case library") + " is the concrete "
        "version of what that looks like when it goes wrong."))
    o.append(pk.checklist(
        "Questions worth answering before you agree to anything", [
            "Does your liability policy cover supervision, at what "
            "limit, and does it cover supervising somebody who is not "
            "your employee? Policies differ, and this is the clause to "
            "read rather than assume &mdash; "
            + plain(INS, "what each policy actually carries &rarr;"),
            "How much of their caseload will you genuinely see, and is "
            "that enough to answer for it?",
            "What happens if you disagree with their employer about a "
            "clinical decision, and who does the supervisee answer to "
            "when you do?",
            "What is your exit? Ending a supervision relationship "
            "mid-accrual has consequences for the supervisee that are "
            "not symmetrical with the consequences for you.",
            "If they are your employee, is every non-clinical hour "
            "being paid? Unpaid administrative time is a wage claim "
            "rather than a Board matter, and "
            + plain(UNPAID, "that distinction has its own page") + ".",
        ]))
    o.append("</section>")

    # --------------------------------------------------------------- fee
    o.append(sec("fee", "What it pays",
                 "And why this page will not quote you a rate."))
    o.append(p(
        "There is no published, authoritative figure for what California "
        "clinical supervisors charge. There are survey numbers, forum "
        "numbers and vendor numbers, and not one of them traces to a "
        "source that could be linked here. Every other figure on this "
        "site points at the page or the statute it came from, and a rate "
        "range invented to fill a gap would be the one number on the "
        "site that could not do that. So there is not one."))
    o.append(p(
        "What can be said is what moves it: whether the supervisee or "
        "their employer is paying, whether the hour is individual or "
        "held in a group, how much of the caseload you are accepting "
        "responsibility for, and what the local market pays associates "
        "in the first place &mdash; which "
        + plain(PAY, "this site does publish, from real pay scales")
        + ". If you are being paid by an agency rather than by an "
        "individual, the question underneath the fee is usually whether "
        "that setting can bill for a pre-licensed clinician at all, "
        "which is set out on "
        + plain(GETHIRED, "the getting-hired page") + "."))
    o.append(pk.callout(
        "The honest summary",
        ["Supervising for a fee is a modest hourly income with an "
         "unmodest tail of responsibility, and a fixed cost of fifteen "
         "training hours before it starts. Employing an associate is a "
         "different proposition entirely, priced properly on "
         + plain(HIRE, "the hiring page") + ", where the answer turns on "
         "whether the caseload fills rather than on what you charge for "
         "an hour of supervision.",
         "Anybody who tells you the second question is answered by the "
         "first number is selling something."]))
    o.append("</section>")

    src, nsrc = pk.sources([
        ("Who may supervise, and on what terms", [
            ("Business and Professions Code section 4980.03 - the "
             "supervisor definition, including both two-year tests",
             BPC4980_03),
            ("Section 4980.43.3 - an associate or trainee &ldquo;shall "
             "only perform mental health and related services as an "
             "employee or volunteer, and not as an independent "
             "contractor&rdquo;, and trainees not in private practice",
             BPC4980_43_3),
            ("The same section, as read for this page", F4980_43_3),
            ("The Board's Supervision Agreement form", BBSSUP),
        ]),
        ("The training requirement", [
            ("16 CCR section 1821.3 - fifteen hours before supervising "
             "for the first time, six in each subsequent renewal period, "
             "and the content each must cover", CCR1821_3),
        ]),
        ("The economics, on the pages that compute them", [
            ("Hiring an associate - the loaded cost, the break-even "
             "caseload and the classification rule", HIRE),
            ("What associate jobs actually pay, from published pay "
             "scales", PAY),
            ("Which settings can lawfully bill for a pre-licensed "
             "clinician", GETHIRED),
            ("Unpaid non-clinical hours - a wage claim rather than a "
             "Board matter", UNPAID),
            ("Liability insurance compared, including what each policy "
             "carries", INS),
            ("The discipline case library", CASES),
            ("Finding a supervisor - the supervisee's side of the same "
             "arrangement", FINDSUP),
            ("The 3,000 hours, and the logs that have to be kept "
             "separately", HOURS),
            ("Continuing education for the license itself, which the "
             "six supervision hours sit alongside", CE),
        ]),
    ], note="leginfo blocks automated reading, so section 4980.43.3 was "
            "read at the mirror linked beside it and the regulation at "
            "Cornell's copy; leginfo is linked as the place to read each "
            "section. Checked " + READ + ". <b>This page quotes no rate "
            "for supervision</b>, because no authority publishes one and "
            "every other figure on this site traces to the page or "
            "statute that produced it. Nothing here is legal, tax or "
            "employment advice. This site earns nothing from any link on "
            "this page.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Becoming a clinical supervisor in California: the real cost",
    "Fifteen training hours before you start, six every renewal, two "
    "separate eligibility tests, and why supervising for a fee is not "
    "employing an associate.",
    "practice", "guide",
    "What does it cost, and pay, to be a clinical supervisor?",
    "Two different decisions with different economics: an hourly fee "
    "with a training bill and real liability, or a hiring decision",
    "15 hours of training, then 6 every renewal period",
    weight=4)


def main():
    print("the supervisor-economics page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    path = os.path.join(SITE, PAGE)
    open(path, "w", encoding="utf-8").write(html)
    print("  wrote " + PAGE + ", " + format(len(html), ",d")
          + " bytes, " + str(nsrc) + " sources")

    bad = 0
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
        ("BPC 4980.03", "sectionNum=4980.03."),
        ("BPC 4980.43.3", "sectionNum=4980.43.3."),
        ("the training regulation", "16-CCR-1821.3"),
        # The training hours, quoted.
        ("the initial training hours", "fifteen (15) hours"),
        ("the renewal training hours", "six (6) hours"),
        # The eligibility point the page exists for.
        ("the second two-year test",
         "practicing psychotherapy or providing clinical supervision"),
        # The employment rule that separates the two economics.
        ("the contractor prohibition", "not as an independent"),
        # The pages it hands each half to.
        ("the hiring page", HIRE),
        ("the finding-a-supervisor page", FINDSUP),
        ("the pay page", PAY),
        ("the insurance page", INS),
    ], [h for h, _ in JUMPS])

    s = open(path, encoding="utf-8").read()
    art = pk.article(s)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # ---- NO INVENTED SUPERVISION RATE. This is the page's whole
    # discipline: no authority publishes what supervisors charge, and a
    # plausible range would be the one figure on this site that could not
    # point at its source. If a real published source ever appears, cite
    # it and update this guard deliberately.
    for pattern in (r"\$\s?\d[\d,]*\s*(?:an|per|/|a)\s*hour",
                    r"\$\s?\d[\d,]*\s*(?:to|-|&ndash;)\s*\$\s?\d",
                    r"\$\s?\d[\d,]*\s*(?:a|per)\s*(?:session|week|month)"):
        m = re.search(pattern, flat)
        if m:
            print("GUARD: \"" + m.group(0).strip() + "\" is a rate on a "
                  "page that states it quotes none. Either it has a "
                  "linkable primary source - in which case cite it and "
                  "change this guard on purpose - or it is invented.")
            bad += 1
    # ---- and the refusal must be stated, not silently observed
    if "quotes no rate" not in flat and "will not quote you a rate" not in flat:
        print("GUARD: the page no longer explains WHY it gives no rate. "
              "An absence without a reason reads as an omission.")
        bad += 1
    # ---- the two-questions frame is the page; it may not collapse
    if "not the same decision" not in flat and "two questions" not in flat:
        print("GUARD: the two-different-decisions frame has gone, which "
              "is the one thing this page does that the others do not")
        bad += 1

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
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        bad += 1

    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    dlen = len(desc.group(1)) if desc else 0
    if not 70 <= dlen <= 168:
        print("GUARD: the meta description is " + str(dlen)
              + " characters; seo_rules wants 70 to 168")
        bad += 1

    if n or bad:
        sys.exit(str(n + bad) + " check failure(s)")
    print("  checks passed - both two-year tests stated, training hours "
          "quoted, no rate invented, description " + str(dlen)
          + " chars, " + str(nsrc) + " sources")


if __name__ == "__main__":
    main()
