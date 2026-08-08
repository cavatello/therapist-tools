#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tell Bing, Yandex, Seznam, Naver and Yep that pages changed, the moment they do.

WHY THIS EXISTS. Google is the only engine with a real submission path for this
site, and it is rationed - Search Console's "Request indexing" button has a
daily quota of roughly a dozen URLs, which is nothing against 130 pages. Every
other engine either waits for its own crawler to come round (weeks, for a site
with no inbound links) or accepts IndexNow.

IndexNow needs no account, no OAuth and no verification beyond a key file served
from the site's own root. That is the whole protocol: if you can put a file at
https://therapistsupport.org/<key>.txt containing <key>, you have proved you
control the host, and the API will take your word for what changed.

THE KEY IS NOT A SECRET. It is a capability, not a credential - anyone who
fetches the .txt can read it. Losing it costs nothing; rotating it means writing
a new file and changing KEY here. Do not treat it like a password, and do not
put it in .gitignore: the file MUST be committed and published or every
submission fails with 403.

WHAT IT SUBMITS. By default, everything in sitemap.xml. That is correct for the
first run and wasteful afterwards - IndexNow asks you to submit what CHANGED,
and submitting all 130 URLs every time trains the engines to discount you. So
--since compares against the last run's manifest (_dev/_snap/indexnow.json) and
sends only URLs whose lastmod moved.

  python3 _dev/indexnow.py            # everything in the sitemap
  python3 _dev/indexnow.py --since    # only what changed since the last run
  python3 _dev/indexnow.py --dry-run  # print the payload, send nothing

RUN IT AFTER discovery.py, never before: discovery.py is what regenerates
sitemap.xml with fresh lastmod values, and this script reads that file rather
than the directory, on purpose - if a page is not in the sitemap it should not
be announced either.

A 202 IS THE SUCCESS CASE. IndexNow returns 200 or 202 with an empty body; 202
means "accepted, not yet validated". A 403 means the key file is missing or does
not match, which on this host almost always means the publish has not landed
yet - wait for the watcher and retry rather than regenerating the key.
"""
import os, re, sys, json, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

HOST = "therapistsupport.org"
KEY  = "8b57d97a98d2a853791c5cb9a3b9872c"
KEY_LOCATION = "https://%s/%s.txt" % (HOST, KEY)
ENDPOINT = "https://api.indexnow.org/indexnow"
SNAP = os.path.join(HERE, "_snap", "indexnow.json")


def sitemap_entries():
    """[(loc, lastmod)] straight from the generated sitemap."""
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        sys.exit("sitemap.xml not found - run _dev/discovery.py first.")
    xml = open(p, encoding="utf-8").read()
    out = []
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        mod = re.search(r"<lastmod>([^<]+)</lastmod>", block)
        if loc:
            out.append((loc.group(1).strip(), mod.group(1).strip() if mod else ""))
    return out


def guard_key_file():
    """Refuse to submit if the key file is not actually being served.

    Catching this here turns a silent 403 into a sentence that says what to do.
    """
    try:
        with urllib.request.urlopen(KEY_LOCATION, timeout=15) as r:
            body = r.read().decode(errors="replace").strip()
    except Exception as e:
        sys.exit("Key file unreachable at %s (%s).\n"
                 "The publish has probably not landed yet - wait for the "
                 "auto-publish watcher and run again." % (KEY_LOCATION, e))
    if body != KEY:
        sys.exit("Key file at %s contains %r, expected %r.\n"
                 "Fix the file rather than the key." % (KEY_LOCATION, body[:64], KEY))


def main():
    since   = "--since"   in sys.argv
    dry_run = "--dry-run" in sys.argv

    entries = sitemap_entries()
    urls = [loc for loc, _ in entries]

    if since:
        old = {}
        if os.path.exists(SNAP):
            old = json.load(open(SNAP)).get("lastmod", {})
        urls = [loc for loc, mod in entries if old.get(loc) != mod]
        if not urls:
            print("Nothing changed since the last run. Sent nothing.")
            return

    print("%d URL(s) to submit%s." % (len(urls), " (changed only)" if since else ""))
    if dry_run:
        for u in urls[:20]:
            print("   ", u)
        if len(urls) > 20:
            print("    ... and %d more" % (len(urls) - 20))
        return

    guard_key_file()

    payload = {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION,
               "urlList": urls}
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            code, reason = r.status, r.reason
    except urllib.error.HTTPError as e:
        print("IndexNow refused: HTTP %s %s" % (e.code, e.reason))
        print(e.read()[:500].decode(errors="replace"))
        sys.exit(1)

    print("IndexNow accepted: HTTP %s %s" % (code, reason))

    os.makedirs(os.path.dirname(SNAP), exist_ok=True)
    json.dump({"submitted_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "count": len(urls),
               "lastmod": {loc: mod for loc, mod in entries}},
              open(SNAP, "w"), indent=1)
    print("Manifest written to %s - next --since run compares against it."
          % os.path.relpath(SNAP, ROOT))


if __name__ == "__main__":
    main()
