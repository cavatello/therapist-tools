#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stop routing the whole site through a redirect stub.

nav_consolidate.py repointed the HEADER nav from tools.html to resources.html
and stopped there. A link audit run afterwards found what it had missed:

  header links to tools.html    0   <- consolidated
  FOOTER links to tools.html   18   <- every page on the site
  body links to tools.html      9   <- including five of the tools themselves

So the hub was reachable directly from the top nav and through a zero-delay
meta refresh from everywhere else. It worked - that is what made it easy to
miss - but every reader arriving from a footer or an in-page link paid a
navigation hop, and the canonical URL only won when someone used the nav.

The stub itself is left exactly as it is. It stays as a redirect for anything
already linking to /tools.html from outside the site, and deliberately carries
no noindex (see build_redirect.py). What changes is that nothing INSIDE the
site points at it any more.

Two stale labels go with it. index.html said "Or see all four tools"; there
are seven calculators, and the hub also carries articles and 72 external
references, so the number was wrong in both directions. It is now written
without a count, which stays true as the set grows.

Idempotent: after one run there are no tools.html hrefs left to rewrite.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
STUB = "tools.html"
HUB = "resources.html"

# Label rewrites, applied only inside an <a> that we just repointed. Keyed on
# the exact inner text so a wrong match is impossible rather than unlikely.
LABELS = {
    "Or see all four tools": "Or see every tool",
    "All the tools": "All the tools and reference",
}


def pages():
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html") and f != STUB:
            yield f


def main():
    total_href = total_label = 0
    touched = []
    for f in pages():
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s

        # 1. repoint. Only bare tools.html and tools.html#anchor - never a file
        #    whose name merely ends in "tools.html".
        s, n = re.subn(r'href="' + re.escape(STUB) + r'((?:[#?][^"]*)?)"',
                       'href="' + HUB + r'\1"', s)

        # 2. retitle, but only inside anchors now pointing at the hub
        m_label = 0
        def fix(m):
            nonlocal m_label
            inner = m.group(2)
            plain = re.sub(r"<[^>]+>", "", inner).strip()
            for old, new in LABELS.items():
                # Exact match, not startswith. "All the tools" is a PREFIX of its
                # own replacement "All the tools and reference", so a prefix test
                # re-fires on the second run and yields "...and reference and
                # reference". Idempotence here has to be structural, not a marker.
                if plain == old and new not in inner:
                    m_label += 1
                    return m.group(1) + inner.replace(old, new, 1) + m.group(3)
            return m.group(0)
        s = re.sub(r'(<a[^>]+href="' + re.escape(HUB) + r'[^"]*"[^>]*>)([\s\S]{0,200}?)(</a>)',
                   fix, s)

        if s != before:
            open(path, "w", encoding="utf-8").write(s)
            touched.append((f, n, m_label))
            total_href += n
            total_label += m_label

    for f, n, l in touched:
        print("%-44s %2d href%s%s" % (f, n, "s" if n != 1 else " ",
                                      ", %d label(s)" % l if l else ""))
    print("%d href(s), %d label(s) across %d page(s)"
          % (total_href, total_label, len(touched)))

    # ---- guards
    bad = 0
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        left = re.findall(r'href="' + re.escape(STUB) + r'(?:[#?][^"]*)?"', s)
        if left:
            print("GUARD %s: %d link(s) still point at the stub" % (f, len(left))); bad += 1
        if s.count("<h1") != 1 and f not in ("privacy.html", "terms.html"):
            print("GUARD %s: %d h1" % (f, s.count("<h1"))); bad += 1
    # the stub must survive, and must still send people to the hub
    stub = os.path.join(SITE, STUB)
    if not os.path.exists(stub):
        print("GUARD: the stub was deleted; external links to /tools.html would 404"); bad += 1
    else:
        t = open(stub, encoding="utf-8").read()
        if HUB not in t:
            print("GUARD: the stub no longer points at %s" % HUB); bad += 1
    if re.search(r"all four tools", open(os.path.join(SITE, "index.html"), encoding="utf-8").read()):
        print("GUARD: index.html still claims four tools"); bad += 1
    if bad:
        sys.exit("relink_hub: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
