#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Where to apply for a county therapy job, in all 58 California counties.

WHY THIS PAGE EXISTS

Four pages on this site point at the county job and none of them says where
the form is. The hiring page explains why a county is one of the few employers
that can lawfully bill for a pre-licensed clinician. The county pay page says
what the work pays, across 51 counties. The safety-net directory names the 57
behavioral health plans. The loan-forgiveness page says a county is a
government employer, so PSLF asks nothing further.

Then the reader has to go and find the application portal themselves, and for
eight of the fifty-eight that goes wrong in a way they will not notice.

THE FINDING

Guessing the URL fails silently. `governmentjobs.com/careers/marin` is the
Marin County Superior Court. `/sandiego` and `/santabarbara` are the cities.
`/santacruz` is a city portal. `/alameda`, `/countyofmonterey` and `/trinity`
are unbranded, empty tenants, and all three counties have a real portal at a
different address - Alameda is not on NeoGov at all.

Every one of those loads, looks right, and is somebody else.

WHY A PORTAL DIRECTORY RATHER THAN A JOB BOARD

A posting expires in six weeks; a portal does not. The site already decided
against a job archive for exactly this reason. This page is an address book
with a verification record attached, which is the part that keeps working.

WHAT IT MUST NOT SAY

Nothing about whether a county is hiring, and nothing about what a listing
pays - the pay page is next door and says it from payroll data rather than
from a posting. A guard below fails the build on availability language, the
same way the loan-forgiveness page bans verdict words.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import county_portals_data as cpd
import county_pay_data as cp

SITE = pk.SITE
PAGE = "county-job-portals-california.html"
DONOR = "county-therapist-pay-california.html"

PAY = "county-therapist-pay-california.html"
HIRED = "getting-hired-as-a-california-associate.html"
EMPLOYERS = "medi-cal-safety-net-employers-california.html"
FORGIVE = "loan-forgiveness-employers-california.html"
MBH = "mbh-slrp-california.html"
ATLAS = "therapists-by-county-california.html"
ASSOCPAY = "associate-therapist-pay-los-angeles-bay-area.html"
PRACTICUM = "practicum-california-mft-trainee.html"

JUMPS = [("wrong", "The eight that trick you"),
         ("systems", "Four systems, 58 counties"),
         ("table", "Every county"),
         ("method", "How each was checked"),
         ("sources", "Sources")]

N = len(cpd.PORTALS)
NWRONG = len(cpd.WRONG_GUESS)
NEOGOV = cpd.COUNTS.get("neogov", 0)


def body():
    o = ['<article class="pk-wrap">']

    o.append(pk.hero(
        "County job portals &middot; all %d counties &middot; every link "
        "fetched %s" % (N, cpd.CHECKED),
        "For eight California counties, the job portal you would guess "
        "belongs to somebody else.",
        "Where the application form actually is, county by county &mdash; with "
        "the wording on each destination that proves it belongs to the county "
        "rather than to a city or a court.",
        [(str(N), "counties, all verified"),
         (str(NWRONG), "guessable URLs are wrong"),
         (str(NEOGOV), "share one system"),
         (str(len(cpd.COUNTS)), "systems in total")],
        JUMPS))

    # ----------------------------------------------------------------- wrong
    o.append('<section class="pk-sec" id="wrong">')
    o.append(pk.quote(
        "Why this page is not just a list of links",
        ["Every one of the addresses below loads a real, working, "
         "professional-looking job portal. None of them is the county.",
         "That is the failure mode worth publishing: a person applying for a "
         "county behavioral health post does not get a 404 and go looking. "
         "They get a page that looks exactly right, and they apply to the "
         "wrong employer &mdash; or to nobody, because three of these are "
         "empty shells."]))

    o.append('<p class="pk-k">The eight that trick you</p>')
    o.append('<h2 class="pk-h">The obvious URL, and what actually answers '
             "there.</h2>")
    rows = []
    for county, guess, what in cpd.WRONG_GUESS:
        real = [r for r in cpd.PORTALS if r["county"] == county][0]
        rows.append([("<b>%s</b>" % county),
                     ("<code>%s</code>" % guess, "m"),
                     what,
                     ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
                      % (real["url"], cpd.SYSTEM_NAME[real["system"]]))])
    o.append(pk.table(
        ["County", "What you would try", "What it actually is",
         "Where the county really is"], rows,
        caption="Marin, San Diego, Santa Barbara and Santa Cruz resolve to a "
                "different public employer of the same name. Alameda, Monterey "
                "and Trinity resolve to an unbranded tenant with no listings, "
                "and all three counties recruit somewhere else entirely.",
        minw=820))

    o.append(pk.callout(
        "The one worth saying out loud",
        ["<b>Alameda County is not on NeoGov.</b> It recruits through JobAps, "
         "and its human resources department links there as the only "
         "application route. The NeoGov address that carries its name has no "
         "listings and no class specifications at all.",
         "Alameda is the fourth-largest county workforce in the state and "
         'runs one of the largest behavioral health plans, so <a href="%s">the '
         "pay data</a> and <a href=\"%s\">the employer directory</a> both have "
         "a great deal to say about it. Getting to the application form is the "
         "step that breaks." % (PAY, EMPLOYERS)]))
    o.append("</section>")

    # --------------------------------------------------------------- systems
    o.append('<section class="pk-sec" id="systems">')
    o.append('<p class="pk-k">Four systems, %d counties</p>' % N)
    o.append('<h2 class="pk-h">%d of the %d share one system, which is worth '
             "knowing before you make %d accounts.</h2>" % (NEOGOV, N, N))
    o.append('<p class="pk-d">California counties do not run a common hiring '
             "platform, but they are close to it. One profile and one saved "
             "search covers most of the state; the rest have to be visited "
             "individually.</p>")

    rows = []
    for key in sorted(cpd.COUNTS, key=lambda k: -cpd.COUNTS[k]):
        names = sorted(r["county"] for r in cpd.PORTALS if r["system"] == key)
        rows.append([("<b>%s</b>" % cpd.SYSTEM_NAME[key]),
                     (str(cpd.COUNTS[key]), "f"),
                     ", ".join(names) if len(names) <= 12
                     else "%s and %d others" % (", ".join(names[:6]),
                                                len(names) - 6)])
    o.append(pk.table(["System", "Counties", "Which"], rows,
                      caption="One account on the largest system reaches "
                              "roughly four counties in five. It does not "
                              "reach the other ten, and nothing warns you of "
                              "that &mdash; a saved search simply never "
                              "returns their postings.",
                      minw=680))

    o.append('<p class="pk-p">This is the practical reason a portal directory '
             "beats a job board. A posting for a behavioral health clinician "
             "is gone in six weeks. The address it was posted at has been the "
             "same for years, and will be there the next time you look "
             "&mdash; which is also why "
             '<a href="%s">a job archive was decided against</a> on this '
             "site.</p>" % "changes.html")
    o.append("</section>")

    # ----------------------------------------------------------------- table
    o.append('<section class="pk-sec" id="table">')
    o.append('<p class="pk-k">Every county</p>')
    o.append('<h2 class="pk-h">All %d, with the proof attached.</h2>' % N)
    o.append('<p class="pk-d">The third column is the wording on the '
             "destination page that establishes it belongs to the county. It "
             "is there because for eight of these the obvious answer is wrong, "
             "and an assertion without evidence would not have caught "
             "them.</p>")

    paid = {r["county"]: r for r in cp.COUNTIES}
    rows = []
    for r in cpd.PORTALS:
        p = paid.get(r["county"])
        rows.append([
            ('<a href="%s" rel="nofollow noopener" target="_blank">%s</a>'
             % (r["url"], pk.esc(r["county"]))),
            (cpd.SYSTEM_NAME[r["system"]], "m"),
            pk.esc(r["evidence"]),
            (("$%s" % format(p["max_med"], ",d")) if p else "&mdash;", "f"),
            ((format(p["n"], ",d")) if p else "&mdash;", "m"),
        ])
    o.append(pk.table(
        ["County &mdash; links to its portal", "System",
         "What the destination calls itself", "Top of range",
         "Clinical posts"],
        rows,
        caption="Pay and headcount are the county&rsquo;s own returns to the "
                "State Controller for %s, from <a href=\"%s\">the county pay "
                "page</a>, and are blank where a county reported too few "
                "comparable positions to rank. <b>A portal here is an address, "
                "not a vacancy</b> &mdash; whether anything is open on the day "
                "you look is between you and the county."
                % (cp.YEARS[-1], PAY),
        minw=980))
    o.append("</section>")

    # ---------------------------------------------------------------- method
    o.append('<section class="pk-sec" id="method">')
    o.append('<p class="pk-k">How each one was checked</p>')
    o.append('<h2 class="pk-h">Two passes, which disagreed &mdash; and that is '
             "the reason for both.</h2>")
    o.append(pk.numbered([
        ("1", "Predictable addresses, kept only where the page named the county.",
         "Seven address patterns per county against the largest shared system. "
         "Anything whose own page title did not name the county was rejected "
         "rather than assumed. That produced 19 counties &mdash; and caught "
         "four addresses answering for a city or a court."),
        ("2", "The remaining counties, from their own human resources pages.",
         "Resolved by starting at each county&rsquo;s own site and following "
         "where it sends applicants, recording the exact wording that proves "
         "the destination is the county. This pass corrected three more that "
         "the first had accepted as plausible &mdash; unbranded tenants that "
         "answer, look normal, and hold nothing."),
        ("3", "Then every address was fetched.",
         "A California government site answering <b>403</b> to a script is "
         "working perfectly in a browser, so only a refused connection, a "
         "timeout, a DNS failure or an explicit 404 counts as broken. All %d "
         "answered. Ignoring that distinction reported 22 false deaths the "
         "last time this site checked a set of government links." % N),
    ]))

    o.append(pk.callout(
        "What this page deliberately does not tell you",
        ["Whether any county is hiring, and what any listing pays. Both change "
         "weekly and neither can be kept true.",
         'What the work actually pays comes from payroll rather than postings, '
         'on <a href="%s">the county pay page</a>. Why a county can employ '
         'someone who is not yet licensed is <a href="%s">a Medi-Cal billing '
         'rule</a>. What a county job is worth against loan repayment is '
         '<a href="%s">the forgiveness page</a>, and why a trainee cannot take '
         'just any placement is <a href="%s">the practicum page</a>.'
         % (PAY, HIRED, FORGIVE, PRACTICUM)]))
    o.append("</section>")

    # --------------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The portals", [
            ("All %d county portals, each fetched %s. The full list with the "
             "identifying wording is the table above." % (N, cpd.CHECKED),
             None),
        ]),
        ("Where the county job comes up elsewhere on this site", [
            ("What each county actually paid, from the State Controller's file",
             "https://therapistsupport.org/%s" % PAY),
            ("Why a county can bill for a pre-licensed clinician when most "
             "employers cannot", "https://therapistsupport.org/%s" % HIRED),
            ("The 57 county behavioral health plans, by name",
             "https://therapistsupport.org/%s" % EMPLOYERS),
            ("Which employers unlock loan forgiveness, and on what test",
             "https://therapistsupport.org/%s" % FORGIVE),
            ("How crowded each county already is with therapists",
             "https://therapistsupport.org/%s" % ATLAS),
        ]),
    ], note="Each address was resolved from the county&rsquo;s own human "
            "resources page or from a portal whose page names the county, and "
            "then fetched, by <b>_dev/county_portals.py</b>. <b>A link here is "
            "an address, not a vacancy</b>: this page says nothing about "
            "whether a county is hiring, what any post pays, or whether you "
            "would be considered. Counties reorganize their recruitment "
            "systems, so check the county&rsquo;s own site if an address "
            "stops working. Nothing here is career advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Where to apply for a California county job, all 58 counties",
    "The application portal for every California county, each one fetched and "
    "checked - including the eight where the address you would guess belongs "
    "to a city, a court, or nobody at all.",
    "licensure", "reference",
    "Where do I apply for a county behavioral health job in California?",
    "All 58 county job portals with the wording that proves each belongs to "
    "the county, and the eight guessable URLs that do not",
    "%d of %d guessable portal URLs are the wrong employer" % (NWRONG, N),
    weight=4)


def main():
    print("county job portals")

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    html_body, nsrc = body()
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d counties, %d sources"
          % (PAGE, format(len(html), ",d"), N, nsrc))

    bad = pk.check_page(p, [
        ("the wrong-employer finding", "belongs to somebody else"),
        ("the address-not-vacancy caveat", "an address, not a vacancy"),
        ("the 403 convention", "working perfectly in a browser"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # All 58 must appear. A county missing from a portal directory reads as
    # "this county does not hire", which is never what it means.
    for r in cpd.PORTALS:
        if pk.esc(r["county"]) not in art:
            print("GUARD: %s is missing from the table" % r["county"])
            bad += 1

    # Every published URL must have answered. Shipping an unchecked link on a
    # page whose whole argument is that links lie would be self-defeating.
    if cpd.DEAD:
        print("GUARD: %d portal(s) did not answer and must not ship: %s"
              % (len(cpd.DEAD), ", ".join(cpd.DEAD)))
        bad += 1
    for r in cpd.PORTALS:
        if r["url"] not in art:
            print("GUARD: %s's URL is not on the page" % r["county"])
            bad += 1

    # It is an address book. It must never read as a claim about vacancies.
    for phrase in ("now hiring", "currently hiring", "has openings",
                   "is recruiting for", "apply today for"):
        if phrase in art.lower():
            print("GUARD: the page appears to claim a vacancy: %r" % phrase)
            bad += 1

    # The eight wrong guesses are the reason the page exists.
    for county, guess, _ in cpd.WRONG_GUESS:
        if guess not in art:
            print("GUARD: the wrong-guess row for %s is missing" % county)
            bad += 1

    for w in pk.spelling(s):
        print("GUARD: British spelling %r" % w)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok")


if __name__ == "__main__":
    main()
