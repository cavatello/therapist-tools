#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate `_dev/PASSES.md` - what each pass injects, and how to find it.

WHY THIS EXISTS

Because a duplicate shipped. A second Formspree submit handler was written and
deployed on 9 August 2026, because the first one lives in
`mock/amft/_chrome_js.txt` rather than in `_dev/`, and nothing in this
directory answers the question "does this behaviour already exist?". Two
handlers then raced to replace the same `<form>` node and fired two POSTs for
one click.

`_dev/` is forty-odd passes with names like `fill.py`, `measure.py` and
`stage_router.py`. The names describe intent, not output. What a maintainer
actually needs to know before writing a new pass is:

  - which marker string that pass leaves in the page, so it can be grepped for
  - what it injects, in one line
  - whether it is in the pipeline or has been superseded

So the index is generated from the passes themselves rather than written by
hand, because a hand-written one is out of date the first time somebody is in
a hurry - which is exactly the condition under which it gets consulted.

HOW IT READS THE PASSES

  the marker    a module-level `MARK`, `JSMARK` or `BLOCK` string literal,
                which is this project's convention for "the thing I injected"
  the summary   the first line of the module docstring
  the stage     read from `_dev/ship.py`, so a pass that is written but not
                wired shows as `not in the pipeline` rather than silently
                looking active

Nothing is imported. Every pass would run its `main()` on import if it were,
and a documentation generator must not be able to change the site. The values
are read with `ast`, which evaluates literals and nothing else.
"""
import ast, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = os.path.join(HERE, "PASSES.md")
MARKER_NAMES = ("MARK", "JSMARK", "BLOCK", "END", "BODYCLASS")

# Behaviour that does NOT come from `_dev/`. This is the list the duplicate
# handler would have been caught by, so it goes at the top of the generated
# file rather than in a footnote.
ELSEWHERE = [
    ("mock/amft/_chrome_js.txt", "`Post the signup in the background`",
     "the Formspree submit handler - posts by fetch and answers in the page. "
     "`_dev/form_inline.py` lifts it onto every other page rather than "
     "writing a second one."),
    ("mock/amft/_chrome_css.txt", "`.nlok`, `.nlerr`",
     "the confirmation and error styling that handler renders into."),
    ("mock/psychedelics/build_psy.py", "&mdash;",
     "the psychedelic training pages. **Builder cannot run** - its `data/` "
     "directory is gone."),
    ("mock/articles/build_articles.py", "&mdash;",
     "every article page. **Builder cannot run** - its `_chrome.html` is "
     "gone, which is why `headline_figures.py`, `payer_links.py` and "
     "`ehr_market.py` exist as passes."),
]


# ------------------------------------------------------------------ verdicts
# Every unwired pass was run twice against a throwaway copy of the site on
# 9 August 2026 - `git archive HEAD | tar -x -C /tmp/sitecopy` - and judged on
# two things: does it exit 0, and does a second run change anything a first run
# did not. Re-run the same way before trusting any of this; it is a snapshot of
# a moving site, not a property of the file.
#
# It is written down because the alternative is finding out the way we did:
# `eap_rates.py` was re-run against the LIVE tree to test it, relocated a block
# on rates.html, orphaned a <div>, reintroduced a British spelling, reported
# "guards clean", and was committed by the watcher inside a minute.
#
#   safe      exits 0, idempotent, output already live. Re-runnable.
#   unstable  exits 0 but a second run keeps changing the page.
#   broken    exits non-zero on today's site.
#   one-shot  a migration that has already happened. Do not re-run.
#   module    imported by another pass; not a pass at all.
#   tool      run by hand, deliberately outside the pipeline.
#   retired   superseded, and says so in its own docstring.
VERDICTS = {
    "widen": ("safe", "the two large-display width steps that one_grid.py and "
                      "rates_grid.py both mirror"),
    "measure": ("safe", "the reading-measure cap, 159 pages"),
    "registry_meta": ("safe", ""),
    "link_cards": ("safe", ""),
    "mobile_hero": ("safe", ""),
    "hero_notes": ("safe", ""),
    "tax_assumptions": ("safe", "no-op on today's site"),
    "layout_fixes": ("safe", ""),
    "tool_chain": ("safe", ""),
    "cta_scale": ("safe", ""),

    "side_nav": ("unstable", "a second run changes the page again"),
    "dir_two_views": ("unstable", "a second run changes the page again"),
    "eap_rates": ("refuses", "**re-running this damaged the live site once.** "
                             "It strips its own block and re-inserts it "
                             "against anchors that have since moved. It now "
                             "refuses to run when its block is present; "
                             "regenerating means removing the block by hand "
                             "first, so the destructive step is a decision"),

    "cluster_links": ("broken", "TypeError: insert_at returns an int, and the "
                                "caller unpacks two values"),
    "doc_rails": ("broken", "asserts the article's five h2s on rates.html and "
                            "finds two"),
    "legal_rails": ("broken", "exits non-zero"),
    "quest_hud": ("broken", "exits non-zero"),
    "insurance_wire": ("broken", "exits non-zero, writes nothing"),

    "case_data": ("module", "imported by build_cases.py"),
    "case_depth": ("module", "imported by build_cases.py"),
    "psyd_data": ("module", "imported by build_psyd.py"),
    "insurance_data": ("module", "imported by build_insurance.py"),

    "serve": ("tool", "local dev server"),
    "seo_monitor": ("tool", "crawls the LIVE site; needs the network"),
    "linkcheck_external": ("tool", "checks outbound links; needs the network"),
    "indexnow": ("tool", "pings search engines; run after a deploy"),
    "passes_index": ("tool", "this file"),
    "ship": ("tool", "the pipeline itself"),

    "hub_about_link": ("retired", ""),
    "hub_cluster02_links": ("retired", ""),
    "hub_guide_link": ("retired", ""),
    "hub_headway_link": ("retired", ""),
    "hub_programs_link": ("retired", ""),
    "hub_psychedelic_link": ("retired", "superseded by registry.json"),
    "fill": ("retired", "superseded by measure + content_frame + "
                        "wide_measure; no output left on the site"),
    "hero_action": ("retired", "superseded by hub_hero; no output left"),

    # second triage batch, same method, same day
    "empty_outputs": ("unstable", "a second run changes six pages again"),
    "fixups": ("unstable", "a second run changes the page again"),
    "hub_owid": ("unstable", "a second run changes five hubs again"),

    "affiliate": ("broken", "exits non-zero after writing four pages, which "
                            "is the worst combination: it half-applies"),
    "ciis_tuition": ("broken", "exits non-zero, writes nothing"),
    "feepatch": ("broken", "exits non-zero, writes nothing"),
    "nav_consolidate": ("broken", "exits non-zero, writes nothing"),
    "typeface": ("broken", "exits non-zero, writes nothing"),

    "analytics": ("safe", "the GA4 tag on all 164 pages; idempotent. Not "
                          "wired because analytics_events.py already asserts "
                          "the tag is present"),
    "nav_rebuild": ("safe", "158 pages; idempotent. The nav that restyle.py "
                            "now maintains - keep for reference, not for the "
                            "pipeline"),
    "build_psyd": ("safe", "rebuilds the PsyD directory from psyd_data.py"),
    "registry_sync": ("safe", "rebuilds registry.json from the pages"),
    "build_redirect": ("safe", "the tools.html -> resources.html stub"),
    "hero_palette": ("safe", ""),
    "ads_state": ("safe", "no-op on today's site"),
    "claims": ("safe", "no-op on today's site"),
    "copy_trim": ("safe", "no-op on today's site"),
    "figure_scope": ("safe", "no-op on today's site"),
    "gold_slab": ("safe", "no-op on today's site"),
    "landing": ("safe", "no-op on today's site"),
    "pacifica_tuition": ("safe", "no-op on today's site"),
    "rates_contrast": ("safe", "no-op on today's site"),
    "rates_fix": ("safe", "no-op on today's site"),
    "rates_tokens": ("safe", "no-op on today's site"),
    "urlfix": ("safe", "no-op on today's site"),
}

# Anything beginning with one of these is a migration that has already run.
ONESHOT_PREFIXES = ("add_", "fix_", "rebase_", "relink_", "rename_")


def verdict(name):
    if name in VERDICTS:
        return VERDICTS[name]
    if name.startswith(ONESHOT_PREFIXES):
        return ("one-shot", "a migration that has already happened")
    return ("untriaged", "")


def literals(path):
    """Module-level string constants, read without importing."""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except SyntaxError:
        return {}, None
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in MARKER_NAMES:
                    try:
                        out[t.id] = ast.literal_eval(node.value)
                    except (ValueError, SyntaxError):
                        pass
    return out, ast.get_docstring(tree)


def stages():
    """name -> stage, read from ship.py without importing it."""
    p = os.path.join(HERE, "ship.py")
    if not os.path.exists(p):
        return {}
    s = open(p, encoding="utf-8").read()
    out = {}
    for stage in ("BUILD", "STRUCTURE", "FLOORS", "SEO", "CSSCHAIN", "LAST",
                  "VERIFY"):
        m = re.search(r"^%s = \[([\s\S]*?)^\]" % stage, s, re.M)
        if not m:
            continue
        for name in re.findall(r'"_dev/([a-z0-9_]+)\.py"', m.group(1)):
            out[name] = stage.replace("CSSCHAIN", "CSS").lower()
    return out


def main():
    st = stages()
    rows = []
    for f in sorted(os.listdir(HERE)):
        if not f.endswith(".py") or f.startswith("_"):
            continue
        name = f[:-3]
        lits, doc = literals(os.path.join(HERE, f))
        summary = (doc or "").strip().split("\n")[0] if doc else ""
        marks = []
        for k in ("MARK", "JSMARK", "BLOCK"):
            v = lits.get(k)
            if isinstance(v, str) and len(v) > 3:
                marks.append(v.strip())
        if isinstance(lits.get("BODYCLASS"), str):
            marks.append("body class %s" % lits["BODYCLASS"])
        rows.append((name, st.get(name), marks, summary))

    wired = [r for r in rows if r[1]]
    loose = [r for r in rows if not r[1]]

    o = ["# What every pass injects",
         "",
         "**Generated by `_dev/passes_index.py`. Do not edit by hand** - run "
         "the pass instead, or the next run will overwrite you.",
         "",
         "Read this before writing a new pass. It exists because a duplicate "
         "Formspree handler shipped on 9 August 2026: the original lives in "
         "`mock/`, not in `_dev/`, and nothing here answered *does this "
         "already exist?* Two handlers then raced on the same `<form>` node "
         "and fired two POSTs for one click.",
         "",
         "The **marker** column is the string to grep a built page for. If "
         "the behaviour you are about to add already has a marker, extend "
         "that pass rather than writing a second one.",
         "",
         "## Behaviour that does not come from `_dev/`",
         "",
         "The list that would have caught it.",
         "",
         "| Where | Marker | What |",
         "|---|---|---|"]
    for where, marker, what in ELSEWHERE:
        o.append("| `%s` | %s | %s |" % (where, marker, what))

    o += ["",
          "## In the pipeline",
          "",
          "In `_dev/ship.py` order of stages, alphabetical within a stage.",
          "",
          "| Pass | Stage | Marker in the page | What it does |",
          "|---|---|---|---|"]
    order = {"build": 0, "structure": 1, "floors": 2, "seo": 3, "css": 4,
             "last": 5, "verify": 6}
    for name, stage, marks, summary in sorted(
            wired, key=lambda r: (order.get(r[1], 9), r[0])):
        o.append("| `%s.py` | %s | %s | %s |"
                 % (name, stage,
                    " · ".join("`%s`" % m for m in marks) or "&mdash;",
                    summary.replace("|", "\\|")))

    o += ["",
          "## Written, not wired",
          "",
          "In `_dev/` but not in `ship.py`. **Verdicts come from running each "
          "one twice against a throwaway copy of the site** "
          "(`git archive HEAD | tar -x -C /tmp/sitecopy`), never against the "
          "working tree - the watcher commits within a minute, and one such "
          "test shipped a damaged `rates.html`.",
          "",
          "| Verdict | Meaning |",
          "|---|---|",
          "| `safe` | exits 0, idempotent, output already live |",
          "| `unstable` | exits 0, but a second run keeps changing the page |",
          "| `broken` | exits non-zero on today's site |",
          "| `one-shot` | a migration that has already happened |",
          "| `module` | imported by another pass; not a pass |",
          "| `tool` | run by hand, deliberately outside the pipeline |",
          "| `retired` | superseded, and says so in its own docstring |",
          "| `refuses` | not idempotent, and now stops itself running twice |",
          "",
          "| Pass | Verdict | Marker | What it does |",
          "|---|---|---|---|"]
    rank = {"unstable": 0, "broken": 1, "refuses": 2, "safe": 3,
            "untriaged": 4, "module": 5, "tool": 6, "one-shot": 7,
            "retired": 8}
    for name, _s, marks, summary in sorted(
            loose, key=lambda r: (rank.get(verdict(r[0])[0], 9), r[0])):
        v, note = verdict(name)
        o.append("| `%s.py` | **%s** | %s | %s%s |"
                 % (name, v, " · ".join("`%s`" % m for m in marks) or "&mdash;",
                    summary.replace("|", "\\|"),
                    (" — " + note) if note else ""))
    o.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(o))
    print("wrote _dev/PASSES.md")
    print("  %d pass(es) in the pipeline, %d written but not wired"
          % (len(wired), len(loose)))

    # --------------------------------------------------------------- guards
    bad = 0
    nomark = [r[0] for r in wired if not r[2]]
    nodoc = [r[0] for r in rows if not r[3]]
    if nodoc:
        print("GUARD: no module docstring, so nothing to index: %s"
              % ", ".join(nodoc))
        bad += 1
    # A pass with no marker cannot be grepped for, which is the whole point of
    # the index. Reported, not fatal: several passes legitimately rewrite
    # existing markup rather than injecting anything.
    if nomark:
        print("  note: %d wired pass(es) inject no marker and cannot be "
              "grepped for: %s" % (len(nomark), ", ".join(sorted(nomark))))

    # Markers must be unique. Two passes sharing one would make every
    # "is this already here?" check answer for the wrong pass.
    seen = {}
    for name, _s, marks, _d in rows:
        for m in marks:
            seen.setdefault(m, []).append(name)
    for m, who in seen.items():
        if len(who) > 1:
            print("GUARD: %r is the marker for %s. Markers must be unique or "
                  "an idempotency check strips the wrong block."
                  % (m, " and ".join(who)))
            bad += 1

    # A pass with no verdict has never been triaged. Reported, not fatal -
    # a new pass is untriaged by definition on the day it is written.
    un = [r[0] for r in loose if verdict(r[0])[0] == "untriaged"]
    if un:
        print("  note: %d unwired pass(es) have no verdict yet: %s"
              % (len(un), ", ".join(sorted(un))))

    # A verdict for something that is not there any more is worse than none.
    names = {r[0] for r in rows}
    for k in VERDICTS:
        if k not in names:
            print("GUARD: a verdict is recorded for %s, which is not in _dev/"
                  % k)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - every pass documented, every marker unique")


if __name__ == "__main__":
    main()
