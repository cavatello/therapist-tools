#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The override sheets the family passes strip, put back where they belong.

THE MECHANISM, FOUND IN SOURCE RATHER THAN GUESSED AT

Seven passes in the FLOORS stage write a `<style>` block of overrides.
`extract_css.py` hoists each block into its own `css/<hash>.css` - one
marker per file, nothing else mixed in, which is what makes this fixable:

    314849add915.css  token_floor        1,486 b
    3cdb931d4f5e.css  block_spacing        870 b
    76e7e0da7d86.css  nav_type_floor     2,946 b
    88f6a971a5b9.css  one_grid           5,155 b
    97ebf82c2256.css  dark_band_labels     392 b
    9fb0332fa15a.css  contrast_pass        586 b
    cc63adb6f6f0.css  content_frame      6,161 b

Then `family_art.py`, `family_pk.py`, `family_sc.py` and `family_for.py`
each run `HASH_LINK.sub("", s)` - **strip every content-addressed link** -
because rollout step 5 says a converted page carries no legacy CSS. That
was right when the hashed sheets held only legacy page CSS. It stopped
being right the moment the floors' overrides were hoisted into the same
namespace.

WHAT IT ACTUALLY COST, MEASURED

Not "a marker is missing" - that proves nothing, since a family pass can
port a rule without its comment. The test is: **does a page that HAS the
element lack the rule?**

    content_frame   `.bcr` (the breadcrumb) on  89 of 134 pages that have it
                    `.artwrap`/`.artband`  on  23 of  24
    block_spacing   `.tsshort + *` et al  on  89 of 112
    token_floor     `.n.n.n`              on  43 of  55

Spacing and one contrast lift, which is why nothing looked broken and no
sweep complained: a margin is slightly wrong, a colour is not lifted. The
kind of thing that is invisible individually and is the whole difference
between a design system and a pile of pages.

WHY NOT THE TWO OBVIOUS FIXES

**Stop hoisting them** - opt these blocks out of `extract_css.py` so they
stay inline and nothing can strip them. Measured: **17.2 KB per page**,
uncacheable, on 242 pages. That is ~4 MB, and `extract_css.py` exists
precisely because this site once shipped 3.5 MB of duplicated CSS and a
Pages deploy timed out on the payload. Trading that back to fix a margin
is the wrong trade.

**Move the seven passes after the families** - which worked for
`surface_fix.py`. But `token_floor.py` also rewrites and rehashes
stylesheets, and moving it past `dead_css.py`/`dead_rules.py` would let it
rename sheets those passes have already accounted for. Splitting a pass in
two to reorder half of it is worse than this.

So: the sheets are re-linked, after the families have finished stripping
them. One pass, no new bytes, and the sheets stay shared and cached.

WHICH PAGES GET WHICH SHEET

Only a page that carries at least one class the sheet's selectors name. A
page with no `.artwrap` has no use for `content_frame`'s rules and should
not spend a request on them. That check is what keeps this from being
seven extra requests on 242 pages.

The link goes at the END of the body, after the family sheets, so an
override still outranks the family rule it is there to override. It goes
in BEFORE `surface_fix.py` and `mobile_last.py` inject theirs, so those
two keep the last word - and `mobile_last.py` guards that nothing is
linked after it, which is the check that this pass has not stolen it.

Idempotent: a page that already links a sheet is left alone.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# The passes whose overrides must survive the family rewrite. Discovered by
# marker rather than by filename: a content-addressed sheet is renamed
# whenever its bytes change, so hardcoding the hash would go stale on the
# next build that touches any of these blocks.
PROTECTED = ("_dev/contrast_pass.py", "_dev/token_floor.py",
             "_dev/block_spacing.py", "_dev/content_frame.py",
             "_dev/dark_band_labels.py", "_dev/nav_type_floor.py",
             "_dev/one_grid.py")
CLS = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")
HASHED = re.compile(r"^[0-9a-f]{12}$")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    # ---- which sheet carries which pass, and what classes it styles
    owned = {}
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css") or not HASHED.fullmatch(fn[:-4]):
            continue
        body = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        who = [m for m in PROTECTED if m in body]
        if not who:
            continue
        classes = set(CLS.findall(body))
        owned[fn] = (who, classes)
    if not owned:
        print("no override sheet found - extract_css may not have run yet")
        return
    for fn, (who, cs) in sorted(owned.items()):
        print("  css/%-20s %-22s %d class(es)"
              % (fn, ",".join(w.split("/")[-1][:-3] for w in who), len(cs)))

    added, touched = 0, 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        used = set()
        for m in re.finditer(r'class="([^"]*)"', s):
            used |= set(m.group(1).split())
        up = "../" * rel.count("/")
        want = []
        for fn, (_who, classes) in sorted(owned.items()):
            if "css/" + fn in s:
                continue                      # already linked
            if not (classes & used):
                continue                      # nothing on this page needs it
            want.append(fn)
        if not want:
            continue
        i = s.rfind("</body>")
        if i < 0:
            print("  SKIP %s has no </body>" % rel)
            continue
        block = "".join('<link rel="stylesheet" href="%scss/%s">\n' % (up, fn)
                        for fn in want)
        s = s[:i] + block + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1
            added += len(want)
    print("%d override link(s) restored on %d page(s)" % (added, touched))

    # ------------------------------------------------------------- guards
    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        used = set()
        for m in re.finditer(r'class="([^"]*)"', s):
            used |= set(m.group(1).split())
        for fn, (who, classes) in owned.items():
            if (classes & used) and "css/" + fn not in s:
                print("GUARD %s has %d class(es) styled by css/%s and does "
                      "not link it" % (rel, len(classes & used), fn))
                bad += 1
        for m in re.finditer(r'href="(?:\.\./)*css/([^"?]+\.css)', s):
            if not os.path.exists(os.path.join(CSSDIR, m.group(1))):
                print("GUARD %s links css/%s, which is not there"
                      % (rel, m.group(1)))
                bad += 1
    if bad:
        sys.exit("%d problem(s)" % bad)
    print("guard clean - every page that carries a class one of these sheets "
          "styles now links it")


if __name__ == "__main__":
    main()
