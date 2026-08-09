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
    ("_dev/uplinks.py", "the More-on-this block"),
    ("_dev/breadcrumbs.py", "breadcrumb trails where a trail exists"),
    ("_dev/pixel_concepts.py", "the In-short card and the provenance strip"),
    ("_dev/footer_band.py", "the signup band - inserts ABOVE the up-link"),
    ("_dev/footer_fix.py", "footer colour overrides"),
    ("_dev/analytics_events.py", "the event listener"),
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
    ("_dev/stage_router.py", "the situation router on resources.html"),
    ("_dev/footer_order.py",
     "MOVES the band down against the footer. Must follow footer_band and "
     "pixel_concepts, both of which insert in the same place"),
]

# FLOORS. Colour, tap area, spacing. These read the finished markup, so they run
# after everything that emits markup and before the CSS is hoisted.
FLOORS = [
    ("_dev/contrast_pass.py", "label contrast"),
    ("_dev/token_floor.py", "the hex tokens under the floor"),
    ("_dev/chrome_armor.py", "chrome that has to outrank the page body"),
    ("_dev/mobile_floor.py", "overflow, hit area, and the 12px text floor"),
    ("_dev/block_spacing.py", "every injected block owns the space beneath it"),
    ("_dev/content_frame.py",
     "one content frame: breadcrumb rhythm, headline measure, and wide blocks "
     "that used to run past their column with no scroll affordance"),
    ("_dev/wide_measure.py",
     "line length on a 27-inch 5K, where the failures are the opposite of the "
     "mobile ones and nobody looks for them"),
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
]

# VERIFY. Read-only. Never writes, so it is safe to run at any time.
VERIFY = [
    ("_dev/linkcheck.py", "every internal link resolves"),
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
        r = subprocess.run([sys.executable, os.path.join(SITE, path)],
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
            if not os.path.exists(os.path.join(SITE, path)):
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
