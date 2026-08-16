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
]

# STRUCTURE. Chrome, navigation, cross-links, the blocks that carry meaning.
# restyle is first because every later pass assumes the masthead exists.
STRUCTURE = [
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
    ("_dev/contrast_pass.py", "label contrast"),
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
    ("_dev/orphan_guard.py",
     "the reverse of linkcheck: every indexable page must have at least "
     "one inbound link - a page in the sitemap that no other page links "
     "to fails the build"),
    ("_dev/seo_rules.py", "the SEO rules, against the recorded baseline"),
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
