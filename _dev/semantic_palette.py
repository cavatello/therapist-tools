#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One red, one amber, one green - instead of thirty-eight near-misses.

WHAT WAS LEFT

`palette_conform.py` collapsed 113 neutral colours onto the twelve tokens
they were approximating, and deliberately stopped at the hue boundary. Its
own docstring says why: *"the reds, the verdict green, the amber ... are
semantic, and a decision about them is a decision about the design."*

That was the right place to stop then and it is the wrong place to stop
now, because the census shows the semantic colours have exactly the same
disease as the neutrals did:

    red      18 colours, 91 uses.  #B5483F (38), then #9C3F37, #9C3E36,
             #8E3A32, #8E3A33, #8A3730, #8A3B33, #8A4038, #7E3630, #7E2F28,
             #7A3A34, #7A2C27, #A8422F, #8E4B45, #A25A52, and three more.
             Fifteen of those are within a few units of one another. Nobody
             chose fifteen reds.
    amber    #C98B4B (22), #B08430 (11), #8A6A2E (12), #8A6A2A (6),
             #B98F1F, #B5843F, #946C28
    green    #3F9577 (25) plus eight dark greens that are simply --deep and
             --pine spelled slightly wrong, and six mints that are the
             on-dark text colour spelled slightly wrong

The DESIGN question - should this site have a verdict colour system at all,
and should red mean "costly" or "wrong"? - is still open and is not
answered here. This pass answers the CONFORMANCE question underneath it,
which has only one sane answer: whatever the system turns out to be, it is
not fifteen reds.

ROLE, AGAIN, BECAUSE COLOUR ALONE KEEPS BEING WRONG

The third time in this repository. `palette_conform.py` learned it on the
pale tans (one hex, 102 backgrounds, 85 borders, 23 colours), and the same
split applies here, for a reason that is arithmetic rather than taste:

    #B5483F on white is 5.30:1 and on --paper 4.96:1 - it clears the floor
    with very little room. Every other red in the family is DARKER. So
    mapping them all onto #B5483F would move fifteen colours in the one
    direction that costs contrast.

So the red canonical is split by job. A bar, a border or a chip takes
`#B5483F`, the established accent. Letters take `#9C3F37`, which is 6.60:1
on white and 6.19:1 on paper - the darker end of the family, so text can
only get more legible, never less.

The amber family goes the same way for the same reason: `#C98B4B` reads
2.89:1 on white and is fine as a rule and hopeless as a word, which is why
`token_floor.py` already swaps it in text contexts. Here the whole family
lands on `#8A6516` for text (5.31:1, sanctioned) and `#C98B4B` for fills.

The pale tints - the surfaces under a warning - collapse to two: one edge
and one fill, both carrying ink at better than 8:1.

NOT IN SCOPE

`practice-simulator.html`, `tycoon.html`, `concepts.html`. The blue band on
`therapist-working-remotely-california.html` is one colour used once and is
left alone: a family of one is not drift.

Idempotent. Guarded: no key survives in scope, every hashed sheet is named
for its contents, and `_dev/_viewports.mjs` is the empirical check across
all five widths.
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
SKIP = {"practice-simulator.html", "tycoon.html", "concepts.html"}
TEMPLATES = ("_dev/chrome_donor.html",)

# family -> {role: canonical}. `text` is used where the declaration paints
# letters, `edge` on borders/outlines/shadows, `fill` everywhere else.
BY_ROLE = {
    "red":   {"text": "#9C3F37", "edge": "#B5483F", "fill": "#B5483F"},
    "tint":  {"text": "#9C3F37", "edge": "#E4B7B2", "fill": "#FBEFEC"},
    "amber": {"text": "#8A6516", "edge": "#C98B4B", "fill": "#C98B4B"},
    "green": {"text": "#2C6350", "edge": "#2C6350", "fill": "#2C6350"},
    "mint":  {"text": "#84AC99", "edge": "#C6DBD1", "fill": "#C6DBD1"},
}
FAMILY = {}
for _f, _keys in [
    # the mid and dark reds
    ("red", ("#9C3F37", "#9C3E36", "#8E4B45", "#8E3A32", "#8E3A33",
             "#8A3730", "#8A4038", "#8A3B33", "#7E3630", "#7E2F28",
             "#7A3A34", "#7A2C27", "#A8422F", "#A25A52", "#5B3833",
             "#5A423F", "#5A3B37")),
    # the pale red surfaces under a warning
    ("tint", ("#F0A79E", "#EBC7BE", "#E4B7B2", "#EBCFCC", "#E8CFCB",
              "#F3E0DE", "#FBEDEC", "#FBF4F3", "#FCF1F0", "#FBF0EF",
              "#F7EDEB", "#FDF4F2", "#FBEDEA", "#FCF1EF", "#FBF1F0",
              "#FBEFEC")),
    # the ambers that are not already a token
    ("amber", ("#B08430", "#8A6A2E", "#8A6A2A", "#B98F1F", "#B5843F",
               "#946C28", "#D8AC63", "#C99C46", "#8A5B22", "#8A5A26",
               "#7A5418", "#6B5321", "#6B5220", "#6B4A18", "#5E4818",
               "#7F5A1F", "#4A3A1E", "#3A2A08", "#8A7B58", "#7A6B4A")),
    # dark greens that are --pine and --deep spelled wrong
    ("green", ("#3F9577", "#48A382", "#5EC49B", "#245244", "#1F4A3B",
               "#1F4C3C", "#2C4A3B", "#2F7259", "#3C7A64", "#245046",
               "#2C4227", "#2F6E56", "#25584A", "#20614B", "#2F5E4E")),
    # mints that are the on-dark text colour spelled wrong
    ("mint", ("#9FC4B4", "#A9CFBC", "#9DB8AA", "#9DBFB1", "#6E9587",
              "#7FDDB6", "#8FD9B6", "#9FE0C4", "#B9CFC2", "#AEC6BB",
              "#B7CFC3", "#BFD3C7", "#C8D2CB", "#C9DED5", "#BEDDD0")),
]:
    for _k in _keys:
        FAMILY[_k] = _f

KEYS = re.compile("(" + "|".join(re.escape(k) for k in sorted(FAMILY)) + r")\b",
                  re.IGNORECASE)
EDGE = re.compile(r"^(border|outline)|shadow|^(line|rule|edge|hair|stroke)$")
TEXT = re.compile(r"^color$|^(ink|dim|mut|muted|txt|text|fg)$")
PROP = re.compile(r"\s*(--)?([-a-zA-Z]+)\s*:[^:]*$")
SVGATTR = re.compile(r'\b(fill|stroke|stop-color|flood-color|lighting-color)'
                     r'="([^"]*)"')
LINKED = re.compile(r'href="((?:\.\./)*)css/([0-9a-f]{12})\.css"')


def _role_at(text, i):
    seg = text[max(0, i - 240):i]
    cut = max(seg.rfind(";"), seg.rfind("{"), seg.rfind("}"),
              seg.rfind('"'), seg.rfind("'"), seg.rfind(">"))
    m = PROP.match(seg[cut + 1:])
    if not m:
        return "fill"
    p = m.group(2).lower()
    if EDGE.search(p):
        return "edge"
    if TEXT.search(p):
        return "text"
    return "fill"


def conform(text, force=None):
    out, last, n = [], 0, 0
    for m in KEYS.finditer(text):
        key = m.group(1).upper()
        fam = FAMILY[key]
        role = force or _role_at(text, m.start())
        tgt = BY_ROLE[fam][role]
        if tgt.upper() == key:
            continue
        out.append(text[last:m.start()])
        out.append(tgt)
        last = m.end()
        n += 1
    out.append(text[last:])
    return "".join(out), n


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def html_files():
    out = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs
                   if d not in ("_dev", "_to_delete", ".git", "node_modules")]
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(root, f), SITE))
    out += [t for t in TEMPLATES if os.path.exists(os.path.join(SITE, t))]
    return sorted(out)


def main():
    # a canonical must not itself be a key, or the pass never settles
    bad = 0
    for fam, roles in BY_ROLE.items():
        for role, tgt in roles.items():
            if tgt.upper() in FAMILY and FAMILY[tgt.upper()] == fam:
                if BY_ROLE[fam][role].upper() != tgt.upper():
                    print("GUARD %s/%s -> %s is a key of its own family"
                          % (fam, role, tgt))
                    bad += 1
    if bad:
        sys.exit("%d cyclic mapping(s)" % bad)

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
            new = hashlib.sha1(fixed.encode("utf-8")).hexdigest()[:12]
            open(os.path.join(CSSDIR, "%s.css" % new), "w",
                 encoding="utf-8").write(fixed)
            remap[fn[:-4]] = new
            print("  css/%s -> %s  (%d colour(s))" % (fn[:-4], new, n))
        else:
            open(path, "w", encoding="utf-8").write(fixed)
            print("  css/%-22s in place    (%d colour(s))" % (fn, n))

    inline, touched = 0, 0
    for rel in html_files():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        if remap:
            s = LINKED.sub(
                lambda m: 'href="%scss/%s.css"'
                          % (m.group(1), remap.get(m.group(2), m.group(2))), s)
        if os.path.basename(rel) not in SKIP:
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

            def svg(m):
                nonlocal inline
                role = "edge" if m.group(1) == "stroke" else "fill"
                fixed, n = conform(m.group(2), force=role)
                inline += n
                return '%s="%s"' % (m.group(1), fixed)
            s = SVGATTR.sub(svg, s)
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            touched += 1

    print("%d colour(s) in %d stylesheet(s), %d in page markup, %d page(s) "
          "rewritten" % (swapped, sheets, inline, touched))

    if remap:
        binned = os.path.join(SITE, "_to_delete")
        os.makedirs(binned, exist_ok=True)
        current = {rel: open(os.path.join(SITE, rel), encoding="utf-8").read()
                   for rel in html_files()}
        for old in sorted(remap):
            if any("%s.css" % old in s for s in current.values()):
                continue
            try:
                os.replace(os.path.join(CSSDIR, "%s.css" % old),
                           os.path.join(binned, "pre-semantic-%s.css" % old))
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
            print("GUARD css/%s: %d colour(s) survived" % (fn, n))
            bad += 1
        if re.fullmatch(r"[0-9a-f]{12}", fn[:-4]):
            h = hashlib.sha1(b.encode("utf-8")).hexdigest()[:12]
            if h != fn[:-4]:
                print("GUARD css/%s: not named for its contents (%s)"
                      % (fn, h))
                bad += 1
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        for _u, h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css, which is not there"
                      % (rel, h))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - the semantic families are one red, one amber and "
          "one green, split by whether the declaration paints letters")


if __name__ == "__main__":
    main()
