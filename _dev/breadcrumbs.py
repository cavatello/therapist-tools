#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A visible breadcrumb on every page, plus matching BreadcrumbList JSON-LD.

Why. `therapist-tax-strategy-california.html` opened with "CHAPTER 04 ·
CALIFORNIA · 2026 RATES" — a leftover from when the site was one page with
numbered chapters. Standing alone it implies a sequence the reader cannot see:
chapter of what, and where are one to three? On a page arrived at cold from a
forum link, nobody can answer that.

A breadcrumb is the same three-token shape, but navigable, and it answers the
question the chapter number was pretending to: where am I in this site. It also
does the orientation job the user asked for — someone landing from search must
know in one screen that this is Therapist Support and which part of it they are
in. And Google reads BreadcrumbList for rich results, which matters for a site
whose traffic is meant to arrive on deep pages.

Four pages already emitted BreadcrumbList JSON-LD. None of them showed the
trail, and none of the four went past a single "home" item, so the structured
data was claiming a hierarchy the markup did not have. Both are rewritten here
from one table, so they cannot disagree.

Placement. The crumb goes ABOVE the kicker, not between the kicker and the h1.
Every hero here is `<p class="kicker">` immediately followed by `<h1>`, so the
insertion point is the last <p> opening tag within ~300 characters before the
first <h1>. Where there is no kicker it falls back to the h1 itself.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
BASE = "https://cavatello.github.io/therapist-tools"
MARK = "/* _dev/breadcrumbs.py */"
TAG = "<!-- breadcrumb -->"

# page -> (section label, section href or None, page label)
# None for the section href means the section is a menu, not a page, so that
# crumb segment is plain text rather than a dead link.
TRAILS = {
    "practice-simulator.html":                  ("Tools", "tools.html", "Practice simulator"),
    "therapist-tax-strategy-california.html":   ("Tools", "tools.html", "Tax &amp; retirement"),
    "grow-your-therapy-practice.html":          ("Tools", "tools.html", "Grow your practice"),
    "associate-mft-job-advisor.html":           ("Tools", "tools.html", "Job advisor"),
    "amft-3000-hours-california.html":          ("Tools", "tools.html", "3,000 hours"),
    "therapist-cost-of-living-california.html": ("Tools", "tools.html", "Cost of living"),
    "rates.html":                               ("Learn", None, "The rate gap"),
    "therapist-working-remotely-california.html": ("Learn", None, "Working remotely"),
    "about.html":                               ("About", None, "What this is"),
    "contact.html":                             ("About", None, "Contact"),
    "newsletter.html":                          ("About", None, "Stay updated"),
    "terms.html":                               (None, None, "Terms of Use"),
    "privacy.html":                             (None, None, "Privacy"),
    "tools.html":                               (None, None, "All free tools"),
}

CSS = """
/* The breadcrumb. Replaces the "Chapter NN" kicker, which only meant something
   to a reader who could see the other chapters. Deliberately the same weight
   and tracking as the kicker it sits above, so it reads as chrome rather than
   as content. Colour is inherited so it works on paper and on a dark slab
   without a second rule. */
/* Measured 44-86px of dead air between the masthead and the crumb, because the
   hero's own padding-top was set before the crumb existed and the crumb then
   added to it. Pulled up rather than reaching into each page's hero padding,
   which differs per template. */
.bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;
  margin:clamp(-30px,-2.2vw,-14px) 0 10px;
 padding:0;list-style:none;font-family:'IBM Plex Mono',monospace;font-size:10.4px;
 letter-spacing:.1em;text-transform:uppercase;line-height:1.4}
.bcr li{display:flex;align-items:center;gap:8px}
.bcr a{color:inherit;opacity:.62;text-decoration:none;padding:5px 0;min-height:24px;
 display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.bcr a:hover{opacity:1;border-bottom-color:currentColor}
.bcr a:focus-visible{outline:2px solid currentColor;outline-offset:3px;border-radius:3px}
.bcr .sep{opacity:.36}
.bcr [aria-current]{opacity:.95;font-weight:600}
@media (max-width:520px){.bcr{font-size:9.8px;letter-spacing:.08em}}
"""


def trail_html(section, section_href, page):
    li = ['<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>']
    if section:
        seg = ('<a href="%s">%s</a>' % (section_href, section)) if section_href else (
            '<span>%s</span>' % section)
        li.append('<li>%s<span class="sep">&rsaquo;</span></li>' % seg)
    li.append('<li><span aria-current="page">%s</span></li>' % page)
    return (TAG + '<ol class="bcr" aria-label="Breadcrumb">' + "".join(li) + "</ol>")


def trail_ld(slug, section, section_href, page):
    items = [{"@type": "ListItem", "position": 1, "name": "Therapist Support",
              "item": BASE + "/"}]
    n = 2
    if section and section_href:
        items.append({"@type": "ListItem", "position": n, "name": section,
                      "item": BASE + "/" + section_href})
        n += 1
    items.append({"@type": "ListItem", "position": n,
                  "name": re.sub(r"&[a-z]+;", "&", page),
                  "item": BASE + "/" + slug})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}


BLOCKY = re.compile(r"</?(div|section|nav|ul|ol|header|main|article|aside)\b", re.I)


def insert_point(s):
    """Above the kicker, not between the kicker and the h1.

    The candidate must be a TRUE SIBLING kicker: the last <p> before the h1 with
    no block-level boundary between the two. Without that test, rates.html - whose
    h1 is preceded by a <span> eyebrow, not a <p> - matched a <p> hundreds of
    characters earlier inside the nav panel, and the crumb was injected into the
    navigation menu.
    """
    h1 = s.find("<h1")
    if h1 < 0:
        return None
    window = s[max(0, h1 - 300):h1]
    last = None
    for m in re.finditer(r"<p[ >]", window):
        last = m
    if last:
        between = window[last.start():]
        if not BLOCKY.search(between):
            return max(0, h1 - 300) + last.start()
    return h1


def main():
    changed = 0
    for slug, (section, href, page) in sorted(TRAILS.items()):
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            print("%-44s MISSING" % slug)
            continue
        s = open(path, encoding="utf-8").read()

        # idempotent: strip our previous crumb, style and JSON-LD
        s = re.sub(re.escape(TAG) + r'<ol class="bcr".*?</ol>', "", s, flags=re.S)
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end bcr \*/</style>\n?",
                   "", s, flags=re.S)
        s = re.sub(r'<script type="application/ld\+json" data-bcr>.*?</script>\s*',
                   "", s, flags=re.S)
        # and any earlier hand-written BreadcrumbList, which claimed a hierarchy
        # the markup never had. Several pages emit an ARRAY of schema objects
        # with the crumb as one member, so a regex over the whole <script> would
        # have deleted the WebApplication block with it. Parse, filter, re-emit.
        def _strip_bc(m):
            try:
                data = json.loads(m.group(1))
            except ValueError:
                return m.group(0)
            if isinstance(data, list):
                kept = [d for d in data if d.get("@type") != "BreadcrumbList"]
                if not kept:
                    return ""
                if len(kept) == len(data):
                    return m.group(0)
                return ('<script type="application/ld+json">'
                        + json.dumps(kept, separators=(",", ":")) + "</script>")
            if isinstance(data, dict) and data.get("@type") == "BreadcrumbList":
                return ""
            return m.group(0)

        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _strip_bc, s, flags=re.S)

        # the chapter kicker this replaces
        s = re.sub(r"Chapter\s+0?\d+\s*&middot;\s*", "", s)
        s = re.sub(r"Chapter\s+0?\d+\s*·\s*", "", s)

        i = insert_point(s)
        if i is None:
            print("%-44s no <h1>, skipped" % slug)
            continue
        s = s[:i] + trail_html(section, href, page) + s[i:]

        ld = ('<script type="application/ld+json" data-bcr>'
              + json.dumps(trail_ld(slug, section, href, page), separators=(",", ":"))
              + "</script>\n")
        s = s.replace("</head>", ld + "</head>", 1)
        s = s.replace("</body>", "\n<style>" + MARK + CSS + "/* end bcr */</style>\n</body>", 1)

        open(path, "w", encoding="utf-8").write(s)
        changed += 1

    # ---- guards
    for slug in TRAILS:
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        assert s.count('class="bcr"') == 1, "%s has %d crumbs" % (slug, s.count('class="bcr"'))
        assert s.count("BreadcrumbList") == 1, "%s has %d BreadcrumbList" % (
            slug, s.count("BreadcrumbList"))
        assert not re.search(r"Chapter\s+0?\d+\s*(&middot;|·)", s), "chapter kicker left in " + slug
        assert s.count("<h1") == 1, slug
    print("%d page(s) crumbed" % changed)


if __name__ == "__main__":
    main()
