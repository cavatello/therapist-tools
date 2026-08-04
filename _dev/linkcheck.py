#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every internal link on the site, checked against what actually exists.

Three separate classes of dead link have shipped on this site and none of them
produced an error of any kind:

  1. a link to a page that does not exist
  2. a link to an ANCHOR that no longer exists, because the section moved to
     its own page (#sim, #sec-income, #tax, #grow)
  3. a link that resolves fine but points at the WRONG page - the Associate
     planner card on tools.html pointing at the simulator

This catches 1 and 2 mechanically. 3 needs the CLAIMS table below, which pairs
the visible link text with the page it is supposed to reach.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PAGES = ["index.html", "practice-simulator.html", "tools.html", "about.html",
         "newsletter.html", "contact.html", "rates.html", "therapist-working-remotely-california.html",
    "therapist-cost-of-living-california.html",
    "amft-3000-hours-california.html",
    "terms.html", "privacy.html",
         "associate-mft-job-advisor.html", "therapist-tax-strategy-california.html",
         "grow-your-therapy-practice.html"]

# index.html is the prototype: its router has no page tokens, its anchors are
# real element ids. (practice-simulator.html was the React app until 2 Aug 2026;
# "#grow" are PAGE TOKENS handled by pageFromHash(), not element ids - so they
# are declared valid here rather than looked up in the markup.
ROUTER_TOKENS = {}

# Link text -> the page it must reach. Matched case-insensitively on the text.
CLAIMS = [
    ("associate job advisor", "associate-mft-job-advisor.html"),
    ("associate planner", "associate-mft-job-advisor.html"),
    ("associate mft", "associate-mft-job-advisor.html"),
    ("tax & retirement", "therapist-tax-strategy-california.html"),
    ("tax and retirement", "therapist-tax-strategy-california.html"),
    ("grow your practice", "grow-your-therapy-practice.html"),
    ("grow your therapy practice", "grow-your-therapy-practice.html"),
    # The simulator moved to practice-simulator.html on 2 Aug 2026, when
    # index.html became the landing page. "full simulator" is retired language -
    # there is only one simulator now.
    ("practice simulator", "practice-simulator.html"),
    ("all free tools", "tools.html"),
    ("field notes", "rates.html"),
    ("newsletter", "newsletter.html"),
]

ids_by_page = {}
for p in PAGES:
    src = open(os.path.join(ROOT, p)).read()
    ids_by_page[p] = set(re.findall(r'id="([\w-]+)"', src))
# app.js used to render practice-simulator.html's body, so its ids belonged to
# that page. It was retired on 2 Aug 2026 - the page is now a plain HTML file
# and carries its own ids - so this is skipped when the file is absent rather
# than crashing the checker.
_appjs = os.path.join(ROOT, "app.js")
if os.path.exists(_appjs):
    app = open(_appjs).read()
    ids_by_page["practice-simulator.html"] |= set(re.findall(r'id: ?"([\w-]+)"', app))
    ids_by_page["practice-simulator.html"] |= set(re.findall(r'id:"([\w-]+)"', app))

problems = []
checked = 0

for p in PAGES:
    src = open(os.path.join(ROOT, p)).read()
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', src, re.S):
        href, inner = m.group(1), m.group(2)
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner)).strip()
        if href.startswith(("http", "mailto:", "tel:", "data:")) or not href:
            continue
        # hrefs built by JS at render time ("' + taxHref() + '") are not links in
        # the source and cannot be resolved here; they are covered by the
        # hand-off test instead.
        if "' +" in href or "+ '" in href:
            continue
        checked += 1
        file_part, _, anchor = href.partition("#")
        target = file_part or p

        # 1. does the file exist?
        if file_part and not os.path.exists(os.path.join(ROOT, file_part)):
            problems.append((p, href, text, "target file does not exist"))
            continue
        # 2. does the anchor exist on it?
        if anchor:
            valid = ids_by_page.get(target, set()) | ROUTER_TOKENS.get(target, set())
            if target in ids_by_page and anchor not in valid:
                problems.append((p, href, text, "anchor #%s is not on %s" % (anchor, target)))
                continue
        # 3. does it go where the words say it goes?
        low = text.lower()
        for claim, want in CLAIMS:
            if low == claim and file_part and file_part != want:
                problems.append((p, href, text,
                                 'link text says "%s" but points at %s, not %s'
                                 % (text, file_part, want)))
                break

print("checked %d internal links across %d pages" % (checked, len(PAGES)))
if problems:
    print("\n%d PROBLEM(S):\n" % len(problems))
    for page, href, text, why in problems:
        print("  %-40s %-40s" % (page, href))
        print("      text: %-30s  %s" % ('"' + text[:28] + '"', why))
    sys.exit(1)
print("no dead or misdirected internal links")
