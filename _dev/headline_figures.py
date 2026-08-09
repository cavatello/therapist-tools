#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Change a page's headline figure when its builder no longer exists.

THE REPORT

  "THIS IS A STUPID FEE, WHO CARES WHAT MEBMERSHIP COSTS"

about the number in the Alma page's hero, which read:

  $1.24
  what the membership costs you per session

The arithmetic is right - Alma's $1,140 a year over 920 sessions is $1.24 a
session, and the page derives it carefully. It is still the wrong number to
lead with. Nobody arrives at that page wanting to know the per-session cost of
a membership; they arrive wanting to know whether to join a network at all.

The page already contains the number that answers that:

  $115.77
  what a network has to beat, at 20 sessions a week

That is a decision. $1.24 is a footnote that was promoted.

WHY A PASS

`mock/articles/build_articles.py` cannot run - its `_chrome.html` input is
gone, the same way `mock/psychedelics/build_psy.py` lost its `data/` directory.
Every article page on this site is now frozen HTML that only a pass can touch.
That is a structural fact about this project, not a one-off, so this file is
written as the place where "the headline figure on an article is wrong" gets
fixed, rather than as a single edit.

WHAT IT CHANGES, PER PAGE

  the hero figure   the big number and its caption
  ts:number         the meta tag, which is what `_dev/pixel_concepts.py` reads
                    to fill the "In short" card, so leaving it stale would put
                    the old number back on the page in a different box

Idempotent - it recognises its own output and both source and target values, so
it can run before or after itself. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "<!-- _dev/headline_figures.py -->"

# page, (old figure, old caption), (new figure, new caption), new ts:number, why
FIXES = [
    (
        "alma-for-california-therapists.html",
        ("$1.24", "what the membership costs you per session"),
        ("$115.77", "what a network has to beat, at 20 sessions a week"),
        "$115.77 a session",
        "The cost of a membership per session is a footnote. What a network "
        "has to beat is the decision the reader came for.",
    ),
]


def esc_variants(text):
    """The same string as it may appear after the entity passes have run."""
    return {text,
            text.replace("'", "&rsquo;").replace("&", "&amp;"),
            text.replace("-", "&ndash;")}


def main():
    print("headline figures, on pages whose builder can no longer run:")
    changed = 0
    bad = 0

    for page, (oldfig, oldcap), (newfig, newcap), tsnum, why in FIXES:
        p = os.path.join(SITE, page)
        if not os.path.exists(p):
            print("  MISSING  %s" % page)
            bad += 1
            continue
        s = open(p, encoding="utf-8").read()
        orig = s

        # ------------------------------------------------------- the figure
        # Matched as the <b>/<span> pair inside .artfig so a bare "$1.24"
        # elsewhere in the prose - where the page derives it, correctly - is
        # left completely alone. That derivation is good writing; only the
        # promotion of it to a headline was wrong.
        pat = re.compile(
            r'(<div class="artfig">\s*<b>)\s*' + re.escape(oldfig) +
            r'\s*(</b>\s*<span>)\s*' + re.escape(oldcap) + r'\s*(</span>)',
            re.I)
        if pat.search(s):
            s = pat.sub(r"\1" + newfig + r"\2" + newcap + r"\3", s)
            print("  ok       %-44s %s -> %s" % (page[:44], oldfig, newfig))
        elif newfig in s and newcap in s:
            print("  already  %-44s %s" % (page[:44], newfig))
        else:
            print("  MISSING  %-44s could not find the hero figure block"
                  % page[:44])
            bad += 1

        # ---------------------------------------------------- the meta tag
        # pixel_concepts reads ts:number to build the "In short" card. Leaving
        # it stale would put the old figure back on the page in another box -
        # the change and the check looking at different things, again.
        m = re.search(r'(<meta name="ts:number" content=")([^"]*)(")', s)
        if m:
            if m.group(2) != tsnum:
                s = s[:m.start()] + m.group(1) + tsnum + m.group(3) + s[m.end():]
                print("           ts:number %r -> %r" % (m.group(2), tsnum))
        else:
            print("  MISSING  %s has no ts:number" % page)
            bad += 1

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1

    # ------------------------------------------------------------- guards
    for page, (oldfig, oldcap), (newfig, newcap), tsnum, _why in FIXES:
        p = os.path.join(SITE, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if oldcap in s:
            print("GUARD %s: the old caption %r is still on the page"
                  % (page, oldcap))
            bad += 1
        if newfig not in s:
            print("GUARD %s: the new figure never landed" % page)
            bad += 1
        m = re.search(r'<meta name="ts:number" content="([^"]*)"', s)
        if m and m.group(1) != tsnum:
            print("GUARD %s: ts:number is %r, expected %r"
                  % (page, m.group(1), tsnum))
            bad += 1
        # The derivation in the body must survive. Removing it would make the
        # new headline unsourced, which is worse than the wrong headline was.
        if oldfig not in s:
            print("GUARD %s: %s no longer appears anywhere. It should still be "
                  "derived in the body - only the HEADLINE was wrong."
                  % (page, oldfig))
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("\n%d page(s) changed. guards clean - the old figure is still "
          "derived in the body, just no longer the headline" % changed)


if __name__ == "__main__":
    main()
