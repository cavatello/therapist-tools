# Therapist Support — GPT work log

Last updated: August 20, 2026  
Production: <https://therapistsupport.org/>  
Cloudflare Pages project: `therapist-tools`

This is the durable handoff for the substantial hosting, DNS, SEO, publishing, and responsive-design work completed in this conversation. The companion visual dashboard is at <https://therapistsupport.org/ops/gpt/>.

> This document is served under `/ops/` with `noindex, nofollow`. That is not authentication, so credentials and private account identifiers are intentionally omitted.

## Current state

- The production site is hosted on Cloudflare Pages.
- `therapistsupport.org` serves the Pages deployment successfully.
- `www.therapistsupport.org` redirects with HTTP 301 to the apex domain and preserves deep paths and query strings.
- The direct publishing workflow no longer depends on the previous hosting provider.
- The sitemap contains 244 public URLs.
- Structured data is present on 195 pages.
- Strict local SEO validation reports zero findings.
- All 22 project release checks pass.
- The responsive audit covered 245 pages at phone, tablet, and desktop sizes with no horizontal-overflow or JavaScript-error findings.

## Work completed

### 1. Cloudflare hosting and DNS

- Moved authoritative nameservers to Cloudflare:
  - `aaden.ns.cloudflare.com`
  - `cloe.ns.cloudflare.com`
- Configured the apex and `www` records for the Cloudflare Pages project.
- Removed the imported legacy A, AAAA, and old `www` records.
- Rebuilt the `www` Pages custom-domain association.
- Added a permanent `www` → apex redirect that preserves the request path and query string.
- Verified the apex returns HTTP 200 and the redirect behaves correctly on root and deep URLs.

### 2. Cloudflare-only release workflow

- Reworked `_dev/publish.sh` to:
  1. regenerate sitemap and structured data;
  2. run strict SEO checks;
  3. assemble a clean `_publish` directory;
  4. deploy directly to Cloudflare Pages with Wrangler.
- Added `_headers` for security headers, internal-area noindex directives, and long-lived CSS caching.
- Added `_redirects` for site routing behavior.
- Rewrote the project README around the Cloudflare workflow.
- Removed obsolete hosting configuration and helper files.

### 3. Legacy-provider cleanup

- Removed textual references and filenames associated with the prior hosting and repository workflow from the project content.
- Deleted obsolete root configuration files and the retired domain-rebase helper.
- Important nuance: local Git metadata/history may still exist; it is not required for production publishing.

### 4. Technical SEO

- Ran `_dev/discovery.py` and regenerated discovery assets.
- Generated a 244-URL sitemap from the public HTML inventory; internal-only pages remain excluded.
- Added or refreshed structured data on 195 pages.
- Ran `_dev/seo_rules.py --all --strict` with zero findings.
- Confirmed `robots.txt` and response headers exclude `/ops/`, `/seo/`, `/hours/`, and other internal areas from indexing.

### 5. Design-system and CSS review

- Wrote `_dev/DESIGN-SYSTEM-AUDIT-2026-08-20.md`.
- Confirmed the rendered visual system broadly follows the project design language.
- Identified structural debt in older page-family stylesheets and accumulated override layers.
- Replaced an undefined `var(--mono)` usage with the project token `var(--mn)` in `css/house.css`.

### 6. Global responsive improvements

- Enhanced `_dev/mobile_reassert.py` and applied its global last-loaded resilience block to 244 pages.
- Added protections for:
  - horizontal overflow;
  - responsive images and embedded media;
  - shrinking grid/flex children;
  - long heading and prose wrapping;
  - form-control width;
  - visible keyboard focus;
  - 44px navigation and standalone touch targets;
  - responsive tables;
  - mobile stacking for strip layouts;
  - reduced-motion preferences.
- Enhanced `_dev/audit.mjs` to cover public subdirectories, add a tablet viewport, avoid third-party test noise, and provide summary output.
- Updated `_dev/subdirs_check.py` to ignore the generated `_publish/` directory.

## Validation evidence

| Check | Result |
| --- | --- |
| Strict SEO rules | 0 findings |
| Project ship checks | 22 passed, 0 failed |
| Sitemap | 244 public URLs |
| Structured data | 195 pages |
| Responsive coverage | 245 pages × 3 viewport sizes |
| Horizontal overflow | No findings |
| JavaScript errors | No findings |
| Production apex | HTTP 200 |
| Production `www` | HTTP 301 to apex |

The responsive heuristic still emits noisy flags that require human interpretation. Examples include transparent/RGBA contrast calculations, full-card links misclassified as oversized calls to action, and small visible form controls whose wrapping labels provide larger hit areas. Do not represent those heuristics as a completely clean accessibility audit.

## Known follow-ups

1. Fix the apparent typo in the GA4 stream URL (`therapsitsupport.org`) and verify events reach the correct property.
2. Investigate the Search Console discrepancy between submitted/indexed reporting and the pages already receiving impressions.
3. Consolidate legacy stylesheet layers into fewer canonical components and tokens.
4. Manually review the remaining responsive/contrast heuristic flags in a real browser.
5. Confirm the legacy local auto-publish launch agent is disabled if automatic commits are no longer desired.
6. Continue the planned competitor, inbound-marketing, and content-production work; that larger editorial program was requested but was not executed as part of this infrastructure/CSS pass.

## Continued SEO work — August 20, 2026

- Confirmed the misspelled analytics domain is not present in production source; it must be corrected in the GA4 web-stream configuration.
- Rewrote four priority title tags to better match California-specific search intent:
  - California therapist rates: insurance versus private pay
  - Psychedelic therapy training in California
  - California therapist insurance reimbursement rates
  - California AMFT 3,000-hours calculator and timeline
- Repaired two meta descriptions that previously ended mid-sentence: the psychedelic-training guide and AMFT hours calculator.
- Updated the SEO strategy to record the Cloudflare migration and post-cutover verification as complete rather than blocked.
- Rebuilt `/seo/` as a data-backed SEO command center using a versioned `seo/data.json` snapshot.
- Connected fresh GA4 and Google Search Console reporting for search KPIs, daily traffic, organic landing-page engagement, and event status.
- Added a California term/competitor watch based on a live result-set check, plus a dated work-to-impact ledger for future before/after comparisons.
- Diagnosed severe bot-like pollution in Direct traffic and explicitly excluded it from editorial-impact conclusions; Organic Search remains highly engaged.
- Inspected five priority URLs in Google Search Console. All five passed indexing, mobile crawl, canonical, fetch, and breadcrumb checks.
- Confirmed `newsletter_signup` is already configured as a GA4 key event and corrected the SEO dashboard's earlier configuration warning.
- Strengthened the California LMFT continuing-education page with a query-aligned description, current freshness metadata, and visible-answer-backed FAQ structured data.

## Key project files

- `README.md` — Cloudflare-oriented project handoff
- `_dev/publish.sh` — production build and deployment
- `_dev/DESIGN-SYSTEM-AUDIT-2026-08-20.md` — CSS/design review
- `_dev/mobile_reassert.py` — global responsive layer generator
- `_dev/audit.mjs` — multi-viewport audit runner
- `_dev/discovery.py` — sitemap and structured-data generation
- `_dev/seo_rules.py` — strict SEO validation
- `_dev/subdirs_check.py` — project directory checks
- `_headers` — security, caching, and noindex response headers
- `_redirects` — redirect configuration
- `seo/index.html` — SEO dashboard
- `seo/strategy.md` — SEO strategy document

## Safe workflow for future agents

1. Read this work log and `README.md` before changing hosting, DNS, or publishing.
2. Preserve the Cloudflare-only production path unless the owner explicitly requests another migration.
3. Run `python3 _dev/ship.py --check` before publishing.
4. Use `_dev/publish.sh` for production deployment; it runs discovery and strict SEO checks again.
5. Verify the apex URL and at least one `www` deep-link redirect after deployment.
6. Update this file and the `/ops/gpt/` dashboard whenever a substantial operational workstream is completed.
