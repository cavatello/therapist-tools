#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A pass that writes CSS onto every page, and reaches only some of them.

THE BUG CLASS THIS EXISTS FOR

Three times in this repository a pass has done its work, passed its own
guard on the file it had just written, and had the result removed by a
later pass:

  1. `css/house-skin.css` was re-attached to `tools.html` by
     `house_swap.py` after `build_redirect.py` had written a stub with no
     stylesheets and asserted exactly that.
  2. `build_redirect.py`'s assertion passed for the same reason, on the
     same file, for months.
  3. `surface_fix.py` wrote its overrides, `extract_css.py` hoisted them
     into `css/<hash>.css` - correctly - and then `family_art.py`,
     `family_pk.py`, `family_sc.py` and `family_for.py` rewrote their
     pages' stylesheet list to a fixed set that did not include it. The
     masthead CTA label stayed at **2.28:1 on 142 pages** after the fix
     had shipped and every guard had said clean.

The shape is always the same and no per-pass guard can see it: **a guard
that checks the moment of writing cannot see what happens two stages
later.** The check has to run at the END, against the page as it ships.

WHAT IT MEASURES

Every pass stamps its rules with a `/* _dev/<name>.py */` marker. For each
marker, this counts the published pages whose CASCADE still contains it -
the page's own inline blocks plus every stylesheet the page links - and
compares that count against a recorded baseline.

A drop is the signal. If `surface_fix.py` reached 242 pages yesterday and
100 today, some pass downstream started dropping it, and that is worth
failing a build over even though nothing looks broken and every other
guard is green.

WHAT A LOW COUNT DOES NOT PROVE

A marker is a comment, and a family pass that PORTS a rule into
`house-<family>.css` may carry the rule without the comment. So a low
count is a flag, not a verdict - which is why this records the number
rather than demanding 242. The baseline is the current, measured, shipped
reality; the guard is against CHANGE.

Passes that legitimately touch a handful of pages - a builder that writes
one page, a fix aimed at three - sit in the baseline at their real number
and are just as protected.

    python3 _dev/pass_reach.py                report
    python3 _dev/pass_reach.py --check        fail on a DROP
    python3 _dev/pass_reach.py --write-baseline
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
BASELINE = os.path.join(HERE, "reach_baseline.json")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARKER = re.compile(r"/\*\s*(_dev/[a-z_0-9]+\.py)")
# A drop of fewer than this many pages is noise - a page renamed, a builder
# that ran on one fewer item. Anything larger is a pass losing its grip.
SLACK = 3


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def measure():
    sheets = {f: open(os.path.join(CSSDIR, f), encoding="utf-8").read()
              for f in os.listdir(CSSDIR) if f.endswith(".css")}
    count = {}
    rels = pages()
    for rel in rels:
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()
        blob = html + "\n" + "\n".join(
            sheets[n] for n in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)',
                                          html) if n in sheets)
        for m in set(MARKER.findall(blob)):
            count[m] = count.get(m, 0) + 1
    return count, len(rels)


def main():
    count, total = measure()

    if "--write-baseline" in sys.argv:
        json.dump(count, open(BASELINE, "w", encoding="utf-8"), indent=1,
                  sort_keys=True)
        print("baseline written: %d pass marker(s) across %d page(s)"
              % (len(count), total))
        return

    print("%d pass marker(s) reachable from a page's cascade, of %d page(s)"
          % (len(count), total))
    full = sum(1 for v in count.values() if v == total)
    print("  %d pass(es) reach every page; %d reach fewer"
          % (full, len(count) - full))

    if "--check" not in sys.argv:
        for k, v in sorted(count.items(), key=lambda x: x[1]):
            print("  %4d  %s" % (v, k))
        return

    if not os.path.exists(BASELINE):
        sys.exit("no baseline - run --write-baseline first")
    old = json.load(open(BASELINE, encoding="utf-8"))
    bad = []
    for k, was in sorted(old.items()):
        now = count.get(k, 0)
        if now < was - SLACK:
            bad.append("%s reached %d page(s), now %d" % (k, was, now))
    gone = sorted(set(old) - set(count))
    for k in gone:
        if old[k] > SLACK:
            bad.append("%s has disappeared entirely (was %d page(s))"
                       % (k, old[k]))
    if bad:
        print()
        for b in bad:
            print("  DROPPED  %s" % b)
        sys.exit("%d pass(es) lost ground. Something downstream is removing "
                 "their work - see this file's docstring for the three times "
                 "that has happened before." % len(bad))
    print("no pass has lost ground against the baseline.")


if __name__ == "__main__":
    main()
