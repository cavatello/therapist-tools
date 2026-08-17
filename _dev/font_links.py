#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A page that asks for a typeface must also load it.

WHAT WAS WRONG

`rates.html` sets its body serif with

    font-family:'Newsreader',Georgia,serif

and loads, from Google Fonts, exactly three families: Fraunces, Inter and
Bricolage Grotesque. So the essay's serif has never once rendered in
Newsreader for any reader. It renders in Georgia. Its figures, set
`font-family:'IBM Plex Mono',monospace`, render in whatever the operating
system calls monospace.

Nothing failed. No console error, no layout break, no contrast finding -
the page simply ships in faces nobody chose, and the only symptom is that
it does not look like the rest of the site. Which is the report that
started this work.

`_dev/type_census.py` finds this class by pairing two things no single-file
check ever pairs: what a page's CSS ASKS for, and what the page's <link>s
actually LOAD. This pass closes the gap it finds.

THE PRIMARY-POSITION RULE

Only the FIRST real face in a stack is a request. `Archivo` is named on 240
pages and loaded on almost none of them, and that is correct: every one of
those declarations reads `'Bricolage Grotesque','Archivo',Inter,...`, so
Archivo sits behind a face that does load and will never be reached. Adding
Archivo to 240 font URLs would download a webfont that cannot render.

A face at the head of its stack is different. If it is not loaded, the
fallback IS what ships.

HOW IT FIXES

By rewriting the `family=` list of the page's existing Google Fonts <link>,
not by adding a second link - two stylesheet requests to the same host for
the same purpose is how a page ends up loading nine faces. Axis and weight
syntax comes from WEIGHTS below, one entry per house face, matching the
weights the rest of the site already requests.

A page with a primary face and no Google Fonts link at all is REPORTED, not
patched: it either wants a link this pass should not invent, or it wants the
declaration removed, and those are different decisions. `tools.html` is
that case, and it is the right answer for it - see `build_redirect.py`,
which reduces it to a redirect stub with no faces at all.

Idempotent: a face present in the family list is not added again.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
# Mockups pick their own faces on purpose.
SKIP = {"tycoon.html", "concepts.html"}

# The axis and weight syntax for each face this pass may add, copied from
# the URL the other 249 pages already use so a page does not end up asking
# for a different cut of the same family.
WEIGHTS = {
    "newsreader": "Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;"
                  "0,6..72,600;1,6..72,400",
    "ibm plex mono": "IBM+Plex+Mono:wght@400;500;600",
    "inter": "Inter:wght@400;500;600;700",
    "fraunces": "Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700",
    "bricolage grotesque": "Bricolage+Grotesque:opsz,wght@12..96,600;"
                           "12..96,700;12..96,800",
}
GENERIC = {"system-ui", "sans-serif", "serif", "monospace", "ui-monospace",
           "ui-sans-serif", "ui-serif", "cursive", "fantasy", "inherit",
           "initial", "unset", "georgia", "arial", "helvetica",
           "helvetica neue", "times", "times new roman", "courier",
           "courier new", "segoe ui", "roboto", "menlo", "monaco",
           "consolas", "liberation mono", "sf mono", "sfmono-regular",
           "apple color emoji", "-apple-system", "blinkmacsystemfont",
           "emoji", "noto color emoji", "segoe ui emoji", "segoe ui symbol",
           "arial narrow", "cambria", "palatino", "verdana", "tahoma"}

FACE = re.compile(r"font-family\s*:\s*([^;}]+)")
LINK = re.compile(r'(<link[^>]*href=")(https://fonts\.googleapis\.com/css2\?)'
                  r'([^"]*)(")')


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def primary_faces(text):
    """The first real face of every stack. See THE PRIMARY-POSITION RULE."""
    out = set()
    for m in FACE.finditer(text):
        for part in m.group(1).split(","):
            name = re.sub(r'[\\"\']', "", part)
            name = re.sub(r"!\s*important", "", name).strip().lower()
            if not name or name.startswith("var("):
                continue
            if name not in GENERIC:
                out.add(name)
            break
    return out


def main():
    sheet = {}
    for fn in sorted(os.listdir(CSSDIR)):
        if fn.endswith(".css"):
            sheet[fn] = open(os.path.join(CSSDIR, fn), encoding="utf-8").read()

    fixed, reported, unknown = 0, [], []
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        p = os.path.join(SITE, rel)
        html = open(p, encoding="utf-8").read()
        blob = html + "\n" + "\n".join(
            sheet[n] for n in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)',
                                         html) if n in sheet)
        want = primary_faces(blob)
        links = LINK.findall(html)
        if not links:
            if want:
                reported.append((rel, sorted(want)))
            continue

        # Everything any of this page's font links already carries.
        have = set()
        for _a, _b, query, _d in links:
            for fam in re.findall(r"family=([^&:]+)", query):
                have.add(fam.replace("+", " ").strip().lower())

        missing = sorted(f for f in want - have)
        addable = [f for f in missing if f in WEIGHTS]
        for f in missing:
            if f not in WEIGHTS:
                unknown.append((rel, f))
        if not addable:
            continue

        # Append to the FIRST font link only, before any &display=.
        done = [False]

        def one(m):
            if done[0]:
                return m.group(0)
            done[0] = True
            query = m.group(3)
            extra = "".join("&family=" + WEIGHTS[f] for f in addable)
            if "&display=" in query:
                head, tail = query.split("&display=", 1)
                query = head + extra + "&display=" + tail
            else:
                query = query + extra
            return m.group(1) + m.group(2) + query + m.group(4)
        out = LINK.sub(one, html)
        if out != html:
            open(p, "w", encoding="utf-8").write(out)
            fixed += 1
            print("  ok  %-44s +%s" % (rel, ", ".join(addable)))

    if reported:
        print("  no font <link> at all, so not patched here:")
        for rel, want in reported:
            print("      %-40s wants %s" % (rel, ", ".join(want)))
    if unknown:
        print("  a primary face with no entry in WEIGHTS - add one "
              "deliberately:")
        for rel, f in unknown:
            print("      %-40s %s" % (rel, f))

    print("%d page(s) had a primary face they never loaded" % fixed)

    # ------------------------------------------------------------- guard
    bad = 0
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        html = open(os.path.join(SITE, rel), encoding="utf-8").read()
        blob = html + "\n" + "\n".join(
            sheet[n] for n in re.findall(r'href="(?:\.\./)?css/([^"?]+\.css)',
                                         html) if n in sheet)
        have = set()
        for _a, _b, query, _d in LINK.findall(html):
            for fam in re.findall(r"family=([^&:]+)", query):
                have.add(fam.replace("+", " ").strip().lower())
        if not have:
            continue          # reported above; a stub is allowed no faces
        for f in sorted(primary_faces(blob) - have):
            if f in WEIGHTS:
                print("GUARD %s: sets %s first and never loads it" % (rel, f))
                bad += 1
    if bad:
        sys.exit("%d page(s) still render a primary face as a fallback" % bad)
    print("guard clean - every page that loads faces loads every face it "
          "sets at the head of a stack")


if __name__ == "__main__":
    main()
