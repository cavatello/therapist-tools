#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The parts of the status board only a person knows. Edit this, not the HTML.

`_dev/ops_board.py` reads this file plus the live registry and rebuilds
`_ops/index.html` on every deploy. So page counts, titles and links are always
current without anyone touching them; what lives here is the judgment -
what is blocked, on whom, and what is worth doing next.

Keep it short. A status board nobody trusts is one that has grown into a
second backlog.
"""

UPDATED = "12 August 2026"

# The passphrase that decrypts the published board. Change it here and the next
# deploy re-encrypts under the new one. An environment variable OPS_PASSPHRASE
# overrides it, which is the better home if this file ever goes anywhere public.
#
# The ciphertext IS public - anyone can fetch ops/index.html - so this is the
# only thing between a passer-by and the board. Make it long, and do not reuse
# a passphrase that guards anything that matters. Nothing genuinely
# confidential belongs on the board in the first place.
PASSPHRASE = "pine-gate-4980-associate"


# Things waiting on the site's owner. Anything here should be doable in
# minutes; if it takes longer it belongs in NEXT with a note.
ASKS = [
    {"title": "Send one email to HCAI",
     "why": "Three questions, all unaddressed in every published document - I "
            "checked the grant guide specifically. Their answer unlocks a page "
            "whose analysis is already finished.",
     "do": "MBHSLRP@hcai.ca.gov &middot; or 916-326-3899, Mon&ndash;Fri 8&ndash;5",
     "detail": [
         "Can a practitioner who owns their own California professional "
         "corporation be employed by it, and have that corporation count as the "
         "qualifying employer, assuming the setting itself qualifies?",
         "If so, can the Employment Verification Form be signed by the "
         "applicant in their capacity as owner, or must somebody else sign it?",
         "Does telehealth delivered from a clinician&rsquo;s home count toward "
         "the 32 hours a week of direct client care, or must those hours be "
         "delivered at the eligible practice site?"]},
    {"title": "Say whether the associates door is right before more are built",
     "why": "The first one is live and follows the recommendation exactly. "
            "Everything after it - the sitewide band on 200 pages, then three "
            "more doors - is much harder to unpick, so this is the cheap "
            "moment to change direction.",
     "do": "Open /for/associates and say keep, change, or stop",
     "detail": [
         "The ledger leads because this traffic arrives on a phone. If you "
         "would rather it opened on the six-tile Desk or on the three "
         "questions, that is a small change now and a large one later.",
         "The shelf annotations are the part that takes the time - one line "
         "per page per stage, written by hand. 20 are written. The next door "
         "needs its own."]},
    {"title": "The door build order, for the rest",
     "why": "P2 now carries 16 rendered mockups &mdash; two or three real "
            "alternatives for every door plus three for the sitewide band, each "
            "with a recommendation and what it costs. Four of the five doors "
            "can open; the student one opened yesterday.",
     "do": "Read P2, then say go, or name the variants you prefer",
     "detail": [
         "The recommendations are: Deciding &rarr; Two Questions. Students "
         "&rarr; Placement Desk over the Rules Card. Associates &rarr; the "
         "Ledger. Licensed &rarr; the Change Log, not the masthead. Owners "
         "&rarr; not yet.",
         "The sitewide band is the bigger half: 5 hub pages against 200 leaf "
         "pages that need a stage line. Recommendation is the annotated "
         "breadcrumb plus the next-step band, and not the sticky rail.",
         "One line of configuration decides whether any of it is visible - "
         "`/for/` has to be added to SUBDIRS in the same commit that creates "
         "the directory, or every pass and the sitemap skip it silently."]},
    {"title": "Yes or no on the Bay Area directories",
     "why": "P3. Sourcing is proved from three federal files rather than "
            "argued: 313 nonprofit clinical organizations and 517 health-center "
            "sites, both re-downloadable by anybody.",
     "do": "Read P3, then say go or later",
     "detail": [
         "It is two directories, not one. A trainee cannot work in a private "
         "practice at all; a registered associate can. Building one list and "
         "relabelling it would send students somewhere they legally cannot go.",
         "The directory can only claim eligibility, never availability - no "
         "public source says who takes trainees, and a wrong yes costs a "
         "student an application cycle."]},
]

# Work with the data in hand and nothing blocking it.
NOW = [
    {"title": "The first stage door is live &mdash; /for/associates",
     "state": "go", "tag": "Shipped",
     "meta": "Variant 3C, the Ledger &middot; 20 pages on its shelf",
     "body": ["Steps 1 and 2 of the build order in <b>P2</b>. The whole 3,000-"
              "hour requirement as one bar with the four gates inside it, the "
              "<b>500 relational hours</b> highlighted because that is the one "
              "people reach 3,000 without, then the three questions the "
              "pre-licensed groups actually ask, then the shelf.",
              "Everything is computed in the browser &mdash; no storage, no "
              "share hash, no network call &mdash; and a guard fails the build "
              "if that ever stops being true. Each shelf entry carries what "
              "that page says <em>at this stage</em>, from the new registry "
              "field, so the door cannot become a re-listed topic hub."]},
    {"title": "&ldquo;for&rdquo; added to SUBDIRS in all 40 passes",
     "state": "go", "tag": "The trap, closed",
     "meta": "Plus a new pass that stops them drifting again",
     "body": ["Forty passes each carried their own copy of the directory list. "
              "A new top-level directory was invisible to every one of them "
              "and to the sitemap, <b>while every guard still reported "
              "clean</b>. All forty now agree, and "
              "<code>_dev/subdirs_check.py</code> runs in VERIFY to fail the "
              "build if they ever disagree, if the list names a directory that "
              "does not exist, or if a directory of pages is missing from "
              "it."]},
    {"title": "registry_sync was deleting the stage tagging",
     "state": "go", "tag": "Caught on the first run",
     "meta": "Predicted in P2, and it happened exactly that way",
     "body": ["The pass rebuilds every page record from the page&rsquo;s own "
              "meta tags, so a field held only in the registry vanished "
              "silently on the next build. It now carries across any key it "
              "does not own, and a guard fails if a field disappears from "
              "every record at once."]},
]

# Blocked, and explicitly on what. Never on "time".
BLOCKED = [
    {"title": "&ldquo;Your contract or theirs&rdquo; &mdash; leaving Headway, Alma, Grow",
     "tag": "Needs a primary source",
     "meta": "Highest remaining demand &middot; a 30-reaction / 30-comment thread",
     "body": ["Whether joining a platform credentials you under <em>their</em> "
              "group contract rather than giving you a portable individual one "
              "decides whether somebody depanels. Everything reachable is "
              "third-party blogs. <b>Not building it on that.</b>"]},
    {"title": "&ldquo;Can I be my own qualifying employer?&rdquo;",
     "tag": "Waiting on HCAI",
     "meta": "Analysis finished &middot; see ask 1",
     "body": ["Medi-Cal fee-for-service pays <b>$38.01</b> for the code private "
              "pay bills at <b>$150&ndash;250</b>, and the obligation is 32 "
              "direct hours a week rather than 20. At FFS rates roughly $83,000 "
              "a year worse off; at the higher county rate about a wash, with a "
              "third more clinical hours."]},
    {"title": "The Bay Area directories",
     "tag": "Waiting on your decision",
     "meta": "Feasibility done &middot; 313 orgs and 517 sites reachable",
     "body": ["Sourcing is proved and the design is written up as <b>P3</b>. It "
              "needs a yes because it is two new page types and about 22 "
              "profiles, and because the honest version says out loud that "
              "<b>group private practices are unreachable</b> &mdash; the "
              "largest associate employer, with no public register of any "
              "kind."]},
]

# Unblocked and queued, most valuable first.
NEXT = [
    ("The &ldquo;you are here&rdquo; band &mdash; S1 and S3",
     "Step 3 of the door build order",
     "The doors are five pages; the band is 200. A reader who lands on a leaf "
     "page from a search never sees a hub unless the page tells them one "
     "exists. Annotated breadcrumb above, next-step band below, and not the "
     "sticky rail."),
    ("Repoint the home &ldquo;Who this is for&rdquo; band",
     "Ships with S1 and S3",
     "It already carries four situations pointing at a filtered list. They "
     "become the doors, and that is what makes any of this visible."),
    ("/for/students &mdash; the Placement Desk",
     "Step 4 &middot; runs entirely off practicum_data",
     "The most shareable single thing in the whole proposal: pick your "
     "program, get its published answer to who finds your practicum site."),
    ("Ask-a-question surface", "Item 27 of the 28",
     "Questions in, answered by the site with citations, each answer becomes a "
     "page."),
    ("The rest of the editorial list", "21 of 28 remaining",
     "Advertising rule, telehealth documentation, paying associates, what "
     "licensure costs, records, subpoenas, legislation tracker."),
]

# Decided against, with the reason, so a future session does not re-propose it.
CLOSED = [
    ("Scoping county pay on the department instead of the title",
     "Measured against the thirteen flagged counties and it makes the page "
     "worse. County behavioral health departments are full of case managers, "
     "peer support workers, accounting and office staff &mdash; Glenn&rsquo;s "
     "largest title is &ldquo;HHSA Case Manager II&rdquo; &mdash; and four "
     "counties file environmental health in the same combined department. The "
     "flagged counties are mostly just small, and their genuinely clinical "
     "titles are already matched. The under-25 note stays as the answer."),
    ("On-site community forum",
     "Cold start against groups with 22,800 members, moderation liability for "
     "this audience, and it would put confident wrong answers under the "
     "masthead."),
    ("Job-posting archive",
     "There is no such thing as an &ldquo;MBH-SLRP position&rdquo; &mdash; the "
     "program awards the individual, not the employer &mdash; and republishing "
     "postings is not available. The portal directory is the durable version: "
     "a posting expires in six weeks, an address does not."),
    ("Rural health clinic directory",
     "One clinic is filed under three counties at once, another under five. The "
     "source data does not support publishing it."),
    ("A second credentialing page",
     "The existing panels page already covers CAQH, PECOS, PAVE, 855, NPI, "
     "Medicare, Medi-Cal and timelines. The real gap is the platform-contract "
     "question above."),
]

# Prototypes and proposals published alongside this board so it can link to
# them. Paths are relative to /_ops/.
DOCS = [
    ("redesign-37signals-products.html",
     "P7 &middot; Four products, four identities &mdash; the current "
     "proposal",
     "<b>Start here.</b> 37signals does not have a house style; it has four "
     "products that look deliberately unlike each other. The site drawn four "
     "times &mdash; as <b>Basecamp</b>, <b>HEY</b>, <b>Campfire</b> and "
     "<b>Fizzy</b> &mdash; logo, home page, path page, content page and "
     "directory in each, with every color, radius and type classification "
     "read off the real product's stylesheets. The words are identical in "
     "all twenty mockups, so the only thing varying is the design. Ends with "
     "a recommendation that is a fifth thing rather than any one of them."),
    ("redesign-37signals.html",
     "P6 &middot; If 37signals had built this site &mdash; three invented skins",
     "Logo, typography, color, navigation, footer, four "
     "home pages, the six paths, a path page, an article, a directory, the "
     "newsletter and the about page &mdash; drawn in <b>three complete "
     "skins</b> plus phone views, so the choice is between finished "
     "directions rather than between adjectives. The structural change is "
     "that the six paths become the primary navigation and the topic hubs "
     "move to an index at the foot of every page. Ends with a build order, "
     "and with why a redesign and a move to Rails are two projects."),
    ("home-page-options.html",
     "P5 &middot; Six home pages, one column each &mdash; the home page alone",
     "The five-card band in P4 section 03 was "
     "rejected: a band of five equal cards is a menu of menus, it asks a "
     "stranger to classify themselves before anybody has told them what the "
     "site is, and it is made of the same bordered cards as the eleven blocks "
     "under it. Six alternatives drawn in the 37signals discipline &mdash; "
     "one column, big plain type, prose instead of grids, one thing to do "
     "&mdash; each with what it costs, and one recommended."),
    ("information-architecture.html",
     "P4 &middot; One pattern, five doors &mdash; superseded in part",
     "Every landing page mocked up, the architecture "
     "underneath them, and the six-block pattern each door follows. Rebuilt "
     "after the first door shipped and came back with two corrections: lead "
     "with what the reader gets rather than the tool, and say it in words a "
     "stranger already knows. Supersedes the design half of P2."),
    ("stage-doors.html",
     "P2 &middot; Five doors, three ways each &mdash; superseded in part",
     "16 mockups with a recommendation each. The impact list in section 09 is "
     "still current and still the thing that decides the timeline. The door "
     "designs were drawn before the first one shipped and lead with the tool, "
     "which is the mistake P4 corrects."),
    ("stage-architecture.html",
     "P1 &middot; Visitor-stage architecture &mdash; the case",
     "Whether to do this at all. Six-stage model, the coverage audit of all "
     "182 registry pages, the evidence and the namespace argument. Not "
     "repeated in P4."),
    ("bay-area-directories.html",
     "P3 &middot; Bay Area practicum and associate sites",
     "Whether the two directories can be sourced honestly, and from what. "
     "313 nonprofit clinical organizations and 517 health-center sites are "
     "reachable from federal files; group private practices are not reachable "
     "at all, which is the finding."),
]

# The pages worth surfacing on the board, newest first. Titles and links are
# resolved from the live registry, so renaming a page cannot leave a stale
# entry here.
HIGHLIGHTS = [
    ("for/associates.html",
     "The first stage door, and the reference implementation for the other "
     "four. Rebuilt for the cold arrival: what this is, who it is for, and "
     "how big it is, before any tool. <b>Nothing typed into it leaves the "
     "browser.</b>"),
        ("county-job-portals-california.html",
     "Where to apply, in all 58 counties, every link fetched. <b>Seven "
     "guessable URLs belong to a city, a court, or nobody</b> &mdash; and "
     "Alameda is not on the system its own name is registered under."),
    ("practicum-california-mft-trainee.html",
     "All 78 programs on one question &mdash; whose job is it to find your "
     "practicum site. <b>29 publish nothing, 10 say it is yours.</b> Plus the "
     "seven trainee rules, starting with the one that rules out every private "
     "practice in the state."),
    ("becoming-a-therapist-california-career-change.html",
     "California&rsquo;s clinical master&rsquo;s pipeline grew <b>66% in eight "
     "years</b> while graduate education overall grew 14%. The three licenses "
     "compared on statute rather than temperament."),
    ("county-therapist-pay-california.html",
     "Every county ranked by what it actually paid, three years running. "
     "<b>2.8&times; between the top and the bottom.</b>"),
    ("mbh-slrp-california.html",
     "32 direct-care hours a week, one lump payment, <b>breach means repaying "
     "the whole award within a year</b>, and cycle 1 was 3.7&times; "
     "oversubscribed &mdash; $331m requested against $90.1m available."),
    ("medi-cal-safety-net-employers-california.html",
     "57 county behavioral health plans and 218 health center organizations, "
     "every link fetched before publishing. <b>23 of the state&rsquo;s own "
     "links no longer point where they say.</b>"),
    ("loan-forgiveness-employers-california.html",
     "Four programs, <b>three different tests</b>. PSLF ignores your license "
     "entirely, so a county associate is likely accruing qualifying payments "
     "right now."),
    ("getting-hired-as-a-california-associate.html",
     "&ldquo;Nobody will hire me&rdquo; is a <b>billing rule</b>, not an hour "
     "count. Medi-Cal names associates as billable staff; commercial payers "
     "do not."),
    ("out-of-state-to-california-licensure.html",
     "Path A against Path B across all three licenses, and the correction that "
     "<b>continuing education cannot fix a transcript</b>."),
]

# Numbers the board prints that are not derivable from the repository.
FIGURES = {
    "editorial_done": 7,
    "editorial_total": 28,
    "county_pay": [
        ("Positions found", "12,297", "13,041", "13,184"),
        ("Counties reporting", "56", "56", "55"),
        ("Published range &mdash; median floor", "$77,392", "$77,355", "$80,954"),
        ("Published range &mdash; median top", "$102,170", "$100,656", "$105,827"),
        ("Actual total wages &mdash; median", "$89,568", "$90,078", "$93,215"),
    ],
    "county_pay_years": ("2023", "2024", "2025"),
    "spread_high": [("San Mateo", "$140,483"), ("Monterey", "$132,775"),
                    ("Solano", "$128,455"), ("Napa", "$126,822")],
    "spread_low": [("Tuolumne", "$58,048"), ("Lake", "$55,203"),
                   ("Imperial", "$50,855")],
}
