#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three defects reported from the live site, fixed together.

1. HEADWAY'S CARDS RENDERED ONE WORD PER LINE.

   A class collision, and a good one. headway-for-california-therapists.html
   defines its own `.fact` inline as a two-column ROW - label on the left, the
   figure on the right:

       .fact{display:grid;grid-template-columns:minmax(0,1fr) 190px}

   The shared site stylesheet defines a `.facts` from a completely different
   template - the three-across card grid on the About page:

       .facts{display:grid;grid-template-columns:repeat(3,1fr)}

   `extract_css.py` emits the shared file as a <link> AFTER the page's inline
   <style>, so the shared rule wins. Each row was squeezed into a 285px cell
   while still reserving 190px for its figure, leaving 45px for the text. At
   45px, "Membership or subscription fee" is five lines of one word.

   Renamed rather than fought with !important: two templates wanted the same
   four-letter class name for different things, and only one of them can have
   it. The page-local one is the one that moves.

2. THE COST CHART NAMED 34 SCHOOLS AND LINKED NONE OF THEM.

   Every bar carries an institution that has a page on this site. A reader
   looking at "$152,340 - University of Southern California" and wanting to
   know what that buys had to scroll back up and find it in the directory.
   Hrefs are read from the directory's own rows, so a school with no page yet
   stays plain text rather than getting a link that 404s.

3. THE BADGE LEGEND ON about.html WAS UNREADABLE.

   Each row was one <p> with the pill as its first inline child, so the badge
   sat on the sentence's baseline with its text starting hard against the
   pill's right edge. Pills are objects, not words; they need their own column.

Idempotent. Guarded. Run before restyle.py.
"""
import os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

HEADWAY = os.path.join(SITE, "headway-for-california-therapists.html")
DIRECTORY = os.path.join(SITE, "mft-programs-california.html")
ABOUT = os.path.join(SITE, "about.html")


# --------------------------------------------------------------- 1. collision
def fix_headway():
    if not os.path.exists(HEADWAY):
        return 0
    s = open(HEADWAY, encoding="utf-8").read()
    orig = s
    # The inline stylesheet and the markup, together - renaming one without the
    # other is worse than leaving both.
    pairs = [
        (".facts{", ".hwfacts{"),
        (".facts {", ".hwfacts {"),
        (".fact{", ".hwfact{"),
        (".fact {", ".hwfact {"),
        (".fact h4", ".hwfact h4"),
        (".fact p", ".hwfact p"),
        (".fact .v", ".hwfact .hwv"),
        ('<div class="facts">', '<div class="hwfacts">'),
        ('<div class="fact">', '<div class="hwfact">'),
        ('<div class="v ">', '<div class="hwv">'),
        ('<div class="v np">', '<div class="hwv np">'),
        ('<div class="v">', '<div class="hwv">'),
    ]
    for a, b in pairs:
        s = s.replace(a, b)
    if s != orig:
        open(HEADWAY, "w", encoding="utf-8").write(s)
        return 1
    return 0


# ------------------------------------------------------------------ 2. links
def norm(name):
    n = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    n = re.sub(r"&(?:[a-z]+|#\d+|#x[0-9a-fA-F]+);", " ", n)
    n = re.sub(r"\([^)]*\)", " ", n)
    return re.sub(r"[^a-z0-9]+", "", n.lower())


def link_chart():
    if not os.path.exists(DIRECTORY):
        return 0
    s = open(DIRECTORY, encoding="utf-8").read()

    links = {}
    for art in re.findall(r'<article class="pg"[\s\S]*?</article>', s):
        h3 = re.search(r"<h3>(.*?)</h3>", art)
        a = re.search(r'href="([a-z0-9-]+-mft\.html)"', art)
        if h3 and a:
            links[norm(h3.group(1))] = a.group(1)

    # Labels are truncated in the chart ("California State University, Full...")
    # so an exact match will miss. Fall back to a prefix match on the
    # normalised name, which is unambiguous here: no two institutions on the
    # Board's list share a 20-character prefix.
    keys = sorted(links)

    def find(label):
        k = norm(label)
        if k in links:
            return links[k]
        k = k.rstrip(".")
        cands = [x for x in keys if x.startswith(k[:20])] if len(k) >= 12 else []
        return links[cands[0]] if len(cands) == 1 else None

    n = [0]

    def sub(m):
        label = m.group(1)
        if "<a " in label:
            return m.group(0)
        href = find(re.sub(r"<[^>]+>", "", label))
        if not href:
            return m.group(0)
        n[0] += 1
        return ('<span class="ig-l"><a href="%s">%s</a></span>' % (href, label))

    out = re.sub(r'<span class="ig-l">(.*?)</span>', sub, s)
    if out != s:
        open(DIRECTORY, "w", encoding="utf-8").write(out)
    return n[0]


# ----------------------------------------------------------------- 3. legend
LEGEND_CSS = """<style>/* _dev/fixups.py */
/* The badge legend on about.html. Two columns - pill, then meaning - so the
   pill is never on the same baseline as the sentence it labels. */
.tblegend>div{display:grid;grid-template-columns:212px minmax(0,1fr);
  gap:6px 18px;align-items:start;padding:12px 0;border-top:2px dashed #D9D0BA}
.tblegend>div:first-child{border-top:none;padding-top:4px}
.tblegend .tsbadge{margin:1px 0 0;justify-self:start}
.tblegend p{margin:0;font-size:13.6px;line-height:1.6;color:#3A3529;max-width:62ch}
@media (max-width:760px){.tblegend>div{grid-template-columns:minmax(0,1fr);gap:8px}}
</style>"""


def fix_legend():
    if not os.path.exists(ABOUT):
        return 0
    s = open(ABOUT, encoding="utf-8").read()
    orig = s
    # <p><span class=tsbadge …>…</span>text…</p>  ->  <div><span…></span><p>text…</p></div>
    def one(m):
        return "<div>%s<p>%s</p></div>" % (m.group(1), m.group(2))

    s = re.sub(r'<p>(<span class="tsbadge[^"]*">[^<]*</span>)([\s\S]*?)</p>',
               one, s)
    s = re.sub(r"\n?<style>/\* _dev/fixups\.py \*/[\s\S]*?</style>\n?", "", s)
    i = s.lower().rfind("</body>")
    s = s[:i] + LEGEND_CSS + "\n" + s[i:]
    if s != orig:
        open(ABOUT, "w", encoding="utf-8").write(s)
        return 1
    return 0


def main():
    print("headway .fact collision: %s"
          % ("renamed" if fix_headway() else "already clean"))
    print("cost chart: %d bar label(s) linked" % link_chart())
    print("about legend: %s" % ("rebuilt" if fix_legend() else "already clean"))

    bad = 0
    s = open(HEADWAY, encoding="utf-8").read()
    if re.search(r'<div class="fact">', s) or ".fact{" in s or ".fact {" in s:
        print("GUARD headway: a bare .fact survives and will collide again")
        bad += 1
    if 'class="hwfact"' not in s:
        print("GUARD headway: the renamed cards are gone")
        bad += 1
    d = open(DIRECTORY, encoding="utf-8").read()
    for href in set(re.findall(r'<span class="ig-l"><a href="([^"]+)"', d)):
        if not os.path.exists(os.path.join(SITE, href)):
            print("GUARD directory: chart links %s which does not exist" % href)
            bad += 1
    a = open(ABOUT, encoding="utf-8").read()
    if re.search(r'<p><span class="tsbadge', a):
        print("GUARD about: a legend row is still an inline <p>")
        bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
