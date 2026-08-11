#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The parts of the status board only a person knows. Edit this, not the HTML.

`_dev/ops_board.py` reads this file plus the live registry and rebuilds
`_ops/index.html` on every deploy. So page counts, titles and links are always
current without anyone touching them; what lives here is the judgement -
what is blocked, on whom, and what is worth doing next.

Keep it short. A status board nobody trusts is one that has grown into a
second backlog.
"""

UPDATED = "11 August 2026"

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
    {"title": "Decide on the visitor-stage hubs",
     "why": "Approved in principle and parked at your instruction. The full "
            "proposal, with three rendered mockups and the coverage audit of "
            "all 182 registry pages, is linked below. Say go and it moves to "
            "the top of the queue.",
     "do": "Read the proposal, then say go or later",
     "detail": []},
]

# Work with the data in hand and nothing blocking it.
NOW = [
    {"title": "The two stages the site had nothing for",
     "state": "go", "tag": "Both shipped",
     "meta": "78 programs reduced &middot; nine years of federal completions",
     "body": ["The coverage audit found <b>0 pages</b> for &ldquo;in a "
              "program&rdquo; and <b>0</b> for &ldquo;deciding whether to "
              "start&rdquo;, against 73 for people already inside. Both now "
              "exist, and both carry a finding nobody else has published: "
              "<b>29 of the 78 programs publish nothing about who finds your "
              "practicum site</b>, and <b>only the MFT license lets any of "
              "those hours count</b> &mdash; the LPCC and LCSW statutes "
              "require all 3,000 after the degree."]},
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
]

# Unblocked and queued, most valuable first.
NEXT = [
    ("Ask-a-question surface", "Item 27 of the 28 &mdash; worth promoting",
     "Questions in, answered by the site with citations, each answer becomes a "
     "page. Would have helped all three MBH-SLRP posters who got four comments, "
     "one, and none."),
    ("Application-portal directory", "No blockers",
     "County HR and jobs URLs, CalOpps, county NeoGov instances, verified like "
     "the county plans. Portals do not expire the way postings do."),
    ("A supervisor directory", "Now the obvious next one",
     "The practicum page names the supervision ratio a trainee needs and the "
     "career-change page names supervision as an unpriced cost. Neither can "
     "say where to find one."),
    ("The rest of the editorial list", "21 of 28 remaining",
     "Advertising rule, telehealth documentation, paying associates, what "
     "licensure costs, records, subpoenas, legislation tracker."),
]

# Decided against, with the reason, so a future session does not re-propose it.
CLOSED = [
    ("On-site community forum",
     "Cold start against groups with 22,800 members, moderation liability for "
     "this audience, and it would put confident wrong answers under the "
     "masthead."),
    ("Job-posting archive",
     "There is no such thing as an &ldquo;MBH-SLRP position&rdquo; &mdash; the "
     "program awards the individual, not the employer &mdash; and republishing "
     "postings is not available."),
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
    ("stage-architecture.html",
     "Visitor-stage architecture &mdash; the full proposal",
     "Six-stage model, the coverage audit of all 182 registry pages, three IA "
     "options and three rendered mockups (the Desk, the Ladder, the Front "
     "Page). This is the thing awaiting your decision."),
]

# The pages worth surfacing on the board, newest first. Titles and links are
# resolved from the live registry, so renaming a page cannot leave a stale
# entry here.
HIGHLIGHTS = [
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
        ("Positions found", "12,679", "12,729", "12,850"),
        ("Counties reporting", "56", "56", "55"),
        ("Published range &mdash; median floor", "$80,080", "$82,285", "$84,074"),
        ("Published range &mdash; median top", "$102,730", "$102,981", "$106,605"),
        ("Actual total wages &mdash; median", "$91,266", "$92,276", "$94,879"),
    ],
    "county_pay_years": ("2023", "2024", "2025"),
    "spread_high": [("San Mateo", "$140,483"), ("Monterey", "$132,775"),
                    ("Solano", "$128,455"), ("Napa", "$126,822")],
    "spread_low": [("Tuolumne", "$58,048"), ("Lake", "$55,203"),
                   ("Imperial", "$50,855")],
}
