#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bringing a license from another state: Path A, Path B, and why CE cannot help.

THE QUESTION THIS ANSWERS

The single largest theme in the California associate support group, and the one
with no incumbent serving it at all. From that group:

    "I applied for APCC and was denied based on 'missing 4 credits that did not
     meet CA requirements'. I am curious if anyone has had this issue when
     applying from out of state. I came from a CACREP school."

    "if I have 2000 hours in another state can I transfer them when trying to
     get my California license?"

Nine distinct posts, the highest comment counts in the group, and members
solving deficiency notices by hand in comment threads one at a time.

THE STRUCTURE THIS PAGE IMPOSES, AND WHY IT IS NOT OBVIOUS

The Board publishes the answer three times - once each for LMFT, LCSW and LPCC
- in three separate documents that never reference each other. Read side by
side they are the same machine:

    Path A - licensure by credential. Four conditions, four California courses,
             the law and ethics exam, and the clinical exam is waived.
    Path B - licensure via education and experience. Everyone else. Your
             graduate transcript is reopened and measured against California's
             content requirements, and both exams apply.

Nobody publishes that comparison, and it is the thing that tells a person in
about ten seconds which of two very different years they are facing.

THE CORRECTION THIS PAGE EXISTS TO MAKE

The deficiency notices say "missing units" and everybody's first instinct is to
buy CE hours. That does not work, and the reason is a distinction the Board
draws but does not shout:

  * REMEDIATION coursework - the overall unit floor, missing core content
    areas, the advanced-coursework block, and the 3-semester-unit law and
    ethics course - must be GRADUATE LEVEL, from a regionally or nationally
    accredited or BPPE-approved school. Continuing education is not accepted.

  * ADDITIONAL coursework - the 12-hour California law and ethics course, child
    abuse, suicide risk, human sexuality and the rest - MAY come from an
    acceptable continuing education provider.

Same word, "coursework", on the same page of the same notice, two completely
different products at two completely different prices. That is the page.

A NOTE ON WHAT IS NOT CLAIMED

The Board's LMFT out-of-state requirements chart carries the filename stamp
01012016. Where the statute and the chart could be read differently the statute
is quoted and the chart is cited as a chart, not as law. And the fee figures
printed inside the Board's own out-of-state application PDFs are pre-reduction:
they predate 1 July 2026. This page does not restate them - it links to the fee
page, which has the current arithmetic, and says why.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "out-of-state-to-california-licensure.html"

# The donor supplies the masthead, footer, stylesheet links and the nav-panel
# script. Any recently built pagekit page will do; this one is chosen because
# it is in the same cluster and so carries the same nav state.
DONOR = "associate-hours-telehealth-out-of-state.html"

HOURS = "amft-3000-hours-california.html"
FEES = "bbs-fees-california-2026.html"
TELE = "associate-hours-telehealth-out-of-state.html"
EXAMS = "bbs-exam-pass-rates-california.html"
TIMES = "bbs-processing-times-california.html"
JOBS = "associate-mft-job-advisor.html"

CHART_STAMP = "01012016"

# The conversion in BPC 4980.74(c), and its siblings for the other two
# licenses. Verified against the statute text, not against a summary.
RATE_PER_MONTH = 100
RATE_CAP = 1200
TOTAL_HOURS = 3000
YEARS_LICENSED = 2
EXPERIENCE_WINDOW_YEARS = 6
DIRECT_MIN = 1750
NONCLINICAL_MAX = 1250

JUMPS = [("which", "Which path"),
         ("checker", "Check yours"),
         ("patha", "Path A"),
         ("pathb", "Path B"),
         ("hours", "Your hours"),
         ("supervision", "Supervision"),
         ("cost", "What it costs"),
         ("sources", "Sources")]


# --------------------------------------------------------------- the coursework
#
# Every row below is transcribed from the Board's own requirement documents,
# named in the sources. `ce` records whether an acceptable continuing education
# provider can satisfy it, because that single column is the difference between
# a few hundred dollars and a semester of graduate tuition.
#
# The four marked path="A" are the ONLY coursework Path A requires. They are
# identical across LMFT, LCSW and LPCC, which is worth seeing.
CALIFORNIA_COURSES = [
    ("California law and professional ethics", "12 hours", True, "A",
     "Scope of practice, confidentiality and its limits, child abuse "
     "reporting, advertising, disciplinary action and the licensing law "
     "itself &mdash; all California-specific."),
    ("Child abuse assessment and reporting", "7 hours", True, "A",
     "CANRA, the indicators, the assessment methods and the reporting "
     "procedure. The out-of-state version of this course does not count; it "
     "has to be the California one."),
    ("California cultures and the social and psychological "
     "implications of socioeconomic position", "15 hours or 1 semester unit",
     True, "A",
     "Named in the statute in those words. There is no national equivalent, "
     "so essentially nobody arrives holding it."),
    ("Suicide risk assessment and intervention", "6 hours", True, "A",
     "Required of applicants since 1 January 2021."),
    ("Human sexuality", "10 hours", True, "B",
     "Physiological, psychological and social-cultural, including sexual "
     "dysfunction and gender identity."),
    ("Spousal or partner abuse assessment, detection and intervention",
     "15 hours", True, "B",
     "Including same-gender dynamics."),
    ("Aging and long-term care, including elder and dependent adult abuse",
     "10 hours", True, "B",
     "Biological, social and cognitive aspects of aging, plus the assessment "
     "and reporting duty."),
    ("Substance use disorders and co-occurring conditions", "15 hours", True,
     "B",
     "The LMFT chart splits this into two 15-hour blocks; the LPCC guide "
     "carries it as addictions counseling inside the core content areas."),
    ("Mental health recovery-oriented care", "45 hours or 3 semester units",
     True, "B",
     "The largest of the additional courses by a wide margin, and the one "
     "most often missed when people budget for this."),
]

# Path B also reopens the degree itself. These are the parts a continuing
# education certificate cannot touch, which is the whole point of the page.
GRADUATE_ONLY = [
    ("The overall unit floor",
     "48 semester units, or 60 if your program began after 1 August 2012 or "
     "you graduated after 31 December 2018",
     "Up to 12 semester units of remediation are accepted toward the floor."),
    ("Any missing core content area",
     "3 semester units each, at graduate level",
     "The LPCC scheme names 13 of them. The ones out-of-state applicants "
     "most often lack are psychopharmacology, addictions counseling, crisis "
     "or trauma counseling, and advanced theories and techniques."),
    ("The advanced-coursework block",
     "15 semester units on specific treatment issues or populations",
     "Core content area courses cannot be double-counted into this."),
    ("The 3-semester-unit law and ethics course",
     "3 semester units, if your degree's version was shorter",
     "Distinct from the 12-hour California law and ethics course, which CE "
     "does satisfy. Two different requirements, similar names."),
]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Out-of-state licensure &middot; Paths A and B &middot; checked %s"
        % pk.CHECKED,
        "Your license travels. Your transcript does not.",
        "California has two routes in, and they are not close. One asks for "
        "four courses. The other reopens your graduate degree &mdash; and "
        "<b>continuing education cannot close that gap</b>, whatever the "
        "deficiency letter looks like.",
        [("%d years" % YEARS_LICENSED, "licensed elsewhere, for the fast route"),
         ("4", "California courses under Path A"),
         ("%d/mo" % RATE_PER_MONTH, "licensed time converts, capped at %s"
          % format(RATE_CAP, ",d")),
         ("0", "CE courses accepted for a transcript gap")],
        JUMPS))

    # ------------------------------------------------------------ the question
    o.append('<section class="pk-sec">')
    o.append(pk.quote(
        "From the associate group, and thirteen comments of guesses",
        ["I applied for APCC and was denied based on <b>&ldquo;missing 4 "
         "credits that did not meet CA requirements&rdquo;</b>. I am curious "
         "if anyone has had this issue when applying from out of state. I came "
         "from a CACREP school.",
         "And, separately: if I have 2,000 hours in another state, can I "
         "transfer them when trying to get my California license?"]))

    o.append('<p class="pk-k">The short version</p>')
    o.append('<h2 class="pk-h">Two routes, and the letter you got does not '
             "say which one you are on.</h2>")
    o.append('<p class="pk-d">The Board publishes this answer three times '
             "&mdash; once for marriage and family therapists, once for "
             "clinical social workers, once for professional clinical "
             "counselors &mdash; in three documents that never reference each "
             "other. Read side by side they describe the same machine, and "
             "seeing the shape of it is most of the work.</p>")

    o.append(pk.numbered([
        ("1", "Path A is licensure by credential.",
         "Four conditions, all of which are about the license you already "
         "hold rather than the degree behind it. Meet them and California "
         "asks for four courses, one exam, and nothing else. Your clinical "
         "exam is waived."),
        ("2", "Path B is licensure via education and experience.",
         "Everyone who does not qualify for A. Your graduate transcript is "
         "reopened and measured against California's content requirements, "
         "you owe up to nine California-specific courses on top, and you sit "
         "both exams."),
        ("3", "The difference between them is years and thousands of dollars.",
         "Which is why it is worth knowing which one you are on before you "
         "pay an application fee to find out."),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------- which path
    o.append('<section class="pk-sec" id="which">')
    o.append('<p class="pk-k">The four conditions</p>')
    o.append('<h2 class="pk-h">Path A is not about your degree. It is about '
             "your license.</h2>")
    o.append('<p class="pk-d">All four have to be true at once. Any one of '
             "them failing puts you on Path B, and there is no partial "
             "credit.</p>")

    o.append(pk.table(
        ["The condition", "What it actually means"],
        [["You hold the license in another <b>U.S.</b> jurisdiction",
          "Another country does not qualify you for Path A, however senior "
          "the license. Out-of-country applicants are on Path B and also need "
          "a NACES-member credential evaluation."],
         ["At the <b>highest level for independent practice</b> there",
          "An associate, provisional, conditional or supervised-practice "
          "credential is not it. This is the condition that surprises people "
          "who have been practicing for years under a two-tier scheme."],
         ["<b>Current, active and unrestricted</b>",
          "Not lapsed, not inactive, not on probation. Past discipline does "
          "not automatically disqualify you but must be disclosed for the "
          "Board to review."],
         ["For at least <b>two years</b> before you apply",
          "Two continuous years immediately before the application. Time "
          "before a lapse does not bridge the gap."]],
        caption="Identical for LMFT, LCSW and LPCC. The LCSW route adds that "
                "the master&rsquo;s must be from a CSWE-accredited school; "
                "the other two accept a regionally or nationally accredited "
                "or BPPE-approved institution.",
        minw=620))

    o.append(pk.callout(
        "The sentence that decides it",
        ["California&rsquo;s statute for marriage and family therapists puts "
         "the boundary in one line. Section 4980.74 &mdash; the Path B "
         "section &mdash; opens by saying it applies to people with "
         "out-of-state education or experience <b>&ldquo;who do not qualify "
         "for a license under Section 4980.72&rdquo;</b>, which is the Path A "
         "section.",
         "So Path B is not a second option you might prefer. It is the "
         "residual. You are on it by default and leave it only by satisfying "
         "all four conditions above."]))
    o.append("</section>")

    # --------------------------------------------------------------- the tool
    o.append('<section class="pk-sec" id="checker">')
    o.append('<p class="pk-k">The checker</p>')
    o.append('<h2 class="pk-h">Which path, and what you would owe.</h2>')
    o.append('<p class="pk-d">Answer the four conditions and, if you have '
             "them, your hours. Everything is computed in this browser: no "
             "account, no storage, nothing sent anywhere, and nothing kept "
             "when you close the tab.</p>")
    o.append(CALC_HTML)
    o.append("</section>")

    # -------------------------------------------------------------- path A
    o.append('<section class="pk-sec" id="patha">')
    o.append('<p class="pk-k">Path A</p>')
    o.append('<h2 class="pk-h">Four courses, one exam, and the clinical exam '
             "is waived.</h2>")
    o.append('<p class="pk-d">This is the whole of it. The four courses below '
             "are the only coursework Path A asks for, they are the same four "
             "for all three licenses, and an acceptable continuing education "
             "provider can supply every one of them.</p>")

    rows = []
    for name, amount, ce, path, note in CALIFORNIA_COURSES:
        if path != "A":
            continue
        rows.append([name, (amount, "m"), note])
    o.append(pk.table(["Course", "Length", "What it covers"], rows, minw=640))

    o.append('<p class="pk-p">Then the California Law and Ethics Exam, and '
             "that is the end of the examination requirement. For marriage "
             "and family therapists the statute says so directly: an "
             "applicant qualifying under section 4980.72 passes the "
             "California law and ethics examination <b>with the clinical "
             "examination waived</b>. The clinical social work and "
             "professional clinical counselor guides run the same way "
             "&mdash; a Path A applicant is never sent to the national "
             "clinical examination.</p>")

    o.append(pk.checklist(
        "What Path A does not ask you for",
        ["A unit count on your degree.",
         "Any of the thirteen core content areas.",
         "The advanced-coursework block.",
         "Practicum hours, or evidence of them.",
         "Verification of 3,000 supervised hours &mdash; the license you "
         "already hold stands in for all of it.",
         "The clinical examination."]))
    o.append("</section>")

    # -------------------------------------------------------------- path B
    o.append('<section class="pk-sec" id="pathb">')
    o.append('<p class="pk-k">Path B</p>')
    o.append('<h2 class="pk-h">The part where continuing education stops '
             "working.</h2>")
    o.append('<p class="pk-d">Path B has two halves that look alike in the '
             "letter and behave nothing alike in practice. The Board calls "
             "one <b>remediation</b> and the other <b>additional "
             "coursework</b>, and the difference is who is allowed to teach "
             "it.</p>")

    o.append(pk.callout(
        "The distinction the deficiency notice buries",
        ["<b>Remediation</b> &mdash; the overall unit floor, any missing core "
         "content area, the advanced-coursework block, and the "
         "three-semester-unit law and ethics course &mdash; must be "
         "<b>graduate level, from a regionally or nationally accredited or "
         "BPPE-approved school</b>. Continuing education courses are not "
         "accepted for any of it.",
         "<b>Additional coursework</b> &mdash; the 12-hour California law and "
         "ethics course and the other California topics &mdash; may come from "
         "an acceptable continuing education provider.",
         "Same word on the same page of the same notice. One of them is a "
         "few hundred dollars. The other is a semester of graduate tuition, "
         "per course, and it is the one the letter was almost certainly "
         "talking about."],
        big="&ldquo;Missing 4 credits&rdquo; is a graduate-credit problem."))

    o.append('<h3 class="pk-h3">What only a graduate school can fix</h3>')
    o.append(pk.table(
        ["Requirement", "What it takes", "The detail people miss"],
        [[n, (a, "m"), d] for n, a, d in GRADUATE_ONLY],
        caption="Remediation coursework may count toward more than one of "
                "these at once, but a core content area course cannot be "
                "counted into the advanced-coursework block.",
        minw=660))

    o.append('<h3 class="pk-h3">What a continuing education provider can fix</h3>')
    o.append('<p class="pk-p">Nine courses, and Path A applicants owe only '
             "the first four. Everything here is available from acceptable "
             "continuing education providers, which is why this half is the "
             "cheap half.</p>")
    rows = []
    for name, amount, ce, path, note in CALIFORNIA_COURSES:
        rows.append([name, (amount, "m"),
                     "Both paths" if path == "A" else "Path B only"])
    o.append(pk.table(["Course", "Length", "Who owes it"], rows, minw=600))
    o.append('<p class="pk-cap">Transcribed from the Board&rsquo;s LMFT '
             "out-of-state requirements chart, whose filename carries the "
             "stamp <b>%s</b>, and from the LPCC and LCSW out-of-state "
             "guides. Where the chart and the statute could be read "
             "differently, the statute above is what is quoted. Check your "
             "own license&rsquo;s current guide before spending money on "
             "any of it.</p>" % CHART_STAMP)
    o.append("</section>")

    # --------------------------------------------------------------- hours
    o.append('<section class="pk-sec" id="hours">')
    o.append('<p class="pk-k">The 3,000 hours</p>')
    o.append('<h2 class="pk-h">Time spent licensed converts into hours. '
             "Time spent unlicensed does not.</h2>")
    o.append('<p class="pk-d">This is the second question the group asks, and '
             "the answer is better than most people expect &mdash; with one "
             "condition that does most of the work.</p>")

    o.append(pk.numbered([
        ("1", "If your state required 3,000 hours or more, you are done.",
         "An applicant currently licensed at the highest independent level in "
         "a U.S. jurisdiction whose own scheme required at least 3,000 "
         "supervised hours does not submit experience verification at all."),
        ("2", "Otherwise, licensed time converts at %d hours a month."
         % RATE_PER_MONTH,
         "The statute directs the Board to accept, as qualifying supervised "
         "experience, the time you held an active license in good standing in "
         "another state or country at the highest level for independent "
         "practice &mdash; at %d hours per month, <b>up to a maximum of "
         "%s hours</b>. No verification of the underlying work is required "
         "for the converted portion." % (RATE_PER_MONTH,
                                         format(RATE_CAP, ",d"))),
        ("3", "The cap is the catch.",
         "%s hours is %d months of the conversion and %d%% of the %s you "
         "need. The rest has to be real, documented, substantially equivalent "
         "supervised experience &mdash; and if you were never licensed at the "
         "highest level, the conversion is worth nothing to you."
         % (format(RATE_CAP, ",d"), RATE_CAP // RATE_PER_MONTH,
            round(100.0 * RATE_CAP / TOTAL_HOURS), format(TOTAL_HOURS, ",d"))),
    ]))

    o.append('<h3 class="pk-h3">What &ldquo;substantially equivalent&rdquo; '
             "means for the hours you do have to document</h3>")
    o.append(pk.table(
        ["Test", "The requirement"],
        [["When it was gained",
          "Within the %d years before the Board receives your California "
          "application." % EXPERIENCE_WINDOW_YEARS],
         ["Direct counseling",
          "At least %s hours with individuals, groups, couples or families."
          % format(DIRECT_MIN, ",d")],
         ["Non-clinical",
          "No more than %s hours of supervision, testing, report writing, "
          "advocacy and training." % format(NONCLINICAL_MAX, ",d")],
         ["Who supervised it",
          "A licensed mental health professional at the highest level for "
          "independent practice, licensed at least two years before "
          "supervising you, active and in good standing throughout."]],
        minw=560))
    o.append('<p class="pk-p">If you are still gaining hours rather than '
             "counting old ones, the separate question of whether they can be "
             "gained by telehealth from outside California is answered on "
             '<a href="%s">its own page</a> &mdash; and the projection of '
             'when the 3,000 actually close is on <a href="%s">the hours '
             "page</a>.</p>" % (TELE, HOURS))
    o.append("</section>")

    # ---------------------------------------------------------- supervision
    o.append('<section class="pk-sec" id="supervision">')
    o.append('<p class="pk-k">16 CCR &sect;1833.2</p>')
    o.append('<h2 class="pk-h">Your out-of-state supervisor has to pass a '
             "test too.</h2>")
    o.append('<p class="pk-d">There is a regulation devoted entirely to this, '
             "and it is where otherwise-good hours are lost. Three "
             "conditions, and the third one is the escape hatch nobody knows "
             "about.</p>")

    o.append(pk.table(
        ["&sect;1833.2", "What it requires of the person who supervised you"],
        [["(a)(1)",
          "At the time of supervision they were licensed or certified in that "
          "jurisdiction, and the license was current and active and "
          "<b>not under suspension or probation</b>."],
         ["(a)(2)",
          "They had been licensed or certified there for at least <b>two of "
          "the five years</b> immediately before supervising you &mdash; as a "
          "psychologist, clinical social worker, board-certified "
          "psychiatrist, professional clinical counselor, marriage and "
          "family therapist or similarly titled practitioner, or an "
          "equivalent license permitting independent clinical practice."],
         ["(a)(3)",
          "In a jurisdiction that <b>does not license</b> marriage and family "
          "therapists at all, supervision may instead come from someone who "
          "held clinical membership in the American Association for Marriage "
          "and Family Therapy for at least two years and kept it throughout "
          "the period of supervision."]],
        caption="Subdivision (a)(3) is the provision that rescues hours "
                "gained in states with no MFT license. It is rarely cited and "
                "it is the reason a flat &ldquo;those hours won&rsquo;t "
                "count&rdquo; is often wrong.",
        minw=620))
    o.append("</section>")

    # ---------------------------------------------------------------- cost
    o.append('<section class="pk-sec" id="cost">')
    o.append('<p class="pk-k">What it costs</p>')
    o.append('<h2 class="pk-h">The Board&rsquo;s own out-of-state forms print '
             "the old fees.</h2>")
    o.append('<p class="pk-d">Board fees were cut by roughly half on 1 July '
             "2026 and revert on 30 June 2030. The out-of-state application "
             "PDFs still show the pre-reduction figures, so a number read off "
             "one of them is not what you will be charged.</p>")
    o.append('<p class="pk-p">Rather than reprint figures from a document '
             "that has not caught up, the current arithmetic &mdash; "
             "application, examination and initial license, at the rates in "
             'force now &mdash; is kept on <a href="%s">the fee page</a>, '
             "which also carries the two things the headline reduction leaves "
             "out. One of them applies to you specifically: the <b>$49 "
             "hard-card fingerprint fee</b> for applicants outside "
             "California was not reduced.</p>" % FEES)
    o.append(pk.checklist(
        "Three things to settle before you send anything",
        ["Which path you are on. Paying a Path B application fee to discover "
         "you qualified for Path A is a refundable mistake in nobody&rsquo;s "
         "policy &mdash; the application fee is earned and nonrefundable.",
         "Whether your deficiency is remediation or additional coursework. "
         "The first cannot be bought from a continuing education provider at "
         "any price.",
         "Whether your supervisor met &sect;1833.2 at the time. That is a "
         "fact about a past date and it does not improve with waiting."]))
    o.append('<p class="pk-p">Once you are through, the two waits that follow '
             'are the exams and the Board&rsquo;s own processing &mdash; '
             '<a href="%s">real pass rates</a> and <a href="%s">real '
             "processing times</a> are both transcribed from board "
             "packets.</p>" % (EXAMS, TIMES))
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The statute", [
            ("BPC &sect;4980.72 &mdash; out-of-state licensure by credential, "
             "marriage and family therapists",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?sectionNum=4980.72&lawCode=BPC"),
            ("BPC &sect;4980.74 &mdash; out-of-state education and "
             "experience, including the %d-hours-per-month conversion at "
             "subdivision (c)" % RATE_PER_MONTH,
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?sectionNum=4980.74&lawCode=BPC"),
            ("BPC &sect;4980.78 &mdash; substantial equivalence of "
             "out-of-state education",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?sectionNum=4980.78&lawCode=BPC"),
        ]),
        ("The regulation", [
            ("16 CCR &sect;1833.2 &mdash; supervision of experience gained "
             "outside of California",
             "https://www.law.cornell.edu/regulations/california/"
             "16-CCR-1833.2"),
        ]),
        ("The Board&rsquo;s own documents", [
            ("Requirements for out-of-state and out-of-country applicants for "
             "LMFT licensure &mdash; the Path A and Path B chart, filename "
             "stamped %s" % CHART_STAMP,
             "https://www.bbs.ca.gov/pdf/forms/mft/"
             "lmft_oos_req_chart_01012016.pdf"),
            ("LMFT out-of-state application flowchart",
             "https://www.bbs.ca.gov/pdf/forms/mft/lmft_oos_app_flowchart.pdf"),
            ("Application for LMFT licensure, Path B, out-of-state &mdash; "
             "the eligibility wording quoted above, and pre-reduction fees",
             "https://bbs.ca.gov/pdf/forms/mft/mftapp_oos_path_b.pdf"),
            ("Guide to requirements for out-of-state and out-of-country "
             "applicants for LPCC licensure &mdash; the fullest of the three, "
             "and the source for the remediation-versus-additional "
             "distinction",
             "https://www.bbs.ca.gov/pdf/forms/lpc/lpcc_oos_req_guide.pdf"),
            ("LPCC degree requirements &mdash; the thirteen core content "
             "areas",
             "https://www.bbs.ca.gov/pdf/forms/lpc/lpc_degree.pdf"),
            ("Statutes and regulations guide for clinical social workers "
             "&mdash; the LCSW Path A and Path B conditions",
             "https://www.bbs.ca.gov/pdf/lcsw_guide.pdf"),
            ("Licensed Marriage and Family Therapist &mdash; the Board&rsquo;s "
             "applicant page, where the current forms are listed",
             "https://www.bbs.ca.gov/applicants/lmft.html"),
        ]),
    ], note="Where this page describes a requirement, the Board document "
            "carrying it is listed so you can read the wording yourself. The "
            "LMFT requirements chart is cited as a chart: its filename stamp "
            "is %s, and it is not the law. Nothing here is legal advice, and "
            "an evaluation of your own transcript is a decision only the "
            "Board makes." % CHART_STAMP)
    o.append(src)

    o.append("</article>")
    return "".join(o), n


# ------------------------------------------------------------- the checker
#
# Nothing typed here leaves the page: no URL state, no storage, no analytics
# call, no network. A person checking whether their license transfers is
# entering the name of a jurisdiction and a count of months, and the site's
# printed promise is that nothing typed is sent anywhere.
CALC_HTML = """<div class="pk-calc" id="oos-calc">
<div class="pk-cg">
<div class="pk-cc">
<h3>The four conditions</h3>
<label class="pk-fl" for="oos-lic">Which license are you seeking?</label>
<select id="oos-lic">
<option value="LMFT">LMFT &mdash; marriage and family therapist</option>
<option value="LCSW">LCSW &mdash; clinical social worker</option>
<option value="LPCC">LPCC &mdash; professional clinical counselor</option>
</select>
<label class="pk-fl" for="oos-us">Do you hold that license in another U.S. state now?</label>
<select id="oos-us">
<option value="">Choose</option><option value="y">Yes</option><option value="n">No, or another country</option>
</select>
<label class="pk-fl" for="oos-top">Is it the highest level for independent practice there?</label>
<select id="oos-top">
<option value="">Choose</option><option value="y">Yes</option><option value="n">No, or not sure</option>
</select>
</div>
<div class="pk-cc">
<h3>And your hours</h3>
<label class="pk-fl" for="oos-yrs">Years it has been current, active and unrestricted</label>
<input type="number" id="oos-yrs" min="0" max="50" step="0.5" placeholder="0">
<label class="pk-fl" for="oos-deg">Degree from an accredited or approved school?</label>
<select id="oos-deg">
<option value="">Choose</option><option value="y">Yes</option><option value="n">No, or not sure</option>
</select>
<label class="pk-fl" for="oos-hrs">Supervised hours you can document</label>
<input type="number" id="oos-hrs" min="0" max="6000" step="50" placeholder="0">
<label class="pk-fl" for="oos-mo">Months licensed at that highest level</label>
<input type="number" id="oos-mo" min="0" max="600" step="1" placeholder="0">
</div>
</div>
<div class="pk-out">
<div class="r hd"><span>Line</span><span>Where you stand</span></div>
<div class="r"><span class="lbl">Your route</span><span class="va" id="oos-o-path">&mdash;</span></div>
<div class="r"><span class="lbl">California courses you would owe</span><span class="va" id="oos-o-courses">&mdash;</span></div>
<div class="r"><span class="lbl">Graduate-level remediation in play</span><span class="va" id="oos-o-rem">&mdash;</span></div>
<div class="r"><span class="lbl">Hours credited for licensed time &mdash; capped at 1,200</span><span class="va" id="oos-o-conv">&mdash;</span></div>
<div class="r"><span class="lbl">Examinations left</span><span class="va" id="oos-o-exam">&mdash;</span></div>
<div class="r tot"><span class="lbl"><b>Hours still to document</b></span><span class="va" id="oos-o-gap">&mdash;</span></div>
</div>
<p class="pk-note" id="oos-warn">Answer the four conditions on the left. This
runs entirely in your browser, nothing is stored, and nothing is sent anywhere.
It reads the Board&rsquo;s published requirements &mdash; it is not the
Board&rsquo;s evaluation of your file, which only the Board can make.</p>
</div>"""

CALC_JS = """<script>
(function(){
  var EM = '\\u2014';
  function el(id){ return document.getElementById(id); }
  function val(id){ var e = el(id); return e ? e.value : ''; }
  function num(id){
    var e = el(id); if(!e) return 0;
    var v = parseFloat(e.value);
    return (isFinite(v) && v > 0) ? v : 0;
  }
  function set(id, txt){ var e = el(id); if(e) e.textContent = txt; }
  function run(){
    var lic = val('oos-lic') || 'LMFT';
    var us = val('oos-us'), top = val('oos-top'), deg = val('oos-deg');
    var yrs = num('oos-yrs'), hrs = num('oos-hrs'), mo = num('oos-mo');
    var warn = el('oos-warn');

    /* Every condition has to be answered before a verdict means anything.
       An unanswered dropdown is not a "no" and must not be treated as one. */
    if(!us || !top || !deg || !yrs){
      ['oos-o-path','oos-o-courses','oos-o-rem','oos-o-conv','oos-o-exam',
       'oos-o-gap'].forEach(function(id){ set(id, EM); });
      if(warn) warn.innerHTML = 'Answer the four conditions on the left. ' +
        'This runs entirely in your browser, nothing is stored, and nothing ' +
        'is sent anywhere.';
      return;
    }

    var pathA = (us === 'y' && top === 'y' && deg === 'y' && yrs >= 2);
    var conv = Math.min(Math.floor(mo) * 100, 1200);
    /* Only licensed time at the highest independent level converts. Someone
       who answered "no" to that has no conversion, whatever the months say. */
    if(top !== 'y'){ conv = 0; }
    var gap = Math.max(0, 3000 - (hrs + conv));

    set('oos-o-path', pathA ? 'Path A' : 'Path B');
    set('oos-o-courses', pathA ? '4' : '9');
    set('oos-o-rem', pathA ? 'None' : 'Likely');
    set('oos-o-conv', conv ? conv.toLocaleString('en-US') + ' hrs' : EM);
    set('oos-o-exam', pathA ? 'Law and ethics only' : 'Both');
    set('oos-o-gap', pathA ? 'Not required' :
        (gap ? gap.toLocaleString('en-US') + ' hrs' : 'None'));

    var why = [];
    if(!pathA){
      if(us !== 'y'){ why.push('the license is not held in another U.S. state'); }
      if(top !== 'y'){ why.push('it is not at the highest level for independent practice'); }
      if(deg !== 'y'){ why.push('the degree is not from an accredited or approved school'); }
      if(yrs < 2){ why.push('it has been current and unrestricted for under two years'); }
    }

    if(warn){
      if(pathA){
        warn.innerHTML = '<b>All four conditions are met, so Path A is open ' +
          'to you.</b> Four California courses, the law and ethics exam, and ' +
          'the clinical exam is waived. Your degree is not reopened and your ' +
          'hours are not verified &mdash; the license you hold stands in for ' +
          'both. Nothing here is stored or sent anywhere.';
      } else {
        warn.innerHTML = '<b>Path B, because ' + why.join(', and ') + '.</b> ' +
          'That means nine California courses rather than four, both ' +
          'examinations, and a transcript review against California\\u2019s ' +
          'content requirements. Any shortfall there is <b>graduate-level ' +
          'remediation</b> &mdash; continuing education cannot satisfy it. ' +
          'Nothing here is stored or sent anywhere.';
      }
    }
  }
  ['oos-lic','oos-us','oos-top','oos-deg','oos-yrs','oos-hrs','oos-mo']
    .forEach(function(id){
      var e = el(id);
      if(e){ e.addEventListener('input', run); e.addEventListener('change', run); }
    });
  run();
})();
</script>"""


META = pk.meta_block(
    PAGE,
    "Out-of-state to California licensure: Path A, Path B, and your hours",
    "You are licensed elsewhere and moving to California. Path A asks for "
    "four courses and waives the clinical exam. Path B reopens your degree, "
    "and continuing education cannot close a transcript gap.",
    "licensure", "guide",
    "Can I bring my license and my supervised hours from another state?",
    "Which of the Board&rsquo;s two routes you are on, the coursework each "
    "one costs, and how much of your licensed time converts into hours",
    "%d hrs/month, capped at %s" % (RATE_PER_MONTH, format(RATE_CAP, ",d")),
    weight=5)


def main():
    print("out-of-state to California licensure")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=CALC_JS)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d sources"
          % (PAGE, format(len(html), ",d"), nsrc))

    bad = pk.check_page(p, [
        ("the residual-section rule", "who do not qualify for a license"),
        ("the CE-cannot-fix-it correction", "Continuing education courses are "
                                            "not accepted"),
        ("the conversion cap", "up to a maximum of"),
        ("the 1833.2 escape hatch", "American Association for Marriage"),
        ("the checker", 'id="oos-calc"'),
        ("the checker script", "oos-o-path"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every California course has to appear in the coursework table. A course
    # silently dropped would leave the checker saying "9" while eight are
    # listed, which is the kind of quiet disagreement this project has shipped
    # before.
    for name, amount, ce, path, note in CALIFORNIA_COURSES:
        if name.split("&mdash;")[0][:34] not in art:
            print("GUARD: the course %r is not on the page" % name[:44])
            bad += 1
    if len(CALIFORNIA_COURSES) != 9:
        print("GUARD: the checker prints 9 courses for Path B and the table "
              "holds %d" % len(CALIFORNIA_COURSES))
        bad += 1
    n_a = len([c for c in CALIFORNIA_COURSES if c[3] == "A"])
    if n_a != 4:
        print("GUARD: the page says four courses under Path A and the table "
              "marks %d" % n_a)
        bad += 1

    # The whole page turns on remediation and additional coursework being
    # different things. If either word disappears the correction is gone.
    for word in ("Remediation", "Additional coursework"):
        if word not in art:
            print("GUARD: %r has gone from the Path B section" % word)
            bad += 1

    # The fee warning must not be replaced by an actual fee figure read off a
    # pre-reduction PDF. If a dollar amount other than the fingerprint fee
    # appears, something has restated a stale number.
    import re as _re
    amounts = set(_re.findall(r"\$\d[\d,]*", art))
    if amounts - {"$49"}:
        print("GUARD: unexpected dollar figures on the page: %s - the "
              "out-of-state PDFs print pre-reduction fees and this page "
              "links to the fee page instead" % ", ".join(sorted(amounts)))
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
