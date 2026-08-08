#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resources.html — the curated external links page.

tools.html has advertised this page for a while as three "Coming soon" cards
(fee schedules, licensing and supervision, key dates). This is that page.

Construction follows build_grow.py and build_tax.py: chrome lifted verbatim
from a published page at build time so it cannot drift from the rest of the
site. The one difference is that those builders read cached chrome from
mock/amft/_chrome_*.txt, and this one lifts straight from the live tools.html
instead, because device staging was unavailable when it was written and the
caches could not be pulled. The caches were themselves cut from a published
page, so this is the same source, one step fresher. If you rebuild this later
with the caches available, prefer them for consistency with the other builders.

CONTENT RULE, and it is the whole point of the page: every entry in content.py
was fetched and read on 5 August 2026. No price, hour count or deadline appears
here unless it was read off the page it describes. Where a figure could not be
verified, the entry omits it rather than repeating a number from a review site.

NO TOP-NAV ENTRY YET. Every item in the lifted nav carries its own inline
pixel-art icon (see claude/pixel-art-system.md) and this page has no icon drawn
for it. Rather than reuse another page's art and make the menu lie, the page
ships linked from the footer and from tools.html, and the nav entry waits for
its own icon. All class="on" markers are stripped so no page falsely claims to
be the current one.
"""
import os, re, json, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import GROUPS
from questions import QUESTIONS, STAGES

SITE = "https://therapistsupport.org"
SLUG = "resources.html"
SOURCE = os.environ.get("CHROME_SOURCE", os.path.join(HERE, "_tools.html"))

TITLE = ("Resources for California Therapists — the Board, panels, insurance and tax, "
         "with every link checked")
DESC = ("A checked list of what a California therapist in private practice actually needs: "
        "BBS licence and CE rules, insurance panel applications, telehealth law, malpractice "
        "and HIPAA, entity and tax, and client directories with real prices. Every link "
        "verified August 2026.")

src = open(SOURCE, encoding="utf-8").read()


def span(s, tag, start=None):
    """Byte span of the first balanced <tag>...</tag>."""
    i = s.find("<" + tag) if start is None else s.find("<" + tag, start)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


# ------------------------------------------------------------------ chrome ---
head_end = src.find("</head>")
assert head_end > 0, "no </head> in the chrome source"
head = src[src.find("<head") : head_end]

# keep the stylesheet and font links; drop the source page's own metadata,
# which is about tools.html and would otherwise describe this page wrongly.
keep = []
for m in re.finditer(r"<link\b[^>]*>", head):
    if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0) or 'rel="preconnect"' in m.group(0):
        keep.append(m.group(0))
styles = re.findall(r"<style>.*?</style>", head, re.S)
assert styles, "no inline stylesheet found in the chrome source"

hs = span(src, "header")
assert hs, "no <header> in the chrome source"
header = src[hs[0]:hs[1]]
# Lifted onto another page, tools.html's class="on" is a lie on every entry.
header = re.sub(r'(<a href="[^"]*") class="on"', r"\1", header)
assert 'class="on"' not in header

fs = span(src, "footer")
assert fs, "no <footer> in the chrome source"
footer = src[fs[0]:fs[1]]
# The footer carries the same lie: tools.html is marked current there too.
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", footer)
# add ourselves to the footer's Learn column, which is plain text links
_learn = re.search(r"(<h5>Learn</h5>)", footer)
assert _learn, "no Learn column in the lifted footer"
footer = footer.replace(_learn.group(1),
    _learn.group(1) + '<a href="%s">Resources</a>' % SLUG, 1)

# ------------------------------------------------------------------- body ---
# Page-scoped stylesheet. Two things went wrong reusing the .ref component and
# both were caught by looking at a screenshot, not by any audit:
#
#   1. `.ref b{display:block}` styles the card TITLE. Every <b> inside a
#      description therefore broke onto its own line, so "halved on 1 July 2026"
#      and "and there is no grace period" rendered as orphaned fragments and the
#      cards read as broken sentences. Scoped back to inline inside the <i>.
#   2. The hero note sits inside .band, which sets a light text colour for a
#      dark background. .ref paints itself white but sets no colour on its own
#      <b>, so the title inherited near-white ON white and was invisible.
#      This is the same bare-descendant-selector trap as the cost-of-living bug
#      (claude/cola-hero-overflow.md); a component lifted onto a new surface
#      inherits whatever that surface says.
#
# Appended after the lifted sheet so it wins on source order at equal
# specificity - the convention the rest of this codebase already documents.
PAGE_CSS = """
<style>/* resources.html */
/* ---- the question index (direction C), the first section on the page.
   Nobody arrives at this site browsing; they arrive with a question. So the
   index is what a therapist types, and a calculator is a legitimate answer to
   one - which is why a tool row is washed gold and says so. */
.qx{border-top:1px solid var(--line)}
.qx a{display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;
 padding:15px 2px;text-decoration:none;border-bottom:1px solid var(--line)}
.qx a:hover h3{color:var(--pine)}
.qx h3{font-size:16.6px;line-height:1.32;font-weight:600;margin:0;letter-spacing:0}
.qx .tag{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.2px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--pine);font-weight:600}
.qx .m{display:flex;gap:10px;align-items:center;margin-top:4px;flex-wrap:wrap}
.qx .g{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.06em;
 text-transform:uppercase;color:#8A8477}
.qx .ar{font-size:18px;color:var(--pine)}
.qx a.qtool{background:linear-gradient(90deg,rgba(246,197,96,.17),transparent 60%);
 margin:0 -11px;padding-left:13px;padding-right:13px}
.qxnote{background:var(--white);border:1px solid var(--line);border-left:3px solid var(--pine);
 border-radius:0 12px 12px 0;padding:15px 17px;margin:22px 0 0;font-size:13px;
 line-height:1.65;color:var(--muted)}
/* ---- career-stage rails (direction A). Three per rail, never more: the cap is
   the point, not a limitation. */
.rail{margin-top:34px}
.railh{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
 flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:15px}
.railh h3{font-family:Fraunces,Georgia,serif;font-size:clamp(18px,2.1vw,23px);margin:0;
 font-weight:600;letter-spacing:-.018em}
.railh span{font-family:'IBM Plex Mono',monospace;font-size:10.2px;letter-spacing:.1em;
 text-transform:uppercase;color:#8A8477}
.railg{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}
.rc{background:var(--white);border:1px solid var(--line);border-radius:13px;padding:16px 17px;
 text-decoration:none;display:flex;flex-direction:column;gap:7px}
.rc:hover{border-color:var(--pine)}
.rc b{font-family:Fraunces,Georgia,serif;font-size:16px;line-height:1.26;font-weight:600}
.rc i{font-style:normal;font-size:12.9px;line-height:1.6;color:var(--muted)}
.rc .k{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--pine);font-weight:600;margin-top:auto;padding-top:5px}
.rc.tool{background:linear-gradient(160deg,rgba(246,197,96,.15),var(--white) 62%)}
/* ---- newsletter */
.hubnl{background:linear-gradient(135deg,#1E4436,#2C6350);color:#EFF5F2;border-radius:16px;
 padding:26px 28px;margin:34px 0 6px;display:grid;grid-template-columns:1.25fr .75fr;
 gap:22px;align-items:center}
.hubnl h3{font-family:Fraunces,Georgia,serif;font-size:clamp(18px,2.2vw,23px);margin:0;color:#fff}
.hubnl p{margin:8px 0 0;font-size:13.4px;line-height:1.62;color:rgba(255,255,255,.84)}
.hubnl a{display:inline-flex;align-items:center;min-height:46px;padding:0 20px;
 border-radius:10px;background:var(--pop);color:#2A2010;font-weight:800;font-size:14px;
 text-decoration:none}
@media(max-width:760px){.railg{grid-template-columns:1fr}.hubnl{grid-template-columns:1fr}}
.ref i b{display:inline;font-size:inherit;margin:0;font-weight:600;color:#2A2620}
.band .ref{background:#fff;color:#2A2620}
.band .ref b{color:#17271F}
.band .ref i{color:#4E4940}
.band .ref i b{color:#17271F}
.ref i a{white-space:nowrap}
@media (max-width:700px){.reflist{grid-template-columns:1fr}}
/* ---- very large displays. On a 27" 5K the hub used 46% of the window: a
   1120px container in a 2560px viewport, which is a lot of empty cream. The
   prose measure still has to be protected, so the CONTAINER grows and the
   reference grid gains a third column rather than the text lines getting
   longer. Below 1800px nothing changes. */
@media (min-width:1800px){
  .pw{max-width:1460px}
  .reflist{grid-template-columns:repeat(3,1fr)}
  .qx h3{max-width:78ch}
  .sub{max-width:88ch}
}
</style>"""
def esc_attr(u):
    return u.replace("&", "&amp;")


def card(title, url, desc):
    return ('<div class="ref"><span><b>' + title + "</b><i>" + desc
            + ' <a href="' + esc_attr(url) + '" target="_blank" '
              'rel="noopener noreferrer">Open &rarr;</a></i></span></div>')


B = []
A = B.append

A('<section class="band"><div class="pw"><div>')
A('<p class="kick">California &middot; free, no account, nothing saved</p>')
A('<h1>Free tools for California therapists, <em>and the rules behind them</em>.</h1>')
A('<p class="lede">Five calculators that run on <b>your own numbers</b> &mdash; take-home, '
  'tax, caseload, a job offer, the cost of living &mdash; plus the Board rules, panel '
  'requirements and reference links behind them. Every figure is computed or cited, and '
  'nothing here is saved or sent anywhere.</p>')
A('</div><div>')
A('<div class="ref"><span><b>Why the dates matter</b><i>Two things on this page moved '
  'recently and are still moving. BBS fees <b>halved on 1 July 2026</b> and revert in 2030. '
  'One large insurance panel is <b>closed to new applicants</b> until September. Where '
  'something is in flux the entry says so, because a confidently wrong link costs you a '
  'week.</i></span></div>')
A("</div></div></section>")

# ---- the question index (direction C), first because nobody arrives browsing
A('<section class="sec"><div class="pw">')
A('<div class="grouplab"><h2>Start with the question you came with</h2>'
  '<span>14 of them</span></div>')
A('<p class="sub">Indexed by what therapists actually type. A shaded row hands you a '
  'calculator that runs on your own numbers; a plain row is something to read or a '
  'section of the reference list below.</p>')
A('<div class="qx">' + "".join(
    '<a class="q' + kind + '" href="' + dest + '"><div><h3>' + q + '</h3>'
    '<div class="m"><span class="tag">' + cat + '</span>'
    '<span class="g">' + ("Tool &middot; " if kind == "tool"
                          else "Reference &middot; " if kind == "ref" else "Read &middot; ")
    + lab + '</span></div></div><span class="ar">&rarr;</span></a>'
    for q, cat, dest, lab, kind in QUESTIONS) + '</div>')
A('<div class="qxnote"><b>Why some rows are gold.</b> A shaded row does the arithmetic '
  'for you from numbers you type in. You should never have to guess whether a link is '
  'going to answer the question or just discuss it.</div>')
A("</div></section>")

# ---- Field Notes. It came OUT of the top nav on purpose - a nav is a set of
# choices and Hick's law bites on those, whereas a long-form document is
# something you arrive at, not something you navigate to. Removing it without
# giving it a home would have buried the best writing on the site, so it gets
# a section of its own here, with the figure that makes someone open it.
A('<section class="sec"><div class="pw">')
A('<div class="grouplab"><h2>Field Notes</h2><span>The long reads</span></div>')
A('<p class="sub">Two research documents rather than blog posts: each names its sources, '
  'admits its sample size, and shows the arithmetic behind the headline number.</p>')
A('<div class="reflist">'
  '<div class="ref"><span><b>The California therapy rate gap</b><i>What therapists are '
  'actually paid &mdash; insurance reimbursement against private pay, by metro, with the '
  'sample sizes admitted rather than hidden. The gap is widest exactly where the rent is '
  'highest. <a href="rates.html">Read Field Notes &rarr;</a></i></span></div>'
  '<div class="ref"><span><b>Working remotely as a California therapist</b><i>What the '
  'Board actually allows, what it costs you in tax, and what changes if you leave the '
  'state. Licensure follows your client&rsquo;s location, not yours. '
  '<a href="therapist-working-remotely-california.html">Read the document &rarr;</a>'
  '</i></span></div></div>')
A("</div></section>")

# ---- career-stage rails (direction A), capped at three each
A('<section class="sec alt"><div class="pw">')
A('<div class="grouplab"><h2>Where you are right now</h2><span>Three each, on purpose</span></div>')
A('<p class="sub">An associate and someone eight years into a practice need different '
  'pages, and the commonest way to lose a reader is to hand them the right answer to '
  'somebody else&rsquo;s question.</p>')
for stage, sub, items in STAGES:
    A('<div class="rail"><div class="railh"><h3>' + stage + '</h3><span>' + sub + '</span></div>')
    A('<div class="railg">' + "".join(
        '<a class="rc' + (" tool" if k == "tool" else "") + '" href="' + href + '">'
        '<b>' + title + '</b><i>' + blurb + '</i><span class="k">'
        + ("Calculator" if k == "tool" else "Reference" if k == "ref" else "Read")
        + '</span></a>' for href, title, blurb, k in items) + '</div></div>')
A('<div class="hubnl"><div><h3>One email a month. What changed in the numbers.</h3>'
  '<p>When the Board moves a fee, when the IRS publishes next year&rsquo;s limits, when a '
  'panel closes to new applicants. Nothing else, and one click to leave.</p></div>'
  '<div><a href="newsletter.html">Stay updated &rarr;</a></div></div>')
A("</div></section>")

# ---- the reference index
A('<section class="sec"><div class="pw">')
A('<div class="grouplab"><h2>The reference list</h2><span>72 links, all checked</span></div>')
A('<p class="sub">Everything a California therapist in private practice actually needs to '
  'reach: the Board, CE and supervision, insurance panels, telehealth law, malpractice and '
  'HIPAA, entity and tax, and the client directories with what they cost. No price or '
  'deadline appears unless it was on the page it describes.</p>')
A('<p class="sub" style="margin-top:-8px"><b>Not here yet, and worth saying so:</b> '
  'Medi-Cal and Medicare fee schedules by billing code, and a calendar of the dates that '
  'actually bite &mdash; quarterly estimated tax, renewal months, and when California '
  'publishes next year&rsquo;s figures. Both were promised on the old tools page as '
  '&ldquo;coming soon&rdquo;; neither is written, so neither is linked.</p>')
A("</div></section>")

for i, (name, tag, sub, items) in enumerate(GROUPS):
    gid = "g-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    A('<section class="sec%s" id="%s"><div class="pw">'
      % (" alt" if i % 2 == 0 else "", gid))
    A('<div class="grouplab"><h2>' + name + "</h2><span>" + tag + "</span></div>")
    A('<p class="sub">' + sub + "</p>")
    A('<div class="reflist">' + "".join(card(*it) for it in items) + "</div>")
    A("</div></section>")

A('<section class="sec"><div class="pw">')
A('<p class="sub" style="max-width:70ch">Nothing here is advice, and no link is an '
  'endorsement &mdash; several are competitors of each other and the prices are given so '
  'you can compare them yourself. If one of these has moved or gone wrong, '
  '<a href="contact.html">tell us</a> and it will be fixed.</p>')
A("</div></section>")

# ------------------------------------------------------------- structured ---
LD = [
 {"@context": "https://schema.org", "@type": "CollectionPage",
  "name": "Resources for California Therapists", "url": SITE + "/" + SLUG,
  "description": DESC,
  "audience": {"@type": "Audience",
               "audienceType": "Therapists in private practice in California"},
  "isAccessibleForFree": True},
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Therapist Support", "item": SITE + "/"},
   {"@type": "ListItem", "position": 2, "name": "Resources",
    "item": SITE + "/" + SLUG}]},
]

out = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
       '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
       "<title>" + TITLE + "</title>\n"
       '<meta name="description" content="' + DESC + '">\n'
       '<link rel="canonical" href="' + SITE + "/" + SLUG + '">\n'
       '<meta name="robots" content="index, follow, max-image-preview:large">\n'
       '<meta property="og:type" content="website">\n'
       '<meta property="og:title" content="' + TITLE + '">\n'
       '<meta property="og:description" content="' + DESC + '">\n'
       '<meta property="og:url" content="' + SITE + "/" + SLUG + '">\n'
       + "\n".join(keep) + "\n" + "\n".join(styles) + "\n"
       + "".join('<script type="application/ld+json">'
                 + json.dumps(d, separators=(",", ":")) + "</script>" for d in LD)
       + PAGE_CSS
       + "\n</head>\n<body>\n" + header + "\n" + "\n".join(B) + "\n" + footer
       + "\n</body>\n</html>\n")

# ------------------------------------------------------------------ guards ---
n_items = sum(len(g[3]) for g in GROUPS)
# The .ref component is used three places: once per reference link, once for the
# hero's "why the dates matter" note, and twice for the Field Notes documents.
# Keep this arithmetic explicit - it has already caught two mistakes, a class
# name collision and this one.
HERO_NOTES, FIELD_NOTES = 1, 2
expect = n_items + HERO_NOTES + FIELD_NOTES
assert out.count('class="ref"') == expect, (
    "card count %d does not match content %d" % (out.count('class="ref"'), expect))
assert out.count("<h1") == 1, "expected exactly one h1"
assert 'class="on"' not in out, "a lifted nav marker survived"
assert out.count('href="%s"' % SLUG) >= 1, "the footer link to self is missing"
# every href must be absolute-external or a real sibling page
bad = [u for u in re.findall(r'href="([^"#]+)"', out)
       if not u.startswith(("http://", "https://", "mailto:"))
       and not u.endswith((".html", ".png", ".svg", ".xml", ".ico", ".css", ".js", "/"))]
assert not bad, "suspicious relative links: %r" % bad[:5]

dest = os.path.join(HERE, SLUG)
open(dest, "w", encoding="utf-8").write(out)
print("%s  %d bytes  %d cards in %d groups"
      % (SLUG, len(out.encode("utf-8")), n_items, len(GROUPS)))
