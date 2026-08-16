#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The practicum-site method page - remaining P3, item two.

The directory (practicum-sites-bay-area.html) answers WHERE; the rules page
(practicum-california-mft-trainee.html) answers WHAT IS LEGAL. Neither
answers the question people actually arrive with, which is HOW: whose job
the search is, in what order to run it, and what to ask a site before
saying yes. This page is that method, and every load-bearing fact on it is
either quoted from a statute this site has already fetched from leginfo, or
re-stated from a figure already published and sourced on one of those two
pages (the 78-program placement survey, the supervision-ratio table, the
nonprofit universe counts from the IRS EO BMF via _dev/nonprofit_data.py).

NOTHING HERE IS NEW RESEARCH. That is deliberate: a method page invents no
facts, it sequences verified ones. The two facts most likely to rot - the
78-program split and the agency counts - are stated with their read dates
and linked to the pages that own them, so a refresh there is a refresh
here.

BUILD MECHANISM, same as build_ninety.py: chrome, head scripts and tail
scripts taken verbatim from bbs-fees-california-2026.html (converted
artband family), so the page is born in the house design and family_art.py
keeps it there. This builder's own: head metadata, the ts:meta block, the
<article>, the tsfoot provenance block.

Guards: the site-agreement quote, the independent-contractor sentence and
the private-practice exclusion present; all four leginfo links present; the
at-least-six-sites advice present; every internal link resolves to a file
on disk; no affirmative availability language; title 15-68; description
70-168; exactly one h1; every artnav anchor resolves.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = "how-to-find-a-practicum-site-california.html"
TEMPLATE = "bbs-fees-california-2026.html"

TITLE = "How to find a practicum site in California, and what to ask"
DESC = ("Whose job the search legally is, the settings a trainee can never "
        "use, where California practicum seats exist, and what to ask a "
        "site before you accept.")
CANON = "https://therapistsupport.org/" + OUT

TSMETA = """<!-- ts:meta -->
<meta name="ts:topic" content="licensure">
<meta name="ts:format" content="answer">
<meta name="ts:question" content="How do I actually find a practicum site?">
<meta name="ts:outcome" content="Where your program stands, the settings the law forbids, the four places seats actually exist, and the questions that protect your hours">
<meta name="ts:number" content="At least six applications, starting the term before your practicum">
<meta name="ts:weight" content="4">
<!-- /ts:meta -->"""

ARTICLE = """<article class="art"><section class="artband"><div class="in"><div><ol class="bcr" aria-label="Breadcrumb"><li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li><li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li><li><span aria-current="page">Licensure</span></li></ol><p class="kick">California &middot; the practicum search</p><h1>Finding your practicum site, when <em>nobody owns the finding</em></h1><p class="dek">You cannot see clients until you have a site &mdash; and at 29 of California&rsquo;s 78 MFT programs, nobody says whose job it is to find one. At 13 more, it is plainly yours. This page walks the search in order: what your program owes you by law, the settings that can never count, the four places seats actually exist, and the questions to ask before you say yes &mdash; so every hour you work counts toward your 3,000.</p><div class="artmeta"><span>Licensure</span><span>12 min read</span></div><!-- _dev/pixel_concepts.py --><div class="tsshort"><p class="tsk">In short</p><q>How do I actually find a practicum site?</q><p class="tsa">Ask your fieldwork office which placement model your program runs, cross off the settings the law forbids, then apply wide &mdash; at least six sites, starting the term before your practicum</p><span class="tsfig">6+ applications &middot; start the term before</span></div><!-- /pixel_concepts --></div><div class="artfig"><b>29 of 78</b><span>California MFT programs publish nothing about whose job the placement search is &mdash; you find out after you enroll.</span></div></div></section><div class="artwrap"><nav class="artnav"><b>On this page</b><a href="#whose-job-the-search-is"><i class="tsn">1</i>Whose job the search is &mdash; your program answers first</a><a href="#settings-the-law-rules-out"><i class="tsn">2</i>The settings the law rules out</a><a href="#where-the-seats-exist"><i class="tsn">3</i>Where the seats actually exist</a><a href="#running-the-search"><i class="tsn">4</i>Running the search</a><a href="#what-to-ask"><i class="tsn">5</i>What to ask before you accept a seat</a><a href="#the-paper-trail"><i class="tsn">6</i>The paper trail, from the first week</a></nav><div class="artbody">
<h2 id="whose-job-the-search-is">Whose job the search is &mdash; your program answers first</h2>
<p>Before any search starts, know what the law already assigns. Whoever does the finding, the approving is never yours:</p>
<div class="quote"><p>&ldquo;The school shall approve each site and shall have a written agreement with each site that details each party&rsquo;s responsibilities, including the methods by which supervision shall be provided.&rdquo;</p><cite>BPC &sect;4980.42(e) &mdash; see source [1]</cite></div>
<p>So a site you discover on your own is a <em>candidate</em>, not a placement, until your program has approved it and signed with it. That single sentence sets the method&rsquo;s first step: go to your fieldwork office before you go to any agency, and ask which of the five placement models your program actually runs. When <a href="practicum-california-mft-trainee.html">this site read all 78 California MFT programs</a> for that one question in August 2026, the answers fell like this: 3 programs guarantee a seat, 6 place you themselves, 27 hand you an approved-site list to apply against, 13 say plainly that finding the site is your job &mdash; and 29 publish nothing either way. If yours is one of the 29, the first phone call of your search is to your own program, because every later step depends on the answer.</p>
<p>One more program fact changes the search&rsquo;s shape: 33 of the 78 run a training clinic of their own. An in-house seat moves the search to the second stage rather than the first &mdash; but a clinic caseload is whatever walks in, and the <b>500 relational hours</b> the Board requires &mdash; couples and families, not individuals &mdash; can be harder to accumulate there than at a community agency. A clinic year that defers the search does not always defer it for free. Choosing between programs on exactly this axis is what <a href="mft-programs-california.html">the programs directory</a> is for.</p>
<h2 id="settings-the-law-rules-out">The settings the law rules out</h2>
<p>Run these five strikes against every candidate before you spend an application on it. They are statute, not preference, and no willing supervisor waives any of them.</p>
<figure class="ig ig-steps"><figcaption class="ig-cap">Five strikes &mdash; any one makes a site unusable for a trainee</figcaption><ol><li><b>A private practice, or a professional corporation</b><span>&ldquo;A trainee shall not perform services in a private practice or a professional corporation.&rdquo; Absolute &mdash; not as an employee, not as a volunteer, not with a supervisor who has room and would gladly have you. The setting must be one that lawfully and regularly provides mental health counseling or psychotherapy, with oversight of your work: agencies, clinics, schools, county programs, nonprofits. &sect;4980.43.3(b)<sup><a href="#s4">[4]</a></sup></span></li><li><b>Any seat offered on a 1099</b><span>&ldquo;A trainee, associate, or applicant for licensure shall only perform mental health and related services as an employee or volunteer, and not as an independent contractor.&rdquo; A site that offers contractor status is offering hours that will not count. &sect;4980.43.3(a)<sup><a href="#s4">[4]</a></sup></span></li><li><b>Any arrangement where money moves from client to you, or from you to the site</b><span>You may be paid only by the employer. No fees or gifts from clients &mdash; and no proprietary interest in the employer&rsquo;s business, no leasing or renting space from it, no paying for its furnishings, equipment or supplies. The &ldquo;rent a room at a practice&rdquo; arrangement fails here even before it fails strike one. &sect;4980.43.3(e), (f)<sup><a href="#s4">[4]</a></sup></span></li><li><b>A supervisor you are related or connected to</b><span>Not a spouse, relative or domestic partner &mdash; and not anyone with whom a personal, professional or business relationship undermines the supervision&rsquo;s authority or effectiveness. The second clause is broader than people assume, and the Board judges it after the fact. &sect;4980.43.3(d)<sup><a href="#s4">[4]</a></sup></span></li><li><b>Any start before you are eligible to start</b><span>No hour counts before 12 semester or 18 quarter units are complete (&sect;4980.43(c)(6)<sup><a href="#s2">[2]</a></sup>), and you must be enrolled in a practicum course while seeing clients &mdash; with one precise exception: a gap in enrollment of fewer than 90 days, sandwiched directly between practicum courses or ended by the degree itself. &sect;4980.42(c)<sup><a href="#s1">[1]</a></sup></span></li></ol></figure>
<p>Strike one deletes the placement most people imagine first &mdash; the solo practitioner down the road who would love the help. That door opens at associate registration, never during the degree. The full seven trainee rules, with the statutory text of each, are on <a href="practicum-california-mft-trainee.html">the practicum rules page</a>.</p>
<h2 id="where-the-seats-exist">Where the seats actually exist</h2>
<p>Cross out private practices and professional corporations, and what remains is four shelves. Every usable practicum seat in California sits on one of them.</p>
<div class="tw"><table class="tbl"><thead><tr><th>The shelf</th><th class="n">How many</th><th>What the seat is like</th></tr></thead><tbody><tr><td>Your program&rsquo;s own training clinic</td><td class="n">33 of 78 programs</td><td>The program controls the seat and employs the supervision. Often part-time, caseload is whatever walks in &mdash; watch the relational hours.</td></tr><tr><td>County behavioral health systems and their contractors</td><td class="n">58 counties</td><td>Public mental health at scale: high acuity, structured supervision, and the county&rsquo;s contractor network multiplies the doors.</td></tr><tr><td>Community health centers</td><td class="n">39 organizations with Bay Area sites alone</td><td>Federally supported primary-care organizations with behavioral health integrated &mdash; medical-adjacent work, often bilingual caseloads.</td></tr><tr><td>Nonprofit clinical agencies</td><td class="n">1,766 statewide</td><td>The deepest shelf by far: every California nonprofit whose IRS classification is clinical mental-health treatment, from storefront counseling centers to multi-county agencies.</td></tr></tbody></table></div>
<p>Those counts are the universe, not a vacancy list &mdash; no register of openings exists anywhere, which is precisely why the method below is &ldquo;apply wide,&rdquo; not &ldquo;apply to the right one.&rdquo; For the nine Bay Area counties, <a href="practicum-sites-bay-area.html">the practicum-sites directory</a> lays the whole universe out by name: 5 program training clinics, 9 county behavioral health plans, 39 health-center organizations and 318 nonprofit clinical agencies, each mapped from the federal data it was found in.</p>
<h2 id="running-the-search">Running the search</h2>
<p>The honest core of the method is a number published by a placement office rather than this site. The California Institute of Integral Studies &mdash; a program that owns <em>three</em> clinics of its own &mdash; tells its students that practicum placements are competitive and advises applying to <b>at least six sites</b>. If six is the floor at a school with three in-house clinics, it is not a pessimistic floor for anyone else.</p>
<div class="pull"><b>At least six</b><span>applications &mdash; the floor one program&rsquo;s own placement office advises, not a number this site invented.</span></div>
<p>Sequence it backward from your program&rsquo;s calendar. The seats are cohort-shaped: agencies bring trainees in against the academic year, so a search that begins the term your practicum course starts is late by definition. Work the prior term, in this order:</p>
<p><b>First, the fieldwork office</b> &mdash; the placement model, the approved-site list if one exists, and which agencies took students last year. Where the school holds an agreement already, your application is to the agency alone; where it does not, the school&rsquo;s willingness to sign one is part of what you are asking for &mdash; and the statute puts that agreement on the school, not on you<sup><a href="#s1">[1]</a></sup>.</p>
<p><b>Then the shelves, wide.</b> Six or more applications across at least two of the four shelves &mdash; a clinic seat and an agency seat are different years, and applying across both hedges the caseload question as well as the odds. Treat the directory pages as the map, and expect most inquiries to die silently; that is what the width is for.</p>
<p><b>Then the interview, run in both directions.</b> An agency interviewing you is also you interviewing the agency against the strikes above and the questions below &mdash; asked before you accept, because every one of them is cheap to ask in an interview and expensive to discover in an audit.</p>
<h2 id="what-to-ask">What to ask before you accept a seat</h2>
<p>Six questions. Each is pinned to a rule that decides whether the seat&rsquo;s hours count, and a site that answers them impatiently is answering a seventh question you did not ask.</p>
<figure class="ig ig-steps"><figcaption class="ig-cap">Six questions, each pinned to the rule that makes it matter</figcaption><ol><li><b>&ldquo;Am I an employee or a volunteer here &mdash; and can I see that in writing?&rdquo;</b><span>Either status works; an independent-contractor arrangement makes every hour uncountable. &sect;4980.43.3(a)<sup><a href="#s4">[4]</a></sup></span></li><li><b>&ldquo;Who is my supervisor, and how many supervision hours a week can this site actually staff?&rdquo;</b><span>The trainee floor is the strictest in the chapter: one hour of direct supervisor contact per week per setting, plus another hour for every five hours of direct clinical counseling that week. A site that cannot staff the ratio produces hours that do not count. &sect;4980.43.2<sup><a href="#s3">[3]</a></sup></span></li><li><b>&ldquo;Has this site signed a written agreement with my school before &mdash; and if not, will it?&rdquo;</b><span>No agreement, no placement, whatever else is agreed verbally. The agreement must detail each party&rsquo;s responsibilities including how supervision is provided. &sect;4980.42(e)<sup><a href="#s1">[1]</a></sup></span></li><li><b>&ldquo;What does the caseload actually look like &mdash; and will I see couples and families?&rdquo;</b><span>The Board requires 500 relational hours across the licensure path. A site with an individuals-only caseload leaves them unearned, and clinic caseloads especially are whatever walks in.</span></li><li><b>&ldquo;How does money move here?&rdquo;</b><span>Only from employer to you, ever. Any arrangement where a client pays you, or where you pay the site &mdash; rent, supplies, a &ldquo;materials fee&rdquo; &mdash; is disqualifying on its face. &sect;4980.43.3(e), (f)<sup><a href="#s4">[4]</a></sup></span></li><li><b>&ldquo;Who signs my weekly logs, and how quickly?&rdquo;</b><span>Not a statute &mdash; a tell. The paperwork below is your burden to keep, and a site that is casual about signatures in the interview will be casual about them in week thirty.</span></li></ol></figure>
<h2 id="the-paper-trail">The paper trail, from the first week</h2>
<p>Two facts make the file you keep worth more than the file anyone keeps for you. First, if your hours were gained at a school other than the one that confers your degree, the statute puts the burden of proving they were compliant on <em>you</em>, not the school<sup><a href="#s1">[1]</a></sup>. Second, the Board reads this paperwork years after the fact, when supervisors have moved on and agencies have closed. So from the first week, hold your own copies of the signed site agreement, every weekly hour log, and the supervision records &mdash; collected as they are signed, not reconstructed later.</p>
<p>The stakes are not small: up to <b>1,300 pre-degree hours</b> can count toward your 3,000 &mdash; of which no more than 750 may be counseling and direct supervisor contact &mdash; which is 1,300 fewer to find after graduation, in the season when you are also job-hunting. &sect;4980.43(c)(4), (5)<sup><a href="#s2">[2]</a></sup>.</p>
<p>And if you expect to stay at your agency past graduation, two pieces of end-game paperwork start <em>during</em> the practicum: the employer&rsquo;s Live Scan, which a trainee may complete while still a trainee, and the registration application the Board must receive within 90 days of the degree. Both are on <a href="bbs-90-day-rule-california.html">the 90-day rule page</a>, and both are cheaper to read now than in your final term.</p>
<div class="arttool"><b>Searching in the Bay Area?</b><p>The practicum-sites directory lays out the full universe for the nine counties by name &mdash; every program clinic, county plan, health-center organization and clinical nonprofit, with every listed link checked by hand.</p><a href="practicum-sites-bay-area.html">Open the directory &rarr;</a></div>
<div class="artsrc"><h2>Sources</h2><ol><li id="s1"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=4980.42." target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4980.42</a> &mdash; subdivision (e): the school shall approve each site and shall have a written agreement with each site; the burden of proof for hours gained at a school other than the degree-conferring one; subdivision (c): enrollment in a practicum course, and the under-90-day gap exception</li><li id="s2"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=4980.43." target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4980.43</a> &mdash; subdivision (c)(4)&ndash;(5), the 1,300-hour pre-degree ceiling and the 750-hour inner cap; subdivision (c)(6), no hours before 12 semester or 18 quarter units</li><li id="s3"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=4980.43.2." target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4980.43.2</a> &mdash; the supervision floor: one hour of direct supervisor contact per setting per week, plus one additional hour per five hours of direct clinical counseling</li><li id="s4"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&amp;sectionNum=4980.43.3." target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4980.43.3</a> &mdash; subdivision (a), employee or volunteer and never independent contractor; (b), no private practice or professional corporation; (d), supervisor conflicts; (e)&ndash;(f), payment only from the employer and no proprietary interest, lease or rent</li></ol><p class="disc">The 78-program placement survey, the in-house-clinic count and the quoted placement-office advice are this site&rsquo;s own August 2026 read of each program&rsquo;s published materials, documented program by program on <a href="practicum-california-mft-trainee.html">the practicum rules page</a>. The agency counts are computed from the IRS Exempt Organizations Business Master File and shown organization by organization on <a href="practicum-sites-bay-area.html">the Bay Area directory</a>. Statutory text is quoted from the sections linked above. This is not legal advice.</p></div>
<div class="artnext"><b>Read next</b><div class="g"><a href="practicum-california-mft-trainee.html"><i>Licensure</i><strong>The seven trainee rules, and all 78 programs compared on placement.</strong></a><a href="bbs-90-day-rule-california.html"><i>Licensure</i><strong>The 90-day rule, and the hours that vanish without it.</strong></a></div></div></div></div></article>"""

TSFOOT = """<!-- _dev/pixel_concepts.py --><div class="tsfoot"><div class="tsmeta"><div class="tsrow"><span class="tsk">Last checked</span><span class="tsv">16 August 2026</span><a class="tsall" href="changes.html">All updates &rarr;</a></div><div class="tsvint"><span class="tsk">Figures current as of</span><b>the August 2026 program survey and the current IRS EO Business Master File</b><i>Program handbooks move without notice; the BMF is republished monthly.</i></div><div class="tsdepth"><a class="tsbadge full" href="about.html#how-pages-are-checked">Figures and narrative checked together</a><p class="tswhat">Statutory text was verified against leginfo; the survey figures are restated from the pages that own them, with their read dates.</p></div></div></div><!-- /pixel_concepts -->"""

# Affirmative availability claims are banned on directory-adjacent pages.
BANNED = ("is hiring", "has openings", "takes trainees", "accepting trainees",
          "currently accepting", "spots available", "positions open")


def main():
    tpl = open(os.path.join(SITE, TEMPLATE), encoding="utf-8").read()
    s = tpl

    # ---- head surgery
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, s,
               count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               r"\g<1>%s\g<2>" % DESC, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
               r"\g<1>%s\g<2>" % CANON, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               r"\g<1>%s\g<2>" % CANON, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
               r"\g<1>%s\g<2>" % TITLE, s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
               r"\g<1>%s\g<2>" % DESC, s, count=1)

    # ---- ts:meta block: this page's registry identity
    m = re.search(r"<!-- ts:meta -->.*?<!-- /ts:meta -->", s, re.S)
    if not m:
        sys.exit("template has no ts:meta block")
    s = s[:m.start()] + TSMETA + s[m.end():]

    # ---- JSON-LD: rewrite the Article block, regenerate the breadcrumb
    art_ld = ('{"@context":"https://schema.org","@type":"Article",'
              '"headline":"%s",'
              '"description":"%s",'
              '"url":"%s",'
              '"datePublished":"2026-08-16","dateModified":"2026-08-16",'
              '"author":{"@type":"Organization","name":"Therapist Support"},'
              '"publisher":{"@type":"Organization","name":"Therapist Support",'
              '"url":"https://therapistsupport.org/"}}'
              % (TITLE.replace('"', ''), DESC.replace('"', ''), CANON))
    bcr_ld = ('{"@context":"https://schema.org","@type":"BreadcrumbList",'
              '"itemListElement":[{"@type":"ListItem","position":1,'
              '"name":"Therapist Support",'
              '"item":"https://therapistsupport.org/"},'
              '{"@type":"ListItem","position":2,"name":"Resources",'
              '"item":"https://therapistsupport.org/resources.html"},'
              '{"@type":"ListItem","position":3,"name":"Licensure"}]}')
    lds = list(re.finditer(
        r'<script type="application/ld\+json">.*?</script>', s, re.S))
    if len(lds) < 2:
        sys.exit("template carries %d JSON-LD blocks, expected 2+" % len(lds))
    s = (s[:lds[0].start()]
         + '<script type="application/ld+json">%s</script>' % art_ld
         + s[lds[0].end():lds[1].start()]
         + '<script type="application/ld+json">%s</script>' % bcr_ld
         + s[lds[1].end():])

    # ---- body surgery: swap the article and the provenance block
    m = re.search(r'<article class="art">.*?</article>', s, re.S)
    if not m:
        sys.exit("template has no <article class=\"art\">")
    s = s[:m.start()] + ARTICLE + s[m.end():]
    m = re.search(r'<!-- _dev/pixel_concepts\.py --><div class="tsfoot">'
                  r'.*?<!-- /pixel_concepts -->', s, re.S)
    if not m:
        sys.exit("template has no tsfoot block")
    s = s[:m.start()] + TSFOOT + s[m.end():]

    # ---- guards
    bad = []
    for needle, why in [
        ("shall have a written agreement with each site",
         "the site-agreement quote"),
        ("not as an independent contractor",
         "the independent-contractor sentence"),
        ("private practice or a professional corporation",
         "the private-practice exclusion"),
        ("at least six sites", "the placement-office advice"),
        ("sectionNum=4980.42.", "the 4980.42 link"),
        ("sectionNum=4980.43.\"", "the 4980.43 link"),
        ("sectionNum=4980.43.2.", "the 4980.43.2 link"),
        ("sectionNum=4980.43.3.", "the 4980.43.3 link"),
    ]:
        if needle not in s:
            bad.append("missing %s" % why)
    low = re.sub(r"<[^>]+>", " ", s).lower()
    for phrase in BANNED:
        if phrase in low:
            bad.append("availability language: %r" % phrase)
    for f in ("practicum-california-mft-trainee.html",
              "practicum-sites-bay-area.html",
              "bbs-90-day-rule-california.html",
              "mft-programs-california.html"):
        if 'href="%s"' % f not in s:
            bad.append("internal link to %s missing" % f)
        if not os.path.exists(os.path.join(SITE, f)):
            bad.append("internal link target %s not on disk" % f)
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
    print("build_findsite: %s written, guards clean" % OUT)


if __name__ == "__main__":
    main()
