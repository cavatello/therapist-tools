#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3, page one: where a Bay Area MFT trainee can actually be placed.

THE SPLIT THAT DEFINES THIS PAGE (ops/bay-area-directories.html, approved
13 Aug 2026): a trainee and an associate have different legal universes, one
strictly inside the other, so the Bay Area work is TWO directories. This is
the trainee one. BPC 4980.43.3(b) bars a trainee from private practice and
professional corporations entirely, which means the one category no public
dataset can enumerate - group private practices - costs THIS page nothing.
The associate page, where that absence is a real hole, is built separately
and must state it in the first screen.

WHAT MAY BE CLAIMED, AND WHAT MAY NOT. Everything here describes what an
organization IS: that it exists, which universe it belongs to under the
statute, its county, its size band from reported revenue, a link fetched
before publication. Nothing here says whether anyone HAS A SEAT. The words
are banned by the guard at the bottom, the same discipline the portals and
loan-forgiveness pages run under: a wrong "yes" costs a student an
application cycle at the moment they have least slack.

THE FOUR SOURCED UNIVERSES (all trainee-eligible):
  - the five program training clinics, from the site's own 78-program file -
    the only rows where taking students is certain, because it is what a
    training clinic is for
  - the nine county behavioral health plans, already fetched and published
    in the safety-net and portals work
  - the health-center organizations operating Bay Area sites, from HRSA via
    _dev/hc_orgs.py, links already fetched
  - the nonprofit clinical organizations, from the IRS master file via
    _dev/nonprofits.py; the largest carry links that were fetched, the rest
    publish unlinked rather than guessed

Chrome borrows from the safety-net page's donor chain (pagekit), so this
page joins the pagekit family and converts with it at rollout step 5.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import nonprofit_data as nd
import hc_orgs_data as hc
import county_bh_data as cb
import practicum_data as pdta

SITE = pk.SITE
PAGE = "practicum-sites-bay-area.html"
DONOR = "loan-forgiveness-employers-california.html"

PRACTICUM = "practicum-california-mft-trainee.html"
SAFETYNET = "medi-cal-safety-net-employers-california.html"
PORTALS = "county-job-portals-california.html"
SUPERVISOR = "finding-a-clinical-supervisor-california.html"
NINETY = "bbs-90-day-rule-california.html"

LEG = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
       "?sectionNum=%s.&lawCode=BPC")

# The five Bay Area programs that run their own training clinics. Pinned by
# institution name against the practicum file rather than parsed from city
# strings - the city field carries parentheticals that defeat parsing, and a
# pinned list fails loudly in the guard if the file drops one.
CLINIC_PROGRAMS = [
    "California Institute of Integral Studies",
    "California State University, East Bay",
    "Kaiser Permanente School of Allied Health Sciences",
    "Palo Alto University",
    "University of San Francisco",
]

BAY = nd.BAY_COUNTIES


def bay_programs():
    out = []
    for want in CLINIC_PROGRAMS:
        hit = [p for p in pdta.PROGRAMS if p["inst"] == want]
        if len(hit) != 1 or not hit[0].get("own_clinic"):
            sys.exit("build_baysites: %r is not a clinic program in the "
                     "practicum file any more - re-check the pinned list"
                     % want)
        out.append(hit[0])
    return out


def bay_hc():
    return sorted((o for o in hc.ORGS
                   if any(c in BAY for c in o["counties"])),
                  key=lambda o: -o["sites"])


def bay_plans():
    return [p for p in cb.PLANS if p["county"].split(",")[0] in BAY]


def bay_nonprofits():
    return [o for o in nd.ORGS
            if o["county"] in BAY and o["bucket"] == "clinical"]


def band(rev):
    if rev >= 5_000_000:
        return "over $5m"
    if rev >= 1_000_000:
        return "$1m&ndash;$5m"
    if rev > 0:
        return "under $1m"
    return "none reported"


JUMPS = [("rules", "The three rules"),
         ("clinics", "The five program clinics"),
         ("counties", "The nine county plans"),
         ("centers", "The health centers"),
         ("nonprofits", "The nonprofit organizations"),
         ("ask", "How to ask"),
         ("sources", "Sources")]


def body():
    progs = bay_programs()
    hcs = bay_hc()
    plans = bay_plans()
    nps = bay_nonprofits()
    linked_np = sum(1 for o in nps if o.get("url"))
    n_clinics = sum(len(p["clinics"] or []) for p in progs)

    o = ['<article class="pk-wrap">']
    o.append(pk.hero(
        "Bay Area &middot; the practicum year &middot; data read %s"
        % nd.CHECKED,
        "Where a Bay Area trainee can lawfully be placed.",
        "The %d organizations across nine counties that are the kind of "
        "setting the code allows a trainee to work in: %d program training "
        "clinics, %d county behavioral health plans, %d health-center "
        "organizations and %d nonprofit clinical agencies. <b>This page "
        "answers what a setting is, never whether it has a seat</b> &mdash; "
        "no public source says who is taking students, and a directory that "
        "guesses costs you an application cycle."
        % (len(progs) + len(plans) + len(hcs) + len(nps),
           len(progs), len(plans), len(hcs), len(nps)),
        [(str(n_clinics), "clinics run by the five programs"),
         (str(len(plans)), "county behavioral health plans"),
         (str(len(hcs)), "health-center organizations"),
         (str(len(nps)), "nonprofit clinical agencies")],
        JUMPS))

    # ------------------------------------------------------- the loud warning
    o.append('<section class="pk-sec">')
    o.append(pk.callout(
        "Read this before you read the lists",
        ["Every row below is an organization that <b>exists and is the kind "
         "of setting a trainee may work in</b> under the statute. That is "
         "the entire claim. Nothing here says a setting takes students this "
         "year, runs a training program, or has anyone to supervise you "
         "&mdash; no public dataset records any of that, and this site does "
         "not print what it cannot check.",
         "What the page can do is stop you spending an application cycle on "
         "the one category the law rules out: <b>a trainee may not work in "
         "a private practice or a professional corporation at all</b>, and "
         "may never work as an independent contractor anywhere. Roughly "
         "half of the informal advice a Bay Area student gets &mdash; "
         "&ldquo;ask around, somebody&rsquo;s supervisor has room&rdquo; "
         "&mdash; points at exactly those settings.",
         "Your program also cannot simply send you anywhere on this page: "
         "the school must approve the site and hold a <b>written agreement</b> "
         "with it before your hours there can count. That rule is the "
         "single most useful sentence to carry into any conversation below, "
         "and it puts the site agreement on the school, not on you."],
        big="A list of settings the code allows. Not of openings."))
    o.append("</section>")

    # --------------------------------------------------------- the three rules
    o.append('<section class="pk-sec" id="rules">')
    o.append('<p class="pk-k">The statute, in three rows</p>')
    o.append('<h2 class="pk-h">What decides whether a setting can hold a '
             "trainee at all.</h2>")
    o.append(pk.table(
        ["The rule", "Where it is written", "What it means here"],
        [["A trainee works as an employee or a volunteer, never as an "
          "independent contractor",
          '<a href="%s" target="_blank" rel="noopener noreferrer">'
          "BPC &sect;4980.43.3(a)</a>" % (LEG % "4980.43.3"),
          "Any setting offering a 1099 arrangement is offering something "
          "the Board will not count"],
         ["A trainee may not work in a private practice or a professional "
          "corporation, at all",
          '<a href="%s" target="_blank" rel="noopener noreferrer">'
          "BPC &sect;4980.43.3(b)</a>" % (LEG % "4980.43.3"),
          "This is why group practices are absent below &mdash; for a "
          "trainee the absence costs nothing, because the category is "
          "closed anyway"],
         ["The school approves each site and holds a written agreement "
          "with it",
          '<a href="%s" target="_blank" rel="noopener noreferrer">'
          "BPC &sect;4980.42(e)</a>" % (LEG % "4980.42"),
          "Before investing in any conversation, ask your program who "
          "signs the site agreement and how long approval takes"]],
        caption="The trainee rules in full, including the practicum "
                'enrollment requirement and the 90-day lapse trap, are on '
                '<a href="%s">the practicum page</a>.' % PRACTICUM,
        minw=660))
    o.append("</section>")

    # ------------------------------------------------------------ the clinics
    o.append('<section class="pk-sec" id="clinics">')
    o.append('<p class="pk-k">Universe one &middot; the sure thing</p>')
    o.append('<h2 class="pk-h">The five programs that run their own '
             "clinics.</h2>")
    o.append('<p class="pk-d">A program training clinic exists to train '
             "students &mdash; these are the only rows on this page where "
             "that purpose is certain rather than possible. Several also "
             "take trainees from other schools; the clinic&rsquo;s own page "
             "says whether, and your program&rsquo;s approval is still "
             "required either way.</p>")
    rows = []
    for p in bay_programs():
        cl = p["clinics"] or []
        rows.append([
            '<a href="%s">%s</a>' % (p["page"], pk.esc(p["inst"]))
            if p.get("page") else pk.esc(p["inst"]),
            pk.esc(p["city"]),
            "; ".join(pk.esc(c) for c in cl) or "&mdash;",
        ])
    o.append(pk.table(["Program", "Where", "Its clinics"], rows, minw=620))
    o.append("</section>")

    # ------------------------------------------------------------- the plans
    o.append('<section class="pk-sec" id="counties">')
    o.append('<p class="pk-k">Universe two &middot; the public system</p>')
    o.append('<h2 class="pk-h">The nine county behavioral health plans.</h2>')
    o.append('<p class="pk-d">Every Bay Area county runs a behavioral health '
             "department, and each one is both a large clinical employer and "
             "the contractor behind many of the nonprofits further down. "
             "These nine links were fetched and corrected as part of the "
             '<a href="%s">statewide safety-net directory</a>; the county '
             'application forms live on <a href="%s">the county job portals '
             "page</a>.</p>" % (SAFETYNET, PORTALS))
    rows = []
    for p in bay_plans():
        nm = pk.esc(p["county"])
        rows.append([
            '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
            % (p["url"], nm) if p.get("url") else nm,
            "county behavioral health plan",
        ])
    o.append(pk.table(["County", "What it is"], rows, minw=480))
    o.append("</section>")

    # ------------------------------------------------------------ the centers
    o.append('<section class="pk-sec" id="centers">')
    o.append('<p class="pk-k">Universe three &middot; the federal file</p>')
    o.append('<h2 class="pk-h">The %d organizations running Bay Area '
             "health-center sites.</h2>" % len(hcs))
    o.append('<p class="pk-d">Federally designated health centers and '
             "look-alikes with service-delivery sites in the nine counties, "
             "from HRSA&rsquo;s bulk file. Site counts are statewide for "
             "each organization; a row without a link means the address in "
             "the federal file did not answer when checked, <b>not</b> that "
             "the organization has no website.</p>")
    rows = []
    for r in hcs:
        nm = pk.esc(r["name"])
        bayc = sorted(c for c in set(r["counties"]) if c in BAY)
        rows.append([
            '<a href="https://%s" target="_blank" rel="noopener noreferrer">'
            "%s</a>" % (r["url"], nm) if r.get("url") else nm,
            ", ".join(bayc),
            (format(r["sites"], ",d"), "n"),
        ])
    o.append(pk.table(["Organization", "Bay Area counties", "Sites, statewide"],
                      rows, minw=620))
    o.append("</section>")

    # --------------------------------------------------------- the nonprofits
    o.append('<section class="pk-sec" id="nonprofits">')
    o.append('<p class="pk-k">Universe four &middot; the long list</p>')
    o.append('<h2 class="pk-h">The %d nonprofit clinical organizations.</h2>'
             % len(nps))
    o.append('<p class="pk-d">Every active IRS-registered nonprofit in the '
             "nine counties whose activity code is clinical mental health "
             "&mdash; treatment, community mental health, residential, "
             "crisis, counseling. The code is self-reported, so treat a row "
             "as a lead to check rather than a certification. Size is "
             "reported revenue: an organization reporting none is usually "
             "small or newly filed rather than inactive. The %d largest "
             "carry links that were fetched before publication; the rest "
             "publish unlinked rather than guessed. A further %d "
             "substance-use treatment organizations are a real clinical "
             "system too, and are deliberately not mixed into this table."
             % (linked_np, nd.BAY_BY_BUCKET["substance"]))
    rows = []
    for np_ in nps:
        nm = pk.esc(np_["name"])
        rows.append([
            '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
            % (np_["url"], nm) if np_.get("url") else nm,
            pk.esc(np_["city"] or "&mdash;"),
            np_["county"],
            (band(np_["revenue"]), "m"),
        ])
    o.append(pk.table(["Organization", "City", "County", "Size, by revenue"],
                      rows,
                      caption="From the IRS Exempt Organizations master "
                              "file, California extract, NTEE F30&ndash;F79 "
                              "and F99, mapped to county through the Census "
                              "ZCTA relationship file. Read %s."
                              % nd.CHECKED,
                      minw=640))
    o.append("</section>")

    # ---------------------------------------------------------------- how to
    o.append('<section class="pk-sec" id="ask">')
    o.append('<p class="pk-k">What to do with a list this size</p>')
    o.append('<h2 class="pk-h">How to ask, in the order that saves you '
             "cycles.</h2>")
    o.append(pk.numbered([
        ("1", "Start from your program's approved-site list, not from "
              "this page.",
         "Your school already holds signed agreements with some of these "
         "organizations, and a site on that list is weeks closer than an "
         "identical site off it. This page is for reading the market and "
         "for finding names your program has not thought of &mdash; in "
         "that order."),
        ("2", "For a new site, ask your program two questions before "
              "contacting anyone.",
         "Who signs the site agreement, and how long does approval take? "
         "&sect;4980.42(e) puts the agreement on the school. If approval "
         "takes a term, a site approved today is a spring placement, not "
         "a fall one."),
        ("3", "Ask the organization what it is, not whether it wants you.",
         "Whether clinical staff include pre-licensed trainees, whether "
         "supervision meets the Board&rsquo;s form, and who the training "
         "contact is. An organization that has never held a trainee can "
         "still become a site &mdash; that is what the written agreement "
         "is for."),
        ("4", "If you will stay after graduating, read the 90-day rule "
              "before your last term.",
         'The employer&rsquo;s Live Scan has to be stamped before '
         "post-degree hours start counting, and the whole trap is "
         'avoidable while you are still enrolled. <a href="%s">The '
         "90-day rule page</a> walks the four conditions." % NINETY),
    ]))
    o.append("</section>")

    # ---------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The statutes", [
            ("BPC &sect;4980.43.3 &mdash; employee or volunteer only; no "
             "private practice or professional corporation for trainees",
             LEG % "4980.43.3"),
            ("BPC &sect;4980.42 &mdash; practicum enrollment, and the "
             "school&rsquo;s written agreement with each site",
             LEG % "4980.42"),
        ]),
        ("The data", [
            ("IRS Exempt Organizations Business Master File, California "
             "extract &mdash; the nonprofit universe, reduced by "
             "_dev/nonprofits.py with the classification rule documented "
             "in the pass", "https://www.irs.gov/charities-non-profits/"
             "exempt-organizations-business-master-file-extract-eo-bmf"),
            ("Census 2020 ZCTA-to-county relationship file &mdash; the "
             "ZIP-to-county mapping",
             "https://www.census.gov/geographies/reference-files/"
             "time-series/geo/relationship-files.html"),
            ("HRSA Data Downloads &mdash; health center service delivery "
             "sites, aggregated by _dev/hc_orgs.py with every link fetched "
             "before publication", "https://data.hrsa.gov/data/download"),
            ("The site&rsquo;s own 78-program practicum research file "
             "&mdash; the program clinics", PRACTICUM),
        ]),
    ], note="<b>This page lists settings, not openings.</b> No organization "
            "here has said it takes students, supervision availability is "
            "not a public fact, and the federal and IRS files behind the "
            "tables change monthly. Your program&rsquo;s approval and a "
            "written agreement are required before any hours count "
            "anywhere on this page. Nothing here is legal or career advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "Bay Area practicum sites: where an MFT trainee can be placed",
    "The Bay Area settings a trainee may lawfully work in: 5 program "
    "clinics, 9 county plans, and the health centers and nonprofit clinical "
    "agencies, named.",
    "licensure", "reference",
    "Where can a Bay Area trainee actually do practicum hours?",
    "Every trainee-eligible setting the public files can name, across nine "
    "counties, with the statutory rules that define the list",
    "5 program clinics, 9 county plans",
    weight=4)

# Availability language is banned as a claim this page could never keep
# current. Same rule as the portals page. Checked against the rendered
# article text, lowercased.
BANNED = ["is hiring", "now hiring", "has openings", "open positions",
          "vacanc", "accepting applications", "accepting trainees",
          "takes trainees", "taking trainees", "accepting students",
          "spots available", "positions available", "apply now",
          "currently accepting"]


def main():
    html_body, n_sources = body()
    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)

    s = open(p, encoding="utf-8").read()
    problems = pk.check_page(p, [
        ("the 4980.43.3 citation", "4980.43.3"),
        ("the 4980.42 citation", "4980.42"),
        ("the private-practice exclusion", "private practice"),
        ("the site-agreement sentence", "written agreement"),
        ("the not-of-openings verdict", "Not of openings"),
        ("the unlinked-row explanation", "did not answer when checked"),
    ], [j for j, _ in JUMPS])

    bad = []
    art = pk.article(s).lower()
    for phrase in BANNED:
        if phrase in art:
            bad.append("availability language: %r" % phrase)

    # every organization present, by name
    for np_ in bay_nonprofits():
        if pk.esc(np_["name"]) not in s:
            bad.append("nonprofit missing: %s" % np_["name"]); break
    for r in bay_hc():
        if pk.esc(r["name"]) not in s:
            bad.append("health center missing: %s" % r["name"]); break
    if len(bay_plans()) != 9:
        bad.append("expected 9 bay plans, found %d" % len(bay_plans()))

    if bad or problems:
        for b in bad:
            print("GUARD %s: %s" % (PAGE, b))
        sys.exit(1)
    print("build_baysites: %s written - %d nonprofits, %d health centers, "
          "9 plans, 5 clinic programs, %d sources"
          % (PAGE, len(bay_nonprofits()), len(bay_hc()), n_sources))


if __name__ == "__main__":
    main()
