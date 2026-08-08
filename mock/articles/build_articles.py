#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The article system. One builder, N pages.

Step 2 of claude/content-hub-proposal.md, built against three REAL articles
rather than lorem - which is the whole point. A template proved on placeholder
text is a template that has never met a citation block, a long heading, or a
figure that has to trace back to a source.

THE CONTRACT. Every article declares, in `content.py`:

    slug, title, h1, kicker, dek, category, stage, minutes, updated
    figure   (value, caption)  the number that makes someone open it
    tool     the calculator it hands off to, and why
    sections [(heading, [blocks])]
    sources  [(n, cite, url, note)]

`sources` feeds the same numbered citation block the rest of the site uses.
`tool` generates the two-way link between an article and the calculator it
belongs to - block 04 in claude/content-block-system.md, specified long ago and
never built until now.

WHAT THE BUILD REFUSES TO SHIP:
  - an article with no sources
  - a `figure` that is not repeated somewhere in the body
  - a citation marker [n] in the prose with no matching source
  - a source that is never cited in the prose
  - a tool handoff pointing at a page that does not exist

That last set is the difference between a content system and a folder of HTML.

Chrome is lifted from the published resources.html at build time so the nav
cannot drift. Run the _dev order afterwards as usual.
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import ARTICLES

# Articles written since the first six live as one JSON file each in new/,
# rather than as more dicts in content.py.
#
# WHY THE SPLIT. content.py is now over a thousand lines of hand-typed prose in
# Python literal syntax, and every addition to it is a chance to break the
# module for every article at once - a stray quote in article nine takes down
# article one. A JSON file cannot do that: it either parses or it does not, and
# it fails alone. It is also what the research agents can write directly.
#
# The block shapes are the same in both. JSON gives arrays where content.py
# gives tuples, and the builder does not care, so the only conversion needed is
# for `figure` and `tool`, which are indexed positionally.
_NEW = os.path.join(HERE, "new")
if os.path.isdir(_NEW):
    for _f in sorted(os.listdir(_NEW)):
        if not _f.endswith(".json"):
            continue
        try:
            _a = json.load(open(os.path.join(_NEW, _f), encoding="utf-8"))
        except ValueError as _e:
            sys.exit("build_articles: new/%s is not valid JSON: %s" % (_f, _e))
        _a["figure"] = tuple(_a["figure"])
        _a["tool"] = tuple(_a["tool"])
        _a["sections"] = [(t, [tuple(b) for b in blocks])
                          for t, blocks in _a["sections"]]
        # content.py writes sources as 4-tuples (n, cite, url, note); JSON
        # writes them as objects, which is far easier to author and to check.
        # Unpacking a dict yields its keys, so without this the footnote number
        # arrives as the string "n" and the failure surfaces 200 lines away in
        # a %d format error.
        _a["sources"] = [(int(x["n"]), x["cite"], x.get("url"), x.get("note"))
                         if isinstance(x, dict) else tuple(x)
                         for x in _a["sources"]]
        if any(x["slug"] == _a["slug"] for x in ARTICLES):
            sys.exit("build_articles: new/%s duplicates an existing slug" % _f)
        ARTICLES.append(_a)

SITE = "https://therapistsupport.org"
SRC = os.path.join(HERE, "_chrome.html")
OUT = HERE

src = open(SRC, encoding="utf-8").read()


def balanced(s, tag):
    i = s.find("<" + tag)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


head_end = src.find("</head>")
links = [m.group(0) for m in re.finditer(r"<link\b[^>]*>", src[:head_end])
         if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
         or 'rel="preconnect"' in m.group(0)]
# EVERY <style> in the source, not just the ones in <head>. Several _dev passes
# append their stylesheet before </body> - breadcrumbs.py is one of them - so a
# head-only lift produced an article whose breadcrumb rendered as a default
# numbered list. Caught in a screenshot, not by any assert.
styles = re.findall(r"<style>.*?</style>", src, re.S)
assert styles, "no inline stylesheet in the chrome source"
# NOT asserting that .bcr came with the chrome. It did not, and an earlier
# assert for the substring ".bcr{" passed anyway - satisfied by touch_polish's
# `@media(max-width:520px){.bcr{font-size:10.2px}}`, a font tweak, not the
# layout rule. The breadcrumb rendered as a default numbered list and the build
# said it was fine. resources.html is not in breadcrumbs.py's TRAILS table, so
# it carries no crumb and no crumb stylesheet; lifting from it could never have
# worked. The article template now ships its own, which is the right dependency
# anyway - it generates its own crumb, so it should own the CSS for it.
assert styles, "no stylesheet lifted"

hs = balanced(src, "header")
header = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[hs[0]:hs[1]])
fs = balanced(src, "footer")
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[fs[0]:fs[1]])

CSS = """
<style>/* articles */
/* Self-contained breadcrumb. Deliberately not inherited from the chrome: the
   hub has no crumb of its own, so there was nothing to inherit. Same visual
   language as _dev/breadcrumbs.py, on a dark band. */
.artband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;
 margin:0 0 14px;padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:10.4px;letter-spacing:.1em;text-transform:uppercase;line-height:1.4}
.artband .bcr li{display:flex;align-items:center;gap:8px}
.artband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
 display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.artband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.artband .bcr .sep{opacity:.36;color:#EFF5F2}
.artband .bcr [aria-current]{opacity:.95;font-weight:600;color:#F6C560}
@media (pointer:coarse){.artband .bcr a{min-height:32px}}
.art{padding:0 0 10px}
.artband{background:linear-gradient(135deg,#141712,#1E241C 52%,#2C6350);color:#EFF5F2;
 padding:30px 0 34px}
.artband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
 grid-template-columns:minmax(0,1.35fr) minmax(240px,.65fr);gap:32px;align-items:center}
.artband .kick{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.4px;
 letter-spacing:.13em;text-transform:uppercase;color:#F6C560;margin:0 0 11px}
.artband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(26px,3.5vw,40px);
 line-height:1.07;font-weight:600;letter-spacing:-.022em;color:#fff;margin:0 0 13px;max-width:19ch}
.artband h1 em{font-style:normal;color:#F6C560}
.artband .dek{font-size:15.2px;line-height:1.72;color:rgba(255,255,255,.86);margin:0;max-width:56ch}
.artmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:16px;
 font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
 text-transform:uppercase;color:rgba(255,255,255,.62)}
.artfig{background:rgba(0,0,0,.24);border:1px solid rgba(255,255,255,.18);border-radius:16px;
 padding:20px 22px}
.artfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(30px,4vw,44px);
 line-height:1;color:#F6C560}
.artfig span{display:block;font-size:12.4px;line-height:1.55;color:rgba(255,255,255,.72);
 margin-top:9px}
.artwrap{max-width:1180px;margin:0 auto;padding:30px 26px 10px;display:grid;
 grid-template-columns:210px minmax(0,1fr);gap:38px;align-items:start}
.artnav{position:sticky;top:18px}
.artnav b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10.4px;
 letter-spacing:.12em;text-transform:uppercase;color:#8A8477;margin-bottom:10px}
.artnav a{display:block;font-size:12.8px;line-height:1.45;color:#5D574C;text-decoration:none;
 padding:7px 0 7px 11px;border-left:2px solid #E4DCC8}
.artnav a:hover{color:#2C6350}
.artnav a.on{color:#17271F;font-weight:600;border-left-color:#2C6350}
/* Grid children default to min-width:auto, so a wide child - here a table with
   nowrap figure cells - pushes the whole track past the viewport. Measured at
   390px: the .artwrap grid was 394px inside a 338px column. Both children need
   min-width:0 before max-width means anything. */
.artnav,.artbody{min-width:0}
.artbody{max-width:70ch}
.artbody h2{font-family:Fraunces,Georgia,serif;font-size:clamp(20px,2.3vw,26px);font-weight:600;
 letter-spacing:-.018em;margin:32px 0 12px;scroll-margin-top:22px}
.artbody h2:first-child{margin-top:0}
.artbody p{font-size:15.6px;line-height:1.78;color:#2A2620;margin:0 0 16px}
.artbody p b{font-weight:600}
.artbody ul{margin:0 0 16px;padding-left:20px}
.artbody li{font-size:15.2px;line-height:1.72;color:#2A2620;margin-bottom:8px}
.artbody sup a{color:#2C6350;font-weight:600;text-decoration:none;font-size:11px}
.pull{border-left:3px solid #F6C560;padding:4px 0 4px 18px;margin:22px 0}
.pull b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(24px,3vw,34px);
 line-height:1;color:#2C6350}
.pull span{display:block;font-size:13px;line-height:1.6;color:#5D574C;margin-top:8px;max-width:44ch}
.quote{background:#FFFDF6;border:1px solid #E4DCC8;border-left:3px solid #2C6350;
 border-radius:0 12px 12px 0;padding:16px 18px;margin:22px 0}
.quote p{font-size:14.4px;line-height:1.7;margin:0;color:#2A2620}
.quote cite{display:block;font-style:normal;font-family:'IBM Plex Mono',monospace;
 font-size:10.6px;letter-spacing:.06em;text-transform:uppercase;color:#8A8477;margin-top:9px}
/* A data table that will not fit a phone should scroll, not overflow. This is
   the same .tw wrapper the tax page uses, and nowrap-audit deliberately skips
   anything inside a real horizontal scroll container - a wide table behind a
   scroll bar is a design decision, an overflowing one is a bug. */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:20px 0;max-width:100%}
.tw .tbl{margin:0;min-width:420px}
.tbl{width:100%;border-collapse:collapse;margin:20px 0;background:#FFFDF6;
 border:1px solid #E4DCC8;border-radius:12px;overflow:hidden;font-size:14.2px}
.tbl th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.1em;
 text-transform:uppercase;color:#8A8477;padding:10px 13px;border-bottom:1px solid #E4DCC8}
.tbl td{padding:10px 13px;border-bottom:1px solid #E4DCC8;line-height:1.5}
.tbl tr:last-child td{border-bottom:0}
.tbl td.n{font-family:Fraunces,Georgia,serif;font-size:16px;color:#2C6350;white-space:nowrap}
.arttool{background:linear-gradient(135deg,#1E4436,#2C6350);color:#EFF5F2;border-radius:16px;
 padding:24px 26px;margin:30px 0 8px}
.arttool b{display:block;font-family:Fraunces,Georgia,serif;font-size:19px;color:#fff;
 margin-bottom:8px}
.arttool p{font-size:13.8px;line-height:1.68;color:rgba(255,255,255,.85);margin:0 0 15px;
 max-width:58ch}
.arttool a{display:inline-flex;align-items:center;min-height:46px;padding:0 20px;
 border-radius:11px;background:#F6C560;color:#2A2010;font-weight:800;font-size:14px;
 text-decoration:none}
.artsrc{margin:34px 0 0;padding-top:20px;border-top:1px solid #E4DCC8}
.artsrc h2{font-family:Fraunces,Georgia,serif;font-size:19px;margin:0 0 12px}
.artsrc ol{margin:0;padding-left:22px}
.artsrc li{font-size:13px;line-height:1.66;color:#5D574C;margin-bottom:10px}
.artsrc li a{color:#2C6350;font-weight:600}
.artsrc .disc{font-size:12.4px;line-height:1.65;color:#8A8477;margin:16px 0 0;max-width:66ch}
.artnext{border-top:1px solid #E4DCC8;margin-top:30px;padding-top:22px}
.artnext b{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.12em;
 text-transform:uppercase;color:#8A8477;display:block;margin-bottom:12px}
.artnext .g{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.artnext a{background:#FFFDF6;border:1px solid #E4DCC8;border-radius:12px;padding:15px 16px;
 text-decoration:none;display:block}
.artnext a:hover{border-color:#2C6350}
.artnext a i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9.6px;
 letter-spacing:.09em;text-transform:uppercase;color:#2C6350;font-weight:600}
.artnext a strong{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;
 font-weight:600;line-height:1.28;margin-top:5px;color:#17271F}
@media (max-width:900px){
  .artband .in{grid-template-columns:1fr}
  .artwrap{grid-template-columns:1fr;gap:18px;padding-top:22px}
  .artnav{position:static;display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
  .artnav b{display:none}
  .artnav a{border-left:0;border-bottom:2px solid #E4DCC8;white-space:nowrap;padding:7px 2px}
  .artnav a.on{border-bottom-color:#2C6350}
  .artnext .g{grid-template-columns:1fr}
}
</style>"""

JS = """<script>
/* Scroll-spy for the section rail. rootMargin is asymmetric on purpose: the
   highlighted entry should be the section being READ, not the one just
   entering the bottom of the screen. Same values as _dev/doc_rails.py. */
(function(){
  var links = [].slice.call(document.querySelectorAll('.artnav a'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var map = {};
  links.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
  var obs = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if (!e.isIntersecting) return;
      links.forEach(function(a){ a.classList.remove('on'); });
      var a = map[e.target.id]; if (a) a.classList.add('on');
    });
  }, { rootMargin: '-12% 0px -80% 0px' });
  /* Highlight the first section on load. Without this the rail is blank until
     the reader scrolls far enough for a heading to enter the observed band,
     which reads as broken rather than as "you are at the top". */
  links[0].classList.add('on');
  Object.keys(map).forEach(function(id){
    var el = document.getElementById(id); if (el) obs.observe(el);
  });
})();
</script>"""


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def render_block(b):
    k = b[0]
    if k == "p":
        return "<p>" + b[1] + "</p>"
    if k == "ul":
        return "<ul>" + "".join("<li>" + x + "</li>" for x in b[1]) + "</ul>"
    if k == "pull":
        return ('<div class="pull"><b>' + b[1] + "</b><span>" + b[2] + "</span></div>")
    if k == "quote":
        return ('<div class="quote"><p>' + b[1] + "</p><cite>" + b[2] + "</cite></div>")
    if k == "table":
        head, rows = b[1], b[2]
        return ('<div class="tw"><table class="tbl"><thead><tr>'
                + "".join("<th>" + h + "</th>" for h in head) + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join(
                    ('<td class="n">' if c.startswith("$") or c.startswith("&sect;")
                     else "<td>") + c + "</td>" for c in r) + "</tr>" for r in rows)
                + "</tbody></table></div>")
    raise ValueError("unknown block: " + k)


def library_meta(a):
    """Emit the ts:* block that puts this article into the content library.

    The library used to be driven by hand-added records in registry.json, which
    meant a new article did not exist to the hub, the topic pages or the
    question index until someone remembered to register it. Emitting the
    metadata here closes that loop: _dev/registry_sync.py reads these tags back
    out and rebuilds the registry from the pages, so writing the article IS
    registering it.

    An article with no `library` block still builds - it just will not appear in
    any listing, which is the correct failure. Silently guessing a topic and a
    question would put a page on a hub under a heading nobody wrote.
    """
    lib = a.get("library")
    if not lib:
        return ""
    out = ["<!-- ts:meta -->"]
    for key in ("topic", "format", "question", "outcome", "number"):
        v = lib.get(key)
        if v:
            out.append('<meta name="ts:%s" content="%s">' % (key, esc_attr(str(v))))
    out.append('<meta name="ts:weight" content="%d">' % int(lib.get("weight", 1)))
    for key in ("leaf", "stale", "skip"):
        if lib.get(key):
            out.append('<meta name="ts:%s" content="true">' % key)
    out.append("<!-- /ts:meta -->")
    return "\n".join(out) + "\n"


def esc_attr(x):
    return (x.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def build(a, others):
    body, nav = [], []
    for heading, blocks in a["sections"]:
        sid = slugify(heading)
        nav.append('<a href="#' + sid + '">' + heading + "</a>")
        body.append('<h2 id="' + sid + '">' + heading + "</h2>")
        body.extend(render_block(b) for b in blocks)

    tool_href, tool_title, tool_why = a["tool"]
    tool = ('<div class="arttool"><b>' + tool_title + "</b><p>" + tool_why + "</p>"
            '<a href="' + tool_href + '">Open the calculator &rarr;</a></div>')

    srcs = ('<div class="artsrc"><h2>Sources</h2><ol>'
            + "".join('<li id="s%d">%s%s</li>'
                      % (n, ('<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                             % (url, cite)) if url else "<b>" + cite + "</b>",
                         " &mdash; " + note if note else "")
                      for n, cite, url, note in a["sources"])
            + '</ol><p class="disc">Every figure here is either computed by the calculator '
              "linked above from numbers you enter, or quoted from the source named beside "
              "it. Nothing on this page is illustrative. This is not legal, tax or financial "
              "advice, and reading it does not create a professional relationship.</p></div>")

    nxt = ('<div class="artnext"><b>Read next</b><div class="g">'
           + "".join('<a href="%s.html"><i>%s</i><strong>%s</strong></a>'
                     % (o["slug"], o["category"], o["h1_plain"]) for o in others)
           + "</div></div>")

    crumb = ('<ol class="bcr" aria-label="Breadcrumb">'
             '<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>'
             '<li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li>'
             '<li><span aria-current="page">' + a["category"] + "</span></li></ol>")

    ld = [{"@context": "https://schema.org", "@type": "Article",
           "headline": a["h1_plain"], "description": a["dek_plain"],
           "url": SITE + "/" + a["slug"] + ".html",
           "dateModified": a["updated"], "isAccessibleForFree": True,
           "author": {"@type": "Organization", "name": "Therapist Support"},
           "about": a["category"]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Therapist Support", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Resources",
             "item": SITE + "/resources.html"},
            {"@type": "ListItem", "position": 3, "name": a["h1_plain"],
             "item": SITE + "/" + a["slug"] + ".html"}]}]

    html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<title>" + a["title"] + "</title>\n"
            '<meta name="description" content="' + a["dek_plain"] + '">\n'
            '<link rel="canonical" href="' + SITE + "/" + a["slug"] + '.html">\n'
            + library_meta(a)
            + '<meta name="robots" content="index, follow, max-image-preview:large">\n'
            '<meta property="og:type" content="article">\n'
            '<meta property="og:title" content="' + a["h1_plain"] + '">\n'
            '<meta property="og:description" content="' + a["dek_plain"] + '">\n'
            + "\n".join(links) + "\n" + "\n".join(styles) + "\n" + CSS + "\n"
            + "".join('<script type="application/ld+json">'
                      + json.dumps(d, separators=(",", ":")) + "</script>" for d in ld)
            + "\n</head>\n<body>\n" + header
            + '\n<article class="art"><section class="artband"><div class="in"><div>'
            + crumb
            + '<p class="kick">' + a["kicker"] + "</p><h1>" + a["h1"] + "</h1>"
            + '<p class="dek">' + a["dek"] + "</p>"
            + '<div class="artmeta"><span>' + a["category"] + "</span><span>"
            + str(a["minutes"]) + " min read</span><span>Updated " + a["updated"]
            + "</span></div></div>"
            + '<div class="artfig"><b>' + a["figure"][0] + "</b><span>"
            + a["figure"][1] + "</span></div></div></section>"
            + '<div class="artwrap"><nav class="artnav"><b>On this page</b>'
            + "".join(nav) + "</nav>"
            + '<div class="artbody">' + "".join(body) + tool + srcs + nxt
            + "</div></div></article>\n" + footer + "\n" + JS + "\n</body>\n</html>\n")
    return html


def main():
    pages = {a["slug"] + ".html" for a in ARTICLES}
    known = pages | {"index.html", "resources.html", "contact.html",
                     "practice-simulator.html", "therapist-tax-strategy-california.html",
                     "grow-your-therapy-practice.html", "amft-3000-hours-california.html",
                     "associate-mft-job-advisor.html", "rates.html",
                     "therapist-cost-of-living-california.html",
                     "therapist-working-remotely-california.html"}
    bad = 0
    for a in ARTICLES:
        others = [o for o in ARTICLES if o["slug"] != a["slug"]][:2]
        html = build(a, others)

        # ---- the guards. An article that fails these is not publishable.
        prose = " ".join(str(b) for _, blocks in a["sections"] for b in blocks)
        cited = {int(m) for m in re.findall(r"#s(\d+)", prose)}
        declared = {n for n, _, _, _ in a["sources"]}
        if not declared:
            print("GUARD %s: no sources" % a["slug"]); bad += 1
        for n in cited - declared:
            print("GUARD %s: prose cites [%d] with no such source" % (a["slug"], n)); bad += 1
        for n in declared - cited:
            print("GUARD %s: source [%d] declared but never cited" % (a["slug"], n)); bad += 1
        if a["figure"][0].replace("&sect;", "§") not in html.replace("&sect;", "§"):
            print("GUARD %s: headline figure never appears in the body" % a["slug"]); bad += 1
        if a["tool"][0] not in known:
            print("GUARD %s: tool handoff to unknown page %s" % (a["slug"], a["tool"][0]))
            bad += 1
        if html.count("<h1") != 1:
            print("GUARD %s: %d h1" % (a["slug"], html.count("<h1"))); bad += 1

        open(os.path.join(OUT, a["slug"] + ".html"), "w", encoding="utf-8").write(html)
        print("%-42s %6d bytes  %d sections  %d sources"
              % (a["slug"] + ".html", len(html.encode("utf-8")),
                 len(a["sections"]), len(a["sources"])))
    if bad:
        sys.exit("build_articles: %d guard failure(s)" % bad)
    missing = [a["slug"] for a in ARTICLES
               if a.get("library")
               and '<meta name="ts:question"' not in
               open(os.path.join(OUT, a["slug"] + ".html"), encoding="utf-8").read()]
    if missing:
        sys.exit("build_articles: library block declared but no ts:meta emitted: "
                 + ", ".join(missing))
    print("%d article(s) built, %d carrying library metadata"
          % (len(ARTICLES), sum(1 for a in ARTICLES if a.get("library"))))


if __name__ == "__main__":
    main()
