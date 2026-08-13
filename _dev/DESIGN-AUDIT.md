# Comprehensive design audit — 13 August 2026, end of the skin campaign

Requested by the user after reviewing live: "the content is not rendering
well." This is the honest global assessment, written after six shipped
batches and three full-site automated audits.

## What is now solid, verified, live

- One palette and one type system on all 201 pages: bc2 tokens, Bricolage
  800 headings, Fraunces figures, IBM Plex Mono labels, Inter body.
- Contrast: 3,700+ text elements audited against their REAL rendered
  grounds at 1440 — 0 below 4.5:1. Overflow: 0 pages at 375/768/1024/1440/
  2560. Both re-runnable (audit script pattern is in ROLLOUT.md history).
- Chrome: masthead + The Rule lockup, nav panel (hub card deep), dark
  signup band, deep footer — coherent everywhere.
- Home page: full bc2 markup (option A + waterfall), capped at a 1240px
  well at wide widths.
- Both house sheets content-versioned in every page link — no stale-cache
  loops. (Several "still a mess" reports were the browser's cached copy.)

## What is structurally wrong, and CANNOT be fixed by more skin CSS

The site is old markup wearing a new skin. ~45 legacy sheets (231KB) still
do all LAYOUT. The skin (house-skin.css, ~20KB, sections 1-14) only
re-colors and de-ornaments them. Consequences seen live:

1. LAYOUT breakage survives: the tax page's "reasoning" card scroller and
   the floating "On this page" toc render detached/full-bleed at 27".
   Grid/positioning bugs in old sheets; recoloring cannot touch them.
2. VISUAL DEBT survives: old component shapes (pixel-art promos, ledger
   chrome, game-y sim widgets) read as a different product wearing the
   same colors. "Where is Basecamp style?" is exactly this gap.
3. FRAGILITY compounds: every skin rule is a specificity bet against 45
   sheets. Six batches each fixed a regression the previous batch caused
   (documented in ROLLOUT.md). The whack-a-mole is inherent to the layer,
   not to carelessness.

## The cure is rollout step 5, family by family — the plan that stands

For each family: rewrite its template/pass to emit bc2 components styled
by css/house.css ONLY, unlink every legacy sheet from those pages, delete
the skin sections that existed for that family, re-run the two audits,
ship, verify live. One family per run, mirror-gated, in this order:

  1. article family (.artband/.scband + body) — ~150 pages, biggest win
  2. pagekit directories (.pk-*) — ~25 pages incl. the money tables
  3. hubs (money/licensure/getting-paid/practice/training + resources)
  4. tool pages (simulator, tax, advisor, cost-of-living) — the hardest;
     their inline app CSS must be rewritten against bc2 tokens
  5. discipline library (.dc-*), then stragglers (newsletter, about,
     contact, questions)

house.css grows a small component library as needed (ledger row, gap bar,
pay ladder, cohort calendar, negative-finding card = the approved P12 set).
Every skin section is annotated with what retires when.

## Also open, in queue order

- 90-day rule page (statute verified in RESEARCH/), Ahrefs checkpoint,
  P3 Bay Area directories, doors, band, ask surface, footer index,
  editorial pages; then the two banked new asks (pre-licensed job sites,
  financial assistance incl. SLRP deadline note), then the MIND Foundation
  Berlin expansion (queue item 8).

Bottom line: the theme IS global now; the rendering quality ceiling is the
old markup. Step 5 raises the ceiling. Do not spend another session on
skin rules.
