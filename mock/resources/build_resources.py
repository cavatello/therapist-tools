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

SITE = "https://cavatello.github.io/therapist-tools"
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
.ref i b{display:inline;font-size:inherit;margin:0;font-weight:600;color:#2A2620}
.band .ref{background:#fff;color:#2A2620}
.band .ref b{color:#17271F}
.band .ref i{color:#4E4940}
.band .ref i b{color:#17271F}
.ref i a{white-space:nowrap}
@media (max-width:700px){.reflist{grid-template-columns:1fr}}
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
A('<p class="kick">California &middot; every link checked 5 August 2026</p>')
A('<h1>The things you actually need, <em>and nothing else</em>.</h1>')
A('<p class="lede">Seventy-two links a California therapist in private practice genuinely '
  'uses &mdash; the Board, CE and supervision rules, insurance panels, telehealth law, '
  'malpractice and HIPAA, entity and tax, and the client directories with what they '
  '<b>actually cost</b>. Each one was opened and read, and no price or deadline appears '
  'here unless it was on the page it describes.</p>')
A('</div><div>')
A('<div class="ref"><span><b>Why the dates matter</b><i>Two things on this page moved '
  'recently and are still moving. BBS fees <b>halved on 1 July 2026</b> and revert in 2030. '
  'One large insurance panel is <b>closed to new applicants</b> until September. Where '
  'something is in flux the entry says so, because a confidently wrong link costs you a '
  'week.</i></span></div>')
A("</div></div></section>")

for i, (name, tag, sub, items) in enumerate(GROUPS):
    A('<section class="sec%s"><div class="pw">' % ("" if i % 2 == 0 else " alt"))
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
assert out.count('class="ref"') == n_items + 1, (
    "card count %d does not match content %d" % (out.count('class="ref"'), n_items + 1))
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
