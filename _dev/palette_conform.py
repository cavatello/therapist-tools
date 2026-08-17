#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""113 near-misses collapse onto the twelve colours they were trying to be.

WHY THIS EXISTS, AND WHY house_tokens.py WAS NOT ENOUGH

`ship.py` already says the thing out loud, in the comment above
`house_tokens.py`: *"the eight were wrong on all 234 pages - close, never
equal, which is how a design system dies quietly."* That pass fixed the
eight. It fixed them by rewriting seven old->new pairs that had been
MEASURED on `body`, which means it only ever found the drift it had
already been shown.

`palette_census.py` asked the question the other way round - not "did the
tokens land?" but "what colours does this site actually use?" - and the
answer was **297 colours in 2,497 uses across 240 published pages**, of
which 21 were sanctioned. `#16211B` alone appears 430 times: the old ink,
twelve units of perceptual distance from `--ink #1B2420`, indistinguishable
side by side and different in every stylesheet that carries it.

That is the disease, not a symptom of it. A reader does not see `#16211B`;
they see that this page is a shade off the last one, and they cannot say
why. Which is exactly the report that started this: *"colors seem
different across site."*

WHAT IT CONFORMS, AND WHAT IT DELIBERATELY LEAVES

113 colours, 1,363 uses. Every one of them is inside 32 units of a
sanctioned colour in the same hue family, so each swap is a rounding
correction rather than a design decision. Grouped by the token they
collapse onto, the families are legible on sight - eight dark green-blacks
onto `--ink`, thirty-one near-white tints onto `--paper`, fourteen warm
greys onto the muted label colour, twenty pale tans onto `--line`.

Three gates decide membership, and all three matter:

  distance <= 32   a bigger jump is a visible change, and a visible change
                   is a design decision that belongs in a design doc, not
                   in a normalising pass.
  house hue        25-65 degrees (the warm neutrals and golds) or 100-200
                   (the greens), or chroma under 0.02 (a true grey). This
                   is the gate that saves the semantics: `#FBEFEC` is a
                   near-white too, but it is a near-white with a red cast,
                   because it is the surface under a warning. Collapsing
                   it onto `--paper` would delete the warning and pass
                   every contrast check while doing it.
  same family      the target is the nearest anchor, and the anchor list
                   holds only real roles.

So the reds (`#B5483F` and its nine drifted cousins), the verdict green
`#3F9577`, the amber `#C98B4B`, the simulator's purples and the whole
`tycoon.html` game palette are NOT touched here. They are semantic or
deliberately other, they are recorded in `_dev/palette_baseline.json`, and
a decision about them is a decision about the design.

WHERE IT WRITES

Everywhere a colour can hide, which is four places, and the fourth is the
one that gets missed:

  css/house*.css        hand-authored, edited in place
  css/<12-hex>.css      content-addressed - the filename IS the sha1 of the
                        contents, so these are rewritten under a NEW hash,
                        every <link> in the repository is repointed, and the
                        stale file is moved to _to_delete/ once nothing
                        references it. Same mechanism as token_floor.py.
  <style> blocks        1,693 of the 2,497 uses were here, in per-page
                        blocks that `extract_css.py` never hoisted because
                        fewer than four pages shared them
  style="..."          80 uses, invisible to anything that only reads
                        stylesheets

THE TEMPLATE THAT IS NOT A PAGE

`_dev/chrome_donor.html` had to be added to scope, and finding out why cost
a whole failed pipeline run. It reads like frozen scratch - it is in `_dev/`,
nothing links to it, it is not in the sitemap - and it is nothing of the
kind: **eight builders read it every run and copy its <head> and chrome into
the pages they write.** It hardcodes twenty-five stylesheet <link>s.

So conforming the site and skipping the donor produced a site whose builders
immediately un-conformed it: the donor still named the pre-rename hashed
sheets, the builders copied those names onto the pages they rebuild, and
`token_floor.py` failed with **1,008 dangling stylesheet links** on the very
next build. A template is in scope for both halves of this pass - repointing
AND recolouring - because everything it stamps out is in scope.

The mockups under `_dev/mohel-mockups/` and `_dev/mockups/` are not
templates and stay out.

NOT IN SCOPE, ON PURPOSE

`tycoon.html` and `concepts.html` are visual-direction mockups. Neither is
in `sitemap.xml`. Holding a mockup to the house palette is how you lose the
mockup. Their <link>s are still repointed - a renamed sheet must not 404
anywhere - they are simply not recoloured.

WHY IT RUNS WHERE IT RUNS

After the CSS chain, so hoisted sheets are conformed too, and before
`discovery.py` and `linkcheck.py`, so the repointed links are what those
two see. After `token_floor.py`, which is upstream of it in a specific
sense: token_floor lifts eleven under-floor colours onto targets of its
own (`#635E53`, `#8A6023`, `#4A5A46`), three of which are themselves
off-palette. This pass then normalises those onward. Two passes, one
direction, no cycle - and there is a guard below that proves no target of
this pass is also one of its keys.

WHY ONE GROUP IS MAPPED BY DECLARATION, NOT BY COLOUR

The twenty pale tans were first mapped flat onto `--line`, because that is
the nearest anchor to all twenty. The browser sweep answered with **141 new
findings on 88 pages**: `--dim` on `--line` is 4.37:1, and `.orient`,
`.arttool` and `.fchip` had been sitting on a pale tan at 4.5-plus.

The colour was not the mistake. The ROLE was. Counted over the repository,
those twenty hexes appear in 102 background declarations, 85 border
declarations and 23 `color` declarations - one hex doing three jobs, so one
target cannot be right for all three. `--line #DFE4E0` is a hairline; it is
a full shade darker than `--paper #F6F8F6`, which is why using it as a chip
surface put text under the floor. So this group maps three ways:

    background, fill, --soft/--wash   -> --paper   (--dim on it is 5.2:1)
    border, outline, box-shadow       -> --line    (a hairline stays a
                                                    hairline)
    color                             -> the light mint, which is what a
                                        pale colour painting letters means:
                                        text on a dark band

Same mechanism as `token_floor.py`'s TEXT_ONLY, generalised from two roles
to three. This is the general lesson and it is now written down twice in
this repository: **a class or a colour can have two surfaces, and you have
to measure both.**

Idempotent: every target is sanctioned and no target is a key, so a second
run finds nothing. Guarded: no key may survive in scope, every hashed sheet
must still be named for its own contents, and every linked sheet must exist.

The empirical check is not in here. It is `_dev/_contrast_audit.mjs` run
over all 242 pages before and after, and `palette_census.py --check` in
ship.py's verify stage. Arithmetic on a cross-product of colours produces
false alarms - `--line` as a text background is a pairing that does not
occur - so the pass is measured in a browser, on the real pages.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
# Mockups. See "NOT IN SCOPE" above. Recolouring is skipped; link
# repointing is not.
NOCOLOUR = {"tycoon.html", "concepts.html"}

LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')

# old -> new. Generated by the three gates in the docstring, then read
# through by hand family by family; the comment above each block is the
# role its target plays, which is the only way to review a colour table.
MAP = {}
for _olds, _new in [
    # -> #1B2420  --ink. The old ink and its seven neighbours.
    (("#12281F", "#14261E", "#16211B", "#17271F", "#1E241C", "#22301F",
      "#26241E", "#2A2620"), "#1B2420"),
    # -> #F6F8F6  --paper. Thirty-one ways to spell "not quite white",
    # which is what happens when every pass picks its own tint.
    (("#E7F1EB", "#E9F2EC", "#EAF0EB", "#EAF2EC", "#EEF5F1", "#EFF5F2",
      "#EFF7F3", "#F1F0E8", "#F1F7F4", "#F2F7F4", "#F2F8F1", "#F3FAF6",
      "#F4F1E7", "#F4F1E8", "#F4F2EC", "#F4F7F3", "#F6F3EA", "#F6FBF8",
      "#F7F3E9", "#F7F4EC", "#F7FAF6", "#FAF7EF", "#FBF6E9", "#FBF7EE",
      "#FBF9F3", "#FBFAF6", "#FCFAF2", "#FCFAF4", "#FDF8EF", "#FDFCF8",
      "#FFFCF4"), "#F6F8F6"),
    # -> #635D4E  the muted label colour, 6.07:1 on cream.
    (("#5A5647", "#5A6754", "#5B5344", "#5C574D", "#5D574C", "#5E5A50",
      "#635E53", "#67604F", "#6B6455", "#6C6555", "#6C6558", "#6E6553",
      "#6E6656", "#6E6857"), "#635D4E"),
    # -> #C6DBD1  the light mint: on-dark body text at 9.6:1, and the
    # canonical light mint surface.
    (("#BEDDD0", "#BEDFD1", "#BFD3C7", "#BFE0D3", "#C6DCD1", "#C8D2CB",
      "#C9DED5", "#CFE0D6", "#CFE3CB", "#CFE3D6"), "#C6DBD1"),
    # -> #123C30  --deep, the slab green.
    (("#173B2E", "#1A4739", "#1B4536", "#1E3B30", "#1E4436"), "#123C30"),
    # -> #8A6516  gold as text. token_floor lifts three under-floor
    # colours onto #8A6023; this finishes the journey.
    (("#7F5A1F", "#8A5A22", "#8A5B22", "#8A6023", "#8A6318", "#8A6620",
      "#8A6A20"), "#8A6516"),
    # -> #2C6350  --pine, the one accent.
    (("#20614B", "#25584A", "#2F5E4E", "#2F6B57", "#2F6E56"), "#2C6350"),
    # -> #5F6A64  --dim, 5.2:1.
    (("#5A6A56", "#6B6A63", "#6E695E"), "#5F6A64"),
    # -> #14372C  the ink used on the CTA gold, 8.11:1.
    (("#123026", "#15342B", "#16382B", "#17352A", "#1A3A2E"), "#14372C"),
    # -> #84AC99  the muted kicker on a dark band, 4.86:1.
    (("#7FB79B", "#8FAF9F", "#8FB3A3"), "#84AC99"),
    # -> #FFFFFF  --card.
    (("#FCFEFC", "#FFFDF6"), "#FFFFFF"),
]:
    for _o in _olds:
        MAP[_o] = _new

# The twenty pale tans, mapped by the job the declaration gives them. See
# "WHY ONE GROUP IS MAPPED BY DECLARATION" above - a flat map onto --line
# put 141 text/background pairs under 4.5:1, because --line is a hairline
# and these were being used as chip surfaces.
BY_ROLE = {
    "fill": "#F6F8F6",   # --paper. --dim on it is 5.2:1.
    "edge": "#DFE4E0",   # --line. A hairline stays a hairline.
    "text": "#C6DBD1",   # the light mint: a pale colour painting letters
}                        # is text on a dark band.
ROLED = ("#DCEAE2", "#DCEAE3", "#E0F0EA", "#E4DFD2", "#E6E0D2", "#E6E4DC",
         "#E7E0D0", "#E7E2D6", "#E7F0EA", "#EDE7D8", "#EDE8DA", "#EDE8DC",
         "#EDEAE0", "#EFEADC", "#EFEDE4", "#EFEDE7", "#F0EADA", "#F0EBDE",
         "#F1EDE0", "#F1EDE2")
for _o in ROLED:
    MAP[_o] = None       # a placeholder, so the guards and the loop check
                         # still see these as keys

# Word-boundary matters: `#16211B0A` is not `#16211B`.
KEYS = re.compile("(" + "|".join(re.escape(k) for k in sorted(MAP)) + r")\b",
                  re.IGNORECASE)
# Which job a property gives a colour. `--line` counts as an edge and
# `--mut` as text: a custom property named for a role IS that role, which
# is the one case where a variable can be resolved safely.
EDGE = re.compile(r"^(border|outline)|shadow|^(line|rule|edge|hair|stroke)$")
TEXT = re.compile(r"^color$|^(ink|dim|mut|muted|txt|text|fg)$")
# The declaration a hex sits in, read backwards from the hex to the nearest
# boundary. A stylesheet declaration ends at `;` or `}`; one inside a
# `style="..."` attribute ends at `;` or the quote.
PROP = re.compile(r"\s*(--)?([-a-zA-Z]+)\s*:[^:]*$")


def _role_at(text, i):
    """fill | edge | text, for the hex starting at index i."""
    seg = text[max(0, i - 240):i]
    cut = max(seg.rfind(";"), seg.rfind("{"), seg.rfind("}"),
              seg.rfind('"'), seg.rfind("'"), seg.rfind(">"))
    m = PROP.match(seg[cut + 1:])
    if not m:
        # A hex outside a declaration - a comment, a selector, an SVG
        # attribute - reads as a fill, which is what an unqualified colour
        # in this repository has always meant.
        return "fill"
    p = m.group(2).lower()
    if EDGE.search(p):
        return "edge"
    if TEXT.search(p):
        return "text"
    return "fill"


def conform(text):
    """Rewrite every mapped colour. Returns (text, count).

    Substitutes in place rather than rebuilding declarations, so no
    whitespace moves and a file with no mapped colour is not rewritten.
    """
    out, last, n = [], 0, 0
    for m in KEYS.finditer(text):
        tgt = MAP[m.group(1).upper()]
        if tgt is None:
            tgt = BY_ROLE[_role_at(text, m.start())]
        out.append(text[last:m.start()])
        out.append(tgt)
        last = m.end()
        n += 1
    out.append(text[last:])
    return "".join(out), n


# A page in `_dev/` that eight builders copy their chrome from. See "THE
# TEMPLATE THAT IS NOT A PAGE".
TEMPLATES = ("_dev/chrome_donor.html",)


def html_files():
    """Every .html the site is built from or built into.

    `_dev/` is skipped except for the templates named above - a builder's
    donor is in scope precisely because its bytes end up on real pages.
    """
    out = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs
                   if d not in ("_dev", "_to_delete", ".git", "node_modules")]
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(root, f), SITE))
    out += [t for t in TEMPLATES if os.path.exists(os.path.join(SITE, t))]
    return sorted(out)


def in_scope(rel):
    return os.path.basename(rel) not in NOCOLOUR


def main():
    # --------------------------------------------------- loop-free, or bust
    bad = 0
    for k, v in MAP.items():
        if v in MAP:
            print("GUARD %s -> %s, and %s is itself a key" % (k, v, v))
            bad += 1
    if bad:
        sys.exit("%d cyclic mapping(s) - the pass would not be idempotent"
                 % bad)

    # ------------------------------------------------------- the stylesheets
    remap, swapped, sheets = {}, 0, 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        path = os.path.join(CSSDIR, fn)
        body = open(path, encoding="utf-8").read()
        fixed, n = conform(body)
        if not n:
            continue
        sheets += 1
        swapped += n
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            # Content-addressed: the name is the hash, so it moves.
            new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(fixed)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d colour(s))" % (fn[:-4], new, n))
        else:
            open(path, "w", encoding="utf-8").write(fixed)
            print("  css/%-22s in place    (%d colour(s))" % (fn, n))

    # ---------------------------------------------------------- the pages
    touched, inline = 0, 0
    for rel in html_files():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        # A renamed sheet must not 404 anywhere, mockups included.
        if remap:
            s = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)

        if in_scope(rel):
            def block(m):
                nonlocal inline
                fixed, n = conform(m.group(2))
                inline += n
                return m.group(1) + fixed + m.group(3)
            s = re.sub(r"(<style\b[^>]*>)([\s\S]*?)(</style>)", block, s)

            def attr(m):
                nonlocal inline
                fixed, n = conform(m.group(1))
                inline += n
                return 'style="%s"' % fixed
            s = re.sub(r'style="([^"]*)"', attr, s)

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    print("%d colour(s) in %d stylesheet(s), %d in page markup, %d page(s) "
          "rewritten" % (swapped, sheets, inline, touched))

    # ----------------------------------------- retire the superseded sheets
    if remap:
        binned = os.path.join(SITE, "_to_delete")
        os.makedirs(binned, exist_ok=True)
        allhtml = {rel: open(os.path.join(SITE, rel), encoding="utf-8").read()
                   for rel in html_files()}
        for old in sorted(remap):
            if any("%s.css" % old in s for s in allhtml.values()):
                print("  css/%s.css still referenced - left in place" % old)
                continue
            try:
                os.replace(os.path.join(CSSDIR, "%s.css" % old),
                           os.path.join(binned, "pre-palette-%s.css" % old))
            except OSError as e:
                print("  could not move css/%s.css (%s)" % (old, e))

    # ------------------------------------------------------------- guards
    bad = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        b = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()
        _f, n = conform(b)
        if n:
            print("GUARD css/%s: %d mapped colour(s) survived" % (fn, n))
            bad += 1
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
            if h != fn[:-4]:
                print("GUARD css/%s: named for %s, not its own contents (%s)"
                      % (fn, fn[:-4], h))
                bad += 1
    for rel in html_files():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css, which is not there"
                      % (rel, h))
                bad += 1
        if not in_scope(rel):
            continue
        for m in re.finditer(r"<style\b[^>]*>([\s\S]*?)</style>", s):
            _f, n = conform(m.group(1))
            if n:
                print("GUARD %s: a <style> block kept %d mapped colour(s)"
                      % (rel, n))
                bad += 1
                break
        for m in re.finditer(r'style="([^"]*)"', s):
            _f, n = conform(m.group(1))
            if n:
                print("GUARD %s: style=%r kept a mapped colour"
                      % (rel, m.group(1)[:60]))
                bad += 1
                break

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d mapped colour(s) remain nowhere in scope, every "
          "hashed sheet is named for its contents, every link resolves"
          % len(MAP))


if __name__ == "__main__":
    main()
