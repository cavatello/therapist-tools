#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check every OUTBOUND link on the site still resolves.

_dev/linkcheck.py checks links BETWEEN pages here. Nothing checked links
leaving the site — and resources.html alone ships 72 of them, every one a
promise that it was real on the day it shipped. External links rot: a fee PDF
moves, a payer restructures its provider section, an agency redesigns.

WHY 403 IS NOT A FAILURE. Eleven of the 72 return 403 to a datacenter IP while
serving fine to a browser — hhs.gov, ssa.gov, bls.gov, naswca.org, headway.co.
An audit that reports those as broken every run gets muted, and a muted audit
catches nothing. They are listed below and a 403 from them passes; a 403 from
anywhere else is reported, because it may be real. 404, 410, DNS failures and
timeouts always fail.

Usage:  python3 _dev/linkcheck_external.py [dir]
        python3 _dev/linkcheck_external.py --page resources.html
"""
import os, re, sys, ssl, socket, time
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SKIP_FILES = {"tycoon.html", "concepts.html"}

# Serve fine in a browser, refuse datacenter IPs. Verified by hand 5 Aug 2026.
BLOCKS_ROBOTS = {
    "www.hhs.gov", "hhs.gov",
    "www.ssa.gov", "ssa.gov",
    "www.bls.gov", "bls.gov",
    "www.naswca.org", "naswca.org",
    "headway.co", "www.headway.co",
    "leginfo.legislature.ca.gov",
    "data.bls.gov",
    # Intermittent: returned 200 to a single request and 403 under a parallel
    # sweep, so it appears to rate-limit rather than block outright. Confirmed
    # live by hand on 5 Aug 2026, prices and all.
    "www.goodtherapy.org", "goodtherapy.org",
}

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def links(dirname, only=None):
    seen = {}
    for f in sorted(os.listdir(dirname)):
        if not f.endswith(".html") or f in SKIP_FILES:
            continue
        if only and f != only:
            continue
        s = open(os.path.join(dirname, f), encoding="utf-8").read()
        # Skip resource hints. <link rel="preconnect" href="https://fonts.
        # googleapis.com"> is a connection warm-up, not a page: the bare origin
        # 404s by design and reporting it as a broken link on 15 pages is
        # exactly the noise that gets an audit ignored.
        s = re.sub(r'<link\b[^>]*rel="(?:preconnect|dns-prefetch|preload|'
                   r'modulepreload)"[^>]*>', "", s)
        for m in re.finditer(r'href="(https?://[^"]+)"', s):
            u = m.group(1).replace("&amp;", "&")
            seen.setdefault(u, set()).add(f)
    return seen


def check(u, _retry=True):
    """One retry on a transport error before reporting.

    cms.gov reset the connection once under a 12-way parallel sweep and
    answered 200 on three consecutive retries a moment later. A checker that
    reports a transient reset as a dead link trains you to ignore it.
    """
    req = urllib.request.Request(u, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*"})
    try:
        r = urllib.request.urlopen(req, timeout=30, context=CTX)
        return u, r.status, ""
    except urllib.error.HTTPError as e:
        return u, e.code, ""
    except (urllib.error.URLError, socket.timeout, ssl.SSLError) as e:
        if _retry:
            time.sleep(2)
            return check(u, _retry=False)
        return u, "ERR", str(getattr(e, "reason", e))[:60]
    except Exception as e:
        if _retry:
            time.sleep(2)
            return check(u, _retry=False)
        return u, "ERR", type(e).__name__


def main():
    only = None
    args = [a for a in sys.argv[1:]]
    if "--page" in args:
        only = args[args.index("--page") + 1]
        args = [a for a in args if a != "--page" and a != only]
    d = args[0] if args else SITE

    found = links(d, only)
    if not found:
        print("no external links found in %s" % d)
        return 0
    print("checking %d unique external links" % len(found))

    with ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(check, found.keys()))

    ok = blocked = bad = 0
    problems = []
    for u, code, note in sorted(results):
        host = re.sub(r"^https?://([^/]+).*$", r"\1", u)
        if code == 200:
            ok += 1
        elif code == 403 and host in BLOCKS_ROBOTS:
            blocked += 1
        else:
            bad += 1
            problems.append((code, u, sorted(found[u]), note))

    for code, u, pages, note in problems:
        print("  [%s] %s" % (code, u[:96]))
        print("        on %s %s" % (", ".join(pages[:3]), note))

    print("\n%d ok  ·  %d blocked-to-robots (expected)  ·  %d PROBLEM"
          % (ok, blocked, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
