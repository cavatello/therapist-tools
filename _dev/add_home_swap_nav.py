#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the home-page swap into every navigation.

index.html is now the prototype-design home page. The React simulator has moved
to practice-simulator.html and is NOT deleted: it is the only place residency,
the Social Security deep dive, the biweekly pay calendar and the citation blocks
exist. Every nav gets an entry for it so nothing that works today becomes
unreachable.

Idempotent: a file that already carries the entry is skipped.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "practice-simulator.html"
TITLE = "Full simulator"
BLURB = "residency, Social Security, associates in detail"

PAGES = ["tools.html", "about.html", "newsletter.html", "contact.html", "rates.html",
         "associate-mft-job-advisor.html", "therapist-tax-strategy-california.html",
         "grow-your-therapy-practice.html"]
changed = []

for name in PAGES:
    path = os.path.join(ROOT, name)
    s = open(path).read()
    if SLUG in s:
        print("  %-42s already has it" % name)
        continue
    m = re.search(r'(<a href="index\.html(?:#sim)?"[^>]*>)(.*?)(</a>)', s, re.S)
    assert m, name + ": no simulator entry in the nav panel"
    icon = re.search(r'<img src="(data:image/svg\+xml[^"]*)"', m.group(2))
    assert icon, name + ": the simulator entry has no icon to copy"
    entry = ('<a href="' + SLUG + '"><img src="' + icon.group(1) + '" alt="" '
             'aria-hidden="true"><span><b>' + TITLE + '</b><i>' + BLURB + '</i></span></a>')
    s = s.replace(m.group(0), m.group(0) + entry, 1)
    # the footer inventory, where there is one
    fm = re.search(r'(<div><h5>Tools</h5>)((?:<a [^>]*>[^<]*</a>)+)', s)
    if fm and '>Practice Simulator<' in fm.group(2):
        s = s.replace(fm.group(0),
                      fm.group(0) + '<a href="' + SLUG + '">' + TITLE + '</a>', 1)
    open(path, "w").write(s)
    changed.append(name)
    print("  %-42s nav entry added" % name)

# --- app.js: it is now practice-simulator.html's script, and its own nav has to
#     point home at the new home page, not at itself -------------------------
path = os.path.join(ROOT, "app.js")
s = open(path).read()
if SLUG in s:
    print("  %-42s already has it" % "app.js")
else:
    a = ('["piggy", "All free tools", "every calculator and widget, in one place", '
         '"tools.html"],')
    assert s.count(a) == 1, "app.js: NAV_PANEL anchor not found exactly once"
    s = s.replace(a, a + '\n               ["dollar", "' + TITLE + '", "' + BLURB
                  + '", "' + SLUG + '"],', 1)
    open(path, "w").write(s)
    changed.append("app.js")
    print("  %-42s NAV_PANEL entry added" % "app.js")

# --- sitemap ---------------------------------------------------------------
path = os.path.join(ROOT, "sitemap.xml")
s = open(path).read()
if SLUG in s:
    print("  %-42s already listed" % "sitemap.xml")
else:
    tools = ('  <url>\n    <loc>https://cavatello.github.io/therapist-tools/tools.html</loc>\n'
             '    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n')
    assert s.count(tools) == 1
    entry = ('  <url>\n    <loc>https://cavatello.github.io/therapist-tools/' + SLUG + '</loc>\n'
             '    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
    s = s.replace(tools, tools + entry, 1)
    open(path, "w").write(s)
    changed.append("sitemap.xml")
    print("  %-42s added" % "sitemap.xml")

print("\nchanged:", ", ".join(changed) if changed else "nothing")
