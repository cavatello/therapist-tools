#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repoint every "Tax & Retirement" link at the new standalone page.

Step 2 of claude/site-architecture-and-seo.md moves the tax chapter out of the
simulator. The nav must follow it, and it must REPLACE rather than duplicate:
two entries both called "Tax & Retirement", one an anchor and one a page, is
worse than either alone.

The anchor `index.html#tax` still resolves - the chapter has not been removed
from the home page yet, that is step 4 - so nothing breaks in the meantime.

Idempotent: a file that already points at the new page is skipped.
"""
import os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "therapist-tax-strategy-california.html"
BLURB_OLD = "sole prop vs professional corp, priced"
BLURB_NEW = "how much of your tax bill is optional"

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
    n_panel = len(re.findall(r'<a href="index\.html#tax">', s))
    s = s.replace('<a href="index.html#tax">', '<a href="' + SLUG + '">')
    s = s.replace(BLURB_OLD, BLURB_NEW)
    assert n_panel >= 1, name + ": no #tax link found"
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
    a = '["calc", "Tax & Retirement", "sole prop vs professional corp, priced", "#tax"]'
    assert s.count(a) == 1, "app.js: NAV_PANEL tax entry not found exactly once"
    s = s.replace(a, '["calc", "Tax & Retirement", "' + BLURB_NEW + '", "' + SLUG + '"]', 1)
    f = '["#tax", "Tax & Retirement"]'
    if s.count(f) == 1:
        s = s.replace(f, '["' + SLUG + '", "Tax & Retirement"]', 1)
    open(path, "w").write(s)
    changed.append("app.js")
    print("  %-18s NAV_PANEL + footer" % "app.js")

# --- sitemap: next to the simulator it came out of ---------------------------
path = os.path.join(ROOT, "sitemap.xml")
s = open(path).read()
if SLUG in s:
    print("  %-18s already listed" % "sitemap.xml")
else:
    tools = ('  <url>\n    <loc>https://therapistsupport.org/tools.html</loc>\n'
             '    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n')
    assert s.count(tools) == 1
    entry = ('  <url>\n    <loc>https://therapistsupport.org/' + SLUG + '</loc>\n'
             '    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n')
    s = s.replace(tools, tools + entry, 1)
    open(path, "w").write(s)
    changed.append("sitemap.xml")
    print("  %-18s added" % "sitemap.xml")

print("\nchanged:", ", ".join(changed) if changed else "nothing")
