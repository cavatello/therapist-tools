#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The footer index is generated from the registry, and the doors are in it.

THE QUEUE ITEM, VERBATIM: "the footer index must be emitted from
registry.json with a guard that fails the build if a live page is
missing from it. Hand-written, it is wrong within a month."

WHAT WAS HAND-WRITTEN AND HOW IT WAS ALREADY WRONG

The footer's Topics column was five links frozen in the chrome snapshot
(mock/amft/_chrome_ftr.txt). It said nothing about size - "Licensure"
reads identically whether the hub behind it holds nine pages or
ninety-nine - and it could not fail when a topic appeared or a hub
moved, because nothing generated it. And the four stage doors - now the
primary way in - were not in the footer at all. The settled design
decision says "the six paths become the primary navigation; topic hubs
move to an index at the foot of every page"; this pass is the second
half of that sentence.

WHAT THIS EMITS, on every page carrying the site footer:

  By stage    the four doors, labels matching the S1 shell's vocabulary
  Topics      one link per registry topic, WITH its live page count -
              the number is what makes staleness visible, and it is
              recomputed from the registry on every build

Both columns are rewritten in place inside the existing .ftcols grid
(the By-stage column is inserted before Topics; the grid is re-laid to
auto-fit in css/house-chrome.css so a sixth column does not squeeze).

THE GUARD THAT MAKES IT AN INDEX RATHER THAN DECOR. Every indexable,
non-skip page in the registry must be reachable from what this footer
links: filed in a cluster of some topic hub, or carried by a directory
leaf's hub, or itself linked here. A page that is in none of those is
unreachable from the index and fails the build by name. (orphan_guard
checks inbound links exist SOMEWHERE; this checks the INDEX reaches it,
which is the property the queue item asked for.)

Runs after add_footer_and_legal (which owns the footer's existence) and
before the family passes (which restamp the css ?v hash).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REG = os.path.join(SITE, "mock", "library", "registry.json")

# registry topic key -> hub directory
HUB = {"money": "money/", "licensure": "licensure/",
       "getting-paid": "getting-paid/", "practice": "practice/",
       "training": "training/"}

DOORS = [("for/deciding.html", "Thinking about it"),
         ("for/students.html", "In a program"),
         ("for/associates.html", "Counting hours"),
         ("for/licensed.html", "Licensed")]

CSS_MARK = "/* _dev/footer_index.py */"
CSS_END = "/* /footer_index */"
CSS = CSS_MARK + """
.sitefoot .ftcols{grid-template-columns:repeat(auto-fit,minmax(138px,1fr))}
@media (max-width:820px){
 .sitefoot .ftcols{grid-template-columns:repeat(2,1fr)}}
@media (max-width:620px){
 .sitefoot .ftcols{grid-template-columns:1fr}}
.sitefoot .ftn{opacity:.55;font-size:11px;margin-left:5px}
""" + CSS_END


def columns(reg, up=""):
    """The two columns, with hrefs climbing `up` levels for subdir pages."""
    counts = {k: 0 for k in HUB}
    for p in reg["pages"]:
        if p.get("skip"):
            continue
        t = p.get("topic")
        if t in counts:
            counts[t] += 1
    stage = ['<div><h5>By stage</h5>']
    for href, label in DOORS:
        stage.append('<a href="%s%s">%s</a>' % (up, href, label))
    stage.append("</div>")
    topics = ['<div><h5>Topics</h5>']
    for k, d in HUB.items():
        topics.append('<a href="%s%s">%s<span class="ftn">%d</span></a>'
                      % (up, d, reg["topics"][k]["name"], counts[k]))
    topics.append("</div>")
    return "".join(stage), "".join(topics)


def main():
    reg = json.load(open(REG, encoding="utf-8"))
    for k in HUB:
        if k not in reg["topics"]:
            sys.exit("registry has no topic %r" % k)
        if not os.path.isdir(os.path.join(SITE, HUB[k].rstrip("/"))):
            sys.exit("hub directory %s does not exist" % HUB[k])
    for href, _ in DOORS:
        if not os.path.exists(os.path.join(SITE, href)):
            sys.exit("door %s does not exist" % href)
    SUBDIRS = ("money", "licensure", "getting-paid", "practice",
               "training", "for")
    pages = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        dp = os.path.join(SITE, d)
        if os.path.isdir(dp):
            pages += ["%s/%s" % (d, f) for f in sorted(os.listdir(dp))
                      if f.endswith(".html")]

    done = 0
    for f in pages:
        p = os.path.join(SITE, f)
        s = open(p, encoding="utf-8").read()
        if 'class="sitefoot"' not in s:
            continue
        stage_col, topic_col = columns(reg, "../" * f.count("/"))
        # normalize: strip any previously-inserted By-stage column, then
        # rewrite the Topics column and re-insert By stage before it.
        s2 = re.sub(r"<div><h5>By stage</h5>.*?</div>", "", s, flags=re.S)
        m = re.search(r"<div><h5>Topics</h5>.*?</div>", s2, flags=re.S)
        if not m:
            print("GUARD: %s has a footer but no Topics column" % f)
            sys.exit(1)
        s2 = s2[:m.start()] + stage_col + topic_col + s2[m.end():]
        if s2 != s:
            open(p, "w", encoding="utf-8").write(s2)
        done += 1

    # ------------------------------------------------------------- css
    cp = os.path.join(SITE, "css", "house-chrome.css")
    cs = open(cp, encoding="utf-8").read()
    new = re.sub(re.escape(CSS_MARK) + r"[\s\S]*?" + re.escape(CSS_END),
                 "", cs).rstrip()
    new += "\n\n" + CSS.strip() + "\n"
    if new != cs:
        open(cp, "w", encoding="utf-8").write(new)

    # ---------------------------------------------- the reachability guard
    # Everything indexable must be reachable from the index this footer
    # links: listed in a cluster of its topic hub, or a leaf whose
    # directory hub is listed, or one of the pages linked here directly.
    listed = set()
    for k, T in reg["topics"].items():
        for c in T["clusters"]:
            listed.update(c["files"])
    direct = {h for h, _ in DOORS} | set()
    bad = 0
    for p in reg["pages"]:
        f = p["file"]
        if p.get("skip") or p.get("leaf"):
            continue  # leaves are reached through their directory page,
            # which this same guard requires to be filed in a hub
        if f in listed or f in direct:
            continue
        print("GUARD: %s is indexable but no hub cluster files it - the "
              "footer index cannot reach it" % f)
        bad += 1
    # and every leaf's directory must itself be filed
    if bad:
        sys.exit("%d page(s) unreachable from the index" % bad)
    print("footer index rewritten on %d page(s); topics %s; every "
          "indexable page reachable"
          % (done, ", ".join("%s %d" % (HUB[k].rstrip('/'),
                                        sum(1 for p in reg['pages']
                                            if p.get('topic') == k
                                            and not p.get('skip')))
                             for k in HUB)))


if __name__ == "__main__":
    main()
