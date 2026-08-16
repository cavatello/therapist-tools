#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The 24 Bay Area organization profiles - one leaf per curated org.

P3's last open item. The two Bay directories list the organizations; the
training-programs page holds the ten with published programs on one
sheet. What was missing is the page you send SOMEBODY ELSE: one org, what
it is, what its own site publishes about clinical training, and the
questions to bring - with every fact linked to the page it came from and
the read date on all of it.

THE CONTENT CONTRACT (same as every P3 page, enforced here by guard):
  - claim EXISTENCE, never availability. "Its internships page states"
    is checkable; "it is hiring" is a guess about today. The banned
    phrases fail the build.
  - a "nothing published" profile is a real finding, not filler - it is
    the afternoon the next person does not have to spend.
  - no personal names or personal email addresses, anywhere. The
    research recorded some; they do not ship. Program pages are linked
    instead.
  - every profile carries the Family-Paths-style flag when the org's own
    site announces one.

LEAVES, NOT CLUSTER ROWS. All 24 carry ts:leaf, like the 66 school pages
and the 48 case pages: represented on the Licensure hub by the directory
pages, reachable through the two Bay directories (build_baysites.py links
each profiled org's row here) - 24 rows in a topic hub would be the
catch-all problem taxonomy_leaves.py exists to prevent.

Data in _dev/orgprofile_data.py, hand-written from the banked research
(all fetched 16 Aug 2026). Chrome from the same donor as the other
pagekit pages; article.pk-wrap, so _dev/family_pk.py adopts and guards
the design.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk
import orgprofile_data as od
from nonprofits import CURATED_URLS

SITE = pk.SITE
DONOR = "county-job-portals-california.html"
DIRECTORY = "practicum-sites-bay-area.html"
ASSOC_DIR = "associate-employers-bay-area.html"
METHOD = "how-to-find-a-practicum-site-california.html"
RULES = "practicum-california-mft-trainee.html"

JUMPS = [("org", "What it is"), ("training", "What its site publishes"),
         ("bring", "The questions to bring"), ("sources", "Sources")]

BANNED = ("is hiring", "has openings", "takes trainees",
          "accepting trainees", "currently accepting", "spots available",
          "positions open")
# personal emails the research recorded; they must never ship
LEAKS = ("twang@", "mhenry@", "kimberly.watson@", "mailto:")

STATUS_KICKER = {
    "published": "Published clinical training program",
    "paused": "Published program &middot; pause announced",
    "none": "No training program published",
    "volunteer": "Volunteer track, not a practicum",
    "collective": "An associate collective",
    "nonclinical": "Not a clinical organization",
}


def ext(url, label):
    return ('<a href="%s" target="_blank" rel="noopener noreferrer">%s'
            "</a>" % (url, label))


def body(o_):
    st = o_["status"]
    o = ['<article class="pk-wrap">']

    o.append('<section class="pk-hero">')
    o.append('<p class="hk">Bay Area organization profile &middot; %s '
             "&middot; read %s</p>" % (STATUS_KICKER[st], od.READ))
    o.append("<h1>%s.</h1>" % o_["name"])
    o.append('<p class="hl">%s &mdash; what the organization is, what '
             "its own site publishes about clinical training, and the "
             "questions to bring. Every fact below was read from a "
             "fetched page on the date above, and each one links the "
             "page it came from. Nothing here says what is available "
             "today &mdash; sites change; the organization "
             "answers that.</p>" % o_["where"])
    o.append('<p class="hj">')
    for h, l in JUMPS:
        o.append('<a href="#%s">%s</a>' % (h, l))
    o.append("</p></section>")

    # ---------------------------------------------------------------- org
    o.append('<section class="pk-sec" id="org">')
    o.append('<p class="pk-k">What it is</p>')
    o.append('<h2 class="pk-h">The organization, from its own site.</h2>')
    for para in o_["what"]:
        o.append('<p class="pk-p">%s</p>' % para)
    o.append('<p class="pk-p">Its site: %s.</p>'
             % ext("https://" + o_["site"], o_["site"]))
    o.append("</section>")

    # ----------------------------------------------------------- training
    o.append('<section class="pk-sec" id="training">')
    o.append('<p class="pk-k">What its site publishes about training</p>')
    if st in ("published", "paused"):
        o.append('<h2 class="pk-h">A program its own pages describe.</h2>')
        o.append('<p class="pk-d">Each statement below is what the '
                 "organization&rsquo;s own site said on %s, with the "
                 "page it said it on. A program existing on a page is "
                 "not a seat existing today &mdash; the page is where "
                 "you check.</p>" % od.READ)
        for txt, url in o_["facts"]:
            o.append('<p class="pk-p">%s %s</p>'
                     % (txt, ext(url, "The page that says so &rarr;")))
    else:
        o.append('<h2 class="pk-h">What was found, and what was '
                 "not.</h2>")
        for para in o_.get("none_note", []):
            o.append('<p class="pk-p">%s</p>' % para)
        o.append('<p class="pk-p">Where a question about roles belongs: '
                 "%s.</p>" % ext(o_["careers"], "its careers page"))
    o.append("</section>")

    # -------------------------------------------------------------- bring
    o.append('<section class="pk-sec" id="bring">')
    o.append('<p class="pk-k">Before you write to anyone</p>')
    o.append('<h2 class="pk-h">The three questions that protect your '
             "hours.</h2>")
    o.append('<p class="pk-p">A trainee cannot count hours from a '
             "private practice or a professional corporation &mdash; "
             '&sect;&thinsp;4980.43.3 draws that line, and <a href="%s">'
             "the trainee rules page</a> walks all seven of the rules "
             "that decide whether a placement counts. A registered "
             "associate has a wider map; both start from the same three "
             "questions: who signs the supervision paperwork and on "
             "what schedule, which settings the hours would come from, "
             "and &mdash; for a trainee &mdash; whether your "
             "program&rsquo;s site agreement exists yet, because "
             "&sect;&thinsp;4980.42 puts that agreement on your school, "
             "not on you.</p>" % RULES)
    o.append('<p class="pk-p">The whole search method &mdash; whose job '
             "the search is, the order that saves cycles, and the paper "
             'trail to keep &mdash; is on <a href="%s">the '
             "how-to-find-a-practicum-site page</a>. This profile is "
             'one shelf of it; the full Bay Area shelves are <a '
             'href="%s">the practicum-sites directory</a> and <a '
             'href="%s">the associate-employers directory</a>.</p>'
             % (METHOD, DIRECTORY, ASSOC_DIR))
    o.append("</section>")

    # ------------------------------------------------------------ sources
    seen, links = set(), []
    links.append(("The organization&rsquo;s site, fetched before "
                  "publication", "https://" + o_["site"]))
    for txt, url in o_.get("facts", []):
        if url not in seen and url != "https://" + o_["site"]:
            seen.add(url)
            links.append(("The program page each statement above quotes",
                          url))
    if o_.get("careers") and o_["careers"] not in seen:
        links.append(("Its careers page", o_["careers"]))
    src, nsrc = pk.sources([
        ("Read on %s" % od.READ, links),
        ("The statutes the questions come from", [
            ("Business and Professions Code &sect;&thinsp;4980.43.3 "
             "&mdash; the settings a trainee may and may not count "
             "hours from",
             "https://leginfo.legislature.ca.gov/faces/codes_display"
             "Section.xhtml?lawCode=BPC&sectionNum=4980.43.3."),
            ("&sect;&thinsp;4980.42 &mdash; the site agreement your "
             "school must hold before a trainee placement starts",
             "https://leginfo.legislature.ca.gov/faces/codes_display"
             "Section.xhtml?lawCode=BPC&sectionNum=4980.42."),
        ]),
    ], note="This profile records what the organization&rsquo;s own "
            "site published on the read date, and nothing else. It is "
            "not a statement about today, it is not an endorsement, "
            "and it is not legal advice. Sites change; the links above "
            "are where to check.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


def main():
    print("the %d Bay Area organization profiles" % len(od.ORGS))

    # ---- the two sets must match exactly, or the gap is loud
    prof = {o["irs"] for o in od.ORGS}
    cur = set(CURATED_URLS)
    missing = sorted(cur - prof)
    extra = sorted(prof - cur)
    if missing:
        sys.exit("curated org(s) with no profile: %s" % ", ".join(missing))
    if extra:
        sys.exit("profile(s) for uncurated org(s): %s" % ", ".join(extra))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    nbad = 0
    for o_ in od.ORGS:
        html_body, nsrc = body(o_)
        meta = pk.meta_block(
            o_["slug"],
            "%s - Bay Area org profile" % re.sub(
                r"\s*\(.*\)", "", o_["name"]),
            o_["desc"], "licensure", "reference",
            o_["question"], o_["outcome"], o_["number"], weight=1)
        meta += '<meta name="ts:leaf" content="true">\n'
        html = pk.assemble(head, meta, header, html_body, footer, links,
                           scripts)
        p = os.path.join(SITE, o_["slug"])
        open(p, "w", encoding="utf-8").write(html)

        n = pk.check_page(p, [
            ("the org site link", 'href="https://%s"' % o_["site"]),
            ("the pk wrapper family_pk adopts", 'class="pk-wrap'),
            ("the leaf flag", 'name="ts:leaf" content="true"'),
            ("the trainee-rules link", RULES),
            ("the method-page link", METHOD),
            ("the 4980.43.3 source", "sectionNum=4980.43.3."),
        ], [h for h, _ in JUMPS])
        s = open(p, encoding="utf-8").read()
        text = re.sub(r"<[^>]+>", " ", s).lower()
        for phrase in BANNED:
            if phrase in text:
                print("GUARD %s: availability language %r"
                      % (o_["slug"], phrase))
                n += 1
        for leak in LEAKS:
            if leak in s:
                print("GUARD %s: personal contact %r must not ship"
                      % (o_["slug"], leak))
                n += 1
        # Only this builder's own article - the chrome nav legitimately
        # EXPLAINS the LLC prohibition ("cannot form an LLC"), which is
        # the correct usage the sitewide rule protects.
        art = re.search(r'<article class="pk-wrap[\s\S]*?</article>', s)
        if art and "LLC" in art.group(0):
            print("GUARD %s: 'LLC' has no business in this article"
                  % o_["slug"])
            n += 1
        nbad += n
        print("  wrote %-46s %s bytes, %d sources"
              % (o_["slug"], format(len(html), ",d"), nsrc))

    if nbad:
        sys.exit("%d check failure(s)" % nbad)
    print("  all %d profiles written, checks passed, guards clean"
          % len(od.ORGS))


if __name__ == "__main__":
    main()
