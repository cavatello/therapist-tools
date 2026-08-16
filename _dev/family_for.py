#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout step 5 + P2: the /for/ stage doors go bc2 as their own family.

Family "for" (15 Aug): article.fd-wrap pages -> body.bcf + css/house-for.css

/for/associates.html is the first member and the TEMPLATE the other three
doors copy - P2 door 3, option 3C "The Ledger" (3A's tiles as the expanded
state after input, 3B's questions below the bar), decluttered to the A2
verdict: one dark band, white cards, one accent, room. The markup comes
from _dev/build_forassociates.py; ALL design lives in css/house-for.css.

Follows _dev/family_pk.py exactly:

  1. every hash-named legacy sheet link is removed (head and body-end),
     the house-skin link with them, and any stray house-* family link a
     borrowed chrome brought along; the family's INLINE style blocks are
     removed too (markers: _dev/pagekit.py, _dev/build_forassociates.py,
     _dev/pixel_concepts.py - passes re-emit them on a rebuild and this
     pass, running LAST, re-strips them). A converted page loads exactly
     three stylesheets, in this order, all in <head>:
         css/house.css?v=<hash>         tokens + element rules (.bc2)
         css/house-chrome.css?v=<hash>  the shared chrome, extracted
         css/house-for.css?v=<hash>     this family's layout (body.bcf)
  2. <body class="house"> becomes <body class="bc2 bcf house">.
  3. nothing else. No markup changes, no script changes: the ledger's
     ids and class hooks, the nav toggle, GA4/Ahrefs/Clarity, form_inline
     and every content byte keep their positions.

WHY THIS IS SAFE AGAINST THE 30-NAME COLLISION AUDIT: a converted page
carries NO old sheet, so the audit's collisions are moot on it; every
rule in house-for.css is gated on body.bcf anyway. family_art.py's
borrowed-chrome sweep lists "bcf" in FAMILY_CLASSES so it does not strip
house-chrome off these pages; family_pk's sweep strips any borrowed
house-pk link off them (they are not body.bcp), which is correct.

GUARDS (a page that fails any of these fails the run, loudly):
  - after conversion: exactly the three named sheets, no 12-hex sheet,
    no skin link, no inline <style> left anywhere in the page
  - the fonts request is still present, untouched
  - every hero jump chip href="#..." still has a matching id=
  - the body class list carries bc2, bcf and house exactly once each
  - every class used in static body markup (scripts stripped first) is
    in the covered-vocabulary allowlist, so a page with a component this
    sheet does not style cannot ship half-dressed
  - the ledger's expanded-state hook (.lg-g) is present, so the sheet's
    display:none cannot orphan the tiles

USAGE
    python3 _dev/family_for.py           convert/refresh the family
    python3 _dev/family_for.py --check   verify only, change nothing

Idempotent: a second run only refreshes the ?v= content hashes.
ship.py carries it at the very end of LAST, after house_swap (which
re-skins these pages every run - this pass undoes that) and after the
other family passes (whose sweeps skip or correctly trim body.bcf).
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

FAM = {
    "cls": "bcf", "marker": 'class="fd-wrap', "sheet": "house-for.css",
    "exclude": {"tycoon.html", "rates.html"},
}

SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")

HASH_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/[0-9a-f]{12}\.css">\n?')
SKIN_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-skin\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HOUSE_LINKS = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house'
    r'(?:-art|-sc|-pk|-tool|-rest|-chrome|-for)?\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
FOR_SHEET = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-for\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
BODY = re.compile(r"<body([^>]*)>")

# The family's own inline style blocks, by their pass markers. Builders and
# passes re-emit these on a full rebuild; this pass re-strips them. Any
# OTHER <style> left on a converted page fails the run - unrecognized
# styling is exactly what must not ship half-old (the house_swap rule).
STYLE_BLOCKS = [
    re.compile(r'<style>/\* _dev/pagekit\.py \*/[\s\S]*?</style>\n?'),
    re.compile(r'<style>/\* _dev/build_forassociates\.py'
               r'[\s\S]*?</style>\n?'),
    re.compile(r'<style>/\* _dev/pixel_concepts\.py \*/[\s\S]*?</style>\n?'),
]

# Class allowlist: chrome + shared names, then the door vocabulary.
COVERED = set("""
house bc2 bcf
sitenav sitenav-in sitenav-mark sitenav-fig sitenav-wordmark sitenav-sub
sitenav-links sitenav-top on sitenav-cta hamb navpanel np-col np-h np-hub
np-hub-t np-hub-d npq np-all np-promo long short sr
bcr sep consent nlform nlmeta nlok-tick nlrow ftby
ftnl ftin ftroom ftnl-row ftnl-t ftmail ftbtn ftnote
sitefoot ftcols ftcol ftlbl
tsshort tsk tsa tsfig tsfoot tsdepth tsbadge part full tswhat
uplink uk ud ug uc uall
fd-wrap pk-sec pk-k pk-h pk-h3 pk-d pk-fine
pk-hero hk hl hj hpriv pk-call pk-src
lg lg-in lg-read lg-bar lg-mk lg-g lg-note req hot done open k v s
ask an q start t n shelf card
""".split())


def family():
    out = []
    rels = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            rels += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                     if f.endswith(".html")]
    for rel in rels:
        if os.path.basename(rel) in FAM["exclude"]:
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if FAM["marker"] in s:
            out.append(rel)
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
    if "<style" in s:
        bad.append("an inline <style> block survived conversion")
    if "fonts.googleapis.com/css2" not in s:
        bad.append("fonts request missing")
    classes, _ = body_classes(s)
    for c in ("bc2", FAM["cls"], "house"):
        if classes.count(c) != 1:
            bad.append("body class %r count %d" % (c, classes.count(c)))
    for chips in re.findall(r'<p class="hj">(.*?)</p>', s, re.S):
        for anchor in re.findall(r'href="#([^"]+)"', chips):
            if ('id="%s"' % anchor) not in s:
                bad.append("hero jump #%s has no target" % anchor)
    if 'class="lg-g req"' not in s:
        bad.append("the ledger's expanded-state hook (.lg-g) is missing")
    body = s[s.find("<body"):]
    static = re.sub(r"<(script|style)\b[\s\S]*?</\1>", " ", body)
    unknown = set()
    for cl in re.findall(r'class="([^"]*)"', static):
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

    s = HASH_LINK.sub("", s)
    s = SKIN_LINK.sub("", s)
    s = HOUSE_LINKS.sub("", s)
    for rx in STYLE_BLOCKS:
        s = rx.sub("", s)

    fonts = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', s)
    if not fonts:
        return "NO FONTS LINK", s
    up = "../" * rel.count("/")
    links = "".join('\n<link rel="stylesheet" href="%scss/%s?v=%s">'
                    % (up, n, v(n))
                    for n in ("house.css", "house-chrome.css", FAM["sheet"]))
    s = s[:fonts.end()] + links + s[fonts.end():]

    classes, m = body_classes(s)
    if m is None:
        return "NO BODY", s
    lead = ["bc2", FAM["cls"], "house"]
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
    """Builders lift chrome (head included) from donor pages; a page built
    from a converted door donor would inherit the house-for link on top of
    its own CSS. Strip house-for from every page that is not body.bcf -
    the other families' sweeps handle their own sheets."""
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
        if FAM["cls"] in classes:
            continue
        new = FOR_SHEET.sub("", s)
        if new != s:
            if check_only:
                print("SWEEP %s: borrowed house-for link present" % rel)
                bad += 1
            else:
                open(p, "w", encoding="utf-8").write(new)
                fixed += 1
    if fixed:
        print("  swept borrowed house-for link off %d non-family page(s)"
              % fixed)
    return bad


def main():
    check_only = "--check" in sys.argv
    if not os.path.exists(os.path.join(SITE, "css", FAM["sheet"])):
        sys.exit("family_for: css/%s is missing" % FAM["sheet"])
    pages = family()
    if not pages:
        print("family_for: no %s pages found" % FAM["marker"])
        sys.exit(1)
    failures = 0
    for rel in pages:
        if check_only:
            s = open(os.path.join(SITE, rel), encoding="utf-8").read()
            classes, _ = body_classes(s)
            if FAM["cls"] not in classes:
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
    failures += sweep_borrowed(check_only)
    if failures:
        print("family_for: %d page(s), %d FAILURE(S)" % (len(pages), failures))
        sys.exit(1)
    print("family_for: %d page(s) %s, all guards clean"
          % (len(pages), "checked" if check_only else "converted"))


if __name__ == "__main__":
    main()
