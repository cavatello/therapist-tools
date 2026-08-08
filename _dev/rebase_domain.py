#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the site from cavatello.github.io/therapist-tools to its own domain.

RUN THIS ONCE, AFTER THE DNS RECORDS ARE LIVE AND NOT BEFORE. It checks, and it
refuses to run early - see THE ORDER OF OPERATIONS below for why that guard is
the most important line in the file.

WHAT CHANGES, AND WHY IT IS MORE THAN A FIND-AND-REPLACE

This is a GitHub Pages PROJECT site, so it is served today at
`cavatello.github.io/therapist-tools/`. A custom domain moves it to the root of
that domain: `therapistsupport.org/rates.html`, not
`therapistsupport.org/therapist-tools/rates.html`. The repository path segment
disappears.

Relative links are therefore fine and are not touched - including the `../`
links on the five topic hubs, which still resolve correctly from the root.

What is NOT fine is every ABSOLUTE self-reference, because each one still names
the old host and the old path:

  - sitemap.xml, 130 URLs
  - the canonical tag on every page that has one
  - BreadcrumbList and other structured data emitted by _dev/discovery.py
  - any og: tags carrying an absolute URL
  - robots.txt, which points at the sitemap

A page served from the new domain whose canonical tag names the old one is the
single most reliable way to lose the rankings a migration is supposed to keep.
Google is being told, on every page, that the real version lives somewhere else.
So the canonicals and the DNS have to change in the same push.

THE ORDER OF OPERATIONS, WHICH IS NOT OPTIONAL

  1. Add the A, AAAA and CNAME records at Porkbun.
  2. Wait until the domain actually resolves. This script tests it.
  3. Run this script. It rewrites the URLs, updates the builder constants so
     future rebuilds emit the new domain, and writes the CNAME file last.
  4. Let the auto-publish watcher commit and push.
  5. In the repository: Settings -> Pages, confirm the custom domain is
     detected, then tick Enforce HTTPS once the certificate provisions.

Doing step 3 before step 2 takes the whole site dark. The CNAME file is what
tells GitHub to start redirecting github.io to the custom domain, and if that
domain does not yet resolve there is nowhere for the redirect to land - so the
old URL stops working and the new one does not yet work. That is why the
resolve check below is a hard exit and not a warning.

THE CNAME FILE IS WRITTEN LAST, AND DELIBERATELY

GitHub also creates this file for you when you set the domain in the web UI.
Do not let it. This repository has an auto-publish watcher that commits the
entire working tree fifteen seconds after any change: a CNAME file that exists
on GitHub but not on this disk gets DELETED by the next publish, and the custom
domain silently detaches. Creating it locally first means the watcher pushes it
and GitHub reads the domain from the file, so there is no race to lose.

REVERSIBLE. Run with --revert to put every URL back and remove the CNAME file.
Idempotent either way: a second run reports nothing to do.
"""
import os, re, sys, socket, argparse

OLD_BASE = "https://therapistsupport.org"
OLD_HOST = "cavatello.github.io"

SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

# The builders carry the base as a constant. Updating them here means the next
# rebuild emits the new domain rather than silently reintroducing the old one -
# which is exactly how a migration half-reverts a week later and nobody knows.
BUILDER_GLOBS = [
    "mock/mftguide", "mock/library", "mock/cola", "mock/articles",
    "mock/psychedelics", "mock/affiliates", "mock/amft", "_dev",
]


def resolves(host):
    try:
        socket.getaddrinfo(host, 443)
        return True
    except socket.gaierror:
        return False


def targets(site):
    out = []
    for f in sorted(os.listdir(site)):
        if f.endswith((".html", ".xml", ".txt")):
            out.append(f)
    for d in SUBDIRS:
        p = os.path.join(site, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    for d in BUILDER_GLOBS:
        p = os.path.join(site, d)
        if not os.path.isdir(p):
            continue
        for root, _dirs, files in os.walk(p):
            for f in files:
                if f.endswith((".py", ".json", ".txt")):
                    rel = os.path.relpath(os.path.join(root, f), site)
                    out.append(rel)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", help="e.g. therapistsupport.org")
    ap.add_argument("--site", default=".")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="skip the DNS check. Do not use this.")
    a = ap.parse_args()

    site = os.path.abspath(a.site)
    new_base = "https://" + a.domain

    if not a.revert and not a.force:
        if not resolves(a.domain):
            sys.exit(
                "REFUSING TO RUN.\n\n"
                "  %s does not resolve yet.\n\n"
                "  Running now would write a CNAME file, which makes GitHub\n"
                "  redirect cavatello.github.io to a domain that does not\n"
                "  answer - the old URL stops working and the new one does not\n"
                "  yet work, so the site goes dark.\n\n"
                "  Add the DNS records at Porkbun, wait for them to resolve,\n"
                "  then run this again." % a.domain)
        print("DNS check: %s resolves. Proceeding.\n" % a.domain)

    frm, to = (new_base, OLD_BASE) if a.revert else (OLD_BASE, new_base)

    changed, hits, skipped = 0, 0, []
    for rel in targets(site):
        path = os.path.join(site, rel)
        try:
            s = open(path, encoding="utf-8").read()
        except (IOError, UnicodeDecodeError):
            continue
        n = s.count(frm)
        if not n:
            continue
        # A file the process cannot write must not abort the run. Aborting
        # halfway is the worst outcome available here: some canonicals point at
        # the new domain and some at the old, which is a harder state to reason
        # about than either end. Skip it, name it, keep going, and let the
        # guard at the bottom decide whether the result is publishable.
        try:
            open(path, "w", encoding="utf-8").write(s.replace(frm, to))
        except (IOError, OSError) as e:
            skipped.append("%s (%s)" % (rel, e.__class__.__name__))
            continue
        changed += 1
        hits += n
        print("  %5d  %s" % (n, rel))

    print("\n%d absolute URL(s) rewritten across %d file(s)" % (hits, changed))
    if skipped:
        print("COULD NOT WRITE %d file(s):" % len(skipped))
        for x in skipped:
            print("   " + x)

    # ---- the CNAME file, last, and only on the way forward
    cname = os.path.join(site, "CNAME")
    if a.revert:
        if os.path.exists(cname):
            os.remove(cname)
            print("removed CNAME")
    else:
        want = a.domain + "\n"
        if not os.path.exists(cname) or open(cname).read() != want:
            open(cname, "w").write(want)
            print("wrote CNAME -> %s" % a.domain)
        else:
            print("CNAME already correct")

    # ---- guards
    bad = 0
    if not a.revert:
        # Nothing may still name the old base. A single surviving canonical is
        # a page telling Google the real version is on the old host.
        for rel in targets(site):
            p = os.path.join(site, rel)
            try:
                s = open(p, encoding="utf-8").read()
            except (IOError, UnicodeDecodeError):
                continue
            if OLD_BASE in s:
                if rel.endswith((".html", ".xml", ".txt")):
                    print("GUARD %s: still names the old base" % rel)
                    bad += 1
                else:
                    print("  note: %s still names the old base (builder source, "
                          "not served - fix before the next rebuild)" % rel)
        # The bare host may legitimately survive as a CNAME target in docs, but
        # not inside a canonical or a sitemap entry.
        for rel in [r for r in targets(site) if r.endswith((".html", ".xml"))]:
            s = open(os.path.join(site, rel), encoding="utf-8").read()
            for m in re.finditer(r'(rel="canonical" href="|<loc>)([^"<]+)', s):
                if OLD_HOST in m.group(2):
                    print("GUARD %s: %s still points at the old host"
                          % (rel, m.group(1).strip('<>="rel canonicalhref')))
                    bad += 1
                    break
        if not os.path.exists(cname):
            print("GUARD: no CNAME file - the domain will not attach")
            bad += 1
    if bad:
        sys.exit("\n%d guard failure(s) - do NOT let this publish" % bad)
    print("guards clean")
    print("\nNext: let the watcher publish, then Settings -> Pages and tick "
          "Enforce HTTPS once the certificate is issued.")


if __name__ == "__main__":
    main()
