# Design-system implementation audit — 20 August 2026

## Verdict

The UI broadly follows the visual specification in `ops/house-style.html`: restrained green/neutral surfaces, one warm accent, readable body copy, compact mono labels, Fraunces figures, consistent chrome, and deliberate content slabs. It does **not** yet follow that specification as a clean implementation system. The same appearance is assembled from a canonical layer plus legacy page-family CSS and corrective overrides.

## Evidence reviewed

- `ops/house-style.html` and `_dev/DESIGN-AUDIT.md`
- 57 stylesheets in `css/` (6,371 lines)
- 247 HTML documents and all stylesheet references
- Palette, type-size, token, selector, and legacy-wrapper searches
- Full SEO and structured-data regeneration

## What conforms

- House tokens converge on ink `#1B2420`, pine `#2C6350`, deep green `#123C30`, paper `#F6F8F6`, white cards, muted text `#5F6A64`, hairlines `#DFE4E0`, and pale gold `#FFE7A3`.
- Core type roles are present: Inter for display/body, Fraunces for figures, IBM Plex Mono for labels.
- `house.css` defines the intended base spacing, radii, typography, surfaces, and heading system.
- Family sheets provide consistent navigation and page-family behavior.
- The prior rendered audit recorded no contrast failures or horizontal overflow at tested viewports.

## Material deviations and risks

1. **Parallel token systems.** Legacy sheets still declare older colors before house layers override them. That violates the specification's “one stylesheet / eight color tokens” implementation goal even when the final screen looks correct.
2. **Override architecture.** `house-skin.css` and repeated token blocks in other house sheets repair older page families after the fact. Selector ordering therefore affects correctness and increases regression risk.
3. **Type-scale fragmentation.** The most common fixed micro-sizes are 12px, 10.5px, 13.5px, and 9.5px. Some suit labels and dense tools, but they are not expressed through a shared scale and the smallest need accessibility scrutiny.
4. **Palette duplication.** Equivalent colors appear in multiple forms and semantic values are repeatedly hard-coded instead of using house tokens.
5. **Legacy structure.** Much of the HTML still carries legacy skin/layout classes. Presentation is consistent, but markup is not yet built from the final article, directory, hub, and tool templates.

## Required remediation order

1. Keep `house.css` as the single token and base-type authority.
2. Move shared navigation, footer, signature, slab, card, and callout rules into explicit components.
3. Convert article pages first, then directory pages, hubs, and tools.
4. Remove each legacy sheet only after its page family no longer references it; delete matching corrective rules at the same time.
5. Replace repeated literal colors and font sizes with semantic tokens.
6. Re-run viewport, contrast, focus, reduced-motion, and overflow checks after every family conversion.

## Acceptance criteria

- One authoritative token declaration; no page-family redeclaration of core colors or fonts.
- No corrective skin layer.
- Every public page uses a documented template.
- Exactly one intentional slab per content page.
- Body copy remains at least 16px on narrow screens; sub-12px text is limited to nonessential labels.
- Automated checks show no WCAG AA contrast, keyboard-focus, reduced-motion, or horizontal-overflow failures.

The next sound move is a family-by-family template migration, not another accumulation of global overrides.
