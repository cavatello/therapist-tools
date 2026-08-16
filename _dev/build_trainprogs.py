#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 item three, first cut: the Bay Area published training programs.

The practicum-sites directory lists the universe of settings; this page
answers the follow-up question - which of the large Bay clinical agencies
PUBLISH a clinical training program, and on what terms. Ten do, and every
fact below was read from the organization's own site on 16 August 2026,
with the page it came from linked beside it (research banked in the
project doc claude/bay-org-profiles-research.md; every URL was fetched
during that read). Programs whose sites publish nothing are named too,
because the absence is information.

AVAILABILITY LANGUAGE IS BANNED here exactly as on the directories: this
page reports that a program PAGE EXISTS and what it SAYS, never that an
org has openings. The one org whose site announces a pause (Family Paths)
carries that flag verbatim.

BUILD MECHANISM: build_findsite.py's - chrome from the fees page, own
ts:meta, artband family keeps it converted.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = "training-programs-bay-area.html"
TEMPLATE = "bbs-fees-california-2026.html"

TITLE = "Bay Area agencies with published clinical training programs"
DESC = ("The ten large Bay Area clinical agencies whose own sites publish "
        "a trainee or associate program, with the stipends and supervision "
        "hours each one states in writing.")
CANON = "https://therapistsupport.org/" + OUT

TSMETA = """<!-- ts:meta -->
<meta name="ts:topic" content="licensure">
<meta name="ts:format" content="reference">
<meta name="ts:question" content="Which Bay Area agencies publish a clinical training program?">
<meta name="ts:outcome" content="Ten agencies with a published trainee or associate program, the terms each one states, and the page every fact came from">
<meta name="ts:number" content="10 of 24 large Bay clinical agencies publish a program">
<meta name="ts:weight" content="3">
<!-- /ts:meta -->"""

# (org, program page label+url, what the site says - quotes kept short)
PROGRAMS = [
 ("Momentum for Health", "San Jose / Santa Clara County",
  "https://momentumforhealth.org/internships/",
  "Its internships page offers &ldquo;both mentored practicum and field "
  "placement opportunities&rdquo; across outpatient, residential and "
  "partial-hospitalization settings, at about 16&ndash;24 hours a week and "
  "described as paid; the careers page adds &ldquo;we offer hours toward "
  "licensure and clinical supervision in a community behavioral health "
  "nonprofit setting.&rdquo; A 550-person staff working in 44 languages."),
 ("WestCoast Children's Clinic", "Oakland / East Bay",
  "https://www.westcoastcc.org/internships",
  "An 8-month clinical training program for incoming second-year MSW or "
  "MFT students, compensated, running September to April with a week-long "
  "August orientation; partner schools named include CSU East Bay, Palo "
  "Alto University, SFSU, Smith, Saint Mary&rsquo;s and UC Berkeley. Its "
  "doctoral assessment practicum states two hours of individual and 1.5 "
  "hours of group supervision a week, with a $3,500 annual stipend."),
 ("RAMS (Richmond Area Multi-Services)", "San Francisco",
  "https://ramsinc.org/programs/rams-training-institute/",
  "The RAMS Training Institute runs &ldquo;Social Work, MFT and PCC "
  "Practicums&rdquo; described as systems-oriented community mental health "
  "placements, an outpatient clinical practicum, and the National Asian "
  "American Psychology Training Center doctoral internship, established "
  "1979. Care delivered in 30+ languages across 130+ sites."),
 ("Lincoln Families", "Oakland / Alameda &amp; Contra Costa",
  "https://lincolnfamilies.org/clinicians-training-program",
  "A practicum for clinical/counseling psychology, MFT and social work "
  "students: one hour a week of individual supervision, two hours a week "
  "of group case conference, two hours of didactics &mdash; and "
  "educational reimbursements the page states as $4,000 for first-year "
  "and $2,000 for later-year graduate students."),
 ("One Life Counseling Center", "San Carlos / San Mateo County",
  "https://www.onelifecounselingcenter.org/work-with-us",
  "&ldquo;Tailored trainee and associate positions&rdquo; for counseling "
  "psychology, MFT and LPCC students; the page describes paid roles "
  "(&ldquo;earn competitive pay while gaining the hours&rdquo;), six "
  "active supervision groups, a community of over 70 licensed therapists, "
  "and explicit Spanish-language capacity."),
 ("Caminar / Family &amp; Children Services", "San Jose &amp; Peninsula",
  "https://www.caminar.org/careers",
  "A school-based practicum description linked from its careers page "
  "offers &ldquo;group and individual supervision and extensive "
  "training&rdquo; for interns and trainees pursuing BBS licensure, with "
  "20 to 40 hours of paid clinical work per week in San Jose-area school "
  "and community settings."),
 ("Side by Side", "Marin, Alameda, Sonoma &amp; Napa",
  "https://www.sidebysideyouth.org/careers-and-internships/",
  "Community counseling internships stating one hour of clinical "
  "supervision and two hours of group supervision per week, plus training "
  "opportunities within the agency. Serves ages 5&ndash;26 and families."),
 ("Crisis Support Services of Alameda County", "Oakland",
  "https://www.crisissupport.org/join-our-team",
  "&ldquo;Our interns are graduate and doctoral students who have "
  "progressed far enough through their degree programs to start obtaining "
  "hours for licensure&rdquo; &mdash; training areas named include child "
  "psychology, grief, crisis counseling and geriatric mental health. The "
  "same page recruits licensed clinicians to supervise its trainees and "
  "associates."),
 ("East Bay Agency for Children", "Oakland / Alameda County",
  "https://ebac.org/careers/careers.asp",
  "Practicum placements for master&rsquo;s-level social work students, "
  "focused on grief and loss: support groups, grief education and "
  "short-term grief therapy for children, alongside placements for "
  "graduate and undergraduate students."),
 ("Family Paths", "Oakland / Alameda County",
  "https://www.familypaths.org/volunteer",
  "A clinical program for second-year graduate students and registered "
  "interns &mdash; the page states an annual stipend of $2,500 for "
  "trainees and $3,000 for registered interns, weekly individual and "
  "group supervision, and supervision available in Spanish. <b>Read the "
  "page&rsquo;s own flag first:</b> &ldquo;Due to some planned "
  "reorganization in 2026, the agency will be pausing our Clinical Intern "
  "Program at the end of August 2026.&rdquo;"),
]

NONE_PUBLISHED = ("Progress Foundation, Edgewood Center, PRC (Baker Places), "
                  "Buckelew Programs, Westside Community Mental Health "
                  "Center, JFCS East Bay, Peninsula Healthcare Connection, "
                  "Fred Finch (its Training Institute is continuing "
                  "education for licensed providers, not a licensure "
                  "track) and John Muir Behavioral Health")

ARTICLE_HEAD = """<article class="art"><section class="artband"><div class="in"><div><ol class="bcr" aria-label="Breadcrumb"><li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li><li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li><li><span aria-current="page">Licensure</span></li></ol><p class="kick">Bay Area &middot; published training programs</p><h1>The Bay agencies that put their <em>training program in writing</em></h1><p class="dek">Of the 24 largest Bay Area clinical nonprofits, ten publish a real clinical training program on their own site &mdash; who it is for, how much supervision it carries, and in four cases what it pays. This page holds each program to its own words: every fact below is quoted or closely paraphrased from the page linked beside it, read on 16 August 2026. It is a list of published programs, not of openings &mdash; no such register exists.</p><div class="artmeta"><span>Licensure</span><span>9 min read</span></div><!-- _dev/pixel_concepts.py --><div class="tsshort"><p class="tsk">In short</p><q>Which Bay Area agencies publish a clinical training program?</q><p class="tsa">Ten of the 24 largest &mdash; with supervision structures in writing at seven, stipends or pay stated at five, and one announcing a pause on its own page</p><span class="tsfig">10 of 24 &middot; read 16 Aug 2026</span></div><!-- /pixel_concepts --></div><div class="artfig"><b>10 of 24</b><span>large Bay clinical agencies publish a trainee or associate program on their own site. The other 14 may train too &mdash; they just do not say so publicly.</span></div></div></section><div class="artwrap"><nav class="artnav"><b>On this page</b><a href="#how-to-read-this"><i class="tsn">1</i>How to read this page</a><a href="#the-ten"><i class="tsn">2</i>The ten published programs</a><a href="#nothing-published"><i class="tsn">3</i>The agencies that publish nothing</a></nav><div class="artbody">
<h2 id="how-to-read-this">How to read this page</h2>
<p>A published program page is a signal, not a seat. It tells you the agency has a structure for trainees &mdash; named supervision hours, a contact, sometimes a stipend &mdash; and that it expects applications. It does not tell you whether this year&rsquo;s cohort is full, and this page never claims to. Treat each entry as an address to write to, hold it against the six questions on <a href="how-to-find-a-practicum-site-california.html">the search method page</a>, and remember the statutory floor from <a href="practicum-california-mft-trainee.html">the trainee rules</a>: one hour of individual supervisor contact per week per setting, plus one more per five hours of direct clinical work.</p>
<h2 id="the-ten">The ten published programs</h2>"""

ARTICLE_TAIL = """<h2 id="nothing-published">The agencies that publish nothing</h2>
<p>The remaining large agencies from the same 24 &mdash; %s &mdash; had no clinical training or practicum page anywhere their public sites reach at the August 2026 read. That is a statement about disclosure, not about whether they train: several certainly do. It simply means your first contact there is a cold ask to the clinical director rather than an application to a published program. Two adjacent notes for honesty&rsquo;s sake: the <b>Contra Costa Crisis Center</b> publishes a 54-hour volunteer crisis-line training that is not a clinical licensure track, and <b>Trans Lifeline</b> says clinical-hours credit for its volunteer operators &ldquo;may be possible&rdquo; depending on your program &mdash; case by case, through its volunteer manager.</p>
<div class="arttool"><b>The rest of the universe</b><p>These ten sit inside a much larger map &mdash; every program clinic, county plan, health center and clinical nonprofit in the nine Bay counties, laid out by name.</p><a href="practicum-sites-bay-area.html">Open the practicum-sites directory &rarr;</a></div>
<div class="artsrc"><h2>Sources</h2><p class="disc">Every program description above is quoted or closely paraphrased from the organization page linked in its own entry, all read on 16 August 2026. Program pages move without notice &mdash; the linked page is the authority, not this summary. The 24-agency universe is the revenue-ranked Bay clinical set from the IRS Exempt Organizations Business Master File, documented on <a href="practicum-sites-bay-area.html">the practicum-sites directory</a>. This is not an endorsement of any program.</p></div>
<div class="artnext"><b>Read next</b><div class="g"><a href="how-to-find-a-practicum-site-california.html"><i>Licensure</i><strong>The search, run in the right order &mdash; and what to ask before you accept.</strong></a><a href="east-bay-practicum-site-directory.html"><i>Licensure</i><strong>EB CAMFT&rsquo;s own 2026&ndash;27 practicum site directory, read closely.</strong></a></div></div></div></div></article>""" % NONE_PUBLISHED

BANNED = ("is hiring", "has openings", "takes trainees", "accepting trainees",
          "currently accepting", "spots available", "positions open")


def entries():
    o = []
    for i, (org, where, url, body) in enumerate(PROGRAMS, 1):
        o.append('<h3 id="p%d">%d &middot; %s <small>&mdash; %s</small></h3>'
                 % (i, i, org, where))
        o.append("<p>%s</p>" % body)
        o.append('<p><i><a href="%s" target="_blank" '
                 'rel="noopener noreferrer">The program page this was read '
                 "from &rarr;</a></i></p>" % url)
    return "\n".join(o)


def main():
    tpl = open(os.path.join(SITE, TEMPLATE), encoding="utf-8").read()
    s = tpl
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, s,
               count=1, flags=re.S)
    for pat, val in [
        (r'(<meta name="description" content=")[^"]*(")', DESC),
        (r'(<link rel="canonical" href=")[^"]*(")', CANON),
        (r'(<meta property="og:url" content=")[^"]*(")', CANON),
        (r'(<meta property="og:title" content=")[^"]*(")', TITLE),
        (r'(<meta property="og:description" content=")[^"]*(")', DESC),
    ]:
        s = re.sub(pat, r"\g<1>%s\g<2>" % val, s, count=1)
    m = re.search(r"<!-- ts:meta -->.*?<!-- /ts:meta -->", s, re.S)
    if not m:
        sys.exit("template has no ts:meta block")
    s = s[:m.start()] + TSMETA + s[m.end():]
    art_ld = ('{"@context":"https://schema.org","@type":"Article",'
              '"headline":"%s","description":"%s","url":"%s",'
              '"datePublished":"2026-08-16","dateModified":"2026-08-16",'
              '"author":{"@type":"Organization","name":"Therapist Support"},'
              '"publisher":{"@type":"Organization","name":"Therapist Support",'
              '"url":"https://therapistsupport.org/"}}'
              % (TITLE, DESC, CANON))
    bcr_ld = ('{"@context":"https://schema.org","@type":"BreadcrumbList",'
              '"itemListElement":[{"@type":"ListItem","position":1,'
              '"name":"Therapist Support","item":"https://therapistsupport.org/"},'
              '{"@type":"ListItem","position":2,"name":"Resources",'
              '"item":"https://therapistsupport.org/resources.html"},'
              '{"@type":"ListItem","position":3,"name":"Licensure"}]}')
    lds = list(re.finditer(
        r'<script type="application/ld\+json">.*?</script>', s, re.S))
    if len(lds) < 2:
        sys.exit("template carries %d JSON-LD blocks" % len(lds))
    s = (s[:lds[0].start()]
         + '<script type="application/ld+json">%s</script>' % art_ld
         + s[lds[0].end():lds[1].start()]
         + '<script type="application/ld+json">%s</script>' % bcr_ld
         + s[lds[1].end():])
    m = re.search(r'<article class="art">.*?</article>', s, re.S)
    if not m:
        sys.exit("template has no article")
    s = s[:m.start()] + ARTICLE_HEAD + entries() + ARTICLE_TAIL + s[m.end():]
    m = re.search(r'<!-- _dev/pixel_concepts\.py --><div class="tsfoot">'
                  r'.*?<!-- /pixel_concepts -->', s, re.S)
    if not m:
        sys.exit("template has no tsfoot")
    TSFOOT = ('<!-- _dev/pixel_concepts.py --><div class="tsfoot">'
              '<div class="tsmeta"><div class="tsrow"><span class="tsk">Last '
              'checked</span><span class="tsv">16 August 2026</span>'
              '<a class="tsall" href="changes.html">All updates &rarr;</a>'
              '</div><div class="tsvint"><span class="tsk">Figures current '
              'as of</span><b>each organization&rsquo;s own program page at '
              'the dated read</b><i>Program pages move without notice; the '
              'linked page is the authority.</i></div><div class="tsdepth">'
              '<a class="tsbadge thin" href="about.html#how-pages-are-checked">'
              'Published sources only</a><p class="tswhat">Built from what '
              'each organization publishes about itself. Nothing here is '
              'independently verified.</p></div></div></div>'
              '<!-- /pixel_concepts -->')
    s = s[:m.start()] + TSFOOT + s[m.end():]

    bad = []
    low = re.sub(r"<[^>]+>", " ", s).lower()
    for p in BANNED:
        if p in low:
            bad.append("availability language: %r" % p)
    for f in ("how-to-find-a-practicum-site-california.html",
              "practicum-california-mft-trainee.html",
              "practicum-sites-bay-area.html",
              "east-bay-practicum-site-directory.html"):
        if 'href="%s"' % f not in s:
            bad.append("internal link to %s missing" % f)
        if not os.path.exists(os.path.join(SITE, f)):
            bad.append("link target %s not on disk" % f)
    if "pausing our Clinical Intern Program" not in s:
        bad.append("the Family Paths pause flag is missing")
    if len(re.findall(r'target="_blank"', s)) < 10:
        bad.append("fewer than 10 program links")
    if not 15 <= len(TITLE) <= 68:
        bad.append("title length %d" % len(TITLE))
    dl = len(re.sub(r"&[a-z]+;", "-", DESC))
    if not 70 <= dl <= 168:
        bad.append("description length %d" % dl)
    if s.count("<h1") != 1:
        bad.append("%d h1s" % s.count("<h1"))
    for a in re.findall(r'href="#([a-z-]+)"',
                        re.search(r'<nav class="artnav">.*?</nav>',
                                  s, re.S).group(0)):
        if 'id="%s"' % a not in s:
            bad.append("artnav anchor #%s unresolved" % a)
    if bad:
        for b in bad:
            print("GUARD %s: %s" % (OUT, b))
        sys.exit(1)
    open(os.path.join(SITE, OUT), "w", encoding="utf-8").write(s)
    print("build_trainprogs: %s written, guards clean" % OUT)


if __name__ == "__main__":
    main()
