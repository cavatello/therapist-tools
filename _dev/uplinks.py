#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every content page a way back up to its topic.

WHY. The library restructure gave the site five topic hubs and a route down
into them. What it did not give it was the route back UP from a leaf, and that
direction is the one that carries the SEO weight: a hub that links to forty
pages and receives nothing from them concentrates no authority and tells a
crawler nothing about which pages belong together.

Help Scout gets away with having no up-link at all - no breadcrumb, no related
posts, three in-body links in a 3,500-word article - because it has three
categories, a persistent sub-nav on every page, and enormous domain authority.
We have none of those, so we do the thing properly.

WHAT IT ADDS, at the foot of every registered page: the topic it belongs to,
three siblings chosen from the same topic, and a link to the hub. Siblings are
picked by weight, so a leaf page links to its topic's strongest pages rather
than to whatever sorted first - which is also the behaviour that makes the
block worth a reader's attention rather than being furniture they learn to skip.

WHAT IT DELIBERATELY DOES NOT ADD. No "you might also like" across topics, no
tag list, no recirculation module with eight thumbnails. One block, one topic,
four links.

Directory leaves - the 65 programme pages and the 16 training pages - get the
block too, but their siblings are drawn from the non-leaf pages of their topic.
A school page listing three other school pages would be a worse version of the
directory it already links to.

Idempotent: the block is delimited by a marker and rewritten in place.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")
MARK = "<!-- _dev/uplinks.py -->"
END = "<!-- /uplinks -->"
CHECKED = "Aug 2026"


def esc(x):
    return html.escape(str(x)) if x is not None else ""


if not os.path.exists(REGISTRY):
    sys.exit("uplinks: %s missing - refusing to run rather than write a block "
             "that points nowhere" % REGISTRY)
REG = json.load(open(REGISTRY, encoding="utf-8"))
PAGES = {p["file"]: p for p in REG["pages"]}
TOPICS = REG["topics"]

# THE MARKER INSIDE THE STYLESHEET MUST BE A CSS COMMENT, NOT AN HTML ONE.
#
# This block used to open with MARK - the string "<!-- _dev/uplinks.py -->" -
# and that one line silently deleted the rule underneath it for as long as the
# up-link has existed.
#
# "<!--" is a CDO token. CSS tolerates it BETWEEN rules, so nothing errored and
# nothing showed in the console - but the text after it, "_dev/uplinks.py -->",
# is then read as the start of a selector, and the parser keeps consuming until
# it finds a "{". The "{" it finds is the one belonging to `.uplink`. So the
# rule that actually shipped was
#
#     _dev/uplinks.py --> .uplink { max-width:1120px;margin:34px auto 8px }
#
# an invalid selector, and the whole rule was dropped. The up-link therefore had
# no max-width and no auto margins: it ran the full width of the viewport with
# 26px of padding, while the footer directly beneath it sat in a 1180px centred
# column. On a 1280px screen that reads as slightly off; on a 2560px screen the
# two blocks are 700px out of alignment, which is what "the footer looks broken"
# was describing.
#
# A CSS comment marks the block just as well and cannot eat a selector.
CSSMARK = "/* _dev/uplinks.py */"

CSS = """<style>%s
/* The up-link. Quiet by default - it is the last thing on the page and it is
   for the reader who finished, not a mid-article interruption. */
.uplink{max-width:1120px;margin:34px auto 8px;padding:0 26px}
.uplink>div{background:#FBF6E9;border:1px solid #EFE6D2;border-radius:14px;padding:22px 24px}
.uplink .uk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.6px;
  letter-spacing:.12em;text-transform:uppercase;color:#9A8F76;margin:0 0 6px}
.uplink h2{font-family:Fraunces,Georgia,serif;font-size:20px;line-height:1.25;
  font-weight:600;color:#17271F;margin:0 0 5px}
.uplink .ud{font-size:14.2px;line-height:1.62;color:#4A5A46;margin:0 0 15px;max-width:64ch}
.uplink .ug{display:grid;grid-template-columns:repeat(auto-fit,minmax(228px,1fr));gap:10px}
.uplink a.uc{display:block;background:#fff;border:1px solid #E7DFCC;border-radius:10px;
  padding:13px 15px;text-decoration:none;min-width:0}
.uplink a.uc:hover{border-color:#C9BFA4}
.uplink a.uc b{display:block;font-size:14.2px;line-height:1.4;color:#17271F;
  font-weight:500;margin-bottom:4px}
.uplink a.uc span{display:block;font-size:12.6px;line-height:1.5;color:#5A6A56}
.uplink .uall{display:inline-block;margin-top:14px;font-size:13.6px;color:#2C6350}
@media (max-width:560px){.uplink{padding:0 18px}.uplink>div{padding:18px 17px}}
</style>""" % CSSMARK


def siblings(p, n=3):
    """Three from the same topic, strongest first, never the page itself.

    Leaves draw from non-leaves: a school page pointing at three other school
    pages is a worse directory, and the directory is one click away already.
    """
    pool = [q for q in REG["pages"]
            if q["topic"] == p["topic"] and not q.get("skip")
            and q["file"] != p["file"] and q["format"] != "reference"
            and not q.get("leaf")]
    if len(pool) < n:
        pool += [q for q in REG["pages"]
                 if q["topic"] == p["topic"] and not q.get("skip")
                 and q["file"] != p["file"] and q not in pool]
    return sorted(pool, key=lambda q: (-q.get("weight", 1), q["question"]))[:n]


def block(p):
    T = TOPICS[p["topic"]]
    sibs = siblings(p)
    if not sibs:
        return ""
    cards = "".join(
        '<a class="uc" href="%s"><b>%s</b><span>%s</span></a>'
        % (esc(q["file"]), esc(q["question"]), esc(q["outcome"]))
        for q in sibs)
    n = len([q for q in REG["pages"]
             if q["topic"] == p["topic"] and not q.get("skip")])
    return ("%s\n<section class=\"uplink\"><div>"
            '<p class="uk">More on this</p><h2>%s</h2>'
            '<p class="ud">%s</p><div class="ug">%s</div>'
            '<a class="uall" href="%s/">All %d pages on %s &rarr;</a>'
            "</div></section>\n%s\n" % (MARK, esc(T["name"]), esc(T["tagline"]),
                                        cards, esc(p["topic"]), n,
                                        esc(T["name"].lower()), END))


SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")


def pages():
    return [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]


def main():
    added = skipped = 0
    for f in pages():
        p = PAGES.get(f)
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s
        # remove any previous block first, so the pass is a rewrite not an append
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)
        s = re.sub(r"\n?<style>(?:" + re.escape(MARK) + "|"
                   + re.escape(CSSMARK) + r")[\s\S]*?</style>\n?", "", s)

        # A page with no registry record gets nothing. That is not a failure -
        # the topic hubs, the question index and the changelog are the library
        # itself and already carry their own navigation.
        if p and not p.get("skip") and f not in (
                "resources.html", "questions.html", "calculators.html",
                "changes.html"):
            # Eleven pages predate the <main> convention and wrap their body
            # in <article> or nothing at all. They all have a <footer>, so the
            # block goes immediately above it, which is the same place visually.
            b = block(p)
            anchor = "</main>" if "</main>" in s else (
                "<footer" if "<footer" in s else None)
            if b and anchor:
                s = s.replace(anchor, b + anchor, 1)
                s = s.replace("</body>", "\n" + CSS + "\n</body>", 1)
                added += 1
            elif b:
                skipped += 1
        if s != before:
            open(path, "w", encoding="utf-8").write(s)

    print("up-link blocks written %d" % added)
    if skipped:
        print("no </main> to anchor to %d" % skipped)

    # ---- guards
    bad = 0
    live = set(pages())
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        n = s.count(MARK)
        if n > 2:                       # the block marker plus the stylesheet
            print("GUARD %s: %d markers - the pass appended instead of "
                  "rewriting" % (f, n)); bad += 1
        if MARK not in s:
            continue
        if s.count(END) != 1:
            print("GUARD %s: unterminated block" % f); bad += 1
        m = re.search(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), s)
        for href in re.findall(r'href="([^"#?]+)"', m.group(0) if m else ""):
            tgt = href.rstrip("/")
            if href.endswith("/"):
                if tgt not in SUBDIRS:
                    print("GUARD %s: up-link points at unknown topic %s"
                          % (f, href)); bad += 1
            elif href not in live:
                print("GUARD %s: up-link points at missing %s" % (f, href))
                bad += 1
        # the block must come before the footer, never after it
        if "<footer" in s and s.index(MARK) > s.index("<footer"):
            print("GUARD %s: block sits below the footer" % f); bad += 1
        if s.count("</h1>") and s.count("<h1") != 1:
            print("GUARD %s: %d h1" % (f, s.count("<h1"))); bad += 1
    if bad:
        sys.exit("uplinks: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
