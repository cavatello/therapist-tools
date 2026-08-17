#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exam prep courses compared - on price, and on what each one claims.

EDITORIAL #8 of the approved list. The queued brief said "needs Pearson
VUE handbook + vendor prices". Half of that was already answered on this
site: `become-an-mft-california.html` establishes that **Pearson VUE
charges the candidate nothing** - the exam fee is already inside what you
paid the Board - and `bbs-exam-pass-rates-california.html` carries both
published pass rates for all seven exams across seven quarters.

So the gap is the third-party prep market, and the gap is not really
price. It is that the market's central claim cannot be checked.

THE FINDING

Four vendors, and their pass-rate claims are four DIFFERENT KINDS OF
STATEMENT. Only one is even the same shape as the Board's number:

  Therapist Development Center  "pass rate has remained above 90%" and
      "95% of our users PASS" - a rate over people who bought and used
      the program. Self-selected, self-reported, unaudited.
  High Pass Education           "among customers who scored 80% or above
      on their first attempt at their final mock exam, 100% passed" -
      conditioned on ALREADY doing well on a proxy for the exam. It is
      not a pass rate for buyers, and it cannot be.
  Gerry Grossman Seminars       no rate at all. A "Pass Guarantee" that
      says in its own words it ensures the program stays available for a
      retake - explicitly access, not passage.
  AATBS                         no rate on the product page.

And the one vendor that does compare itself to the Board compares itself
to a figure from **the first half of 2018**: "over 70%". The Board's most
recent published quarter has LMFT Clinical first-time at 80%. So the gap
the claim implies - 90-plus against 70 - is roughly half what it looks
like against the real current number, which this site already publishes.

None of that makes any of these products bad. It makes the advertised
numbers uncomparable, which is a different and more useful thing to know
before spending $139 to $620.

SOURCING RULE

Every price is from the vendor's own product or pricing page, read
17 August 2026, and quoted as published. Every pass-rate claim is quoted
verbatim and attributed. Nothing is characterised as a fact about
outcomes, because none of it is verifiable from outside the company.
Board figures are lifted from the pages on this site that carry them,
under the same no-new-numbers rule as build_viable.py.

NO AFFILIATE LINKS. The site owner's instruction on 17 Aug 2026 was
"no affiliate code now, will add later", so every vendor link here is a
plain link and a guard below fails the build if a tracking parameter ever
appears in one. When affiliate links are added, that guard is the thing
to update deliberately - and the affiliate-disclosure page is the thing
to update with it.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "exam-prep-courses-california-compared.html"
DONOR = "bbs-advertising-rules-2026.html"

RATES = "bbs-exam-pass-rates-california.html"
ROUTE = "become-an-mft-california.html"
FEES = "bbs-fees-california-2026.html"
COST = "what-licensure-actually-costs-california.html"

# Vendor pages, read 17 August 2026. PLAIN LINKS - see the module docstring.
TDC_CLIN = "https://therapistdevelopmentcenter.com/product/california-mft-clinical-exam"
TDC_LE = "https://therapistdevelopmentcenter.com/product/california-mft-law-ethics"
TDC_COMBO = ("https://therapistdevelopmentcenter.com/product/"
             "ca-combo-mft-law-ethics-and-clinical-exam")
HP_CLIN = "https://highpass.com/products/california-mft-clinical-exam-prep"
HP_VS = ("https://highpass.com/pages/"
         "high-pass-education-versus-therapist-development-center-tdc")
GG_SELF = "https://gerrygrossman.com/mft-cce-exam-prep-self-study-course"
GG_LIVE = "https://gerrygrossman.com/mft-cce-exam-prep-course-and-live-online-workshop"
AATBS_SELF = "https://aatbs.com/california-mft-exam-prep-package-self-study-3m"
PEARSON = "https://home.pearsonvue.com/cabbs"
LE_FAQ = "https://www.bbs.ca.gov/pdf/publications/law_ethics_faq.pdf"
LMFT_HB = "https://www.bbs.ca.gov/pdf/publications/lmft_handbook.pdf"

# Figures carried from pages on this site, not introduced here.
FIGURES = [("80%", RATES), ("78%", RATES), ("$75", FEES), ("$125", FEES)]

JUMPS = [("free", "What costs nothing"),
         ("prices", "What the courses cost"),
         ("claims", "What they claim"),
         ("stale", "The stale comparison"),
         ("fail", "What failing costs"),
         ("sources", "Sources")]


def plain(u, t):
    """An internal link. No rel/target - those are for outbound only."""
    return '<a href="%s">%s</a>' % (u, t)


def link(u, t):
    return ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
            % (u, t))


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Four vendors &middot; every price from its own page &middot; "
        "read 17 August 2026",
        "Prep costs more than the exam. The pass rates it advertises "
        "cannot be compared.",
        "The Board&rsquo;s exam fees are $75 and $125, and the test "
        "vendor charges you nothing. Prep courses run $139 to $620. "
        "Three of the four companies make a claim about how many of "
        "their users pass, and the three claims are three different "
        "kinds of sentence &mdash; only one of which is the same shape "
        "as the number the Board publishes.",
        [("$139&ndash;$620", "the range of published prep prices"),
         ("$0", "what the exam vendor charges you"),
         ("80%", "LMFT Clinical, first-time, Board-published"),
         ("3", "different kinds of claim, from 4 vendors")],
        JUMPS))

    # ---------------------------------------------------------------- free
    o.append('<section class="pk-sec" id="free">')
    o.append('<p class="pk-k">Before you buy anything</p>')
    o.append('<h2 class="pk-h">The exam vendor charges you nothing, and '
             "the Board publishes the handbooks.</h2>")
    o.append('<p class="pk-p">Pearson VUE administers both California '
             "exams and takes no money from the candidate &mdash; the "
             "fee is already inside what you paid the Board, which is "
             "worked through on "
             + plain(ROUTE, "the route page")
             + ". The candidate handbook for each exam, which contains "
             "the content outline the questions are built from, is "
             "published at " + link(PEARSON, "Pearson VUE's California "
             "BBS page") + ". The Board also publishes a "
             + link(LMFT_HB, "Handbook for Future LMFTs") + " and a "
             + link(LE_FAQ, "law and ethics exam FAQ")
             + ". All of it is free, and none of it is a course.</p>")
    o.append('<p class="pk-p">That matters for reading the prices '
             "below. None of these companies is selling you access to "
             "the exam, or to the outline, or to the rules. They are "
             "selling structure, practice questions and someone to ask "
             "&mdash; which is a real product, and a different one from "
             "what the price sometimes implies.</p>")
    o.append("</section>")

    # -------------------------------------------------------------- prices
    o.append('<section class="pk-sec" id="prices">')
    o.append('<p class="pk-k">Published prices, from each vendor&rsquo;s '
             "own page</p>")
    o.append('<h2 class="pk-h">$139 to $620, and the access window '
             "varies more than the price.</h2>")

    rows = [
        ["High Pass Education", link(HP_VS, "Law &amp; Ethics"),
         ("$139", "f"), "&mdash;", "None on the page"],
        [link(AATBS_SELF, "AATBS"), "CA MFT, self-study",
         ("$289", "f"), "3 months", "None on the page; +$125 coaching"],
        [link(TDC_LE, "Therapist Development Center"), "Law &amp; Ethics",
         ("$295", "f"), "4 months, free extensions", "&ldquo;95% of our "
         "users PASS&rdquo;"],
        [link(HP_CLIN, "High Pass Education"), "Clinical, self-study",
         ("$249", "f"), "180 days, free extensions", "None on this page"],
        [link(HP_CLIN, "High Pass Education"), "Clinical, supported",
         ("$399", "f"), "180 days", "See the claim below"],
        [link(GG_SELF, "Gerry Grossman Seminars"), "Clinical, self-study",
         ("$329", "f"), "8 months of testbank",
         "No rate; a Pass Guarantee"],
        [link(GG_LIVE, "Gerry Grossman Seminars"),
         "Clinical + 22h live online", ("$399", "f"),
         "8 months of testbank", "No rate; a Pass Guarantee"],
        [link(TDC_CLIN, "Therapist Development Center"), "Clinical",
         ("$375", "f"), "6 months, free extensions",
         "&ldquo;above 90%&rdquo;"],
        [link(TDC_COMBO, "Therapist Development Center"),
         "Both exams, combined", ("$620", "f"), "&mdash;", "&mdash;"],
    ]
    o.append(pk.table(["Vendor", "Product", "Published price", "Access",
                       "Pass claim on the page"], rows,
                      caption="Every figure read from the vendor's own "
                              "product or pricing page on 17 August "
                              "2026. Prices change; the link beside "
                              "each one is the thing to check, not this "
                              "table.", minw=760))
    o.append('<p class="pk-p">Two things are worth noticing before the '
             "claims. The <b>access window</b> ranges from three months "
             "to eight, and three of the four vendors say they extend "
             "it at no cost if you need longer &mdash; which quietly "
             "matters more than fifty dollars of list price, because "
             "the thing that actually goes wrong is a delayed exam "
             "date. And the <b>live-instruction premium</b> is small: "
             "Grossman charges $70 more for 22 hours of live online "
             "teaching on top of the same materials.</p>")
    o.append("</section>")

    # -------------------------------------------------------------- claims
    o.append('<section class="pk-sec" id="claims">')
    o.append('<p class="pk-k">The part that does not compare</p>')
    o.append('<h2 class="pk-h">Three claims, three different kinds of '
             "sentence.</h2>")
    o.append('<p class="pk-p">Each of these is quoted from the '
             "vendor&rsquo;s own page. None of them is audited by "
             "anyone, and no vendor is obliged to publish one at all. "
             "Read them as advertising that happens to contain a "
             "number.</p>")
    o.append(pk.numbered([
        ("1", "A rate over people who bought and used the program.",
         "Therapist Development Center: its clinical page says its "
         "&ldquo;pass rate has remained above 90% for individuals who "
         "used our comprehensive program&rdquo;, and its law and ethics "
         "page says &ldquo;95% of our users PASS&rdquo;. This is the "
         "only one of the three that is even the same shape as the "
         "Board&rsquo;s figure &mdash; but the population is people who "
         "chose to buy a course and then worked through it, which is "
         "not the population the Board measures."),
        ("2", "A rate conditioned on already doing well.",
         "High Pass Education, on its comparison page: &ldquo;among "
         "customers who scored 80% or above on their first attempt at "
         "their final mock exam, 100% passed their real exam.&rdquo; "
         "Read the condition. This describes people who had already "
         "demonstrated they could pass a full-length practice exam. It "
         "is a statement about the mock exam&rsquo;s predictive value, "
         "not about what buying the course does &mdash; and by "
         "construction it cannot tell you what happened to the "
         "customers who scored under 80%."),
        ("3", "No rate at all, and a guarantee about access.",
         "Gerry Grossman Seminars publishes no pass rate. What it "
         "publishes is a Pass Guarantee, and the wording is careful: it "
         "&ldquo;can ensure that your study program will be available "
         "at no additional cost to you if you do not pass the exam and "
         "elect to retake it within 12 months&rdquo;. That guarantees "
         "the program stays open to you. It does not guarantee the "
         "result, and it does not pretend to. AATBS&rsquo;s "
         "self-study product page likewise states no rate."),
    ]))
    o.append(pk.callout(
        "What this means practically",
        ["You cannot rank these four products by their advertised "
         "numbers, because the numbers are not measuring the same "
         "thing and nobody outside the companies can check any of "
         "them.",
         "What you CAN compare is the published price, the length of "
         "access, whether extensions are free, whether there is live "
         "teaching, and how many practice questions come with it. "
         "Those are all in the table above and all verifiable."]))
    o.append("</section>")

    # --------------------------------------------------------------- stale
    o.append('<section class="pk-sec" id="stale">')
    o.append('<p class="pk-k">One number worth correcting</p>')
    o.append('<h2 class="pk-h">The comparison in the advertising is '
             "eight years old.</h2>")
    o.append('<p class="pk-p">The one vendor that sets its claim '
             "against the Board&rsquo;s own figure does it like this, "
             "on its clinical page: &ldquo;The BBS publishes the pass "
             "rates&hellip;the pass rate for first time test takers of "
             "the California Clinical MFT Exam in the first half of "
             "2018 was over 70%.&rdquo;</p>")
    o.append('<p class="pk-p">That was true of the first half of 2018. '
             "The most recent quarter the Board has published has the "
             "LMFT Clinical exam at <b>80% first-time</b>, and the LMFT "
             "Law and Ethics exam at <b>78% first-time</b> &mdash; both "
             "of them, across seven quarters, are on "
             + plain(RATES, "the pass-rates page")
             + ". So &ldquo;above 90%&rdquo; against a real 80% is a "
             "different-sized claim from &ldquo;above 90%&rdquo; against "
             "70%, and it is the kind of gap that closes quietly when "
             "nobody updates a sentence.</p>")
    o.append('<p class="pk-p">The pass-rates page is also where to see '
             "the distinction the vendors do not draw: the Board "
             "publishes a first-time rate AND an all-sittings rate for "
             "every exam, and they are not close. A course advertising "
             "against the lower one is flattering itself.</p>")
    o.append("</section>")

    # ---------------------------------------------------------------- fail
    o.append('<section class="pk-sec" id="fail">')
    o.append('<p class="pk-k">The actual downside</p>')
    o.append('<h2 class="pk-h">Failing costs 90 days and another exam '
             "fee &mdash; not your registration.</h2>")
    o.append('<p class="pk-p">This is the part worth being calm about, '
             "because it is the fear the whole market is priced "
             "against. From the Board&rsquo;s own law and ethics FAQ: "
             "you are eligible to retake <b>after a 90-day waiting "
             "period</b>, once a re-exam application and fee are in. "
             "The exam fees themselves are $75 for California Law and "
             "Ethics and $125 for the LMFT clinical exam &mdash; both "
             "halved on 1 July 2026 and both reverting in 2030, which "
             "is set out on " + plain(FEES, "the fee-schedule page")
             + ".</p>")
    o.append(pk.quote(
        "And the thing almost nobody tells associates, from the "
        "Board&rsquo;s FAQ",
        ["&ldquo;If you have taken the exam a minimum of one time "
         "during your renewal cycle, you have met the exam requirement "
         "for renewal. You are not required to pass the exam, except to "
         "qualify for obtaining a subsequent registration, or to obtain "
         "your license.&rdquo;"]))
    o.append('<p class="pk-p">So a failed law and ethics attempt does '
             "not cost you your registration renewal. Taking it is the "
             "renewal condition; passing it is the condition for a "
             "later registration or the license itself. That is a "
             "materially smaller consequence than the way it is usually "
             "described, and it is worth knowing before deciding how "
             "much prep to buy.</p>")
    o.append('<p class="pk-p">Set against that: a retake is 90 days and '
             "another exam fee. Where prep pays for itself is in not "
             "spending a quarter of a year waiting &mdash; and the whole "
             "cost of getting licensed, prep excluded because this site "
             "does not price it into that total, is on "
             + plain(COST, "the cost-of-licensure page") + ".</p>")
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The vendors' own pages, read 17 August 2026. Plain links - "
         "this site earns nothing from any of them", [
            ("Therapist Development Center - California MFT Clinical, "
             "$375, and the 'above 90%' claim", TDC_CLIN),
            ("Therapist Development Center - California MFT Law and "
             "Ethics, $295, and the '95% of our users PASS' claim",
             TDC_LE),
            ("Therapist Development Center - the combined package, $620",
             TDC_COMBO),
            ("High Pass Education - California LMFT Clinical, $249 "
             "self-study and $399 supported, 180 days", HP_CLIN),
            ("High Pass Education - its comparison page, source of the "
             "$139 Law and Ethics price and the mock-exam claim", HP_VS),
            ("Gerry Grossman Seminars - clinical self-study, $329, and "
             "the Pass Guarantee wording", GG_SELF),
            ("Gerry Grossman Seminars - clinical with 22 hours of live "
             "online instruction, $399", GG_LIVE),
            ("AATBS - California MFT self-study, three months, $289",
             AATBS_SELF),
        ]),
        ("The Board and the test vendor", [
            ("Pearson VUE's California BBS page - where both candidate "
             "handbooks live, at no charge", PEARSON),
            ("The Board's law and ethics exam FAQ - the 90-day retake "
             "wait, and the renewal rule that does not require passing",
             LE_FAQ),
            ("The Board's Handbook for Future LMFTs", LMFT_HB),
        ]),
        ("Figures carried from pages on this site", [
            ("The pass-rates page - both published rates for all seven "
             "exams across seven quarters, including the 80% and 78% "
             "first-time figures used above", RATES),
            ("The route page - why the exam vendor charges the "
             "candidate nothing", ROUTE),
            ("The fee schedule - the $75 and $125 exam fees, halved to "
             "2030", FEES),
            ("What licensure actually costs - the whole bill, which "
             "deliberately does not price prep", COST),
        ]),
    ], note="Prices and claims were read on 17 August 2026 and both "
            "change; the link beside each figure is the authority, not "
            "this page. Every pass-rate claim above is quoted from the "
            "company that makes it and is not audited by anyone - "
            "including by this site, which has no way to verify any of "
            "them and does not endorse any of these products. This site "
            "earns nothing from these links. Nothing here is legal or "
            "financial advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "California therapist exam prep compared: price and claims",
    "Four California MFT exam prep vendors on published price and "
    "access, $139 to $620, and why their advertised pass rates cannot "
    "be compared.",
    "licensure", "reference",
    "Which California therapist exam prep course should I buy?",
    "Every published price and access window, and what each vendor's "
    "pass-rate claim actually measures",
    "$139 to $620, and 3 kinds of unverifiable claim",
    weight=4)


def main():
    print("the exam-prep comparison page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = 0
    # ---- Board figures must exist on the page they are attributed to
    for fig, src_page in FIGURES:
        s = open(os.path.join(SITE, src_page), encoding="utf-8").read()
        if fig.replace("$", "") not in s.replace("$", ""):
            print("GUARD: %s is attributed to %s, which does not "
                  "contain it" % (fig, src_page))
            bad += 1

    n = pk.check_page(p, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        ("the pass-rates link", RATES),
        ("the fee-schedule link", FEES),
        ("the cost-of-licensure link", COST),
        ("the Pearson VUE link", "home.pearsonvue.com/cabbs"),
        ("the law and ethics FAQ", "law_ethics_faq.pdf"),
        ("the TDC clinical price", "$375"),
        ("the TDC law and ethics price", "$295"),
        ("the High Pass clinical price", "$249"),
        ("the Grossman self-study price", "$329"),
        ("the AATBS price", "$289"),
        ("the combined price", "$620"),
    ], [h for h, _ in JUMPS])

    s = open(p, encoding="utf-8").read()
    artm = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s)
    art = artm.group(0)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", art)).lower()

    # ---- THE AFFILIATE GUARD. The owner's instruction on 17 Aug 2026 was
    # "no affiliate code now, will add later". Until that changes, a
    # tracking parameter on a vendor link is a bug, and this is where the
    # decision gets revisited rather than drifting in.
    for track in ("?ref=", "&ref=", "?aff", "&aff", "utm_", "?tap_",
                  "impact.com", "shareasale", "partnerize", "?a_aid",
                  "clickbank", "?pa=", "avantlink"):
        if track in art:
            print("GUARD: vendor links must stay plain - found %r. If "
                  "affiliate links are being added deliberately, update "
                  "this guard AND affiliate-disclosure.html in the same "
                  "change." % track)
            bad += 1
    # And the page must say so out loud, since the reader cannot tell.
    if "earns nothing" not in flat:
        print("GUARD: the page no longer states that the site earns "
              "nothing from these links")
        bad += 1

    # ---- the three claim-types are the argument; all three must survive
    for must, why in (("above 90%", "the TDC clinical claim"),
                      ("95% of our users", "the TDC law-ethics claim"),
                      ("100% passed", "the High Pass conditional claim"),
                      ("pass guarantee", "the Grossman access guarantee"),
                      ("first half of 2018", "the stale comparison")):
        if must not in flat:
            print("GUARD: %s (%r) is missing - the comparison loses its "
                  "point without it" % (why, must))
            bad += 1
    # No claim may be restated as this site's own finding.
    for wrong in ("we found that", "our testing shows",
                  "the best course", "we recommend buying"):
        if wrong in flat:
            print("GUARD: %r turns a quoted claim into an endorsement"
                  % wrong)
            bad += 1

    for phrase in ("is hiring", "has openings", "guaranteed",
                   "accepting new"):
        if phrase in flat:
            print("GUARD: banned phrase %r in the article" % phrase)
            n += 1
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        n += 1

    if n or bad:
        sys.exit("%d check failure(s)" % (n + bad))
    print("  checks passed - 9 published prices, 3 claim types quoted, "
          "no affiliate parameters")


if __name__ == "__main__":
    main()
