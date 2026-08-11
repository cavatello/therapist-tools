#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The practicum year: the rules, and how each of the 78 programs places you.

WHY THIS PAGE EXISTS

The site has 78 program pages, a licensure hub, an associate hours calculator
and a hiring page. It has nothing at all for the person who is already
enrolled and about to start seeing clients - which is the single most anxious
year of the whole path, and the one where the rules are least known.

Two things nobody has published:

1. WHAT A TRAINEE MAY ACTUALLY DO. The rules are spread across four sections
   of the Business and Professions Code and they are unusually strict. A
   trainee cannot work in a private practice at all. Not as an employee, not
   as a volunteer, not with a willing supervisor. An associate can, once
   registered; a trainee never can. People find this out after arranging a
   placement.

2. HOW EACH PROGRAM HANDLES THE PLACEMENT. 29 of 78 do not say anywhere
   public. 10 say plainly that finding the site is the student's job. The
   comparison does not exist anywhere, and it is the thing that decides
   whether the practicum year is administered or survived.

THE FINDING THAT TIES THE TWO TOGETHER

Section 4980.42(e) says the school shall approve each site and shall have a
written agreement with it detailing each party's responsibilities. So even
where the student sources the site, the school cannot simply wave it through
- the obligation to hold the agreement is the school's, by statute. A student
told to "find your own placement" is entitled to ask which of them is going
to sign that, and that is a far more useful sentence than any encouragement.

THE OTHER FINDING, WHICH BELONGS TO THE CAREER-CHANGE PAGE TOO

Only the MFT license lets pre-degree hours count. Section 4980.43(c)(4)
allows a maximum of 1,300 of the 3,000 hours before the degree is awarded.
Section 4999.46(c)(1) requires the LPCC's 3,000 to be postdegree, and section
4996.23(a) requires the LCSW's to be post-master's. Same practicum, same
work, and only one of the three licenses banks it.

GUARDS

Every one of the 78 must appear. A program missing from a placement table
reads as "no information", which is different from "not published" and is
never what it means. The 1,300 / 750 / 90-day figures each have to be on the
page, and the no-private-practice rule has to be stated before the placement
table rather than after it.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import practicum_data as pd

SITE = pk.SITE
PAGE = "practicum-california-mft-trainee.html"
DONOR = "county-therapist-pay-california.html"

PROGRAMS = "mft-programs-california.html"
BECOME = "become-an-mft-california.html"
HIRED = "getting-hired-as-a-california-associate.html"
CALC = "amft-3000-hours-california.html"
UNPAID = "associate-unpaid-hours-california.html"
TIMES = "bbs-processing-times-california.html"
FEES = "bbs-fees-california-2026.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"

LEG = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
       "?lawCode=BPC&sectionNum=%s.")

JUMPS = [("rules", "What a trainee may do"),
         ("placement", "Who finds your site"),
         ("table", "All 78 programs"),
         ("hours", "Hours your program wants"),
         ("supervision", "The supervision ratio"),
         ("bank", "What counts toward 3,000"),
         ("gap", "Degree to registration"),
         ("sources", "Sources")]

LABEL = {
    "guaranteed": "Guaranteed",
    "placed": "Program places you",
    "assisted": "Approved-site list",
    "student-sourced": "You find it",
    "not published": "Not published",
}

BLURB = {
    "guaranteed": "The program states every student gets a seat.",
    "placed": "The program assigns the site. You may be consulted; you are "
              "not doing the finding.",
    "assisted": "A list of sites the school has already contracted with. You "
                "apply and interview, but you are choosing from a shelf that "
                "already exists.",
    "student-sourced": "Finding the site is your job. The school approves it "
                       "afterward &mdash; and by statute has to hold a "
                       "written agreement with it.",
    "not published": "Nothing on the public site, catalog or fieldwork "
                     "handbook says. This describes the disclosure, not the "
                     "practice: some of these place students well. You "
                     "cannot tell before you enroll, which is the finding.",
}

C = pd.COUNTS
SOURCED = C["student-sourced"]
SILENT = C["not published"]
KNOWN = pd.N - SILENT


def link(r):
    if r["page"]:
        return '<a href="%s">%s</a>' % (r["page"], pk.esc(r["inst"]))
    return pk.esc(r["inst"])


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "The practicum year &middot; %d California programs &middot; read %s"
        % (pd.N, pd.CHECKED),
        "Your practicum is the part of the degree your program controls "
        "least &mdash; and %d of %d will not tell you how it works." % (SILENT, pd.N),
        "What a trainee may legally do, who is responsible for finding your "
        "site, how many client hours each program wants before it will "
        "graduate you, and which of those hours the Board will still be "
        "counting three years later.",
        [("%d" % SILENT, "programs publish nothing"),
         ("%d" % SOURCED, "say you find the site"),
         ("%d" % pd.OWN_CLINIC, "have their own clinic"),
         ("1,300", "hours you can bank early")],
        JUMPS))

    # ----------------------------------------------------------------- rules
    o.append('<section class="pk-sec" id="rules">')
    o.append(pk.quote(
        "The sentence that catches people out",
        ["&ldquo;A trainee shall not perform services in a private practice "
         "or a professional corporation.&rdquo;",
         "That is section 4980.43.3(b)(1), and it is absolute. Not as an "
         "employee, not as a volunteer, not with a willing licensed "
         "supervisor who has room and would be glad to have you. An "
         "<em>associate</em> may work in a private practice once the Board "
         "has issued the registration. A trainee never can. People arrange "
         "the placement first and read this second."]))

    o.append('<p class="pk-k">What a trainee may do</p>')
    o.append('<h2 class="pk-h">Seven rules, and where each one lives.</h2>')
    o.append('<p class="pk-d">These are the ones that decide whether a '
             "placement is usable. They sit in four different sections of the "
             "Business and Professions Code, which is most of the reason "
             "hardly anyone has read all of them.</p>")

    o.append(pk.numbered([
        ("1", "Not in a private practice, and not in a professional corporation.",
         'The setting has to be something that is neither &mdash; and that '
         '&ldquo;lawfully and regularly provides mental health counseling or '
         'psychotherapy&rdquo; and provides oversight of your work. '
         '<a href="%s" rel="nofollow noopener" target="_blank">'
         "&sect;&thinsp;4980.43.3(b)</a>. Agencies, clinics, schools, county "
         "programs and nonprofits qualify; the solo practice down the road "
         "does not, however good the supervisor." % (LEG % "4980.43.3")),
        ("2", "An employee or a volunteer. Never an independent contractor.",
         "&ldquo;A trainee, associate, or applicant for licensure shall only "
         "perform mental health and related services as an employee or "
         "volunteer, and not as an independent contractor.&rdquo; The hour "
         "and supervision rules apply identically either way, so a 1099 does "
         "not buy anybody flexibility &mdash; it just makes the hours "
         "uncountable. &sect;&thinsp;4980.43.3(a)."),
        ("3", "No money from a client, ever.",
         "You may be paid only by your employer. You may not take a fee, a "
         "co-pay or a gift from the person you are seeing, and you may not "
         "have any proprietary interest in the employer&rsquo;s business, "
         "lease or rent space from it, or pay for its furnishings, equipment "
         "or supplies. &sect;&thinsp;4980.43.3(e) and (f). The second half of "
         "that is what rules out the arrangement where a trainee &ldquo;rents "
         "a room&rdquo; from a practice."),
        ("4", "Not before 12 semester or 18 quarter units.",
         'No hour of experience counts if it was gained before you finished '
         'them. <a href="%s" rel="nofollow noopener" target="_blank">'
         "&sect;&thinsp;4980.43(c)(6)</a>. This is why practicum sits in year "
         "two of nearly every program on the list below." % (LEG % "4980.43")),
        ("5", "Enrolled in a practicum course while you are seeing clients.",
         "With one exception, and it is worth knowing precisely: you may keep "
         "counseling clients through a gap in enrollment of "
         "<b>fewer than 90 calendar days</b>, if that gap is immediately "
         "preceded by a practicum course and immediately followed by another "
         "one or by finishing the degree. &sect;&thinsp;4980.42(c). That is "
         "the rule that lets a summer work."),
        ("6", "Your school must approve the site and hold a written agreement "
              "with it.",
         "&ldquo;The school shall approve each site and shall have a written "
         "agreement with each site that details each party&rsquo;s "
         "responsibilities, including the methods by which supervision shall "
         "be provided.&rdquo; It must also provide for regular progress "
         "reports and evaluations. "
         '<a href="%s" rel="nofollow noopener" target="_blank">'
         "&sect;&thinsp;4980.42(e)</a>. Read that next to the table below: "
         "even where <b>you</b> find the site, the agreement is the "
         "<b>school&rsquo;s</b> obligation." % (LEG % "4980.42")),
        ("7", "Not supervised by a spouse, a relative or a domestic partner.",
         "Nor by anyone with whom you have a personal, professional or "
         "business relationship that undermines the authority or "
         "effectiveness of the supervision. &sect;&thinsp;4980.43.3(d). The "
         "second clause is broader than people assume and it is the Board "
         "that decides, after the fact."),
    ]))

    o.append(pk.callout(
        "The one that costs the most to learn late",
        ["If you gained hours at a school other than the one that confers "
         "your degree, <b>you</b> carry the burden of proving to the Board "
         "that they were gained in compliance &mdash; not the school. "
         "&sect;&thinsp;4980.42(e), last sentence.",
         "Which is a reason to keep your own copies of the site agreement, "
         "the supervision log and the weekly hour sheets from the first week "
         "rather than the last. The Board is reading them up to six years "
         'later, and <a href="%s">what happens when a signature cannot be '
         "produced</a> is a matter of public record."
         % "therapist-discipline-cases-california.html"]))
    o.append("</section>")

    # ------------------------------------------------------------- placement
    o.append('<section class="pk-sec" id="placement">')
    o.append('<p class="pk-k">Who finds your site</p>')
    o.append('<h2 class="pk-h">%d of %d publish nothing about it at all.</h2>'
             % (SILENT, pd.N))
    o.append('<p class="pk-d">Every one of the %d programs on this site was '
             "read for a single question: when practicum comes, whose job is "
             "it to find the seat? Five answers were possible. This is how "
             "they fell.</p>" % pd.N)

    rows = []
    for k in pd.ORDER:
        rows.append([("<b>%s</b>" % LABEL[k]), (str(C[k]), "f"),
                     ("%.0f%%" % (100.0 * C[k] / pd.N), "m"), BLURB[k]])
    o.append(pk.table(
        ["What the program says", "Programs", "Share", "What it means for you"],
        rows,
        caption="Where a program runs two stages &mdash; an in-house clinic "
                "first, an external traineeship second &mdash; it is "
                "classified on the stage that carries the risk, because that "
                "is the one that can go wrong. The notes explaining those "
                "calls are printed with the programs below.",
        minw=680))

    o.append('<p class="pk-p">Read the first row and the last row together. '
             "<b>%d programs</b> tell you plainly that finding the site is "
             "your job, which is hard but honest. <b>%d</b> say nothing "
             "either way &mdash; and a prospective student comparing two "
             "schools cannot tell which kind of year they are buying. That "
             "is not the same as a bad program. It is a gap in disclosure "
             "about the highest-variance part of the degree.</p>"
             % (SOURCED, SILENT))

    why = [r for r in pd.PROGRAMS if r["why"]]
    if why:
        o.append('<p class="pk-k">The close calls</p>')
        o.append('<h3 class="pk-h3">%d needed a judgment, and here it is.</h3>'
                 % len(why))
        o.append('<div class="pk-src"><ol>')
        for r in why:
            o.append("<li><b>%s</b> &mdash; %s <i>%s</i></li>"
                     % (pk.esc(r["inst"]), LABEL[r["placement"]].lower(),
                        pk.esc(r["why"])))
        o.append("</ol></div>")

    o.append(pk.callout(
        "%d of the %d run a clinic of their own" % (pd.OWN_CLINIC, pd.N),
        ["An in-house training clinic changes the shape of the year: the "
         "first hours happen in a building the program controls, with "
         "supervision it employs, and the placement question moves to the "
         "second stage rather than the first. It is the single most useful "
         "thing to ask about on a campus visit, and it is marked for every "
         "program in the table below.",
         "It is not automatically better. A clinic seat is often part time "
         "and the caseload is whatever walks in, so a student who needs "
         "relational hours &mdash; the couples-and-families hours the Board "
         "requires 500 of &mdash; can find them harder to get there than at "
         "an agency."],
        big="%d / %d" % (pd.OWN_CLINIC, pd.N)))
    o.append("</section>")

    # ----------------------------------------------------------------- table
    o.append('<section class="pk-sec" id="table">')
    o.append('<p class="pk-k">All %d programs</p>' % pd.N)
    o.append('<h2 class="pk-h">Ordered by how much of the finding falls on '
             "you.</h2>")
    o.append('<p class="pk-d">Not published first, then student-sourced, then '
             "the ones that get progressively more administered. The quoted "
             "column is the program&rsquo;s own wording, not a "
             "characterization of it &mdash; where the cell is empty, nothing "
             "public said anything.</p>")

    rows = []
    for r in pd.PROGRAMS:
        ev = pk.esc(r["evidence"]) if r["evidence"] else None
        rows.append([link(r), ("<b>%s</b>" % LABEL[r["placement"]], "m"),
                     ("Yes" if r["own_clinic"] else "&mdash;", "m"),
                     ("%d h" % r["dcc"] if r["dcc"] else "&mdash;", "f"),
                     "&ldquo;%s&rdquo;" % ev if ev else "&mdash;"])
    o.append(pk.table(
        ["Program", "Who finds the site", "Own clinic", "Client hours",
         "In the program's own words"],
        rows,
        caption="Read %s from each program&rsquo;s public fieldwork page, "
                "handbook or catalog. Wording changes; the linked program "
                "page carries the source for each one. A program named here "
                "is a program with a published page on this site or a record "
                "in the research file behind "
                "<a href=\"%s\">the program comparison</a>. "
                "&ldquo;Client hours&rdquo; is the direct-client-contact "
                "minimum the program states for graduation, curated by hand "
                "&mdash; the full wording behind each one is on that "
                "program&rsquo;s own page."
                % (pd.CHECKED, PROGRAMS),
        minw=900))
    o.append("</section>")

    # ----------------------------------------------------------------- hours
    o.append('<section class="pk-sec" id="hours">')
    o.append('<p class="pk-k">Hours your program wants</p>')
    o.append('<h2 class="pk-h">Half the published minimums sit exactly on a '
             "number the state wrote.</h2>")
    o.append('<p class="pk-d">%d of the %d state a direct-client-contact '
             "minimum you must reach before they will graduate you. They "
             "range from %d to %d &mdash; and the two commonest values are "
             "not arbitrary.</p>"
             % (pd.DCC_N, pd.N, pd.DCC_MIN, pd.DCC_MAX))

    rows = []
    for h, n in sorted(pd.DCC_BUCKETS):
        note = ""
        if h == 225:
            note = ("The LMFT statutory floor: 150 face-to-face hours plus 75 "
                    "of either client-centered advocacy or more counseling. "
                    "&sect;&thinsp;4980.36(d)(1)(B)")
        elif h == 280:
            note = ("The LPCC statutory floor: 280 hours of face-to-face "
                    "supervised clinical experience. &sect;&thinsp;4999.33(c)(3)")
        elif h == 150:
            note = "The face-to-face component of the LMFT floor, on its own"
        rows.append([("%d hours" % h, "f"), (str(n), "m"), note or "&mdash;"])
    o.append(pk.table(
        ["Direct client contact required", "Programs", "Why that number"],
        rows,
        caption="Curated by hand from each program&rsquo;s own wording rather "
                "than parsed, because the wording mixes counseling hours with "
                "supervision and observation hours and a pattern match gets "
                "roughly two thirds of them right &mdash; which is worse than "
                "not printing a number. %d programs state a total that is not "
                "a direct-client-contact figure; their exact words are in the "
                "table above." % (pd.N - pd.DCC_N),
        minw=620))

    o.append('<p class="pk-p">A program asking for <b>280</b> rather than '
             "<b>225</b> is usually not asking more of you for its own sake. "
             "It is holding the door open to the LPCC license as well as the "
             "LMFT, and the counselor statute wants 280. %d of the %d here "
             "advertise both. If you are certain you only want the LMFT, the "
             "extra 55 hours are still real hours in a real chair &mdash; "
             "they are simply not being asked for by the MFT statute.</p>"
             % (sum(1 for r in pd.PROGRAMS if r["lpcc"]), pd.N))
    o.append("</section>")

    # ----------------------------------------------------------- supervision
    o.append('<section class="pk-sec" id="supervision">')
    o.append('<p class="pk-k">The supervision ratio</p>')
    o.append('<h2 class="pk-h">A trainee is supervised twice as intensively '
             "as an associate.</h2>")
    o.append('<p class="pk-d">Section 4980.43.2 sets the floor, and the '
             "trainee line is the strictest number in the whole chapter. If "
             "your site cannot meet it, the hours do not count &mdash; which "
             "is a question worth asking a site before you accept a seat, not "
             "after.</p>")

    o.append(pk.table(
        ["Requirement", "Trainee", "Registered associate"],
        [["Direct supervisor contact, per setting, per week",
          ("1 hour", "f"), ("1 hour", "f")],
         (["<b>Extra supervision tied to caseload</b>",
           "<b>1 more hour for every 5 hours of direct clinical counseling "
           "that week</b>",
           "1 more hour if more than 10 hours of direct clinical counseling "
           "that week"], "hi"),
         ["Maximum supervision credited in any one week",
          ("6 hours", "f"), ("6 hours", "f")],
         ["Must fall in the same week as the hours claimed", "Yes", "Yes"],
         ["Individual or triadic, rather than group",
          "&mdash;", "52 of the 104 weeks"],
         ["Group supervision counts as", "2 hours face to face, 8 people maximum",
          "2 hours face to face, 8 people maximum"]],
        caption="Face-to-face means in person or two-way real-time "
                "videoconferencing, or a combination. A supervisor has to "
                "assess in writing, within 60 days of starting, whether "
                "videoconferenced supervision is appropriate for you at all "
                "&mdash; and may not use it if the assessment says no. "
                "&sect;&thinsp;4980.43.2(d).",
        minw=680))

    o.append('<p class="pk-p">The practical reading of row two: at a site '
             "where you carry <b>ten</b> direct counseling hours a week, a "
             "trainee needs <b>two</b> hours of supervisor contact and an "
             "associate needs one. Sites that take both sometimes budget "
             "supervision at the associate rate. That is the site&rsquo;s "
             "error and your uncountable hours.</p>")
    o.append("</section>")

    # ------------------------------------------------------------------ bank
    o.append('<section class="pk-sec" id="bank">')
    o.append('<p class="pk-k">What counts toward 3,000</p>')
    o.append('<h2 class="pk-h">Only one of the three licenses lets your '
             "practicum count.</h2>")
    o.append('<p class="pk-d">This is the single largest difference between '
             "the MFT track and the other two, it is decided before you "
             "enroll, and almost nobody states it plainly.</p>")

    o.append(pk.table(
        ["License", "Hours required", "May any be earned before the degree?",
         "Where it says so"],
        [(["<b>LMFT</b>", ("3,000", "f"),
           "<b>Yes &mdash; up to 1,300</b>, of which no more than 750 may be "
           "counseling and direct supervisor contact",
           ("&sect;&thinsp;4980.43(c)(4), (5)", "m")], "hi"),
         ["<b>LPCC</b>", ("3,000", "f"),
          "No. The statute says &ldquo;3,000 postdegree hours&rdquo;",
          ("&sect;&thinsp;4999.46(c)(1)", "m")],
         ["<b>LCSW</b>", ("3,000", "f"),
          "No. The statute says &ldquo;post-master&rsquo;s degree supervised "
          "experience&rdquo;",
          ("&sect;&thinsp;4996.23(a)", "m")]],
        caption="All three also require the experience to span at least 104 "
                "weeks, so banking pre-degree hours shortens the hour count "
                "and not necessarily the calendar. What it buys is slack: "
                "1,300 fewer hours to find after graduation, in the period "
                "when you are also job hunting.",
        minw=720))

    o.append(pk.numbered([
        ("1,300", "the ceiling on pre-degree hours",
         "&sect;&thinsp;4980.43(c)(4). Everything you accrue as a trainee "
         "counts against it, including nonclinical time."),
        ("750", "the ceiling inside the ceiling",
         "Of those 1,300, no more than 750 may be counseling plus direct "
         "supervisor contact. &sect;&thinsp;4980.43(c)(5). So a program that "
         "wants 500 direct client contact hours is already two thirds of the "
         "way through your pre-degree counseling allowance before supervision "
         "is added."),
        ("500", "the hours that never expire",
         "Hours older than six years at the date the Board receives your "
         "license application do not count &mdash; <b>except</b> up to 500 "
         "hours of clinical experience gained in the required practicum, "
         "which are exempt. &sect;&thinsp;4980.43(c)(7). If life happens "
         "between the degree and the license, those are the ones that "
         "survive it."),
        ("40", "the weekly ceiling",
         "No more than 40 hours in any seven consecutive days, at any stage. "
         "&sect;&thinsp;4980.43(c)(2). A site offering to sign for more is "
         "offering you hours the Board will strike."),
    ]))

    o.append('<p class="pk-p">Once you are registered, the arithmetic of the '
             'remaining hours is <a href="%s">the 3,000-hour calculator</a>, '
             "and what the Board will and will not credit from out of state "
             'is <a href="%s">on the out-of-state page</a>.</p>'
             % (CALC, "associate-hours-telehealth-out-of-state.html"))
    o.append("</section>")

    # ------------------------------------------------------------------- gap
    o.append('<section class="pk-sec" id="gap">')
    o.append('<p class="pk-k">Degree to registration</p>')
    o.append('<h2 class="pk-h">Ninety days, and the clock starts at the '
             "degree award date.</h2>")
    o.append('<p class="pk-d">The gap between graduating and holding an '
             "associate registration is the one stretch of the path with no "
             "institution looking after you. Three things decide whether it "
             "costs you anything.</p>")

    o.append(pk.numbered([
        ("1", "The Board must <em>receive</em> your application within 90 days.",
         "Not postmark, not submit &mdash; receive, counted from the date the "
         "qualifying degree was granted. Do that and postdegree hours gained "
         "before the registration is issued still count, as long as the "
         "registration is subsequently granted. Miss it and every hour "
         "between the degree and the registration is gone. "
         "&sect;&thinsp;4980.43(b)(1)(A)."),
        ("2", "The workplace must have required Live Scan before you started.",
         "For anybody who completed graduate study on or after 1 January "
         "2020, those pre-registration hours only count if the workplace "
         "required completed Live Scan fingerprinting <em>before</em> you "
         "gained them, and you file a copy of the form with your license "
         "application. &sect;&thinsp;4980.43(b)(1)(B)."),
        ("3", "Still no private practice until the registration is issued.",
         "&sect;&thinsp;4980.43(b)(2) repeats the trainee rule for this "
         "window specifically. The 90-day grace period covers agency and "
         "clinic work; it does not open the private-practice door early."),
    ]))

    o.append(pk.callout(
        "What the wait actually is",
        ["The Board publishes how long it is taking to process each "
         "application type every quarter, and the numbers move a lot. "
         '<a href="%s">The processing-time page</a> tracks them, and '
         '<a href="%s">the fee page</a> covers what the application costs '
         "since the July 2026 reduction." % (TIMES, FEES),
         "The other half of this window is the job. Why agencies hire "
         'pre-licensed clinicians at all is <a href="%s">a billing rule</a> '
         "rather than an hour count, and what those first jobs pay is on "
         '<a href="%s">the associate pay page</a>. If a placement or a first '
         "post asks you to work unpaid, "
         '<a href="%s">the wage-claim page</a> sets out what the law says.'
         % (HIRED, PAY, UNPAID)]))
    o.append("</section>")

    # --------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The statute", [
            ("Business and Professions Code &sect;&thinsp;4980.42 &mdash; "
             "what a trainee may do, the 90-day enrollment gap, and the "
             "school&rsquo;s duty to approve each site", LEG % "4980.42"),
            ("&sect;&thinsp;4980.43 &mdash; the 3,000 hours, the 1,300 and "
             "750 pre-degree ceilings, the six-year rule and its 500-hour "
             "exemption", LEG % "4980.43"),
            ("&sect;&thinsp;4980.43.2 &mdash; supervision ratios, the 6-hour "
             "weekly cap and the videoconferencing assessment",
             LEG % "4980.43.2"),
            ("&sect;&thinsp;4980.43.3 &mdash; employee or volunteer only, no "
             "private practice for trainees, no payment from clients",
             LEG % "4980.43.3"),
            ("&sect;&thinsp;4980.36 &mdash; the degree, and the practicum "
             "floor of 150 face-to-face hours plus 75", LEG % "4980.36"),
            ("&sect;&thinsp;4999.33 &mdash; the LPCC degree, and its 280-hour "
             "practicum floor", LEG % "4999.33"),
            ("&sect;&thinsp;4999.46 &mdash; the LPCC&rsquo;s 3,000 postdegree "
             "hours", LEG % "4999.46"),
            ("&sect;&thinsp;4996.23 &mdash; the LCSW&rsquo;s 3,000 "
             "post-master&rsquo;s hours", LEG % "4996.23"),
        ]),
        ("The program data", [
            ("The %d California MFT programs compared, with the fieldwork "
             "page, handbook or catalog each placement description was read "
             "from" % pd.N,
             "https://therapistsupport.org/%s" % PROGRAMS),
            ("How to become an LMFT in California, end to end",
             "https://therapistsupport.org/%s" % BECOME),
        ]),
    ], note="Placement categories are a reading of what each program "
            "publishes, reduced by <b>_dev/practicum.py</b>. "
            "<b>&ldquo;Not published&rdquo; means nothing public said, not "
            "that the program does not help</b> &mdash; several of them "
            "place students well and simply do not write it down. "
            "Direct-client-contact figures are each program&rsquo;s own "
            "stated minimum for graduation, not a Board requirement, and the "
            "program&rsquo;s exact words are printed beside every one. "
            "Statutory text is quoted from the California Legislative "
            "Information site and was read %s; sections are amended, so check "
            "the current text before relying on any of it. Nothing here is "
            "legal advice, and the Board decides what it credits." % pd.CHECKED)
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "The practicum year in California: rules, hours and placement",
    "What a California trainee may legally do, which of the 78 MFT programs "
    "finds your practicum site and which leaves it to you, and which hours "
    "the Board will still be counting three years later.",
    "licensure", "reference",
    "How does the practicum work for a California MFT student?",
    "The seven trainee rules, all 78 programs compared on who finds your "
    "site, and the 1,300 hours only one of the three licenses lets you bank",
    "%d of %d programs publish nothing about placement" % (SILENT, pd.N),
    weight=4)


def main():
    print("the practicum year")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d programs, %d sources"
          % (PAGE, format(len(html), ",d"), pd.N, nsrc))

    bad = pk.check_page(p, [
        ("the no-private-practice rule", "shall not perform services in a "
                                         "private practice"),
        ("the not-published caveat", "describes the disclosure, not the"),
        ("the 1,300-hour ceiling", "up to 1,300"),
        ("the 750 sub-ceiling", "no more than 750"),
        ("the 90-day receipt rule", "within 90 days"),
        ("the curated-not-parsed note", "Curated by hand"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every program must appear. A school missing from a placement table reads
    # as "no information", which is not what "not published" means.
    for r in pd.PROGRAMS:
        if pk.esc(r["inst"]) not in art:
            print("GUARD: %s is missing from the table" % r["inst"])
            bad += 1

    # The five counts must add to the total, and each must be printed.
    if sum(pd.COUNTS.values()) != pd.N:
        print("GUARD: the placement counts do not add to %d" % pd.N)
        bad += 1

    # The no-private-practice rule has to be read before the placement table,
    # because a reader who meets the table first goes looking for a supervisor.
    i_rule = art.find("shall not perform services in a private practice")
    i_table = art.find('id="table"')
    if i_rule < 0 or i_table < 0 or i_rule > i_table:
        print("GUARD: the private-practice rule is not above the program table")
        bad += 1

    # The three-license comparison is the reason the page exists for anybody
    # choosing a track. Losing it silently would be easy.
    for needle in ("4999.46(c)(1)", "4996.23(a)", "4980.43(c)(4)"):
        if needle not in art:
            print("GUARD: %s is not cited" % needle)
            bad += 1

    for w in pk.spelling(s):
        print("GUARD: British spelling %r" % w)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
