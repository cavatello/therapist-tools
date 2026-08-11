#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The named employers behind the safety-net category, with checked links.

WHY THIS EXISTS

`loan-forgiveness-employers-california.html` explains that MBH-SLRP pays
associate-level practitioners up to $180,000 and that the service obligation
has to be completed in a Medi-Cal safety-net setting. The obvious next question
is: name them.

Three of the four qualifying setting categories cannot be enumerated from
public data. The fourth can, completely: HRSA publishes every federally
designated health center site in the country, and California has 3,038 active
ones run by about 218 organizations.

THE HONESTY PROBLEM THIS PAGE HAS TO SOLVE

A list like this is read as "these employers will get you $180,000", and it
cannot mean that. It is a list of ORGANIZATIONS operating sites in one of the
qualifying categories. It is not a list of employers who take part in the
program, not a list of open jobs, and not an eligibility determination. And
crucially, ABSENCE FROM IT MEANS NOTHING: community mental health centers,
rural health clinics, and any setting where 40% of the population is on
Medicaid or uninsured are all qualifying categories that are not in this file.

So the page says all of that before it shows a single row, and the builder
guards that it keeps saying it.

THE LINKS

Every link was fetched before it shipped - see `_dev/hc_orgs.py`. The
organizations whose address in the federal file did not answer are listed with
NO link rather than a guessed one, and the page explains that this means the
check failed, not that the organization has no website.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import hc_orgs_data as hc
import hrsa_stats as hs

SITE = pk.SITE
PAGE = "medi-cal-safety-net-employers-california.html"
DONOR = "loan-forgiveness-employers-california.html"

FORGIVE = "loan-forgiveness-employers-california.html"
HIRED = "getting-hired-as-a-california-associate.html"
ATLAS = "therapists-by-county-california.html"
PAY = "associate-therapist-pay-los-angeles-bay-area.html"

MBH_ASSOCIATE = 180000
MBH_YEARS = 4
MEDICAID_SHARE = 40
RURAL_SHARE = 30
MBH_NEXT = "1 May 2027"

VERIFY_HCAI = "https://hcai.ca.gov/loans-scholarships-grants/eligibility/"
VERIFY_PSLF = "https://studentaid.gov/pslf/"
FINDER = "https://findahealthcenter.hrsa.gov/"

JUMPS = [("what", "What this is not"),
         ("twice", "Why they count twice"),
         ("list", "The 218"),
         ("sources", "Sources")]

# The four settings MBH-SLRP names. Only the first is enumerable from a public
# file, and saying so is the most important sentence on the page.
SETTINGS = [
    ("Federally qualified health centers, and look-alikes",
     "Yes &mdash; all %d organizations below" % len(hc.ORGS),
     "HRSA publishes every designated site in the country and updates the file "
     "daily."),
    ("Community mental health centers", "No",
     "There is no equivalent public list. Many are county-operated or "
     "county-contracted, and you find them through the county rather than "
     "through a federal file."),
    ("Rural health clinics", "Partly",
     "%d carry a live mental health shortage-area designation, but the "
     "designation file names facilities rather than employers."
     % hs.CA_MH_HPSA_BY_TYPE.get("Rural Health Clinic", 0)),
    ("Any setting at least %d%% Medicaid or uninsured &mdash; %d%% for rural "
     "hospitals" % (MEDICAID_SHARE, RURAL_SHARE), "No",
     "This is a fact about an employer&rsquo;s own patient mix. It is not "
     "published anywhere, and it is the category most likely to include the "
     "job you are actually looking at."),
]


def body():
    o = ['<article class="pk-wrap">']

    counties = sorted({c for r in hc.ORGS for c in r["counties"]})
    o.append(pk.hero(
        "Safety-net employers &middot; federal health center file read %s"
        % hc.CHECKED,
        "%d organizations. %s sites. And four things this list is not."
        % (len(hc.ORGS), format(hc.TOTAL_SITES, ",d")),
        "These are the California organizations running federally designated "
        "health center sites &mdash; one of the four settings that can carry "
        "an <b>MBH-SLRP</b> service obligation, and the only one that can be "
        "listed at all. <b>It is not a list of employers in the program, and "
        "not a list of jobs.</b>",
        [(str(len(hc.ORGS)), "organizations"),
         (format(hc.TOTAL_SITES, ",d"), "active sites"),
         (str(len(counties)), "counties covered"),
         (str(hc.LINKED), "links checked before shipping")],
        JUMPS))

    # ------------------------------------------------------- the loud warning
    o.append('<section class="pk-sec">')
    o.append(pk.callout(
        "Read this before you read the list",
        ["This is a list of <b>organizations operating federally designated "
         "health center sites in California</b>, taken from HRSA&rsquo;s bulk "
         "file on the date in the hero. That is all it is.",
         "<b>It is not a list of employers who take part in the loan "
         "repayment program.</b> Participation is not a public fact, the award "
         "is applied for by you rather than by the employer, and no employer "
         "on this list has told anyone it will support an application. <b>It "
         "is not a list of open jobs</b>, and it is <b>not an eligibility "
         "determination</b>.",
         "<b>Absence from this list means nothing.</b> Three of the four "
         "qualifying setting categories cannot be listed from public data at "
         "all &mdash; including the broadest one, which is any setting where "
         "at least %d%% of the population is on Medicaid or uninsured. The job "
         "you are looking at may well qualify and not be here."
         % MEDICAID_SHARE,
         "<b>And none of it can be guaranteed current.</b> Sites open and "
         "close, organizations merge, and the federal file changes daily. "
         'Verify with <a href="%s" rel="nofollow noopener" target="_blank">'
         "HCAI&rsquo;s own eligibility checker</a> and with the employer "
         "before you act on anything here."
         % VERIFY_HCAI],
        big="A list of organizations. Not of jobs, and not of eligibility."))
    o.append("</section>")

    # ------------------------------------------------------------ what it is
    o.append('<section class="pk-sec" id="what">')
    o.append('<p class="pk-k">The four settings</p>')
    o.append('<h2 class="pk-h">One of them is public. Three are not.</h2>')
    o.append('<p class="pk-d">MBH-SLRP names four kinds of setting where the '
             "%d-year service obligation can be completed. This page can "
             "enumerate exactly one of them, and the honest thing is to show "
             "you which.</p>" % MBH_YEARS)
    o.append(pk.table(
        ["Qualifying setting", "Listed here?", "Why, or why not"],
        [[a, (b, "m"), c] for a, b, c in SETTINGS],
        caption="Which is why this page is a starting point and not an "
                "answer. If the job you are considering is not on the list, "
                "the question to ask the employer is whether their patient "
                "mix crosses the Medicaid threshold &mdash; not whether they "
                "appear in a federal file.",
        minw=660))
    o.append("</section>")

    # ----------------------------------------------------------- twice over
    o.append('<section class="pk-sec" id="twice">')
    o.append('<p class="pk-k">Why these employers are worth knowing</p>')
    o.append('<h2 class="pk-h">A health center can matter to you twice.</h2>')
    o.append(pk.numbered([
        ("1", "As an MBH-SLRP setting.",
         "A federally qualified health center is named in the program&rsquo;s "
         "own list of safety-net settings, and the associate-level tier of "
         "that program goes up to $%s over %d years. The next application "
         "window opens %s."
         % (format(MBH_ASSOCIATE, ",d"), MBH_YEARS, MBH_NEXT)),
        ("2", "As a PSLF employer.",
         "Health center program awardees are public entities or private "
         "non-profits, which is the shape PSLF&rsquo;s employer definition "
         "asks for &mdash; and PSLF asks nothing about your license. Several "
         "organizations on this list are counties outright. That does not "
         'make any of them qualifying: run the employer through <a href="%s" '
         'rel="nofollow noopener" target="_blank">the federal employer '
         "search</a> and certify, rather than assuming from a category."
         % VERIFY_PSLF),
        ("3", "And, separately, as somewhere that can bill for your work.",
         "The billing question is the one that decides whether an associate "
         'gets hired at all, and it is <a href="%s">answered on its own '
         "page</a>. The three questions overlap heavily, which is why the same "
         "handful of settings keeps appearing in all three answers."
         % HIRED),
    ]))
    o.append("</section>")

    # ------------------------------------------------------------- the list
    o.append('<section class="pk-sec" id="list">')
    o.append('<p class="pk-k">The directory</p>')
    o.append('<h2 class="pk-h">All %d, by name.</h2>' % len(hc.ORGS))
    o.append('<p class="pk-d">Every link below was fetched before it was '
             "published. %d answered. The %d that did not are shown without a "
             "link &mdash; that means the check failed, <b>not</b> that the "
             "organization has no website, and several of them are simply "
             "behind bot protection. A wrong link is worse than no link.</p>"
             % (hc.LINKED, hc.UNLINKED))

    rows = []
    for r in hc.ORGS:
        name = pk.esc(r["name"])
        cell = ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
                % (r["url"], name)) if r["url"] else "<b>%s</b>" % name
        cos = ", ".join(r["counties"][:4])
        if len(r["counties"]) > 4:
            cos += " and %d more" % (len(r["counties"]) - 4)
        rows.append([cell, (format(r["sites"], ",d"), "f"), cos,
                     ("Look-alike" if r["lookalike"] else "FQHC", "m")])
    o.append(pk.table(
        ["Organization", "Sites", "Counties", "Type"], rows,
        caption="Organizations running an active health center service "
                "delivery or look-alike site in California, aggregated from "
                "HRSA&rsquo;s site-level file read %s. A look-alike meets the "
                "health center program requirements without receiving the "
                "grant funding; both are named settings for the state "
                "program. Site counts include administrative locations."
                % hc.CHECKED,
        minw=700))
    o.append('<p class="pk-p">To search by address rather than by employer, '
             'HRSA runs <a href="%s" rel="nofollow noopener" target="_blank">a '
             "health center finder</a> over the same data. How crowded each "
             'county already is with therapists is on <a href="%s">the county '
             "atlas</a>, and what associate roles in these settings pay is on "
             '<a href="%s">the pay page</a>.</p>' % (FINDER, ATLAS, PAY))
    o.append("</section>")

    # ------------------------------------------------------------- sources
    src, n = pk.sources([
        ("The list", [
            ("HRSA Data Downloads &mdash; Health Center Program service "
             "delivery and look-alike sites, read %s, aggregated to "
             "organizations by _dev/hc_orgs.py with every link fetched before "
             "publication" % hc.CHECKED,
             "https://data.hrsa.gov/data/download"),
            ("Find a Health Center &mdash; HRSA&rsquo;s own search over the "
             "same data", FINDER),
        ]),
        ("The program the list is for", [
            ("Medi-Cal Behavioral Health Student Loan Repayment Program "
             "&mdash; the safety-net setting categories and the "
             "associate-level tier",
             "https://hcai.ca.gov/workforce/initiatives/"
             "behavioral-health-bh-connect/mbhslrp/"),
            ("HCAI eligibility quiz &mdash; the state&rsquo;s own checker, "
             "which is the thing to use rather than this page", VERIFY_HCAI),
            ("Federal Student Aid &mdash; PSLF and its employer search",
             VERIFY_PSLF),
        ]),
    ], note="<b>This page lists organizations, not jobs, and not eligibility.</b> "
            "No employer here has said it will support a loan repayment "
            "application, absence from the list does not mean a setting fails "
            "to qualify, and the federal file behind it changes daily. "
            "<b>Verify with the program and with the employer before you act.</b> "
            "Nothing here is legal, financial or career advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), n


META = pk.meta_block(
    PAGE,
    "Medi-Cal safety-net employers in California: the health centers, named",
    "The %d California organizations running federally designated health "
    "center sites - one of the four settings that can carry an MBH-SLRP "
    "obligation. Organizations, not jobs." % len(hc.ORGS),
    "licensure", "reference",
    "Which California employers are in the Medi-Cal safety net?",
    "All %d health center organizations by name, with sites, counties and "
    "links that were checked before publication" % len(hc.ORGS),
    "%d organizations, %s sites" % (len(hc.ORGS), format(hc.TOTAL_SITES, ",d")),
    weight=4)


def main():
    print("Medi-Cal safety-net employers")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d orgs, %d linked, %d sources"
          % (PAGE, format(len(html), ",d"), len(hc.ORGS), hc.LINKED, nsrc))

    bad = pk.check_page(p, [
        ("the not-a-job-list warning", "not a list of open jobs"),
        ("the absence-means-nothing warning", "Absence from this list means "
                                              "nothing"),
        ("the unchecked-link explanation", "the check failed"),
        ("the four-settings table", "Medicaid or uninsured"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every organization has to appear. A row silently dropped from a
    # directory reads as "this employer is not in the safety net".
    missing = [r["name"] for r in hc.ORGS if pk.esc(r["name"]) not in art]
    if missing:
        print("GUARD: %d organization(s) missing from the table, first: %s"
              % (len(missing), missing[0]))
        bad += 1

    # Only checked links may ship. If a row without a verified URL has somehow
    # acquired an anchor, the page is asserting something nobody verified.
    import re as _re
    anchors = len(_re.findall(r'<a href="https?://[^"]+" rel="nofollow noopener" '
                              r'target="_blank">', art))
    if anchors < hc.LINKED:
        print("GUARD: %d checked links but only %d anchors in the article"
              % (hc.LINKED, anchors))
        bad += 1

    # The four warnings are the page's license to exist. Guarded individually.
    for what, needle in (
            ("the hero caveat", "not a list of employers in the program"),
            ("the panel", "A list of organizations. Not of jobs, and not of "
                          "eligibility."),
            ("the participation caveat", "Participation is not a public fact"),
            ("the currency caveat", "none of it can be guaranteed current"),
            ("the sources note", "Verify with the program and with the "
                                 "employer before you act.")):
        if needle not in s:
            print("GUARD: %s is missing (%s)" % (what, needle[:44]))
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
