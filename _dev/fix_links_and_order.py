#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the dead links and put the simulator first.

Four things, all reported or found by _dev/linkcheck.py:

1. `index.html#sim` is dead. The old React home page had a #sim section; the
   prototype home page does not, and an anchor that does not resolve just drops
   you at the top of the page with no explanation. 13 occurrences.

2. tools.html's "Associate planner" card pointed at `index.html#sec-income` -
   dead anchor AND the wrong page. That card is about EMPLOYING associates
   (supervision hours, splits, liability, workers' comp), which is the employer
   side and lives in the full simulator. It is NOT the Associate MFT Job
   Advisor, which is the associate's own side. Renamed so the two cannot be
   confused again, and pointed at the page that actually has it.

3. The Associate MFT Job Advisor was missing from the tools page body entirely.
   A whole tool that only appeared in the nav.

4. The simulator was fourth in the Tools column of every nav. It is the thing
   the site is for; it goes first.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PAGES = ["index.html", "practice-simulator.html", "tools.html", "about.html",
         "newsletter.html", "contact.html", "rates.html",
         "associate-mft-job-advisor.html", "therapist-tax-strategy-california.html",
         "grow-your-therapy-practice.html"]

# the order the Tools column should read, top to bottom
ORDER = ["index.html", "therapist-tax-strategy-california.html",
         "grow-your-therapy-practice.html", "associate-mft-job-advisor.html",
         "practice-simulator.html", "tools.html"]

changed = []

# --- 1. the dead #sim anchor, everywhere -----------------------------------
for name in PAGES:
    path = os.path.join(ROOT, name)
    s = open(path).read()
    n = s.count('index.html#sim')
    if not n:
        continue
    s = s.replace('index.html#sim', 'index.html')
    open(path, "w").write(s)
    changed.append(name)
    print("  %-42s %d dead #sim link(s) fixed" % (name, n))

# app.js carries its own copy in NAV_PANEL
path = os.path.join(ROOT, "app.js")
s = open(path).read()
if '"#sim"' in s or 'index.html#sim' in s:
    s = s.replace('"index.html#sim"', '"index.html"').replace('"#sim"', '"index.html"')
    open(path, "w").write(s)
    changed.append("app.js")
    print("  %-42s NAV_PANEL simulator link fixed" % "app.js")

# --- 2 + 3. the tools page body --------------------------------------------
path = os.path.join(ROOT, "tools.html")
s = open(path).read()

old_assoc = ('<h3>Associate planner</h3><p>Supervision hours, splits, liability and '
             'workers&rsquo; comp &mdash; the real cost of bringing someone on.</p>'
             '<a href="index.html#sec-income">Open it &rarr;</a>')
if old_assoc in s:
    new_assoc = ('<h3>Employing associates</h3><p>Supervision hours, splits, liability and '
                 'workers&rsquo; comp &mdash; the real cost of bringing someone on. This is '
                 'the employer&rsquo;s side; if you are the associate, the job advisor below '
                 'is yours.</p>'
                 '<a href="practice-simulator.html">Open it &rarr;</a>')
    s = s.replace(old_assoc, new_assoc, 1)
    print("  %-42s Associate planner -> Employing associates, repointed" % "tools.html")
else:
    # the #sim pass above may already have rewritten the href
    alt = old_assoc.replace('index.html#sec-income', 'index.html')
    assert alt in s, "tools.html: the Associate planner card was not found"
    s = s.replace(alt, alt.replace('<h3>Associate planner</h3>', '<h3>Employing associates</h3>')
                          .replace('href="index.html"', 'href="practice-simulator.html"'), 1)
    print("  %-42s Associate planner repointed (post-#sim form)" % "tools.html")

# the advisor card, built from the Grow card so it inherits the exact markup
if 'associate-mft-job-advisor.html">Open it' not in s:
    i = s.index('<h3>Grow Your Practice</h3>')
    a = s.rfind('<div class="tool"', 0, i)
    b = s.index('</div>', s.index('Open it', i)) + 6
    tmpl = s[a:b]
    card = (tmpl.replace('<h3>Grow Your Practice</h3>', '<h3>Associate MFT Job Advisor</h3>')
                .replace('<p>Referral funnels, lead targets and conversion, worked back from '
                         'the income you actually want.</p>',
                         '<p>For pre-licensed associates. Compare two offers on take-home, on '
                         'what an hour is really worth once unpaid notes are counted, and on '
                         'how fast each one closes your 3,000 BBS hours.</p>')
                .replace('href="grow-your-therapy-practice.html"',
                         'href="associate-mft-job-advisor.html"'))
    assert 'Associate MFT Job Advisor' in card and 'associate-mft-job-advisor.html' in card
    s = s[:b] + card + s[b:]
    print("  %-42s Associate MFT Job Advisor card added" % "tools.html")
open(path, "w").write(s)
if "tools.html" not in changed:
    changed.append("tools.html")

# --- 4. simulator first in every Tools column ------------------------------
def reorder_panel(src, name):
    m = re.search(r'(<div class="np-col"><h5>Tools</h5>)(.*?)(</div>)', src, re.S)
    if not m:
        return src, 0
    entries = re.findall(r'<a href="[^"]*"[^>]*>.*?</a>', m.group(2), re.S)
    if not entries:
        return src, 0
    def key(e):
        h = re.search(r'href="([^"]+)"', e).group(1)
        return ORDER.index(h) if h in ORDER else len(ORDER)
    ordered = sorted(entries, key=key)
    if ordered == entries:
        return src, 0
    # the "you are here" class must follow the page, not the position
    body = "".join(ordered)
    return src.replace(m.group(0), m.group(1) + body + m.group(3), 1), 1

def reorder_footer(src):
    m = re.search(r'(<div><h5>Tools</h5>)((?:<a [^>]*>[^<]*</a>)+)', src)
    if not m:
        return src, 0
    entries = re.findall(r'<a [^>]*>[^<]*</a>', m.group(2))
    def key(e):
        h = re.search(r'href="([^"]+)"', e).group(1)
        return ORDER.index(h) if h in ORDER else len(ORDER)
    ordered = sorted(entries, key=key)
    if ordered == entries:
        return src, 0
    return src.replace(m.group(0), m.group(1) + "".join(ordered), 1), 1

for name in PAGES:
    path = os.path.join(ROOT, name)
    s = open(path).read()
    s, a = reorder_panel(s, name)
    s, b = reorder_footer(s)
    if a or b:
        open(path, "w").write(s)
        if name not in changed:
            changed.append(name)
        print("  %-42s Tools column reordered (%s)" % (
            name, ", ".join(x for x, y in (("nav", a), ("footer", b)) if y)))

# app.js builds its nav from data
path = os.path.join(ROOT, "app.js")
s = open(path).read()
m = re.search(r'\["Tools", \[(.*?)\]\],\n', s, re.S)
if m:
    entries = re.findall(r'\[".*?"\]', m.group(1), re.S)
    def key(e):
        h = re.findall(r'"([^"]+)"', e)[-1]
        return ORDER.index(h) if h in ORDER else len(ORDER)
    ordered = sorted(entries, key=key)
    if ordered != entries:
        s = s.replace(m.group(1), ",\n               ".join(ordered), 1)
        open(path, "w").write(s)
        if "app.js" not in changed:
            changed.append("app.js")
        print("  %-42s NAV_PANEL Tools reordered" % "app.js")

print("\nchanged:", ", ".join(changed) if changed else "nothing")
