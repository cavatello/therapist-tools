#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every builder that owns a published page is still wired into ship.py.

WHY THIS EXISTS, AND IT IS RECENT

On 18 August 2026 two sessions worked this repository at once. One of them
added its own passes to a copy of `ship.py` that predated the other's work
and wrote the whole file back. **Five builders and a verify pass silently
left the pipeline.**

Nothing looked wrong. All five pages still existed, still served 200, still
carried their chrome, still appeared in the sitemap and the hubs. They had
simply stopped being REBUILT - which means their content was frozen at
whatever the last run produced, and any correction made in a builder would
never reach the page again.

The worst of it: `build_bills.py` carries a **freshness lock** that stops
the entire pipeline from 1 September unless the bill tracker has been
updated. Unwired, that lock can never fire. The page would have gone on
saying two bills are "pending" long after they were decided, the two
scheduled tasks that exist to clear it would have found nothing blocking,
and every guard on the site would have reported clean.

**An unwired builder is worse than a missing one.** A missing page is
obvious the moment somebody looks. A stale one is invisible forever.

THE INVARIANT

    a builder that declares a PAGE, whose PAGE exists on the site,
    must be wired into ship.py

That is it. It is checkable in a second, it has no baseline - and having
no baseline is the point. `pass_reach.py` guards an adjacent bug class and
could not have caught this one, because it compares against a recorded
baseline, and a baseline records what IS rather than what OUGHT (handoff
rule 2). A file rewritten by another session takes the baseline with it.
This pass derives the expectation from the builders themselves every run,
so there is nothing to drift.

THE THREE FINDINGS IT REPORTS

  unwired      a builder owns a published page and is not in ship.py.
               The failure above.
  missing      ship.py wires a `_dev/build_*.py` that is not on disk.
               A rename or a deletion that did not finish.
  orphan page  a builder is wired and its PAGE is absent from the site.
               Either the build never ran or the page was removed by hand.

A builder with no `PAGE = "..."` at module level is ignored on purpose:
that is how a retired stub looks (`build_billtracker.py`), and how a
multi-page builder looks (`build_cases.py` writes thirty). Neither is a
defect, and a guard that fired on them would be switched off.

    python3 _dev/builder_wired.py
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SHIP = os.path.join(HERE, "ship.py")

# Deliberately not named MARK / END / JSMARK / BLOCK / BODYCLASS.
# `_dev/passes_index.py` reads those five names out of every pass by AST
# and treats the value as the marker THAT pass injects, then fails the
# build if two passes claim the same one. This pass injects nothing into
# any page; it only reads. Using one of those names cost a build once
# already, in a file that was likewise only describing something.
PAGE_DECL = re.compile(r'^PAGE\s*=\s*"([^"]+\.html)"', re.M)


def declared():
    """(builder path relative to the repo, the page it owns)."""
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "build_*.py"))):
        src = open(path, encoding="utf-8").read()
        m = PAGE_DECL.search(src)
        if m:
            out.append(("_dev/" + os.path.basename(path), m.group(1)))
    return out


def main():
    ship = open(SHIP, encoding="utf-8").read()
    wired = set(re.findall(r'\("(_dev/build_[a-z0-9_]+\.py)', ship))

    findings, checked = [], 0

    for rel, page in declared():
        published = os.path.exists(os.path.join(SITE, page))
        is_wired = rel in wired
        checked += 1
        if published and not is_wired:
            findings.append(
                "%s owns %s, which is published, and is NOT wired into "
                "ship.py - that page has stopped being rebuilt" % (rel, page))
        elif is_wired and not published:
            findings.append(
                "%s is wired and owns %s, which is not on the site - the "
                "build never ran, or the page was removed by hand"
                % (rel, page))

    for rel in sorted(wired):
        if not os.path.exists(os.path.join(SITE, rel)):
            findings.append(
                "ship.py wires %s, which is not on disk" % rel)

    if findings:
        for f in findings:
            print("  GUARD: " + f)
        sys.exit("%d builder(s) out of step with ship.py" % len(findings))

    print("guards clean - %d builder(s) own a page, every one of them "
          "published and wired" % checked)


if __name__ == "__main__":
    main()
