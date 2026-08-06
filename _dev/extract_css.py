#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lift the stylesheets that every page carries a private copy of into shared
files, and leave the ones that are genuinely per-page inline.

WHY. Every page on this site is built by lifting the chrome - links, styles,
header, footer, nav script - out of a published page. That is deliberate and it
is why the header cannot drift. But it means the ~45 KB of shared CSS is written
into all seventy-nine documents, and the site was 12 MB of which roughly 3.5 MB
was the same bytes over and over. The reader pays for it on every single
navigation, because an inline <style> cannot be cached; the deploy pays for it
too, and this project has already had one Pages deploy time out on payload.

HOW, AND WHY IT IS SAFE. CSS at equal specificity is decided by source order,
so the only safe transformation is one that changes nothing about order. Each
<style> block is therefore replaced IN PLACE by a <link> to a file containing
exactly its bytes - not merged, not reordered, not concatenated. A page with
four style blocks ends up with four links in the same four positions. Blocks are
deduplicated by content hash across pages, which is where the saving comes from.

A block is only extracted if it appears on MIN_PAGES pages. A one-off block -
the infographics on the directory, the ledger on a training page - stays inline,
because a separate request for 3 KB used once is worse than the inline copy.

Idempotent: a page whose blocks are already links has nothing left to match.

GUARDS. The rendered stylesheet text of every page must be byte-identical before
and after, in the same order. That is checked here by reassembling each page's
CSS from its links and comparing; it is checked again in a real browser by
verify.mjs, which is the one that matters.
"""
import os, re, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
MIN_PAGES = 4

STYLE = re.compile(r"[ \t]*<style>([\s\S]*?)</style>\n?")
LINKED = re.compile(r'<link rel="stylesheet" href="css/([0-9a-f]{12})\.css">')


def pages():
    return sorted(f for f in os.listdir(SITE)
                  if f.endswith(".html") and not f.startswith("."))


def main():
    docs = {}
    for f in pages():
        docs[f] = open(os.path.join(SITE, f), encoding="utf-8").read()

    # How many distinct pages carry each block?
    seen = {}
    for f, s in docs.items():
        for body in set(m.group(1) for m in STYLE.finditer(s)):
            h = hashlib.sha1(body.encode("utf-8")).hexdigest()[:12]
            seen.setdefault(h, [body, set()])[1].add(f)

    shared = {h: v[0] for h, v in seen.items() if len(v[1]) >= MIN_PAGES}
    if not shared:
        print("extract_css: nothing shared by %d+ pages" % MIN_PAGES)
        return

    os.makedirs(CSSDIR, exist_ok=True)
    for h, body in shared.items():
        open(os.path.join(CSSDIR, "%s.css" % h), "w", encoding="utf-8").write(body)

    def sub(m):
        h = hashlib.sha1(m.group(1).encode("utf-8")).hexdigest()[:12]
        if h in shared:
            return '<link rel="stylesheet" href="css/%s.css">\n' % h
        return m.group(0)

    saved = 0
    changed = 0
    for f, s in docs.items():
        out = STYLE.sub(sub, s)
        if out == s:
            continue
        # ---- the only guard that matters: same CSS, same order
        def expand(doc):
            parts = []
            for m in re.finditer(r"<style>([\s\S]*?)</style>|" + LINKED.pattern, doc):
                if m.group(1) is not None:
                    parts.append(m.group(1))
                else:
                    parts.append(open(os.path.join(CSSDIR, "%s.css" % m.group(2)),
                                      encoding="utf-8").read())
            return parts
        if expand(s) != expand(out):
            sys.exit("extract_css: %s would change its CSS or its order" % f)
        if out.count("<style") + out.count('href="css/') \
           != s.count("<style") + s.count('href="css/'):
            sys.exit("extract_css: %s lost or gained a stylesheet" % f)
        saved += len(s) - len(out)
        changed += 1
        open(os.path.join(SITE, f), "w", encoding="utf-8").write(out)

    shared_bytes = sum(len(b.encode("utf-8")) for b in shared.values())
    print("%d block(s) shared by %d+ pages -> css/ (%.0f KB)"
          % (len(shared), MIN_PAGES, shared_bytes / 1024))
    print("%d page(s) rewritten, %.2f MB removed from the HTML"
          % (changed, saved / 1e6))

    # Nothing may point at a stylesheet that was not written.
    missing = set()
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        for h in LINKED.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                missing.add((f, h))
    if missing:
        sys.exit("extract_css: %d dangling stylesheet link(s): %r"
                 % (len(missing), sorted(missing)[:3]))
    print("guards clean")


if __name__ == "__main__":
    main()
