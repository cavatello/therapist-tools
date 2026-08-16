#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""'Why do people say there's no money in therapy?' - answered in numbers.

TIER 1, ITEM 4 of the approved editorial list. The question is asked in
those words in the California groups - 68 comments of people arguing
about it, and nobody answering with arithmetic. The practice simulator
already answers it numerically and nobody knows it exists; this page is
the PROSE FRONT DOOR to it: the whole-career arithmetic from the degree
through the associate years to a full private-practice caseload, every
figure lifted from a page on this site that computes or documents it,
ending at the calculator.

THE CONTENT RULE THIS PAGE LIVES BY: no new numbers. Every dollar figure
here already exists on another page of this site, where it carries its
own source and its own checked date. This page ONLY assembles them into
one career-shaped argument and links each figure to the page it came
from. If a figure moves, the source page moves first and this page's
link still lands on the truth. A guard asserts every named figure
appears on the page it is attributed to.

Not a yes/no page. The honest answer is "viable under conditions", and
the conditions are three numbers the reader controls - rate, caseload,
county - which is exactly what the simulator lets them set.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "is-therapy-financially-viable-california.html"
DONOR = "county-job-portals-california.html"

# every figure this page uses, and the page it must appear on
FIGURES = [
    ("$37,800", "mft-programs-california.html"),
    ("$152,340", "mft-programs-california.html"),
    ("$875", "bbs-fees-california-2026.html"),
    ("$70,304", "associate-therapist-pay-los-angeles-bay-area.html"),
    ("$105,827", "county-therapist-pay-california.html"),
    ("2.8", "county-therapist-pay-california.html"),
    ("$4,851", "therapist-cost-of-living-california.html"),
    ("250,000", "index.html"),
    ("41,650", "index.html"),
    ("69,410", "index.html"),
    ("138,940", "index.html"),
]

JUMPS = [("price", "The price of entry"),
         ("assoc", "The associate years"),
         ("practice", "The practice arithmetic"),
         ("verdict", "The honest answer"),
         ("sources", "Sources")]


def body():
    o = ['<article class="pk-wrap">']

    o.append('<section class="pk-hero">')
    o.append('<p class="hk">The career, in numbers &middot; every figure '
             "from a page that computes it</p>")
    o.append("<h1>Why do people say there&rsquo;s no money in "
             "therapy?</h1>")
    o.append('<p class="hl">It is asked in exactly those words, and the '
             "answers it gets are stories. This page is the arithmetic "
             "instead: what entering the profession costs, what the "
             "associate years actually pay, and what a full private "
             "practice nets after every expense and every tax &mdash; "
             "each figure lifted from the page on this site that "
             "computes it, so you can check every step. The short "
             "version: the money is real, it arrives late, and three "
             "numbers you control decide almost all of it.</p>")
    o.append('<p class="hj">')
    for h, l in JUMPS:
        o.append('<a href="#%s">%s</a>' % (h, l))
    o.append("</p></section>")

    # -------------------------------------------------------------- price
    o.append('<section class="pk-sec" id="price">')
    o.append('<p class="pk-k">Chapter one &middot; what you pay to '
             "enter</p>")
    o.append('<h2 class="pk-h">The degree is the whole price of '
             "admission. Everything after it is cheap.</h2>")
    o.append('<p class="pk-p">The 78 California MFT programs charge '
             'between <a href="mft-programs-california.html">$37,800 and '
             "$152,340 for the same qualifying degree</a> &mdash; a "
             "4&times; spread for a credential the Board treats as "
             "identical. That one enrollment decision moves more money "
             "than every other choice in this article combined, and it "
             "is made earliest, with the least information. The program "
             "directory compares all 78 on cost and on the year that "
             "varies most &mdash; who finds your practicum site.</p>")
    o.append('<p class="pk-p">The state, by contrast, is nearly free: '
             '<a href="bbs-fees-california-2026.html">$875 in Board fees '
             "covers the entire route at the six-year ceiling</a> "
             "&mdash; halved from $1,750 on 1 July 2026, reverting in "
             "2030. Registration, exams, licensure, renewals: all of it "
             "is a rounding error against one semester of tuition.</p>")
    o.append('<p class="pk-p">Time is the other entry price: two to '
             "three years of degree, then at least 104 weeks of "
             "supervised hours, then two exams. Six years from first "
             "class to license number is a normal, unremarkable pace "
             "&mdash; and the money below arrives in that order.</p>")
    o.append("</section>")

    # -------------------------------------------------------------- assoc
    o.append('<section class="pk-sec" id="assoc">')
    o.append('<p class="pk-k">Chapter two &middot; the associate '
             "years</p>")
    o.append('<h2 class="pk-h">The lean years are real, bounded, and '
             "priced county by county.</h2>")
    o.append('<p class="pk-p">This is the stretch the &ldquo;no money in '
             "therapy&rdquo; stories come from, and the stories are not "
             "wrong about the level &mdash; they are wrong about it "
             "being unknowable. A full-time associate offer paid as an "
             'exempt salary has a legal floor: <a href="associate-'
             'therapist-pay-los-angeles-bay-area.html">$70,304 in 2026'
             "</a>, and the pay page prices real LA and Bay Area offers "
             "against it. Public employers publish their scales: the "
             '<a href="county-therapist-pay-california.html">county pay '
             "page</a> ranks every California county from the "
             "government&rsquo;s own salary files &mdash; the statewide "
             "median top of range is $105,827, and the same clinical "
             "job pays 2.8&times; more in the top county than the "
             "bottom one. Where you count your hours is a salary "
             "decision, not just a housing one.</p>")
    o.append('<p class="pk-p">Two pages on this site exist because the '
             "associate years also have traps with dollar signs: "
             '<a href="associate-unpaid-hours-california.html">unpaid '
             "non-clinical time is a wage claim, not a norm</a>, and "
             '<a href="loan-forgiveness-employers-california.html">the '
             "right employer unlocks loan repayment programs</a> that "
             "the wrong one quietly does not. An associate year at a "
             "qualifying employer can be worth more than a "
             "higher-salaried year at a non-qualifying one &mdash; that "
             "arithmetic is on the forgiveness page.</p>")
    o.append("</section>")

    # ----------------------------------------------------------- practice
    o.append('<section class="pk-sec" id="practice">')
    o.append('<p class="pk-k">Chapter three &middot; the practice '
             "arithmetic</p>")
    o.append('<h2 class="pk-h">A full private caseload, walked from '
             "gross to bank account.</h2>")
    o.append('<p class="pk-p">Here is the worked example this '
             "site&rsquo;s home page runs live, at $200 a session and "
             "24 clients a week: <b>$250,000</b> gross across a working "
             "year; minus <b>$41,650</b> of running costs across twelve "
             "itemized categories; minus <b>$69,410</b> of "
             "self-employment and California tax; leaving "
             "<b>$138,940</b> reaching your account. Every step of "
             'that walk is live in <a href="practice-simulator.html">'
             "the practice simulator</a> &mdash; change the rate, the "
             "caseload, the expenses or the filing status and watch "
             "the whole column recompute.</p>")
    o.append('<p class="pk-p">Against that, the cost side of being the '
             'business: <a href="therapist-cost-of-living-california.'
             'html">the cost-of-living page</a> computes a break-even '
             "of $4,851 a month in its worked example, student loan "
             "included &mdash; which a $138,940 net clears with room, "
             "and a half-full caseload at a discounted rate does not. "
             "That is the honest hinge of the whole question: the same "
             "license, the same county, the same year can be "
             "comfortable or underwater on three inputs.</p>")
    o.append('<p class="pk-p">The tax line deserves its own sentence, '
             "because part of it is optional: <a href=\"therapist-tax-"
             'strategy-california.html">the tax strategy page</a> works '
             "the sole-proprietorship-versus-professional-corporation "
             "decision on your own numbers, with the payroll gap most "
             "comparisons leave out, and the retirement moves that "
             "turn tax into savings.</p>")
    o.append("</section>")

    # ------------------------------------------------------------ verdict
    o.append('<section class="pk-sec" id="verdict">')
    o.append('<p class="pk-k">The honest answer</p>')
    o.append('<h2 class="pk-h">Viable is a number you set three '
             "times.</h2>")
    o.append('<p class="pk-p">&ldquo;Is therapy financially '
             "viable&rdquo; has no yes or no, because the profession "
             "does not pay a wage &mdash; it pays an equation. The "
             "three inputs you control are your rate, your caseload, "
             "and your county, and the spread between weak and strong "
             "answers to those three is wider than the spread between "
             "therapy and most salaried professions. What IS "
             "answerable, precisely, is your own case: put your "
             'numbers into <a href="practice-simulator.html">the '
             "simulator</a> and read what your practice would actually "
             "pay you. If the answer is thin, the levers are on the "
             "same page.</p>")
    o.append('<p class="pk-p">And if you are reading this before '
             'enrolling anywhere: <a href="for/deciding.html">the '
             "deciding door</a> holds every page on this site written "
             "for exactly that question, costs first.</p>")
    o.append("</section>")

    # ------------------------------------------------------------ sources
    src, nsrc = pk.sources([
        ("Where every figure on this page is computed", [
            ("The 78 programs compared on cost - the $37,800 to "
             "$152,340 spread", "mft-programs-california.html"),
            ("The Board&rsquo;s whole fee schedule - $875 at the "
             "six-year ceiling, halved through 2030",
             "bbs-fees-california-2026.html"),
            ("Associate pay against the $70,304 exempt floor, offer by "
             "offer", "associate-therapist-pay-los-angeles-bay-area.html"),
            ("Every county ranked from the state&rsquo;s own salary "
             "files - the 2.8&times; spread",
             "county-therapist-pay-california.html"),
            ("The cost-of-living break-even, loan included",
             "therapist-cost-of-living-california.html"),
            ("The live walk from gross to bank account",
             "practice-simulator.html"),
        ]),
    ], note="This page introduces no figures of its own. Each number "
            "above is computed or documented on the page it links, "
            "where it carries its own primary source and its own "
            "checked date. Nothing here is financial advice; it is "
            "arithmetic on published figures, and the simulator runs "
            "it on yours.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Is therapy financially viable in California? The arithmetic",
    "The whole-career arithmetic on published figures - what the degree "
    "costs, what the associate years pay, and what a full private "
    "practice nets after expenses and tax, ending at the live "
    "calculator.",
    "money", "guide",
    "Is being a therapist in California financially viable?",
    "The career walked in numbers - degree cost, the associate floor, "
    "the county spread, and a full caseload gross to net",
    "From a $70,304 associate floor to $138,940 practice net",
    weight=4)


def main():
    print("the viability page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    # ---- no new numbers: every figure must live on its source page
    bad = 0
    for fig, src_page in FIGURES:
        s = open(os.path.join(SITE, src_page), encoding="utf-8").read()
        if fig.replace("$", "") not in s.replace("$", ""):
            print("GUARD: %s is attributed to %s, which does not "
                  "contain it" % (fig, src_page))
            bad += 1

    n = pk.check_page(p, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        ("the simulator link", "practice-simulator.html"),
        ("the program-cost link", "mft-programs-california.html"),
        ("the county-pay link", "county-therapist-pay-california.html"),
        ("the deciding-door link", "for/deciding.html"),
        ("the exempt floor", "$70,304"),
        ("the net figure", "$138,940"),
    ], [h for h, _ in JUMPS])
    s = open(p, encoding="utf-8").read()
    # the article only - donor chrome carries scripts whose STRINGS
    # legitimately contain these words (the forgiveness checker's own
    # disclaimer says "not guaranteed current")
    artm = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s)
    text = re.sub(r"<[^>]+>", " ",
                  artm.group(0) if artm else s).lower()
    for phrase in ("is hiring", "has openings", "guaranteed",
                   "you will earn"):
        if phrase in text:
            print("GUARD: %r has no business on an arithmetic page"
                  % phrase)
            n += 1
    art = artm
    if art and "LLC" in art.group(0):
        print("GUARD: 'LLC' in the article")
        n += 1
    if n or bad:
        sys.exit("%d check failure(s)" % (n + bad))
    print("  checks passed, every figure verified on its source page")


if __name__ == "__main__":
    main()
