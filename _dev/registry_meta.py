#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write each page's library metadata into the page itself.

THE PROBLEM THIS SOLVES. Every listing on this site is generated from
mock/library/registry.json - the hub, the five topic hubs, the question index,
the calculators index, the up-link block at the foot of every page. That was the
right move, and it removed the O(n) hand-editing that a flat question index
forces.

But it left one hand edit behind, and it is the one that matters: a new page
does not exist to the library until somebody adds a record to registry.json. At
a hundred and twenty pages that is a small tax. At three hundred it is the same
failure the restructure was meant to remove - long-tail pages arrive faster than
records, and the ones nobody remembers to register become orphans reachable only
from the sitemap.

THE FIX, IN TWO PASSES. This one writes the metadata INTO each page as
<meta name="ts:*"> tags. registry_sync.py then reads them back out and rebuilds
the registry from the pages. After that the page is the source of truth: an
author (or a builder) writes the meta, and the page joins the library on the
next build with no central file to edit.

This pass is the backfill half. It seeds the meta from the registry as it stands
today, so nothing is lost in the handover. Once a page carries its own meta,
sync treats the page as authoritative and this pass leaves it alone unless the
page has drifted from a record that was edited by hand.

WHY META TAGS RATHER THAN A SIDECAR FILE OR FRONT MATTER. A sidecar is one more
thing to keep in step with the page, which is the problem restated. Front matter
would mean Jekyll processing every page, and none of this site's HTML has it -
Jekyll currently copies each file verbatim, which is why the build is fast and
predictable. A meta tag travels with the document, survives every post-pass,
costs about 200 bytes, and can be read by anything that can read HTML.

The `ts:` prefix is deliberate: not `og:`, not `twitter:`, not `article:`. Those
namespaces belong to consumers who will interpret them, and putting internal
build state in them would leak site plumbing into a Facebook card.

Idempotent: a page whose meta already matches is untouched.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARK = "<!-- ts:meta -->"
END = "<!-- /ts:meta -->"

# field -> (meta name, how to serialise). Order is fixed so a rewrite produces
# byte-identical output and the pass stays a no-op on a second run.
FIELDS = [
    ("topic", "ts:topic", str),
    ("format", "ts:format", str),
    ("question", "ts:question", str),
    ("outcome", "ts:outcome", str),
    ("number", "ts:number", str),
    ("weight", "ts:weight", lambda v: str(int(v))),
    ("leaf", "ts:leaf", lambda v: "true" if v else "false"),
    ("stale", "ts:stale", lambda v: "true" if v else "false"),
    ("skip", "ts:skip", lambda v: "true" if v else "false"),
]


def esc(x):
    return html.escape(str(x), quote=True)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def block(rec):
    lines = [MARK]
    for key, name, ser in FIELDS:
        v = rec.get(key)
        if v is None or v == "":
            continue
        if key in ("leaf", "stale", "skip") and not v:
            continue          # absent means false; do not write noise
        lines.append('<meta name="%s" content="%s">' % (name, esc(ser(v))))
    lines.append(END)
    return "\n".join(lines) + "\n"


def read_meta(doc):
    out = {}
    for m in re.finditer(r'<meta name="ts:([a-z]+)" content="([^"]*)">', doc):
        k, v = m.group(1), html.unescape(m.group(2))
        if k in ("leaf", "stale", "skip"):
            out[k] = (v == "true")
        elif k == "weight":
            out[k] = int(v)
        else:
            out[k] = v
    return out


def main():
    if not os.path.exists(REGISTRY):
        sys.exit("registry_meta: %s missing" % REGISTRY)
    REG = json.load(open(REGISTRY, encoding="utf-8"))
    by = {p["file"]: p for p in REG["pages"]}

    wrote = already = nometa = 0
    unregistered = []
    for f in pages():
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        rec = by.get(f)
        if not rec:
            # A page with no record and no meta is invisible to the library.
            # Naming it is the whole point - silence here is how orphans happen.
            if MARK not in s:
                unregistered.append(f)
                nometa += 1
            continue
        want = block(rec)
        cur = re.search(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", s)
        if cur and cur.group(0) == want:
            already += 1
            continue
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?", "", s)
        # Immediately after the canonical link if there is one, else after the
        # charset declaration - both are inside <head> on every page here.
        anchor = re.search(r'<link rel="canonical"[^>]*>\n?', s)
        if anchor:
            s = s[:anchor.end()] + want + s[anchor.end():]
        else:
            anchor = re.search(r"<meta charset=[^>]*>\n?", s)
            if not anchor:
                unregistered.append(f + " (no <head> anchor)")
                continue
            s = s[:anchor.end()] + want + s[anchor.end():]
        open(path, "w", encoding="utf-8").write(s)
        wrote += 1

    print("meta written    %d" % wrote)
    print("already correct %d" % already)
    if unregistered:
        print("NOT IN THE LIBRARY (%d) - neither a record nor page meta:" % len(unregistered))
        for f in unregistered[:12]:
            print("   %s" % f)

    # ---- guards
    bad = 0
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        n = s.count(MARK)
        if n > 1:
            print("GUARD %s: %d meta blocks - the pass appended" % (f, n))
            bad += 1
        if MARK in s and s.count(END) != 1:
            print("GUARD %s: unterminated meta block" % f)
            bad += 1
        if MARK not in s:
            continue
        if s.index(MARK) > s.index("</head>"):
            print("GUARD %s: meta block is outside <head>" % f)
            bad += 1
        got = read_meta(s)
        rec = by.get(f)
        if rec:
            for key, _name, _ser in FIELDS:
                v = rec.get(key)
                if key in ("leaf", "stale", "skip"):
                    if bool(v) != bool(got.get(key)):
                        print("GUARD %s: %s is %r on the page, %r in the registry"
                              % (f, key, got.get(key), v))
                        bad += 1
                elif v not in (None, "") and str(got.get(key, "")) != str(v):
                    print("GUARD %s: %s differs between page and registry" % (f, key))
                    bad += 1
        # A page that claims a topic the registry does not define would break
        # every listing that groups by topic.
        if got.get("topic") and got["topic"] not in REG["topics"]:
            print("GUARD %s: unknown topic %r" % (f, got["topic"]))
            bad += 1
    if bad:
        sys.exit("registry_meta: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
