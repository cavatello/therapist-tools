#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout step 5, family 4: the tool pages go bc2 - keeping their apps.

Family 4 (16 Aug): the interactive tools -> body.bct + css/house-tool.css

The three earlier families converted by REPLACING their CSS wholesale,
because a family sheet could restyle their whole vocabulary. The tools
cannot convert that way: each carries a real application (the simulator,
the advisor, the hours calculator...) whose extracted app sheets and
inline style blocks hold hundreds of layout rules nobody should re-type.
So this family converts by SUBTRACTION AND RE-GROUNDING instead:

  1. drop exactly the legacy sheets that css/house-chrome.css replicates
     (derived at runtime from its own "from css/XXXX.css" markers - the
     list maintains itself), plus the house-skin link and any stray house
     links. THE APP'S OWN HASH SHEETS AND INLINE <style> BLOCKS STAY.
  2. add, right after the fonts link and before the app sheets:
         css/house.css?v=<hash>          tokens + element rules (.bc2)
         css/house-chrome.css?v=<hash>   the shared chrome
         css/house-tool.css?v=<hash>     this family's re-grounding
     house-tool.css is the set of house-skin rules that touched tool-app
     vocabulary, ported verbatim with body.house -> body.bct (and the
     token block restated, since the skin carried it) - so a converted
     page looks exactly as it did skinned, minus the flash of unstyled
     old design, because the replicated chrome no longer loads at all.
  3. <body class="..."> gains bc2 + bct + house.

MEMBERSHIP IS A LIST, not a marker: the tools share no wrapper class.
finding-a-clinical-supervisor-california.html sits here rather than in
family 2 because it embeds the advisor app (family_pk.py's own note).

GUARDS: no replicated-chrome sheet remains; no skin link; exactly three
house links; the fonts request survives; at least one app sheet remains
on pages that had one (dropping a tool's own CSS is the catastrophic
failure mode here); body carries bc2/bct/house exactly once each.

USAGE
    python3 _dev/family_tool.py           convert/refresh
    python3 _dev/family_tool.py --check   verify only

Idempotent. ship.py runs it in LAST after house_swap (which re-skins
these pages every run - this pass undoes that), family_art and family_pk
(both of whose sweeps must skip body.bct, via FAMILY_CLASSES).
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

CLS = "bct"
SHEET = "house-tool.css"
PAGES = [
    "practice-simulator.html",
    "therapist-tax-strategy-california.html",
    "associate-mft-job-advisor.html",
    "amft-3000-hours-california.html",
    "therapist-cost-of-living-california.html",
    "grow-your-therapy-practice.html",
    "calculators.html",
    # NOT tools.html: it is a meta-refresh redirect stub (ts:skip) with
    # its own 10-line inline style and no fonts link - nothing to convert.
    "finding-a-clinical-supervisor-california.html",
]
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")

SKIN_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-skin\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HOUSE_LINKS = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house'
    r'(?:-art|-sc|-pk|-tool|-chrome)?\.css(?:\?v=[0-9a-f]+)?">\n?')
TOOL_SHEET = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-tool\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HASH_LINK_ANY = re.compile(
    r'<link rel="stylesheet" href="(?:\.\./)*css/([0-9a-f]{12})\.css">')
BODY = re.compile(r"<body([^>]*)>")


def replicated_chrome():
    """The sheets house-chrome.css was extracted from, by its own markers."""
    s = open(os.path.join(SITE, "css", "house-chrome.css"),
             encoding="utf-8").read()
    names = set(re.findall(r'from css/([0-9a-f]{12})\.css', s))
    if len(names) < 5:
        sys.exit("family_tool: house-chrome.css markers name only %d "
                 "sheet(s) - the derivation is broken" % len(names))
    return names


def v(name):
    p = os.path.join(SITE, "css", name)
    return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]


def body_classes(s):
    m = BODY.search(s)
    cm = re.search(r'class="([^"]*)"', m.group(1)) if m else None
    return (cm.group(1).split() if cm else []), m


def check_page(rel, s, chrome, had_app):
    bad = []
    for name in HASH_LINK_ANY.findall(s):
        if name in chrome:
            bad.append("replicated chrome sheet %s.css still linked" % name)
    if SKIN_LINK.search(s):
        bad.append("house-skin still linked")
    n = len(HOUSE_LINKS.findall(s))
    if n != 3:
        bad.append("expected exactly 3 house sheets, found %d" % n)
    if "fonts.googleapis.com/css2" not in s:
        bad.append("fonts request missing")
    if had_app and not HASH_LINK_ANY.search(s):
        bad.append("ALL hash sheets gone - the app's own CSS was dropped")
    classes, _ = body_classes(s)
    for c in ("bc2", CLS, "house"):
        if classes.count(c) != 1:
            bad.append("body class %r count %d" % (c, classes.count(c)))
    return bad


def convert(rel, chrome):
    p = os.path.join(SITE, rel)
    s = open(p, encoding="utf-8").read()
    orig = s

    # drop only the replicated chrome sheets, keep the app's own
    def drop(m):
        return "" if m.group(1) in chrome else m.group(0)
    s = re.sub(r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/'
               r'([0-9a-f]{12})\.css">\n?',
               lambda m: "" if m.group(1) in chrome else m.group(0), s)
    s = SKIN_LINK.sub("", s)
    s = HOUSE_LINKS.sub("", s)

    fonts = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', s)
    if not fonts:
        return "NO FONTS LINK", s
    up = "../" * rel.count("/")
    links = "".join('\n<link rel="stylesheet" href="%scss/%s?v=%s">'
                    % (up, n, v(n))
                    for n in ("house.css", "house-chrome.css", SHEET))
    s = s[:fonts.end()] + links + s[fonts.end():]

    classes, m = body_classes(s)
    if m is None:
        return "NO BODY", s
    lead = ["bc2", CLS, "house"]
    for c in lead:
        if c not in classes:
            classes.append(c)
    order = lead + [c for c in classes if c not in lead]
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs)
    new = 'class="%s"' % " ".join(order)
    attrs = attrs.replace(cm.group(0), new) if cm else attrs + " " + new
    s = s[:m.start()] + "<body%s>" % attrs + s[m.end():]

    changed = s != orig
    open(p, "w", encoding="utf-8").write(s)
    return ("converted" if changed else "already"), s


def sweep_borrowed(check_only):
    """Strip a borrowed house-tool link off any page that is not body.bct."""
    fixed, bad = 0, 0
    rels = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            rels += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                     if f.endswith(".html")]
    for rel in rels:
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        classes, _ = body_classes(s)
        if CLS in classes:
            continue
        new = TOOL_SHEET.sub("", s)
        if new != s:
            if check_only:
                print("SWEEP %s: borrowed house-tool link present" % rel)
                bad += 1
            else:
                open(p, "w", encoding="utf-8").write(new)
                fixed += 1
    if fixed:
        print("  swept borrowed house-tool link off %d non-family page(s)"
              % fixed)
    return bad


def main():
    check_only = "--check" in sys.argv
    if not os.path.exists(os.path.join(SITE, "css", SHEET)):
        sys.exit("family_tool: css/%s is missing" % SHEET)
    chrome = replicated_chrome()
    failures = 0
    for rel in PAGES:
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            print("MISSING %s" % rel); failures += 1; continue
        before = open(p, encoding="utf-8").read()
        had_app = any(n not in chrome
                      for n in HASH_LINK_ANY.findall(before))
        if check_only:
            s = before
            classes, _ = body_classes(s)
            if CLS not in classes:
                print("UNCONVERTED %s" % rel); failures += 1; continue
        else:
            status, s = convert(rel, chrome)
            if status.startswith("NO "):
                print("FAIL %s: %s" % (rel, status)); failures += 1
                continue
        bad = check_page(rel, s, chrome, had_app)
        for b in bad:
            print("GUARD %s: %s" % (rel, b))
        failures += len(bad)
    failures += sweep_borrowed(check_only)
    if failures:
        print("family_tool: %d FAILURE(S)" % failures)
        sys.exit(1)
    print("family_tool: %d page(s) %s, all guards clean"
          % (len(PAGES), "checked" if check_only else "converted"))


if __name__ == "__main__":
    main()
