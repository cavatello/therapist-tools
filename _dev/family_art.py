#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout step 5: page families go bc2, one family at a time.

Family 1 (13 Aug): the .artband editorial articles -> body.bca + house-art.css
Family 2 (13 Aug): the .scband program pages   -> body.bcs + house-sc.css

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

# Each family: the marker that identifies membership, the body class that
# gates its sheet, the sheet itself, and pages excluded even if they match.
FAMILIES = [
    {"cls": "bca", "marker": 'class="artband', "sheet": "house-art.css",
     "nav": "artnav",
     "exclude": {"psyd-programs-california.html", "tycoon.html",
                 "rates.html"}},
    {"cls": "bcs", "marker": 'class="scband', "sheet": "house-sc.css",
     "nav": "scnav",
     "exclude": {"associate-mft-job-advisor.html",
                 "tycoon.html", "rates.html"}},
]
# "bcp" is family 2 (the pagekit pages, _dev/family_pk.py); it is listed
# here so sweep_borrowed_chrome does not strip house-chrome.css off a
# page that family owns. "bcf" is the /for/ stage doors (_dev/family_for.py),
# listed for the same reason.
FAMILY_CLASSES = tuple(f["cls"] for f in FAMILIES) + ("bcp", "bct", "bcz",
                                                      "bcf")

HASH_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/[0-9a-f]{12}\.css">\n?')
SKIN_LINK = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-skin\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')
HOUSE_LINKS = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house'
    r'(?:-art|-sc|-chrome)?\.css(?:\?v=[0-9a-f]+)?">\n?')
BODY = re.compile(r"<body([^>]*)>")

# Class allowlists. Chrome and shared names are common; each family adds
# its own vocabulary. A class outside the union for its family means a
# component nobody restyled - that page must not convert.
SHARED = set("""
house bc2 bca bcs
sitenav sitenav-in sitenav-mark sitenav-fig sitenav-wordmark sitenav-sub
sitenav-links sitenav-top on sitenav-cta hamb navpanel np-col np-h np-hub
np-hub-t np-hub-d npq np-all np-promo long short sr
bcr sep tsshort tsk tsa tsfig tsn
tsfoot tsmeta tsrow tsv tsall tsvint tsdepth tsbadge part full tswhat tsupd
uplink uk ud ug uc uall
consent nlform nlmeta nlok-tick ftby
ftnl ftin ftroom ftnl-row ftnl-t nlrow ftmail ftbtn ftnote
sitefoot ftcols ftcol ftlbl
""".split())

COVERED = {
 "bca": SHARED | set("""
art artband in kick dek artmeta artfig
artwrap artnav artbody tw tbl n pull quote disc ehrp ehrq
row who track fill val ig ig-cap ig-note seg a b l pl g
arttool artsrc artnext
afl ig-steps ig-bars pl-dl pl-note pl-pub lo cap
""".split()),
 "bcs": SHARED | set("""
scband in sub dek scmeta scfig row scwrap scnav scbody
orient media vfig vplay vbtn vkind pfig cred
crsl crs chd ccode cun cq cwhy srcl
cutot trml trm tn
verd mix ok warn neg pos pq exwarn
tbl r prg pr np yr q
exg exb sw
ocl octw octbl ocdef
voxl vox vwho thl th tm sn
ask nxt nx srcs gapl pnote inf board
sc gap thin vmeta
""".split()),
}

def family(fam):
    out = []
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in fam["exclude"]:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if fam["marker"] in s:
            out.append(f)
    return out


def v(name):
    p = os.path.join(SITE, "css", name)
    return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]


def body_classes(s):
    m = BODY.search(s)
    cm = re.search(r'class="([^"]*)"', m.group(1)) if m else None
    return (cm.group(1).split() if cm else []), m


def check_page(rel, s, fam):
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
    for c in ("bc2", fam["cls"], "house"):
        if classes.count(c) != 1:
            bad.append("body class %r count %d" % (c, classes.count(c)))
    for href in re.findall(r'class="%s"[^>]*>.*?</nav>' % fam["nav"],
                           s, re.S):
        for anchor in re.findall(r'href="#([^"]+)"', href):
            if ('id="%s"' % anchor) not in s:
                bad.append("%s anchor #%s has no target"
                           % (fam["nav"], anchor))
    body = s[s.find("<body"):]
    unknown = set()
    for cl in re.findall(r'class="([^"]*)"', body):
        for c in cl.split():
            if c not in COVERED[fam["cls"]]:
                unknown.add(c)
    if unknown:
        bad.append("uncovered classes: %s" % " ".join(sorted(unknown)))
    return bad


def convert(rel, fam):
    p = os.path.join(SITE, rel)
    s = open(p, encoding="utf-8").read()
    orig = s

    s = HASH_LINK.sub("", s)
    s = SKIN_LINK.sub("", s)
    s = HOUSE_LINKS.sub("", s)

    fonts = re.search(r'<link href="https://fonts\.googleapis\.com[^>]*>', s)
    if not fonts:
        return "NO FONTS LINK", s
    links = "".join('\n<link rel="stylesheet" href="css/%s?v=%s">'
                    % (n, v(n))
                    for n in ("house.css", "house-chrome.css",
                              fam["sheet"]))
    s = s[:fonts.end()] + links + s[fonts.end():]

    classes, m = body_classes(s)
    if m is None:
        return "NO BODY", s
    lead = ["bc2", fam["cls"], "house"]
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


SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")
FAMILY_SHEETS = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-'
    r'(?:art|sc|pk|tool|rest|chrome)\.css(?:\?v=[0-9a-f]+)?">\n?')
HOUSE_SHEET = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')


def sweep_borrowed_chrome(check_only):
    """Builders lift chrome (head included) from donor pages. Once a donor
    is family-converted, every page rebuilt from it inherits the three
    named sheets on top of its own legacy CSS - the exact mixed state the
    collision audit forbids. This sweep, running last, strips the family
    sheets from every non-family page: house-art/house-chrome always, and
    house.css too unless the page really carries bc2 markup (the home
    page does; a borrowed head does not make a page bc2)."""
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
        if any(c in classes for c in FAMILY_CLASSES):
            continue
        has_bc2_markup = re.search(r'class="bc2[ "]', s) is not None
        new = FAMILY_SHEETS.sub("", s)
        if not has_bc2_markup:
            new = HOUSE_SHEET.sub("", new)
        if new != s:
            if check_only:
                print("SWEEP %s: borrowed family sheet(s) present" % rel)
                bad += 1
            else:
                open(p, "w", encoding="utf-8").write(new)
                fixed += 1
    if fixed:
        print("  swept borrowed family sheets off %d non-family page(s)"
              % fixed)
    return bad


def main():
    check_only = "--check" in sys.argv
    failures, total = 0, 0
    for fam in FAMILIES:
        pages = family(fam)
        if not pages:
            print("family_art: no %s pages found" % fam["marker"])
            sys.exit(1)
        total += len(pages)
        for rel in pages:
            if check_only:
                s = open(os.path.join(SITE, rel), encoding="utf-8").read()
                classes, _ = body_classes(s)
                if fam["cls"] not in classes:
                    print("UNCONVERTED %s" % rel); failures += 1; continue
            else:
                status, s = convert(rel, fam)
                if status.startswith("NO "):
                    print("FAIL %s: %s" % (rel, status)); failures += 1
                    continue
            bad = check_page(rel, s, fam)
            for b in bad:
                print("GUARD %s: %s" % (rel, b))
            failures += len(bad)
    failures += sweep_borrowed_chrome(check_only)
    if failures:
        print("family_art: %d page(s), %d FAILURE(S)" % (total, failures))
        sys.exit(1)
    print("family_art: %d page(s) %s across %d families, all guards clean"
          % (total, "checked" if check_only else "converted", len(FAMILIES)))


if __name__ == "__main__":
    main()
