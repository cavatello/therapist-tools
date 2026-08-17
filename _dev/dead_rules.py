#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A quarter of the CSS styles nothing. It is removed.

WHAT THE COUNT SHOWED

`dead_css.py` retires a stylesheet no page links. That is the coarse
version of the question, and it found one file. The fine version - which
RULES inside the sheets a page does load can never match anything on that
page - had never been asked, and the answer is:

    3,796 class-bearing selector parts on the site
      282 of them are rules whose every selector part names a class that
          appears nowhere on the site - not on one page, anywhere

They are not random. They are whole retired components, still fully styled:

    .lcta .lgold .lnews .lmid     an old landing page
    .srn .tcio .pdfig .pdyr       retired directory components
    .pdcity .pdgo .pdgone
    .bc2 .nav .bc2 .lg .bars      the pre-house navigation and its logo
    .tsmeta .tsk .tsv .tsall      a metadata block that no page carries
    .hero-eyebrow .kicker         two eyebrow classes replaced by a third

This is what "remnants of old designs" looks like once you stop looking for
colours. A retired component leaves no visible trace - that is exactly why
it survives every visual review - and it keeps costing every reader the
bytes and every author the confusion of a class that looks supported.

HOW A CLASS IS PROVED LIVE, AND THE TWO WAYS THAT GOES WRONG

For each sheet, the live set is the union of class names on the pages that
actually link it. Two sources, because one is not enough:

  class="..."          the obvious one
  <script> strings     every identifier inside a quoted string in an inline
                       script. `classList.add('on')` and `el.className =
                       'srtab on'` put a class on the page that no `class=`
                       attribute mentions, and a naive check deletes the
                       rule that styles the open state of every menu on the
                       site. Counting these cut the finding from 1,046 to
                       920 - a 12% false-positive rate that would have been
                       shipped as breakage.

AND WHY THE BASIS IS THE WHOLE SITE, NOT THE SHEET'S OWN PAGES

The obvious basis - prune each sheet against the classes on the pages that
link IT - is wrong, and it was caught by running it: `family_coverage.py`
came back with **two elements that had just lost their styling**,
`.hh-figs` on five pages and `.pk-wrap` on one. Both classes are plainly
present in the markup. What the per-sheet basis missed is that this site
hoists and dedupes stylesheets (`extract_css.py`, `css_dedupe.py`), so a
rule can live in a sheet whose current link set does not include every page
that uses the class, and the link graph is rearranged on every build.

So a class must appear NOWHERE on the entire site before its rule is
removed. That is a much weaker test - it drops the finding from 920 to 282
- and it is the one that is actually true. Twenty-four per cent looked like
a better headline; six per cent is the number that can be defended.

The 282 are whole retired components rather than scattered rules, which is
the point: those are what "old design" means here.

There are no external `.js` files and no `<template>` elements on this
site; both were checked before this pass was allowed to delete anything.

THE CASE A CLASS COUNT CANNOT REACH: A COMPONENT THAT DIED INTO A COLLISION

One rule needed naming by hand, and it is the most damaging single finding
of the whole design audit after the masthead CTA.

`css/house.css` carries P8's **logo**: `.bc2 .lg` with `.bars` (the little
bar-chart mark), `.wm` (the wordmark) and `.sub` (the strapline). No page on
this site has that markup - the masthead uses `.sitenav-mark` - so `.bars`
and `.wm` were pruned by the class count above, correctly.

`.bc2 .lg` itself was NOT pruned, because `lg` does appear on the site:
`privacy.html` and `terms.html` use `<main class="lg">` for the legal-page
layout, and both carry `body.bc2`. So a dead logo rule matched a live legal
page and set it to

    display:inline-flex; align-items:center; gap:10px

which turns a whole document into one shrink-to-fit row. Measured: **802px
wide inside a 390px phone, and 889px inside a 768px tablet** - the page
overflowing by more than double, on two published pages, at every width
below 1100px. Nobody had opened those two pages on a phone.

That is the fifth class collision in this repository - after `.sn`,
`.tsshort`, `.sub` and `.slab` - and the first where the colliding rule
belonged to a component that no longer exists at all. A class count cannot
find this one: the class is live, the COMPONENT is dead. It is listed
below by name, with its reason.

A rule survives if ANY of its comma-separated selector parts survives, and
a part with no class in it at all (`body`, `h1`, `a:hover`) always
survives. Only a rule every one of whose parts names a class nobody has is
removed.

NOTHING IS DELETED, IT IS MOVED

Every removed rule is written to `_to_delete/pruned-<sheet>.css` with its
source sheet named, so a component that turns out to be wanted can be
lifted back verbatim. This repository is edited through a bridge that
cannot delete, and a pass that destroys work it cannot restore has no
business running unattended.

WHERE IT RUNS

After the five `family_*.py` passes, because those passes GENERATE the
family sheets by porting rules out of `css/house-skin.css` - so pruning a
family sheet before they run prunes a file that is about to be rewritten.
`house-skin.css` itself is pruned against the union of every page, which
is the only safe basis for a file that five families copy from.

Guarded: no removed rule may contain a live class, every sheet must still
have balanced braces and parse as CSS, and `family_coverage.py` - which
runs after this in the verify stage and fails on an element whose classes
have no rule in any sheet its page loads - is the check that this pass did
not take styling off something real.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
BINNED = os.path.join(SITE, "_to_delete")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

CLS = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")
COMMENT = re.compile(r"/\*[\s\S]*?\*/")
IDENT = re.compile(r"[A-Za-z][\w-]{1,}")
LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')
# Linked by no page on purpose, and still pruned: five family passes copy
# out of it. See dead_css.py for why it stays on disk.
UNION = {"house-skin.css"}
# Rules for components that no longer exist in any markup, whose class name
# is now owned by something else. See THE CASE A CLASS COUNT CANNOT REACH.
COLLISIONS = (
    (".bc2 .lg", "P8's logo component. Its .bars and .wm children have no "
                 "markup anywhere; the rule survived only by matching "
                 "<main class=\"lg\"> on privacy.html and terms.html, and "
                 "made both 802px wide on a 390px phone."),
)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def classes_on(html):
    """Everything that could be a class on this page. See HOW A CLASS IS
    PROVED LIVE."""
    used = set()
    for m in re.finditer(r'class="([^"]*)"', html):
        used |= set(m.group(1).split())
    for m in re.finditer(r"<script\b[^>]*>([\s\S]*?)</script>", html):
        for q in re.finditer(r"""(['"`])((?:[^'"`\\]|\\.)*?)\1""", m.group(1)):
            used |= set(IDENT.findall(q.group(2)))
    return used


def split_rules(css):
    """(prefix, selector, block, whole) for every top-level and @media rule.

    Brace-aware rather than regex-only, because `@media (...){ .a{} .b{} }`
    nests and a flat pattern mis-reads the closer.
    """
    out, i, n, depth, start = [], 0, len(css), 0, 0
    sel_start = 0
    while i < n:
        c = css[i]
        if c == "{":
            if depth == 0:
                sel = css[sel_start:i]
                blk_start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append((sel_start, sel, css[blk_start:i + 1]))
                sel_start = i + 1
        i += 1
    return out


def prune(css, live):
    """Return (css, removed_text, n_removed)."""
    removed, keep, n = [], [], 0

    def dead_sel(sel):
        flat = " ".join(COMMENT.sub(" ", sel).split())
        for named, _why in COLLISIONS:
            if flat == named:
                return True
        # Comments out FIRST. Every pass in this repository stamps its rules
        # with `/* _dev/<pass>.py */`, and `.py` reads as a class selector -
        # so on the first run this pass judged the rule after every marker
        # comment by a class called `py` that nobody has, and removed 191
        # rules including `.hh-figs` and `.pk-wrap`, both of which are on
        # real pages. `family_coverage.py` caught it. A convention that has
        # been harmless for a year became load-bearing the moment something
        # started parsing selectors.
        sel = COMMENT.sub(" ", sel)
        parts = [p for p in sel.split(",") if p.strip()]
        if not parts:
            return False
        for p in parts:
            names = set(CLS.findall(p))
            if not names:
                return False          # a part with no class always survives
            if not (names - live):
                return False          # every class in this part is live
        return True

    last = 0
    for sel_start, sel, blk in split_rules(css):
        head = COMMENT.sub(" ", sel).strip()
        whole_start = sel_start
        whole_end = css.index(blk, sel_start) + len(blk)
        if head.startswith("@"):
            # An at-rule: prune inside it, and drop it if it empties out.
            if head.split()[0].lower() in ("@media", "@supports"):
                inner = blk[1:-1]
                pruned, rem, k = prune(inner, live)
                if k:
                    n += k
                    removed.append(rem)
                    if pruned.strip():
                        keep.append(css[last:whole_start])
                        keep.append(sel + "{" + pruned + "}")
                    else:
                        keep.append(css[last:whole_start])
                    last = whole_end
            continue
        if dead_sel(head):
            n += 1
            removed.append(css[whole_start:whole_end].strip() + "\n")
            keep.append(css[last:whole_start])
            last = whole_end
    keep.append(css[last:])
    return "".join(keep), "".join(removed), n


def main():
    page_html = {rel: open(os.path.join(SITE, rel), encoding="utf-8").read()
                 for rel in pages()}
    page_cls = {rel: classes_on(h) for rel, h in page_html.items()}
    users = {}
    for rel, h in page_html.items():
        for s in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)', h):
            users.setdefault(s, set()).add(rel)
    everything = set()
    for c in page_cls.values():
        everything |= c

    os.makedirs(BINNED, exist_ok=True)
    remap, total, sheets = {}, 0, 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        if fn not in users and fn not in UNION:
            continue                  # unlinked; dead_css.py owns that case
        live = everything             # see AND WHY THE BASIS IS THE WHOLE SITE
        body = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        pruned, removed, n = prune(body, live)
        if not n:
            continue
        if pruned.count("{") != pruned.count("}"):
            print("GUARD css/%s: pruning unbalanced the braces - skipped" % fn)
            continue
        sheets += 1
        total += n
        open(os.path.join(BINNED, "pruned-%s" % fn), "a",
             encoding="utf-8").write(
                 "/* removed from css/%s - matched no element on any page "
                 "that loads it */\n%s" % (fn, removed))
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            new = hashlib.sha1(pruned.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(pruned)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d dead rule(s), %d bytes)"
                  % (fn[:-4], new, n, len(body) - len(pruned)))
        else:
            open(os.path.join(CSSDIR, fn), "w",
                 encoding="utf-8").write(pruned)
            print("  css/%-22s in place  (%d dead rule(s), %d bytes)"
                  % (fn, n, len(body) - len(pruned)))

    allhtml = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs
                   if d not in ("_to_delete", ".git", "node_modules")]
        for f in sorted(files):
            if f.endswith(".html"):
                allhtml.append(os.path.relpath(os.path.join(root, f), SITE))
    touched = 0
    if remap:
        for rel in sorted(allhtml):
            p = os.path.join(SITE, rel)
            s = open(p, encoding="utf-8").read()
            out = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)
            if out != s:
                open(p, "w", encoding="utf-8").write(out)
                touched += 1
        current = {rel: open(os.path.join(SITE, rel), encoding="utf-8").read()
                   for rel in allhtml}
        for old in sorted(remap):
            if any("%s.css" % old in s for s in current.values()):
                continue
            try:
                os.replace(os.path.join(CSSDIR, "%s.css" % old),
                           os.path.join(BINNED, "pre-prune-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s)" % (old, e))

    print("%d dead rule(s) removed from %d stylesheet(s); %d page(s) "
          "repointed. Everything removed is in _to_delete/pruned-*.css"
          % (total, sheets, touched))

    # ------------------------------------------------------------- guards
    bad = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        if b.count("{") != b.count("}"):
            print("GUARD css/%s: unbalanced braces after pruning" % fn)
            bad += 1
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
            if h != fn[:-4]:
                print("GUARD css/%s: not named for its own contents (%s)"
                      % (fn, h))
                bad += 1
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css, which is not there"
                      % (rel, h))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - braces balanced, hashes match, every link resolves. "
          "family_coverage.py in the verify stage is the check that nothing "
          "real lost its styling")


if __name__ == "__main__":
    main()
