#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put the Associate MFT Job Advisor into every navigation on the site.

There are three separate navigations and they are NOT one shared include:
  - the nav panel inside the masthead, present on each static page as its own
    copy of the same markup
  - the site footer's Tools column, on the pages that carry a footer
  - NAV_PANEL in app.js, which the simulator renders from data

Each is edited in place with an exactly-once assertion, and the script refuses
to touch a file that already has the entry, so it can be re-run safely.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "associate-mft-job-advisor.html"
TITLE = "Associate Job Advisor"
BLURB = "compare AMFT jobs, pay and your 3,000 hours"

PANEL_PAGES = ["tools.html", "about.html", "newsletter.html", "contact.html", "rates.html"]

changed = []

for name in PANEL_PAGES:
    path = os.path.join(ROOT, name)
    s = open(path).read()
    if SLUG in s:
        print("  %-18s already has it, skipped" % name)
        continue
    before = s

    # --- 1. the masthead nav panel -----------------------------------------
    # Anchor on the whole first <a> of the Tools column and append after it, so
    # the new entry inherits that column's icon and markup exactly. Matching on
    # '<h5>Tools</h5>' alone would also hit the footer, which has different
    # markup and no icons.
    m = re.search(r'(<div class="np-col"><h5>Tools</h5>)(<a href="tools\.html"[^>]*>.*?</a>)',
                  s, re.S)
    assert m, name + ": no Tools column in the nav panel"
    icon = re.search(r'<img src="(data:image/svg\+xml[^"]*)"', m.group(2))
    assert icon, name + ": the Tools column's first entry has no icon to copy"
    entry = ('<a href="' + SLUG + '"><img src="' + icon.group(1) + '" alt="" '
             'aria-hidden="true"><span><b>' + TITLE + '</b><i>' + BLURB + '</i></span></a>')
    s = s.replace(m.group(0), m.group(0) + entry, 1)

    # --- 2. the footer's Tools column, where there is one -------------------
    fm = re.search(r'(<div><h5>Tools</h5>)(<a href="tools\.html">[^<]*</a>)', s)
    if fm:
        s = s.replace(fm.group(0),
                      fm.group(0) + '<a href="' + SLUG + '">' + TITLE + '</a>', 1)

    assert s.count(SLUG) == (2 if fm else 1), name + ": wrong number of links inserted"
    assert len(s) > len(before)
    open(path, "w").write(s)
    changed.append(name)
    print("  %-18s nav panel%s" % (name, " + footer" if fm else ""))

# --- 3. app.js, which builds its nav from data ------------------------------
path = os.path.join(ROOT, "app.js")
s = open(path).read()
if SLUG in s:
    print("  %-18s already has it, skipped" % "app.js")
else:
    anchor = ('["piggy", "All free tools", "every calculator and widget, in one place", '
              '"tools.html"],')
    assert s.count(anchor) == 1, "app.js: NAV_PANEL Tools anchor not found exactly once"
    new = (anchor + '\n               ["calc", "' + TITLE + '", "' + BLURB + '", "'
           + SLUG + '"],')
    s = s.replace(anchor, new, 1)
    # the simulator's own footer carries the same inventory
    fanchor = '["tools.html", "All free tools"]'
    if s.count(fanchor) == 1:
        s = s.replace(fanchor, fanchor + ', ["' + SLUG + '", "' + TITLE + '"]', 1)
    open(path, "w").write(s)
    changed.append("app.js")
    print("  %-18s NAV_PANEL%s" % ("app.js", " + footer" if s.count(SLUG) == 2 else ""))

# --- 4. sitemap -------------------------------------------------------------
path = os.path.join(ROOT, "sitemap.xml")
s = open(path).read()
if SLUG in s:
    print("  %-18s already has it, skipped" % "sitemap.xml")
else:
    import datetime
    today = datetime.date.today().isoformat()
    m = re.search(r'<url>.*?</url>', s, re.S)
    assert m, "sitemap.xml: no <url> block to copy the shape from"
    entry = ('<url><loc>https://cavatello.github.io/therapist-tools/' + SLUG + '</loc>'
             '<lastmod>' + today + '</lastmod><changefreq>monthly</changefreq>'
             '<priority>0.9</priority></url>')
    s = s.replace("</urlset>", entry + "\n</urlset>", 1)
    open(path, "w").write(s)
    changed.append("sitemap.xml")
    print("  %-18s added, lastmod %s" % ("sitemap.xml", today))

print("\nchanged:", ", ".join(changed) if changed else "nothing")
