# Therapist Support — complete build-source handoff

**This bundle contains the ONLY copy of every uncommitted change.** Unzip into
`/Users/cava/Developer/therapy-practice-site/` and **commit `mock/` and `_dev/`
to the repo before doing anything else.**

## Why this exists

`github.com/cavatello/therapist-tools` holds **only generated HTML**. There is no
`mock/` directory in it — never committed, and not gitignored either. Cloud
containers are ephemeral. So every session's build source has lived only on the
Mac, and anything a cloud session builds evaporates unless it is committed back
through the device bridge before the session ends.

**That is the actual failure mode.** Fixing it (committing `mock/` and `_dev/`)
matters more than any single item below.

A previous handoff in this session claimed "nothing is lost — this project's
state lives in the repo and the project docs." That was wrong. A later session
verified it and was right to.

---

## What is at risk, ranked

### 1. The Grow seasonality engine — BUILT, never deployed, never committed

`mock/growpage/render.py` and `mock/growpage/_engine_core.js`. This is genuinely
new work that exists nowhere else. Full detail in the section at the bottom.

### 2. `_dev/audit.mjs` — the NARROW check, added minutes ago

Detects a card that is wide while its **content** is not — a different bug from
the container being narrow. Found 17 instances across the site, worst at 32%.
Never run to completion, never committed.

### 3. `mock/cola/build_cola.py` — Option 3 hero, BUILT, deliberately NOT deployed

The compact-band treatment: hero from ~700px to 425px, gains the CTA it never
had, figures beside the copy. **Held back because it still has 55–70px of
horizontal overflow on phones.** The overflowing element is the `.clbig` figure
rows (406px wide inside a 390px viewport, starting at x=39); `min-width:0` plus a
stacked-row media query did not clear it, so the cause is elsewhere — likely the
`.clband` grid item's intrinsic minimum or a `.clwrap` padding interaction. The
live page was restored from production; nothing broken shipped.

### 4. Two mock-ups, delivered but not in the repo

- `mock/content-page-templates.html` — three deep-page templates rendered at
  fidelity, with the breadcrumb component and the page × template matrix.
- `mock/content-blocks-system.html` — the five promotion blocks, Eisenberg's
  Conversion Trinity, the page × block matrix, six rules.
- `mock/landing/herolab.py` — the four hero variants.

### 5. Everything else in `mock/`

All the page builders — the site is generated from these. Losing them means the
site can only be edited as generated HTML.

---

## What IS safe

Everything deployed is live at `therapistsupport.org` and in the
repo as generated HTML: hero v3, the answer grid, the NEXT block, breadcrumbs on
all 14 pages, the CTA rescale, the three-rail documents, the section navs, the
global width pass, and every bug fix. **24 files, all in sync as of the last
check.** None of that is at risk — only the *source it was generated from*.

---

## Open work, in the user's priority order

1. **Grow playable funnel** — engine built (below), UI entirely unbuilt.
2. **Resources page**, Help Scout style.
3. **Citation popover + build-time quote verifier** — do this together with the
   Ramsey sourcing in item 8; they are the same job.

Then:

4. **17 cards wide, contents narrow.** `widen.py` grew the containers; inner
   grids never followed. Worst: index `.lmid` 32%, contact `.sec` 33%,
   about/contact/newsletter `.band` 43%, the `.slab` family 44–50%. The Job
   Advisor form (~900px column in an ~1800px card) is the clearest case; the
   contact form left-aligned in its card is the same root cause. Fix = inner
   grids go multi-column as the card grows.
5. **Cost-of-living Option 3** — finish the mobile overflow (item 3 above), then
   the same treatment for simulator, grow, job advisor.
6. **Cost-of-living hero band** — figures, captions and the worked-example note
   collide in one row at three type scales.
7. **Add the Bay Area** to the area picker. Must be fetched and cited from the
   MIT Living Wage Calculator, not estimated. Constants in
   `mock/cola/content.py` → `AREAS`.
8. **Take-home AND AGI both asked for** on cost-of-living §02. Should be one
   clearly-labelled number, or one derived from the other with the assumption
   stated.
9. **Ramsey section needs real sourcing** — cites the Baby Steps but carries no
   quote or link about student loans specifically, and nothing about California.
10. **Booking widget heading** → "Find a time with Steven". Note the current mock
    says "Shawn"; confirm which is wanted.
11. **Audit gap:** `audit.mjs` samples an element's background in its **static**
    position, so a `position:fixed` element over a dark band is not covered —
    that is how the side nav shipped invisible. Add fixed-element sampling per
    overlaid band.
12. **"Outside California?"** — see `claude/multi-state-expansion.md`. Ship the
    placeholder; do NOT generate other states until the engine is parameterised.
13. Blocks 02 / 04 / 05 from `claude/content-block-system.md`. Job Advisor hours
    trim (24 references to an apparatus with its own page). Return presets and
    the tax profit pull-in — both blocked on sourcing, not effort.

---

## Site conventions

- **Never deploy while `./_dev/sync.sh check` reports DRIFT** on a file you did
  not intend to change — a deploy uploads the whole directory.
- **Deploy flow:** `SendUserFile` → `device_commit_files` to the **macOS** path
  `/Users/cava/Developer/therapy-practice-site/` → wait ~120s → `sync.sh check`
  → verify the live URL with `curl`.
- **Do not run git via `device_bash`** — no network, and it cannot delete, so it
  can strand a `.git/index.lock`. Read-only `git log` / `git ls-files` are fine.
- **`device_bash` cannot delete.** `mv` into a `_to_delete/` subfolder.
- **`tycoon.html` belongs to a different chat session. Never touch it.**
- **`_dev` run order after any page rebuild:** `breadcrumbs.py` → `side_nav.py`
  → `widen.py` → `cta_scale.py` → `link_cards.py` → `linkcheck.py` →
  `sync.sh check`
- **`audit.mjs` must run one viewport per invocation**
  (`node _dev/audit.mjs <port> laptop`), fresh browser every four pages.
- **Sandbox gotcha:** chromium may lose `localhost` access mid-session while
  `curl` still returns 200. `page.setContent()` with the file bytes is the
  workaround — every asset is inlined, so it renders identically.

## Two standing rules

- **No display figure ≥24px above the fold may render as an em-dash.** Show the
  page's own worked example at the same type size, tagged `worked example`, and
  swap to the reader's numbers on first keystroke.
- **Every figure is computed or cited. Never illustrative.**

---

# The Grow seasonality engine

Everything else on the Grow page is an **annual average**, which is why a
caseload plan built from it fails — the year is not flat. Enquiries collapse over
the December holidays and again in high summer; January is the biggest intake
month most private practices see.

## In `mock/growpage/render.py`

- **`SHAPES`** — four twelve-month presets, each with a `note` giving its
  reasoning: `flat`; `typical` (January surge, summer dip, December off a
  cliff); `school` (school year — dead in July, heavy in September); `steady`.
  These are **shapes, not data** — they ship as editable starting points because
  the site does not print unsourced figures as fact.
- **`shapeOf()`** — resolves the shape, applies per-month overrides, then
  **normalises so the twelve multipliers average exactly 1.0**.
- **`monthly(g)`** — walks the year: arrivals scaled by the shape, churn held
  flat (people do not stop coming because it is July — which is exactly what
  produces the summer trough). Returns per-month
  `{m, mult, arrive, leave, load, need}` plus `low`, `lowMonth`, `high`,
  `highMonth`, `swing`, `overMonths`.
- **`grow()` is wrapped** at the bottom so every caller gets `g.monthly`
  attached — the seasonality can never silently disagree with the annual figures
  it derives from.

## In `mock/growpage/_engine_core.js`

`blank()` gained `shape:"typical"` and `months:["", ×12]`. Overrides are stored
as **percentages** of the annual average — a reader typing `70` for July is
unambiguous in a way `0.7` is not.

## The decision that matters most

**Normalisation.** Without it, choosing a spikier shape would silently change the
annual total and every other figure on the page would move for a reason the
reader could not see.

**Verified:** the twelve multipliers sum to exactly **12.000**, and switching
`flat` → `school` gives **identical annual arrivals (12 and 12)** with completely
different month-to-month curves.

Test practice — $180 rate, 20-session tenure, 30 clients, 24 annual churn, 25
sessions/week, one channel at 1000 views / 40 enquiries / 12 clients — caseload
swings **11.5 clients** between Jan (high) and Dec (low). Nothing on the page
could show that before.

```js
S.rate="180"; S.tenure="20"; S.clients="30"; S.churn="24"; S.sessions="25";
S.chan.pt={views:"1000",enq:"40",got:"12"};     // key is "pt", not a name
const g = grow();
g.monthly.rows.reduce((a,r)=>a+r.mult,0)        // exactly 12
g.monthly.swing                                  // 11.5
```

## What is NOT built: the entire UI

`g.monthly` is returned and **nothing renders it.** No shape picker, no
draggable months, no chart. Remaining brief:

1. **Shape picker** — four preset cards, each showing its `note`, writing
   `S.shape`.
2. **Twelve draggable months** writing `S.months[i]` as percentages; blank
   follows the preset, typed overrides that month only.
3. **Month-by-month caseload chart** — `load` against `g.capacity`, trough and
   peak named, `swing` as the headline figure.
4. **The funnel as a real visual** — views → enquiries → booked → retained as
   connected draggable stages, flow scaling live. Not a bar chart of the same
   four numbers.
5. **Visible feedback on every lever** — the number moves, the changed stage
   pulses, the consequence updates in the same frame.

User's words: *"visual funnels so the simulation is actually fun… playable and
fun to mess with… good visual feedback of all the levers."*

---

# VERIFIED: what this bundle can actually rebuild

Not asserted — **run**. Every builder was executed from this bundle alone:

| Builder | Result |
|---|---|
| `growpage/build_grow.py` | wrote 165 kB, 15 inputs |
| `home/build_index.py` | wrote 202 kB, 134 ids, no duplicates |
| `tax/build_tax.py` | wrote 227 kB, 11 inputs, 8 reference blocks |
| `cola/build_cola.py` | wrote 129 kB |
| `amft/build_advisor.py`, `amft/build_hours.py` | OK |
| `remote/build_remote.py` | OK |
| `tmpl/build_tmpl.py`, `blocks2/build_system.py` | OK |
| `landing/herolab.py` | OK |
| `landing/build.py` | OK **only with a `site/` sibling** (see below) |
| `legal/build_legal.py` | needs `site/tools.html` (same cause) |

## THE DIRECTORY LAYOUT MATTERS — read before unzipping

The builders assume this shape:

```
<parent>/
  mock/          the build source (this bundle)
  site/          the published HTML
```

`landing/build.py` and `legal/build_legal.py` **lift the chrome from published
pages** at `../../site/tools.html`. The repo currently keeps its HTML at the
**repo root**, not in a `site/` subdirectory.

So one of these has to happen:

- **(a)** restructure the repo so HTML lives in `site/` and `mock/` sits beside
  it, or
- **(b)** change `SITE_DIR` in `legal/build_legal.py` and the path assertion in
  `landing/build.py` to point at the repo root.

**(b) is smaller and safer.** Two files, one path each. Do it before running
those two builders.

## Three earlier gaps in this bundle, now fixed

Found by trying to run the builders rather than by assuming:

1. **`mock/proto/index.html` was missing** — the practice simulator is spliced
   from it by `home/build_index.py`. Without it that page cannot be rebuilt.
2. **`mock/tree5/fonts/` was missing** — the hero lab and both mock-ups inline
   these as base64.
3. **`mock/tax/_blocks.json`** and other data files were missing — the tax build
   reads 8 reference blocks from JSON.

The very first zip also had a **flattening bug**: `content.py`, `css.py` and
`render.py` from different directories were copied into one folder and
overwrote each other. That zip is void — use this one.
