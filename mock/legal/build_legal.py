#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terms.html and privacy.html, on the site chrome.

Also writes _chrome_ftr.txt - the footer markup, lifted from a published page
so the three generated pages can finally have one. The footer CSS was already
inside the lifted _chrome_css.txt; only the markup was never taken, which is why
the advisor, tax and grow pages simply stop.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
import content as C

CH = os.path.join(HERE, "..", "amft")
SITE_DIR = os.path.join(HERE, "..", "..")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]

# ------------------------------------------------------- lift the footer ---
src = open(os.path.join(SITE_DIR, "tools.html")).read()
m = re.search(r"<footer.*?</footer>", src, re.S)
assert m, "no footer in tools.html to lift"
footer = m.group(0)
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", footer)

# The small-print column gains the two new pages. Doing it here means every
# page that lifts the footer gets them, including ones not built yet.
OLD_SMALL = ("<div><h5>The small print</h5>"
             "<p>2026 federal and California rates. Estimates only &mdash; not tax advice.</p>"
             "<p>Nothing is saved and nothing is sent. Your setup lives in the URL.</p></div>")
NEW_SMALL = ("<div><h5>The small print</h5>"
             '<a href="terms.html">Terms of Use</a>'
             '<a href="privacy.html">Privacy</a>'
             '<a href="contact.html">Report a wrong figure</a>'
             "<p>2026 federal and California rates. Estimates only &mdash; not tax, "
             "legal or financial advice.</p></div>")
# Idempotency. The published tools.html this lifts from was itself generated
# AFTER an earlier run of this script, so it already carries NEW_SMALL. A bare
# `assert OLD_SMALL in footer` therefore fails on a clean checkout of a
# perfectly healthy repo. Accept either state; fail only if NEITHER is present,
# which is the case that really means "the footer moved".
if OLD_SMALL in footer:
    footer = footer.replace(OLD_SMALL, NEW_SMALL, 1)
else:
    assert NEW_SMALL in footer, "the small-print column is not where it was"

OLD_BY = ("<p class=\"ftby\"><b>Built by Cavatello.</b> This does not constitute "
          "legal, tax or clinical advice.</p>")
NEW_BY = ('<p class="ftby"><b>Built by Cavatello.</b> Free, and not selling anything. '
          'Nothing here is legal, tax, financial or clinical advice, and using this site '
          'does not create a professional relationship &mdash; see the '
          '<a href="terms.html">Terms of Use</a>.</p>')
if OLD_BY in footer:
    footer = footer.replace(OLD_BY, NEW_BY, 1)
else:
    assert NEW_BY in footer, "the built-by line is not where it was"

open(os.path.join(CH, "_chrome_ftr.txt"), "w").write(footer)

# ------------------------------------------------------------------ CSS ----
CSS = """
.lg{--paper:#FBF9F3;--white:#fff;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
  --pine:#2C6350;--gold:#B08430;--pop:#F6C560;
  background:var(--white);color:var(--ink);font-family:Inter,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
.lg *,.lg *::before,.lg *::after{box-sizing:border-box}
.lgwrap{max-width:760px;margin:0 auto;padding:0 24px}
@media (max-width:520px){.lgwrap{padding:0 18px}}
.lghero{background:var(--paper);border-bottom:1px solid var(--line);
  padding:clamp(36px,5vw,64px) 0 clamp(28px,3.5vw,44px)}
.lgeyebrow{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}
.lg h1{font-family:Fraunces,Georgia,serif;font-weight:700;letter-spacing:-.016em;
  font-size:clamp(30px,3.6vw,46px);line-height:1.08;margin:0 0 .3em}
.lgdeck{font-size:clamp(16.5px,1.4vw,19px);line-height:1.62;color:#3A362E;margin:0;
  max-width:62ch}
.lgdate{margin:22px 0 0;font-family:'IBM Plex Mono',monospace;font-size:11.5px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.lgbody{padding:clamp(30px,4vw,56px) 0 clamp(40px,5vw,72px)}
.lgsec{margin:0 0 34px}
.lgsec h2{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:clamp(19px,1.8vw,24px);
  line-height:1.2;margin:0 0 .5em;letter-spacing:-.01em}
.lgsec p{font-size:16px;line-height:1.68;color:#3A362E;margin:0 0 .9em;max-width:66ch}
.lgsec p:last-child{margin-bottom:0}
.lgsec a{color:var(--pine);font-weight:600}
.lgtoc{background:var(--paper);border:1px solid var(--line);border-radius:14px;
  padding:20px 22px;margin:0 0 40px}
.lgtoc h2{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}
.lgtoc ol{margin:0;padding-left:1.2em;columns:2;column-gap:28px}
@media (max-width:600px){.lgtoc ol{columns:1}}
.lgtoc li{font-size:14.2px;line-height:1.5;margin:0 0 7px;break-inside:avoid}
.lgtoc a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.lgtoc a:hover{border-bottom-color:var(--pine);color:var(--pine)}
.lgnote{margin:36px 0 0;padding:18px 20px;background:#FFFCF4;
  border-left:4px solid var(--gold);border-radius:0 12px 12px 0;font-size:14.5px;
  line-height:1.6;color:#6B5321}
.lgpair{display:flex;gap:12px;flex-wrap:wrap;margin:34px 0 0;padding-top:24px;
  border-top:1px solid var(--line)}
.lgpair a{display:inline-flex;align-items:center;min-height:46px;padding:0 20px;
  border-radius:999px;border:1.5px solid var(--line);text-decoration:none;
  font-weight:600;font-size:15px;color:var(--ink)}
.lgpair a:hover{border-color:var(--pine);color:var(--pine)}
.lg :focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:6px}
"""

_bare = set(re.findall(r"^\.([A-Za-z][\w-]*)\s*\{", CSS, re.M))
_chrome = set(re.findall(r"\.([A-Za-z][\w-]*)", chrome_css))
assert not (_bare & _chrome), "collides with the lifted chrome: %s" % sorted(_bare & _chrome)

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s &mdash; %(brand)s</title>
<meta name="description" content="%(desc)s" />
<link rel="canonical" href="%(site)s/%(slug)s" />
<meta property="og:title" content="%(title)s &mdash; %(brand)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:type" content="website" />
<meta property="og:url" content="%(site)s/%(slug)s" />
%(head)s
<style>%(chrome_css)s</style>
<style>%(css)s</style>
<script type="application/ld+json">%(ld)s</script>
</head><body>
%(hdr)s
<main class="lg">
  <div class="lghero"><div class="lgwrap">
    <p class="lgeyebrow">%(brand)s</p>
    <h1>%(title)s</h1>
    <p class="lgdeck">%(deck)s</p>
    <p class="lgdate">Effective %(eff)s</p>
  </div></div>
  <div class="lgbody"><div class="lgwrap">
    %(toc)s
    %(sections)s
    %(note)s
    <div class="lgpair">%(pair)s</div>
  </div></div>
</main>
%(ftr)s
<script>%(js)s</script>
</body></html>
"""

NOTE = ('<p class="lgnote"><b>Plain-language summary, which does not replace the '
        'text above.</b> This site is free, stores nothing you type, and is not '
        'advice. Check anything that matters with a professional who knows your '
        'situation before you act on it.</p>')


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def page(slug, title, deck, sections, desc, other_slug, other_label):
    toc = ('<nav class="lgtoc"><h2>On this page</h2><ol>'
           + "".join('<li><a href="#%s">%s</a></li>'
                     % (slugify(h), re.sub(r"^\d+\.\s*", "", h)) for h, _ in sections)
           + "</ol></nav>")
    body = "".join(
        '<section class="lgsec" id="%s"><h2>%s</h2>%s</section>'
        % (slugify(h), h, "".join("<p>%s</p>" % p for p in ps))
        for h, ps in sections)
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebPage",
        "name": title, "url": "%s/%s" % (C.SITE, slug), "description": desc,
        "isPartOf": {"@type": "WebSite", "name": C.BRAND, "url": C.SITE + "/"},
        "publisher": {"@type": "Organization", "name": C.OWNER},
        "dateModified": "2026-08-02"})
    pair = ('<a href="%s">%s</a><a href="%s">Contact</a><a href="index.html">Home</a>'
            % (other_slug, other_label, C.CONTACT_PAGE))
    return SHELL % dict(title=title, brand=C.BRAND, desc=desc, site=C.SITE, slug=slug,
                        head=chrome_head, chrome_css=chrome_css, css=CSS, ld=ld,
                        hdr=chrome_hdr, deck=deck, eff=C.EFFECTIVE, toc=toc,
                        sections=body, note=NOTE, pair=pair, ftr=footer, js=chrome_js)


def main():
    out = []
    out.append(("terms.html", page(
        "terms.html", C.TERMS_TITLE, C.TERMS_DECK, C.TERMS,
        "Terms of use for %s. Nothing on this site is tax, legal, financial or "
        "clinical advice, and using it creates no professional relationship." % C.BRAND,
        "privacy.html", "Privacy Policy")))
    out.append(("privacy.html", page(
        "privacy.html", C.PRIVACY_TITLE, C.PRIVACY_DECK, C.PRIVACY,
        "What %s collects and what it does not. The calculators store nothing; the "
        "site carries Google Analytics, and one page carries ads." % C.BRAND,
        "terms.html", "Terms of Use")))
    for name, html in out:
        assert html.count("<h1") == 1, name + ": not exactly one h1"
        assert "<footer" in html, name + ": no footer"
        open(os.path.join(HERE, name), "w", encoding="utf-8").write(html)
        print("wrote %-14s %d kB" % (name, len(html) // 1024))
    print("wrote _chrome_ftr.txt  %d bytes" % len(footer))


if __name__ == "__main__":
    main()
