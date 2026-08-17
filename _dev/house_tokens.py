#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every design token is close to the house style. None of them equals it.

THE SPEC

`claude/house-style-the-fifth-thing.md` (board entry P8) is the decided
visual direction - the Basecamp-derived synthesis - and it states its
tokens as exact hex:

    --paper #F6F8F6   --card #FFFFFF   --ink #1B2420   --dim #5F6A64
    --line  #DFE4E0   --pine #2C6350   --deep #123C30  --gold #FFE7A3

THE MEASUREMENT

`_dev/_designaudit.mjs` read the computed value of each token on all 234
pages. Seven of the eight are wrong on every single page:

    paper  #F4F7F4  should be #F6F8F6
    ink    #161F1B  should be #1B2420
    dim    #5B665F  should be #5F6A64
    line   #DDE4DE  should be #DFE4E0
    pine   #26604C  should be #2C6350
    deep   #0F3227  should be #123C30
    gold   #FFD976  should be #FFE7A3

Only `--card #FFFFFF` is right.

WHY THIS IS WORTH A PASS RATHER THAN A SHRUG

Every value is *close* - two or three points off in one channel. Nobody
can see a single wrong hex. That is exactly how a design system dies:
each sheet was written from memory of the palette rather than from the
palette, the drift is individually invisible, and collectively the site
stops reading as one thing. Which is the report that started this:
"colors seem different across site".

The literals live in the hand-authored sheets - `house.css`,
`house-chrome.css`, and the five family sheets - which their passes do
NOT regenerate (verified by checksum: running family_rest.py and
family_tool.py leaves the sheets byte-identical, they only edit HTML). So
rewriting them on disk is durable. `_dev/` sources that emit colour
literals are rewritten too, so the next emission is already right, and
the logo's inline SVG in the page footers is included because it is drawn
from the same palette.

WHAT THIS DELIBERATELY DOES NOT TOUCH

`#F6C560`, the CTA button gold, and `#8A6516`, the gold-on-light text
value. Neither is a house token; both are separate verified values, and
`_dev/surface_fix.py` computes contrast against them by name.

Idempotent - after one run there is nothing left to match. Re-run
`_dev/_contrast_audit.mjs` afterwards: `--ink` gets lighter and `--gold`
gets lighter, and both feed contrast pairs.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")

# old -> new, the P8 house style. Order does not matter; none of the new
# values is also an old value, which the guard below asserts.
TOKENS = [
    ("#F4F7F4", "#F6F8F6", "paper"),
    ("#161F1B", "#1B2420", "ink"),
    ("#5B665F", "#5F6A64", "dim"),
    ("#DDE4DE", "#DFE4E0", "line"),
    ("#26604C", "#2C6350", "pine"),
    ("#0F3227", "#123C30", "deep"),
    ("#FFD976", "#FFE7A3", "gold"),
    # NOT a P8 token - a derived value that the P8 palette breaks.
    #
    # #79A08F is the muted on-dark mint used for kickers and emphasis
    # spans in eleven places across the hand-authored sheets. It cleared
    # 4.5:1 against the OLD --deep (#0F3227). Against the spec --deep
    # (#123C30), three points lighter, it measures 4.22:1 - so conforming
    # the palette put 48 pages under the floor. #84AC99 is the smallest
    # lift that clears it (4.86:1), chosen over the bright on-dark mint
    # because this is a quiet kicker and the design intent is muted.
    #
    # It lives here rather than in surface_fix.py because the pk family
    # swaps its stylesheet list wholesale and never loads surface_fix's
    # hoisted sheet - so an override could not reach the 47 pages that
    # need it. Fixing the declaration is the only thing that works.
    ("#79A08F", "#84AC99", "mint"),
]

# Files that carry the literals. _dev sources are included so the next
# emission is already correct rather than being corrected afterwards.
DEV_FILES = ("build_logo.py", "restyle.css", "surface_fix.py",
             "nav_skin_fix.py", "contrast_pass.py", "dark_band_labels.py",
             "token_floor.py", "chrome_armor.py")

# The body metric, same spec, same reasoning. "16.5px body - these pages
# are 6,000 words with tables, not 400 words with a screenshot."
#
# ONLY the .bc2 body rule in house.css. Eight other sheets carry
# `font-size:17.5px` and every one of them is a dek, a hero lede or a
# card headline - display type, not body copy. Changing those would
# shrink the headings too, which the spec does not ask for.
BODY_FILE = os.path.join(SITE, "css", "house.css")
BODY_OLD = "font-size:17.5px; line-height:1.6; letter-spacing:-.011em}"
BODY_NEW = "font-size:16.5px; line-height:1.6; letter-spacing:-.011em}"


HASHED = re.compile(r"^[0-9a-f]{12}\.css$")


def targets():
    """Hand-authored sheets only.

    A sheet named as twelve hex characters is CONTENT-ADDRESSED: the
    filename is sha1(contents)[:12], guarded by token_floor.py and
    css_cdo_fix.py. Editing one means renaming it, and renaming it means
    rewriting every reference - which the family passes then undo,
    because they carry hardcoded sheet-name lists. That was tried, and it
    failed with 216 dangling references.

    The palette is DECLARED in the hand-authored sheets (`.bc2{}` in
    house.css, `body.house{}` in house-chrome.css), so fixing those fixes
    every rule that reads `var(--token)` - which is most of them. Any
    hardcoded old hex left inside a hashed sheet is handled by an
    override, not by an edit.
    """
    out = []
    for f in sorted(os.listdir(CSSDIR)):
        if f.endswith(".css") and not HASHED.match(f):
            out.append(os.path.join(CSSDIR, f))
    for f in DEV_FILES:
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            out.append(p)
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html"):
            out.append(os.path.join(SITE, f))
    d = os.path.join(SITE, "for")
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                out.append(os.path.join(d, f))
    return out


def main():
    # A new value must never also be an old value, or one substitution
    # would undo another depending on order.
    olds = {o.upper() for o, _, _ in TOKENS}
    for _, new, name in TOKENS:
        if new.upper() in olds:
            sys.exit("house_tokens: %s's new value %s is also an old value - "
                     "the rewrite would not be order-independent"
                     % (name, new))

    changed, hits = 0, {}
    for p in targets():
        s = open(p, encoding="utf-8").read()
        orig = s
        for old, new, name in TOKENS:
            # Case-insensitive, but only the exact 6-digit literal, and
            # not when it is part of a longer hex-ish token.
            pat = re.compile(re.escape(old) + r"\b", re.I)
            n = len(pat.findall(s))
            if n:
                hits[name] = hits.get(name, 0) + n
                s = pat.sub(new, s)
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1

    for name, n in sorted(hits.items()):
        print("  %-6s %3d literal(s) rewritten" % (name, n))
    print("  %d file(s) touched" % changed)

    # ---- the body metric
    s = open(BODY_FILE, encoding="utf-8").read()
    if BODY_OLD in s:
        open(BODY_FILE, "w", encoding="utf-8").write(
            s.replace(BODY_OLD, BODY_NEW, 1))
        print("  body   17.5px -> 16.5px (the .bc2 rule only)")

    # ------------------------------------------------------------- guards
    bad = 0
    for p in targets():
        s = open(p, encoding="utf-8").read()
        for old, new, name in TOKENS:
            if re.search(re.escape(old) + r"\b", s, re.I):
                print("GUARD: %s still carries the off-spec %s (%s)"
                      % (os.path.basename(p), name, old))
                bad += 1
    # The spec values must actually be present, or this pass rewrote
    # nothing and is silently doing no work.
    chrome = os.path.join(CSSDIR, "house-chrome.css")
    if os.path.exists(chrome):
        s = open(chrome, encoding="utf-8").read()
        for _, new, name in TOKENS:
            if new not in s:
                print("GUARD: house-chrome.css does not carry the spec %s "
                      "(%s) - the token may have been renamed" % (name, new))
                bad += 1
    s = open(BODY_FILE, encoding="utf-8").read()
    if BODY_NEW not in s:
        print("GUARD: the .bc2 body rule is not at the spec 16.5px - it "
              "was reworded, so this pass no longer knows where it is")
        bad += 1
    if BODY_OLD in s:
        print("GUARD: a 17.5px body rule survives in house.css")
        bad += 1

    if bad:
        sys.exit("%d guard failure(s)" % bad)
    print("  guards clean - 7 tokens and the body metric match the P8 "
          "house style")


if __name__ == "__main__":
    main()
