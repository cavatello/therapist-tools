#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The 1 April 2026 advertising rule, translated into what a profile says.

TIER 2, ITEM 5 of the approved editorial list. 16 CCR section 1811 was
amended effective 1 April 2026, and the Board published a revised fact
sheet and two example sheets alongside it (all Revised 03/2026,
Effective 4/1/2026). Every advertisement - website, directory profile,
social media, business card, email that implies a title - must carry a
fixed set of elements, and an associate's set is LONGER than a
licensee's: employer and a supervision statement on top of name, full
registration title and number. Nobody has translated that into "here is
what your Psychology Today profile must literally say" - which is what
the Board's own example sheets do, and what this page assembles.

SOURCING RULE: everything on this page comes from the Board's own three
publications and the regulation itself, all fetched 16 August 2026. The
Board's example sheets use invented example names; this page states the
PATTERNS instead of reprinting the fictional people, because this site
prints no personal names - the sheets are linked for anyone who wants
the worked examples.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "bbs-advertising-rules-2026.html"
DONOR = "county-job-portals-california.html"

FACT = "https://www.bbs.ca.gov/pdf/publications/adv_guide.pdf"
EX_LIC = "https://www.bbs.ca.gov/pdf/publications/adv_licensees.pdf"
EX_ASC = "https://www.bbs.ca.gov/pdf/publications/adv_associates_trainees.pdf"
REG = "https://www.law.cornell.edu/regulations/california/16-CCR-1811"
S651 = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection."
        "xhtml?sectionNum=651.&lawCode=BPC")

JUMPS = [("what", "What counts as an ad"),
         ("lic", "Licensees: three things"),
         ("assoc", "Associates: five things"),
         ("trainee", "Trainees: five things"),
         ("fails", "How profiles fail"),
         ("sources", "Sources")]


def body():
    o = ['<article class="pk-wrap">']

    o.append('<section class="pk-hero">')
    o.append('<p class="hk">16 CCR &sect;&thinsp;1811, amended &middot; '
             "effective 1 April 2026 &middot; read 16 August 2026</p>")
    o.append("<h1>What your profile must literally say, since "
             "April 2026.</h1>")
    o.append('<p class="hl">The Board rewrote its advertising rule and '
             "republished its fact sheet and example sheets to match, "
             "all effective 1 April 2026. A licensee&rsquo;s ad must "
             "carry three elements; an associate&rsquo;s must carry "
             "five, including an employer name and a supervision "
             "statement; a trainee&rsquo;s five include the "
             "supervisor&rsquo;s license number. And "
             "&ldquo;advertisement&rdquo; includes your website, your "
             "directory profiles and your social media &mdash; not "
             "just print. This page is the rule as a checklist, from "
             "the Board&rsquo;s own publications.</p>")
    o.append('<p class="hj">')
    for h, l in JUMPS:
        o.append('<a href="#%s">%s</a>' % (h, l))
    o.append("</p></section>")

    # ---------------------------------------------------------------- what
    o.append('<section class="pk-sec" id="what">')
    o.append('<p class="pk-k">Scope first</p>')
    o.append('<h2 class="pk-h">Your website is an advertisement. So is '
             "your bio.</h2>")
    o.append('<p class="pk-p">The definition reaches &ldquo;mail, '
             "television, radio, motion picture, newspaper, book, list "
             "or directory of healing arts practitioners, Internet, or "
             "other electronic communication&rdquo; &mdash; plus "
             "business cards, signs and printed material. In practice "
             "that means the places a therapist actually appears: the "
             "practice website, a Psychology Today-style directory "
             "profile, Instagram and LinkedIn bios, and an email "
             "signature that states a title. The Board&rsquo;s FAQ "
             "adds two operating rules for the web: on a website the "
             "required elements must be easy to find and appear near "
             "each other, and on space-limited social media the "
             "required information must still appear &mdash; a link to "
             "a compliant page is the accepted escape valve.</p>")
    o.append("</section>")

    # ----------------------------------------------------------------- lic
    o.append('<section class="pk-sec" id="lic">')
    o.append('<p class="pk-k">Licensed &middot; three required '
             "elements</p>")
    o.append('<h2 class="pk-h">Name as filed, full title or allowed '
             "abbreviation, license number.</h2>")
    o.append(pk.numbered([
        ("1", "First and last name, as filed with the Board.",
         "The name on the license, not only a nickname or a shortened "
         "professional name. A preferred name may appear alongside it, "
         "but the filed name has to be there."),
        ("2", "The complete title, or an allowed abbreviation.",
         "&ldquo;Licensed Marriage and Family Therapist&rdquo; or "
         "LMFT/MFT; &ldquo;Licensed Clinical Social Worker&rdquo; or "
         "LCSW; &ldquo;Licensed Professional Clinical Counselor&rdquo; "
         "or LPCC; &ldquo;Licensed Educational Psychologist&rdquo; or "
         "LEP. Invented abbreviations are the classic citation."),
        ("3", "The license number.",
         "On the profile, not behind a link. The pattern the "
         "Board&rsquo;s example sheet blesses is simply: filed name, "
         "title, number."),
    ]))
    o.append('<p class="pk-p">The Board&rsquo;s worked examples for '
             "licensees &mdash; compliant and non-compliant side by "
             "side &mdash; are in %s.</p>"
             % ('<a href="%s" target="_blank" rel="noopener noreferrer">'
                "its licensee example sheet</a>" % EX_LIC))
    o.append("</section>")

    # --------------------------------------------------------------- assoc
    o.append('<section class="pk-sec" id="assoc">')
    o.append('<p class="pk-k">Registered associates &middot; five '
             "required elements</p>")
    o.append('<h2 class="pk-h">Everything a licensee shows, plus your '
             "employer, plus a supervision statement.</h2>")
    o.append(pk.numbered([
        ("1", "First and last name, as filed with the Board.",
         "Same rule as licensees: a nickname or a former name may "
         "appear, but only alongside the registered name."),
        ("2", "The complete registration title.",
         "&ldquo;Registered Associate Marriage and Family "
         "Therapist&rdquo; (or Registered Associate MFT), "
         "&ldquo;Registered Associate Clinical Social Worker,&rdquo; "
         "or &ldquo;Registered Associate Professional Clinical "
         "Counselor&rdquo; (or Registered Associate PCC). AMFT, ASW "
         "and APCC are allowed ONLY when the full title also appears "
         "&mdash; the abbreviation alone is not compliant."),
        ("3", "The registration number.",
         "Called a registration, not a license &mdash; the "
         "Board&rsquo;s non-compliant examples flag &ldquo;License "
         "No.&rdquo; on an associate as misleading."),
        ("4", "The employer&rsquo;s name - or the volunteer entity.",
         "The rule&rsquo;s subdivision (b): a registrant advertises "
         "as somebody&rsquo;s supervisee, never as a freestanding "
         "practice."),
        ("5", "A supervision statement.",
         "&ldquo;Supervised by a licensed person&rdquo; is the minimum "
         "the fact sheet accepts; &ldquo;Supervised by a Licensed "
         "Marriage and Family Therapist&rdquo; or naming the "
         "supervisor with their title are the fuller forms in the "
         "example sheet. Vague forms like &ldquo;practicing under "
         "supervision&rdquo; appear in the NON-compliant column."),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------- trainee
    o.append('<section class="pk-sec" id="trainee">')
    o.append('<p class="pk-k">Trainees &middot; five required '
             "elements</p>")
    o.append('<h2 class="pk-h">No abbreviations at all, and the '
             "supervisor&rsquo;s number goes in.</h2>")
    o.append('<p class="pk-p">A trainee&rsquo;s advertisement must '
             "spell out &ldquo;marriage and family therapist "
             "trainee&rdquo; in full &mdash; no abbreviation of the "
             "trainee title is permitted &mdash; plus the employer or "
             "volunteer entity, a statement of licensed supervision, "
             "the supervisor&rsquo;s license designation, and the "
             "supervisor&rsquo;s license number. The minimum compliant "
             "shape from the Board&rsquo;s example sheet: full name, "
             "the spelled-out trainee title, the placement&rsquo;s "
             "name, and &ldquo;Supervised by a&rdquo; plus the "
             "supervisor&rsquo;s license type and number.</p>")
    o.append("</section>")

    # --------------------------------------------------------------- fails
    o.append('<section class="pk-sec" id="fails">')
    o.append('<p class="pk-k">The non-compliant column</p>')
    o.append('<h2 class="pk-h">How real-shaped profiles fail, in the '
             "Board&rsquo;s own examples.</h2>")
    o.append(pk.numbered([
        ("1", "An invented abbreviation.",
         "MFTA and ACSW both appear in the Board&rsquo;s non-compliant "
         "examples. The allowed set is closed: if it is not on the "
         "list, spelling it out is the only safe move."),
        ("2", "An abbreviation doing the whole job.",
         "AMFT on its own fails - the full registration title has to "
         "appear somewhere on the same advertisement."),
        ("3", "&ldquo;License No.&rdquo; on a registration.",
         "An associate holds a registration; calling it a license in "
         "an ad is flagged as implying licensure."),
        ("4", "&ldquo;MFT&rdquo; inside an email address or handle.",
         "The example sheet flags an address of the form "
         "name.MFT@&hellip; on a pre-licensed person as implying "
         "licensure - handles and addresses are part of the ad."),
        ("5", "The supervision statement in fine print, or missing.",
         "A supervision statement rendered in tiny type draws the same "
         "flag as omitting it."),
        ("6", "A nickname or former name standing alone.",
         "Preferred names are fine ALONGSIDE the filed name, never "
         "instead of it."),
        ("7", "Outcome promises.",
         "&ldquo;Cure&rdquo; language fails under Business and "
         "Professions Code &sect;&thinsp;651&rsquo;s false-or-"
         "misleading standard, which rides along with every element "
         "above."),
    ]))
    o.append('<p class="pk-p">The Board&rsquo;s stated posture on '
             "getting it wrong: a notification first, with a chance to "
             "correct before formal action in many cases &mdash; and "
             "citation authority under &sect;&thinsp;651 behind it. "
             "The fix costs an afternoon; the audit costs more.</p>")
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The Board&rsquo;s own publications, all Revised 03/2026, "
         "Effective 4/1/2026, fetched 16 August 2026", [
            ("The Advertising Fact Sheet and FAQ - the requirement "
             "lists this page restates", FACT),
            ("Advertising Examples for Associates and Trainees - the "
             "worked compliant and non-compliant profiles", EX_ASC),
            ("Advertising Examples for Licensees", EX_LIC),
        ]),
        ("The law under the publications", [
            ("16 CCR &sect;&thinsp;1811 - the advertising regulation "
             "itself", REG),
            ("Business and Professions Code &sect;&thinsp;651 - the "
             "false-or-misleading standard every ad also answers to",
             S651),
        ]),
    ], note="This page restates the Board's own published requirements "
            "as a checklist and adds nothing to them. Where your "
            "situation is unusual - multiple employers, a name change "
            "mid-registration, a shared group website - the fact sheet "
            "and the Board's licensing staff are the authority, not "
            "this page. Nothing here is legal advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "The BBS advertising rule, effective April 2026: a checklist",
    "What every California therapist ad must contain since 1 April 2026 "
    "- three elements for licensees, five for associates including the "
    "supervision statement, five for trainees - from the Board's own "
    "fact sheet and example sheets.",
    "practice", "reference",
    "What must my therapist profile legally say in California?",
    "The required elements for licensees, associates and trainees, and "
    "the seven ways the Board's own examples show profiles failing",
    "Three required elements for licensees, five for associates",
    weight=4)


def main():
    print("the advertising-rules page")
    html_body, nsrc = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links,
                       scripts)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    n = pk.check_page(p, [
        ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
        ("the fact sheet link", "adv_guide.pdf"),
        ("the associate examples link", "adv_associates_trainees.pdf"),
        ("the 1811 regulation link", "16-CCR-1811"),
        ("the 651 statute link", "sectionNum=651."),
        ("the effective date", "1 April 2026"),
    ], [h for h, _ in JUMPS])
    s = open(p, encoding="utf-8").read()
    artm = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s)
    text = re.sub(r"<[^>]+>", " ", artm.group(0)).lower()
    # the Board's fictional example names must not have leaked in
    for name in ("kyung-soon", "rafael", "jackson clarke", "keisha",
                 "janelle", "rashida", "aurelias", "sharma"):
        if name in text:
            print("GUARD: example-sheet name %r leaked into the "
                  "article" % name)
            n += 1
    if "LLC" in artm.group(0):
        print("GUARD: 'LLC' in the article")
        n += 1
    if n:
        sys.exit("%d check failure(s)" % n)
    print("  checks passed, no example names leaked")


if __name__ == "__main__":
    main()
