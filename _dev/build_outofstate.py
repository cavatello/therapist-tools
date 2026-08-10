#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Can you finish your hours from another state? The Board has answered, five times.

THE QUESTION THIS ANSWERS

From a California associate support group: "I have yet to find anyone who has
ever successfully completed their associateship via telehealth [from outside
California]." Nobody in the thread produced a rule either way, and the
prevailing assumption was that it must be forbidden.

It is not forbidden. The Board has published an answer in five separate
documents, the most recent marked new in February 2026, and the answer is yes,
with conditions. The thread was describing what employers permit, and treating
it as what the law allows.

THE STRUCTURE THIS PAGE IMPOSES

Two questions get merged in every one of these conversations and they have
different answers from different bodies of law:

  A. Where is the CLIENT? That decides which state's practice act applies.
     16 CCR 1815.5(a) - a client physically in California needs a provider
     with a California license OR REGISTRATION. An active AMFT, ASW or APCC
     registration satisfies it. This rule never bends.

  B. Where are YOU? That decides whether the hours count. No California
     statute addresses it at all. The only "location of services" section in
     the whole scheme, BPC 4980.43.4(a), delegates the question to your
     employer.

Separating those two is the page's entire job.

THE THREE CORRECTIONS THIS PAGE MAKES

1. The temporary practice allowance is BPC 4980.11, it runs INTO California,
   and the Board states in terms that a pre-licensed associate cannot get one.
   It is the most commonly cited and least relevant provision here.
2. The Out-of-State Experience Verification form is not for you. It is filed
   with a Path B application by somebody who was never a California
   registrant, and its supervisor attestation certifies compliance with
   another jurisdiction's requirements.
3. There is no compact. California is not in the Counseling Compact or the
   Social Work Licensure Compact, none of them covers pre-licensed people, and
   there is no MFT compact operating anywhere.

WHAT THE BOARD HAS NOT ANSWERED, PRINTED AS SUCH

Whether the state you are physically sitting in wants its own credential. The
BBS has no jurisdiction over that and does not pretend to; 16 CCR 1815.5(e)
covers only the mirror-image case. That is the real exposure and it is the
page's headline caveat rather than a footnote.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pagekit as pk

PAGE = "associate-hours-telehealth-out-of-state.html"
DONOR = "hiring-first-associate-california-therapist.html"

HOURS = "amft-3000-hours-california.html"
REMOTE = "therapist-working-remotely-california.html"
HIRING = "hiring-first-associate-california-therapist.html"
UNPAID = "associate-unpaid-hours-california.html"
TRACKERS = "associate-hours-trackers-compared.html"

LAWBOOK = "https://www.bbs.ca.gov/pdf/publications/lawsregs.pdf"
LAWBOOK_ED = "January 2026"

TEMP_DAYS = 30
TOTAL_HOURS = 3000

# The five published Board answers, oldest revision last. Each is quoted rather
# than summarised, because a paraphrase of a regulator's answer is not the
# regulator's answer, and this page's whole value is that the answer exists.
ANSWERS = [
    ("FAQs for Supervisors, question 22", "new February 2026",
     "A California Associate whose registration number is current and active, "
     "or an MFT Trainee, <b>can practice with clients located in California "
     "while the supervisee is out-of-state or in another country if the "
     "supervisor permits it.</b>",
     "https://www.bbs.ca.gov/pdf/publications/faqs_for_supervisors.pdf"),
    ("ASW FAQ, question 21", "revised January 2026",
     "Asked whether an associate traveling out of state may serve a "
     "California client and count the hours: <b>&ldquo;Yes&rdquo;</b>, "
     "subject to the four conditions below. The same document adds that "
     "<b>there is no limit on the number of telehealth hours</b> that can "
     "count toward the supervised experience requirement.",
     "https://www.bbs.ca.gov/pdf/publications/asw_faq.pdf"),
    ("MFT FAQ, question 31", "revised February 2025",
     "The same question and the same answer, citing BPC &sect;&sect;2290.5, "
     "4980.42, 4980.43 and 4980.43.2 and 16 CCR &sect;1815.5.",
     "https://www.bbs.ca.gov/pdf/publications/mft_faq.pdf"),
    ("APCC FAQ, question 22", "revised February 2025",
     "The same question and the same answer for professional clinical "
     "counselor associates, citing BPC &sect;&sect;2290.5, 4999.46 and "
     "4999.46.2.",
     "https://www.bbs.ca.gov/pdf/publications/pcci_faq.pdf"),
    ("Telehealth FAQ", "last updated June 2025",
     "<b>&ldquo;A California associate whose registration number is current "
     "and active can continue to practice with clients located in California "
     "while the associate is out-of-state if the supervisor permits "
     "it.&rdquo;</b>",
     "https://www.bbs.ca.gov/pdf/publications/telehealth_faq.pdf"),
]

JUMPS = [
    ("two", "Two questions, not one"),
    ("client", "Where the client is"),
    ("you", "Where you are"),
    ("conditions", "The four conditions"),
    ("open", "What nobody has answered"),
    ("wrong", "Three things that do not apply"),
]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Out-of-state hours &middot; telehealth &middot; checked %s"
        % pk.CHECKED,
        "Can you finish your hours from another state?",
        "The prevailing belief in associate groups is that you cannot. "
        "<b>The Board has published the opposite answer %d times</b>, most "
        "recently in February 2026 &mdash; and there is a real risk in this, "
        "but it is not the one people are worried about." % len(ANSWERS),
        [("%d" % len(ANSWERS), "published Board answers"),
         ("Feb 2026", "the most recent"),
         ("0", "statutes limiting where you sit"),
         ("1", "question nobody in California can answer")],
        JUMPS))

    # ------------------------------------------------------------ the question
    o.append('<section class="pk-sec">')
    o.append(pk.quote(
        "The post this page was written for",
        ["I have yet to find anyone who has ever successfully completed their "
         "associateship via telehealth."]))
    o.append('<p class="pk-d">That is almost certainly a true observation and '
             "a false conclusion. It describes what employers have been "
             "willing to arrange. It does not describe a rule, and the rules "
             "that do exist point the other way.</p>")

    o.append('<p class="pk-k">The reframe</p>')
    o.append('<h2 class="pk-h" id="two">It is two questions, and they have '
             "different answers from different bodies of law.</h2>")
    o.append(pk.numbered([
        ("A", "Where is the client?",
         "This decides <b>which state&rsquo;s practice act applies</b>. It is "
         "the question with a hard answer, it is answered by regulation, and "
         "it does not bend."),
        ("B", "Where are you?",
         "This decides <b>whether the hours count</b> toward your %s. No "
         "California statute addresses it. The only section in the entire "
         "scheme headed &ldquo;location of services&rdquo; hands the question "
         "to your employer." % format(TOTAL_HOURS, ",d")),
    ]))
    o.append('<p class="pk-d">Almost every confused conversation about this '
             "is two people answering different questions. Below, they are "
             "separated.</p>")
    o.append("</section>")

    # ------------------------------------------------------------- the client
    o.append('<section class="pk-sec" id="client">')
    o.append('<p class="pk-k">Question A</p>')
    o.append('<h2 class="pk-h">Where the client is: the rule that never '
             "bends.</h2>")
    o.append(pk.callout(
        "16 CCR &sect;1815.5(a)",
        ["All persons practicing marriage and family therapy, educational "
         "psychology, clinical social work or professional clinical "
         "counseling by telehealth <b>with a client who is physically "
         "located in this State must have a current and active license "
         "<i>or registration</i> issued by the Board</b>.",
         "The words that matter are <b>&ldquo;or registration&rdquo;</b>. "
         "Your active AMFT, ASW or APCC registration satisfies this rule on "
         "its own terms. Nothing in it is about where the provider is "
         "sitting; the whole subdivision is about the client."]))
    o.append('<p class="pk-d">Subdivision (b) adds that telehealth services '
             "sit within the Board&rsquo;s jurisdiction exactly as in-person "
             "services do &mdash; the same statutes, the same regulations, "
             "the same standards of care. And the definition of telehealth "
             "the regulation borrows, at BPC &sect;2290.5, is built around "
             "the client being at an &ldquo;originating site&rdquo; and the "
             "provider at a &ldquo;distant site&rdquo;. The architecture of "
             "the law already assumes the two are in different places.</p>")
    o.append('<p class="pk-d">The mirror case is covered too, and it is worth '
             "knowing which way it runs. <b>&sect;1815.5(e)</b>: a California "
             "licensee or registrant may serve a client located in another "
             "jurisdiction only if they meet that jurisdiction&rsquo;s "
             "requirements and that jurisdiction allows telehealth. So "
             "California does regulate you when your <i>client</i> leaves. "
             "It says nothing about when <i>you</i> do.</p>")
    o.append("</section>")

    # ----------------------------------------------------------------- you
    o.append('<section class="pk-sec" id="you">')
    o.append('<p class="pk-k">Question B</p>')
    o.append('<h2 class="pk-h">Where you are: no statute, and five published '
             "answers.</h2>")
    o.append('<p class="pk-d">The supervised-experience sections &mdash; BPC '
             "&sect;4980.43 for MFTs, &sect;4996.23 for social workers, "
             "&sect;4999.46 for clinical counselors &mdash; contain no "
             "reference to California, to state lines, to residence or to "
             "location of any kind. They are hour counts, week counts and "
             "category caps. That is a verified absence, not an "
             "oversight.</p>")
    o.append(pk.callout(
        "BPC &sect;4980.43.4(a) &mdash; the section actually headed "
        "&ldquo;location of services&rdquo;",
        ["&ldquo;A trainee, associate, or applicant for licensure shall only "
         "perform mental health and related services <b>at the places where "
         "their employer permits business to be conducted</b>.&rdquo;",
         "The identical sentence appears at &sect;4996.23.3(a) and "
         "&sect;4999.46.4(a). California&rsquo;s only statutory rule about "
         "where a registrant may work points at the <b>employer</b>, not at "
         "the state line. Your employer can say no. The Legislature has "
         "not."]))
    o.append('<p class="pk-d">And the statute affirmatively authorizes the '
             "modality: <b>&sect;4980.43.3(i)</b> says an associate or "
             "trainee <i>may</i> provide services by telehealth within their "
             "scope of practice, with no cap, no location clause and no time "
             "limit. &sect;4996.23.2(j) and &sect;4999.46.3(j) say the same "
             "for the other two registrations.</p>")

    o.append('<h3 class="pk-h3">The Board has been asked directly, and has '
             "answered %d times.</h3>" % len(ANSWERS))
    rows = []
    for title, dated, quote, url in ANSWERS:
        rows.append([("<b>%s</b>" % title), (dated, "m"), quote])
    o.append(pk.table(
        ["Where", "Dated", "What it says"],
        rows,
        "Read them in order and one thing changes. The 2025 answers are "
        "framed around an associate who is <i>traveling</i>. The February "
        "2026 supervisor FAQ drops the word, drops any duration, and extends "
        "the answer to another <i>country</i>. What it keeps is the gate: "
        "<b>if the supervisor permits it</b>.", minw=680))
    o.append("</section>")

    # ------------------------------------------------------------ conditions
    o.append('<section class="pk-sec" id="conditions">')
    o.append('<p class="pk-k">What &ldquo;yes&rdquo; is conditional on</p>')
    o.append('<h2 class="pk-h">Four conditions, all of which are ordinary.</h2>')
    o.append('<p class="pk-d">These are the Board&rsquo;s own, listed in the '
             "MFT and ASW FAQ answers. None of them is special to being out "
             "of state; they are the conditions on any associate&rsquo;s "
             "hours, applied to this situation.</p>")
    o.append(pk.numbered([
        ("1", "Your supervisor assesses it and permits it",
         "Not a formality. <b>BPC &sect;4980.43.2(d)</b> requires the "
         "supervisor, within 60 days of supervision starting, to assess "
         "whether videoconference supervision is appropriate &mdash; "
         "considering your abilities, both parties&rsquo; preferences, and "
         "the privacy of both locations &mdash; to <b>document that "
         "assessment</b>, and not to use videoconference supervision if the "
         "assessment says it is inappropriate."),
        ("2", "Telehealth standards of practice are met",
         "The same standards that apply to any California telehealth "
         "session, under BPC &sect;2290.5 and 16 CCR &sect;1815.5. Being "
         "physically elsewhere changes nothing about informed consent, "
         "emergency planning, or knowing where your client is sitting."),
        ("3", "Supervision runs through your California supervisor, by video",
         "<b>Two-way, real-time videoconferencing counts as face-to-face "
         "contact</b> under &sect;4980.43.2(b)(2), and there is no cap "
         "&mdash; nothing must be in person. Two limits do bite: "
         "<b>telephone does not count at all</b>, and supervisor contact "
         "must occur <b>within the same week as the hours claimed</b>."),
        ("4", "Everything else about being an associate still holds",
         "W-2 employment or documented volunteer status, never an "
         "independent contract. Weekly logs. The supervision agreement. The "
         "employer&rsquo;s permitted place of business. <b>This is where the "
         "arrangement actually falls apart</b>, and the next section is "
         "about why."),
    ]))

    o.append(pk.callout(
        "One date worth knowing",
        ["Videoconference supervision was on a sunset clause that would have "
         "expired on 1 January 2026. <b>SB 775, chaptered 13 October 2025</b>, "
         "deleted the sunset and extended the provisions indefinitely. If you "
         "read something written before autumn 2025 that treats remote "
         "supervision as temporary, that is why &mdash; and it is no longer "
         "true."]))
    o.append("</section>")

    # ---------------------------------------------------------------- open
    o.append('<section class="pk-sec" id="open">')
    o.append('<p class="pk-k">The risk that is real</p>')
    o.append('<h2 class="pk-h">The question nobody in California can answer '
             "for you.</h2>")
    o.append('<p class="pk-d">Everything above is about California. None of '
             "it says anything about the state you are physically sitting "
             "in, and that is not an omission this page can fill.</p>")
    o.append(pk.table(
        ["The open question", "Where it stands"],
        [(["Does the state you are sitting in require its own credential?",
           "<b>The Board does not say, and has no authority to.</b> 16 CCR "
           "&sect;1815.5(e) covers only the reverse case &mdash; a California "
           "registrant serving a client in another jurisdiction. Whether "
           "Texas or New York or Oregon considers an unlicensed person "
           "delivering psychotherapy from inside its borders to be practicing "
           "there is a question for that state&rsquo;s board, and it is the "
           "one worth an email before you move."], "bad"),
         ["Is a permanent move treated differently from travel?",
          "<b>Not addressed.</b> Three of the five Board answers say "
          "&ldquo;traveling&rdquo;; the newest does not, and none sets a day "
          "limit, a residency test or a temporary-absence standard."],
         ["Does the out-of-state experience regulation apply to you?",
          "<b>Unreconciled.</b> 16 CCR &sect;1833.2 requires experience "
          "&ldquo;gained outside of California&rdquo; to have been supervised "
          "by someone licensed in that jurisdiction. Read flatly, someone "
          "sitting in Nevada is gaining experience outside California. The "
          "Board&rsquo;s published answers treat the arrangement as "
          "California experience &mdash; the client, employer, supervisor and "
          "registration are all Californian &mdash; but it has never printed "
          "a reconciliation of the two."]],
        "The first row is the one to act on. It is also the one nobody in a "
        "California support group can settle, which may be part of why the "
        "thread that prompted this page never resolved."))
    o.append("</section>")

    # ----------------------------------------------------------- what blocks
    o.append('<section class="pk-sec">')
    o.append('<p class="pk-k">Why it stays rare anyway</p>')
    o.append('<h2 class="pk-h">The obstacles are practical, and they belong '
             "to your employer.</h2>")
    o.append(pk.numbered([
        ("1", "You have to stay a W-2 employee",
         "&sect;4980.43.3(a) allows an associate to be an employee or a "
         "volunteer and nothing else. An employee living in another state "
         "generally means the employer registering for payroll there, "
         "withholding there, and carrying workers&rsquo; compensation there "
         "&mdash; a real administrative cost for a practice with two or three "
         "people in it. <b>&ldquo;Just go 1099&rdquo; is not available</b>, "
         'and <a href="%s">why not is its own page</a>.' % HIRING),
        ("2", "Your employer has an unreviewable veto",
         "&sect;4980.43.4(a) again: services only at the places the employer "
         "permits. A supervisor who does not want to think about any of the "
         "above simply says no, and there is nothing to appeal."),
        ("3", "Nobody wants to be the first",
         "Which is the actual content of the original post. An arrangement "
         "that is lawful, documented by the regulator, and that no employer "
         "has done before is still a conversation you have to have from a "
         "standing start &mdash; with the five citations in the table above, "
         "which is what this page is for."),
    ]))
    o.append('<p class="pk-fine">The first two are inferences from the '
             "statutory structure rather than positions the Board has stated, "
             "and are marked as such. The Board has published nothing about "
             "why the arrangement is uncommon, only that it is "
             "permitted.</p>")
    o.append("</section>")

    # ----------------------------------------------------------------- wrong
    o.append('<section class="pk-sec" id="wrong">')
    o.append('<p class="pk-k">Cited constantly, relevant never</p>')
    o.append('<h2 class="pk-h">Three things that do not apply to you.</h2>')
    o.append(pk.table(
        ["What people cite", "What it actually is"],
        [["The %d-day temporary practice allowance" % TEMP_DAYS,
          "<b>BPC &sect;4980.11</b> &mdash; not &sect;4980.03, which is the "
          "definitions section. It lets someone <i>licensed in another "
          "state</i> serve an existing client who is <b>located in "
          "California</b>, for %d consecutive days once a calendar year. It "
          "runs <b>into</b> California, not out of it. And the Board&rsquo;s "
          "own FAQ answers the associate question in one word: asked whether "
          "a pre-licensed associate in another state can get one, "
          "<b>&ldquo;No.&rdquo;</b>" % TEMP_DAYS],
         ["The Out-of-State Experience Verification form",
          "Form <b>37A-304</b> for MFTs, 37A-202 for LCSWs, 37A-668 for "
          "LPCCs. It is completed by <b>your out-of-state supervisor</b> and "
          "filed with a <b>Path B</b> application &mdash; the route for "
          "somebody who was never a California registrant. Its attestation "
          "certifies that the hours complied with <i>the other "
          "jurisdiction&rsquo;s</i> requirements. A California associate "
          "supervised by a California LMFT has nobody who can sign it."],
         ["An interstate compact",
          "<b>There is no compact available to you.</b> California is not a "
          "member of the Counseling Compact or the Social Work Licensure "
          "Compact; the bill that would have joined the latter, AB 427, died "
          "in January 2026 with the Board opposed. Both compacts exclude "
          "anyone whose practice requires supervision. PSYPACT is for "
          "psychologists, and the Board of Psychology&rsquo;s published "
          "action plan lists &ldquo;California remains outside of "
          "PSYPACT&rdquo; as a success measure. <b>No MFT compact exists "
          "anywhere.</b>"]],
        "All three come up in every thread on this subject, and all three are "
        "answers to somebody else&rsquo;s question. The provisions that "
        "govern your situation are the two in the sections above."))

    o.append('<p class="pk-fine">Nothing here is legal advice. If you are '
             "planning a move, the two things worth doing before it are "
             "getting your supervisor&rsquo;s written agreement and asking "
             "the licensing board of the state you are moving to whether it "
             "considers you to be practicing there. If it is a fully "
             'licensed move you are contemplating rather than an associate '
             'one, <a href="%s">that is a different page</a>; if you are '
             'still counting, <a href="%s">the hours calculator</a> works '
             "from your own numbers and sends nothing anywhere.</p>"
             % (REMOTE, HOURS))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The Board's published answers", [
            (t + " &mdash; " + d, u) for t, d, q, u in ANSWERS]),
        ("The regulations and statutes", [
            ("BBS Statutes and Regulations, %s edition &mdash; every section "
             "quoted on this page is reproduced here" % LAWBOOK_ED, LAWBOOK),
            ("BPC &sect;4980.43 &mdash; supervised experience, with no "
             "geographic condition in it",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.43.&lawCode=BPC"),
            ("BPC &sect;4980.43.2 &mdash; direct supervisor contact, "
             "videoconference as face-to-face, the 60-day assessment",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.43.2.&lawCode=BPC"),
            ("BPC &sect;4980.43.3 &mdash; employment status, and subdivision "
             "(i) on telehealth",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.43.3.&lawCode=BPC"),
            ("BPC &sect;4980.43.4 &mdash; location of services: the "
             "employer&rsquo;s permitted places",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.43.4.&lawCode=BPC"),
            ("BPC &sect;4980.11 &mdash; the temporary practice allowance, "
             "for out-of-state licensees serving clients in California",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=4980.11.&lawCode=BPC"),
            ("BPC &sect;2290.5 &mdash; the definition of telehealth, "
             "originating and distant sites",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection"
             ".xhtml?sectionNum=2290.5.&lawCode=BPC"),
        ]),
        ("The rest", [
            ("BBS temporary practice allowance FAQ &mdash; &ldquo;No&rdquo; "
             "for pre-licensed associates",
             "https://www.bbs.ca.gov/licensees/"
             "temporary_practice_allowance_faqs.pdf"),
            ("BBS &mdash; planning to supervise by videoconference: "
             "telephone does not count",
             "https://www.bbs.ca.gov/pdf/publications/sup_vid_conf.pdf"),
            ("MFT Out-of-State Experience Verification, form 37A-304 "
             "&mdash; read for who it is addressed to",
             "https://www.bbs.ca.gov/pdf/forms/mft/"
             "lmft_oos_expver_option1.pdf"),
            ("SB 775 (2025) &mdash; deleting the sunset on videoconference "
             "supervision",
             "https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml"
             "?bill_id=202520260SB775"),
            ("Counseling Compact &mdash; the member map, and the exclusion "
             "of anyone requiring supervision",
             "https://counselingcompact.org/faq/"),
            ("AB 427 (2025-26), the Social Work Licensure Compact bill, "
             "which died on 31 January 2026",
             "https://legiscan.com/CA/bill/AB427/2025"),
        ]),
    ], note="Where this page says the Board has not addressed something, the "
            "documents checked are the five FAQs above, the Board&rsquo;s "
            "newsletters from spring 2024 to spring 2026, the full FAQ index, "
            "and the 2025 and 2026 legislative summaries. Absence established "
            "by looking is worth printing; absence assumed is not.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "Can a California associate accrue hours from out of state? Yes",
    "The BBS has published the answer five times, most recently February "
    "2026: a California associate can serve California clients from out of "
    "state and count the hours, if the supervisor permits it. The conditions, "
    "and the one question nobody in California can answer.",
    "licensure", "guide",
    "Can I finish my supervised hours by telehealth from another state?",
    "The five published Board answers, the four conditions, and the risk that "
    "is real &mdash; which is not the one people worry about",
    "%d published Board answers" % len(ANSWERS),
    weight=5)


def main():
    print("out-of-state hours by telehealth")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources, %d Board answers"
          % (PAGE, format(len(html), ",d"), nsrc, len(ANSWERS)))

    bad = pk.check_page(p, [
        ("the client-location regulation", "1815.5"),
        ("the location-of-services statute", "4980.43.4"),
        ("the temporary-practice correction", "4980.11"),
        ("the compact answer", "no compact available"),
    ], [j[0] for j in JUMPS] + ["sources"])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every Board answer must appear with its date, because the page's claim
    # is not "the Board allows this" but "the Board has said so, here, on
    # these dates". A quote that loses its date loses the argument.
    for title, dated, quote, url in ANSWERS:
        if title not in art:
            print("GUARD: the answer %r is not on the page" % title)
            bad += 1
        if dated not in art:
            print("GUARD: %r has lost its date" % title)
            bad += 1
        if url not in art:
            print("GUARD: %r is quoted but not linked" % title)
            bad += 1

    # The two sections the page exists to keep apart.
    for what, needle in (("the client question", 'id="client"'),
                         ("the associate question", 'id="you"')):
        if needle not in art:
            print("GUARD: %s section is missing, and the page's whole "
                  "structure is the separation of the two" % what)
            bad += 1

    # The wrong citation this page was written partly to correct. If it ever
    # appears, an old draft has been reintroduced.
    # The page names the wrong section once, on purpose, to say it is wrong.
    # Any second appearance means a draft has cited it as though it were the
    # temporary-practice provision - which is the error this page corrects,
    # reintroduced into the page that corrects it.
    n_wrong = art.count("4980.03")
    if n_wrong != 1 or "not &sect;4980.03" not in art:
        print("GUARD: 4980.03 appears %d times and %s in the correcting "
              "sentence. It is the definitions section; the temporary "
              "practice allowance is 4980.11."
              % (n_wrong, "is" if "not &sect;4980.03" in art else "is not"))
        bad += 1

    if nsrc < 15:
        print("GUARD: %d sources for a page that is entirely citation" % nsrc)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - %d Board answers each quoted, dated and linked, "
          "%d sources" % (len(ANSWERS), nsrc))


if __name__ == "__main__":
    main()
