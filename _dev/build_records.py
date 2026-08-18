#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client records: how long to keep them, and what a client is entitled to.

TIER 3 EDITORIAL #1d, and the companion to `_dev/build_subpoena.py`.

WHY THIS IS A SECOND PAGE AND NOT PART OF THE SUBPOENA ONE

The brief asked for that decision to be made before either was written.
It was, and the answer is two pages, because the two readers are in
incompatible states. A subpoena page is read in a panic and has to be
short, sequenced and answerable in one sitting - the one failure mode it
cannot have is length. This page is reference: it gets consulted on a
quiet afternoon, one section at a time, by somebody deciding whether to
shred a box or how to answer a request that arrived by email. Folding
them together would have lengthened the emergency page to protect the
reference one, which is the wrong trade in both directions. They link to
each other instead.

THE FOUR QUESTIONS, AND WHERE EACH ANSWER LIVES

  how long          B&P 4980.49, 4993, 4999.75 and 4989.51 - one rule,
                    four license types, all added by SB 578 in 2014
  what a client
  is entitled to    Health and Safety Code 123110 - inspection in five
                    working days, copies in fifteen, at 25 cents a page
  a summary
  instead           Health and Safety Code 123130 - ten working days,
                    thirty at the outside, and a list of what it must
                    contain
  what may be
  withheld          Health and Safety Code 123115 - the mental health
                    exception, and the duty that comes with using it

THE PART THE STATUTE DOES NOT ANSWER

Nothing in the retention sections says who holds the records if the
therapist dies, or where they go when a practice closes. That silence is
a finding, not a gap in the research, and the page says so in those
terms rather than filling it with an invented rule or with somebody's
blog post. The BBS publishes no rule on it either. What the page can do
is state the obligation that survives - seven years is seven years,
whatever happens to the practice - and leave the reader clear that the
arrangement is theirs to make.

SOURCING. leginfo blocks automated fetching, so each section was read at
the mirror linked beside it, and leginfo is linked as the place to read
the section. Every day count and the per-page fee are guarded, because
they are exactly the figures that get misremembered by one unit.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "client-records-california-therapist.html"
DONOR = "bbs-advertising-rules-2026.html"

READ = "18 August 2026"

SUB = "subpoena-california-therapist.html"
EHR = "therapynotes-vs-simplepractice-california.html"
INS = "therapy-liability-insurance-california.html"
CASE = "discipline-case-billed-for-sessions-that-never-happened.html"
ADRULES = "bbs-advertising-rules-2026.html"
TELE = "telehealth-rules-california-therapist.html"

FIGURES = [("seven years", EHR), ("shredded", CASE),
           ("most commonly reported use", INS)]


def leg(code, section):
    return ("https://leginfo.legislature.ca.gov/faces/"
            "codes_displaySection.xhtml?lawCode=" + code
            + "&sectionNum=" + section + ".")


BPC4980 = leg("BPC", "4980.49")
BPC4993 = leg("BPC", "4993")
BPC4999 = leg("BPC", "4999.75")
BPC4989 = leg("BPC", "4989.51")
HSC123110 = leg("HSC", "123110")
HSC123115 = leg("HSC", "123115")
HSC123130 = leg("HSC", "123130")
J4980 = ("https://law.justia.com/codes/california/code-bpc/division-2/"
         "chapter-13/article-1/section-4980-49/")
SB578 = ("https://www.leginfo.ca.gov/pub/13-14/bill/sen/sb_0551-0600/"
         "sb_578_bill_20140815_enrolled.htm")
O123110 = "https://law.onecle.com/california/health/123110.html"
F123115 = ("https://codes.findlaw.com/ca/health-and-safety-code/"
           "hsc-sect-123115/")
F123130 = ("https://codes.findlaw.com/ca/health-and-safety-code/"
           "hsc-sect-123130/")

JUMPS = [("long", "How long"),
         ("access", "What a client can have"),
         ("summary", "A summary instead"),
         ("withhold", "When you may decline"),
         ("after", "Closing, and dying"),
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
        "Reference &middot; checked " + READ + " &middot; not legal advice",
        "Seven years, five working days, fifteen days, and 25 cents a "
        "page.",
        "Four numbers cover most of what a California therapist needs to "
        "know about records: how long you keep them, how fast a client "
        "may see them, how fast you must copy them, and the most you may "
        "charge for it. Each one is in a statute, each is linked below, "
        "and each is the kind of figure people misremember by one unit "
        "&mdash; which is usually the direction that gets somebody into "
        "trouble.",
        [("7 years", "from the date therapy ends"),
         ("5", "working days to allow inspection"),
         ("15", "days to provide copies"),
         ("$0.25", "a page, the most you may charge")],
        JUMPS))

    # -------------------------------------------------------------- long
    o.append(sec("long", "The retention rule",
                 "Seven years, and the clock starts when therapy ends "
                 "&mdash; not when the file was opened."))
    o.append(p(
        "A marriage and family therapist &ldquo;shall retain a "
        "client&rsquo;s or patient&rsquo;s health service records for a "
        "minimum of <b>seven years from the date therapy is "
        "terminated</b>&rdquo;. That is Business and Professions Code "
        "section 4980.49, and the identical rule sits in three other "
        "sections for three other license types &mdash; all four were "
        "added by the same bill, SB 578, in 2014."))
    o.append(pk.table(
        ["License", "Section", "Rule"],
        [["Marriage and family therapist", ("4980.49", "m"),
          "Seven years from termination"],
         ["Clinical social worker", ("4993", "m"),
          "Seven years from termination"],
         ["Professional clinical counselor", ("4999.75", "m"),
          "Seven years from termination"],
         ["Educational psychologist", ("4989.51", "m"),
          "Seven years from termination"]],
        caption="All four added by SB 578 (2014), and all four apply "
                "only where therapy terminated on or after 1 January "
                "2015.", minw=620))
    o.append(p(
        "Two details do most of the damage when they are missed. "
        "<b>For a client who was a minor</b>, the seven years run from "
        "the date they reach 18, not from the date therapy ended "
        "&mdash; so a file closed when a client was nine has to survive "
        "until they are 25. And the rule applies to therapy terminated "
        "<b>on or after 1 January 2015</b>; anything that ended before "
        "that is outside these sections."))
    o.append(p(
        "Records may be kept on paper or electronically. What that "
        "actually costs over seven years, and who is responsible for "
        "encryption and retrieval under each option, is worked through "
        "on " + plain(EHR, "the records-storage comparison") + "."))
    o.append("</section>")

    # ------------------------------------------------------------ access
    o.append(sec("access", "What a client is entitled to",
                 "Inspection in five working days, copies in fifteen, "
                 "and a fee cap."))
    o.append(pk.numbered([
        ("1", "Inspection: five working days",
         "On a written request, a patient may inspect their records "
         "&ldquo;within five working days after receipt of the "
         "request&rdquo;. Working days, not calendar days &mdash; the "
         "only place in this area where that distinction is drawn."),
        ("2", "Copies: fifteen days",
         "Copies must be transmitted &ldquo;within 15 days after "
         "receiving the request&rdquo;. Where the request relates to an "
         "application for a public benefit program the period is 30 "
         "days."),
        ("3", "The fee is capped, and it is small",
         "A provider may charge &ldquo;twenty-five cents ($0.25) per "
         "page for paper copies or fifty cents ($0.50) per page for "
         "records that are copied from microfilm&rdquo;, plus "
         "reasonable clerical costs. It is not a mechanism for "
         "recovering your time."),
    ]))
    o.append(pk.callout(
        "The request that is not a subpoena",
        ["A client asking for their own records and a lawyer demanding "
         "them are different events with different rules, and answering "
         "one with the procedure for the other is a common way to go "
         "wrong. If what arrived is court paper, start at "
         + plain(SUB, "the subpoena page") + " instead &mdash; a "
         "subpoena is not a court order, and the Evidence Code makes "
         "claiming your client&rsquo;s privilege mandatory rather than "
         "optional."]))
    o.append("</section>")

    # ----------------------------------------------------------- summary
    o.append(sec("summary", "The option most people do not know they "
                 "have",
                 "A provider may prepare a summary instead of handing "
                 "over the record."))
    o.append(p(
        "Health and Safety Code section 123130 lets a provider prepare "
        "a <b>summary</b> of the record rather than give access to the "
        "record itself. It is not a way of saying less: the section "
        "lists what the summary has to contain &mdash; chief complaints "
        "and pertinent history, findings from consultations and "
        "referrals, diagnosis where determined, treatment plan and "
        "regimen including medications, progress, prognosis, and the "
        "reports and results on file."))
    o.append(p(
        "The deadline is tighter than the one for copies. The summary "
        "must be made available <b>within 10 working days</b> of the "
        "request. If the record is extraordinarily long, or the patient "
        "was discharged within the last ten days, the provider tells "
        "the patient and gives a completion date &mdash; but &ldquo;in "
        "no case shall more than 30 days elapse between the request by "
        "the patient and the delivery of the summary&rdquo;."))
    o.append(p(
        "For a therapy file this is often the humane answer and "
        "occasionally the wrong one. It is a clinical decision with a "
        "statutory shape, and it is worth making it deliberately rather "
        "than by default in either direction."))
    o.append("</section>")

    # ---------------------------------------------------------- withhold
    o.append(sec("withhold", "The mental health exception",
                 "You may decline &mdash; and the moment you do, three "
                 "duties attach."))
    o.append(p(
        "Section 123115 lets a provider decline to permit inspection or "
        "copying of <b>mental health records</b> where there is "
        "&ldquo;a substantial risk of significant adverse or "
        "detrimental consequences&rdquo; to the patient. That is a real "
        "threshold and a high one, and it is not a general discretion "
        "to keep a file back because releasing it would be "
        "uncomfortable."))
    o.append(pk.checklist(
        "Using it obliges you to do all three of these", [
            "<b>Write it down.</b> Make a written record noting the "
            "date of the request and explaining the refusal, including "
            "the specific adverse or detrimental consequences you "
            "anticipate.",
            "<b>Tell the patient</b> that you have refused, and tell "
            "them they may nominate someone to receive the records on "
            "their behalf.",
            "<b>Give the records to the professional they nominate.</b> "
            "The patient may designate in writing a licensed physician "
            "and surgeon, psychologist, marriage and family therapist "
            "or other qualified professional, and that person must be "
            "permitted to inspect or receive copies. You also note in "
            "the record whether the request was made under that "
            "provision.",
        ]))
    o.append(p(
        "So the exception is not a door that closes. It redirects the "
        "record to a clinician who can put it in context, which is a "
        "different thing from withholding it, and the paperwork it "
        "creates is the point rather than a formality &mdash; it is "
        "what makes the decision reviewable later."))
    o.append("</section>")

    # ------------------------------------------------------------- after
    o.append(sec("after", "What the statute does not say",
                 "Nothing in the retention sections says who holds the "
                 "records if you die."))
    o.append(p(
        "Section 4980.49 has two subdivisions. One sets seven years; "
        "the other limits it to therapy terminated on or after "
        "1 January 2015. There is no third subdivision about death, "
        "retirement, incapacity or the closing of a practice, and the "
        "same is true of the three parallel sections. <b>That silence "
        "is the finding.</b> It is stated here as silence rather than "
        "filled with a rule, because a confident-sounding invented "
        "answer is worse than none on a question this consequential."))
    o.append(p(
        "What does survive is the obligation itself. The records still "
        "have to exist for seven years after therapy ended &mdash; or "
        "until a child client is 25 &mdash; and somebody has to be able "
        "to answer a client asking for them within the periods above. "
        "If a practice closes or a therapist dies without an "
        "arrangement in place, those duties do not disappear; they "
        "simply have nobody attached to them. Whatever arrangement "
        "answers that is one to make in advance and in writing, and it "
        "is worth asking your own liability carrier what its policy "
        "does and does not do here, since "
        + plain(INS, "the policies differ on what happens at death, "
                "disability or retirement") + "."))
    o.append(pk.callout(
        "One thing the record must never become",
        ["Whatever the file says, it says. This site&rsquo;s discipline "
         "library carries a matter in which a therapist told a state "
         "investigator that subpoenaed records had been "
         "<b>shredded</b>, and in which a client&rsquo;s own signed "
         "form was later shown to have been altered. Retention is the "
         "cheap half of this subject. "
         + plain(CASE, "The case &rarr;")]))
    o.append("</section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("How long, by license type", [
            ("Business and Professions Code section 4980.49 - marriage "
             "and family therapists", BPC4980),
            ("The same section, as read for this page", J4980),
            ("Section 4993 - clinical social workers", BPC4993),
            ("Section 4999.75 - professional clinical counselors",
             BPC4999),
            ("Section 4989.51 - educational psychologists", BPC4989),
            ("SB 578 (2014) as enrolled - the bill that added all four, "
             "and the source for the 1 January 2015 boundary", SB578),
        ]),
        ("What a client can have, and how fast", [
            ("Health and Safety Code section 123110 - inspection in "
             "five working days, copies in fifteen, and the 25-cent "
             "and 50-cent page fees", HSC123110),
            ("The same section, as read for this page", O123110),
            ("Section 123130 - the summary, what it must contain, and "
             "the 10 and 30 day limits", HSC123130),
            ("The same section, as read for this page", F123130),
            ("Section 123115 - the mental health exception and the "
             "duties that come with it", HSC123115),
            ("The same section, as read for this page", F123115),
        ]),
        ("Carried from pages on this site", [
            ("What a subpoena is, and why it is not a request for "
             "records", SUB),
            ("What seven years of storage costs, and who carries the "
             "security duty under each option", EHR),
            ("Liability insurance compared - including what happens at "
             "death, disability or retirement", INS),
            ("The discipline case in which subpoenaed records had been "
             "shredded", CASE),
            ("What you already have to tell clients in writing",
             ADRULES),
            ("The telehealth standard of practice", TELE),
        ]),
    ], note="leginfo blocks automated reading, so each section was read "
            "at the mirror linked beside it, and leginfo is linked as "
            "the place to read the section itself. Everything above was "
            "checked on " + READ + " and statutes change. <b>Nothing "
            "here is legal advice</b>: whether a particular record may "
            "be withheld, summarized or released turns on the client, "
            "the request and the clinical picture, and none of those is "
            "visible from a web page. This site earns nothing from any "
            "link here.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Client records: California therapist retention and access",
    "Seven years from termination, inspection in five working days, "
    "copies in fifteen at 25 cents a page, when you may decline, and "
    "what the statute never says.",
    "practice", "reference",
    "How long do I keep client records, and what can a client demand?",
    "Seven years from termination or from a minor's 18th birthday, with "
    "statutory deadlines and a capped fee for access",
    "7 years, 5 working days, 15 days, 25 cents a page",
    weight=5)


def main():
    print("the client records page")
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
        # Every section, by number, so a rewrite cannot drop one silently.
        ("BPC 4980.49", "sectionNum=4980.49."),
        ("BPC 4993", "sectionNum=4993."),
        ("BPC 4999.75", "sectionNum=4999.75."),
        ("BPC 4989.51", "sectionNum=4989.51."),
        ("HSC 123110", "sectionNum=123110."),
        ("HSC 123115", "sectionNum=123115."),
        ("HSC 123130", "sectionNum=123130."),
        ("the enrolled bill", "sb_578_bill"),
        # THE FOUR NUMBERS. Each is quoted from the statute and each is
        # the kind that gets misremembered by one unit, in the direction
        # that gets somebody into trouble.
        ("the retention quote",
         "seven years from the date therapy is "),
        ("the minor rule", "reach 18"),
        ("the 2015 boundary", "1 January 2015"),
        ("the inspection period", "five working days after receipt"),
        ("the copies period", "within 15 days after receiving"),
        ("the page fee", "twenty-five cents"),
        ("the microfilm fee", "fifty cents"),
        ("the summary deadline", "10 working days"),
        ("the summary long-stop", "30 days elapse"),
        ("the withholding threshold",
         "substantial risk of significant adverse"),
        # The pages it stands beside.
        ("the subpoena page", SUB),
        ("the storage page", EHR),
        ("the insurance page", INS),
    ], [h for h, _ in JUMPS])

    s = open(path, encoding="utf-8").read()
    art = pk.article(s)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # ---- The three duties that attach to withholding are the whole point
    # of that section: a page that says "you may decline" and drops them
    # is worse than a page that never raised it.
    for must, why in (("noting the date of the request",
                       "the duty to write the refusal down"),
                      ("designate", "the client's right to nominate "
                       "someone to receive the records")):
        if must not in flat:
            print("GUARD: " + why + " has gone from the withholding "
                  "section, which turns a narrow exception into a "
                  "general discretion")
            bad += 1

    # ---- The silence about death is a FINDING and must be stated as one.
    # And the reverse: the gap must not be quietly FILLED either. These
    # are the confident-sounding answers that circulate about what
    # happens to a therapy file when the therapist dies, none of which
    # is in the retention sections. If one of them becomes true - a bill
    # passes, the Board publishes a rule - cite it and delete the phrase
    # from this list. Do not let it arrive as prose.
    for invented in ("your executor takes over", "the board will hold",
                     "next of kin inherit", "the board takes custody",
                     "your estate becomes the custodian"):
        if invented in flat:
            print("GUARD: \"" + invented + "\" answers a question the "
                  "statute does not answer. Cite the authority that "
                  "changed, or take it out - an invented rule here is "
                  "worse than the acknowledged silence.")
            bad += 1
    if "that silence is the finding" not in flat:
        print("GUARD: the page no longer states that the statute's "
              "silence about death and closure is the finding. If a rule "
              "has since been enacted, cite it; do not quietly fill the "
              "gap.")
        bad += 1
    if "not legal advice" not in flat:
        print("GUARD: the not-legal-advice line has gone")
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
    print("  checks passed - 7 statutes cited, 4 license types, every "
          "deadline and fee quoted, the silence stated as silence, "
          "description " + str(dlen) + " chars, " + str(nsrc) + " sources")


if __name__ == "__main__":
    main()
