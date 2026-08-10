#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A share card on every page, not on thirty-two of them.

WHAT THE AUDIT FOUND

Thirty-two pages carry a full Open Graph block. **A hundred and fifty-three do
not.** Those hundred and fifty-three include every discipline case page, every
school page, every psychedelic-training page, and the LA/Bay Area associate pay
page - which is to say, the newest and most shareable work on the site.

Why that matters more here than on most sites: this audience shares links to
each other in Facebook groups and Slack channels. The associate-pay page exists
*because* somebody posted a question in a California AMFT Facebook group. A link
pasted there with no Open Graph renders as a bare grey URL with no title, no
description and no image, next to other links that render as cards. The page
does not get read.

WHAT THIS DOES, AND WHAT IT DELIBERATELY DOES NOT

Adds a derived card to pages that have none: `og:title` from the page's
`<title>`, `og:description` from its meta description, `og:url` from its
canonical, plus `og:type`, `og:site_name`, the site's existing 1200x630 image,
and a `summary_large_image` Twitter card.

**It leaves the thirty-two existing blocks completely alone**, and that is a
judgement rather than caution. Those were authored, and they are better than
anything derivable: `about.html` has a 23-character `<title>` and a
74-character `og:title`, and on most of the thirty-two the og description is
written separately from the meta description. A title is written to fit a
68-character search result; a share card has more room and a different job.
Overwriting hand-written copy with a mechanical derivation would be a
regression dressed as consistency.

So: a derived card is a **floor**. Any page can be improved by writing a real
one, and this pass will then step out of the way, because it only ever touches
pages with no `og:title` at all.

ALSO HANDLED HERE

`tycoon.html` is a visual-direction mockup - static, illustrative, not wired to
anything, two `<h1>`s, no canonical, no structured data - and it is indexable.
It gets `noindex, follow` and no share card. `concepts.html` is the same kind of
page and was already noindex; this brings the pair into line.

Idempotent - it recognises its own block and rewrites it. Guarded on the
invariant that matters: exactly one `og:title` per page.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "<!-- _dev/social_cards.py -->"
END = "<!-- /social_cards -->"

BASE = "https://therapistsupport.org/"
IMAGE = BASE + "og-image.png"
SITE_NAME = "Therapist Support"

# Mockups and prototypes. Real pages for a reader who is sent one; not pages a
# search engine should offer to anybody.
NOINDEX = ("tycoon.html", "concepts.html")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def attr(s, pat):
    m = re.search(pat, s, re.I | re.S)
    return m.group(1).strip() if m else None


def esc(x):
    """Escaped for an attribute. The source is already HTML-escaped text, so
    it is unescaped first - otherwise `&amp;` in a title becomes `&amp;amp;`
    in the card, which is what a share preview would then display."""
    return (html.unescape(x).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def card(title, desc, url, kind):
    o = [MARK,
         '<meta property="og:type" content="%s" />' % kind,
         '<meta property="og:site_name" content="%s" />' % SITE_NAME,
         '<meta property="og:title" content="%s" />' % esc(title)]
    if desc:
        o.append('<meta property="og:description" content="%s" />' % esc(desc))
    if url:
        o.append('<meta property="og:url" content="%s" />' % url)
    o += ['<meta property="og:image" content="%s" />' % IMAGE,
          '<meta property="og:image:width" content="1200" />',
          '<meta property="og:image:height" content="630" />',
          '<meta name="twitter:card" content="summary_large_image" />',
          END]
    return "\n".join(o)


def main():
    if not os.path.exists(os.path.join(SITE, "og-image.png")):
        sys.exit("social_cards: og-image.png is missing, so every card this "
                 "pass writes would point at a 404")

    added = kept = hidden = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        # our own block comes out first, so a re-run replaces rather than stacks
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)

        base = os.path.basename(rel)
        if base in NOINDEX:
            if not re.search(r'name="robots"', s, re.I):
                i = s.lower().find("</head>")
                if i > 0:
                    s = (s[:i] + '<meta name="robots" content="noindex, follow">\n'
                         + s[i:])
                    hidden += 1
            if s != orig:
                open(p, "w", encoding="utf-8").write(s)
            continue

        if re.search(r'property="og:title"', s, re.I):
            kept += 1
            if s != orig:
                open(p, "w", encoding="utf-8").write(s)
            continue

        title = attr(s, r"<title>([\s\S]*?)</title>")
        desc = attr(s, r'<meta name="description" content="([^"]*)"')
        url = attr(s, r'<link rel="canonical" href="([^"]*)"')
        if not title:
            print("  SKIP  %s has no <title> to derive a card from" % rel)
            continue
        kind = "website" if base in ("index.html",) else "article"

        i = s.lower().find("</head>")
        if i < 0:
            print("  SKIP  %s has no </head>" % rel)
            continue
        s = s[:i] + card(title, desc, url, kind) + "\n" + s[i:]
        open(p, "w", encoding="utf-8").write(s)
        added += 1

    print("share cards: %d derived, %d authored block(s) left alone, "
          "%d mockup(s) set to noindex" % (added, kept, hidden))

    # --------------------------------------------------------------- guards
    bad = 0
    checked = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        base = os.path.basename(rel)
        if base in NOINDEX:
            if not re.search(r'name="robots"[^>]*noindex', s, re.I):
                print("GUARD %s: a mockup that is still indexable" % rel)
                bad += 1
            continue
        checked += 1
        n = len(re.findall(r'property="og:title"', s, re.I))
        if n != 1:
            print("GUARD %s: %d og:title. Two cards means the network picks "
                  "one at random." % (rel, n))
            bad += 1
        if s.count(MARK) > 1:
            print("GUARD %s: %d of this pass's blocks" % (rel, s.count(MARK)))
            bad += 1
        # A card whose url disagrees with the canonical splits the share count
        # and tells the network the page is somewhere it is not.
        og = attr(s, r'property="og:url" content="([^"]*)"')
        canon = attr(s, r'<link rel="canonical" href="([^"]*)"')
        if og and canon and og != canon:
            print("GUARD %s: og:url %r disagrees with the canonical %r"
                  % (rel, og, canon))
            bad += 1
        if not re.search(r'name="twitter:card"', s, re.I):
            print("GUARD %s: no twitter:card, so the preview is a small "
                  "thumbnail rather than a card" % rel)
            bad += 1
        # Nothing may be double-escaped. `&amp;amp;` renders literally in a
        # share preview and is the classic tell that a pass escaped twice.
        if "&amp;amp;" in s or "&amp;mdash;" in s:
            print("GUARD %s: double-escaped entity in the head" % rel)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d indexable page(s), one share card each, every "
          "og:url agreeing with its canonical" % checked)


if __name__ == "__main__":
    main()
