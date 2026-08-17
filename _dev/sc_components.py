#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The 66 school pages ship two whole components with no CSS at all.

WHAT WAS REPORTED

"colors, text, css look wrong on this page, hard to read" on a school
page, with a screenshot showing:

    Last checked16 August 2026All updates ->
    Figures current as ofeach institution's own current published...
    Published sources onlyKnown gap
    More on this
    Licensure
    ...

Text running together with no spacing, no card, flush to the window edge.
That is not a colour bug and not a layout bug. It is what markup looks
like when NOTHING styles it.

WHAT IT ACTUALLY IS

The school pages are the `sc` family and load exactly three stylesheets:

    house.css   house-chrome.css   house-sc.css

Every other family loads twelve to eighteen. Two components are emitted
onto these pages by passes that run for the whole site -
`_dev/pixel_concepts.py` (the two-clocks freshness block) and
`_dev/uplinks.py` (the "More on this" block) - and NONE of the three
sheets defines their classes. Measured with `_dev/_uncovered.mjs`:

    uncovered on a school page, all 14 carrying visible text:
      tsfoot tsrow tsv tsvint tswhat tsall     <- the freshness block
      uplink uk ud ug uc uall                  <- the up-link block
      exwarn inf                               <- see below

The same check returns 0 on `resources.html` and 1 on
`mft-programs-california.html`, so this is specific to the sc family -
which is exactly the kind of gap `family_art.py`'s "uncovered classes"
guard exists to catch, and the sc family has no equivalent.

WHAT THIS DOES

Copies the canonical rules for those two components out of
`css/house-art.css` AT RUN TIME - not a snapshot - and appends them to
`css/house-sc.css` inside a bracketed block, REWRITING the family prefix
`body.bca` to `body.bcs` on the way. Reading them at run time is the
point: if the art family restyles the freshness block, the school pages
follow instead of drifting.

The prefix rewrite is the whole job. Copying verbatim looks right, keeps
every class name intact, satisfies a naive "is this class mentioned"
guard - and styles nothing, because `body.bca .uplink` cannot match a
page whose body is `bc2 bcs house sc`. Every variable the copied rules
use (--pad, --mn, --dim, --figs, --pine, --line, --card) was checked to
resolve on a school page before this shipped.

`exwarn` and `inf` are deliberately NOT ported. `inf` exists only as
`.vox.inf` in the psychedelic-training sheet, a border-colour modifier,
and `exwarn` is defined nowhere on the site at all - so there is nothing
canonical to copy. Both render as ordinary text without it, which is the
correct fallback; inventing rules for them here would be guessing.

Verify with `_dev/_uncovered.mjs /<a-school-page>.html` - it should drop
from 14 uncovered to 2.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/sc_components.py */"
END = "/* /sc_components */"

SRC = os.path.join(SITE, "css", "house-art.css")
DST = os.path.join(SITE, "css", "house-sc.css")

# The two components, by the classes they are built from.
WANT = {"tsfoot", "tsrow", "tsv", "tsvint", "tswhat", "tsall",
        "uplink", "uk", "ud", "ug", "uc", "uall"}


# The art family scopes every rule to its own body class. Copying them
# verbatim onto the school pages therefore styles nothing at all - the
# first version of this pass did exactly that, passed its own "is the
# class mentioned" guard, and still shipped the unstyled markup. The
# prefix has to be rewritten, and the guard has to check the PREFIX.
SRC_BODY = "body.bca"
DST_BODY = "body.bcs"


def extract(css):
    """Every top-level rule (or @media group) that styles one of WANT."""
    out = []
    for m in re.finditer(r"(@media[^{]*\{(?:[^{}]|\{[^{}]*\})*\}"
                         r"|[^{}@]+\{[^{}]*\})", css):
        blk = m.group(0)
        head = blk if blk.startswith("@media") else blk.split("{")[0]
        if WANT & set(re.findall(r"\.([A-Za-z0-9_-]+)", head)):
            out.append(blk.strip().replace(SRC_BODY, DST_BODY))
    return out


def main():
    for p in (SRC, DST):
        if not os.path.exists(p):
            sys.exit("sc_components: %s is missing" % p)

    blocks = extract(open(SRC, encoding="utf-8").read())
    if not blocks:
        sys.exit("sc_components: nothing matched in house-art.css - the "
                 "component was renamed, and copying nothing would ship "
                 "the unstyled markup again")

    covered = set()
    for b in blocks:
        covered |= WANT & set(re.findall(r"\.([A-Za-z0-9_-]+)", b))
    missing = WANT - covered
    if missing:
        sys.exit("sc_components: house-art.css no longer styles %s - "
                 "refusing to ship a partial copy"
                 % ", ".join(sorted(missing)))

    body = "\n".join([
        MARK,
        "/* The freshness block and the up-link block are emitted onto the",
        "   school pages by pixel_concepts.py and uplinks.py, and none of",
        "   the three sheets this family loads defined them - so they",
        "   shipped as unstyled markup. Copied from house-art.css at build",
        "   time by _dev/sc_components.py so the two cannot drift. */",
    ] + blocks + [END]) + "\n"

    s = open(DST, encoding="utf-8").read()
    orig = s
    if MARK in s:
        if END not in s:
            sys.exit("sc_components: opening mark without its closing mark")
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?",
                   body, s, count=1)
    else:
        s = s.rstrip() + "\n\n" + body
    if s != orig:
        open(DST, "w", encoding="utf-8").write(s)

    # -------------------------------------------------------------- guards
    bad = 0
    s = open(DST, encoding="utf-8").read()
    if s.count(MARK) != 1 or s.count(END) != 1:
        print("GUARD: %d opening and %d closing marks, expected 1 each"
              % (s.count(MARK), s.count(END)))
        bad += 1
    blockonly = s[s.find(MARK):s.find(END)]
    for c in sorted(WANT):
        if ".%s" % c not in blockonly:
            print("GUARD: .%s is still not styled on the sc family" % c)
            bad += 1
    # THE GUARD THAT MATTERS: the copied rules must target THIS family.
    if SRC_BODY in blockonly:
        print("GUARD: %s survived the copy - those rules would match "
              "nothing on a school page" % SRC_BODY)
        bad += 1
    if blockonly.count(DST_BODY) < len(WANT) / 2:
        print("GUARD: only %d %s selectors in the copied block, which is "
              "too few to be the real component"
              % (blockonly.count(DST_BODY), DST_BODY))
        bad += 1
    st = re.sub(r"/\*[\s\S]*?\*/", "", s)
    if st.count("{") != st.count("}"):
        print("GUARD: %d { against %d } in house-sc.css"
              % (st.count("{"), st.count("}")))
        bad += 1
    d = 0
    for ch in st:
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
            if d < 0:
                print("GUARD: a closing brace with nothing open before it")
                bad += 1
                break
    if bad:
        sys.exit("%d guard failure(s)" % bad)
    print("%d rule block(s) copied, %d class(es) now styled on the sc family"
          % (len(blocks), len(WANT)))


if __name__ == "__main__":
    main()
