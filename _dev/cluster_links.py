#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close the loop between the calculators and the articles.

The content plan borrows its cluster shape from HubSpot's pillar-cluster model,
which has three linking rules: every cluster page links to its pillar, the
pillar links back to every cluster page, and clusters cross-link where the
topics genuinely overlap.

This site did the first and none of the second. Each article ends at a
calculator - that handoff is the whole reason an article gets written here -
but the calculators were dead ends. therapist-tax-strategy-california.html was
the destination of two shipped articles and linked to neither of them.

The inversion is worth naming, because it is not a mistake. In HubSpot's model
the pillar is a long page of prose and the clusters are shorter pages of prose.
Here the pillar is a TOOL. A reader who wants the argument reads the article; a
reader who wants their own number opens the calculator. Those are different
appetites, and the site should let a reader move in either direction rather
than only downhill towards the form.

Derived, not listed. The article is the thing that declares where it hands off
(its .arttool block), so the reverse index is read out of the built articles at
every run. Write a new article, point it at a calculator, and that calculator
picks it up on the next pass with no edit here. A hand-maintained table in this
file would be one more thing to forget.

Idempotent. Run after the articles are built and before linkcheck.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/cluster_links.py */"
TAG = "<!-- cluster links -->"

CSS = """
/* Articles that lead here. Deliberately quieter than the page's own calls to
   action: someone already on the calculator has what they came for, and this
   is an offer to read the reasoning, not a demand. */
.clus{margin:34px 0 8px;max-width:100%;border-top:1px solid #E2DACA;padding-top:20px}
.clus > b{display:block;font-size:12px;letter-spacing:.11em;text-transform:uppercase;
  color:#7C8878;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;margin-bottom:12px}
.clus .cl2{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:11px}
.clus a{display:block;background:#fff;border:1px solid #E2DACA;border-left:3px solid #3F9577;
  border-radius:9px;padding:13px 15px;text-decoration:none;color:inherit;min-width:0}
.clus a:hover{border-color:#C9BFA6;border-left-color:#3F9577;background:#FDFCF8}
.clus a strong{display:block;font-size:15.5px;line-height:1.3;margin-bottom:5px;color:#22301F}
.clus a span{display:block;font-size:13px;line-height:1.5;color:#5A6754}
.clus a i{display:block;font-style:normal;font-size:11.5px;color:#3F9577;margin-top:8px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
@media (max-width:520px){.clus a strong{font-size:14.5px}}
"""


def strip(t):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()


def articles():
    """(slug, title, dek, target) for every built article, read from the file."""
    out = []
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if 'class="artbody"' not in s:
            continue
        h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", s)
        dek = re.search(r'<p class="dek">([\s\S]*?)</p>', s)
        tool = re.search(r'<div class="arttool">[\s\S]*?<a href="([a-z0-9\-]+\.html)"', s)
        if not (h1 and dek and tool):
            print("SKIP %s: h1=%s dek=%s tool=%s"
                  % (f, bool(h1), bool(dek), bool(tool)))
            continue
        out.append((f, strip(h1.group(1)), strip(dek.group(1)), tool.group(1)))
    return out


def block(items):
    cards = "".join(
        '<a href="%s"><strong>%s</strong><span>%s</span><i>Read the argument &rarr;</i></a>'
        % (slug, html.escape(title), html.escape(dek if len(dek) < 190 else dek[:187] + "…"))
        for slug, title, dek in items)
    return ('%s<div class="clus"><b>The reasoning behind these numbers</b>'
            '<div class="cl2">%s</div></div>' % (TAG, cards))


# The page's own last paragraph of small print. Whichever of these appears last
# is the end of the content column, and inserting after it puts the block INSIDE
# that column rather than after it.
TAIL_P = ("disc", "pay-note", "fine")


def insert_at(s):
    """Immediately after the page's final line of small print.

    The first version inserted before </main>, which is outside every content
    wrapper on this site - so the cards rendered full-bleed, running to both
    viewport edges while the disclaimer directly above them sat inset by the
    wrapper's padding. Syntactically fine, visibly wrong, and invisible to a
    guard that only counts elements: the block was present, one per page, with
    the right links in it.

    Anchoring to the last <p class="disc|pay-note|fine"> instead puts the block
    in the same box as the page's own closing prose, so it inherits that
    column's width without this pass needing to know what the width is. It also
    keeps the intended reading order - the disclaimer stays the last word on
    the arithmetic, and this is an offer made afterwards.
    """
    main = s.rfind("</main>")
    if main < 0:
        return -1
    best, anchor = -1, None
    for cls in TAIL_P:
        for m in re.finditer(r'<p class="' + re.escape(cls) + r'"[^>]*>[\s\S]*?</p>', s[:main]):
            if m.end() > best:
                best, anchor = m.end(), cls
    return (best, anchor) if best > 0 else (main, None)


def width_rule(s, anchor):
    """Constrain .clus to exactly what constrains the paragraph above it.

    Anchoring inside the content column was necessary but not sufficient. On
    the tax page the paragraph's PARENT is full-bleed and `.disc` carries its
    own `max-width:1060px`, so the block still measured 1440px against the
    paragraph's 1060px - inset text with edge-to-edge cards directly beneath
    it. On the 3,000-hours page the parent is already constrained and the same
    block measured identically to its neighbour, which is why one page looked
    right and one did not.

    So read the anchor's own rule out of the page and copy the width from it,
    rather than hardcoding a number that is correct on one page today. If the
    anchor has no max-width of its own, the parent is doing the work and there
    is nothing to add.
    """
    if not anchor:
        return ""
    styles = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", s))
    for m in re.finditer(r"([^{}]*)\{([^}]*)\}", styles):
        sels = [x.strip() for x in m.group(1).split(",")]
        if "." + anchor not in sels:
            continue
        mw = re.search(r"max-width\s*:\s*([^;]+)", m.group(2))
        if mw:
            return ("\n/* same column as the paragraph above, read from that "
                    "paragraph's own rule */\n.clus{max-width:%s;margin-left:auto;"
                    "margin-right:auto}\n" % mw.group(1).strip())
    return ""


def main():
    arts = articles()
    if not arts:
        sys.exit("cluster_links: no articles found - run the article build first")

    index = {}
    for slug, title, dek, target in arts:
        index.setdefault(target, []).append((slug, title, dek))
    for t in index:
        index[t].sort()

    missing = [t for t in index if not os.path.exists(os.path.join(SITE, t))]
    if missing:
        sys.exit("cluster_links: articles point at pages that do not exist: %s"
                 % ", ".join(missing))

    changed = 0
    for target, items in sorted(index.items()):
        path = os.path.join(SITE, target)
        s = open(path, encoding="utf-8").read()
        # idempotent: drop any previous block and stylesheet, then re-derive, so
        # a newly written article shows up without a special case
        s = re.sub(re.escape(TAG) + r'<div class="clus">[\s\S]*?</div></div>', "", s)
        for end in (r"/\* end clus \*/", r"/\* end clusw \*/"):
            s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?" + end + r"</style>\n?",
                       "", s)
        at, anchor = insert_at(s)
        if at < 0:
            print("%-44s no </main>, skipped" % target)
            continue
        s = s[:at] + block(items) + s[at:]
        s = s.replace("</body>", "\n<style>" + MARK + width_rule(s, anchor)
                      + "/* end clusw */</style>\n</body>", 1)
        s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end clus */</style>\n</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s %d article(s): %s" % (target, len(items),
                                           ", ".join(i[0].replace(".html", "") for i in items)))
        changed += 1

    # ---- guards
    bad = 0
    for target, items in index.items():
        s = open(os.path.join(SITE, target), encoding="utf-8").read()
        if s.count(TAG) != 1:
            print("GUARD %s: %d blocks" % (target, s.count(TAG))); bad += 1
        if s.count(MARK) not in (1, 2):
            print("GUARD %s: %d stylesheets" % (target, s.count(MARK))); bad += 1
        for slug, _, _ in items:
            # the link must exist AND sit inside the block we just wrote
            blk = re.search(re.escape(TAG) + r"[\s\S]*?</div></div>", s)
            if not blk or ('href="%s"' % slug) not in blk.group(0):
                print("GUARD %s: %s not linked from the block" % (target, slug)); bad += 1
        if s.count("<h1") != 1:
            print("GUARD %s: %d h1" % (target, s.count("<h1"))); bad += 1
    # and the other direction must still hold: every article still points at a tool
    for slug, _, _, target in arts:
        s = open(os.path.join(SITE, slug), encoding="utf-8").read()
        if ('href="%s"' % target) not in s:
            print("GUARD %s: lost its handoff to %s" % (slug, target)); bad += 1
    if bad:
        sys.exit("cluster_links: %d guard failure(s)" % bad)
    print("%d calculator(s) linked back to %d article(s) · guards clean"
          % (changed, len(arts)))


if __name__ == "__main__":
    main()
