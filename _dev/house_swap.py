#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout steps 2-3: put a page under the house skin.

WHAT THIS DOES, PER PAGE, IDEMPOTENTLY

  1. adds `house` to the <body> class list
  2. appends <link rel="stylesheet" href="css/house-skin.css"> as the LAST
     stylesheet in the document - after the hash-named sheets, which load at
     the end of <body> - so it wins every equal-specificity tie by order

And nothing else. No markup changes, no link changes, no script changes; the
nav toggle, the Formspree handler and every widget keep their exact bytes.
`css/house-skin.css` gates every rule on `body.house`, so an unconverted page
is untouched even though the sheet is shared, and the cascade on a converted
page is deterministic: skin rules beat old rules by specificity (the body
prefix) and, where specificity ties, by source order (the skin loads last).

WHY THE OLD SHEETS STAY, FOR NOW. The collision audit (12 Aug 2026) found 30
of house.css's 91 class names already live in the old sheets, so bc2 MARKUP
cannot safely coexist with old CSS. This pass introduces no bc2 markup - it
re-tokens the old markup - which is the one safe intermediate state. The old
sheets retire per page family at rollout step 5, when each family's markup
actually converts to bc2 components.

USAGE
    python3 _dev/house_swap.py            convert the GATE list below
    python3 _dev/house_swap.py --all      convert every published page
    python3 _dev/house_swap.py --revert   undo (gate list, or with --all)

Runs anywhere in the pipeline after the page exists; ship.py should carry it
late, after the css chain, so a rebuilt page is re-converted.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# The six gate pages - one of each page family, per the rollout doc.
GATE = [
    "index.html",
    "for/associates.html",
    "amft-3000-hours-california.html",
    "county-job-portals-california.html",
    "newsletter.html",
    "about.html",
]

# Never converted: tycoon.html is a static design mockup, and rates.html
# keeps its own editorial voice by decision (see _dev/rates_grid.py).
EXCLUDE = {"tycoon.html", "rates.html"}
# And never a redirect stub. tools.html is a zero-delay meta refresh to
# resources.html - a reader is on it for no measurable time - and this pass
# was the LAST thing linking css/house-skin.css anywhere on the live site,
# because no family pass claims a ts:skip page, so nothing ever un-skinned
# it. Detected by the refresh rather than by name: any redirect stub is a
# page with no reader to style.
REFRESH = re.compile(r'<meta http-equiv="refresh"', re.I)

BODY = re.compile(r"<body([^>]*)>")
SKIN = re.compile(
    r'[ \t]*<link rel="stylesheet" href="(?:\.\./)*css/house-skin\.css'
    r'(?:\?v=[0-9a-f]+)?">\n?')


def skin_v():
    """Content hash of the skin, so a changed sheet busts the browser cache
    the moment the page is fetched instead of after Pages' max-age."""
    p = os.path.join(SITE, "css", "house-skin.css")
    return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]


def pages_all():
    out = [f for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.startswith(".")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    keep = []
    for r in out:
        if r in EXCLUDE:
            continue
        if REFRESH.search(open(os.path.join(SITE, r), encoding="utf-8").read()):
            print("  skip %s - a redirect stub has no reader to style" % r)
            continue
        keep.append(r)
    return keep


def convert(rel, revert=False):
    p = os.path.join(SITE, rel)
    s = open(p, encoding="utf-8").read()
    orig = s

    m = BODY.search(s)
    if not m:
        return "no <body>"
    attrs = m.group(1)
    cm = re.search(r'class="([^"]*)"', attrs)
    classes = cm.group(1).split() if cm else []

    # Rollout step 5: a family-converted page (body.bca et al) owns its
    # whole cascade - no legacy sheets, no skin. Leave it alone entirely.
    if not revert and "bca" in classes:
        return "bc2 family page, skipped"

    if revert:
        if "house" in classes:
            classes.remove("house")
            new = ('class="%s"' % " ".join(classes)) if classes else ""
            na = (attrs.replace(cm.group(0), new).rstrip()
                  if cm else attrs)
            na = re.sub(r'\s+', ' ', na).rstrip()
            s = s[:m.start()] + "<body%s>" % (na and " " + na.strip() or "") \
                + s[m.end():]
        s = SKIN.sub("", s)
    else:
        if "house" not in classes:
            if cm:
                na = attrs.replace(
                    cm.group(0), 'class="%s house"' % cm.group(1)
                    if cm.group(1) else 'class="house"')
            else:
                na = attrs + ' class="house"'
            s = s[:m.start()] + "<body%s>" % na + s[m.end():]
        # Always (re)position the link LAST - a full pipeline run hoists new
        # style blocks into links after this one, and the skin's whole
        # contract is that it wins every equal-specificity tie by order.
        s = SKIN.sub("", s)
        up = "../" * rel.count("/")
        link = ('<link rel="stylesheet" href="%scss/house-skin.css?v=%s">\n'
                % (up, skin_v()))
        # version the house.css link too, where a page carries one
        hp = os.path.join(SITE, "css", "house.css")
        hv = hashlib.sha1(open(hp, "rb").read()).hexdigest()[:8]
        s = re.sub(r'href="((?:\.\./)*css/house\.css)(?:\?v=[0-9a-f]+)?"',
                   r'href="\1?v=%s"' % hv, s)
        i = s.rfind("</body>")
        if i < 0:
            return "no </body>"
        s = s[:i] + link + s[i:]

    if s == orig:
        return "already"
    open(p, "w", encoding="utf-8").write(s)
    return "reverted" if revert else "converted"


def main():
    args = sys.argv[1:]
    revert = "--revert" in args
    rels = pages_all() if "--all" in args else GATE
    counts = {}
    for rel in rels:
        if not os.path.exists(os.path.join(SITE, rel)):
            print("  MISSING %s" % rel)
            continue
        r = convert(rel, revert)
        counts[r] = counts.get(r, 0) + 1
    for k, v in sorted(counts.items()):
        print("  %-10s %d page(s)" % (k, v))

    # guard: a converted page must have the skin link exactly once, and last
    bad = 0
    for rel in pages_all():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        classes = (re.search(r'<body[^>]*class="([^"]*)"', s) or
                   [None, ""])[1].split()
        if "bca" in classes:
            # step-5 family page: no skin by design; family_art.py guards it
            if SKIN.findall(s):
                print("GUARD %s: family page still carries the skin" % rel)
                bad += 1
            continue
        n = len(SKIN.findall(s))
        has = "house" in classes
        if n > 1 or (n == 1) != has:
            print("GUARD %s: house=%s skin-links=%d" % (rel, has, n))
            bad += 1
        if n == 1:
            tail = s[s.rfind("house-skin.css"):]
            if 'rel="stylesheet"' in tail[len("house-skin.css\">"):]:
                print("GUARD %s: skin is not the last stylesheet" % rel)
                bad += 1
    if bad:
        sys.exit("%d guard problem(s)" % bad)
    print("  guards clean")


if __name__ == "__main__":
    main()
