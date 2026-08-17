#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools.html -> resources.html, on a host with no server-side redirects.

GitHub Pages cannot issue a 301, so this is the next best thing and the
combination matters:

  rel=canonical      tells search engines resources.html is the real page and
                     passes the ranking signal, which is the whole point -
                     tools.html has months of indexing behind "free tools for
                     therapists" and the hub was one day old.
  meta refresh, 0s   Google documents a zero-delay meta refresh as a redirect.
  JS replace()       replaces rather than pushes, so Back does not bounce the
                     reader between the two pages forever.
  a real link        for anyone whose browser honours none of the above. Never
                     ship a redirect page with nothing on it.
  noindex is NOT set - it would stop the canonical being read at all.

Why this direction. Measured: tools.html had 8 internal destinations,
resources.html had 10, and 6 overlapped. The two unique to tools.html were
`index.html` and `resources.html` itself, so it was a strict subset. The hub
absorbs it; this file keeps the URL alive for anything already pointing here.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
BASE = "https://therapistsupport.org"
DEST = "resources.html"

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free tools for California therapists &mdash; moved to Resources</title>
<link rel="canonical" href="{base}/{dest}">
<!-- ts:meta -->
<meta name="ts:topic" content="practice">
<meta name="ts:format" content="reference">
<meta name="ts:question" content="Where did the tools page go?">
<meta name="ts:outcome" content="A redirect to Resources, which now holds every calculator">
<meta name="ts:weight" content="1">
<meta name="ts:skip" content="true">
<!-- /ts:meta -->
<meta http-equiv="refresh" content="0; url={dest}">
<meta name="description" content="The free tools for California therapists now live on one page with the rest of the practice resources.">
<style>
body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
 background:#F6F8F6;color:#1B2420;font-family:system-ui,sans-serif;padding:26px}}
main{{max-width:44ch;text-align:center}}
h1{{font-family:Georgia,serif;font-size:26px;font-weight:600;margin:0 0 12px;
 letter-spacing:-.02em}}
p{{font-size:16.5px;line-height:1.7;color:#5F6A64;margin:0 0 20px}}
a{{display:inline-flex;align-items:center;min-height:46px;padding:0 22px;border-radius:11px;
 background:#123C30;color:#fff;font-weight:700;font-size:16.5px;text-decoration:none}}
</style>
</head>
<body>
<main>
<h1>This page moved.</h1>
<p>Every free tool is still here &mdash; they now sit on one page with the
rest of the practice resources, so you can get to the calculators and the
reference material without guessing which page holds which.</p>
<a href="{dest}">Go to Tools &amp; resources &rarr;</a>
</main>
<script>/* replace() so Back does not bounce between the two pages.
   Resolved against location.href first: a bare relative URL throws when the
   document has no base (a test harness, a file:// copy), and a redirect stub
   that logs an error is one someone later "fixes" by deleting the script. */
(function(){{try{{location.replace(new URL("{dest}",location.href).href)}}
catch(e){{}}}})();</script>
</body>
</html>
""".format(base=BASE, dest=DEST)


def main():
    path = os.path.join(SITE, "tools.html")
    open(path, "w", encoding="utf-8").write(HTML)
    s = open(path, encoding="utf-8").read()
    assert 'rel="canonical"' in s and DEST in s
    assert "noindex" not in s, "noindex would stop the canonical being read"
    assert s.count("<h1") == 1
    # A ts:skip page must keep saying so, or discovery.py puts a redirect
    # stub in the sitemap.
    assert 'name="ts:skip" content="true"' in s
    # No stylesheet and no webfont. This is the file that kept
    # css/house-skin.css alive on the live site, through seventeen <link>s
    # appended by passes that had no idea it was a stub - and it asked for
    # Fraunces and Inter without loading either, so even its own two lines
    # of copy rendered in a fallback. A reader is here for zero
    # milliseconds; it earns no requests. Sanctioned colours and the house
    # 16.5px metric, so palette_conform has nothing to correct.
    assert '<link rel="stylesheet"' not in s
    assert "fonts.googleapis" not in s
    assert "Fraunces" not in s and "Inter," not in s
    print("tools.html  %d bytes  -> %s" % (len(s.encode("utf-8")), DEST))


if __name__ == "__main__":
    main()
