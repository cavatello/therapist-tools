#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The 90-day rule page - path 03's missing content.

The single biggest uncovered gap found by the architecture audit ("small
stage, permanent consequences"): post-degree hours gained before the
associate number issues count ONLY under BPC 4980.43(b)'s four conjunctive
conditions - and one of them (workplace Live Scan) has to be satisfied
before the hours are gained, which for people staying at their trainee
agency means BEFORE the degree is granted. Zero pages covered this.

Verified against primary sources on 13 August 2026, on top of the 11 August
rules-verification pass (claude/bbs-rules-verification-and-corrections.md):

  - BPC 4980.43(a)-(b) fetched from leginfo: the default (active
    registration required to gain post-degree hours) and the four-condition
    exception, quoted verbatim below.
  - bbs.ca.gov/pdf/90day_rule.pdf: "postdegree hours may ONLY be counted
    after the date recorded on the 'Request for Live Scan Service' form";
    DOJ results and employer letters cannot substitute; separate prints per
    employer; cites 4980.43 / 4996.23 / 4999.46 (all three tracks).
  - bbs.ca.gov/pdf/90day_rule_faq.pdf: applies to those graduating on or
    after 1 Jan 2020; "the law does not allow for any alternatives" to the
    processed form; trainees may complete the employer Live Scan during
    trainee status if continuing at the same agency.

BUILD MECHANISM. Chrome, head scripts and tail scripts are taken verbatim
from bbs-fees-california-2026.html (same topic, same converted family), so
this page is born in the house design and family_art.py keeps it there.
Only the head metadata, the <article>, and the tsfoot provenance block are
this builder's own.

Guards: the four conditions present; the no-alternatives sentence present;
the private-practice sentence present; all six statute/source links
present; title 15-68 chars; description 70-168; every artnav anchor
resolves; exactly one h1.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = "bbs-90-day-rule-california.html"
TEMPLATE = "bbs-fees-california-2026.html"

TITLE = "The 90-day rule: when post-degree hours count in California"
DESC = ("Post-degree hours count before your associate number only if the "
        "BBS receives your application within 90 days of your degree, and "
        "your workplace Live Scanned you first.")
DESC_PLAIN = ("Post-degree hours count before your associate number only if "
              "the BBS receives your application within 90 days of your "
              "degree, and your workplace Live Scanned you first.")
H1 = "The 90-day rule, and the hours that <em>vanish without it</em>"
CANON = "https://therapistsupport.org/" + OUT

ARTICLE = """<article class="art"><section class="artband"><div class="in"><div><ol class="bcr" aria-label="Breadcrumb"><li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li><li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li><li><span aria-current="page">Licensure</span></li></ol><p class="kick">California &middot; licensure deadlines</p><h1>The 90-day rule, and the hours that <em>vanish without it</em></h1><p class="dek">Between your degree award date and the day your associate number issues, every supervised hour you work either counts toward your 3,000 or does not &mdash; decided by an application deadline and a fingerprint form, both of which are settled before you start. Here is the rule on all three tracks, the trap inside it, and the arithmetic of missing.</p><div class="artmeta"><span>Licensure</span><span>11 min read</span></div><!-- _dev/pixel_concepts.py --><div class="tsshort"><p class="tsk">In short</p><q>Do hours count before my associate number arrives?</q><p class="tsa">Only if the Board received your application within 90 days of your degree &mdash; and your workplace Live Scanned you first</p><span class="tsfig">90 days &middot; no exceptions</span></div><!-- /pixel_concepts --></div><div class="artfig"><b>90 days</b><span>from the granting of your degree to the Board <b>receiving</b> your application. Receipt, not postmark.</span></div></div></section><div class="artwrap"><nav class="artnav"><b>On this page</b><a href="#the-default-and-the-exception"><i class="tsn">1</i>The default is that your hours do not count</a><a href="#the-four-conditions"><i class="tsn">2</i>The four conditions, and where they bite</a><a href="#the-live-scan-trap"><i class="tsn">3</i>The Live Scan trap: the date that starts your clock</a><a href="#what-missing-costs"><i class="tsn">4</i>What missing it costs, in hours and months</a><a href="#the-edges"><i class="tsn">5</i>The edges the statute does not answer</a><a href="#the-other-deadlines"><i class="tsn">6</i>Two deadlines people confuse with this one</a><a href="#on-monday"><i class="tsn">7</i>What to do, by where you stand</a></nav><div class="artbody">
<h2 id="the-default-and-the-exception">The default is that your hours do not count</h2>
<p>The statute opens with the rule everyone wishes were the exception: &ldquo;all applicants shall have an active associate registration with the board in order to gain postdegree hours of supervised experience.&rdquo;<sup><a href="#s1">[1]</a></sup> No number, no hours. The weeks between the day your degree is granted and the day your registration issues are, by default, unpaid into the 3,000 no matter how supervised the work was.</p>
<p>Subdivision (b) is the exception, and it is the only one. It lets that gap count &mdash; but it is written as a set of conditions joined by <b>and</b>, not <b>or</b>, and the Board applies it that way. The first condition is the one the rule is named for:</p>
<div class="quote"><p>&ldquo;The registration applicant applies for the associate registration and the board receives the application within 90 days of the granting of the qualifying master&rsquo;s degree or doctoral degree.&rdquo;</p><cite>BPC &sect;4980.43(b) &mdash; see source [1]</cite></div>
<p>The same rule, in nearly the same words, sits in the social-work chapter at &sect;4996.23(b) and the counseling chapter at &sect;4999.46(b).<sup><a href="#s2">[2]</a><a href="#s3">[3]</a></sup> Whatever track you are on &mdash; AMFT, ASW or APCC &mdash; the clock, the conditions and the consequences are the same.</p>
<h2 id="the-four-conditions">The four conditions, and where they bite</h2>
<p>All four have to hold. Failing any one of them does not shrink your credit &mdash; it deletes it.</p>
<figure class="ig ig-steps"><figcaption class="ig-cap">The four conditions, in the order they have to happen</figcaption><ol><li><b>Your workplace required completed Live Scan fingerprinting before you gained the hours</b><span>Applies to everyone completing graduate study on or after 1 January 2020 &mdash; which is now everyone. This is the condition that has to be satisfied first, and for people staying at their practicum agency, it can and should be satisfied before the degree is granted.</span></li><li><b>The Board receives your registration application within 90 days of the granting of your degree</b><span>Receives. Not postmarked, not submitted-and-pending &mdash; received. The award date on your transcript starts the clock, not the ceremony.</span></li><li><b>The Board subsequently grants the registration</b><span>A denied application makes the question moot. An approved one reaches back and collects the gap &mdash; if the other conditions held.</span></li><li><b>The setting is not a private practice or professional corporation</b><span>&ldquo;The applicant shall not be employed or volunteer in a private practice or a professional corporation until the applicant has been issued an associate registration.&rdquo;<sup><a href="#s1">[1]</a></sup> For those settings there is no exception to wait inside &mdash; the number comes first.</span></li></ol></figure>
<p>Notice what is absent: intent, hardship, employer error. The Board&rsquo;s own guidance on the rule does not carry a discretion clause, and its FAQ answers the documentation question with a sentence worth reading twice: other documentation cannot be accepted &ldquo;as the law does not allow for any alternatives.&rdquo;<sup><a href="#s5">[5]</a></sup></p>
<h2 id="the-live-scan-trap">The Live Scan trap: the date that starts your clock</h2>
<p>The 90-day deadline gets the name, but the fingerprint condition is where people actually lose hours, for one reason: <b>hours do not start counting at your degree date. They start on the date recorded at the bottom of the processed &ldquo;Request for Live Scan Service&rdquo; form your employer required.</b><sup><a href="#s4">[4]</a></sup></p>
<div class="pull"><b>Day zero</b><span>is the date stamped on your processed Live Scan form &mdash; not your award date, and not your first day of work.</span></div>
<p>Four consequences follow, each of them documented in the Board&rsquo;s own materials rather than inferred:</p>
<p><b>The form is the only evidence.</b> A Department of Justice results letter does not work. A letter from your employer confirming you were fingerprinted does not work. The processed form itself, with its date, is what the Board accepts &mdash; keep your copy as carefully as you keep your transcripts.<sup><a href="#s4">[4]</a><a href="#s5">[5]</a></sup></p>
<p><b>The Board&rsquo;s own Live Scan does not satisfy it.</b> Your registration application includes fingerprinting for the Board. That is a different requirement with a different requester. The condition in the statute is that your <b>workplace</b> required prints before the hours were gained; the Board&rsquo;s prints do not reach it.<sup><a href="#s4">[4]</a></sup></p>
<p><b>Prints do not travel between employers.</b> Change workplaces during the gap and the new employer&rsquo;s hours count only from the date on the new employer&rsquo;s form. Each setting, its own Live Scan, its own day zero.<sup><a href="#s4">[4]</a></sup></p>
<p><b>Trainees are not required to be fingerprinted &mdash; which is exactly the opening.</b> If you will keep working at the same agency after you graduate, the Board&rsquo;s FAQ confirms you may complete the employer&rsquo;s Live Scan while still a trainee.<sup><a href="#s5">[5]</a></sup> Done in your final term, the stamped date precedes your award date and your clock has no hole in it at all.</p>
<h2 id="what-missing-costs">What missing it costs, in hours and months</h2>
<p>The registration itself is currently fast &mdash; a clean AMFT application has been processing in about 15 days, tracked with the Board&rsquo;s other queues on <a href="bbs-processing-times-california.html">the processing-times page</a>. The cost of this rule is not the wait. It is the work you already did.</p>
<p>Run the arithmetic on an ordinary miss. Degree awarded 12 June. Supervised community-mental-health job starts 1 July at 25 hours a week. Nobody mentions the rule; the application goes in on 25 September &mdash; day 105. Registration issues mid-October. Every one of the roughly <b>360 supervised hours</b> worked between 1 July and issuance is gone: not reduced, not partially credited, gone, because condition two failed and the exception never attached.</p>
<div class="pull"><b>360 hours</b><span>lost in one ordinary miss &mdash; 12% of the whole 3,000, and about three and a half months of re-earning at the same pace.</span></div>
<p>Now the compliant version of the same six months. Employer&rsquo;s Live Scan processed 28 June, before the first shift. Application filed in July, received day 45. Registration issues in August. Every hour from 1 July counts, collected retroactively from the form&rsquo;s date. Same job, same supervisor, same client hours &mdash; a different quarter-year of your life, decided by paperwork sequencing that costs nothing to get right.</p>
<h2 id="the-edges">The edges the statute does not answer</h2>
<p>Four questions come up constantly, and honesty requires saying which have answers.</p>
<p><b>What counts as the granting of the degree?</b> The statute says &ldquo;granting&rdquo;; the Board&rsquo;s materials read that as your <b>degree award date</b> &mdash; the date your institution posts to the transcript, which is routinely weeks before commencement and occasionally after it.<sup><a href="#s5">[5]</a></sup> Count from the transcript, never the ceremony.</p>
<p><b>Received means received.</b> Mail time is inside your 90 days, not outside it. Filing through the Board&rsquo;s BreEZe portal removes that variable, and the Board&rsquo;s own application tips amount to the same advice: file early, treat day 60 as your private deadline, and let the margin absorb what you did not predict.<sup><a href="#s6">[6]</a></sup></p>
<p><b>Calendar days or business days?</b> Nothing in the statute or the Board&rsquo;s guidance says business days. Assume calendar days, because assuming otherwise risks five weeks on an interpretation nobody in authority has endorsed.</p>
<p><b>If an application arrives on time but is deficient, does the original receipt date survive?</b> The Board has published no guidance either way. This page will not guess. File complete, file early, and the question never reaches you.</p>
<h2 id="the-other-deadlines">Two deadlines people confuse with this one</h2>
<p>Two other clocks live near this rule and get mistaken for it, in both directions.</p>
<div class="tw"><table class="tbl"><thead><tr><th>The clock</th><th>How long</th><th>What it governs</th></tr><tbody><tr><td>The 90-day rule</td><td class="n">90 days</td><td>Whether post-degree hours gained before your number issues can count at all</td></tr><tr><td>Practicum lapse</td><td class="n">90 days</td><td>A break in practicum enrollment of 90 days or more voids the hours gained in it &mdash; a pre-degree rule for MFT trainees, BPC &sect;4980.42<sup><a href="#s7">[7]</a></sup></td></tr><tr><td>Supervision agreement</td><td class="n">60 days</td><td>You and your supervisor must sign the supervision agreement within 60 days of supervision starting &mdash; 16 CCR &sect;1833(c), and it is 60, not 90<sup><a href="#s8">[8]</a></sup></td></tr></tbody></table></div>
<p>They do not interact, they do not extend one another, and satisfying one buys nothing against the others. The only thing they share is that each is cheap to meet on time and expensive to meet late.</p>
<h2 id="on-monday">What to do, by where you stand</h2>
<p><b>Still enrolled, planning to stay at your agency after graduating.</b> Ask now whether the agency requires Live Scan for post-degree staff, complete the State of California Request for Live Scan Service before your award date, and keep the processed copy. Then file the registration application in your final weeks so the Board receives it well inside the window.</p>
<p><b>Just graduated.</b> Find the award date on your transcript and count. The application does not wait for a job offer &mdash; the registration is yours, not your employer&rsquo;s, and filing it is the one condition entirely inside your control. File through BreEZe and the receipt question answers itself.</p>
<p><b>Working in the gap right now.</b> Confirm two documents exist today: the Board&rsquo;s timestamp on your application, and your employer&rsquo;s processed Live Scan form dated before your first supervised hour. If either is missing, every further week deepens the loss &mdash; and if the window is still open, closing the gap this week is worth more than anything else on your list.</p>
<p><b>Past day 90.</b> The exception is gone and no appeal recreates it. What remains is speed: hours count from issuance, a clean application is currently processing in about two weeks, and the sooner the number issues, the sooner the meter runs. Apply today, and if a private-practice offer is on the table, remember it cannot lawfully start until the number exists.</p>
<div class="arttool"><b>Where does your date actually land?</b><p>The 3,000-hours calculator projects your real working week against every licensure gate at once and names the one deciding your date &mdash; including the weeks this rule just added or saved.</p><a href="amft-3000-hours-california.html">Open the calculator &rarr;</a></div>
<div class="artsrc"><h2>Sources</h2><ol><li id="s1"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4980.43.&amp;lawCode=BPC" target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4980.43</a> &mdash; subdivision (a), the active-registration default; subdivision (b), the four-condition exception, including the 90-day receipt rule, the workplace Live Scan condition for graduate study completed on or after 1 January 2020, and the private-practice exclusion</li><li id="s2"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4996.23.&amp;lawCode=BPC" target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4996.23</a> &mdash; the parallel rule for associate clinical social workers</li><li id="s3"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4999.46.&amp;lawCode=BPC" target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4999.46</a> &mdash; the parallel rule for associate professional clinical counselors</li><li id="s4"><a href="https://bbs.ca.gov/pdf/90day_rule.pdf" target="_blank" rel="noopener noreferrer">Board of Behavioral Sciences, &ldquo;The 90-Day Rule&rdquo;</a> &mdash; &ldquo;postdegree hours may ONLY be counted after the date recorded on the &lsquo;Request for Live Scan Service&rsquo; form&rdquo;; DOJ results and employer letters cannot substitute; the employer&rsquo;s Live Scan is distinct from the Board&rsquo;s; separate prints per employer</li><li id="s5"><a href="https://www.bbs.ca.gov/pdf/90day_rule_faq.pdf" target="_blank" rel="noopener noreferrer">Board of Behavioral Sciences, 90-Day Rule FAQ</a> &mdash; applies to those graduating on or after 1 January 2020; hours count &ldquo;as of the date recorded at the bottom of the Request for Live Scan Service form&rdquo;; other documentation cannot be accepted &ldquo;as the law does not allow for any alternatives&rdquo;; trainees continuing at the same agency may complete the employer Live Scan during trainee status</li><li id="s6"><a href="https://www.bbs.ca.gov/pdf/publications/top_tips_smooth_associate_app.pdf" target="_blank" rel="noopener noreferrer">Board of Behavioral Sciences, Top Tips for a Smooth Associate Application</a> &mdash; the Board&rsquo;s own filing advice</li><li id="s7"><a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4980.42.&amp;lawCode=BPC" target="_blank" rel="noopener noreferrer">Cal. Business and Professions Code &sect;4980.42</a> &mdash; a lapse in practicum enrollment of 90 days or more voids the hours gained in that practicum</li><li id="s8"><a href="https://www.law.cornell.edu/regulations/california/16-CCR-1833" target="_blank" rel="noopener noreferrer">16 CCR &sect;1833(c)</a> &mdash; the supervision agreement must be signed within 60 days of supervision commencing</li></ol><p class="disc">Every figure here is either quoted from the statute or Board document named beside it, or computed in front of you from stated assumptions. Nothing is illustrative. This is not legal advice, and reading it does not create a professional relationship.</p></div>
<div class="artnext"><b>Read next</b><div class="g"><a href="bbs-processing-times-california.html"><i>Licensure</i><strong>How long the Board actually takes, queue by queue.</strong></a><a href="getting-hired-as-a-california-associate.html"><i>Licensure</i><strong>Getting hired as a California associate, without folklore.</strong></a></div></div></div></div></article>"""

TSFOOT = """<!-- _dev/pixel_concepts.py --><div class="tsfoot"><div class="tsmeta"><div class="tsrow"><span class="tsk">Last checked</span><span class="tsv">13 August 2026</span><a class="tsall" href="changes.html">All updates &rarr;</a></div><div class="tsvint"><span class="tsk">Figures current as of</span><b>the Board&rsquo;s January 2026 statutes-and-regulations codification and its posted 90-day-rule guidance</b><i>Statutes move on 1 January; the Board&rsquo;s PDFs move without notice.</i></div><div class="tsdepth"><a class="tsbadge full" href="about.html#how-pages-are-checked">Figures and narrative checked together</a><p class="tswhat">Statutory text, Board guidance and the arithmetic were verified on the date above.</p></div></div></div><!-- /pixel_concepts -->"""


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

    # ---- JSON-LD: rewrite the Article block, regenerate the breadcrumb
    art_ld = ('{"@context":"https://schema.org","@type":"Article",'
              '"headline":"%s",'
              '"description":"%s",'
              '"url":"%s",'
              '"datePublished":"2026-08-13","dateModified":"2026-08-13",'
              '"author":{"@type":"Organization","name":"Therapist Support"},'
              '"publisher":{"@type":"Organization","name":"Therapist Support",'
              '"url":"https://therapistsupport.org/"}}'
              % (TITLE.replace('"', ''), DESC_PLAIN.replace('"', ''), CANON))
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
        ("the board receives the application within 90 days",
         "the statutory quote"),
        ("the law does not allow for any alternatives",
         "the no-alternatives sentence"),
        ("private practice or a professional corporation",
         "the private-practice exclusion"),
        ("sectionNum=4980.43", "the 4980.43 link"),
        ("sectionNum=4996.23", "the 4996.23 link"),
        ("sectionNum=4999.46", "the 4999.46 link"),
        ("90day_rule.pdf", "the Board 90-day PDF link"),
        ("90day_rule_faq.pdf", "the Board FAQ link"),
        ("16-CCR-1833", "the 1833 link"),
        ("sectionNum=4980.42", "the 4980.42 link"),
    ]:
        if needle not in s:
            bad.append("missing %s" % why)
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
    print("build_ninety: %s written, guards clean" % OUT)


if __name__ == "__main__":
    main()
