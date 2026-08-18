#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The pipeline, written down, because it was only ever in someone's head.

WHY THIS EXISTS

There are around fifty passes in `_dev/`. Each one is idempotent, guarded and
well documented on its own terms, and none of them says what has to run before
it or after it. The order was reconstructed from scratch every session by
reading the marker comments left in a built page, and getting it wrong is not
theoretical:

  - `_dev/footer_band.py` before `_dev/footer_order.py`, or the band lands above
    the up-link and stays there.
  - `_dev/extract_css.py` after every pass that emits a <style> block, or that
    block ships inline on 160 pages instead of being hoisted once.
  - `_dev/css_dedupe.py` after `_dev/extract_css.py`, or there is nothing yet to
    dedupe.
  - `_dev/discovery.py` last, because it derives the sitemap from the pages that
    exist at the moment it runs.

Run in the wrong order the passes do not error. They produce a site that is
subtly wrong, and every guard still says "clean" - because each guard checks its
own pass, and nothing checked the sequence. This file is the sequence.

    python3 _dev/ship.py            build, then verify
    python3 _dev/ship.py --check    verify only; writes nothing
    python3 _dev/ship.py --from mobile_floor    resume at a stage

It stops at the first failure and prints that pass's own output, because a pass
that fails halfway leaves the site in a state the passes after it will happily
build on top of.
"""
import os, re, sys, time, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

# (module path relative to the repo root, why it sits here)
#
# BUILDERS come first: they write raw pages from data, carrying only borrowed
# chrome. Everything after this point decorates what exists.
BUILD = [
    ("_dev/build_insurance.py", "the liability insurance directory"),
    ("_dev/build_cases.py", "the discipline case library - hub plus 30 pages"),
    ("_dev/build_assocpay.py",
     "what associate jobs pay in LA and the Bay Area. A BUILDER, not a pass: "
     "it writes its page whole from published pay scales every run, borrowing "
     "chrome from the donor, so everything in STRUCTURE decorates it like any "
     "other page"),
    # The five pages the Facebook sweep produced. All five share
    # `_dev/pagekit.py`, which carries the chrome-borrowing routine and one
    # byte-identical style block - so extract_css hoists it once and
    # css_dedupe collapses the five copies to one. They are BUILDERS: each
    # rewrites its page whole every run, and everything in STRUCTURE
    # decorates the result.
    ("_dev/build_unpaid.py",
     "the wage claim an associate can file when the non-clinical hours go "
     "unpaid, and why the Board is not the place to file it"),
    ("_dev/build_exams.py",
     "seven quarters of both published pass rates for all seven California "
     "behavioral sciences exams, transcribed from the board packets"),
    ("_dev/build_times.py",
     "the Board's own processing times, with the methodology break at "
     "Q2 FY 2025/26 kept as two series rather than spliced into one"),
    ("_dev/build_trackers.py",
     "the five BBS hours trackers compared, with what the Board actually "
     "accepts as a supervisor signature and who is behind each product"),
    ("_dev/build_outofstate.py",
     "whether a California associate can accrue hours from another state - "
     "the Board has published the answer five times and nobody reads it"),
    # The other direction: not "can my hours travel out of California" but
    # "can my license and my hours travel in". Same reader, opposite
    # question, and the loudest unserved theme in the associate group.
    ("_dev/build_oos_license.py",
     "bringing a license from another state - Path A, Path B, and why "
     "continuing education cannot close a transcript gap"),
    # Why half an associate's applications never get a reply. A billing
    # rule, not an hour count - and the loan-repayment tier nobody in
    # those threads mentioned.
    ("_dev/build_gethired.py",
     "getting hired as a California associate - which settings can "
     "legally bill for a pre-licensed clinician, and what that is worth"),
    ("_dev/build_ninety.py",
     "the 90-day rule page - path 03's missing content, statute-verified; "
     "chrome comes from the fees page so it rebuilds inside the family"),
    # The follow-up question the hiring page raises and does not answer:
    # so which employers? Reads _dev/hrsa_stats.py, written by
    # _dev/hrsa_sites.py from HRSA bulk downloads.
    ("_dev/build_forgiveness.py",
     "which California employers unlock loan forgiveness - four programs, "
     "three different tests, and only two that reach an associate"),
    # And the named employers behind one of those four settings. Reads
    # _dev/hc_orgs_data.py, written by _dev/hc_orgs.py, which fetches every
    # candidate domain before it is allowed to ship as a link.
    ("_dev/build_safetynet.py",
     "the 218 California health center organizations by name, with links "
     "that were checked before publication"),
    ("_dev/build_baysites.py",
     "P3 page one - the Bay Area practicum-sites directory: five program "
     "clinics, nine county plans, the health centers and the nonprofit "
     "clinical agencies, availability language banned by guard"),
    # P3's last item: one leaf per curated org, from the banked research.
    # After build_baysites in the list but independent of it - the
    # directories link the profiles via the shared orgprofile_data map.
    ("_dev/build_orgprofiles.py",
     "the 24 Bay Area organization profiles - one ts:leaf page per "
     "curated org: what it is, what its own site publishes about "
     "clinical training with every fact linked and dated, and the "
     "questions to bring; availability language and personal contacts "
     "banned by guard"),
    # Editorial tier 1, item 4: the prose front door to the simulator.
    # Introduces NO figures of its own - a guard asserts every number
    # it uses exists on the page it links it to.
    ("_dev/build_viable.py",
     "the is-therapy-financially-viable page - the whole career in "
     "arithmetic, every figure lifted from the page that computes it, "
     "ending at the simulator"),
    # Editorial tier 2, item 5: the amended 16 CCR 1811, from the
    # Board's own 03/2026 fact sheet and example sheets. A guard fails
    # the build if the example sheets' fictional names leak in.
    ("_dev/build_adrules.py",
     "the April 2026 advertising rule as a checklist - three elements "
     "for licensees, five for associates, five for trainees, and the "
     "non-compliant patterns from the Board's own examples"),
    # Editorial tier 2, item 6: 16 CCR 1815.5 as amended effective
    # 1 Jan 2026. The page is mostly SUBTRACTION - the queued research
    # called the per-session name-and-location duty new, and it dates
    # to 1 July 2016; so does the out-of-state subdivision. A guard
    # fails the build if that framing is ever reintroduced.
    # Editorial #9: the whole entry cost, assembled. Inherits
    # build_viable's no-new-numbers rule - a FIGURES guard asserts every
    # amount appears on the page it is attributed to, and four costs are
    # deliberately left unpriced rather than sourced from marketing.
    # Must run AFTER the pages it lifts from are built.
    ("_dev/build_cost.py",
     "what licensure actually costs - about $549 paid once and $624 to "
     "$924 across the route, against a degree of $37,800 to $152,340, "
     "every figure lifted from the page that documents it"),
    # Editorial #8: the prep market. Prices from each vendor's own page,
    # pass-rate claims quoted and NOT compared, because they are three
    # different kinds of statement. A guard fails the build if a tracking
    # parameter appears in a vendor link - the owner's decision on
    # 17 Aug 2026 was plain links for now.
    ("_dev/build_prep.py",
     "exam prep compared - $139 to $620, and why the advertised pass "
     "rates cannot be ranked against each other or the Board's"),
    ("_dev/build_telehealth.py",
     "the telehealth standard of practice - the two subdivisions the "
     "2026 amendment actually touched, the decade-old duty most "
     "summaries call new, and what naming the HIPAA Security Rule "
     "asks of a solo practice"),
    # The method page the directory and the rules page both point at:
    # whose job the search is, the statutory strikes, the four shelves,
    # and the questions that protect the hours. Invents no facts - it
    # sequences ones already verified on those two pages.
    ("_dev/build_findsite.py",
     "P3 page two - the practicum-search method page: the program's "
     "placement model first, the five statutory strikes, six-plus "
     "applications across the four shelves, and the paper trail"),
    ("_dev/build_trainprogs.py",
     "P3 item three, first cut - the ten Bay agencies whose own sites "
     "publish a clinical training program, each held to its own words, "
     "availability language banned"),
    ("_dev/build_jobsites.py",
     "the statewide pre-licensed employer directory - only the 61 orgs "
     "whose own sites state associate or pre-licensed roles, each row "
     "linking the page that says so, read on one dated day"),
    # The curated half of P3: EB CAMFT's public practicum directory,
    # every entry dated to its read, every site link fetched, the
    # chapter credited as the source of the listing.
    ("_dev/build_bayarea_practicum.py",
     "the EB CAMFT practicum-site directory annotated - 21 dated "
     "entries, the three hires-associates flags broken out, links "
     "fetched before publication"),
    # The one program of the four that reaches an associate, explained in
    # full - including the 32-direct-hour obligation and the tax question
    # HCAI does not answer.
    ("_dev/build_mbhslrp.py",
     "MBH-SLRP in full - the three tiers, the conditions nobody mentions, "
     "and where the published sources disagree"),
    # What a county job actually pays, from the State Controller's bulk
    # files. Reads _dev/county_pay_data.py, written by _dev/county_pay.py
    # from three years of returns cached under _dev/_cache.
    ("_dev/build_countypay.py",
     "county therapist pay - every county ranked by published salary "
     "range, and the 2.8x spread across the state"),
    # The stage the site had nothing for: already enrolled, about to see
    # clients. Reads _dev/practicum_data.py, written by _dev/practicum.py
    # from the 78-program research file. The placement taxonomy is the
    # only comparison of its kind anywhere.
    ("_dev/build_practicum.py",
     "the practicum year - the seven trainee rules, and which of the 78 "
     "programs finds your site and which leaves it to you"),
    # And the stage before that one: deciding at all. Reads
    # _dev/degree_pipeline.py, written by _dev/ipeds_degrees.py from the
    # federal completions survey - the only series that says how many people
    # a year California puts into this.
    # Where the application form actually is. Reads _dev/county_portals_data.py,
    # written by _dev/county_portals.py, which fetches all 58 before shipping.
    # Eight counties have a plausible-looking portal URL that belongs to a
    # city, a court, or nobody.
    ("_dev/build_portals.py",
     "all 58 county job portals, verified - and the eight guessable URLs "
     "that are the wrong employer"),
    # Where to find a supervisor, which the Board answers nowhere because it
    # keeps no roster. Reads _dev/supervisor_lists_data.py, written by
    # _dev/supervisor_lists.py, which fetches every candidate directory before
    # shipping - several of the addresses people are still sent to have been
    # sold or have stopped resolving.
    ("_dev/build_supervisor.py",
     "where a California supervisor list actually is - nine chapters of "
     "twenty-three - and the private-practice rule that decides whether the "
     "person you find can count your hours at all"),
    ("_dev/build_careerchange.py",
     "the numbers somebody retraining deserves first - the pipeline, the "
     "three licenses on statute rather than temperament, and the attrition "
     "visible in the Board's own reporting"),
    # Not a builder: it inserts one section into a hand-written page. It sits
    # in BUILD anyway, because the section nav on that page is generated in
    # STRUCTURE from the headings that exist - a content edit made after that
    # point would ship a heading the page's own nav does not list.
    # The county atlas. Reads `_dev/dca_stats.py`, which is written by
    # `_dev/dca_licensees.py` from the state's monthly register. Every
    # figure on the page is derived at build time, so when the register
    # is refreshed the page moves with it and no prose needs editing.
    # The first stage door. Reads the `stages` / `stage_note` tagging that
    # _dev/stage_tags.py writes into the registry, so its shelf annotations
    # cannot drift from the pages they describe.
    ("_dev/stage_tags.py",
     "which stage of the path each page is written for, and the one line "
     "saying what it tells that reader - the door below reads this"),
    ("_dev/build_forassociates.py",
     "/for/associates - the whole 3,000-hour requirement in one bar, and "
     "every page written for somebody counting them"),
    ("_dev/build_forstudents.py",
     "the second stage door - /for/students to the associates pattern: "
     "cold-arrival hero, the four starting questions, and the shelf "
     "built from hand-written student stage notes"),
    ("_dev/build_fordeciding.py",
     "the third stage door - /for/deciding: the route and its cost, "
     "county pay at the end, the 78 programs on placement, from "
     "hand-written deciding stage notes"),
    ("_dev/build_forlicensed.py",
     "the fourth and last stage door - /for/licensed: take-home at your "
     "rate, panel arithmetic, the entity decision, and the CE clock, "
     "from hand-written licensed stage notes"),
    ("_dev/build_atlas.py",
     "all 165,000 California licensees counted by county, with the "
     "associate-per-supervisor ratio and the delinquency rates"),
    # The state comparison. Reads `_dev/state_workforce.py` - BLS OEWS
    # plus Census population plus each state's own license titles.
    # The page leads with the titles because the obvious chart (MFTs
    # per capita) measures statutes rather than supply, and a guard
    # fails the build if that warning ever moves below the charts.
    ("_dev/build_states.py",
     "what a licensed therapist is called in 17 states, and the "
     "per-capita comparison that survives those titles"),
    # Rollout step 4: the home page, rebuilt whole to option A + the
    # waterfall. A builder like any other - everything in STRUCTURE
    # decorates its output; home_doorway and stage_router detect the new
    # main and skip their old landing work.
    ("_dev/build_home.py",
     "the option-A home page - the tool card with the take-home waterfall, "
     "the six claim rows, one slab"),
    ("_dev/payroll_ops.py",
     "what it costs to RUN the payroll - the EDD registration trigger, "
     "published prices for one employee, and the workers' compensation class "
     "code, onto the page that already prices the hire"),
    # Editorial #7 (paying-your-associates) resolved as a SECTION, not a
    # page: three live pages already carry the $70,304 floor, LAB 226.2 and
    # the published scales, and a fourth URL would compete with all of
    # them. What was missing is that the employer-side page carried none of
    # it. Must run AFTER payroll_ops - both rebuild the same authored rail.
    ("_dev/wage_floor_ops.py",
     "how an associate may lawfully be paid - the $70,304 exempt floor with "
     "its arithmetic, the closed list of exempt professions, and per-session "
     "pay as piece rate under LAB 226.2, onto the employer-side page"),
]

# STRUCTURE. Chrome, navigation, cross-links, the blocks that carry meaning.
# restyle is first because every later pass assumes the masthead exists.
STRUCTURE = [
    # FIRST in STRUCTURE, and it only takes something away. An article page is
    # not rewritten by any builder, so a slab that shipped last time is still
    # in the tree now - and the family passes carry hardcoded lists of the
    # classes their pages may wear, so `family_art.py` fails 7 pages with
    # "uncovered classes: eb mark p8slab slab". Taking the slab out here and
    # putting it back in LAST means every pass in between sees the site it
    # would see on a virgin build, and none of them has to learn about a
    # component that is added after they have all run.
    ("_dev/slab_rollout.py --strip",
     "the slabs from the last build, removed until LAST puts them back"),
    ("_dev/restyle.py", "masthead, nav panel and the nav script, on every page"),
    ("_dev/ehr_market.py",
     "the whole practice-software market with every published price, in place "
     "of the two-product framing. Early in STRUCTURE for two reasons: it sets "
     "ts:number, which pixel_concepts reads to build the In-short card, and "
     "its prose has to reach american.py like any other copy"),
    # The registry handover, both halves, in the order the two passes
    # were designed to run in. `registry_meta` writes each page's
    # library metadata INTO the page; `registry_sync` reads it back and
    # rebuilds registry.json from the pages, so the page is the source
    # of truth and a new one joins the library with no central edit.
    #
    # They were both unwired, and the cost showed the moment a builder
    # rewrote a page: mft-programs-california.html came out of
    # mock/mftguide/build_programs.py with no `ts:` block at all, which
    # made it invisible to every hub on the site and failed
    # stage_router two stages later. Wired, that repairs itself.
    #
    # ORDER MATTERS AND THE FAILURE IS SILENT. registry.json holds
    # UNESCAPED text; the page holds it HTML-escaped in a content=""
    # attribute. meta escapes on the way in, sync unescapes on the way
    # out. Put an already-escaped string into the registry by hand and
    # meta escapes it twice - "&rsquo;" becomes "&amp;rsquo;" and the
    # In-short card renders the entity as text. That is how four pages
    # broke the first time these ran together.
    ("_dev/registry_meta.py",
     "each page's library metadata, written into the page"),
    ("_dev/registry_sync.py",
     "registry.json rebuilt from the pages that now carry it"),
    ("_dev/taxonomy_leaves.py",
     "the 48 case pages become leaves and three reference pages get real\n      clusters, so no topic hub ends in a 50-page catch-all. BEFORE\n      uplinks, which picks a page's siblings out of the registry"),
    ("_dev/hub_clusters.py",
     "sync the licensure hub's cluster sections to registry.json, "
     "lifted from mock/library/build_library.py's output rather than "
     "authored. After the builders, because the registry describes "
     "pages that must already exist; before uplinks and breadcrumbs, "
     "which read the hub's links"),
    ("_dev/uplinks.py", "the More-on-this block"),
    ("_dev/breadcrumbs.py", "breadcrumb trails where a trail exists"),
    ("_dev/link_sinks.py",
     "one contextual sentence into the two pages everything linked to and\n      that linked to nothing back"),
    ("_dev/pixel_concepts.py", "the In-short card and the provenance strip"),
    ("_dev/footer_band.py", "the signup band - inserts ABOVE the up-link"),
    ("_dev/footer_fix.py", "footer colour overrides"),
    # The "you are here" shell from the stage-doors proposal: S1 (one
    # annotated line above the article) + S3 (the next-step band after
    # it), on every stage-tagged page. Runs after the doors exist and
    # after footer_band so S3 has its anchor; the door counts come from
    # the same registry tagging the doors read.
    ("_dev/stage_shell.py",
     "the you-are-here shell - S1 stage line above the article and the "
     "S3 next-step band after it, on every stage-tagged page"),
    # The question box home option F mocked and the options doc queued.
    # After the door builders (it inserts into their output) and before
    # form_inline, whose one-handler-per-page guard it is written to
    # respect (property assignment, different form class).
    ("_dev/ask_surface.py",
     "the ask-a-question surface - the question box on the home page "
     "and inside each stage door, posting to the disclosed Formspree "
     "endpoint with the asking page named"),
    ("_dev/footer_index.py",
     "the footer index generated from the registry - the four doors and "
     "the five topics with live counts, plus the guard that fails the "
     "build when an indexable page is unreachable from the index"),
    ("_dev/affiliate.py",
     "the affiliate disclosure in every footer, a visible tag beside every\n      affiliate link, and rel=sponsored on each. Never wired, which is why\n      nobody noticed its footer anchor had gone stale and it was leaving the\n      disclosure on 4 pages of 177. AFTER the footer passes, whose sentence\n      it appends to"),
    ("_dev/analytics.py",
     "one GA4 property on every page. It was never in this list, which was\n      survivable only because nothing regenerated a page after it had been\n      tagged - until the nine library hubs were rebuilt from registry.json\n      and arrived untagged, and analytics_events stopped the build asking\n      for exactly this pass. It must run BEFORE analytics_events, which\n      binds listeners to the tag this one installs"),
    ("_dev/analytics_events.py", "the event listener"),
    ("_dev/clarity.py",
     "Microsoft Clarity, with data-clarity-mask on every <body> so the whole "
     "document is masked from the markup and not from a dashboard setting "
     "somebody could change"),
    ("_dev/tool_analytics.py",
     "how the seven calculators are actually used - behaviour only, guarded "
     "so no typed value can ever leave the browser"),
    ("_dev/error_tracking.py",
     "uncaught errors, failed resources and rage clicks. Before this, a broken "
     "calculator and an uninterested reader looked identical"),
    ("_dev/form_inline.py",
     "both Formspree forms answer on the page instead of navigating to "
     "formspree.io. After footer_band, which is what puts the signup form on "
     "every page in the first place"),
    ("_dev/mobile_nav.py", "the mobile nav affordance"),
    ("_dev/touch_polish.py", "tap targets"),
    ("_dev/american.py", "American spellings in prose"),
    # Plain nouns instead of a metaphor. "Four gates, all four must close" was
    # in the site nav, so it was on 199 pages - and it framed the 3,000 as the
    # thing that decides your date, which it almost never is. Runs after every
    # builder, like american.py, so a builder cannot reintroduce it.
    ("_dev/plain_gates.py",
     "requirement for an hour minimum, checkpoint for an academic step, and "
     "no unexplained \"gate\" anywhere"),
    ("_dev/american_js.py", "American spellings inside script string literals"),
    ("_dev/block_removal.py",
     "removes the self-describing blocks that were asked for by name. Destructive, "
     "so it refuses to cut when a match runs past a plausible size"),
    ("_dev/payer_links.py",
     "verified enrolment links for every payer, plus NPPES, CAQH, Medi-Cal "
     "and Medicare. Every URL opened and checked, not guessed"),
    ("_dev/headline_figures.py",
     "fixes a chosen headline figure on an article whose builder no longer "
     "runs"),
    ("_dev/infographics.py",
     "the visual vocabulary - five CSS shapes and the pages that use them. "
     "Before FLOORS, so block_spacing and content_frame see the figures"),
    ("_dev/hub_hero.py", "the AIDA heroes, with every figure measured"),
    ("_dev/hub_owid.py",
     "the scope line, the most-asked links and the Key insights block on the\n      five topic hubs. Also never wired, for the same reason analytics.py\n      was not: nothing regenerated a hub, so its output survived by luck.\n      Regenerating the hubs from registry.json deleted all five blocks and\n      no guard noticed, because a missing section is not a broken one"),
    ("_dev/home_doorway.py",
     "the fourth audience card on the home page, for people who have not\n      started yet. BEFORE stage_router, which wraps each card and adds the\n      situation link under it"),
    ("_dev/stage_router.py", "the situation router on resources.html"),
    ("_dev/footer_order.py",
     "MOVES the band down against the footer. Must follow footer_band and "
     "pixel_concepts, both of which insert in the same place"),
]

# FLOORS. Colour, tap area, spacing. These read the finished markup, so they run
# after everything that emits markup and before the CSS is hoisted.
FLOORS = [
    # The house style (board P8) states its tokens as exact hex. Seven of
    # the eight were wrong on all 234 pages - close, never equal, which is
    # how a design system dies quietly. These two conform the palette, the
    # body metric and the decorative fills to it. Both edit or override
    # ONLY hand-authored sheets: the content-addressed css/<hash>.css
    # sheets must keep their bytes, because the filename IS the hash and
    # the family passes carry hardcoded name lists.
    # They run BEFORE the contrast floors, because they move --ink and
    # --gold and the floors measure against whatever the palette is.
    ("_dev/house_tokens.py", "the P8 palette and the body metric"),
    ("_dev/contrast_pass.py", "label contrast"),
    # The second sweep: text coloured for the OPPOSITE surface from the
    # one it sits on - dark-band rules reaching into light cards nested
    # in the band, and the reverse. 31 signatures over 16 pages, worst
    # 1.05:1. Per-context, so it cannot fold into contrast_pass's flat
    # single-colour list. Verify with _dev/_paths.mjs after any change.
    # The masthead still carried a dark header's pill and a three-column
    # grid from when the nav had three items. It has seven, and the
    # masthead is white. Verify with _dev/_navcheck.mjs.
    ("_dev/nav_skin_fix.py", "the masthead's dark-header leftovers"),
    # The sc family loads three stylesheets where every other family
    # loads twelve-plus, and two site-wide components (the freshness
    # block, the up-link block) were defined in none of them - so all 66
    # school pages shipped them as unstyled markup. Copies the canonical
    # rules from house-art.css, rewriting body.bca to body.bcs.
    # Verify with _dev/_uncovered.mjs.
    ("_dev/sc_components.py", "the school pages' two unstyled components"),
    ("_dev/dark_band_labels.py", "dark-band eyebrow contrast"),
    ("_dev/token_floor.py", "the hex tokens under the floor"),
    ("_dev/chrome_armor.py", "chrome that has to outrank the page body"),
    ("_dev/mobile_floor.py", "overflow, hit area, and the 12px text floor"),
    # Three decoration passes that were written, guarded and never wired.
    # Each was verified idempotent before wiring - run twice against a
    # copy of the tree, the second run changes nothing - which is the
    # only safe way to tell "this pass does missing work" from "this
    # pass re-does its own work every time".
    ("_dev/cta_scale.py",
     "the page-foot CTAs back to a button's proportions, on the five "
     "calculator pages that still had them page-width"),
    ("_dev/fill.py",
     "the reading cards narrowed to the column they actually hold"),
    ("_dev/mobile_hero.py", "heroes that fit a phone"),
    ("_dev/block_spacing.py", "every injected block owns the space beneath it"),
    ("_dev/content_frame.py",
     "one content frame: breadcrumb rhythm, headline measure, and wide blocks "
     "that used to run past their column with no scroll affordance"),
    ("_dev/wide_measure.py",
     "line length on a 27-inch 5K, where the failures are the opposite of the "
     "mobile ones and nobody looks for them"),
    ("_dev/nav_type_floor.py",
     "the nav panel's column headings were 9.5px on every page - the smallest "
     "type on the site, and the only thing naming each group of links"),
    ("_dev/one_grid.py",
     "one page grid, so a headline starts where the logo starts. Last in "
     "FLOORS because it has to outrank every container width set above it"),
    ("_dev/rates_grid.py",
     "rates.html's four stray blocks onto that same grid. After one_grid, "
     "because it aligns them to what one_grid puts the article body on"),
]

# SEO. Head-level facts, then the sitemap and structured data, which must see
# the final set of pages.
SEO = [
    ("_dev/seo_head.py", "a canonical and a lang on every published page"),
    ("_dev/seo_meta.py", "titles and descriptions inside what a result shows"),
    ("_dev/social_cards.py",
     "an Open Graph and Twitter card on every indexable page. AFTER\n      seo_meta, because a derived card copies the title and description\n      that pass has just finalised"),
]

# CSS. Hoisting comes after every <style> block exists, and nowhere else.
CSSCHAIN = [
    ("_dev/extract_css.py", "hoist blocks shared by 4+ pages into css/"),
    ("_dev/css_cdo_fix.py", "HTML comments that break a stylesheet. After extract"),
    ("_dev/css_dedupe.py", "superseded links. After extract"),
]

LAST = [
    # tools.html is a meta-refresh redirect stub, ts:skip and not in the
    # sitemap - and this pass had never been wired, so every appending pass
    # in the pipeline had been decorating it for months. It reached 370
    # lines and SEVENTEEN stylesheets, one of which (css/house-skin.css)
    # was the last thing keeping the retired skin on the live site. Runs
    # first in this stage: after everything that appends, before anything
    # that reads the finished page.
    ("_dev/build_redirect.py",
     "tools.html back down to a 44-line redirect stub with no stylesheets, "
     "no webfonts and its ts:skip intact"),
    # A page that names a typeface FIRST in a stack and never loads it ships
    # in the fallback, silently. rates.html set 'Newsreader' and 'IBM Plex
    # Mono' and loaded neither, so the whole editorial page had been
    # rendering in Georgia and the system mono. Found by type_census.py,
    # which is the only check that pairs what the CSS asks for with what the
    # <link>s load. After build_redirect, so the stub is not given faces.
    ("_dev/font_links.py",
     "every page loads every typeface it sets at the head of a stack"),
    # The palette. house_tokens.py conformed the eight tokens; this conforms
    # the 113 near-misses that were quietly sitting beside them - 1,363
    # uses, #16211B alone 430 times, twelve units from --ink. After the CSS
    # chain so hoisted sheets are included, before discovery and linkcheck
    # so the repointed content-addressed links are what they see. It also
    # conforms _dev/chrome_donor.html, because eight builders stamp that
    # file's chrome onto real pages - skipping it cost a whole pipeline run
    # to 1,008 dangling <link>s. Verify with palette_census.py --check and
    # _dev/_contrast_audit.mjs.
    ("_dev/palette_conform.py",
     "113 off-palette colours onto the twelve they were approximating"),
    # P8, verbatim: "Flat fills, hairline ring + soft shadow" and "No
    # gradients from anywhere." The rendered audit found gradients on 32
    # pages. This flattens the 73 that are DECORATION and leaves the 52
    # that are not - the scroll fades, the shadow affordances, the
    # scalloped slab masks P8 actually specifies, and the gold highlighter
    # rule under the home headline. Every replacement is one of the
    # gradient's own stops, which is what the reverted flat_fills.py got
    # wrong. After palette_conform, so the stops it matches are already
    # conformed.
    ("_dev/flat_bands.py",
     "decorative gradients flattened to one of their own stops"),
    # Twenty corner radii to two, and pills to 6px on the twelve rules
    # where a pill is a BUTTON. Progress-bar ends, circles and badges keep
    # their capsule - "no pill buttons" is a rule about buttons.
    ("_dev/radius_floor.py",
     "every corner radius onto --r 10px or --rs 6px"),
    # And the same for type. P8 fixed the 16.5px body metric and named
    # nothing else, so the site grew 92 distinct font sizes, 42 of them off
    # a whole or half pixel. This writes the missing scale - thirteen steps,
    # chosen by measuring three candidates against the real distribution -
    # and conforms to it. clamp() and vw sizes are left fluid.
    ("_dev/type_scale.py",
     "92 font sizes onto a scale of thirteen"),
    # The families palette_conform deliberately stopped at. Eighteen reds,
    # seven ambers and fourteen greens collapse to one each, split by
    # whether the declaration paints letters - #B5483F clears the floor on
    # paper by 0.46, so text takes the darker #9C3F37 and only fills take
    # the accent.
    ("_dev/semantic_palette.py",
     "one red, one amber, one green instead of thirty-eight near-misses"),
    # Two display faces doing one job. Fraunces wins on count (190 pages to
    # 48) and on identity; the retired family also comes out of the Google
    # Fonts URL on all 242 pages, which is a webfont request saved on every
    # one. Reversing it is one line in the pass.
    ("_dev/one_display_face.py",
     "one display face, and 242 pages stop downloading the other"),
    ("_dev/discovery.py",
     "sitemap.xml and structured data, derived from the pages that exist NOW. "
     "Nothing may add or rename a page after this"),
    ("_dev/passes_index.py",
     "regenerates _dev/PASSES.md - what each pass injects and the marker to "
     "grep a built page for. Writes documentation, never the site"),
    # The internal control panel at /_ops/. AFTER discovery, because one of
    # its guards is that /_ops/ has not got into the sitemap discovery just
    # wrote. Reads mock/library/registry.json for page counts and titles, so
    # the board cannot drift from the site it describes.
    ("_dev/ops_board.py",
     "the status board at /_ops/, rebuilt from the registry and "
     "_dev/ops_state.py. noindex, robots-disallowed, not in the sitemap"),
    # Rollout steps 2-3 (August 2026): every published page carries
    # body.house + css/house-skin.css, loaded last. A page a builder just
    # rewrote loses both, so this runs at the very end of every build to
    # re-convert it. Idempotent, guarded, excludes tycoon.html and
    # rates.html by decision.
    ("_dev/house_swap.py --all",
     "the house skin - body.house and the last-loaded skin sheet on every "
     "published page, re-applied after everything above has run"),
    ("_dev/family_art.py",
     "rollout step 5, family 1 - the artband editorial pages carry the "
     "three named house sheets and no legacy CSS; re-applied last so a "
     "rebuilt page is re-converted and the ?v= hashes stay current"),
    ("_dev/family_pk.py",
     "rollout step 5, family 2 - the pagekit research/directory pages "
     "(article.pk-wrap) carry house/house-chrome/house-pk and no legacy "
     "CSS; runs after house_swap (it un-skins these pages) and after "
     "family_art (whose sweep skips body.bcp by name)"),
    # Family 4: the tools keep their app CSS and shed only the chrome
    # that house-chrome replicates - see the pass docstring. Runs last of
    # the families so house_swap's re-skin is always undone.
    ("_dev/family_tool.py",
     "rollout step 5, family 4 - the interactive tools carry the three "
     "named house sheets plus their own app CSS, and no replicated "
     "chrome; the family sheet is the skin's tool rules, ported"),
    # Family 5: everything the skin still covered - the whole remainder
    # converts by the same subtraction, with the skin itself ported as
    # the family sheet. After this pass NOTHING links house-skin.css.
    ("_dev/family_rest.py",
     "rollout step 5, family 5 - every remaining skinned page carries "
     "house/house-chrome/house-rest and its own page CSS; the skin is "
     "fully ported and retired"),
    # The /for/ stage doors (P2 door 3, option 3C The Ledger, per the
    # A2/A3 decisions of 15 Aug 2026). Runs at the very end so a rebuilt
    # door is re-converted after house_swap's re-skin and after the other
    # families' sweeps.
    ("_dev/family_for.py",
     "the /for/ stage doors - article.fd-wrap pages carry house/"
     "house-chrome/house-for and no legacy CSS; /for/associates is the "
     "first member and the template the other doors copy"),
    # Dead last, because the five family passes above are what un-links a
    # sheet: they port the skin's rules into house-<family>.css and remove
    # the <link>. Anything in css/ that nothing links after they have run is
    # residue, and residue in css/ is how css/house-skin.css survived a
    # rollout that had already replaced it. The skin itself is exempt and
    # the pass says why - house_swap.py hashes it on every run.
    # The other half of the same bug. Four family passes strip every
    # content-addressed <link>, and seven FLOORS passes have their override
    # blocks hoisted into exactly those sheets - so `.bcr` spacing was
    # unreachable on 89 of the 134 pages that carry a breadcrumb, and
    # `.artwrap` on 23 of 24. Re-links each sheet, but only on pages that
    # carry a class it styles. Before surface_fix and mobile_last, so those
    # two keep the last word.
    ("_dev/override_relink.py",
     "the override sheets the family passes strip, put back"),
    # MOVED here from FLOORS, and the move is the fix. surface_fix writes an
    # inline <style> block; extract_css hoists it; and then family_art,
    # family_pk, family_sc and family_for rewrite their pages' stylesheet
    # list to a fixed set that does not include the hoisted sheet. Measured
    # in a browser: the masthead CTA label was still #1B2420 on #2C6350 -
    # 2.28:1 - on 142 pages after the fix had been written and its own
    # guard had passed. Only body.bcz and the tool family, which port the
    # skin rather than replace it, were keeping the rules.
    #
    # Running after the families means the block is injected into the page
    # AFTER the list has been rewritten, so there is no sheet to drop.
    ("_dev/surface_fix.py", "text on the wrong surface"),
    ("_dev/dead_css.py",
     "stylesheets no page links, retired to _to_delete/"),
    # The fine-grained version of the same question: which RULES inside a
    # sheet a page does load can never match anything. 173 of them, whole
    # retired components - an old landing page, a retired directory, the
    # pre-house nav. After the family passes, because those generate the
    # family sheets. Everything removed is kept in _to_delete/pruned-*.css.
    ("_dev/dead_rules.py",
     "CSS rules whose classes appear nowhere on the site"),
    # Dead last, and that position is the whole point. mobile_floor.py's
    # hit-area rules were hoisted by extract_css into a stylesheet that the
    # five family passes then stopped 240 of 242 pages loading, so the
    # newsletter consent checkbox shipped at 22x22 and every form control
    # at the browser's default 13.3px - under the 16px at which iOS Safari
    # zooms on focus and does not zoom back. Re-asserted inline, after
    # everything that could drop it.
    ("_dev/mobile_last.py",
     "24px hit areas and a 16.5px control size, after the family passes"),
    # mobile_last re-asserted the form-control half of mobile_floor.py and
    # said so. The other two halves - the 12px sentence floor and the hit
    # area on everything that is not a form control - went the same way and
    # nobody re-asserted them: mobile_floor reaches 2 pages of 242, and the
    # sweep measured 1,281 targets under 24px and 8,786 nodes of sub-12px
    # sentence text. This puts both back, inline, at every width.
    ("_dev/mobile_reassert.py",
     "mobile_floor's 12px floor and 24px hit areas, where nothing can drop "
     "them and at every width, not only under 640px"),
    # P8's slab, from the claims file. Here rather than in STRUCTURE for two
    # reasons. Its anchor check asserts that the figure a claim rests on is
    # present in the page AS IT SHIPS, so it has to run after everything that
    # rewrites page text. And its CSS ships inline, after the hoisting chain,
    # deliberately: the recurring failure in this tree is a pass's rules being
    # hoisted into a shared sheet and then unlinked again by a family pass -
    # which is exactly what happened to mobile_floor.py and cost 3,085 tap
    # targets. A slab whose fill gets unlinked is a white block with white
    # text on it, and nothing static would report it.
    #
    # After mobile_reassert, not before: the slab's eyebrow is a 10.5px label,
    # the same size as the hand-written one on the home page, and running the
    # 12px sentence floor over it would make the rollout disagree with the
    # slab it is rolling out.
    ("_dev/slab_rollout.py",
     "the one claim each page makes, from _dev/slab_claims.json, with every "
     "claim's anchor checked against the page as it ships"),
    # The contrast in the calculators' OUTPUT, which no guard here had ever
    # measured because it does not exist until an input changes. Reported from
    # a phone, not by a tool: eighteen failures at 390px, the worst at 1.29:1.
    # After the palette passes and after mobile_reassert, because it has to
    # outrank both, and inline for the same reason they are.
    ("_dev/tool_surface.py",
     "the seven colour pairs the tools emit onto the wrong surface"),
    # The mark the site owner chose for the header, which has been in every
    # page's markup all along and hidden by `body.house .sitenav-fig
    # {display:none}` since the August masthead rebuild.
    ("_dev/masthead_mark.py",
     "the masthead figure, un-hidden - it was never removed, only turned off"),
    # Four of seven topics were off-screen on a phone, in a scroller with no
    # scrollbar, no visible fade and a cut that lands mid-word.
    ("_dev/nav_wrap.py",
     "the topic row wraps below 900px, so all seven sections are visible"),
    # Last, because it has to outrank the palette passes and surface_fix on a
    # page that has no body class for surface_fix to scope to.
    ("_dev/mockup_floor.py",
     "the two mockups are noindex, not unpublished: the last 26 contrast "
     "pairs and the last overflowing table on the site"),
]

# VERIFY. Read-only. Never writes, so it is safe to run at any time.
VERIFY = [
    # Cheapest and first: forty passes each carry their own copy of SUBDIRS,
    # and a directory missing from that list is invisible to every one of
    # them while every guard still reports clean.
    ("_dev/subdirs_check.py",
     "every pass agrees which directories the site has, and every directory "
     "of pages is in the list"),
    # The DCA licensee counts. `--check` only: it re-reads the committed
    # `_dev/dca_stats.py` and reconciles it. The refresh half of that
    # pass downloads 35MB from the state and CANNOT run here - this
    # machine has no outbound network - so it is run monthly from
    # somewhere that does, and only the derived counts are committed.
    ("_dev/dca_licensees.py --check",
     "the 165,000 California licensee counts still reconcile, and "
     "nothing identifying has crept into the derived file"),
    ("_dev/notruncate.py",
     "a smoke alarm: no published page is empty or implausibly small. Two\n      pages have been committed at zero bytes by an interrupted pass, and\n      neither linkcheck nor seo_rules noticed, because both skip a file with\n      no links and no chrome"),
    ("_dev/linkcheck.py", "every internal link resolves"),
    # The guard that would have caught the school pages shipping two
    # whole components with no CSS. Static - no browser - so it runs
    # anywhere the pipeline runs. Baseline in _dev/coverage_baseline.json;
    # a burst of new signatures means a component lost its stylesheet.
    ("_dev/family_coverage.py",
     "elements whose classes have no rule in any sheet the page loads"),
    ("_dev/orphan_guard.py",
     "the reverse of linkcheck: every indexable page must have at least "
     "one inbound link - a page in the sitemap that no other page links "
     "to fails the build"),
    ("_dev/seo_rules.py", "the SEO rules, against the recorded baseline"),
    # The two censuses, and they are the same lesson: a check that looks for
    # the drift it has already been shown finds only that drift. These count
    # EVERYTHING - every hex on every published page and in every sheet
    # those pages link, every typeface, every font size, every radius, every
    # gradient - and fail on anything NEW against a recorded baseline. That
    # is what stops the palette going from 21 sanctioned colours in 2,422
    # uses back to 346 colours in 2,586.
    ("_dev/palette_census.py --check",
     "no colour outside the sanctioned palette that is not already in "
     "_dev/palette_baseline.json"),
    ("_dev/type_census.py --check",
     "no new typeface, font size, border radius or gradient against "
     "_dev/type_baseline.json - and no page setting a face it never loads"),
    # The guard for the bug class that no per-pass guard can see: a pass
    # writes its rules, its own guard passes on the file it just wrote, and
    # a later pass removes the result. That has happened three times here -
    # the retired skin on tools.html, build_redirect's assertion, and
    # surface_fix's overrides being hoisted into a sheet four families then
    # stopped loading, which left the masthead CTA at 2.28:1 on 142 pages.
    # Counts how many pages each pass's marker still reaches and fails on a
    # DROP against the recorded number.
    ("_dev/pass_reach.py --check",
     "no pass has quietly lost the pages it used to reach"),
    # The guard P8 claims to have and never had. It could not have been
    # written before now: `.slab` names both the HEY panel and a
    # colour-modified section band, so counting the class reported five
    # pages in flagrant violation when none of them carry a P8 slab at all.
    # Reads the modifier instead, and also proves the slab still has the
    # mask that gives it its scalloped edge - the thing flat_bands.py has
    # to keep distinguishing from decoration.
    # Non-mutating half of the rollout: every claim's anchor is still on its
    # page, and every record still fits the budgets. A builder's figure moving
    # is the way a slab goes stale, and this is the thing that notices.
    ("_dev/slab_rollout.py --check",
     "every shipped claim still rests on a figure its page actually carries"),
    ("_dev/tool_surface.py --check",
     "the calculator pages still carry the tool-output colour rules"),
    ("_dev/nav_wrap.py --check",
     "every page with a topic row still carries the wrapping rule"),
    ("_dev/masthead_mark.py --check",
     "the masthead mark is still un-hidden on every page that carries one"),
    ("_dev/slab_guard.py",
     "one slab per page at most, and the scallop is still on it"),
]

STAGES = [("build", BUILD), ("structure", STRUCTURE), ("floors", FLOORS),
          ("seo", SEO), ("css", CSSCHAIN), ("last", LAST), ("verify", VERIFY)]


def run(path, why, timeout=600):
    name = os.path.basename(path)
    t0 = time.time()
    sys.stdout.write("  %-24s " % name)
    sys.stdout.flush()
    try:
        # A pass may carry arguments - "_dev/x.py --check". Split them off
        # the path so the entry stays one readable string in the lists above.
        parts = path.split()
        argv = [sys.executable, os.path.join(SITE, parts[0])] + parts[1:]
        r = subprocess.run(argv,
                           cwd=SITE, capture_output=True, text=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        print("TIMED OUT after %ds" % timeout)
        return False, ""
    out = (r.stdout or "") + (r.stderr or "")
    dt = time.time() - t0
    if r.returncode != 0:
        print("FAILED (%.1fs)" % dt)
        print("\n" + "-" * 72)
        print(out.strip()[-2600:])
        print("-" * 72)
        print("\n  %s: %s" % (name, why))
        return False, out
    tail = [l for l in out.strip().splitlines() if l.strip()]
    print("ok  %-46s %4.1fs" % ((tail[-1][:46] if tail else ""), dt))
    return True, out


def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    start = None
    if "--from" in args:
        start = args[args.index("--from") + 1]
    # `--to <name>` stops AFTER that pass. The pair exists because this repo
    # is edited over a device bridge whose shell kills anything still running
    # when the call returns, and a full run is right at that limit. Half a
    # pipeline committed is worse than two halves run in sequence - it is how
    # a page ended up committed at zero bytes once.
    stop = None
    if "--to" in args:
        stop = args[args.index("--to") + 1]

    stages = [("verify", VERIFY)] if check_only else STAGES
    seen_start = start is None
    stopped = False
    ran = failed = 0

    for label, group in stages:
        print("\n%s" % label.upper())
        for path, why in group:
            name = os.path.basename(path).replace(".py", "")
            if stop is not None and stopped:
                print("  %-24s skipped (--to %s)" % (name, stop))
                continue
            if not seen_start:
                if name == start:
                    seen_start = True
                else:
                    print("  %-24s skipped (--from %s)" % (name, start))
                    continue
            # path may carry arguments; only the first token is a file.
            if not os.path.exists(os.path.join(SITE, path.split()[0])):
                print("  %-24s MISSING - %s" % (name, why))
                failed += 1
                continue
            ok, _ = run(path, why)
            ran += 1
            if stop is not None and name == stop:
                stopped = True
            if not ok:
                failed += 1
                print("\nStopped. Every pass after this one would build on a "
                      "half-finished site.")
                sys.exit(1)

    print("\n%d pass(es) run, %d failed." % (ran, failed))
    if not check_only:
        print("The sitemap was regenerated from the pages that exist now.")
        print("Deploy with:  ./_dev/publish.sh \"<what changed>\"")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
