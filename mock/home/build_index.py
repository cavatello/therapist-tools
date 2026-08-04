#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""index.html — the prototype design, shipped.

Step 4 of claude/site-architecture-and-seo.md, with the design decision the user
made after it was written: the home page becomes the PROTOTYPE, not the React
simulator with two chapters swapped out.

What changes, precisely:

  chapter 04 "What you keep"   ->  a promo block selling therapist-tax-strategy-california.html
  chapter 05 "Bonus level"     ->  a promo block selling grow-your-therapy-practice.html
  the prototype's own masthead ->  the site chrome, lifted from a published page
  the prototype banner         ->  removed
  <head>                       ->  real title, description, canonical, OG, JSON-LD

What the prototype does NOT have, and what happens to it: residency (seven
places plus Pittsburgh), the Social Security deep dive, the biweekly pay
calendar, the retirement strategy cards and the citation blocks all live in the
React app. That app is NOT deleted - it is published at practice-simulator.html
and linked from a third block on this page, so nothing that exists today becomes
unreachable. Giving residency its own page is the obvious next slug.

Both promo CTAs carry the reader's setup in the link, including the twelve
expense categories as exp_* keys, which the tax page already knows how to read.
Without that the split fails outright: nobody types their practice twice.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "proto", "index.html")).read()

SITE = "https://cavatello.github.io/therapist-tools"
TAX = "therapist-tax-strategy-california.html"
GROW = "grow-your-therapy-practice.html"
COLA = "therapist-cost-of-living-california.html"
FULL = "practice-simulator.html"
TITLE = ("California Therapy Practice Simulator — what your practice actually pays you")
DESC = ("Free simulator for California-licensed therapists. Session rate, caseload, twelve "
        "expense categories, self-employment tax and what you actually keep, on 2026 federal "
        "and California rates. No account, nothing saved.")

# ---------------------------------------------------------------- chrome ---
CH = os.path.join(HERE, "..", "amft")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]

# The prototype simulator has moved off "/" - index.html is now the landing
# page. This slug is the one the React app used to hold; it keeps its meaning,
# every inbound link to it still lands on a simulator, and app.js goes away.
SELF = "practice-simulator.html"
# The chrome is lifted from tools.html, where "All free tools" legitimately
# carries class="on". Lifted onto another page that marker is a lie: every page
# was telling the reader they were on the tools page. Strip every marker first,
# then set the one that belongs to THIS page.
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r'\1', chrome_hdr)
_self = re.search(r'<a href="' + re.escape(SELF) + r'"', chrome_hdr)
assert _self, "this page has no entry of its own in the lifted nav: " + SELF
chrome_hdr = (chrome_hdr[:_self.end() - 1] + '" class="on"' + chrome_hdr[_self.end():])
assert chrome_hdr.count('class="on"') == 1

# ------------------------------------------------------------------ head ---
LD = [
 {"@context": "https://schema.org", "@type": "WebApplication",
  "name": "California Therapy Practice Simulator", "url": SITE + "/",
  "applicationCategory": "FinanceApplication", "operatingSystem": "Any web browser",
  "browserRequirements": "Requires JavaScript",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": DESC,
  "audience": {"@type": "Audience",
               "audienceType": "California-licensed marriage and family therapists, clinical "
                               "social workers, professional clinical counselors and "
                               "psychologists"},
  "featureList": ["Session rate and caseload to annual billings",
                  "Twelve expense categories plus card processing as a live percentage",
                  "Self-employment tax, federal and California, on 2026 rates",
                  "What you keep, per year, per month and per session",
                  "Employing associates, priced with employer payroll tax"]},
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Therapist Support", "item": SITE + "/"}]},
]

HEAD = (chrome_head + '\n'
        '<meta charset="utf-8" />\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        '<meta name="robots" content="index, follow, max-image-preview:large" />\n'
        '<meta name="google-adsense-account" content="ca-pub-6079968999170000" />\n'
        '<title>' + TITLE + '</title>\n'
        '<meta name="description" content="' + DESC + '" />\n'
        '<link rel="canonical" href="' + SITE + '/" />\n'
        '<meta property="og:type" content="website" />\n'
        '<meta property="og:site_name" content="Therapist Support" />\n'
        '<meta property="og:title" content="' + TITLE + '" />\n'
        '<meta property="og:description" content="' + DESC + '" />\n'
        '<meta property="og:url" content="' + SITE + '/" />\n'
        '<meta property="og:image" content="' + SITE + '/og-image.png" />\n'
        '<meta name="twitter:card" content="summary_large_image" />\n'
        '<script type="application/ld+json">'
        + json.dumps(LD, separators=(",", ":")) + '</script>\n')

# ------------------------------------------------------ the promo blocks ---
KEEP_A = SRC.index('<section class="slab carbon" id="keep">')
KEEP_B = SRC.index('<!-- ===================== 05 BONUS LEVEL')
GROW_A = KEEP_B
GROW_B = SRC.index("</section>", SRC.index('<section class="bonus" id="grow">')) + len("</section>")

# render() writes into every id those two chapters carried. On the split those
# elements live on the other pages; here they are kept in the DOM, hidden, so
# the prototype's own script runs completely untouched. Derived from the markup
# rather than typed, so it cannot drift.
def parked(chunk, skip):
    ids = sorted(set(re.findall(r'id="([\w-]+)"', chunk)) - skip)
    return "".join(
        ('<select id="%s"><option value="single" selected></option></select>' % i)
        if i == "i-filing" else
        ('<input id="%s">' % i) if i.startswith("i-") else
        ('<button id="%s"></button>' % i) if i.startswith("b-") else
        ('<span id="%s"></span>' % i)
        for i in ids)

PROMO = ('<section class="slab carbon" id="keep"><div id="promo"></div>'
         '<div style="display:none" aria-hidden="true">'
         + parked(SRC[KEEP_A:KEEP_B], {"keep"}) + '</div></section>')

GROWB = ('<section class="bonus" id="grow"><div class="in">'
         '<div class="ribbon">Bonus level</div><div id="growpromo"></div>'
         '<div style="display:none" aria-hidden="true">'
         + parked(SRC[GROW_A:GROW_B], {"grow"}) + '</div></div></section>')

CSS = """
/* ===== the two promo blocks ===== */
.pr-kick{display:inline-flex;align-items:center;gap:8px;background:rgba(246,197,96,.16);
 border:1px solid rgba(246,197,96,.4);border-radius:999px;padding:7px 15px;font-size:10px;
 font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#F6C560;margin:0 0 15px}
.pr-h{font-family:Fraunces,Georgia,serif;font-weight:600;color:#fff;letter-spacing:-.022em;
 line-height:1.08;margin:0 0 13px}
.pr-h b{color:#F6C560;font-weight:600}
/* capped: an unclamped 5vw headline is 128px on a 27-inch 5K inside a 1060px
   block, which looks broken rather than bold. */
.pr-h.big{font-size:clamp(30px,5vw,62px);max-width:17ch}
.pr-h.mid{font-size:clamp(25px,4vw,43px)}
.pr-p,.pr-barn,.pr-fine{max-width:68ch}
.pr-p{font-size:15px;line-height:1.72;color:rgba(255,255,255,.76);margin:0 0 20px}
.pr-p b{color:#fff}
.pr-num{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0 0 20px}
.pr-num > div{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);
 border-radius:14px;padding:15px 17px;min-width:0}
.pr-num .hi{background:rgba(246,197,96,.13);border-color:rgba(246,197,96,.4)}
.pr-num i{display:block;font-style:normal;font-size:10.5px;color:rgba(255,255,255,.55)}
.pr-num b{display:block;font-family:Fraunces,Georgia,serif;font-size:27px;font-weight:600;
 color:#fff;margin:6px 0 3px;line-height:1.03}
.pr-num .hi b{color:#F6C560}
.pr-num u{text-decoration:none;display:block;font-size:10px;color:rgba(255,255,255,.42)}
.pr-cta{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;
 width:100%;text-align:center;background:#F6C560;color:#2A2010;border-radius:18px;
 padding:clamp(22px,3vw,34px) clamp(18px,3vw,40px);text-decoration:none;
 box-shadow:0 7px 0 rgba(140,96,18,.55);transition:transform .1s,box-shadow .1s,background .15s;
 min-height:44px}
.pr-cta:hover{background:#FFD57A;box-shadow:0 7px 0 rgba(140,96,18,.7)}
.pr-cta:active{transform:translateY(6px);box-shadow:0 1px 0 rgba(140,96,18,.55)}
.pr-cta:focus-visible{outline:3px solid #fff;outline-offset:3px}
.pr-cta strong{font-family:Fraunces,Georgia,serif;font-size:clamp(24px,3.4vw,44px);
 font-weight:600;line-height:1.1;letter-spacing:-.018em;max-width:20ch}
.pr-cta span{font-size:clamp(12px,1.2vw,15px);font-weight:700;opacity:.72;letter-spacing:.01em}
.pr-row{display:block;margin:0 0 18px}
.pr-second{font-size:12.8px;color:rgba(255,255,255,.55);line-height:1.6;margin:11px auto 0;
 max-width:56ch;text-align:center}
.pr-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 22px;
 margin:20px 0 0;padding:18px 0 0;border-top:1px solid rgba(255,255,255,.14)}
.pr-list div{display:flex;gap:9px;font-size:12.6px;line-height:1.55;color:rgba(255,255,255,.66)}
.pr-list i{font-style:normal;color:#F6C560;flex:none}
.pr-list b{color:#fff;font-weight:600}
.pr-bar{display:flex;height:46px;border-radius:11px;overflow:hidden;margin:0 0 9px}
.pr-bar div{display:flex;flex-direction:column;align-items:center;justify-content:center;
 font-size:10.5px;font-weight:800;line-height:1.2;padding:0 6px;text-align:center;min-width:0}
.pr-bar .a{background:rgba(255,255,255,.17);color:#fff}
.pr-bar .b{background:rgba(255,255,255,.08);color:rgba(255,255,255,.66)}
.pr-bar .c{background:#F6C560;color:#2A2010}
.pr-bar strong{font-family:Fraunces,Georgia,serif;font-size:15px;font-weight:600}
.pr-barn{font-size:11.5px;color:rgba(255,255,255,.5);margin:0 0 20px}
.pr-fine{font-size:11.4px;line-height:1.65;color:rgba(255,255,255,.42);margin:16px 0 0;
 max-width:74ch}
/* --------------------------------------------------------------- NEXT ---
   Replaces "Where the rest of it went", which failed three ways: it sat
   immediately under the two promos and re-advertised the same two pages; it
   framed them as things this page REFUSES to do, which reads as an apology at
   the exact moment the reader has an answer in hand; and its four bullets
   duplicated the tax promo's own list forty lines above.

   This is the reusable end-of-page component instead - a kicker, one live
   headline, and three routes each carrying a number computed from what the
   reader just typed. Namespaced .nx so it can be lifted onto the tax, grow and
   AMFT pages with a different set of rows and no CSS collision. */
.nx{max-width:1060px;margin:16px auto 0;padding:0 4px}
.nx-k{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:#B08430;margin:0 0 8px;font-weight:600}
.nx-h{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.7vw,31px);margin:0 0 6px;
 font-weight:600;letter-spacing:-.018em;color:#26241E;line-height:1.16;max-width:22ch}
.nx-h b{font-weight:600;color:#2C6350}
.nx-p{font-size:13.4px;line-height:1.7;color:#6E695E;margin:0 0 20px;max-width:62ch}
.nx-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.nx-c{display:flex;flex-direction:column;background:#fff;border:1px solid #E7E2D6;
 border-radius:18px;padding:20px 20px 18px;text-decoration:none;color:inherit;
 border-top:3px solid #2C6350;transition:transform .12s,box-shadow .12s,border-color .12s}
.nx-c:nth-child(2){border-top-color:#B08430}
.nx-c:nth-child(3){border-top-color:#4B3B93}
.nx-c:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(38,36,30,.09)}
.nx-c:focus-visible{outline:3px solid #2C6350;outline-offset:3px}
.nx-c .lab{font-size:11px;letter-spacing:.09em;text-transform:uppercase;font-weight:700;
 color:#6E695E;margin:0 0 12px}
.nx-c .fig{font-family:Fraunces,Georgia,serif;font-size:clamp(24px,2.9vw,33px);font-weight:600;
 line-height:1;letter-spacing:-.02em;color:#26241E;margin:0 0 6px}
.nx-c .of{font-size:12.6px;line-height:1.55;color:#6E695E;margin:0 0 16px;flex:1 1 auto}
.nx-c .go{font-size:13.2px;font-weight:700;color:#2C6350;margin:0}
.nx-c:nth-child(2) .go{color:#8A6318}
.nx-c:nth-child(3) .go{color:#4B3B93}
.nx-c:hover .go{text-decoration:underline}
.nx-f{font-size:11.6px;line-height:1.65;color:#8B8477;margin:16px 0 0;max-width:74ch}
/* the zero-state figure: the same size as the real one, visibly provisional */
.nx-eg{color:#8B8477}
.nx-eg i{display:block;font-family:'IBM Plex Mono',monospace;font-style:normal;
 font-size:9.6px;letter-spacing:.11em;text-transform:uppercase;color:#B08430;margin:3px 0 0}
/* the prototype's own controls sat under the 38px touch minimum */
.mnav a,.mcta,.adj,.ghost,.ghost.sm{min-height:38px;display:inline-flex;align-items:center;
 justify-content:center;padding-top:9px;padding-bottom:9px}
@media (max-width:900px){
 .nx-g{grid-template-columns:1fr}
 /* stacked, three tall cards is a lot of scroll for a hand-off. Flatten each
    to a row: figure left, label and line right, arrow at the end. */
 .nx-c{padding:16px 18px}
 .nx-c .fig{font-size:26px;margin-bottom:4px}
 .nx-c .of{margin-bottom:10px}
}
@media (max-width:760px){
 .pr-num,.pr-list{grid-template-columns:1fr}
}
"""

JS = r"""
(function(){
  function f(v){ return (window.TREE && TREE.fmt) ? TREE.fmt(v) : "$" + Math.round(v); }
  /* The link carries the reader's whole setup, expense categories included.
     Without this they land on the destination with an empty form and have to
     type everything again, which is the single most likely way a two-page
     split fails. */
  function stateQuery(keys){
    var S = window.__S || {}, q = [];
    keys.forEach(function(k){
      if (S[k] !== "" && S[k] !== undefined && S[k] !== null) q.push(k + "=" + encodeURIComponent(S[k]));
    });
    return q;
  }
  function taxHref(){
    var S = window.__S || {};
    var q = stateQuery(["rate","sessions","weeksOff","billingPct","age","filing","contrib"]);
    if (S.exp) Object.keys(S.exp).forEach(function(k){
      if (S.exp[k] !== "" && S.exp[k] != null) q.push("exp_" + k + "=" + encodeURIComponent(S.exp[k]));
    });
    return "TAXSLUG" + (q.length ? "#" + q.join("&") : "");
  }
  function growHref(){
    var q = stateQuery(["rate","sessions","weeksOff","tenure","clients","churn"]);
    return "GROWSLUG" + (q.length ? "#" + q.join("&") : "");
  }
  function list(items){
    return '<div class="pr-list">' + items.map(function(x){
      return '<div><i>&rarr;</i><span><b>' + x[0] + '</b> &mdash; ' + x[1] + '</span></div>';
    }).join("") + '</div>';
  }
  function drawTax(){
    var el = document.getElementById("promo"); if(!el) return;
    var t = window.TREE;
    var items = [["Which account, and what each is worth to you","Solo 401(k), SEP, SIMPLE, IRA"],
      ["How much room you have this year","and why it moves with your profit"],
      ["What it becomes","at a return and a horizon you choose"],
      ["Sole proprietor vs professional corporation","priced, including what it costs your Social Security"],
      ["What hiring associates changes","and what it does not"],
      ["What to actually do, and by when","the deadlines that bite"]];
    if(!t || t.profit <= 0){
      el.innerHTML = '<p class="pr-kick">Next</p>'
        + '<h2 class="pr-h mid">Put a rate and a caseload in above.</h2>'
        + '<p class="pr-p">Once there is profit on this page, this block works out how much of '
        + 'the tax on it is optional &mdash; and hands you a plan for the rest.</p>' + list(items);
      return;
    }
    var tot = Math.max(1, t.net + t.tax), fix = Math.max(0, t.tax - t.optional);
    el.innerHTML = '<p class="pr-kick">Do not skip this one</p>'
      + '<h2 class="pr-h big"><b>' + f(t.optional) + '</b> of your tax bill is optional.</h2>'
      + '<p class="pr-p">Not a loophole and not aggressive &mdash; ordinary accounts the tax '
      + 'code created on purpose. The only question is whether that money goes to the IRS this '
      + 'April or into an account with your name on it.</p>'
      + '<div class="pr-bar">'
      + '<div class="a" style="width:' + Math.round(t.net/tot*100) + '%">yours either way'
      + '<strong>' + f(t.net) + '</strong></div>'
      + '<div class="b" style="width:' + Math.round(fix/tot*100) + '%">tax you owe'
      + '<strong>' + f(fix) + '</strong></div>'
      + '<div class="c" style="width:' + Math.round(t.optional/tot*100) + '%">your call'
      + '<strong>' + f(t.optional) + '</strong></div></div>'
      + '<p class="pr-barn">Every dollar of profit, split three ways.</p>'
      + '<div class="pr-row"><a class="pr-cta" href="' + taxHref() + '">'
      + '<strong>Keep ' + f(t.optional) + ' &rarr;</strong>'
      + '<span>work out your tax strategy &middot; five minutes &middot; nothing is saved</span></a>'
      + '<p class="pr-second">Your rate, caseload and expenses come with you. You will not '
      + 'type anything twice.</p></div>' + list(items)
      + '<p class="pr-fine">Deferred, not avoided: you pay the tax when you withdraw, usually '
      + 'decades later and usually at a lower rate. What it costs you is liquidity &mdash; the '
      + 'money is hard to reach before 59&frac12; without a penalty.</p>';
  }
  function drawGrow(){
    var el = document.getElementById("growpromo"); if(!el) return;
    var S = window.__S || {};
    var rate = parseFloat(S.rate) || 0, ten = parseFloat(S.tenure) || 0;
    var worth = rate * ten;
    el.innerHTML = '<p class="pr-kick">Bonus level &middot; growing the practice</p>'
      + '<h2 class="pr-h mid">Everything above is the practice you have. '
      + '<b>This is the one you could have.</b></h2>'
      + '<p class="pr-p">A practice is a funnel, not a mystery. How many people see you, how '
      + 'many enquire, how many book &mdash; and what one of them is worth over the time they '
      + 'stay. Change one of those and a whole year moves.</p>'
      + '<div class="pr-num">'
      + '<div class="hi"><i>What one client is worth</i><b>'
        + (worth > 0 ? f(worth) : "&mdash;") + '</b><u>'
        + (worth > 0 ? "your rate × how long they stay" : "set your rate and average tenure")
        + '</u></div>'
      + '<div><i>Replace one lost client</i><b>' + (worth > 0 ? f(worth) : "&mdash;")
        + '</b><u>churn costs the same as growth pays</u></div>'
      + '<div><i>Ten more a year</i><b>' + (worth > 0 ? f(worth * 10) : "&mdash;")
        + '</b><u>on the same rate and hours</u></div></div>'
      + '<div class="pr-row"><a class="pr-cta" href="' + growHref() + '">'
      + '<strong>Grow your practice &rarr;</strong>'
      + '<span>lead sources, conversion, and what a client is really worth</span></a>'
      + '<p class="pr-second">A projection, not a forecast. Nothing here changes the figures '
      + 'above.</p></div>'
      + list([["What a client is actually worth","rate × average tenure, not one session"],
         ["Where your clients come from","directories, referrals, search — priced separately"],
         ["Your conversion, honestly","views → enquiries → booked, at each step"],
         ["How many you need a month","just to stand still against churn"],
         ["Which channel to fix first","the one losing you the most, not the loudest"],
         ["How full your week already is","before growth becomes a waiting list"]]);
  }
  /* ------------------------------------------------------------- NEXT ---
     The block that used to sit here said "two questions this page
     deliberately does not try to answer" and then linked the same two pages
     the two promos above it had just sold. Three problems in one card: it
     repeated, it apologised, and it did it at the exact moment the reader
     finally has a number in hand.

     This is the reverse. Same three destinations, but each one arrives as a
     figure computed from what the reader just typed, and each link carries
     the setup so nothing is retyped. It is deliberately generic - the same
     component, with different rows, belongs at the foot of the tax, grow and
     AMFT pages too. */
  function colaHref(){
    var T = window.TREE || {}, q = [];
    if (T.net > 0) q.push("net=" + Math.round(T.net / 12));
    if (T.profit > 0) q.push("agi=" + Math.round(T.profit));
    return "COLASLUG" + (q.length ? "#" + q.join("&") : "");
  }
  function card(href, accentless, lab, fig, of, go){
    return '<a class="nx-c" href="' + href + '">'
      + '<p class="lab">' + lab + '</p>'
      + '<p class="fig">' + fig + '</p>'
      + '<p class="of">' + of + '</p>'
      + '<p class="go">' + go + ' &rarr;</p></a>';
  }
  function drawNext(){
    var el = document.getElementById("nextroutes"); if(!el) return;
    var T = window.TREE || {}, S = window.__S || {};
    var net = T.net || 0, optional = T.optional || 0;
    /* Average tenure is a GROW-page input; on this page its control is parked
       and hidden, so rate x tenure would have been permanently blank. The rate
       itself is live here, and an unfilled hour is the number growth is
       actually about - so that is the figure this card carries. */
    var rate = parseFloat(S.rate) || 0;
    /* NO EM-DASHES. An hour after writing a rule against exactly this, the
       zero state of these three cards shipped as three dashes with captions
       for numbers that were not there. A reader who has typed nothing sees a
       worked example instead, labelled as one, so the card still proves the
       tool does something. */
    var EG = {optional: "$18,244", rate: "$200", month: "$11,578"};
    function fig(v, eg){ return v > 0 ? f(v) : '<span class="nx-eg">' + eg
      + '<i>worked example</i></span>'; }
    el.innerHTML = '<p class="nx-k">Next</p>'
      + '<h2 class="nx-h">' + (net > 0
          ? 'Your <b>' + f(net) + '</b> has three moves left in it.'
          : 'Three moves this number has left in it.') + '</h2>'
      + '<p class="nx-p">Your rate, caseload and twelve expense categories travel with each '
        + 'link. You will not type your practice twice.</p>'
      + '<div class="nx-g">'
      + card(taxHref(), 0, "Still on the table",
          fig(optional, EG.optional),
          optional > 0
            ? "of this year&rsquo;s tax is optional &mdash; retirement accounts, and the sole proprietor against a professional corporation."
            : "how much of your tax bill is optional, once retirement accounts and the entity choice are priced.",
          "Tax &amp; retirement strategy")
      + card(growHref(), 0, "One empty hour",
          fig(rate, EG.rate),
          rate > 0
            ? "is what an unfilled slot costs you. Growth is arithmetic about having fewer of them &mdash; where clients come from, what converts, and what one is worth over the time they stay."
            : "what an unfilled slot costs, where clients come from, and what one is worth over the time they stay.",
          "Grow your practice")
      + card(colaHref(), 0, "A month, after everything",
          fig(net / 12, EG.month),
          net > 0
            ? "a month is what actually lands. Against California housing, a student loan and a savings target, that is either enough or it is not."
            : "what lands each month, against California rent, a student loan and a savings target.",
          "What it costs to live here")
      + '</div>'
      + '<p class="nx-f">Nothing on any of those three pages changes the figures above.</p>';
  }
  window.drawPromo = function(){ drawTax(); drawGrow(); drawNext(); };
  drawTax(); drawGrow(); drawNext();
})();
""".replace("TAXSLUG", TAX).replace("GROWSLUG", GROW).replace("COLASLUG", COLA)

HOOK_ANCHOR = '''    row("Most you can redirect this year", "", fmt(optional), "tot");'''
HOOK = HOOK_ANCHOR + '''

  /* the promo blocks read the same computation as everything else */
  window.TREE = {gross:c.gross, costs:runCost, profit:c.profit, tax:c.totalTax, net:c.net,
    room:c.room, contrib:c.contrib, optional:optional, fmt:fmt};
  window.__S = S;
  if (window.drawPromo) window.drawPromo();'''

# The block that used to sell "the full simulator" is gone: this page IS the
# simulator now, and the things it promised have moved. Residency lives on the
# tax page's working-remotely section, Social Security lives on the tax page,
# and the biweekly calendar is below. Advertising a page that no longer exists
# was the alternative.
DEEPER = """
<div class="nx" id="nextroutes"></div>
"""

# ------------------------------------------------------------------ build ---
s = SRC[:KEEP_A] + PROMO + GROWB + DEEPER + SRC[GROW_B:]

assert s.count(HOOK_ANCHOR) == 1
s = s.replace(HOOK_ANCHOR, HOOK, 1)

# The prototype binds $("b-max") with no null guard and that control lived inside
# the chapter this page hands off. It threw, so render() was never wired and the
# promo sat in its empty state forever. Guard the listener rather than keeping an
# orphan control on a page that no longer owns it.
s = re.sub(r'\$\("(b-max)"\)\.addEventListener',
           r'($("\1") || {addEventListener:function(){}}).addEventListener', s)

# prototype chrome out, site chrome in
s = re.sub(r'<div class="proto">.*?</div>\s*', '', s, count=1, flags=re.S)
_mast = re.search(r'<header class="mast">.*?</header>', s, re.S)
assert _mast, "the prototype masthead was not found"
s = s.replace(_mast.group(0), chrome_hdr, 1)

# head: drop the prototype's noindex + title, keep its font link, add the real head
s = re.sub(r'<meta name="robots"[^>]*>\s*', '', s, count=1)
s = re.sub(r'<title>.*?</title>\s*', '', s, count=1, flags=re.S)
s = s.replace("<head>", "<head>\n" + HEAD, 1)

# stylesheets: the site chrome first so the page's own rules win on source order
s = s.replace("<style>", "<style>\n" + chrome_css + "\n</style>\n<style>", 1)
s = s.replace("</style>", CSS + "\n</style>", 1)
s = s.replace("</body>", "<script>\n" + chrome_js + "\n</script>\n"
                         "<script>\n" + JS + "\n</script>\n</body>", 1)

# ----------------------------------------------------------------- guards ---
assert "Prototype." not in s and "noindex" not in s
assert s.count('id="promo"') == 1 and s.count('id="growpromo"') == 1
assert s.count('class="sitenav"') == 1 and 'class="mast"' not in s
assert s.count(TAX) >= 1 and s.count(GROW) >= 1 and s.count(FULL) >= 1
assert s.count("<title>") == 1
assert s.count("<body>") == 1 and s.count("</body>") == 1
# the parked ids must still be unique - a duplicate id silently breaks render()
_ids = re.findall(r'id="([\w-]+)"', s)
_dupes = sorted({i for i in _ids if _ids.count(i) > 1})
assert not _dupes, "duplicate ids: " + ", ".join(_dupes)

open(os.path.join(HERE, SELF), "w").write(s)
print("wrote " + SELF + "", len(s) // 1024, "kB;", len(_ids), "ids, no duplicates")
