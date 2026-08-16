#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The telehealth standard of practice, and what actually changed in 2026.

TIER 2, ITEM 6 of the approved editorial list. 16 CCR section 1815.5 was
amended, OAL-approved 19 August 2025, effective 1 January 2026. The
research pack this page was queued from framed the per-session duty to
verbally obtain and document the client's full name and present location
as the new thing. IT IS NOT NEW. It has been in subdivision (d)(1) since
the section took effect on 1 July 2016, and the Board's own 2016 adopted
text carries it word for word.

Nor is the out-of-state-client subdivision new: (e) is in the 2016
adopted text too. Both corrections were made against the Board's own
1815_ooa.pdf on 16 August 2026, and the Final Statement of Reasons for
the 2025 rulemaking never mentions either provision - because the
rulemaking did not touch them.

What DID change, per the Notice of Approval's adopted text:

  (a)     "a valid and current license or registration" gains "and
          active".
  (d)(3)  "Utilize industry best practices for telehealth ..." is
          RETAINED - it was not replaced - and a second duty is added
          after it: comply with the privacy, confidentiality and
          security laws governing medical information and PHI,
          naming the Confidentiality of Medical Information Act and
          HIPAA's security standards at 45 C.F.R. 164.302-164.318.
  throughout: "he or she" becomes "they".

That is the whole amendment. So this page's job is subtraction: it says
what changed, says plainly that the duty most people believe is new is a
decade old, and then restates the section that is actually in force. A
guard below fails the build if the page ever claims otherwise.

SOURCING RULE: the amendment comes from the Board's Notice of Approval
(which carries the adopted text) and the Final Statement of Reasons; the
2016 baseline comes from the Board's own 2016 adopted text. Cornell's
section 1815.5 page still showed the 2016 text when this was written on
16 August 2026, so it is cited as the baseline it accurately is, never
as the current rule.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "telehealth-rules-california-therapist.html"
DONOR = "bbs-advertising-rules-2026.html"

NOA = "https://www.bbs.ca.gov/pdf/telehealth_noa.pdf"
FSOR = "https://www.bbs.ca.gov/pdf/telehealth_fsor.pdf"
ISOR = "https://www.bbs.ca.gov/pdf/regulation/pending/telehealth_isor.pdf"
OOA16 = "https://www.bbs.ca.gov/pdf/regulation/2016/1815_ooa.pdf"
OAL16 = "https://www.bbs.ca.gov/pdf/regulation/2016/1815_oalapproval.pdf"
CORNELL = "https://www.law.cornell.edu/regulations/california/16-CCR-1815.5"
S2290 = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection."
         "xhtml?sectionNum=2290.5.&lawCode=BPC")
CMIA = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection."
        "xhtml?sectionNum=56.05.&lawCode=CIV")
CFR306 = "https://www.law.cornell.edu/cfr/text/45/164.306"
CFR308 = "https://www.law.cornell.edu/cfr/text/45/164.308"
CFR310 = "https://www.law.cornell.edu/cfr/text/45/164.310"
CFR312 = "https://www.law.cornell.edu/cfr/text/45/164.312"
CFR314 = "https://www.law.cornell.edu/cfr/text/45/164.314"
CFR316 = "https://www.law.cornell.edu/cfr/text/45/164.316"

HOURS = "associate-hours-telehealth-out-of-state.html"

JUMPS = [("changed", "What changed"),
         ("old", "What did not"),
         ("session", "Every session"),
         ("intake", "At intake"),
         ("outside", "Clients elsewhere"),
         ("security", "The security standard"),
         ("sources", "Sources")]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "16 CCR &sect;&thinsp;1815.5, amended &middot; effective "
        "1 January 2026 &middot; read 16 August 2026",
        "The telehealth rule changed in January. Almost nothing you "
        "think changed, changed.",
        "Two subdivisions of the telehealth standard of practice were "
        "amended effective 1 January 2026, and one of them is a single "
        "added word. The duty people describe as the new one &mdash; "
        "verbally taking the client&rsquo;s full name and present "
        "location at the start of every session &mdash; has been in "
        "force since 1 July 2016. Here is the amendment, and then the "
        "section as it actually reads.",
        [("2", "subdivisions the 2026 amendment touched"),
         ("1 Jul 2016", "when the per-session duty began"),
         ("&sect;&sect;&thinsp;164.302&ndash;.318", "the security rule "
          "now named in the regulation"),
         ("0", "new duties in subdivision (c) or (e)")],
        JUMPS))

    # ------------------------------------------------------------- changed
    o.append('<section class="pk-sec" id="changed">')
    o.append('<p class="pk-k">The amendment, in full</p>')
    o.append('<h2 class="pk-h">One added word, and one added '
             "duty.</h2>")
    o.append('<p class="pk-p">The Board&rsquo;s rulemaking was approved '
             "by the Office of Administrative Law on 19 August 2025 "
             "and took effect on 1 January 2026. The adopted text "
             "attached to the Notice of Approval changes the section "
             "in exactly these places.</p>")
    o.append(pk.numbered([
        ("1", "Subdivision (a) gains &ldquo;and active&rdquo;.",
         "The licensure requirement for treating a client physically "
         "located in California now reads &ldquo;a valid and current "
         "and active license or registration issued by the "
         "Board&rdquo;. A registration that has lapsed or gone "
         "inactive was never a basis for practice; the word closes "
         "the gap on paper."),
        ("2", "Subdivision (d)(3) gains a second sentence.",
         "The industry-best-practices duty is <b>kept</b>, not "
         "replaced &mdash; a point worth being exact about, because "
         "the amendment is often described as a swap. What follows it "
         "is new: a duty to comply with the privacy, confidentiality "
         "and security laws governing a client&rsquo;s medical "
         "information and protected health information, with two of "
         "them named. Those two are the Confidentiality of Medical "
         "Information Act and HIPAA&rsquo;s security standards at "
         "45 C.F.R. &sect;&sect;&thinsp;164.302 through 164.318."),
        ("3", "The pronouns are modernized.",
         "&ldquo;He or she&rdquo; becomes &ldquo;they&rdquo; in "
         "subdivisions (c)(3) and (d). Nothing about the duties "
         "themselves moves with it."),
    ]))
    o.append('<p class="pk-p">That is the entire amendment. The '
             "Board&rsquo;s own Final Statement of Reasons, which "
             "answers the comments the rulemaking drew, discusses "
             "nothing but the privacy and security language &mdash; "
             "no session documentation, no consent, no jurisdiction. "
             "If a duty is not in the three items above, it did not "
             "arrive in January.</p>")
    o.append("</section>")

    # ----------------------------------------------------------------- old
    o.append('<section class="pk-sec" id="old">')
    o.append('<p class="pk-k">The correction</p>')
    o.append('<h2 class="pk-h">The duty you think is new is a decade '
             "old.</h2>")
    o.append('<p class="pk-p">The requirement being circulated as the '
             "January change is subdivision (d)(1): verbally obtain "
             "from the client, and document, the client&rsquo;s full "
             "name and address of present location, at the beginning "
             "of each telehealth session. It is not new. It is in the "
             "text the Board adopted in 2016, word for word, and that "
             "section took effect on 1 July 2016. The 2025 rulemaking "
             "did not amend it, and the Final Statement of Reasons "
             "does not mention it.</p>")
    o.append(pk.quote(
        "Subdivision (d)(1), unchanged since 2016",
        ["&ldquo;Verbally obtain from the client and document the "
         "client&rsquo;s full name and address of present location, "
         "at the beginning of each telehealth session.&rdquo;"]))
    o.append('<p class="pk-p">The same is true of subdivision (e), the '
             "one about clients located in another jurisdiction. It is "
             "sometimes described as a 2026 clarification. It is in "
             "the 2016 adopted text as well.</p>")
    o.append('<p class="pk-p">Which is a more uncomfortable finding '
             "than a new rule would be. A new rule is something to "
             "start doing. A ten-year-old rule that a lot of "
             "practices have not been following is something to "
             "reconcile &mdash; and unprofessional conduct under "
             "subdivision (f) does not distinguish between the two.</p>")
    o.append("</section>")

    # ------------------------------------------------------------- session
    o.append('<section class="pk-sec" id="session">')
    o.append('<p class="pk-k">Subdivision (d) &middot; every single '
             "session</p>")
    o.append('<h2 class="pk-h">Three things, every time, not once at '
             "the start of the work.</h2>")
    o.append('<p class="pk-p">Subdivision (d) is written as a '
             "per-session duty &mdash; &ldquo;each time a licensee or "
             "registrant provides services via telehealth&rdquo; "
             "&mdash; which is what separates it from the intake list "
             "below.</p>")
    o.append(pk.numbered([
        ("1", "Name and present location, verbally, and documented.",
         "Both halves matter and both are commonly half-done. It is "
         "not enough to know where the client lives; the duty is the "
         "address of the location they are in right now, taken out "
         "loud, and written down. From 2016, not 2026."),
        ("2", "Assess whether the client is appropriate for "
              "telehealth.",
         "Explicitly including, in the regulation&rsquo;s own words, "
         "consideration of the client&rsquo;s psychosocial situation. "
         "It is a per-session judgment, not an intake screen that "
         "carries forward untouched."),
        ("3", "Industry best practices for telehealth &mdash; and, "
              "since January, named privacy law.",
         "The confidentiality and security of the communication "
         "medium, plus the compliance duty described in the security "
         "section below."),
    ]))
    o.append("</section>")

    # -------------------------------------------------------------- intake
    o.append('<section class="pk-sec" id="intake">')
    o.append('<p class="pk-k">Subdivision (c) &middot; on initiation</p>')
    o.append('<h2 class="pk-h">Four things when the telehealth work '
             "begins.</h2>")
    o.append(pk.numbered([
        ("1", "Informed consent under Business and Professions Code "
              "&sect;&thinsp;2290.5.",
         "The regulation borrows the statute&rsquo;s consent standard "
         "rather than writing its own, so the statute is the thing to "
         "read for what consent has to cover and how it is "
         "documented."),
        ("2", "Inform the client of the risks and limitations of "
              "treatment by telehealth.",
         "Separate from consent in the text, and separate in "
         "practice: a signature on a consent form is not by itself a "
         "record that the risks were described."),
        ("3", "Give the client your number and the type of license or "
              "registration.",
         "The number and the type. For an associate that means the "
         "registration number and the fact that it is a registration "
         "&mdash; the same distinction the advertising rule turns on."),
        ("4", "Document reasonable efforts to find emergency "
              "resources in the client&rsquo;s area.",
         "The regulation asks for the documented effort, in the "
         "client&rsquo;s geographic area &mdash; which is the reason "
         "the per-session location duty in (d)(1) exists at all. If "
         "the client moves between sessions, the resources you "
         "documented may no longer be theirs."),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------- outside
    o.append('<section class="pk-sec" id="outside">')
    o.append('<p class="pk-k">Subdivision (e) &middot; not new</p>')
    o.append('<h2 class="pk-h">A client outside California is the '
             "other state&rsquo;s question.</h2>")
    o.append('<p class="pk-p">Subdivision (e): a California licensee '
             "or registrant may provide telehealth services to a "
             "client located in another jurisdiction only if they "
             "meet that jurisdiction&rsquo;s requirements to provide "
             "services lawfully there, and telehealth delivery is "
             "allowed there. California&rsquo;s permission is not the "
             "operative one. The other state&rsquo;s is, and "
             "California enforces the answer through subdivision (f).</p>")
    o.append(pk.callout(
        "Two different questions, and people run them together",
        ["<b>Where the client is</b> decides which state&rsquo;s "
         "practice act applies. That is this page, and subdivision "
         "(a) and (e) answer it.",
         "<b>Where you are sitting</b> decides something else "
         "entirely, and for an associate it decides whether the hours "
         "count. No California statute addresses it. That question is "
         "worked in full on "
         '<a href="%s">the out-of-state hours page</a>.' % HOURS]))
    o.append("</section>")

    # ------------------------------------------------------------ security
    o.append('<section class="pk-sec" id="security">')
    o.append('<p class="pk-k">The one real change</p>')
    o.append('<h2 class="pk-h">What naming the Security Rule actually '
             "asks of a solo practice.</h2>")
    o.append('<p class="pk-p">Before January, (d)(3) asked for '
             "&ldquo;industry best practices&rdquo; &mdash; a "
             "standard with no citation behind it, which is exactly "
             "the objection the Board answered. It now also points at "
             "two named bodies of law. Neither is new law; what is "
             "new is that failing them is now unprofessional conduct "
             "in front of the Board, not only a matter for the "
             "agencies that enforce them.</p>")
    o.append(pk.numbered([
        ("1", "The Confidentiality of Medical Information Act.",
         "Civil Code part 2.6, beginning at &sect;&thinsp;56, with "
         "respect to a client&rsquo;s medical information as "
         "&sect;&thinsp;56.05 defines it. California&rsquo;s own "
         "confidentiality statute, which applies to a great many "
         "practices that are not HIPAA covered entities."),
        ("2", "HIPAA&rsquo;s security standards, Subpart C.",
         "45 C.F.R. &sect;&sect;&thinsp;164.302 through 164.318 "
         "&mdash; the Security Rule, and only the Security Rule. The "
         "Privacy Rule is not what the regulation names here."),
    ]))
    o.append('<p class="pk-p">Subpart C is short, and it is organized '
             "into four groups plus a documentation duty. In the "
             "order the regulations run: the general rules and the "
             "flexibility-of-approach standard at "
             "&sect;&thinsp;164.306; administrative safeguards at "
             "&sect;&thinsp;164.308, which is where the required risk "
             "analysis and risk management live, along with workforce "
             "training, incident procedures and contingency planning, "
             "and at (b) the requirement that a business associate "
             "give satisfactory written assurances; physical "
             "safeguards at &sect;&thinsp;164.310; technical "
             "safeguards at &sect;&thinsp;164.312, whose five "
             "standards are access control, audit controls, "
             "integrity, authentication and transmission security; "
             "organizational requirements including the contract "
             "terms themselves at &sect;&thinsp;164.314; and "
             "policies, procedures and documentation at "
             "&sect;&thinsp;164.316.</p>")
    o.append(pk.checklist(
        "The questions this makes concrete",
        ["Is there a written risk analysis for the practice, or only "
         "an assumption that the platform handles it? "
         "&sect;&thinsp;164.308(a)(1) asks for the analysis by name.",
         "Is there a signed business associate agreement with the "
         "video platform, the electronic record, the billing service "
         "and the transcription tool &mdash; each of them, not the "
         "one that was easiest to get?",
         "Do the written policies and procedures exist as documents, "
         "and are they retained? &sect;&thinsp;164.316 is a "
         "documentation standard, and documentation is the part a "
         "one-person practice most often skips.",
         "If a client is in another state, does that state&rsquo;s "
         "law reach further than California&rsquo;s &mdash; and have "
         "you checked, given that subdivision (e) makes their rules "
         "the ones that decide?"]))
    o.append('<p class="pk-p">A note on what this page will not tell '
             "you: whether a particular platform satisfies any of "
             "this. Vendors describe themselves as HIPAA compliant, "
             "and that phrase has no regulatory meaning on its own "
             "&mdash; the duties above attach to the practice, and "
             "the agreement with the vendor is one of them, not a "
             "substitute for the rest.</p>")
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The 2025 rulemaking - approved 19 August 2025, effective "
         "1 January 2026, read 16 August 2026", [
            ("Notice of Approval, Form 400 and the adopted text of "
             "16 CCR &sect;&thinsp;1815.5 - the amendment this page "
             "describes", NOA),
            ("Final Statement of Reasons - the Board's answers to "
             "comment, which discuss the privacy and security "
             "language and nothing else", FSOR),
            ("Initial Statement of Reasons", ISOR),
        ]),
        ("The 2016 baseline, which is where most of the section "
         "actually comes from", [
            ("The adopted text of &sect;&thinsp;1815.5 as filed in "
             "2016 - carries the per-session name and location duty "
             "and the out-of-state subdivision", OOA16),
            ("The 2016 Notice of Approval, effective 1 July 2016",
             OAL16),
            ("16 CCR &sect;&thinsp;1815.5 at Cornell - accurate as "
             "the 2016 baseline; it had not been updated for the "
             "2026 amendment when this page was written", CORNELL),
        ]),
        ("The law the section points at", [
            ("Business and Professions Code &sect;&thinsp;2290.5 - "
             "the telehealth definition and the consent standard "
             "subdivision (c)(1) borrows", S2290),
            ("Civil Code &sect;&thinsp;56.05 - the definition of "
             "medical information under the Confidentiality of "
             "Medical Information Act", CMIA),
            ("45 C.F.R. &sect;&thinsp;164.306 - general rules and "
             "flexibility of approach", CFR306),
            ("45 C.F.R. &sect;&thinsp;164.308 - administrative "
             "safeguards, including the risk analysis and the "
             "business associate requirement", CFR308),
            ("45 C.F.R. &sect;&thinsp;164.310 - physical safeguards",
             CFR310),
            ("45 C.F.R. &sect;&thinsp;164.312 - technical safeguards",
             CFR312),
            ("45 C.F.R. &sect;&thinsp;164.314 - organizational "
             "requirements and business associate contract terms",
             CFR314),
            ("45 C.F.R. &sect;&thinsp;164.316 - policies, procedures "
             "and documentation", CFR316),
        ]),
    ], note="This page restates a regulation and the Board's own "
            "rulemaking record; it adds no requirements of its own and "
            "it is not legal advice. Where a source disagrees with a "
            "summary you have read elsewhere, the Board's adopted "
            "text is the authority. Anything turning on your specific "
            "platform, your specific records, or a client in a "
            "specific other state is a question for a lawyer who "
            "practices in this area, not for a web page.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "California telehealth rules for therapists: what changed in 2026",
    "16 CCR 1815.5 was amended effective 1 January 2026 - one added "
    "word and one added duty naming CMIA and the HIPAA Security Rule. "
    "The per-session name and location requirement people call new has "
    "been in force since 2016.",
    "practice", "reference",
    "What are the telehealth rules for California therapists in 2026?",
    "The two subdivisions that actually changed, the decade-old duty "
    "most people think is new, and what the named Security Rule asks "
    "of a solo practice",
    "2 subdivisions changed; the rest dates to 2016",
    weight=4)


def main():
    print("the telehealth standards page")
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
        ("the Notice of Approval link", "telehealth_noa.pdf"),
        ("the Final Statement of Reasons link", "telehealth_fsor.pdf"),
        ("the 2016 adopted-text link", "1815_ooa.pdf"),
        ("the Security Rule range", "164.302"),
        ("the 164.316 documentation cite", "164.316"),
        ("the 2290.5 consent statute", "sectionNum=2290.5."),
        ("the CMIA definition statute", "sectionNum=56.05."),
        ("the amendment date", "1 January 2026"),
        ("the 2016 effective date", "1 July 2016"),
        ("the link to the out-of-state hours page", HOURS),
    ], [h for h, _ in JUMPS])

    s = open(p, encoding="utf-8").read()
    artm = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s)
    art = artm.group(0)
    text = re.sub(r"<[^>]+>", " ", art)
    flat = re.sub(r"\s+", " ", text).lower()

    # THE GUARD THIS PAGE EXISTS FOR. The queued research pack called
    # the per-session duty new. If an edit ever reintroduces that
    # claim, the build stops.
    if "it is not new" not in flat:
        print("GUARD: the page no longer states that the per-session "
              "duty is not new")
        n += 1
    for wrong in ("new per-session", "newly requires", "new requirement "
                  "to verbally", "as of january, therapists must now "
                  "verbally"):
        if wrong in flat:
            print("GUARD: %r reintroduces the corrected framing" % wrong)
            n += 1
    # "replaced" would restate the other correction backwards: the
    # industry-best-practices sentence was kept, not swapped out.
    if "replaces industry best practices" in flat or \
       "replaced industry best practices" in flat:
        print("GUARD: the page claims the best-practices duty was "
              "replaced; it was retained")
        n += 1

    # House content rules.
    if "LLC" in art:
        print("GUARD: 'LLC' in the article")
        n += 1
    for banned in ("guaranteed", "is hiring", "has openings",
                   "accepting new"):
        if banned in flat:
            print("GUARD: banned phrase %r in the article" % banned)
            n += 1

    if n:
        sys.exit("%d check failure(s)" % n)
    print("  checks passed - amendment scoped to 2 subdivisions, "
          "2016 baseline stated")


if __name__ == "__main__":
    main()
