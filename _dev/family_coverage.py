#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A class used in the body with no rule in any sheet the page loads.

WHAT THIS WOULD HAVE CAUGHT

All 66 school pages shipped the freshness block and the up-link block as
completely unstyled markup - "Last checked17 August 2026All updates ->",
run together, flush to the window edge. Fourteen classes carrying visible
text, no rule for any of them in any of the three stylesheets that family
loads. It was found by the site's owner, in a screenshot, after it had
been live for some time.

`family_art.py` has an "uncovered classes" guard and that is exactly why
the art family never had this problem. No other family had one. This is
that guard, generalised, for every page.

HOW IT WORKS, AND WHY IT IS STATIC

For each page: collect the classes used in the body, collect the classes
mentioned by any selector in the sheets that page links (plus its own
inline <style> blocks), and diff. No browser - this is a text pass, so it
runs in the pipeline on any machine and costs about a second.

That means it cannot tell whether an uncovered class actually carries
visible text; a DOM would be needed for that. So it does not try to
judge. It uses the baseline pattern `seo_rules.py` already uses: the
known set is recorded, and the build fails only on something NEW. A
genuinely unstyled component shows up as a burst of new names on a lot of
pages, which is unmissable; a semantic hook or a JS target added
deliberately shows up as one name and gets added to the baseline with a
one-line reason.

WHAT IT STILL CANNOT TELL YOU, AND WHY THAT IS FINE

It cannot distinguish "a container whose children are styled" from "a
component with no CSS". All six signatures in the initial baseline are
the former: `<form class="askform">` needs no rule of its own because its
inputs have them, and `.gates` is a plain block wrapper around styled
numbered items. Measured in a browser, each has zero padding and no
background - and looks correct, because it is meant to.

So this is a CHANGE detector, not a correctness proof. That is enough for
the bug it exists to prevent: on the school pages the wrapper AND every
child was unstyled, so it would have fired as a burst of new signatures
across 66 pages at once. A quiet single new name is a container; a burst
is a component that lost its stylesheet.

WHY A BASELINE RATHER THAN ZERO

Plenty of classes are legitimately unstyled: JS hooks, ARIA scaffolding,
`ts:`-prefixed metadata markers, and modifiers whose rules live on a
compound selector this pass reads as a different name. Demanding zero
would mean either a fake zero or a switched-off guard. The baseline keeps
the guard honest and cheap: it answers "did we just start shipping
something unstyled", which is the question that actually matters.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
BASELINE = os.path.join(HERE, "coverage_baseline.json")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")

# Never reported: framework-ish or metadata names that are not styling.
IGNORE_PREFIX = ("js-", "is-", "has-", "aria", "ts-", "u-", "sr")
IGNORE = {
    "sr", "sronly", "visually-hidden", "nojs", "active", "on", "open",
    "hidden", "current", "selected", "print", "noprint",
}


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


_sheet_cache = {}


def sheet_classes(name):
    if name in _sheet_cache:
        return _sheet_cache[name]
    p = os.path.join(CSSDIR, name)
    got = set()
    if os.path.exists(p):
        css = open(p, encoding="utf-8").read()
        css = re.sub(r"/\*[\s\S]*?\*/", "", css)
        # only selector text: everything before each {
        for m in re.finditer(r"([^{}]+)\{", css):
            for c in re.findall(r"\.([A-Za-z0-9_-]+)", m.group(1)):
                got.add(c)
    _sheet_cache[name] = got
    return got


def body_of(html):
    """The body with script and style contents removed.

    Scripts matter: they contain strings like `cls === 'x'` and
    `class="..."` fragments, and scanning them produced class names like
    `.'`, `.||`, `.===` and `.(cls` - noise that would have gone straight
    into the baseline and made it worthless.
    """
    m = re.search(r"<body[^>]*>([\s\S]*)</body>", html, re.I)
    body = m.group(1) if m else html
    body = re.sub(r"<script[\s\S]*?</script>", "", body, flags=re.I)
    body = re.sub(r"<style[\s\S]*?</style>", "", body, flags=re.I)
    return body


def main():
    known = {}
    if os.path.exists(BASELINE):
        known = json.load(open(BASELINE, encoding="utf-8"))

    found = {}
    for rel in pages():
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()

        styled = set()
        # Subdirectory pages (money/, licensure/, for/ ...) link
        # `../css/x.css`, so the prefix must be optional. Without this the
        # pass reported every chrome class on all 9 hub pages as uncovered
        # - a false positive that looked exactly like the real bug.
        for name in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)', html):
            styled |= sheet_classes(name)
        # the page's own inline blocks count as coverage
        for m in re.finditer(r"<style>([\s\S]*?)</style>", html):
            blk = re.sub(r"/\*[\s\S]*?\*/", "", m.group(1))
            for mm in re.finditer(r"([^{}]+)\{", blk):
                for c in re.findall(r"\.([A-Za-z0-9_-]+)", mm.group(1)):
                    styled.add(c)

        # PER ELEMENT, not per class name. An element whose class list is
        # `verd warn exwarn` is styled - `.verd` and `.warn` have rules and
        # `exwarn` is a modifier. Reporting bare class names flagged 15
        # names on up to 61 pages and every one of the big ones was a
        # modifier riding a styled base class: `tsbadge part`, `vox inf`,
        # `pnote ocdef`. Useless noise.
        #
        # The bug this guard exists for looks different: `<div
        # class="tsrow">` where NOTHING in the list has a rule anywhere.
        # So the unit is the element, and the test is "not one of its
        # classes is styled".
        gap = set()
        for m in re.finditer(r'class="([^"]*)"', body_of(html)):
            names = [c for c in m.group(1).split()
                     if c not in IGNORE and not c.startswith(IGNORE_PREFIX)]
            if not names:
                continue
            if any(c in styled for c in names):
                continue
            gap.add(" ".join(sorted(names)))

        if gap:
            found[rel] = sorted(gap)

    # ---- compare against the baseline
    new = {}
    for rel, gap in found.items():
        fresh = [c for c in gap if c not in set(known.get(rel, []))]
        if fresh:
            new[rel] = fresh

    total = sum(len(v) for v in found.values())
    if "--write-baseline" in sys.argv:
        json.dump(found, open(BASELINE, "w", encoding="utf-8"),
                  indent=1, sort_keys=True)
        print("baseline written: %d page(s), %d uncovered class name(s)"
              % (len(found), total))
        return

    if new:
        # Report by class name, because a real regression is one component
        # appearing on many pages, not many components on one page.
        byclass = {}
        for rel, cs in new.items():
            for c in cs:
                byclass.setdefault(c, []).append(rel)
        print("NEW unstyled element(s) - no class on these has a rule in "
              "any sheet the page loads:")
        for c, rels in sorted(byclass.items(), key=lambda x: -len(x[1])):
            print("  .%-18s on %3d page(s), e.g. %s"
                  % (c, len(rels), rels[0]))
        print("\nIf these are deliberate (a JS hook, a semantic marker), "
              "run:\n  python3 _dev/family_coverage.py --write-baseline")
        sys.exit("%d new unstyled element signature(s)" % len(byclass))

    print("%d page(s) checked. %d known unstyled element(s) in the baseline, "
          "0 new." % (len(pages()), total))


if __name__ == "__main__":
    main()
