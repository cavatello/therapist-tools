#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout step 5, family 1: the .artband editorial articles go bc2.

WHAT "CONVERTED" MEANS FOR THIS FAMILY

The article family's markup is already semantic and uniform (hero band,
contents rail, prose, tables, pulls, sources), so the family converts by
REPLACING ITS CSS WHOLESALE rather than by re-emitting content:

  1. every hash-named legacy sheet link is removed (head and body-end),
     and the house-skin link with them - a converted page loads exactly
     three stylesheets, in this order, all in <head>:
         css/house.css?v=<hash>         tokens + element rules (.bc2)
         css/house-chrome.css?v=<hash>  the shared chrome, extracted
         css/house-art.css?v=<hash>     this family's layout (body.bca)
  2. <body class="house"> becomes <body class="bc2 bca house"> - bc2 for
     the tokens, bca for the family sheet, house because the extracted
     chrome rules (and their skin re-colors) key on it.
  3. nothing else. No markup changes, no script changes: the scroll-spy
     (.artnav a + .on), the nav toggle, GA4/Ahrefs/Clarity, form_inline
     and every content byte keep their positions.

WHY THIS IS SAFE AGAINST THE 30-NAME COLLISION AUDIT. The audit's rule is
that a page may not carry bc2 markup AND the old sheets. A converted page
carries NO old sheet, so the collisions (.pull, .row, .tbl, .in ...) are
moot on it; unconverted pages don't load house-art.css, and every rule in
it is gated on body.bca anyway.

GUARDS (a page that fails any of these fails the run, loudly):
  - after conversion: exactly the three named sheets, no 12-hex sheet left
  - the fonts request is still present, untouched
  - every artnav href="#..." still has a matching id= in the document
  - the body class list carries bc2, bca and house exactly once each
  - every class used in the body is in the covered-vocabulary allowlist,
    so a page with a component this family sheet does not style cannot
    ship half-dressed (the house_swap "unrecognized fails the run" rule)

USAGE
    python3 _dev/family_art.py           convert/refresh the family
    python3 _dev/family_art.py --check   verify only, change nothing

Idempotent: a second run only refreshes the ?v= content hashes.
ship.py should carry it AFTER house_swap (which skips body.bca pages).
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

# The family: every root page whose hero is section.artband, except the
# psyd directory (build_psyd.py owns it; it converts with the directory
# family, together with the pending internal-links request).
EXCLUDE = {"psyd-programs-california.html", "tycoon.html", "rates.html"}

HASH_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/[0-9a-f]{12}\.css">\n?')
SKIN_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-skin\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HOUSE_LINKS = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house'
    r'(?:-art|-chrome)?\.css(?:\?v=[0-9a-f]+)?">\n?')
BODY = re.compile(r"<body([^>]*)>")

# Every class name a converted page may carry in <body>. Chrome names are
# styled by house-chrome.css, art* and content names by house-art.css,
# generic names by house.css element/component rules. A class outside this
# list means a component nobody restyled - that page must not convert.
COVERED = set("""
house bc2 bca
sitenav sitenav-in sitenav-mark sitenav-fig sitenav-wordmark sitenav-sub
sitenav-links sitenav-top on sitenav-cta hamb navpanel np-col np-h np-hub
np-hub-t np-hub-d npq np-all
art artband in bcr sep kick dek artmeta tsshort tsk tsa tsfig artfig
artwrap artnav tsn artbody tw tbl n pull quote disc ehrp ehrq
row who track fill val ig ig-cap ig-note seg a b l pl g
arttool artsrc artnext
tsfoot tsmeta tsrow tsv tsall tsvint tsdepth tsbadge part full tswhat
uplink uk ud ug uc uall
long short sr consent nlform nlmeta nlok-tick np-promo ftby
tsupd afl ig-steps ig-bars pl-dl pl-note pl-pub lo cap
ftnl ftin ftroom ftnl-row ftnl-t nlrow ftmail ftbtn ftnote
sitefoot ftcols ftcol ftlbl
""".split())


def family():
    out = []
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in EXCLUDE:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if 'class="artband' in s:
            out.append(f)
    return out


def v(name):
    p = os.path.join(SITE, "css", name)
    return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]


def body_classes(s):
    m = BODY.search(s)
    cm = re.search(r'class="([^"]*)"', m.group(1)) if m else None
    return (cm.group(1).split() if cm else []), m


def check_page(rel, s):
    """Return a list of guard failures for a converted page."""
    bad = []
    if HASH_LINK.search(s):
        bad.append("legacy hash sheet still linked")
    if SKIN_LINK.search(s):
        bad.append("house-skin still linked")
    if len(HOUSE_LINKS.findall(s)) != 3:
        bad.append("expected exactly 3 house sheets, found %d"
                   % len(HOUSE_LINKS.findall(s)))
    if "fonts.googleapis.com/css2" not in s:
        bad.append("fonts request missing")
    classes, _ = body_classes(s)
    for c in ("bc2", "bca", "house"):
        if classes.count(c) != 1:
            bad.append("body class %r count %d" % (c, classes.count(c)))
    for href in re.findall(r'class="artnav"[^>]*>.*?</nav>', s, re.S):
        for anchor in re.findall(r'href="#([^"]+)"', href):
            if ('id="%s"' % anchor) not in s:
                bad.append("artnav anchor #%s has no target" % anchor)
    body = s[s.find("<body"):]
    unknown = set()
    for cl in re.findall(r'class="([^"]*)"', body):
        for c in cl.split():
            if c not in COVERED:
                unknown.add(c)
    if unknown:
        bad.append("uncovered classes: %s" % " ".join(sorted(unknown)))
    return bad


def convert(rel):
    p = os.path.join(SITE, rel)
    s = open(p, encoding="utf-8").read()
    orig = s

    # strip every legacy sheet, the skin, and any stale house links
    s = HASH_LINK.sub("", s)
    s = SKIN_LINK.sub("", s)
    s = HOUSE_LINKS.sub("", s)

    # the three sheets, in cascade order, right after the fonts request
    fonts = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', s)
    if not fonts:
        return "NO FONTS LINK", s
    links = "".join('\n<link rel="stylesheet" href="css/%s?v=%s">'
                    % (n, v(n))
                    for n in ("house.css", "house-chrome.css",
                              "house-art.css"))
    s = s[:fonts.end()] + links + s[fonts.end():]

    # body classes
    classes, m = body_classes(s)
    if m is None:
        return "NO BODY", s
    for c in ("bc2", "bca", "house"):
        if c not in classes:
            classes.append(c)
    order = ["bc2", "bca", "house"] + [c for c in classes
                                       if c not in ("bc2", "bca", "house")]
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs)
    new = 'class="%s"' % " ".join(order)
    attrs = attrs.replace(cm.group(0), new) if cm else attrs + " " + new
    s = s[:m.start()] + "<body%s>" % attrs + s[m.end():]

    changed = s != orig
    open(p, "w", encoding="utf-8").write(s)
    return ("converted" if changed else "already"), s


def main():
    check_only = "--check" in sys.argv
    pages = family()
    if not pages:
        print("family_art: no artband pages found");  sys.exit(1)
    failures = 0
    for rel in pages:
        if check_only:
            s = open(os.path.join(SITE, rel), encoding="utf-8").read()
            classes, _ = body_classes(s)
            if "bca" not in classes:
                print("UNCONVERTED %s" % rel); failures += 1; continue
        else:
            status, s = convert(rel)
            if status.startswith("NO "):
                print("FAIL %s: %s" % (rel, status)); failures += 1
                continue
        bad = check_page(rel, s)
        for b in bad:
            print("GUARD %s: %s" % (rel, b))
        failures += len(bad)
    n = len(pages)
    if failures:
        print("family_art: %d page(s), %d FAILURE(S)" % (n, failures))
        sys.exit(1)
    print("family_art: %d page(s) %s, all guards clean"
          % (n, "checked" if check_only else "converted"))


if __name__ == "__main__":
    main()
