#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The statewide pre-licensed job-sites directory - confirmed entries only.

Reads RESEARCH/jobsites-verified-2026-08-16.json and publishes ONLY the
orgs whose OWN sites were independently confirmed (16 Aug 2026, home +
careers/training pages read the same day) to state pre-licensed or
associate roles, or a supervised-hours training program. The lead list
this began from is member-sourced and is neither reproduced nor cited as
authority; every published fact traces to the organization's own page,
linked per row. The not-found and unreachable counts are stated on the
page because the disclosure gap is itself the finding.

Availability language banned, as on every directory. Same build
mechanism as build_trainprogs.py (artband, chrome from the fees page).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = "prelicensed-job-sites-california.html"
TEMPLATE = "bbs-fees-california-2026.html"
DATA = os.path.join(SITE, "RESEARCH", "jobsites-verified-2026-08-16.json")

TITLE = "California employers that say they take pre-licensed clinicians"
DESC = ("Sixty-one California mental-health employers whose own sites state "
        "pre-licensed or associate roles, each with the page that says so, "
        "verified on a single dated read.")
CANON = "https://therapistsupport.org/" + OUT

TSMETA = """<!-- ts:meta -->
<meta name="ts:topic" content="licensure">
<meta name="ts:format" content="reference">
<meta name="ts:question" content="Which California employers say they take pre-licensed clinicians?">
<meta name="ts:outcome" content="61 employers statewide whose own sites state associate or pre-licensed roles, each with the page that says so and the date it was read">
<meta name="ts:number" content="61 of 198 reachable employer sites say it in writing">
<meta name="ts:weight" content="4">
<!-- /ts:meta -->"""

BANNED = ("is hiring", "has openings", "takes trainees", "accepting trainees",
          "currently accepting", "spots available", "positions open")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def rows_html(rows):
    o = ['<div class="tw"><table class="tbl"><thead><tr><th>Organization'
         '</th><th>What its site states, in brief</th></tr></thead><tbody>']
    for r in rows:
        url = r.get("evidence_url") or ""
        name = ('<a href="%s" target="_blank" rel="noopener noreferrer">%s'
                "</a>" % (esc(url), esc(r["org"]))) if url else esc(r["org"])
        o.append("<tr><td>%s</td><td>%s</td></tr>"
                 % (name, esc(r.get("evidence", ""))))
    o.append("</tbody></table></div>")
    return "\n".join(o)


def main():
    rows = [r for r in json.load(open(DATA, encoding="utf-8"))
            if r["verdict"] == "CONFIRMED" and r.get("evidence_url")]
    rows.sort(key=lambda r: r["org"].lower())
    counts = {v: 0 for v in ("CONFIRMED", "NOT-FOUND", "UNREACHABLE")}
    for r in json.load(open(DATA, encoding="utf-8")):
        counts[r["verdict"]] += 1
    if len(rows) < 50:
        sys.exit("build_jobsites: only %d confirmed rows - data missing?"
                 % len(rows))

    head = """<article class="art"><section class="artband"><div class="in"><div><ol class="bcr" aria-label="Breadcrumb"><li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li><li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li><li><span aria-current="page">Licensure</span></li></ol><p class="kick">California &middot; statewide &middot; pre-licensed employers</p><h1>The employers that say, in writing, <em>they take pre-licensed clinicians</em></h1><p class="dek">Two hundred California mental-health employer sites were read on one day &mdash; 16 August 2026 &mdash; for a single sentence: does this organization&rsquo;s own site state that it employs or trains pre-licensed clinicians, with supervision toward the 3,000 hours? Sixty-one do, and every row below links the page that says so. This is a directory of published statements, not of openings; no register of openings exists.</p><div class="artmeta"><span>Licensure</span><span>reference</span></div><!-- _dev/pixel_concepts.py --><div class="tsshort"><p class="tsk">In short</p><q>Which California employers say they take pre-licensed clinicians?</q><p class="tsa">61 of the 198 reachable employer sites checked say it on their own pages &mdash; each row links the exact page, read 16 August 2026</p><span class="tsfig">61 in writing &middot; 198 checked</span></div><!-- /pixel_concepts --></div><div class="artfig"><b>61 of 198</b><span>employer sites state pre-licensed or associate roles in writing. The other 137 may take associates too &mdash; their sites just do not say.</span></div></div></section><div class="artwrap"><nav class="artnav"><b>On this page</b><a href="#what-this-is"><i class="tsn">1</i>What this is, and is not</a><a href="#the-directory"><i class="tsn">2</i>The 61, with their own words</a><a href="#the-gap"><i class="tsn">3</i>The disclosure gap</a></nav><div class="artbody">
<h2 id="what-this-is">What this is, and is not</h2>
<p>Each organization below was checked the same way on the same day: its home page and its careers or training pages, read for an explicit statement that it employs or trains pre-licensed clinicians &mdash; AMFTs, ACSWs, APCCs, registered associates, or clinical trainees banking supervised hours. A row here means the statement exists at the linked page as of 16 August 2026, quoted or closely paraphrased. It does not mean a vacancy exists today, and it is not an endorsement. Before applying anywhere, run the offer against <a href="getting-hired-as-a-california-associate.html">which settings can legally bill for a pre-licensed clinician</a> and the supervision floor on <a href="amft-3000-hours-california.html">the 3,000-hours page</a>.</p>
<h2 id="the-directory">The 61, with their own words</h2>
""" + rows_html(rows) + """
<h2 id="the-gap">The disclosure gap</h2>
<p>Another %d employer sites were reachable on the same read and said nothing findable about pre-licensed roles on their public pages, and %d could not be reached at all. That is a statement about disclosure, not about hiring practice &mdash; community agencies routinely employ associates without saying so online. It does mean your application there starts as a cold ask rather than a response to a published program, and it is why this page prints only what can be pointed at.</p>
<div class="arttool"><b>Bay Area, in depth</b><p>For the nine Bay counties, two companion directories go further: every setting the code allows, and the agencies with full training programs in writing.</p><a href="training-programs-bay-area.html">The published training programs &rarr;</a></div>
<div class="artsrc"><h2>Sources</h2><p class="disc">Every row links the organization page the statement was read from, all on 16 August 2026. Employer pages change without notice &mdash; the linked page is the authority, not this summary. Reachability detail for the full 232-lead set is preserved in the site&rsquo;s research files. This is not an endorsement of any employer and says nothing about current vacancies.</p></div>
<div class="artnext"><b>Read next</b><div class="g"><a href="getting-hired-as-a-california-associate.html"><i>Licensure</i><strong>Why half of associate applications get no reply &mdash; a billing rule.</strong></a><a href="county-job-portals-california.html"><i>Licensure</i><strong>All 58 county job portals, verified.</strong></a></div></div></div></div></article>""" % (counts["NOT-FOUND"], counts["UNREACHABLE"])

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
        sys.exit("no ts:meta in template")
    s = s[:m.start()] + TSMETA + s[m.end():]
    art_ld = ('{"@context":"https://schema.org","@type":"Article",'
              '"headline":"%s","description":"%s","url":"%s",'
              '"datePublished":"2026-08-16","dateModified":"2026-08-16",'
              '"author":{"@type":"Organization","name":"Therapist Support"},'
              '"publisher":{"@type":"Organization","name":"Therapist Support",'
              '"url":"https://therapistsupport.org/"}}' % (TITLE, DESC, CANON))
    bcr_ld = ('{"@context":"https://schema.org","@type":"BreadcrumbList",'
              '"itemListElement":[{"@type":"ListItem","position":1,'
              '"name":"Therapist Support","item":"https://therapistsupport.org/"},'
              '{"@type":"ListItem","position":2,"name":"Resources",'
              '"item":"https://therapistsupport.org/resources.html"},'
              '{"@type":"ListItem","position":3,"name":"Licensure"}]}')
    lds = list(re.finditer(
        r'<script type="application/ld\+json">.*?</script>', s, re.S))
    if len(lds) < 2:
        sys.exit("expected 2+ JSON-LD blocks")
    s = (s[:lds[0].start()]
         + '<script type="application/ld+json">%s</script>' % art_ld
         + s[lds[0].end():lds[1].start()]
         + '<script type="application/ld+json">%s</script>' % bcr_ld
         + s[lds[1].end():])
    m = re.search(r'<article class="art">.*?</article>', s, re.S)
    if not m:
        sys.exit("no article in template")
    s = s[:m.start()] + head + s[m.end():]
    m = re.search(r'<!-- _dev/pixel_concepts\.py --><div class="tsfoot">'
                  r'.*?<!-- /pixel_concepts -->', s, re.S)
    if not m:
        sys.exit("no tsfoot in template")
    TSFOOT = ('<!-- _dev/pixel_concepts.py --><div class="tsfoot">'
              '<div class="tsmeta"><div class="tsrow"><span class="tsk">Last '
              'checked</span><span class="tsv">16 August 2026</span>'
              '<a class="tsall" href="changes.html">All updates &rarr;</a>'
              '</div><div class="tsvint"><span class="tsk">Figures current '
              'as of</span><b>each employer&rsquo;s own pages at the dated '
              'single-day read</b><i>Employer pages move without notice; '
              'the linked page is the authority.</i></div>'
              '<div class="tsdepth"><a class="tsbadge thin" '
              'href="about.html#how-pages-are-checked">Published sources '
              'only</a><p class="tswhat">Built from what each employer '
              'publishes about itself. Nothing here is independently '
              'verified beyond that read.</p></div></div></div>'
              '<!-- /pixel_concepts -->')
    s = s[:m.start()] + TSFOOT + s[m.end():]

    bad = []
    low = re.sub(r"<[^>]+>", " ", s).lower()
    for p in BANNED:
        if p in low:
            bad.append("availability language: %r" % p)
    for f in ("getting-hired-as-a-california-associate.html",
              "amft-3000-hours-california.html",
              "county-job-portals-california.html",
              "training-programs-bay-area.html"):
        if 'href="%s"' % f not in s:
            bad.append("internal link %s missing" % f)
    if s.count("<tr><td>") != len(rows):
        bad.append("row count %d != %d" % (s.count("<tr><td>"), len(rows)))
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
            bad.append("anchor #%s unresolved" % a)
    if bad:
        for b in bad:
            print("GUARD %s: %s" % (OUT, b))
        sys.exit(1)
    open(os.path.join(SITE, OUT), "w", encoding="utf-8").write(s)
    print("build_jobsites: %s written, %d confirmed rows, guards clean"
          % (OUT, len(rows)))


if __name__ == "__main__":
    main()
