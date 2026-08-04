#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""grow-your-therapy-practice.html

Step 3 of claude/site-architecture-and-seo.md. The growth chapter leaves the
home page and becomes a real file with a keyword-bearing slug.

Same construction as the tax page: chrome lifted verbatim from a published page
at build time, the prototype's own engine constants reused so nothing can drift,
every class checked against the chrome before it ships.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
from css import CSS
from render import JS as RENDER_JS

CORE = open(os.path.join(HERE, "_engine_core.js")).read()

SITE = "https://cavatello.github.io/therapist-tools"
SLUG = "grow-your-therapy-practice.html"
TITLE = "Grow Your Therapy Practice — what a client is worth, and how many you need"
DESC = ("Work out what one therapy client is actually worth over their whole time with you, "
        "which of your referral channels is losing the most people, and how many enquiries a "
        "month you need just to stand still. Free, no account, for California private "
        "practice.")

# ---------------------------------------------------------------- chrome ---
CH = os.path.join(HERE, "..", "amft")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
# The footer was never lifted, which is why this page used to just stop.
chrome_ftr = open(os.path.join(CH, "_chrome_ftr.txt")).read()

# Replaces the "Grow Your Practice" entry that pointed at an anchor inside the
# simulator, rather than adding a second thing with the same name.
_anchor = re.search(r'<a href="(?:index\.html)?#grow">(.*?)</a>', chrome_hdr, re.S)
if _anchor and SLUG not in chrome_hdr:
    chrome_hdr = chrome_hdr.replace(_anchor.group(0),
        '<a href="' + SLUG + '" class="on">' + _anchor.group(1).replace(
            "funnels, associates, lead targets",
            "what a client is worth, and where they come from") + '</a>', 1)
SELF = SLUG
# The chrome is lifted from tools.html, where "All free tools" legitimately
# carries class="on". Lifted onto another page that marker is a lie: every page
# was telling the reader they were on the tools page. Strip every marker first,
# then set the one that belongs to THIS page.
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r'\1', chrome_hdr)
_self = re.search(r'<a href="' + re.escape(SELF) + r'"', chrome_hdr)
assert _self, "this page has no entry of its own in the lifted nav: " + SELF
chrome_hdr = (chrome_hdr[:_self.end() - 1] + '" class="on"'
              + chrome_hdr[_self.end():])
assert chrome_hdr.count('class="on"') == 1

# The lifted chrome is a CACHED copy of a published page's nav, and it drifts.
# On 4 Aug it still carried a "Full simulator" entry the live site had dropped,
# pointing at practice-simulator.html — the same destination as "Practice
# Simulator" — so every rebuild silently reintroduced a duplicate nav item with
# a different label. Nothing errored; it just shipped. Two destinations that are
# the same page under two names is mechanically detectable, so detect it.
_navlinks = re.findall(r'<a href="([^"#][^"]*)"[^>]*>(?:(?!</a>).)*?<b>([^<]*)</b>',
                       chrome_hdr, re.S)
_byhref = {}
for _h, _label in _navlinks:
    _byhref.setdefault(_h, []).append(_label)
_dupes = {h: ls for h, ls in _byhref.items() if len(ls) > 1}
assert not _dupes, (
    "the lifted nav points at the same page more than once — the chrome cache "
    "in ../amft/ has drifted from the live site: %r" % _dupes)

# ------------------------------------------------------------ structured ---
LD = [
 {"@context":"https://schema.org","@type":"WebApplication",
  "name":"Grow Your Therapy Practice","url":SITE + "/" + SLUG,
  "applicationCategory":"BusinessApplication","operatingSystem":"Any web browser",
  "browserRequirements":"Requires JavaScript",
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":DESC,
  "audience":{"@type":"Audience","audienceType":"Therapists in private practice"},
  "featureList":["Client lifetime value from your rate and average tenure",
                 "Per-channel funnel: views, enquiries and conversions",
                 "Which referral channel to fix first, by clients lost not by rate",
                 "Enquiries needed per month to replace churn",
                 "Caseload against weekly capacity"]},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
   {"@type":"ListItem","position":1,"name":"Therapist Support","item":SITE + "/"},
   {"@type":"ListItem","position":2,"name":"Free tools","item":SITE + "/tools.html"},
   {"@type":"ListItem","position":3,"name":"Grow your therapy practice",
    "item":SITE + "/" + SLUG}]},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
   {"@type":"Question","name":"What is a therapy client actually worth?",
    "acceptedAnswer":{"@type":"Answer","text":
      "Your session rate multiplied by the number of sessions a client typically stays for. "
      "At $150 a session and a 16-session course of therapy that is $2,400 — not $150. It is "
      "the figure that turns marketing spend from a feeling into arithmetic, and most "
      "practices have never worked it out."}},
   {"@type":"Question","name":"How many enquiries does a private practice need each month?",
    "acceptedAnswer":{"@type":"Answer","text":
      "Enough to replace what you lose. If two clients finish in a typical month and one "
      "enquiry in three becomes a client, you need six enquiries a month simply to stand "
      "still — before any growth at all."}},
   {"@type":"Question","name":"Which referral channel should I fix first?",
    "acceptedAnswer":{"@type":"Answer","text":
      "Not the one with the lowest conversion rate — the one where the most people fell out. "
      "A channel converting 20% of forty enquiries is losing you far more clients than one "
      "converting 10% of six, and the recoverable clients are where the volume is."}},
   {"@type":"Question","name":"Why do people enquire and then not book?",
    "acceptedAnswer":{"@type":"Answer","text":
      "Views-to-enquiry and enquiry-to-client are different problems. The first is your "
      "listing, photo and opening paragraph. The second is what happens in the next 48 "
      "hours: how fast you reply, whether a real appointment time is on offer, and whether "
      "the fee came as a surprise. The second is usually cheaper to fix."}}]}]


def field(fid, label, unit="", mn=None, mx=None, step=None, ph="", kind="number"):
    a = 'id="i-%s" type="%s"' % (fid, kind)
    if mn is not None: a += ' min="%s"' % mn
    if mx is not None: a += ' max="%s"' % mx
    if step is not None: a += ' step="%s"' % step
    if ph: a += ' placeholder="%s"' % ph
    pre = '<span class="unit">$</span>' if unit == "$" else ""
    post = ('<span class="unit">' + unit + "</span>") if unit and unit != "$" else ""
    return ('<label class="f"><em>' + label + '</em><span class="fv">' + pre
            + "<input " + a + ">" + post + "</span></label>")


CHANNELS = [("pt", "Psychology Today", "or any paid directory you are listed in"),
            ("web", "Your own website", "search, your blog, anyone who lands there"),
            ("ref", "Referrals", "GPs, past clients, other therapists")]

B = []
A = B.append
A('<div class="gro">')

# ---- hero
A('<section class="ghero"><div class="in"><div>')
A('<p class="gkick">Growing the practice &middot; California private practice</p>')
A('<h1>Grow your therapy practice in <em>California</em>.</h1>')
A('<p class="gtag">A practice is a funnel, not a mystery.</p>')
A('<p class="glede">How many people see you, how many ask, how many book — and what one of '
  'them is worth over the whole time they stay. Change any one of those and a whole year '
  'moves. <b>This page needs about six numbers</b>, most of which you can estimate from '
  'memory, and it will tell you which of your channels is quietly losing you the most '
  'clients.</p>')
A('<div class="gherocta"><a href="#worth">What a client is worth</a>'
  '<a class="ghost" href="#channels">Where they come from</a>'
  '<a class="ghost" href="#need">How many you need</a></div>')
A('</div><div class="gpanel">'
  '<div class="pr"><em>What one client is worth</em><b class="gold" id="heroworth">$4,800</b></div>'
  '<div class="pr"><em>One more a month, over a year</em><b id="heroyear">$57,600</b></div>'
  '<p class="pn" id="heroeg" style="margin-top:2px"><b>Worked example</b> &mdash; a $200 hour '
  'over 24 sessions. Put your own rate and tenure in below and both figures become yours.</p>'
  '<p class="pn">A projection, not a forecast. Nothing is saved and there is no account — '
  'your setup lives in the address bar, so bookmarking this page keeps it.</p>'
  '</div></div></section>')

# ---- 01 worth
A('<section class="slab pine" id="worth"><div class="chh"><span class="chn">01</span>'
  '<h2>What a client is worth</h2></div>')
A('<p class="dek">Two numbers, multiplied. Almost nobody in private practice knows the answer, '
  'and it is the number that makes every other decision on this page arithmetic instead of '
  'anxiety.</p>')
A('<div class="fgrid">')
A(field("rate", "Your session rate", "$", mn=0, mx=1000, step=5, ph="150"))
A(field("tenure", "Sessions a client typically stays", "", mn=0, mx=200, step=1, ph="16"))
A(field("clients", "Clients you hold right now", "", mn=0, mx=300, step=1, ph="24"))
A(field("sessions", "Sessions you do a week", "", mn=0, mx=60, step=1, ph="25"))
A('</div>')
A('<div id="worthout" style="margin-top:18px"></div>')
A('</section>')

# ---- 02 channels
A('<section class="slab carbon" id="channels"><div class="chh"><span class="chn">02</span>'
  '<h2>Where your clients actually come from</h2></div>')
A('<p class="dek">Last month, for each place people find you. <b>Rough numbers are fine</b> — '
  'the point is which channel is losing people, and that shows up even when the counts are '
  'approximate. Directory dashboards give you views and enquiries; the third number you '
  'already know.</p>')
A('<div class="cinputs">')
for key, name, note in CHANNELS:
    A('<div class="cbox"><b>' + name + '</b><i>' + note + '</i><div class="fgrid">'
      + field(key + "_views", "Saw you", "", mn=0, mx=100000, step=1, ph="210")
      + field(key + "_enq", "Enquired", "", mn=0, mx=10000, step=1, ph="22")
      + field(key + "_got", "Became clients", "", mn=0, mx=1000, step=1, ph="6")
      + '</div></div>')
A('</div>')
A('<div id="funnel" style="margin-top:20px"></div>')
A('</section>')

# ---- 03 need
A('<section class="slab brick" id="need"><div class="chh"><span class="chn">03</span>'
  '<h2>How many you need, just to stand still</h2></div>')
A('<p class="dek">Standing still is not free. People finish — that is the job working — and '
  'every one of them has to be replaced before a single new client counts as growth. This is '
  'the number that decides whether your marketing is enough, and it is almost always higher '
  'than people expect.</p>')
A('<div class="fgrid" style="max-width:420px">')
A(field("churn", "Clients who finish in a typical month", "", mn=0, mx=100, step=1, ph="2"))
A(field("weeksOff", "Weeks off a year", "wks", mn=0, mx=26, step=1, ph="2"))
A('</div>')
A('<div id="needout" style="margin-top:18px"></div>')
A('</section>')

# ---- 04 capacity
A('<section class="slab pine" id="capacity"><div class="chh"><span class="chn">04</span>'
  '<h2>How full your week already is</h2></div>')
A('<p class="dek">There is a point where more marketing stops making you money and starts '
  'making you a waiting list. Worth knowing where it is before you spend anything.</p>')
A('<div id="capout"></div>')
A('</section>')

# ---- 05 seasonality
# Everything above this section is an annual average. This is the only block on
# the page that admits the year has a shape, which is why it sits after capacity
# (you need a ceiling before "over capacity" means anything) and before the CTA.
A('<section class="slab brick" id="season"><div class="chh"><span class="chn">05</span>'
  '<h2>When they actually arrive</h2></div>')
A('<p class="dek">Everything above is a yearly average, and an average is a poor guide to a '
  'year that is not flat. Most practitioners describe a January rush and a summer lull — but '
  '<b>nobody has published data on it</b>, so this section treats that as a hypothesis you test '
  'against your own calendar rather than a fact it asserts at you. What is not in doubt is the '
  'mechanism: people finish therapy at a steady rate whatever the month, so any dip in enquiries '
  'shows up as a caseload trough later, and by then it is too late to market your way out of '
  'it.</p>')
A('<div id="seasout"></div>')
A('</section>')

# ---- CTA
A('<section class="slab carbon" id="next"><div class="chh"><span class="chn">06</span>'
  '<h2>What this is worth in actual money</h2></div>')
A('<p class="dek">Everything above is clients. Turning clients into what lands in your bank '
  'account takes the rest of the picture — expenses, self-employment tax, the retirement '
  'accounts that decide how much of the tax is optional. That is the simulator, and your '
  'numbers travel with you.</p>')
A('<a class="gcta" href="index.html"><strong>Model the whole practice &rarr;</strong>'
  '<span>rate, caseload, expenses and tax &middot; free &middot; nothing is saved</span></a>')
A('<div class="alist" style="border-top:0;padding-top:14px;margin-top:14px;display:grid;'
  'grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 22px">' + "".join(
    '<div style="display:flex;gap:9px;font-size:12.5px;line-height:1.55;opacity:.72">'
    '<i style="font-style:normal;color:#F6C560;flex:none">&rarr;</i><span>'
    '<b style="color:#fff">' + a + '</b> &mdash; ' + b + '</span></div>' for a, b in [
      ("What the caseload above actually pays", "after twelve expense categories and tax"),
      ("How much of your tax bill is optional", "the retirement accounts, priced"),
      ("Sole proprietor or professional corporation",
       "including what it costs your Social Security"),
      ("What employing associates changes", "revenue, payroll tax and supervision hours"),
      ("What CA therapy actually charges", "insurance panels against private pay"),
      ("Where you could live on the same practice", "seven places, priced"),
    ]) + '</div>')
A('</section>')
A('</div>')

# ---- disclaimer
A('<div class="gro"><p class="disc"><b>A projection, not a forecast.</b> Client lifetime '
  'value assumes your average tenure holds, which it will not exactly; funnels move month to '
  'month, and one month of data is a sample of one. The value of a channel is what its '
  'clients are worth over their whole time with you, not what they billed last month. '
  'Nothing here is financial or business advice — it is arithmetic on numbers you supplied, '
  'shown so you can argue with it.</p></div>')

BODY = "\n".join(B)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
{chrome_head}
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="google-adsense-account" content="ca-pub-6079968999170000" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{site}/{slug}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Therapist Support" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{site}/{slug}" />
<meta property="og:image" content="{site}/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{ld}</script>
<style>
{chrome_css}
</style>
<style>
{css}
</style>
</head>
<body>
{hdr}
<main>
{body}
</main>
<script>
{navjs}
</script>
<script>
{core}
{render}
</script>
{ftr}
</body>
</html>
"""

html = HTML.format(chrome_head=chrome_head, title=TITLE, desc=DESC, site=SITE, slug=SLUG,
                   ld=json.dumps(LD, separators=(",", ":")), chrome_css=chrome_css, css=CSS,
                   hdr=chrome_hdr, body=BODY, navjs=chrome_js, core=CORE, render=RENDER_JS, ftr=chrome_ftr)

# ----------------------------------------------------------------- guards ---
assert "</script>" not in RENDER_JS and "</script>" not in CORE
assert html.count("<style>") == 2 and html.count("</style>") == 2
assert html.count("<body>") == 1 and html.count("</body>") == 1
# Three pages shipped with no footer at all because the lift never took it.
assert html.count("<footer") == 1, "exactly one footer, please"
assert 'href="terms.html"' in html and 'href="privacy.html"' in html, \
    "the footer must carry the legal links"

# The collision guard that would have caught .tl, .ref and .sr on the tax page.
def _classes(css, bare_only=False):
    body = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = set()
    for group in re.findall(r"([^{}]+)\{", body):
        if group.strip().startswith("@"):
            continue
        for sel in group.split(","):
            sel = sel.strip()
            if bare_only:
                m = re.fullmatch(r"\.([a-zA-Z][\w-]*)(:[\w-]+(\([^)]*\))?)?", sel)
                if m:
                    out.add(m.group(1))
            else:
                out.update(re.findall(r"\.([a-zA-Z][\w-]*)", sel))
    return out
_clash = sorted(_classes(CSS, True) & _classes(chrome_css))
assert not _clash, "page classes clash with the site chrome: " + ", ".join(_clash)

for need in ['id="worthout"', 'id="funnel"', 'id="needout"', 'id="capout"',
             'id="seasout"', 'id="heroworth"', 'id="heroyear"']:
    assert html.count(need) == 1, "expected exactly one " + need
# every channel input exists
for key, _, _ in CHANNELS:
    for f in ("views", "enq", "got"):
        assert 'id="i-%s_%s"' % (key, f) in html, "missing input for %s %s" % (key, f)
assert "undefined" not in BODY

out = os.path.join(HERE, SLUG)
open(out, "w").write(html)
print("wrote", SLUG, len(html) // 1024, "kB;", len(re.findall(r'id="i-', html)), "inputs")
