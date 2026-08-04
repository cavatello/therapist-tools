#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repoint every "Grow Your Practice" link at the new standalone page.

Step 2 of claude/site-architecture-and-seo.md moves the tax chapter out of the
simulator. The nav must follow it, and it must REPLACE rather than duplicate:
two entries both called "Grow Your Practice", one an anchor and one a page, is
worse than either alone.

The anchor `index.html#grow` still resolves - the chapter has not been removed
from the home page yet, that is step 4 - so nothing breaks in the meantime.

Idempotent: a file that already points at the new page is skipped.
"""
import os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "grow-your-therapy-practice.html"
BLURB_OLD = "funnels, associates, lead targets"
BLURB_NEW = "what a client is worth, and where they come from"

PAGES = ["tools.html", "about.html", "newsletter.html", "contact.html", "rates.html"]
changed = []

for name in PAGES:
    path = os.path.join(ROOT, name)
    s = open(path).read()
    if SLUG in s:
        print("  %-18s already points at the new page" % name)
        continue
    before = s
    # the masthead nav panel entry, icon and all
    n_panel = len(re.findall(r'<a href="index\.html#grow">', s))
    s = s.replace('<a href="index.html#grow">', '<a href="' + SLUG + '">')
    s = s.replace(BLURB_OLD, BLURB_NEW)
    assert n_panel >= 1, name + ": no #grow link found"
    assert s != before
    open(path, "w").write(s)
    changed.append(name)
    print("  %-18s %d link(s) repointed" % (name, n_panel))

# --- app.js: NAV_PANEL data, the footer inventory, and any in-page link -------
path = os.path.join(ROOT, "app.js")
s = open(path).read()
if SLUG in s:
    print("  %-18s already points at the new page" % "app.js")
else:
    a = '["chart_up", "Grow Your Practice", "funnels, associates, lead targets", "#grow"]'
    assert s.count(a) == 1, "app.js: NAV_PANEL tax entry not found exactly once"
    s = s.replace(a, '["chart_up", "Grow Your Practice", "' + BLURB_NEW + '", "' + SLUG + '"]', 1)
    f = '["#grow", "Grow Your Practice"]'
    if s.count(f) == 1:
        s = s.replace(f, '["' + SLUG + '", "Grow Your Practice"]', 1)
    open(path, "w").write(s)
    changed.append("app.js")
    print("  %-18s NAV_PANEL + footer" % "app.js")

# --- sitemap: next to the simulator it came out of ---------------------------
path = os.path.join(ROOT, "sitemap.xml")
s = open(path).read()
if SLUG in s:
    print("  %-18s already listed" % "sitemap.xml")
else:
    tools = ('  <url>\n    <loc>https://cavatello.github.io/therapist-tools/tools.html</loc>\n'
             '    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n')
    assert s.count(tools) == 1
    entry = ('  <url>\n    <loc>https://cavatello.github.io/therapist-tools/' + SLUG + '</loc>\n'
             '    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n')
    s = s.replace(tools, tools + entry, 1)
    open(path, "w").write(s)
    changed.append("sitemap.xml")
    print("  %-18s added" % "sitemap.xml")

print("\nchanged:", ", ".join(changed) if changed else "nothing")
