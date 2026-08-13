#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finding a clinical supervisor in California, and what the law requires.

WHY THIS PAGE EXISTS

It is the first question a newly registered associate asks and the one this
site has never answered. The reason it has never been answered anywhere is
structural: **the Board of Behavioral Sciences does not certify supervisors and
publishes no roster of them.** There is no official list to point at. The
license lookup has no supervisor flag. So the question gets answered by a
scatter of chapter pages, one association directory, two commercial products
and a set of dead domains that search engines still rank.

`_dev/supervisor_lists.py` fetched every one of them. Nine of the twenty-three
CAMFT chapters publish a list; fourteen do not, two of the chapters that are
supposed to carry one no longer exist as organizations, and the coverage that
does exist is not distributed by population - San Diego, Sacramento, San
Francisco, Santa Clara Valley, the San Fernando Valley and Ventura have
nothing, while Marin has 116 names.

THE THING THIS PAGE EXISTS TO CORRECT

"Find your own supervisor" is a false picture for anybody in private practice.
BPC 4980.43.4(b) requires the supervisor to be employed by, contracted by, or
an owner of **the associate's employer**. A supervisor the associate retains
privately, with no relationship to the practice, does not satisfy it, and the
hours are not creditable. There is a lawful route - the employer contracts the
supervisor and a written oversight agreement is signed before supervision
starts - and it requires the employer to act. Somebody who spends three months
paying a supervisor they found themselves, at a private practice that never
contracted them, has bought nothing.

WHAT IT MUST NOT DO

Reproduce anybody's directory. Every list here is somebody else's membership
roster; this page reports how big each one is, what fields it carries and
whether it is usable, and links to it. A guard below fails the build if a
person's name appears in a list block.

It must also not state a supervision rate as though a market rate were
published. It is not. The only public California figure is the Board's own
2024 Pathway to Licensure survey, which asked what people paid per month and
published brackets - so that is what the page prints, with the caveats the
Board's own methodology requires.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import supervisor_lists_data as sd

SITE = pk.SITE
PAGE = "finding-a-clinical-supervisor-california.html"
DONOR = "amft-3000-hours-california.html"

HOURS = "amft-3000-hours-california.html"
ADVISOR = "associate-mft-job-advisor.html"
UNPAID = "associate-unpaid-hours-california.html"
HIRED = "getting-hired-as-a-california-associate.html"
HIRING = "hiring-first-associate-california-therapist.html"
BECOME = "become-an-mft-california.html"
TRACKERS = "associate-hours-trackers-compared.html"
DEDUCT = "therapist-tax-deductions-california.html"
FORGED = "discipline-case-forged-supervisor-signature.html"
SIGNED = "discipline-case-signed-her-supervisors-name.html"
SEVEN = "discipline-case-seven-years-under-supervision.html"
PRACTICUM = "practicum-california-mft-trainee.html"
CASES = "therapist-discipline-cases-california.html"

LEG = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
       "?sectionNum=%s.&lawCode=%s")
CCR = "https://www.law.cornell.edu/regulations/california/16-CCR-%s"
SUNSET = "https://www.bbs.ca.gov/pdf/publications/bbs_2025_sunset_report.pdf"
AGREEMENT = "https://www.bbs.ca.gov/pdf/forms/supervision_agreement.pdf"
SELFASSESS = "https://www.bbs.ca.gov/pdf/forms/supervisor_self_assessment.pdf"
SUPFAQ = "https://www.bbs.ca.gov/pdf/publications/faqs_for_supervisors.pdf"
SUPQUAL = "https://www.bbs.ca.gov/pdf/supervisor_qualifications.pdf"
BBSSUP = "https://www.bbs.ca.gov/licensees/supervisor.html"
DLSE = "https://www.dir.ca.gov/dlse/opinions/2000-11-03.pdf"


def bpc(sec):
    return LEG % (sec, "BPC")


JUMPS = [("lists", "Where the lists are"),
         ("trap", "The private-practice trap"),
         ("qualify", "Whether they may supervise you"),
         ("week", "What the week has to look like"),
         ("cost", "What it costs"),
         ("paper", "Three deadlines"),
         ("ask", "What to ask"),
         ("sources", "Sources")]

CH = [r for r in sd.LISTS if r["kind"] == "chapter" and r["reachable"]]
ASSOC = [r for r in sd.LISTS if r["kind"] == "association" and r["reachable"]]
COMM = [r for r in sd.LISTS if r["kind"] == "commercial" and r["reachable"]]
NCH = len(CH)
CHAPTER_LISTINGS = sum(r["n"] for r in CH if r["n"])
NFREE = len([r for r in sd.LISTS if r["free"] and r["reachable"]])

# The Board's own 2024 Pathway to Licensure survey, from the 2025 Sunset
# Review Report, Attachment C-1C. Q17 n=3,168; Q18 n=559. Brackets are the
# Board's, and the top one is uncapped, which is why no average is computed
# here - an average over a censored top bracket is a made-up number.
PAID_YES, PAID_N = 18, 3168
COST = [("Under $50", 2, 11), ("$50 to $100", 12, 68),
        ("$100 to $150", 13, 73), ("$150 to $200", 15, 86),
        ("$200 to $250", 11, 60), ("$250 to $300", 11, 64),
        ("More than $300", 35, 197)]
COST_N = 559
COST_TOP = 35


def kindname(k):
    return {"chapter": "CAMFT chapter", "association": "Association",
            "commercial": "Commercial"}[k]


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "Finding a supervisor &middot; every list fetched %s" % sd.CHECKED,
        "California licenses 165,000 people and publishes a list of exactly "
        "zero supervisors.",
        "The Board does not certify supervisors and keeps no roster, so this "
        "is where the lists actually are &mdash; each one fetched and counted "
        "&mdash; plus the rule that decides whether the person you find can "
        "lawfully supervise you at all.",
        [("0", "on any official list"),
         ("%d of 23" % NCH, "CAMFT chapters publish one"),
         (format(CHAPTER_LISTINGS, ",d"), "listings across those %d" % NCH),
         ("%d%%" % COST_TOP, "of payers pay over $300 a month")],
        JUMPS))

    # ----------------------------------------------------------------- lists
    o.append('<section class="pk-sec" id="lists">')
    o.append(pk.quote(
        "Why there is no official list",
        ["The Board of Behavioral Sciences sets the rules a supervisor has to "
         "meet, publishes the forms, and disciplines supervisors who break "
         "them. It does not approve them in advance, does not keep a register "
         "of them, and its license lookup has no supervisor field.",
         "So there is nothing to search. What exists instead is nine county "
         "chapter directories, one statewide association list with no contact "
         "details on it, and two commercial products &mdash; and a reader who "
         "searches this question is handed at least three addresses that no "
         "longer exist."]))

    o.append('<p class="pk-k">Every list, fetched %s</p>' % sd.CHECKED)
    o.append('<h2 class="pk-h">The %d places a California supervisor list '
             "actually is.</h2>" % len([r for r in sd.LISTS if r["reachable"]]))
    o.append('<p class="pk-d">Counts are what each source reports on its own '
             "page. Nothing from any of these directories is copied here "
             "&mdash; they are other people&rsquo;s membership lists, and the "
             "useful finding is which ones are real and how big they are, not "
             "the names inside them.</p>")

    rows = []
    for r in sorted(sd.LISTS, key=lambda x: (x["kind"] != "association",
                                             -(x["n"] or 0))):
        if not r["reachable"]:
            continue
        n = format(r["n"], ",d") if r["n"] else "&mdash;"
        rows.append([
            '<a href="%s" rel="nofollow noopener" target="_blank"><b>%s</b></a>'
            % (r["url"], r["name"]),
            kindname(r["kind"]),
            (n, "f"),
            r["fields"],
            "Free" if r["free"] else "Account needed",
        ])
    o.append(pk.table(
        ["List", "Who runs it", "Entries", "What it shows", "To read it"],
        rows,
        caption="Psychology Today is the largest by a wide margin and the "
                "category on it is self-declared &mdash; a paid profile with a "
                "box ticked, not a credential anybody checked. CAMFT&rsquo;s "
                "own list is the opposite: the people on it hold a real "
                "certification, and the directory gives you a name and a city "
                "and nothing else.",
        minw=900))

    o.append(pk.callout(
        "The coverage is not where the people are",
        ["<b>An associate in Petaluma has better options than one in San "
         "Diego.</b> Marin&rsquo;s chapter publishes 116 names and the "
         "Redwood Empire 99, for a combined population under a million. "
         "<b>San Diego, Sacramento, San Francisco, Santa Clara Valley, the "
         "San Fernando Valley and Ventura publish none at all</b> &mdash; "
         "that is most of the state&rsquo;s associates.",
         "Which means the sensible order is: check whether your own chapter "
         "is one of the nine, then check the neighboring chapters anyway, "
         "because supervision by video is lawful and the lists do not stop at "
         "a county line."]))

    o.append('<p class="pk-k">Checked, and there is nothing there</p>')
    o.append('<h3 class="pk-h" style="font-size:22px">The %d places people are '
             "sent that do not have a list.</h3>" % len(sd.NEGATIVE))
    rows = []
    for r in sd.NEGATIVE:
        rows.append(['<a href="%s" rel="nofollow noopener" target="_blank">'
                     "<b>%s</b></a>" % (r["url"], r["name"]), r["why"]])
    o.append(pk.table(["Where people look", "What is actually there"], rows,
                      minw=680))
    o.append('<p class="pk-d"><b>The %d CAMFT chapters with no supervision '
             "directory:</b> %s. Several of them run a therapist directory or "
             "a job board, which is not the same thing and does not say who "
             "supervises.</p>"
             % (len(sd.NO_CHAPTER_LIST), ", ".join(sd.NO_CHAPTER_LIST)))

    dead = [d for d in sd.DEAD]
    o.append('<p class="pk-k">Still ranked, no longer there</p>')
    o.append('<h3 class="pk-h" style="font-size:22px">Three addresses that are '
             "gone, and are still being handed out.</h3>")
    rows = []
    for d in dead:
        state = ("resolves, and lands on <b>%s</b>, an unrelated commercial "
                 "site" % d["landed"]) if d["landed"] else \
                "does not resolve at all"
        rows.append([("<code>%s</code>" % d["host"], "m"), d["name"],
                     "%s &mdash; %s" % (state, d["why"])])
    o.append(pk.table(["Address", "What it used to be", "What answers now"],
                      rows, minw=780,
                      caption="The first one is the dangerous shape. A domain "
                              "that fails to load sends a reader looking; a "
                              "domain that was sold and now loads a working, "
                              "unrelated site reads as though the chapter "
                              "moved on, which it did not &mdash; it closed. "
                              "CAMFT&rsquo;s own chapter-links page still "
                              "points at two of these.", ))
    o.append("</section>")

    # ------------------------------------------------------------------ trap
    o.append('<section class="pk-sec" id="trap">')
    o.append('<p class="pk-k">The part that costs people months</p>')
    o.append('<h2 class="pk-h">In a private practice, you cannot simply hire '
             "your own supervisor.</h2>")
    o.append('<p class="pk-d">This is the single most expensive '
             "misunderstanding in California supervision, and it is easy to "
             "hold, because paying somebody for their professional time is "
             "normally all it takes.</p>")

    o.append(pk.numbered([
        ("1", "The supervisor has to be on the practice&rsquo;s books",
         "<a href=\"%s\">BPC &sect;4980.43.4(b)(1)</a> requires a supervisor "
         "of an associate in a private practice or professional corporation "
         "to be <b>employed by, contracted by, or an owner of the "
         "associate&rsquo;s employer</b>. Those are the three permitted "
         "statuses. &ldquo;Paid by the associate&rdquo; is not one of them."
         % bpc("4980.43.4")),
        ("2", "So a privately retained supervisor does not count",
         "If you find somebody, pay them yourself, and your employer has no "
         "relationship with them, the weeks are not creditable in a private "
         "practice. The work happened, the supervision happened, and the "
         "hours do not exist as far as the Board is concerned."),
        ("3", "There is a lawful route, and it needs your employer to act",
         "The employer contracts the supervisor. The supervisor either sees "
         "clients for that employer, or holds a written contract giving them "
         "employee-equivalent access to your clinical records plus client "
         "authorization to release those records &mdash; "
         "<a href=\"%s\">&sect;4980.43.4(b)(2)</a>. Then a <b>written "
         "oversight agreement between the supervisor and the employer</b> is "
         "executed under <a href=\"%s\">&sect;4980.43.4(d)</a> and "
         "<a href=\"%s\">16 CCR &sect;1833(a)</a>, and that one has to be "
         "signed <b>before supervision starts</b>, not within any grace "
         "period." % (bpc("4980.43.4"), bpc("4980.43.4"), CCR % "1833")),
        ("4", "Who ends up paying is not regulated",
         "Nothing in the statute says whose money it is. The associate may "
         "reimburse the cost. What the statute governs is the <b>contract "
         "line</b> &mdash; it has to run employer to supervisor, not "
         "associate to supervisor."),
        ("5", "None of this applies in an exempt setting",
         "&sect;4980.43.4(b) is written only for &ldquo;a private practice or "
         "a professional corporation.&rdquo; A county agency, a school, a "
         "college or a nonprofit charitable organization is an <b>exempt "
         "setting</b> under <a href=\"%s\">BPC &sect;4980.01(c)</a>, and the "
         "employment-nexus rule does not reach it. The oversight agreement "
         "still does, for any supervisor who is not employed there."
         % bpc("4980.01")),
    ]))

    o.append(pk.callout(
        "One more limit worth knowing before you ask",
        ["A supervisor in a <b>nonexempt</b> setting may hold no more than "
         "<b>six</b> individual or triadic supervisees at a time &mdash; "
         "<a href=\"%s\">BPC &sect;4980.43.4(c)</a>, and the same number at "
         "<a href=\"%s\">&sect;4996.23.3(c)</a> and "
         "<a href=\"%s\">&sect;4999.46.4(c)</a>. A private practice is always "
         "nonexempt, so a busy supervisor in one may simply be full."
         % (bpc("4980.43.4"), bpc("4996.23.3"), bpc("4999.46.4")),
         "The six is counted across every nonexempt setting the supervisor "
         "works in, and it counts pre-licensed people of any kind &mdash; "
         "AMFTs, ASWs, APCCs, trainees, social work interns and Board of "
         "Psychology pre-licensees. <b>Group supervisees do not count toward "
         "it</b>, and there is no limit at all in an exempt setting. Those "
         "two qualifiers are the Board&rsquo;s, from its "
         "<a href=\"%s\" rel=\"nofollow noopener\" target=\"_blank\">FAQs for "
         "Supervisors</a>, not from the statute." % SUPFAQ]))
    o.append("</section>")

    # --------------------------------------------------------------- qualify
    o.append('<section class="pk-sec" id="qualify">')
    o.append('<p class="pk-k">Before you sign anything</p>')
    o.append('<h2 class="pk-h">Whether this person may lawfully supervise '
             "you.</h2>")
    o.append('<p class="pk-d">Every one of these is on the supervisor, not on '
             "you. They are worth checking anyway, because the consequence of "
             "getting it wrong lands on your hours, and a supervisor who is "
             "wrong about their own eligibility is wrong in good faith.</p>")

    rows = [
        ["<b>The license</b>",
         "LMFT, LCSW, LPCC, licensed psychologist, licensed educational "
         "psychologist, or a physician certified in psychiatry by the ABPN",
         '<a href="%s">&sect;4980.03(g)(1)</a>' % bpc("4980.03")],
        ["<b>Current and active, in California</b>",
         "Held now, not under suspension and not on probation. An "
         "out-of-state license does not substitute",
         '<a href="%s">&sect;4980.03(g)(5)</a>' % bpc("4980.03")],
        ["<b>Two years of the last five</b>",
         "Licensed at least two years within the past five &mdash; and "
         "<b>time licensed in another state counts</b> toward that clock, so "
         "somebody newly licensed in California may still qualify",
         '<a href="%s">&sect;4980.03(g)(1)</a>' % bpc("4980.03")],
        ["<b>Actually practiced</b>",
         "Practiced psychotherapy, or provided clinical supervision of it, "
         "in that same two-of-five window",
         '<a href="%s">&sect;4980.03(g)(2)</a>' % bpc("4980.03")],
        ["<b>Fifteen hours of supervision training</b>",
         "Within two years before starting to supervise, <b>or within 60 days "
         "after</b> &mdash; so a supervisor who has not done it yet is not "
         "automatically disqualifying",
         '<a href="%s">16 CCR &sect;1834(a)</a>' % (CCR % "1834")],
        ["<b>Six hours every renewal after that</b>",
         "Continuing professional development in supervision, each renewal "
         "period. Psychologists and psychiatrists are exempt from both "
         "training requirements",
         '<a href="%s">16 CCR &sect;1834(c)</a>' % (CCR % "1834")],
        ["<b>Never your own therapist</b>",
         "Not now and not ever &mdash; the statute reads &ldquo;has not "
         "provided therapeutic services to the supervisee&rdquo;",
         '<a href="%s">&sect;4980.03(g)(4)</a>' % bpc("4980.03")],
        ["<b>Not a spouse, partner or relative</b>",
         "And separately, hours obtained under one are <b>not credited</b>, "
         "which is the part that bites",
         '<a href="%s">&sect;4980.43.3(d)</a>' % bpc("4980.43.3")],
        ["<b>No relationship that undermines the supervision</b>",
         "A standard rather than a list. Being your employee, or your own "
         "supervisee elsewhere, is not separately banned &mdash; it is "
         "measured against this",
         '<a href="%s">&sect;4980.03(g)(7)</a>' % bpc("4980.03")],
    ]
    o.append(pk.table(["What has to be true", "In plain terms", "Where it says so"],
                      rows, minw=880,
                      caption="These are the MFT sections. The social work and "
                              "counseling chapters carry the same test in the "
                              "same words &mdash; BPC &sect;4996.20(a) for an "
                              "ASW, BPC &sect;4999.12(h) for an APCC."))

    o.append(pk.callout(
        "If you are an ASW, two more rules apply and nobody else has them",
        ["<b>1,700 of your 3,000 hours must be supervised by an LCSW</b> "
         "&mdash; <a href=\"%s\">BPC &sect;4996.23(d)(1)(A)</a>. The rest may "
         "be under any of the qualifying licenses."
         % bpc("4996.23"),
         "<b>And 13 of your 52 individual or triadic weeks must be under an "
         "LCSW</b> &mdash; <a href=\"%s\">BPC &sect;4996.23.1(g)</a>. These "
         "are two independent requirements. Meeting one does not meet the "
         "other, and it is possible to satisfy the 1,700 hours and still be "
         "short on the weeks."
         % bpc("4996.23.1"),
         "There is no equivalent rule for AMFTs or APCCs. Neither chapter "
         "requires any minimum number of hours or weeks under a supervisor "
         "holding the same license as the one you are working toward."]))
    o.append("</section>")

    # ------------------------------------------------------------------ week
    o.append('<section class="pk-sec" id="week">')
    o.append('<p class="pk-k">The shape of the week</p>')
    o.append('<h2 class="pk-h">One hour a week is the floor, and it is per '
             "setting, not per person.</h2>")
    o.append('<p class="pk-d">The Board calls an hour of individual or triadic '
             "supervision, or two hours of group, a <b>unit</b>. That word is "
             "not in the statute &mdash; the statute says &ldquo;one hour of "
             "direct supervisor contact&rdquo; and then defines what counts "
             "as one. Both are used below because both are used in the "
             "wild.</p>")

    rows = [
        ["At least one hour of direct supervisor contact <b>in each week, in "
         "each work setting</b> for which hours are claimed",
         '<a href="%s">&sect;4980.43.2(a)(1)</a>' % bpc("4980.43.2")],
        ["One hour individual, one hour triadic, or <b>two hours of group</b> "
         "&mdash; group with no more than eight people receiving supervision",
         '<a href="%s">&sect;4980.43.2(b)(1)</a>' % bpc("4980.43.2")],
        ["A <b>second</b> hour in any week with more than <b>10 hours of "
         "direct clinical counseling in that setting</b>. Two is the ceiling "
         "the rule ever asks for, however busy the week",
         '<a href="%s">&sect;4980.43.2(a)(3)</a>' % bpc("4980.43.2")],
        ["No more than <b>six hours</b> of supervision credited in any single "
         "week, individual, triadic and group combined",
         '<a href="%s">&sect;4980.43.2(a)(2)</a>' % bpc("4980.43.2")],
        ["Of the 104 supervised weeks, <b>52 must be individual or "
         "triadic</b>, or a combination of the two",
         '<a href="%s">&sect;4980.43.2(a)(4)</a>' % bpc("4980.43.2")],
        ["The supervision has to happen <b>in the same week</b> as the hours "
         "it covers",
         '<a href="%s">&sect;4980.43.2(e)</a>' % bpc("4980.43.2")],
        ["Video counts as face to face, and the supervisor has to document "
         "that it is clinically appropriate <b>within 60 days</b> of starting",
         '<a href="%s">&sect;4980.43.2(b)(2), (d)(1)</a>' % bpc("4980.43.2")],
    ]
    o.append(pk.table(["The rule", "Section"], rows, minw=760,
                      caption="Parallel sections govern the other two "
                              "registrations: BPC &sect;4996.23.1 for an ASW "
                              "&mdash; whose six-hour weekly ceiling sits at "
                              "&sect;4996.23(d)(6) instead &mdash; and BPC "
                              "&sect;4999.46.2 for an APCC."))

    o.append(pk.callout(
        "The one that catches people at a county clinic",
        ["<b>The second hour is triggered per setting, and the first hour is "
         "owed per setting.</b> Somebody working two days at a clinic and one "
         "evening at a nonprofit owes an hour in each place, every week they "
         "claim hours in it &mdash; and if the clinic week goes over ten "
         "direct hours, that setting owes two.",
         "Which is why &ldquo;my supervisor is only on site twice a "
         "week&rdquo; is a scheduling problem that quietly becomes an hours "
         "problem. The weeks that fall short are not partly creditable. "
         "<a href=\"%s\">The 3,000-hour tool</a> shows what that does to a "
         "finish date." % HOURS]))

    o.append('<p class="pk-d"><b>A trainee is on a different rule entirely.</b> '
             "Somebody still in a degree program owes an average of one hour "
             "of supervision for every <b>five</b> hours of direct clinical "
             "counseling each week, in each setting &mdash; "
             '<a href="%s">&sect;4980.43.2(a)(2)</a> &mdash; and may not work '
             "in a private practice at all. That is covered on "
             '<a href="%s">the practicum page</a>.</p>'
             % (bpc("4980.43.2"), PRACTICUM))
    o.append("</section>")

    # ------------------------------------------------------------------ cost
    o.append('<section class="pk-sec" id="cost">')
    o.append('<p class="pk-k">What it costs</p>')
    o.append('<h2 class="pk-h">Nobody publishes a rate. The Board asked 3,168 '
             "people what they paid.</h2>")
    o.append('<p class="pk-d">There is no fee schedule for supervision in '
             "California and no survey of what supervisors charge. What does "
             "exist is one question in the Board&rsquo;s own <b>Pathway to "
             "Licensure survey</b>, run in 2024 and published inside the 2025 "
             "Sunset Review Report. It asked supervisees what they paid, "
             "which is a different measure from what supervisors charge, and "
             "it is the only public California figure there is.</p>")

    o.append(pk.callout(
        "First, most people do not pay at all",
        ["<b>%d%% of %s respondents said they paid for supervision.</b> The "
         "other %d%% did not &mdash; their employer provided it, which is the "
         "normal arrangement at a county agency, a nonprofit or a group "
         "practice, and one of the reasons those jobs are worth more than "
         "their salary line suggests."
         % (PAID_YES, format(PAID_N, ",d"), 100 - PAID_YES),
         "So the figures below describe the minority who paid, and they are "
         "the ones worth planning around if you are heading for a private "
         "practice placement."], big="%d%%" % PAID_YES))

    rows = []
    for label, pctv, n in COST:
        bar = int(round(pctv * 2.2))
        rows.append([("<b>%s</b>" % label),
                     ("%d%%" % pctv, "f"),
                     (format(n, ",d"), "f"),
                     '<span style="letter-spacing:-1px">%s</span>'
                     % ("&#9608;" * max(1, bar))])
    o.append(pk.table(
        ["Paid per month", "Share", "People", ""], rows, minw=620,
        caption="Board of Behavioral Sciences, Pathway to Licensure survey "
                "2024, question 18, %d respondents who said they paid. "
                "<b>Read it carefully:</b> respondents were self-selected "
                "rather than sampled, they span licensure years from the "
                "1950s to 2024 with no adjustment for inflation, the top "
                "bracket is uncapped, and it records what people paid, not "
                "what anybody charges. No average is computed here, because "
                "an average over an open-ended top bracket would be an "
                "invented number." % COST_N))

    o.append('<p class="pk-d">The Board itself treats this as a problem rather '
             "than a market. Its current strategic plan carries an unmet goal "
             "to &ldquo;explore ways to reduce financial burdens that arise "
             "from supervision fees,&rdquo; and its own report names the cost "
             "of supervision, alongside the difficulty of finding a "
             "supervisor at all, as a barrier to entering the "
             "profession.</p>")

    o.append('<h3 class="pk-h" style="font-size:22px">And no, you almost '
             "certainly cannot deduct it.</h3>")
    o.append('<p class="pk-d">This is asked constantly and answered wrongly '
             "almost everywhere, so it is worth three careful "
             "sentences.</p>")
    o.append(pk.numbered([
        ("1", "Federally, an employee deducts nothing",
         "A registered associate is required to be a W-2 employee or a "
         "volunteer, never an independent contractor "
         "(<a href=\"%s\">&sect;4980.43.3(a)</a>). Unreimbursed employee "
         "business expenses have been disallowed since 2018, and the "
         "One Big Beautiful Bill Act of July 2025 made that permanent rather "
         "than letting it lapse at the end of 2025. It now sits at "
         "<a href=\"https://www.law.cornell.edu/uscode/text/26/67\">26 U.S.C. "
         "&sect;67(h)</a> &mdash; the subsection was relettered, so a page "
         "citing &sect;67(g) for this is citing something else."
         % bpc("4980.43.3")),
        ("2", "California does not follow, which helps a little",
         "California never conformed, and unreimbursed employee expenses "
         "&mdash; the form names &ldquo;job education&rdquo; explicitly "
         "&mdash; still come off on Schedule CA (540), Part II, to the extent "
         "they exceed 2% of your federal adjusted gross income. You may "
         "itemize for California even if you took the federal standard "
         "deduction."),
        ("3", "But there is a prior question, and it is the one that bites",
         "Education that qualifies you for a <b>new trade or business</b> is "
         "never deductible, by anybody, employee or not &mdash; Treasury "
         "Regulation &sect;1.162-5(b)(3). Hours accumulated toward a license "
         "you do not yet hold are the textbook example. California&rsquo;s "
         "own Office of Tax Appeals applied exactly that reasoning to a "
         "psychology doctoral student. Once you are licensed and "
         "self-employed, supervision or consultation that maintains your "
         "existing license is a different question and an easier one."),
    ]))
    o.append('<p class="pk-fine">That is a reading of published law, not tax '
             "advice, and the pre-licensure question has never been decided "
             "for clinical supervision specifically. If you are paying for "
             "supervision, the arrangement worth asking your employer about "
             "is <b>reimbursement under an accountable plan</b>, which is "
             "excluded from your wages and deducted by them, and sidesteps "
             "the whole question. There is more on what is and is not "
             "deductible in a therapy practice on "
             "<a href=\"%s\">the deductions page</a>.</p>" % DEDUCT)

    o.append('<h3 class="pk-h" style="font-size:22px">If you are being asked '
             "to work unpaid, two agencies disagree.</h3>")
    o.append('<p class="pk-d">The Board accepts volunteer hours and says only '
             "that employers are <b>encouraged</b> to pay. The Labor "
             "Commissioner has taken the position since 2000 that somebody "
             "volunteering to a <b>for-profit</b> business to gain experience "
             "in an occupation is an employee entitled to at least the "
             "minimum wage, and that the nature of the organization is what "
             "decides it &mdash; a public agency or a nonprofit is different. "
             "Board acceptance of your hours is not a finding that the "
             "arrangement was lawful; they are two agencies answering two "
             "questions. <a href=\"%s\">What unpaid associate work actually "
             "costs</a> works the arithmetic.</p>" % UNPAID)
    o.append("</section>")

    # ----------------------------------------------------------------- paper
    o.append('<section class="pk-sec" id="paper">')
    o.append('<p class="pk-k">Three deadlines, and they are not the same one</p>')
    o.append('<h2 class="pk-h">The paperwork, and which piece goes where.</h2>')
    o.append('<p class="pk-d">Two of these are due within 60 days and one is '
             "due before you start, which is the part that gets missed. One "
             "is filed with the Board and two are kept.</p>")

    rows = [
        ["<b>Written oversight agreement</b>",
         "Only when the supervisor is not employed by your employer, or is a "
         "volunteer",
         "<b>Before supervision starts</b>",
         "Between the <b>supervisor and the employer</b> &mdash; you are not "
         "a party to it",
         '<a href="%s">&sect;4980.43.4(d)</a>, <a href="%s">16 CCR '
         "&sect;1833(a)</a>" % (bpc("4980.43.4"), CCR % "1833")],
        ["<b>Supervision Agreement</b> (form 37M-300)",
         "Every supervisory relationship",
         "Within <b>60 days</b> of supervision commencing",
         "Signed under penalty of perjury and <b>kept by you</b>. The "
         "originals go to the Board with your licensure application, not "
         "before",
         '<a href="%s">16 CCR &sect;1833(c)</a>' % (CCR % "1833")],
        ["<b>Supervisor Self-Assessment</b> (form 37M-302)",
         "Your supervisor, the first time they ever supervise",
         "Within <b>60 days</b>",
         "<b>Submitted to the Board</b>, once in a career &mdash; not once "
         "per supervisee",
         '<a href="%s">16 CCR &sect;1833.1(d)</a>' % (CCR % "1833.1")],
    ]
    o.append(pk.table(["What", "When it applies", "By when", "Where it goes",
                       "Section"], rows, minw=960))

    o.append('<p class="pk-fine">A note on form numbers, because the wrong one '
             "circulates: <b>37M-300</b> is the Supervision Agreement. "
             "<b>37A-525</b> is the weekly log of experience hours, a "
             "different document that carries its own "
             "&ldquo;do not submit&rdquo; instruction, which is probably how "
             "the two got conflated.</p>")

    o.append(pk.callout(
        "Why the signature matters more than it looks",
        ["The Board&rsquo;s discipline record contains cases built entirely on "
         "supervision paperwork. One associate <a href=\"%s\">signed her "
         "supervisor&rsquo;s name</a> to her own hours. Another submitted "
         "<a href=\"%s\">a forged supervisor signature</a>. A third spent "
         "<a href=\"%s\">seven years under supervision</a> as a condition of "
         "practicing at all." % (SIGNED, FORGED, SEVEN),
         "The forms are the entire evidence base for three thousand hours of "
         "your working life. <a href=\"%s\">All 48 decisions</a> are "
         "summarized on this site, de-identified." % CASES]))
    o.append("</section>")

    # ------------------------------------------------------------------- ask
    o.append('<section class="pk-sec" id="ask">')
    o.append(pk.checklist(
        "What to ask before you agree to anything",
        ["<b>Are you employed by, contracted by, or an owner of my "
         "employer?</b> In a private practice this is the question that "
         "decides whether the hours exist. If the answer is none of the "
         "three, ask who is going to arrange the contract and the oversight "
         "agreement, and when.",
         "<b>How many individual or triadic supervisees do you have right "
         "now, across all your nonexempt settings?</b> The limit is six, and "
         "it is the supervisor&rsquo;s responsibility to count.",
         "<b>Have you done the 15 hours of supervision training, and when is "
         "your next renewal?</b> Six hours of it are due every renewal after "
         "the first.",
         "<b>Which weeks will you be away, and who covers them?</b> A missed "
         "week is not partly creditable. Substitute supervision has its own "
         "rules, at 16 CCR &sect;1833.1.5.",
         "<b>Will any of this be by video, and have you documented that it is "
         "appropriate?</b> That documentation is due within 60 days.",
         "<b>What happens to my signed hours if I leave, or if you do?</b> "
         "Ask now, in writing, while everybody is well disposed. The "
         "discipline record is full of people who asked at the end.",
         "<b>What does it cost, per month, and does it change if my caseload "
         "goes over ten direct hours in a week?</b> That week needs a second "
         "hour, and somebody is paying for it.",
         "<b>If I am paying you directly and I am in a private practice, how "
         "is that lawful?</b> A supervisor who cannot answer this has not "
         "read &sect;4980.43.4(b), and it is your hours that are at stake."]))

    o.append('<p class="pk-d">And two things worth doing yourself: check the '
             "license on the Department of Consumer Affairs lookup before the "
             "first session &mdash; it shows status, discipline and the issue "
             "date, which is how you confirm the two-of-five years &mdash; "
             "and keep your own copy of every signed page. "
             "<a href=\"%s\">The hours trackers compared</a> covers where "
             "people keep them." % TRACKERS)
    o.append("</section>")

    # --------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("Who may supervise, and the private-practice rule", [
            ("BPC &sect;4980.03(g) &mdash; supervisor qualifications, MFT",
             bpc("4980.03")),
            ("BPC &sect;4996.20(a) &mdash; supervisor qualifications, social "
             "work", bpc("4996.20")),
            ("BPC &sect;4999.12(h) &mdash; supervisor qualifications, "
             "counseling", bpc("4999.12")),
            ("BPC &sect;4980.43.4 &mdash; supervision in a private practice, "
             "the oversight agreement, and the six-supervisee limit",
             bpc("4980.43.4")),
            ("BPC &sect;4980.01(c) &mdash; what an exempt setting is",
             bpc("4980.01")),
            ("BPC &sect;4980.43.3 &mdash; employee or volunteer, never an "
             "independent contractor", bpc("4980.43.3")),
            ("BPC &sect;4996.23(d)(1)(A) &mdash; 1,700 hours under an LCSW",
             bpc("4996.23")),
            ("BPC &sect;4996.23.1(g) &mdash; 13 weeks under an LCSW",
             bpc("4996.23.1")),
        ]),
        ("The supervision week, and the training a supervisor owes", [
            ("BPC &sect;4980.43.2 &mdash; frequency, format and the "
             "ten-hour trigger", bpc("4980.43.2")),
            ("BPC &sect;4996.23.1 &mdash; the same, for an ASW",
             bpc("4996.23.1")),
            ("BPC &sect;4999.46.2 &mdash; the same, for an APCC",
             bpc("4999.46.2")),
            ("16 CCR &sect;1833 &mdash; the oversight agreement and the "
             "60-day supervision agreement", CCR % "1833"),
            ("16 CCR &sect;1833.1 &mdash; supervisor responsibilities and the "
             "self-assessment", CCR % "1833.1"),
            ("16 CCR &sect;1834 &mdash; 15 hours of training, then 6 per "
             "renewal", CCR % "1834"),
        ]),
        ("The Board&rsquo;s own documents", [
            ("Supervision Agreement, form 37M-300", AGREEMENT),
            ("Supervisor Self-Assessment Report, form 37M-302", SELFASSESS),
            ("FAQs for Supervisors", SUPFAQ),
            ("Summary of Supervisor Qualifications", SUPQUAL),
            ("Supervisor resources", BBSSUP),
            ("2025 Sunset Review Report &mdash; the 2024 Pathway to "
             "Licensure survey is Attachment C-1C", SUNSET),
        ]),
        ("On pay, and on what supervision costs", [
            ("Labor Commissioner opinion letter 2000.11.03, on volunteering "
             "to a for-profit business", DLSE),
            ("26 U.S.C. &sect;67 &mdash; the disallowance, now at "
             "subsection (h)", "https://www.law.cornell.edu/uscode/text/26/67"),
            ("Treasury Regulation &sect;1.162-5 &mdash; education that "
             "qualifies you for a new trade or business",
             "https://www.law.cornell.edu/cfr/text/26/1.162-5"),
            ("Schedule CA (540) &mdash; where California still allows the "
             "expense", "https://www.ftb.ca.gov/forms/2025/2025-540-ca.pdf"),
        ]),
        ("Where this comes up elsewhere on this site", [
            ("What is actually holding up your 3,000 hours",
             "https://therapistsupport.org/%s" % HOURS),
            ("Comparing associate jobs, including who provides supervision",
             "https://therapistsupport.org/%s" % ADVISOR),
            ("What unpaid associate work costs",
             "https://therapistsupport.org/%s" % UNPAID),
            ("Getting hired as a California associate",
             "https://therapistsupport.org/%s" % HIRED),
            ("Hiring your first associate, from the other side",
             "https://therapistsupport.org/%s" % HIRING),
            ("Every licensure requirement, with its code section",
             "https://therapistsupport.org/%s" % BECOME),
        ]),
    ], note="Every directory on this page was fetched by "
            "<b>_dev/supervisor_lists.py</b> on %s, and the entry counts are "
            "what each source reports about itself. <b>No listing from any of "
            "them is reproduced here.</b> A link is an address, not a "
            "recommendation: this site has not met these supervisors, does "
            "not check them, and takes nothing from anybody for a mention. "
            "Statute and regulation text was read at the linked sections; "
            "where a rule comes from the Board&rsquo;s interpretation rather "
            "than from the code, it says so on the page. None of this is "
            "legal, tax or career advice." % sd.CHECKED)
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Finding a clinical supervisor in California: every list, checked",
    "There is no official list of California clinical supervisors, so here is "
    "every list that does exist, fetched and counted - plus the private "
    "practice rule that decides whether the person you find can count your "
    "hours at all.",
    "licensure", "reference",
    "How do I find a clinical supervisor in California?",
    "Where every real supervisor list is, what the Board requires of a "
    "supervisor, and why a privately hired supervisor does not count in a "
    "private practice",
    "%d of 23 CAMFT chapters publish a supervisor list" % NCH,
    weight=4)


def main():
    print("finding a clinical supervisor")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d lists, %d sources"
          % (PAGE, format(len(html), ",d"),
             len([r for r in sd.LISTS if r["reachable"]]), nsrc))

    bad = pk.check_page(p, [
        ("the finding the page exists for", "cannot simply hire your own"),
        ("the no-roster fact", "keeps no roster"),
        ("the survey caveat", "self-selected rather than sampled"),
        ("the form-number correction", "37A-525"),
        ("the two-agency point", "two agencies answering two questions"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every list that answered must be on the page, and every list that did
    # not must be absent. Publishing an address that did not respond, on a
    # page whose argument is that half these addresses are dead, would be
    # self-defeating.
    for r in sd.LISTS:
        present = r["url"] in art
        if r["reachable"] and not present:
            print("GUARD: %s answered and is not on the page" % r["key"])
            bad += 1
        if not r["reachable"] and present:
            print("GUARD: %s did not answer and must not be published"
                  % r["key"])
            bad += 1

    # Nine publish one, twelve do not, and two closed. That has to add to the
    # 23 chapters the page claims, or one of the three lists has drifted.
    dead_chapters = len([d for d in sd.DEAD if "CAMFT" in d["name"]])
    if NCH + len(sd.NO_CHAPTER_LIST) + dead_chapters != 23:
        print("GUARD: %d publish + %d do not + %d closed is not 23 chapters"
              % (NCH, len(sd.NO_CHAPTER_LIST), dead_chapters))
        bad += 1

    # The counts in the hero are computed; the prose must not contradict them.
    if "%d of 23" % NCH not in art:
        print("GUARD: the chapter coverage figure is not on the page")
        bad += 1
    if format(CHAPTER_LISTINGS, ",d") not in art:
        print("GUARD: the chapter listing total is not on the page")
        bad += 1

    # It reports on other people's directories and must never become one.
    # Nothing here should look like a person's listing: a name next to a phone
    # number is the shape to catch.
    if re.search(r"\(\d{3}\)\s?\d{3}-\d{4}", art):
        print("GUARD: a telephone number appears - no listing may be "
              "reproduced from any directory")
        bad += 1
    # It links to directories; it must never endorse a person on one. The
    # bare word "recommend" cannot be the test - the disclaimer that says a
    # link is not a recommendation contains it, and a guard that fires on its
    # own disclaimer is a guard somebody switches off.
    for phrase in ("we recommend", "recommended supervisor", "our pick",
                   "the best supervisor", "we suggest you contact"):
        if phrase in art.lower():
            print("GUARD: the page appears to recommend a supervisor: %r"
                  % phrase)
            bad += 1

    # The cost brackets are the Board's and must ship whole - a subset would
    # misrepresent a distribution.
    for label, _p, _n in COST:
        if label not in art:
            print("GUARD: the %r cost bracket is missing" % label)
            bad += 1
    # And no average may be computed over an uncapped top bracket.
    for phrase in ("on average", "the average supervisor charges",
                   "average cost of supervision"):
        if phrase in art.lower():
            print("GUARD: an average over an open-ended bracket: %r" % phrase)
            bad += 1

    # The word this site removed sitewide.
    for m in re.finditer(r"\bgates?\b", re.sub(r"<[^>]+>", " ", art), re.I):
        print("GUARD: %r" % m.group(0))
        bad += 1

    for w in pk.spelling(s):
        print("GUARD: British spelling %r" % w)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
