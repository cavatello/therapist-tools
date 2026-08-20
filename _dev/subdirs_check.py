#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every pass must agree on which directories the site has.

WHY THIS EXISTS

Forty passes in `_dev/` each carry their own copy of

    SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

and walk the site root plus those directories. A new top-level directory is
therefore invisible to every one of them until forty files are edited - no
chrome, no nav, no analytics, no CSS extraction, and absent from the sitemap
because `discovery.py` carries a copy too.

The failure is silent in the worst possible way. The pages build. They render
unstyled. And every guard still reports clean, because each guard checks its
own pass and nothing checked the set of directories. That is exactly what
happened when `/for/` was added, and it is why this file exists.

WHAT IT DOES

Reads the literal out of every pass that declares one and fails if they are
not identical, or if any names a directory that is not on disk, or if a real
top-level directory of pages is missing from the list. It writes nothing.

The right fix is one shared definition that the others import. This is the
cheap version of that: it cannot stop the copies drifting, but it can stop a
build shipping while they have.
"""
import ast, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

# Directories that hold no published pages at all: build inputs, research,
# stylesheets, this folder.
IGNORE = {"mock", "css", "js", "node_modules", "RESEARCH", "_to_delete",
          "_dev", "_ops", "_publish", "img", "assets"}

# `ops/` and `hours/` hold working documents, not published pages, and the
# passes are right to skip them. That exemption is NOT a list of names, and it
# deliberately is not: a hardcoded name is how a genuinely published directory
# gets waved through by somebody in a hurry. A directory is exempt only if it
# can prove it - every page in it carries a robots noindex, and none of them
# is in the sitemap. Publish one indexable page into `ops/` and this check
# starts failing again, which is the correct behavior.


def is_working_dir(path, sitemap):
    pages = [x for x in os.listdir(path) if x.endswith(".html")]
    if not pages:
        return False
    for x in pages:
        head = open(os.path.join(path, x), encoding="utf-8",
                    errors="replace").read(4000)
        m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*>', head, re.I)
        if not m or "noindex" not in m.group(0).lower():
            return False
        if "%s/%s" % (os.path.basename(path), x) in sitemap:
            return False
    return True

PAT = re.compile(r"^SUBDIRS\s*=\s*(\([^)]*\))", re.M)


def main():
    print("SUBDIRS agreement")
    found = {}
    for f in sorted(os.listdir(HERE)):
        if not f.endswith(".py") or f == os.path.basename(__file__):
            continue
        m = PAT.search(open(os.path.join(HERE, f), encoding="utf-8").read())
        if m:
            try:
                found[f] = tuple(ast.literal_eval(m.group(1)))
            except Exception:
                found[f] = ("UNPARSEABLE",)

    if not found:
        sys.exit("no pass declares SUBDIRS - this check is looking in the "
                 "wrong place and would pass forever")

    variants = {}
    for f, v in found.items():
        variants.setdefault(v, []).append(f)

    bad = 0
    if len(variants) > 1:
        print("GUARD: %d different SUBDIRS in %d files:" % (len(variants),
                                                            len(found)))
        for v, files in sorted(variants.items(), key=lambda kv: -len(kv[1])):
            print("   %-58s %d file(s): %s"
                  % (", ".join(v), len(files),
                     ", ".join(sorted(files)[:4])))
        bad += 1

    canon = max(variants, key=lambda v: len(variants[v]))
    for d in canon:
        if not os.path.isdir(os.path.join(SITE, d)):
            print("GUARD: SUBDIRS names %r, which is not a directory" % d)
            bad += 1

    # And the other direction - a directory of pages that no pass can see.
    sm = os.path.join(SITE, "sitemap.xml")
    sitemap = (open(sm, encoding="utf-8").read()
               if os.path.exists(sm) else "")
    for d in sorted(os.listdir(SITE)):
        p = os.path.join(SITE, d)
        if not os.path.isdir(p) or d.startswith(".") or d in IGNORE:
            continue
        if d in canon:
            continue
        html = [x for x in os.listdir(p) if x.endswith(".html")]
        if not html:
            continue
        if is_working_dir(p, sitemap):
            print("  NOTE: %s/ holds %d working document(s) - noindex, absent "
                  "from the sitemap - and is correctly outside the passes"
                  % (d, len(html)))
            continue
        print("GUARD: %s/ holds %d page(s) and is not in SUBDIRS, so every "
              "pass skips it" % (d, len(html)))
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  %d pass(es) agree on: %s" % (len(found), ", ".join(canon)))
    print("  guards clean - every directory in the list exists, and every "
          "directory of pages is in the list")


if __name__ == "__main__":
    main()
