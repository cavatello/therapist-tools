#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Can a Bay Area practicum-site and associate-site directory be built honestly?

THE QUESTION ASKED

"Should you add to the queue: Bay Area practicum sites, directory and
individual pages and as much content as possible? Then plan for the same for
associate sites?"

THE ANSWER, AND WHY IT IS NOT A SIMPLE YES

Yes - but as **two directories, not one with two labels**, because the statute
draws the line for us. Section 4980.43.3(b)(1) says a trainee shall not perform
services in a private practice or a professional corporation. Subdivision (c)
lets a registered associate work in exactly those settings. So the associate
universe strictly contains the trainee universe and adds the largest employer
category in the Bay Area to it. Building one list and relabelling it would send
students to sites they legally cannot use.

WHAT THIS PASS ACTUALLY DID

It is a feasibility probe, not a builder. It fetched three public federal and
state sources and counted what is reachable, so the proposal argues from
numbers rather than from optimism:

  - IRS Exempt Organizations Business Master File, California extract, filtered
    to NTEE code F (mental health and crisis intervention) and to the nine Bay
    Area counties by ZCTA. 614 active organizations, of which 313 are direct
    clinical service, 147 are substance-use, and 154 are associations,
    foundations and financing vehicles that employ nobody clinically.
  - HRSA Health Center Service Delivery Sites. 517 active Bay Area
    service-delivery sites across 39 organizations, 269 with a published web
    address.
  - The site's own verified county behavioral health plans, program training
    clinics and county payroll data.

THE HONEST LIMIT, STATED UP FRONT

None of these sources says whether an organization takes trainees. There is no
public dataset that does. So the directory cannot claim availability, and the
whole design has to be built around claiming eligibility instead - what the
setting is, what the statute says about settings of that kind, and how to ask.
A directory that says "this place takes trainees" and is wrong costs a student
an application cycle, which is the one failure mode that matters here.

DATA IS INLINE, DELIBERATELY

The counts below are transcribed from the probe rather than recomputed at build
time, because the IRS extract is a 35 MB file that is not in the repository and
this is a proposal rather than a page that has to stay current. If it is
approved, the ETL that replaces this is described in section 05.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "bay-area-directories.html")
UPDATED = "11 August 2026"

LEG = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
       "?lawCode=BPC&sectionNum=%s.")
IRS = "https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf"
HRSA = "https://data.hrsa.gov/data/download"
SCO = "https://gcc.sco.ca.gov/Reports/RawExport.aspx"

NAV = [("answer", "The answer"), ("split", "Two directories"),
       ("sources", "What can be sourced"), ("claims", "What may be claimed"),
       ("build", "What to build"), ("scope", "Bay Area or statewide"),
       ("bugs", "Two defects found"), ("queue", "Cost and order")]

# ---- from the feasibility probe, 11 August 2026 -------------------------
CLINICAL_BY_COUNTY = [("Alameda", 80), ("Santa Clara", 54), ("San Francisco", 50),
                      ("Contra Costa", 50), ("Marin", 25), ("San Mateo", 21),
                      ("Sonoma", 18), ("Solano", 8), ("Napa", 7)]
HC_BY_COUNTY = [("Alameda", 155), ("Santa Clara", 92), ("San Francisco", 81),
                ("Contra Costa", 51), ("Sonoma", 44), ("San Mateo", 35),
                ("Solano", 28), ("Marin", 24), ("Napa", 7)]
BIGGEST = [
    ("Momentum for Health", "San Jose", "Santa Clara", "$96.6m"),
    ("John Muir Behavioral Health", "Walnut Creek", "Contra Costa", "$54.2m"),
    ("Caminar", "San Mateo", "San Mateo", "$49.3m"),
    ("Fred Finch Youth Center", "Oakland", "Alameda", "$40.9m"),
    ("Richmond Area Multi-Services", "San Francisco", "San Francisco", "$38.6m"),
    ("Asian Americans for Community Involvement", "San Jose", "Santa Clara", "$37.0m"),
    ("Progress Foundation", "San Francisco", "San Francisco", "$34.1m"),
    ("Edgewood Center for Children and Families", "San Francisco",
     "San Francisco", "$32.2m"),
    ("Lincoln", "Oakland", "Alameda", "$29.6m"),
    ("East Bay Agency for Children", "Oakland", "Alameda", "$25.5m"),
    ("WestCoast Children's Clinic", "Oakland", "Alameda", "$25.2m"),
    ("Buckelew Programs", "Novato", "Marin", "$23.1m"),
]
N_F = 614
N_CLINICAL = 313
N_SUBSTANCE = 147
N_OTHER = 154
N_OVER_1M = 55
N_OVER_5M = 22
N_NO_REV = 171
HC_SITES = 517
HC_ORGS = 39
HC_WEB = 269

EXTRA = """
.two{display:grid;gap:14px;margin:10px 0}
@media(min-width:820px){.two{grid-template-columns:1fr 1fr}}
.univ{border:2px solid var(--ink);background:var(--cream);box-shadow:4px 4px 0 var(--ink);
  padding:15px 17px}
.univ h4{font-size:17px;margin-bottom:3px}
.univ .n{font-family:var(--fig);font-weight:800;font-size:32px;color:var(--pine);
  line-height:1;margin:6px 0 3px}
.univ .s{font-size:12.5px;color:var(--muted);margin-bottom:8px}
.univ p{font-size:14px;margin:0 0 6px}
.univ .tagr{margin-top:9px;display:flex;flex-wrap:wrap;gap:6px}
.univ .t{font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;
  border:1.5px solid var(--ink);padding:3px 7px}
.univ .t.y{background:var(--pine);color:#fff;border-color:var(--pine)}
.univ .t.n{background:var(--red);color:#fff;border-color:var(--red)}
.univ .t.m{background:var(--gold)}
.may{display:grid;gap:12px;margin:12px 0}
@media(min-width:760px){.may{grid-template-columns:1fr 1fr}}
.may div{border:2px solid var(--ink);padding:13px 15px}
.may .ok{background:#F2F8F4;border-left:6px solid var(--green)}
.may .no{background:#FFF6F5;border-left:6px solid var(--red)}
.may ul{margin:7px 0 0;padding-left:19px;font-size:14px}
.may li{margin-bottom:5px}
.cols{display:grid;gap:9px;margin:10px 0}
@media(min-width:700px){.cols{grid-template-columns:repeat(3,1fr)}}
.cols div{border:1.5px solid var(--line);background:#fff;padding:9px 11px;font-size:12.5px}
.cols .v{font-family:var(--fig);font-weight:800;font-size:20px;color:var(--deep);display:block}
.bugbox{border:2px solid var(--ink);background:var(--cream);box-shadow:4px 4px 0 var(--ink);
  padding:15px 17px;margin-bottom:14px}
.bugbox .st{font-family:var(--mono);font-size:9px;letter-spacing:.11em;text-transform:uppercase;
  background:var(--pine);color:#fff;padding:3px 7px}
.bugbox .st.open{background:var(--red);color:#fff}
.bugbox h4{font-size:17px;margin:7px 0 5px}
.bugbox pre{font-family:var(--mono);font-size:11.5px;background:#fff;overflow-x:auto;
  border:1.5px solid var(--line);padding:9px 11px;margin:8px 0 0}
.risk{border:2px solid var(--red);background:#FFF6F5;padding:13px 15px;margin:12px 0}
.risk h4{color:var(--red);font-size:16px}
.risk p{font-size:14px;margin:0 0 8px}.risk p:last-child{margin:0}
code{font-family:var(--mono);font-size:12.5px;background:#fff;border:1px solid var(--line);
  padding:1px 5px}
"""


def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block to inherit.")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>Bay Area practicum and associate sites &mdash; can it be "
         "sourced?</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
         'opsz,wght@12..96,800&family=Fraunces:opsz,wght@9..144,600;9..144,800&'
         'family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&'
         'display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s &middot; not '
             "indexed</span>"
             "<h1>Yes &mdash; but it is two directories, and the statute is "
             "what splits them.</h1>"
             "<p>A feasibility probe rather than a plan on paper: three public "
             "datasets were fetched and counted before any of this was "
             "written. What is reachable, what is not, what may honestly be "
             "claimed about a site, and what it costs to build.</p>"
             '<div class="meta"><span class="chip">313 clinical orgs</span>'
             '<span class="chip">517 health-center sites</span>'
             '<span class="chip">9 counties</span>'
             '<span class="chip">1 category unreachable</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, l in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, l))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    # ---------------------------------------------------------------- answer
    o.append('<section id="answer"><div class="kicker"><span class="n">01</span>'
             "<h2>The answer</h2></div>")
    o.append('<div class="verdict">'
             '<div><ul class="vlist">'
             "<li><b>Build it &mdash; the data is there.</b> 313 Bay Area "
             "nonprofit clinical mental health organizations and 517 active "
             "health-center service-delivery sites are reachable from federal "
             "files that anybody can re-download and check. This is not a "
             "scraping project.</li>"
             "<li><b>Two directories, not one.</b> A trainee cannot lawfully "
             "work in a private practice; a registered associate can. The two "
             "eligible universes are genuinely different sets and merging them "
             "would send students somewhere they cannot go.</li>"
             "<li><b>Claim eligibility, never availability.</b> No public "
             "source says who takes trainees. The directory answers &ldquo;is "
             "this the kind of setting the code allows, and how do I ask?"
             "&rdquo; &mdash; which is a question it can answer completely.</li>"
             "<li><b>Not 600 individual pages.</b> The coverage audit already "
             "found 36% of this library serving the quietest stage. One "
             "directory plus depth on the 22 organizations large enough to "
             "write about, and the long tail stays in the table.</li>"
             "<li><b>Build the data statewide, publish the Bay Area first.</b> "
             "Both federal files are statewide already. A Bay-Area-shaped ETL "
             "would have to be rewritten the first time Los Angeles is "
             "wanted.</li>"
             "</ul></div>"
             '<div class="card pine"><span class="lab">The one that changes '
             "the shape</span><h3>Group private practices are unreachable.</h3>"
             "<p>They are the largest employer of Bay Area associates and "
             "there is no public register of them &mdash; not by IRS status, "
             "not by license, not by anything. The associate directory can "
             "cover county, safety-net and nonprofit employers completely and "
             "the private sector not at all.</p>"
             "<p style=\"margin:0\"><b>That has to be said on the page, in the "
             "first screen.</b> A directory that looks complete and is missing "
             "the biggest category teaches people the wrong shape of the "
             "market.</p></div></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- split
    o.append('<section id="split"><div class="kicker"><span class="n">02</span>'
             "<h2>Why it is two directories</h2></div>")
    o.append('<p class="lede">This is not an editorial preference. The two '
             "readers have different <em>legal</em> universes, one strictly "
             "inside the other.</p>")
    o.append('<div class="tw"><table><tr><th>Setting</th>'
             "<th>Trainee &mdash; still in the program</th>"
             "<th>Associate &mdash; registered</th><th>Authority</th></tr>"
             "<tr><td>County behavioral health department</td><td>Eligible</td>"
             "<td>Eligible</td><td>&sect;&thinsp;4980.43.3(b), (c)</td></tr>"
             "<tr><td>Community clinic, health center, nonprofit agency</td>"
             "<td>Eligible</td><td>Eligible</td>"
             "<td>&sect;&thinsp;4980.43.3(b)(1)(B)</td></tr>"
             "<tr><td>School district or county office of education</td>"
             "<td>Eligible</td><td>Eligible</td><td>&sect;&thinsp;4980.43.3(b)</td></tr>"
             '<tr class="hi"><td><b>Private practice</b></td>'
             "<td><b>Not eligible &mdash; at all</b></td><td>Eligible once the "
             "registration is issued</td>"
             "<td><b>&sect;&thinsp;4980.43.3(b)(1), (c)(3)</b></td></tr>"
             "<tr><td><b>Professional corporation</b></td>"
             "<td><b>Not eligible &mdash; at all</b></td>"
             "<td>Eligible once the registration is issued</td>"
             "<td>&sect;&thinsp;4980.43.3(b)(1)</td></tr>"
             "<tr><td>Any of the above, as an independent contractor</td>"
             "<td>Never</td><td>Never</td><td>&sect;&thinsp;4980.43.3(a)</td></tr>"
             "</table></div>")
    o.append('<p class="src">Sections linked in full at the foot of this page. '
             "The trainee rules are already published on "
             '<a href="../practicum-california-mft-trainee.html">the practicum '
             "page</a>, which is where the directory would link rather than "
             "restating them.</p>")
    o.append('<div class="risk"><h4>The practical consequence</h4>'
             "<p>Roughly half of what a Bay Area student is told to try "
             "&mdash; &ldquo;ask around, someone&rsquo;s supervisor has room&"
             "rdquo; &mdash; points at private practices, which are the one "
             "setting the code rules out entirely for a trainee. The trainee "
             "directory&rsquo;s single most useful function is being the list "
             "of places that are <em>not</em> that.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # --------------------------------------------------------------- sources
    o.append('<section id="sources"><div class="kicker"><span class="n">03</span>'
             "<h2>What can actually be sourced</h2></div>")
    o.append('<p class="lede">Five universes. Four are reachable from public '
             "files and were counted on 11 August; the fifth is the hole.</p>")

    o.append('<div class="two">')
    for h, n, s, p, tags in [
        ("Nonprofit clinical organizations", "313",
         "IRS Exempt Organizations master file &middot; NTEE code F &middot; "
         "nine Bay Area counties by ZCTA",
         "The set that actually employs trainees and associates. %d report "
         "revenue over $1m and %d over $5m; %d report none, which usually "
         "means small or a non-filer rather than inactive. A further %d "
         "substance-use organizations and %d associations and foundations "
         "were separated out rather than mixed in."
         % (N_OVER_1M, N_OVER_5M, N_NO_REV, N_SUBSTANCE, N_OTHER),
         [("Trainee eligible", "y"), ("Associate eligible", "y"),
          ("NTEE is self-reported", "m")]),
        ("Health-center service-delivery sites", "517",
         "HRSA Health Center Service Delivery Sites &middot; %d organizations "
         "&middot; %d with a published web address" % (HC_ORGS, HC_WEB),
         "Federally qualified health centers and look-alikes, at site level "
         "with name, street address, city, county and telephone. Updated "
         "federally, so it stays current without anybody maintaining it.",
         [("Trainee eligible", "y"), ("Associate eligible", "y"),
          ("Behavioral program not flagged", "m")]),
        ("County behavioral health plans", "9",
         "Already verified and published on this site",
         "The nine Bay Area plans are part of the 57 already fetched, checked "
         "and published in the safety-net employer directory. Nothing new to "
         "source &mdash; this is a filter over work that is done.",
         [("Trainee eligible", "y"), ("Associate eligible", "y"),
          ("Already verified", "y")]),
        ("Program training clinics", "5",
         "The site's own 78-program research file",
         "Bay Area programs that run a clinic of their own. These take "
         "trainees <em>by construction</em> &mdash; it is what the clinic is "
         "for &mdash; which makes them the only entries in the whole "
         "directory where availability is not a guess. Several take students "
         "from other schools.",
         [("Trainee eligible", "y"), ("Highest confidence", "y")]),
    ]:
        o.append('<div class="univ"><h4>%s</h4><div class="n">%s</div>'
                 '<div class="s">%s</div><p>%s</p><div class="tagr">%s</div></div>'
                 % (h, n, s, p,
                    "".join('<span class="t %s">%s</span>' % (c, t)
                            for t, c in tags)))
    o.append('<div class="univ" style="border-color:var(--red)">'
             "<h4>Group private practices</h4>"
             '<div class="n" style="color:var(--red)">&mdash;</div>'
             '<div class="s">No public dataset exists</div>'
             "<p>Not registrable as a category. The licensee register lists "
             "people, not employers. Business registration does not record "
             "what a practice does. Directory sites are commercial listings "
             "with their own incentives and are not a source.</p>"
             '<div class="tagr"><span class="t n">Trainee: never eligible</span>'
             '<span class="t m">Associate: eligible, unreachable</span></div>'
             "</div>")
    o.append("</div>")

    o.append('<p class="pk-k lab" style="display:block;margin-top:20px">'
             "Where the 313 are</p>")
    o.append('<div class="tw"><table><tr><th>County</th>'
             "<th>Nonprofit clinical organizations</th>"
             "<th>Health-center sites</th></tr>")
    hc = dict(HC_BY_COUNTY)
    for c, n in CLINICAL_BY_COUNTY:
        o.append('<tr><td>%s</td><td><span class="fig">%d</span></td>'
                 '<td><span class="fig">%d</span></td></tr>'
                 % (c, n, hc.get(c, 0)))
    o.append('<tr class="hi"><td><b>Nine counties</b></td>'
             '<td><b><span class="fig">%d</span></b></td>'
             '<td><b><span class="fig">%d</span></b></td></tr>'
             % (N_CLINICAL, HC_SITES))
    o.append("</table></div>")
    o.append('<p class="src">Counted 11 August 2026. Organization counts are '
             "active registrations with an NTEE code in the F range, mapped to "
             "county from ZIP through the Census ZCTA relationship file. "
             "Health-center counts are active service-delivery sites, "
             "administrative-only locations excluded.</p>")

    o.append('<p class="lab" style="display:block;margin-top:18px">The largest '
             "twelve, by reported revenue</p>")
    o.append('<div class="tw"><table><tr><th>Organization</th><th>City</th>'
             "<th>County</th><th>Reported revenue</th></tr>")
    for nm, city, co, rev in BIGGEST:
        o.append("<tr><td>%s</td><td>%s</td><td>%s</td>"
                 '<td><span class="fig">%s</span></td></tr>' % (nm, city, co, rev))
    o.append("</table></div>")
    o.append('<p class="src">These are the names that come up in Bay Area '
             "placement conversations, which is the check that the sourcing "
             "found the right set rather than a plausible-looking one. "
             "<b>Revenue is size, not relevance</b> &mdash; two organizations "
             "in the top 25 of the raw extract turned out to be a research "
             "foundation and a financing vehicle, and were removed by hand. "
             "That is the tier of checking the build needs.</p>")
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------------- claims
    o.append('<section id="claims"><div class="kicker"><span class="n">04</span>'
             "<h2>What may and may not be claimed</h2></div>")
    o.append('<p class="lede">This is the section that decides whether the '
             "directory is worth having. Everything reachable describes what "
             "an organization <em>is</em>. Nothing reachable describes whether "
             "it has a seat.</p>")
    o.append('<div class="may">'
             '<div class="ok"><span class="lab">May be published</span><ul>'
             "<li>That the organization exists, with its registered name and "
             "the address it filed</li>"
             "<li>Which of the four universes it belongs to, and what that "
             "means under &sect;&thinsp;4980.43.3</li>"
             "<li>Its county, and its size band from reported revenue</li>"
             "<li>Its website &mdash; <b>fetched before publication</b>, the "
             "way the 218 health centers and 57 county plans already are</li>"
             "<li>Whether the county it sits in is a designated mental health "
             "shortage area, and what the county pays its own clinicians</li>"
             "<li>How to ask, and what to ask &mdash; including the question "
             "about who signs the school&rsquo;s site agreement</li>"
             "</ul></div>"
             '<div class="no"><span class="lab">May not be published</span><ul>'
             "<li>That an organization &ldquo;takes trainees&rdquo; or "
             "&ldquo;accepts associates&rdquo;</li>"
             "<li>That it is hiring, or has openings</li>"
             "<li>That it offers supervision, or free supervision</li>"
             "<li>That it pays, or what it pays</li>"
             "<li>Any named individual &mdash; a supervisor, a training "
             "director, a contact</li>"
             "<li>Anything at all sourced from a program&rsquo;s private "
             "approved-site list, which sits behind a login</li>"
             "</ul></div></div>")
    o.append('<div class="risk"><h4>Why the right column is strict</h4>'
             "<p>A wrong &ldquo;yes&rdquo; costs a student an application "
             "cycle at the exact moment they have least slack. There are 313 "
             "organizations; nobody can verify placement availability across "
             "them and keep it verified, and a directory that is 80% right "
             "about availability is worse than one that is 100% right about "
             "eligibility.</p>"
             "<p>It is also the same discipline the loan-forgiveness page "
             "already runs under, where <code>&gt;Eligible&lt;</code>, "
             "<code>&gt;You qualify&lt;</code> and <code>&gt;Qualifies&lt;</code> "
             "are banned as verdicts by a build guard. The same guard should "
             "run here.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- build
    o.append('<section id="build"><div class="kicker"><span class="n">05</span>'
             "<h2>What to build</h2></div>")
    o.append('<p class="lede">Three pages and roughly two dozen profiles '
             "&mdash; not six hundred. The argument against the long tail is "
             "the site&rsquo;s own coverage audit.</p>")

    o.append('<div class="grid g3">')
    for t, s, b in [
        ("Two directory pages",
         "<code>practicum-sites-bay-area.html</code><br>"
         "<code>associate-employers-bay-area.html</code>",
         "Each one filterable by county and universe, each opening with the "
         "statutory line that defines its own list, each linking every "
         "organization to a website that was fetched before it shipped. The "
         "trainee page leads with the five program clinics, because they are "
         "the only entries where availability is certain."),
        ("One method page",
         "<code>how-to-find-a-practicum-site-california.html</code>",
         "The part that is actually scarce: what to ask, in what order, and "
         "what the school owes you. &sect;&thinsp;4980.42(e) puts the site "
         "agreement on the school, which is the single most useful sentence a "
         "student can carry into that conversation, and no directory row can "
         "say it for them."),
        ("About 22 profiles, leaf-flagged",
         "the organizations over $5m",
         "Where there is genuinely something to write: what they do, who they "
         "serve, which counties, how they are funded, whether they hold a "
         "county contract. Flagged <code>ts:leaf</code> like the 78 program "
         "pages and the 48 case studies, so they are reachable and indexed "
         "without burying a topic hub."),
    ]:
        o.append('<div class="card"><h3>%s</h3>'
                 '<p class="lab" style="margin-bottom:7px">%s</p>'
                 '<p style="margin:0">%s</p></div>' % (t, s, b))
    o.append("</div>")

    o.append('<div class="card gold"><h3>The argument against 313 pages</h3>'
             "<p style=\"margin:0\">The visitor-stage coverage audit found that "
             "<b>36% of this library &mdash; 66 of 182 pages &mdash; served the "
             "stage with the least community engagement</b>, because program "
             "reviews were cheap to generate. Three hundred thin organization "
             "pages built from four federal fields each would be the same "
             "mistake at twice the scale, and it would dilute the internal "
             "link graph that is the site&rsquo;s whole position. Depth where "
             "there is something to say; a table everywhere else.</p></div>")

    o.append('<p class="lab" style="display:block;margin-top:18px">The ETL, if '
             "this is approved</p>")
    o.append('<div class="tw"><table><tr><th>Pass</th><th>Reads</th>'
             "<th>Writes</th><th>Note</th></tr>"
             "<tr><td><code>_dev/nonprofits.py</code></td>"
             "<td>IRS EO master file, California extract, plus the Census ZCTA "
             "relationship file</td><td><code>_dev/nonprofit_data.py</code></td>"
             "<td>Needs the network, like <code>ipeds_degrees.py</code>. The "
             "committed artifact is the data module, not the 35&nbsp;MB "
             "extract.</td></tr>"
             "<tr><td><code>_dev/hrsa_sites.py</code></td>"
             "<td>Already exists &mdash; currently reduces to counts</td>"
             "<td>extend to emit site-level rows</td>"
             "<td>The site file is already cached and already parsed. This is "
             "an extension, not a new pass.</td></tr>"
             "<tr><td>domain verification</td><td>every candidate URL</td>"
             "<td>a fetched flag per organization</td>"
             "<td>The same routine <code>hc_orgs.py</code> runs, including "
             "<code>REACHABLE_ERRORS</code> &mdash; California nonprofits "
             "return 403 to scripts while working in a browser, and treating "
             "that as dead reported 22 false deaths last time.</td></tr>"
             "<tr><td><code>_dev/build_baysites.py</code></td>"
             "<td>all of the above plus <code>county_bh_data</code>, "
             "<code>county_pay_data</code>, <code>hrsa_stats</code>, "
             "<code>practicum_data</code></td><td>the three pages</td>"
             "<td>Guards: the availability words are banned; every published "
             "link answered; no named individuals.</td></tr>"
             "</table></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- scope
    o.append('<section id="scope"><div class="kicker"><span class="n">06</span>'
             "<h2>Bay Area, or statewide?</h2></div>")
    o.append('<p class="lede">Build the data statewide. Publish the Bay Area '
             "first. These are not in tension and getting it the other way "
             "round costs a rewrite.</p>")
    o.append('<div class="cols">'
             '<div><span class="v">$0</span>marginal cost of statewide data '
             "&mdash; both federal files are already the whole state, and the "
             "county filter is one line</div>"
             '<div><span class="v">High</span>marginal cost of statewide '
             "<em>editorial</em> depth &mdash; the profiles and the method "
             "page are regional judgment, not a query</div>"
             '<div><span class="v">1</span>rewrite avoided &mdash; a '
             "Bay-Area-shaped ETL has to be unpicked the first time Los "
             "Angeles is wanted</div></div>")
    o.append("<p>Los Angeles is the obvious second region and it is far larger "
             "&mdash; the health-center file alone carries <b>831 Los Angeles "
             "sites</b> against 517 for the whole Bay Area. Sacramento, San "
             "Diego and the Inland Empire follow. If the builder takes a "
             "region as a parameter from the start, each of those is a "
             "configuration entry and a week of editorial work rather than a "
             "new project.</p>")
    o.append('<p class="src">The Bay Area is the right first region anyway: '
             "nine counties, the densest concentration of programs with their "
             "own clinics, and the two counties with the highest published "
             "county pay in the state.</p>")
    o.append("</section><hr class=\"rule\">")

    # ------------------------------------------------------------------ bugs
    o.append('<section id="bugs"><div class="kicker"><span class="n">07</span>'
             "<h2>Two defects this probe found</h2></div>")
    o.append('<p class="lede">Both on a page that shipped this morning. '
             "Looking at Bay Area counties specifically is what surfaced "
             "them.</p>")

    o.append('<div class="bugbox"><span class="st">Fixed</span>'
             "<h4>Contra Costa was ranked on six positions. It has 531.</h4>"
             "<p>The county pay pass matched job titles on spelled-out "
             "keywords. <b>Contra Costa writes &ldquo;Mh Clinical "
             "Specialist&rdquo;</b>, not &ldquo;Mental Health Clinical "
             "Specialist&rdquo; &mdash; 232 people in that one title. Santa "
             "Barbara writes &ldquo;ADMHS Practitioner II&rdquo; after its old "
             "department name, and was ranked on five.</p>"
             "<p>Both counties were on the published table with a median "
             "computed from a handful of rows. That is worse than the "
             "undercount the method note already admits to, because it is a "
             "wrong number wearing a county&rsquo;s name.</p>"
             "<pre>Contra Costa    6 positions, $124,928  &rarr;  531 positions, $118,997\n"
             "Santa Barbara   5 positions, $109,824  &rarr;  215 positions, $101,820\n"
             "statewide      12,850 matched      &rarr;  13,184 matched\n"
             "headline spread   2.8&times;             &rarr;  2.8&times; (unchanged)</pre>"
             "<p style=\"margin-top:9px\">Fixed and redeployed. The top and "
             "bottom counties and the headline finding are unchanged, which is "
             "the reassuring part. A guard now prints a note for any county "
             "ranked on fewer than 25 positions, and the pass carries a "
             "comment saying the durable fix is to scope on the department "
             "name rather than keep adding acronyms &mdash; every county "
             "invents its own and a keyword list will keep losing that "
             "race.</p></div>")

    o.append('<div class="bugbox"><span class="st open">Open</span>'
             "<h4>San Francisco is absent from the county pay page entirely.</h4>"
             "<p>Not under-counted &mdash; <b>absent</b>. There is no employer "
             "named San Francisco anywhere in the State Controller&rsquo;s "
             "county file, because it is a consolidated city-county and files "
             "in the <em>cities</em> dataset instead. The page silently "
             "reports 55 of 58 counties and San Francisco is one of the "
             "missing three.</p>"
             "<p>For a Bay Area directory that is not a footnote: San "
             "Francisco is one of the largest public behavioral health "
             "employers in the region and the page currently says nothing "
             "about what it pays. The fix is to pull the city file for the "
             "same three years and merge the one employer.</p>"
             "<p style=\"margin:0\"><b>Queued, not fixed</b> &mdash; the city "
             "file is a separate download and this pass never touches the "
             "network.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- queue
    o.append('<section id="queue"><div class="kicker"><span class="n">08</span>'
             "<h2>Cost, and the order</h2></div>")
    o.append('<ol class="plan">')
    for h, why, out in [
        ("Merge the San Francisco city file into county pay",
         "Smallest item here and it is a correctness fix on a live page, not a "
         "feature. It also fills the largest hole in the Bay Area picture "
         "before anything is built on top of that picture.",
         "One ETL change. No new pages."),
        ("<code>_dev/nonprofits.py</code> &mdash; statewide, region as a parameter",
         "The IRS extract and the ZCTA crosswalk, reduced to a committed data "
         "module. Substance-use and non-service organizations separated rather "
         "than dropped, because an associate looking at a substance-use agency "
         "should know that is what it is.",
         "One data module. Nothing published yet, so nothing to get wrong in "
         "public."),
        ("Domain verification, then <code>practicum-sites-bay-area.html</code>",
         "Every candidate URL fetched before it ships as a link, exactly as "
         "the 218 health centers were. The trainee page first because it is "
         "the smaller universe, the higher-confidence one, and the reader with "
         "the least help available anywhere else.",
         "One page. The five program clinics lead it."),
        ("<code>how-to-find-a-practicum-site-california.html</code>",
         "The method page. Statewide, not regional &mdash; the questions to "
         "ask and what the school owes you do not change by county, and this "
         "is the page that would rank.",
         "One page, statewide, no new data."),
        ("<code>associate-employers-bay-area.html</code>",
         "The larger universe, and the honest hole in it. Leads with the "
         "county and safety-net employers where the site already knows what "
         "the work pays, and says plainly that private practices are missing "
         "and why.",
         "One page, linked from the hiring and county pay pages."),
        ("About 22 organization profiles",
         "Only the ones over $5m, only where there is something to write. "
         "Leaf-flagged. Stop when the writing stops being worth reading rather "
         "than when the list runs out.",
         "~22 leaf pages behind two directories."),
        ("Los Angeles, as the test of the parameter",
         "831 health-center sites against the Bay Area&rsquo;s 517. If the "
         "second region is a configuration entry and a week of editorial work, "
         "the build was right; if it is a rewrite, it was not.",
         "Two more pages, no new machinery."),
    ]:
        o.append('<li><h4>%s</h4><p class="why">%s</p>'
                 '<span class="out">%s</span></li>' % (h, why, out))
    o.append("</ol>")
    o.append('<p class="src">Net new: <b>5 pages plus about 22 profiles</b> for '
             "the Bay Area, one correctness fix, and one new ETL. Everything "
             "else is a filter over data this site already holds and has "
             "already verified.</p>")

    o.append('<div class="card"><h3>Sources for everything counted above</h3>'
             '<ol class="src">'
             '<li><a href="%s" rel="nofollow noopener" target="_blank">IRS '
             "Exempt Organizations Business Master File</a> &mdash; California "
             "extract, read 11 August 2026</li>"
             '<li><a href="%s" rel="nofollow noopener" target="_blank">HRSA '
             "data downloads</a> &mdash; Health Center Service Delivery Sites"
             "</li>"
             "<li><b>Census ZCTA to county relationship file, 2020</b> &mdash; "
             "used to map ZIP to county, largest-land-area match</li>"
             '<li><a href="%s" rel="nofollow noopener" target="_blank">'
             "Government Compensation in California</a> &mdash; the State "
             "Controller&rsquo;s county files, for the two defects in section "
             "07</li>"
             '<li><a href="%s" rel="nofollow noopener" target="_blank">'
             "&sect;&thinsp;4980.43.3</a> &mdash; which settings a trainee and "
             "an associate may each work in</li>"
             '<li><a href="%s" rel="nofollow noopener" target="_blank">'
             "&sect;&thinsp;4980.42</a> &mdash; the school&rsquo;s duty to "
             "approve the site and hold the agreement</li>"
             "</ol></div>" % (IRS, HRSA, SCO, LEG % "4980.43.3", LEG % "4980.42"))
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "%s. Counts were produced by a feasibility probe on that date and "
             "are transcribed here rather than recomputed at build time; if "
             "this is approved they become a committed data module. Companion "
             'to <a href="stage-architecture.html">the stage-architecture '
             'proposal</a> and <a href="stage-doors.html">the door designs</a>. '
             "<b>Nothing here is live, and no organization named on this page "
             "has said anything about taking trainees.</b></p></div></footer>"
             % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("bay area directories - feasibility")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes" % (os.path.basename(OUT),
                                        format(len(html), ",d")))

    bad = 0
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, which is not on the page" % h)
            bad += 1
    # The whole document turns on two claims. Losing either would leave a
    # proposal that reads as a simple yes.
    for needle, what in [
        ("shall not perform services in a private practice",
         "the trainee/associate split is not stated") if False else
        ("Not eligible &mdash; at all", "the trainee exclusion is not in the table"),
        ("Group private practices", "the unreachable category is not named"),
        ("May not be published", "the claims limit is missing"),
        ("wrong number wearing a county", "the Contra Costa defect is missing"),
        ("consolidated city-county", "the San Francisco defect is missing"),
    ]:
        if needle not in html:
            print("GUARD: %s" % what)
            bad += 1
    # It must never read as though availability had been checked - but the
    # "may not be published" list quotes those exact phrases in order to ban
    # them, so that block is cut out before the check runs. A guard that fires
    # on its own prohibition gets switched off, which is worse than no guard.
    body = re.sub(r'<div class="may">[\s\S]*?</div></div>', " ", html)
    for phrase in ("takes trainees</", "accepting trainees", "has openings",
                   "is hiring</"):
        if phrase in body:
            print("GUARD: the page appears to claim availability: %r" % phrase)
            bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: this is a working document and must not be indexable")
        bad += 1
    if str(N_CLINICAL) not in html or str(HC_SITES) not in html:
        print("GUARD: the two headline counts are not both on the page")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d jump targets, %d universes counted" % (len(NAV), 5))


if __name__ == "__main__":
    main()
