# Rollout Step 2 — the CSS swap, execution plan

## STATUS 13 Aug 2026 (late session): STEPS 2–3 ARE LIVE SITEWIDE

Shipped as the skin approach documented below, verified at every stage:

- `css/house-skin.css` — every rule gated on `body.house`, loads last on every
  page. bc2 tokens override the old `:root` palette (and the .px/.lib/.sc/.adv
  family scopes); Bricolage 800 on headings, Fraunces on figures, mono eyebrows;
  chrome restyled: masthead + The Rule lockup (pure CSS, no image), nav panel,
  dark signup band, deep footer. `!important` used only where chrome_armor.py
  outranks plain rules (band, footer, masthead CTA) — documented in the sheet.
- `_dev/house_swap.py` — adds body.house + the skin link, idempotent, guarded
  (skin present exactly once, last, matching the body class). Excludes
  tycoon.html and rates.html by decision. Wired into ship.py's LAST stage so
  rebuilt pages are re-converted every build.
- Gates run before each live push: 24/24 (six gate pages × 4 breakpoints) and
  36/36 (twelve more pages across every family × 3 breakpoints) — zero
  horizontal overflow, zero JS errors, visual pass on home/footer/band/county
  table/hub/simulator screenshots. Two bugs found at the gate and fixed there
  (chrome_armor outranking the band + footer restyle).
- Live verification: six gate pages pushed and confirmed first (`8057d6c1`),
  then the remaining 195 (`ca8a3a4c`); skin byte-identical on the live host;
  rates.html and tycoon.html confirmed untouched. ship.py --check clean at 203
  pages after each run.

## STEP 4 IS ALSO LIVE (`a9f580e2`, 13 Aug 2026)

`_dev/build_home.py` rebuilt index.html to option A with C's waterfall inside
the tool card. It imports PATHS + WELCOME from build_bcopts.py (one source of
approved copy), replaces only the landing <main> (title/meta/JSON-LD/analytics/
chrome/scripts keep their bytes), drops the five landing-only inline styles,
and guards every written href against disk. Path 03's row points at
/for/associates.html — folded into 04 per the settled decision — until the
90-day page exists. Row targets: 01→career-change, 02→practicum, 03+04→
/for/associates, 05→practice/, 06→hiring-first-associate. The known `.band`
collision (hub_hero's unscoped rules leaking into bc2 markup) appeared exactly
as the audit predicted and is pinned by section 12 of house-skin.css — those
defenses retire with the old sheets at step 5. Gated 4/4 breakpoints on the
mirror before pushing; ship.py --check clean at 203 pages; live page verified
carrying main.bc2.home + the waterfall. NOTE: build_home.py is NOT yet wired
into ship.py BUILD — wire it once home_doorway.py and stage_router.py (which
targeted the old landing markup) are retired; until then a full rebuild that
regenerates index.html must be followed by `python3 _dev/build_home.py`.

What remains of the design rollout: Step 5
(family templates to real bc2 components, retiring each family's old sheets as
its markup converts — this is where the 30-name collision list matters), Step 6
(the doors + the one-slab audit). The original plan below stands for those.

Written 12 August 2026, after Step 1 shipped. Step 1 is live and verified:
`css/house.css` (18,149 bytes) is byte-identical on the live host, `_dev/build_bcopts.py`
reads it back so the design doc and shipped sheet cannot drift, and `css_dedupe.py`'s
orphan sweep now only touches 12-hex hash names — it would otherwise have binned the
unused sheet on the next cycle. Shipped as `ccb1c461`, all passes clean at 203 pages.

## The collision audit — the finding that shapes everything

30 of house.css's 91 class names already exist in the 45 live shared sheets:

- worst: `.sub` (9 sheets), `.on` (8), `.in` (6), `.band` (5), `.n` (5), `.g` (4),
  `.tbl` (4), `.who` (4)
- plus the two known: `.f` (form field, was pagekit) and `.bar` (ops chrome)

house.css is scoped under `.bc2`, but the old sheets are NOT scoped — their selectors
match inside a `.bc2` region. So the rollout doc's rule is not just right, it is the
only option: **a page is either fully old or fully new. All old stylesheet links and
inline blocks come out in the same rewrite that adds bc2 markup.** No page may carry
both for even one watcher cycle. Renaming 30 classes in house.css was considered and
rejected: it would fork the sheet from the approved design doc that generated it.

## Current state of a page (measured on about.html)

24 stylesheet links + 2 inline blocks: restyle.py's chrome layer (masthead `sitenav`,
navpanel, footer) plus ~15 floor passes (token_floor, mobile_floor, one_grid,
content_frame, touch_polish, …) layered over the original base. 45 shared sheets,
231 KB. The floors exist to fix the old base; house.css replaces base and floors
at once.

## Mechanism

One NEW pass file — `_dev/house_swap.py` — new for the restore-survival reason
documented at the top of restyle.py. Per page, in one rewrite:

1. Strip every `css/<hash>.css` link and every inline `<style>` belonging to the
   old system (identified by pass markers; anything unrecognized fails the run,
   listed, rather than being silently kept or dropped).
2. Add `bc2` to `<body>`, link `house.css` (depth-aware `../`), update the Google
   Fonts request to Bricolage Grotesque 800 / Fraunces / IBM Plex Mono / Inter.
3. Re-emit chrome (masthead, nav, footer) as bc2 components — Step 3's markup,
   because chrome cannot keep old markup with the old sheets gone. Steps 2 and 3
   effectively ship as one pass run; the doc's Step 3 items (logo lockup as CSS
   type, favicon crop) ride along.
4. Body content initially styled by house.css element rules (h1–h4, p, tables,
   lede) — page-specific bc2 components arrive at Steps 4–5.

## Atomicity against the watcher

The watcher fingerprints top-level html/css/js/txt/md and pushes on change; `_dev/`
does not trigger it. So: develop and iterate the pass entirely in `_dev/`, test
against a full mirror copy of the site outside the repo, and only when the gate
passes there, run once on the repo — a pass run rewrites 203 pages in seconds,
well inside one watcher cycle — followed immediately by extract_css → css_dedupe →
`ship.py --check`. Recovery is `git revert` of the one auto-publish commit.

## The testing gate (from the rollout doc, run on the mirror BEFORE the real run)

375 / 768 / 1440 / 2560px, on at least: home, a path page, an article, a directory,
the email page, about. Per breakpoint: `scrollWidth == viewport` (no horizontal
overflow), body measure ≤ ~70ch (2560 is where this breaks), body contrast ≥ 7:1,
path hues ≥ 4.5:1, above-the-fold on iPhone = headline + one-liner + primary action.
Then linkcheck / seo_rules / notruncate clean at 203 pages. Playwright over a
localhost mirror — the sandbox cannot reach the live host from Chromium.

## Open question for the next session

Whether `house_swap.py` converts all 203 pages in one run, or ships the six
gate pages first (one run, verified live) and the remaining ~197 in a second run
the same session. The doc's "each step verified live" favors the two-run shape;
the collision audit permits it, since conversion is per-page atomic either way.

## Chrome study for house_swap.py — done, findings

The six gate pages share one chrome: header.sitenav + div.navpanel, section.ftnl
signup band, footer.sitefoot; then per-family bodies (main.lp landing / article.pk-wrap
hub-directory / main.adv tool / .band+.sec editorial). Inline styles are few and
marker-identified (biggest: index's 22.7KB landing sheet and amft's 19.8KB .adv sheet,
both in <head>); all other CSS is the 18–25 hash-linked sheets loaded after the footer.
Scripts to KEEP verbatim: JSON-LD, GA4, Ahrefs, Clarity, nav toggle, Formspree handler,
analytics_events, error_tracking, and the page widgets (ledger, 44KB hours engine,
tool_chain). The fonts request already carries all four bc2 faces — no font work
needed. Full inventory is in the session transcript; the compat layer needs to cover:
lp/pk/adv/band-sec families, bcr breadcrumbs, tsshort/tsfoot, uplink, ftnl, sitefoot,
pk-t tables, fgrid/f form fields (the .f collision is live on amft's calculator).

## Carried forward so it doesn't get lost

- P12 — the infographics/visual-information system for directories and trainings
  (ledger row, gap bar, pay ladder, cohort calendar, negative-finding card, plus
  the four approved bc2 pieces) — drafts as an /ops/ design doc AFTER Step 4,
  ships with Step 5's templates. Decided this session.
- SF Bay Play Therapy's pay ladder page says "check later in 2025" — a 2025
  reference point, not current. Mark it stale wherever cited.
- `hours/` is a password-protected design doc; the subdirs guard exempts it by
  proof, not by name — if an indexable page ever lands there the build fails,
  which is correct.
- After Step 4 and the 90-day page: stop and read Ahrefs before building the
  remaining doors and the 21 editorial pages. The path model is checkable now.

## The queue, in order

STANDING RULE (user, 12 Aug 2026): new asks always join at the BOTTOM of the
queue. They get banked as research immediately so nothing perishes, but they
do not jump the line.

1. Rollout Steps 2–4 (house_swap.py → mirror gate → six gate pages live →
   remaining ~197 → nav/footer/logo → home page)
2. The 90-day rule page (path 03's missing content; verify against BPC + Board
   before writing)
3. Read Ahrefs before building more — the checkpoint the path model exists for
4. P3 Bay Area directories (practicum sites first, then associate employers —
   spec in claude/p3-bay-area-directories-approved.md)
5. Remaining /for/ doors, "you are here" band, ask-a-question surface,
   generated footer index, 21 editorial pages (order per the rollout doc)
6. NEW ASK — pre-licensed job-sites directory, statewide. 232 leads banked in
   RESEARCH/prelicensed-job-sites-leads.md (names + own-site URLs + region only;
   CAMFT's gated text not reproduced). Build on the build_safetynet.py pattern:
   fetch every domain before it ships as a link. Merges with the P3 employer
   work — same page family, same columns.
7. NEW ASK — financial assistance expansion. Snapshot banked in
   RESEARCH/financial-assistance-programs-2026-07-28.md. Note the cost of its
   queue position: the SLRP cycle (up to $50k for LMFTs) closes 15 Sept 2026;
   if this item is reached after that, the open-cycle line ships as "next
   cycle" framing instead. AHLRP ($16k) and LMHSPEP ($15k) are closed cycles.
   Builder edits (build_forgiveness.py / build_mbhslrp.py), every figure
   verified against HCAI's own pages first.

## PIPELINE HARDENED — full build green (13 Aug 2026, second pass)

`python3 _dev/ship.py` runs 86/86 clean end-to-end with the redesign, verified
on a mirror copy first, then run and pushed live (`268cece8`). Five landmines
found by the mirror run and fixed:

1. restyle.py demanded the old `.lp` block on index — now skips when the
   option-A home is present.
2. The approved option-A copy claimed "Nothing sold" — false since affiliate
   links exist; affiliate.py rightly failed the build. build_home.py now
   writes the narrowed, true claim.
3. token_floor.py and 4. css_cdo_fix.py hash-name guards assumed every css/
   file is extract_css output — both now skip named sheets (house.css,
   house-skin.css), same as css_dedupe's orphan sweep.
5. house_swap.py now RE-POSITIONS the skin link last on every run — a full
   build hoists new style blocks into links after it, which broke the
   order-wins contract on 132 pages until fixed.

Also: build_home.py is wired into ship.py BUILD; home_doorway.py and
stage_router.py detect the new home and skip their landing halves
(stage_router's resources.html half still runs in full). The next session can
run a full build with no manual follow-ups.

## DEEP-SKIN PASS — 27-inch audit (13 Aug 2026, third pass, `95ae8b10`)

User-reported mess at 2560px, fixed and re-gated:
- Home content capped at a 1240px well (full-bleed grounds kept) via padding:max().
- Hardcoded dark heroes re-grounded flat bc2 deep: .artband, .dc-hero, .pk-hero,
  section.hero (tool pages), slab.pine/carbon; brick/gold slabs flattened.
- Light headings re-asserted on every dark ground (the global heading-ink rule
  had made .pk-hero/.dc-hero h1s 2.4:1 — caught by the automated contrast gate).
- Brutalist chips → quiet gold-outline mono pills; hard-offset shadows removed;
  off-palette purple game layer (lvchip/xptrack/simbtn) joined the palette.
- Note: the "gold highlighter" screenshot was text SELECTION (::selection gold).
Gate: 14 pages × 5 viewports (375/768/1024/1440/2560) = 70/70 clean — overflow,
JS errors, body ≥16px, h1-on-ground contrast ≥4.5:1 all automated. All of
section 13 in house-skin.css retires with the old sheets at step 5.

## SIM DISASTER FIX + FULL CONTRAST AUDIT (13 Aug 2026, fourth pass, `212020d0`)

- The flat-dark slab treatment made the simulator four dark blocks — against
  the one-slab rule. Tool sections are now WHITE CARDS with a 5px hue accent
  (pine/red/amber/ink); the hero stays the page's single dark band. The purple
  .bonus band joined the palette as deep; .hubnl and .dc-out grounds restored.
- Cause of two regressions found the honest way: my own skin rules (white
  .slab headings on now-white cards; ink .dc-h/.pr-h on dark grounds). The
  audit that catches this class of bug is now the standard: EVERY visible
  heading vs its real ground — 217 headings, 14 pages, all ≥4.5:1 — plus
  56 overflow/JS checks at 375/768/1440/2560. Both clean before shipping.
- house-skin.css link now carries ?v=<content-hash> (house_swap emits it), so
  browsers stop serving stale design after each fix — the user's "still a
  mess" screenshots were partly Pages' max-age cache.
- hours/compare.html (user's own working doc, saved this morning) tripped
  subdirs_check exactly as designed — missing noindex, added.

## GLOBAL CONSISTENCY PASS (13 Aug 2026, fifth pass, `f828d981`, skin v=f976d0ca)

User review on live found the theme not global. Root causes fixed:
- Heading COLOR removed from the global type rule — it had broken ~103 dark
  heroes (scband/psy families). Headings now inherit their ground's color.
- Ornament neutralizer generated FROM the sheets: 71 hard-offset-shadow
  selectors flattened, gold chips quieted, 2px black borders → hairlines.
- Warm-cream .f field family re-toned to white/cool sitewide; heading
  highlighter blocks killed; purple grounds (.bonus, .clband/.clhero) → deep;
  .ftnl band text made light WHOLESALE (its children keep growing shapes).
- Audit hardened: skips screen-reader-only elements, checks h1-h4 + dek/lede/
  kick/labels vs real rendered ground on ALL 201 pages: 3,705 elements,
  0 low-contrast, 0 overflow before shipping.
STILL OPEN: psyd directory cards should link internally to each school's own
page on-site (user request) — build_psyd.py change, mapped but not yet coded.
The real cure for all of section 13-14 remains Step 5 (markup conversion).

## QUEUE ADDITION (bottom, per standing rule) — 13 Aug 2026
8. NEW ASK — expand the MIND Foundation page (psychedelic-training-mind-
   foundation-apt.html) into a full dedicated write-up of the Berlin
   "Augmented Psychotherapy Training" — as much verified content as the
   source supports, videos included, from
   https://www.mind-foundation.org/augmented-psychotherapy-training
   (fetch + verify before writing; existing page is the stub to grow).

## LEGIBILITY BATCH 6 (13 Aug 2026): adaptive breadcrumbs (inherit + opacity,
no container list), newsletter issue keys pine, np-promo hub card deep again,
waterfall inset + wider label column, house.css link now content-versioned.
Audited before ship. NOTE for step 5: the tax-page "reasoning" scroller and
floating page-toc render broken-wide at 27" — layout, not color; needs the
family conversion, not more skin.

## STEP 5, FAMILY 1 GATE RUN + FIXES (13 Aug 2026, evening, `e0daa8e5`)

State found at session start: the article-family conversion had ALREADY
LANDED under `_dev/family_art.py` (wired in ship.py LAST after house_swap;
sheets `css/house-art.css` / `css/house-sc.css` / `css/house-chrome.css`;
commits `dd0655a5`..`78238c7d`) — covering BOTH the .artband family (20
pages; psyd-programs excluded by decision) and the .scband family (66
pages), 86 pages total, each carrying `<body class="bc2 bca|bcs house">`,
exactly the three named house sheets, zero legacy hash sheets, no skin
link. No new `house_articles.py` was written: PASSES.md's own rule is to
extend the pass that already owns the marker, and family_art.py is that
pass. What was MISSING was the gate record — this section is it.

Gate audits, run on a full /tmp mirror (mirror-first, fixes applied there
before the repo was touched):
- CONTRAST at 1440: 586 elements (h1–h4, dek, kick, tsk, labels,
  breadcrumbs incl. separators, artmeta/scmeta) across 23 pages — 16
  family pages + home, simulator, county directory, discipline hub,
  newsletter, about, money/ hub. First run: 33 below 4.5:1 — all but one
  were the breadcrumb separator "›" (var(--hair) on paper, 1.2:1) on
  every converted page; the one other was PRE-EXISTING (proven present at
  pre-family commit `d72a0b9a`): the discipline hub's In-short card,
  where skin rule `body.house .dc-hero p{color:#CFE0D6}` paints the white
  card's own labels pale green (1.37:1). After fixes: 0 below 4.5:1.
- OVERFLOW + JS: 92 checks (23 pages x 375/768/1440/2560) — 0 failures.
- Screenshots at 1440 (top + mid) and 375 of bbs-fees, alliant-mft,
  therapist-llc, reviewed by eye: masthead, breadcrumb, kick, headline
  with gold highlight, dek, dark In-short card, rail figure card, sticky
  "On this page" toc, prose measure — all correct at both widths.

Fixes shipped (one atomic run: sed edits + house_swap --all + family_art
hash refresh + ship.py --check 5/5, inside one watcher cycle):
1. `.bcr .sep` color var(--hair) -> var(--dim) in house-art.css AND
   house-sc.css (the separators are arguably decorative, but the gate
   standard is every breadcrumb element >= 4.5:1, so they comply now).
2. house-skin.css: scoped re-ink `body.house .dc-hero .tsshort p` /
   `.tsk` — a pre-existing live defect the gate caught; retires with the
   dc family's conversion.

Live verification (after watcher push `e0daa8e5`, tree == origin):
three converted pages curled — bc2 bca/bcs body, 3 house sheets, 0
legacy sheets, 0 skin links; house.css, house-art.css, house-sc.css and
house-skin.css all byte-identical between live host and repo.

Now retirable (do NOT delete yet — unconverted families still load the
skin): every house-skin rule keyed on .artband/.scband and their family
vocabulary (the section-13 dark-hero re-grounds for those two heroes, the
scband heading re-asserts from the fifth pass) no longer reaches any
page, because converted pages do not link house-skin.css at all. They
cost nothing where they are; sweep them when the skin itself retires.

Known content defect, out of scope (content is byte-preserved by
mandate): alliant-mft's fact-card Format value is truncated IN SOURCE to
"On-campus and fully online (synchr" — present since `88059cac` (6 Aug);
a builder/content fix, not a conversion issue.

## COORDINATION + DEFECT REPORT — 14 Aug 2026 (session A)

- STEP 5 CONTINUES IN THE USER'S OTHER CHAT (currently family 3, pagekit).
  This session stays off family conversions to avoid colliding in the same
  working tree. It banked research + defect reports instead.
- DEFECT (family 1, for the step-5 session): on converted school pages
  (user screenshot: university-of-san-francisco-mft.html) the page-foot
  metadata strip ("Last checked… / Figures current as of… / Published
  sources only / Known gap") and the "More on this" hub cluster render as
  UNSTYLED run-together text — those injected blocks lost their legacy
  sheets in conversion and house-sc.css/house-art.css do not yet style
  them. Restyle in the family sheets (bc2 vocabulary), re-gate, ship.
- BANKED: RESEARCH/ebcamft-practicum-sites-2026-08-14.md — EB CAMFT's
  public 2026-27 practicum directory, 22 sites, structured. User: "must
  have directory." Slots into P3 practicum-sites (queue item 4), and its
  three hires-associates sites feed the associate-jobs pages.

## 15 Aug 2026 (session A): _dev/verify_leads.py added — the fetch half of
directory link verification, dca_licensees-style: run on a networked machine
(`python3 _dev/verify_leads.py`, or --limit 20 to smoke-test). Covers both
lead files (232 statewide + 22 EBCAMFT). Writes RESEARCH/leads-verified-
<date>.json+.md; builders ship `ok` rows only without review. Also banked
RESEARCH/mind-foundation-apt-2026-08-15.md (full APT program facts, cohort
dates incl. a flagged source contradiction, 12 outcomes, 7 testimonial video
IDs) for queue item 8.

## USER DECISION — 15 Aug 2026: ops-board ask A2 ANSWERED
"Say whether the associates door is right before more are built."

VERDICT: the door CONCEPT is right — keep the /for/associates pattern and
proceed with the remaining doors eventually. But the EXECUTION fails the
bar: "content and design don't look great… messy, cluttered, so much going
on, don't think that is basecamp design."

Consequences, binding until the user says otherwise:
1. Do NOT build the remaining three doors yet. /for/associates must first
   be converted to bc2 (it is one of the two pages excluded from the family
   conversions — the ledger/supervisor-widget CSS port, already item 3 on
   the step-5 list) AND decluttered to the Basecamp standard: one dark band,
   white cards, one accent, generous space, fewer simultaneous elements per
   viewport. The declutter is a content-presentation edit, not just CSS —
   fewer blocks visible at once, the ledger's shelf annotations kept but
   given room.
2. /for/associates after conversion is the TEMPLATE the other three doors
   copy. Getting it right once is the whole point of the user's "cheap
   moment to change direction" framing in the original ask.
3. ops_state.py: mark ask A2 answered with this verdict at the next deploy
   that touches it (avoid concurrent edits; whichever session ships next).

## USER DECISION — 15 Aug 2026: ops-board ask A3 (P2, door build order)
For P2 — the doc carrying 16 rendered mockups (door alternatives + three
sitewide-band options, each with a recommendation): the user chooses
"THE FOUNDATION."

For the executing session: match "The Foundation" against P2's own option
names and apply it as the chosen direction. (Note: a "Foundation" also
appears among the P10 marks in ops/marks.html — if P2's options are named
after marks, confirm the mapping before building; if ambiguous, render the
chosen option once and get a nod before it propagates.) This composes with
the A2 verdict recorded above: /for/associates converts + declutters FIRST,
to the chosen P2 direction, and only then do the remaining doors get built
from that template.

CLAIM (15 Aug 2026, 23:15 PT): session-A agent executing P2 "The Foundation"
on /for/associates — family_for.py conversion + declutter per A2/A3. Other
sessions: stay off for/associates.html, css/house-for.css, _dev/family_for.py
until a shipped/blocked section lands below.

## BLOCKED PENDING USER CONFIRMATION — 15 Aug 2026, 23:20 PT (session A)
P2 "The Foundation" name-match FAILED; nothing was built, per the mandate
("if P2 truly has no option by that name, render nothing and report back").

Findings, checked against the files themselves:
- P2 is ops/stage-doors.html ("Five doors, three ways each", the 16
  mockups). Its complete option roster: Door 1 — 1A The Ladder, 1B The Two
  Questions, 1C The Price Tag. Door 2 — 2A The Placement Desk, 2B The
  Countdown, 2C The Rules Card. Door 3 (associates) — 3A The Desk, 3B The
  Three Questions, 3C The Ledger. Door 4 — 4A The Front Page / The Licensed
  Desk, 4B The Change Log. Door 5 — 5A The Control Panel, 5B The Decision
  Tree. Sitewide band — annotated breadcrumb, next-step band, sticky rail
  (recommendation: breadcrumb + next-step band). The string "Foundation"
  appears NOWHERE in stage-doors.html, in any casing.
- "The Foundation" IS a real option name — but in P10: ops/marks.html mark
  04, three solid bars each wider than the one above, and the marks doc's
  own first pick ("Which three to test — The Foundation, first"). The A3
  verdict's name matches the P10 mark exactly and no P2 option even
  approximately.
- Most probable readings, for the user to pick from: (a) the verdict was
  meant for the P10 marks ask (adopt The Foundation as the site mark), and
  the P2 door answer is still open — in which case the associates door
  rebuild proceeds on P2's own recommendation for Door 3 (3C The Ledger,
  with 3A's six tiles as the expanded state after input and 3B's questions
  directly below the bar), decluttered per A2; or (b) the user wants a new
  Foundation-mark-derived direction not yet drawn in P2, which would need a
  render-once-and-nod cycle first.
- No repo pages, sheets, or passes were touched. The A2/A3 decisions stand
  as recorded; the /for/associates conversion remains queued behind this
  one-word confirmation.
NEXT SESSION: get the user's word, then execute the P2-Foundation plan in
this file's terms (family_for.py + css/house-for.css, mirror gate, one-call
ship) against whichever option the user names.

## CLAIM (15 Aug 2026, ~23:30 PT): session-B agent executing P3 EBCAMFT
practicum directory — new builder _dev/build_bayarea_practicum.py + page
east-bay-practicum-site-directory.html (the curated 21-entry EB CAMFT
directory banked 14 Aug; the settings-universe pair shipped 13 Aug already).
Touches: the new builder, ship.py BUILD, taxonomy_leaves.py, stage_tags.py,
the new page + regenerated hubs/sitemap. Stays OFF for/associates.html,
family_for.py, house-for.css (session A's claim above). A shipped/blocked
section lands below when done.

## SHIPPED — P3 EBCAMFT practicum directory (15 Aug 2026, session B,
## commit `004390d3`)

Live at https://therapistsupport.org/east-bay-practicum-site-directory.html
— byte-identical live vs repo (md5 79160068), all three house sheets
byte-identical live vs repo, sitemap carries it, body `bc2 bcp house`,
zero legacy hash sheets (born pagekit from the loan-forgiveness donor,
converted by family_pk in the same run — the shipped state is bc2-native).

- `_dev/build_bayarea_practicum.py` (new, wired into ship.py BUILD after
  build_findsite): the curated half of P3 — EB CAMFT's public Practicum
  Site Directory 2026-27, ALL data embedded in the builder with per-entry
  src + fetch date. 21 entries (the directory's own counter said
  "Showing all 22 sites"; 21 carried published details at the 15 Aug
  2026 read — the discrepancy is published on the page). Columns per the
  research build-notes: dated acceptance status, mode, hrs/wk, days,
  clinical experience, supervision, populations, school MOUs, BBS flag
  as the directory states it, prerequisites, named contact + email.
  "Not stated" renders as a finding. Chapter credited + linked as the
  listing source throughout; curated-not-exhaustive said plainly;
  trainee frame with §4980.43.3(b) and §4980.42(e) cited. The three
  HIRES-ASSOCIATES sites (Bonita House, Rose MFT, Calliope Coast) broken
  out, Calliope's associates-ONLY / not-practicum distinction published
  as the directory frames it.
- LINKS: verify_leads' JSON only covered the EBCAMFT directory URL
  itself, so every site URL was re-fetched from this workspace 15 Aug
  2026 (4-variant fallback + browser UA): 18/19 answered 200 (finals
  recorded: husd.us, between-therapy.com, trivalleyhaven.org,
  bonitahouse.org); cchealth.org 403s scripted fetches (bot-blocker) and
  is carried on the link form both Bay directories have shipped since 13
  Aug. LifePractice + Rose MFT publish no website — printed as the
  finding. All external links target=_blank rel="noopener noreferrer"
  (guarded).
- Registry seed (entity-free, stale:true per the pk gotcha) +
  taxonomy_leaves "The practicum, and the year before you register" +
  stage_tags (student + associate). Title 55 / description 155 chars,
  asserted in the builder; seo_rules CLEAN at 208 pages.
- Guards in the builder: banned job-availability phrases (acceptance
  language allowed ONLY because it is the source's dated statement, and
  the read-date carry-through is guarded); every site name + verified
  href present; 21 detail entries; no-site finding on both email-only
  entries; field completeness (empty field fails the build).
- GATE (mirror-first at /tmp/mirror, then repo): full ship.py 94/94 on
  the mirror AND the repo; --check 5/5. Playwright over localhost:
  7 pages (new page + one per family: bbs-fees/bca, usf-mft/bcs,
  loan-forgiveness/bcp, amft-3000/tool, about/rest, home) × 375/768/
  1440/2560 = 28 overflow+JS checks, 0 failures; heading/label contrast
  at 1440 on all 7 — 0 findings on the new page and five others.
  PRE-EXISTING defect found and NOT from this run (proven identical at
  HEAD before shipping): about.html (family_rest) breadcrumb renders
  ink at opacity .72 over the dark hero ground (1.21:1). For the
  step-5 session: re-ink `.bcr` on dark grounds in the rest family
  sheet — same class of bug family 1 fixed for its separators.
- Screenshots (1440 top/mid, 375 top/mid) eyeballed: single dark band
  (hero), white cards, one accent, no overflow — the A2 Basecamp-calm
  verdict holds on this page.

Remaining P3: the ~24 Bay org profiles (research banked); the statewide
pre-licensed job-sites page (queue 6) — note for it: the 28-entry "dead"
bucket in leads-verified-2026-08-15.json is mostly bot-blocker false
negatives, browser-check before excluding (see
claude/leads-verification-dead-bucket-warning.md).
