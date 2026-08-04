#!/usr/bin/env python3
"""The prototype home page with chapter 04 replaced by a promo block that sells
the tax-strategy page and links to it.

Three intensities of the same block, switchable in the page, because "aggressive
call to action" is a dial rather than a setting and it is easier to pick one by
looking at all three on the same scroll.

Every figure is the prototype's own live output, and the link carries the
reader's setup so the destination is not an empty form.
"""
import os, re
import patches as P

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "..", "proto", "index.html")).read()

KEEP_A = SRC.index('<section class="slab carbon" id="keep">')
KEEP_B = SRC.index('<!-- ===================== 05 BONUS LEVEL')

PROMO = """
<section class="slab carbon" id="keep">
  <div id="promo"></div>

  <div style="display:none" aria-hidden="true" id="parked">PARKED</div>
</section>
"""

# render() writes into every id the old chapter carried. On the real split those
# elements live on the tax-strategy page; here they are kept in the DOM, hidden,
# so the prototype's own script runs untouched. The list is derived from the
# original markup rather than typed, so it cannot drift.
OLD_IDS = sorted(set(re.findall(r'id="([\w-]+)"', SRC[KEEP_A:KEEP_B])) - {"keep"})
PARKED = "".join(
    ('<select id="%s"><option value="single" selected></option></select>' % i)
    if i == "i-filing" else
    ('<input id="%s">' % i) if i.startswith("i-") else
    ('<button id="%s"></button>' % i) if i.startswith("b-") else
    ('<span id="%s"></span>' % i)
    for i in OLD_IDS)
PROMO = PROMO.replace("PARKED", PARKED)

CSS = """
/* ===== mock-up control, not part of the design ===== */
.promo-switch{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 20px;
 padding:0 0 16px;border-bottom:1px dashed rgba(255,255,255,.2)}
.promo-switch b{font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;
 color:rgba(255,255,255,.45);margin-right:6px}
.ps{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);color:#fff;
 border-radius:999px;padding:8px 14px;font:inherit;font-size:12.3px;font-weight:600;
 cursor:pointer;min-height:38px}
.ps.on{background:#F6C560;border-color:#F6C560;color:#2A2010}

/* ===== the promo block itself ===== */
.pr-kick{display:inline-flex;align-items:center;gap:8px;background:rgba(246,197,96,.16);
 border:1px solid rgba(246,197,96,.4);border-radius:999px;padding:7px 15px;font-size:10px;
 font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#F6C560;margin:0 0 15px}
.pr-h{font-family:Fraunces,Georgia,serif;font-weight:600;color:#fff;letter-spacing:-.022em;
 line-height:1.08;margin:0 0 13px}
.pr-h b{color:#F6C560;font-weight:600}
/* capped: 5.4vw at 2560 is 138px in a 1060px block. */
.pr-h.big{font-size:clamp(30px,5vw,62px);max-width:17ch}
.pr-p,.pr-barn,.pr-fine{max-width:68ch}
.pr-h.mid{font-size:clamp(25px,4vw,43px)}
.pr-p{font-size:15px;line-height:1.72;color:rgba(255,255,255,.76);margin:0 0 20px;max-width:62ch}
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
/* the button */
/* Full width of the block and unmissable. clamp() rather than a vw font size:
   on a 27-inch 5K the viewport is 2560 CSS px, and an unclamped 2.2vw headline
   comes out at 56px inside a 1060px block - which looks broken, not bold. */
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
/* the list of what is on the other page */
.pr-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 22px;
 margin:20px 0 0;padding:18px 0 0;border-top:1px solid rgba(255,255,255,.14)}
.pr-list div{display:flex;gap:9px;font-size:12.6px;line-height:1.55;color:rgba(255,255,255,.66)}
.pr-list i{font-style:normal;color:#F6C560;flex:none}
.pr-list b{color:#fff;font-weight:600}
/* B: the split bar */
.pr-bar{display:flex;height:46px;border-radius:11px;overflow:hidden;margin:0 0 9px}
.pr-bar div{display:flex;flex-direction:column;align-items:center;justify-content:center;
 font-size:10.5px;font-weight:800;line-height:1.2;padding:0 6px;text-align:center}
.pr-bar .a{background:rgba(255,255,255,.17);color:#fff}
.pr-bar .b{background:rgba(255,255,255,.08);color:rgba(255,255,255,.66)}
.pr-bar .c{background:#F6C560;color:#2A2010}
.pr-bar strong{font-family:Fraunces,Georgia,serif;font-size:15px;font-weight:600}
.pr-barn{font-size:11.5px;color:rgba(255,255,255,.5);margin:0 0 20px}
/* C: the loss frame */
.pr-loss{background:rgba(200,90,80,.13);border:1px solid rgba(200,90,80,.4);border-radius:14px;
 padding:16px 19px;margin:0 0 18px}
/* direct child only - an inline <b> inside the paragraph was inheriting
   display:block and breaking the sentence across three lines */
.pr-loss > b{display:block;font-family:Fraunces,Georgia,serif;font-size:20px;color:#F0A79E;
 margin:0 0 6px}
.pr-loss p b{color:#F6C560}
.pr-loss p{margin:0;font-size:13px;line-height:1.68;color:rgba(255,255,255,.7);max-width:66ch}
.pr-yrs{display:flex;gap:0;margin:0 0 18px;border-radius:12px;overflow:hidden;
 border:1px solid rgba(255,255,255,.14)}
.pr-yrs div{flex:1;padding:12px 10px;text-align:center;min-width:0;
 border-right:1px solid rgba(255,255,255,.1)}
.pr-yrs div:last-child{border-right:0}
.pr-yrs.hi div:last-child{background:rgba(246,197,96,.15)}
.pr-yrs i{display:block;font-style:normal;font-size:10px;color:rgba(255,255,255,.5)}
.pr-yrs b{display:block;font-family:Fraunces,Georgia,serif;font-size:18px;color:#fff;
 margin-top:4px}
.pr-yrs div:last-child b{color:#F6C560}
.pr-fine{font-size:11.4px;line-height:1.65;color:rgba(255,255,255,.42);margin:16px 0 0;
 max-width:74ch}

/* The prototype's own controls sit under the 38px touch minimum - a real miss
   on a phone, and this page is meant to ship. The classes are .mnav a, .mcta
   and .adj, found by measuring rather than guessed. Height comes out of padding
   so nothing reflows. */
.mnav a,.mcta,.adj,.ghost,.ghost.sm{min-height:38px;display:inline-flex;align-items:center;
 justify-content:center;padding-top:9px;padding-bottom:9px}
@media (max-width:760px){
 .pr-num,.pr-list{grid-template-columns:1fr}
 .pr-cta{width:100%;align-items:center;text-align:center}
 .pr-yrs{flex-wrap:wrap}
 .pr-yrs div{flex-basis:50%;border-bottom:1px solid rgba(255,255,255,.1)}
}
"""

JS = r"""
(function(){
  var V = 2;   /* Aggressive. The A/B/C switcher was a review device. */
  function f(v){ return (window.TREE && TREE.fmt) ? TREE.fmt(v) : "$" + Math.round(v); }
  // The link carries the reader's setup. Without this they land on the tax page
  // with an empty form and have to type everything again, which is the single
  // most likely way this two-page split fails.
  function href(){
    var S = window.__S || {};
    var q = [];
    ["rate","sessions","weeksOff","age","filing","contrib"].forEach(function(k){
      if (S[k] !== "" && S[k] !== undefined && S[k] !== null) q.push(k + "=" + encodeURIComponent(S[k]));
    });
    return "tax-strategy.html" + (q.length ? "#" + q.join("&") : "");
  }
  function list(){
    return '<div class="pr-list">'
      + [["Which account, and what each is worth to you","Solo 401(k), SEP, SIMPLE, IRA"],
         ["How much room you have this year","and why it moves with your profit"],
         ["What it becomes","at a return and a horizon you choose"],
         ["Sole proprietor vs professional corporation","priced, including what it costs your Social Security"],
         ["What hiring associates changes","and what it does not"],
         ["What to actually do, and by when","the deadlines that bite"]
        ].map(function(x){ return '<div><i>&rarr;</i><span><b>' + x[0] + '</b> &mdash; '
          + x[1] + '</span></div>'; }).join("") + '</div>';
  }
  function cta(label, sub){
    return '<a class="pr-cta" href="' + href() + '"><strong>' + label + '</strong>'
      + '<span>' + sub + '</span></a>';
  }
  function draw(){
    var el = document.getElementById("promo"); if(!el) return;
    var t = window.TREE;
    if(!t || t.profit <= 0){
      el.innerHTML = '<p class="pr-kick">Next</p>'
        + '<h2 class="pr-h mid">Put a rate and a caseload in above.</h2>'
        + '<p class="pr-p">Once there is profit on this page, this block works out how much of '
        + 'the tax on it is optional &mdash; and hands you a plan for the rest.</p>' + list();
      return;
    }
    var S = window.__S || {};
    var yrs = 20, r = 0.07;
    var every = t.optional > 0 ? t.optional * ((Math.pow(1+r, yrs) - 1) / r) : 0;
    var own = Math.max(0, t.room - t.optional);
    var pct = t.room > 0 ? Math.round(t.optional / t.room * 100) : 0;

    if (V === 1) {
      /* A - confident. States the number, explains it once, offers the page. */
      el.innerHTML = '<p class="pr-kick">Chapter 04 &middot; Tax &amp; financial strategy</p>'
        + '<h2 class="pr-h mid">You are about to pay <b>' + f(t.tax) + '</b> in tax. '
        + 'Some of that is a choice.</h2>'
        + '<p class="pr-p">Profit is not the end of the arithmetic. A dollar you move into a '
        + 'retirement account is not taxed this year &mdash; you still own it, the tax is '
        + 'postponed rather than cancelled, and meanwhile it compounds. On your numbers that '
        + 'is worth <b>' + f(t.optional) + '</b> this year alone.</p>'
        + '<div class="pr-num">'
        + '<div><i>Tax on this year&rsquo;s profit</i><b>' + f(t.tax) + '</b><u>if you do nothing</u></div>'
        + '<div class="hi"><i>Of that, optional</i><b>' + f(t.optional) + '</b><u>deferred, not avoided</u></div>'
        + '<div><i>Maximum you could contribute</i><b>' + f(t.room) + '</b><u>' + pct + '% funded by tax</u></div>'
        + '</div>'
        + '<div class="pr-row">' + cta("Work out your tax strategy →",
            "about five minutes · nothing is saved · your numbers travel with you")
        + '<p class="pr-second">Opens the full chapter with the figures from this page already '
        + 'filled in.</p></div>' + list();
      return;
    }

    if (V === 2) {
      /* B - aggressive. Leads with the split, names the figure in the button. */
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
        + '<p class="pr-barn">Every dollar you billed this year, split three ways.</p>'
        + '<div class="pr-row">' + cta("Keep " + f(t.optional) + " →",
            "work out your tax strategy · five minutes · nothing is saved")
        + '<p class="pr-second">Your rate, caseload and expenses come with you. You will not '
        + 'type anything twice.</p></div>' + list()
        + '<p class="pr-fine">Deferred, not avoided: you pay the tax when you withdraw, usually '
        + 'decades later and usually at a lower rate. What it costs you is liquidity &mdash; the '
        + 'money is hard to reach before 59&frac12; without a penalty.</p>';
      return;
    }

    /* C - hard sell. Frames it as a loss, and compounds it. */
    el.innerHTML = '<p class="pr-kick">The most expensive page on this site to skip</p>'
      + '<h2 class="pr-h big">Every year you do nothing costs you <b>' + f(t.optional) + '</b>.</h2>'
      + '<div class="pr-loss"><b>And it does not stay ' + f(t.optional) + '.</b>'
      + '<p>That is money leaving your accounts and never compounding. Do it for twenty years '
      + 'and the gap is not twenty times ' + f(t.optional) + ' &mdash; it is '
      + '<b style="color:#F6C560">' + f(every) + '</b>, because the money you did not send to '
      + 'the IRS would have been earning the whole time.</p></div>'
      + '<div class="pr-yrs hi">'
      + '<div><i>This year</i><b>' + f(t.optional) + '</b></div>'
      + '<div><i>After 5 years</i><b>' + f(t.optional * ((Math.pow(1.07,5)-1)/0.07)) + '</b></div>'
      + '<div><i>After 10</i><b>' + f(t.optional * ((Math.pow(1.07,10)-1)/0.07)) + '</b></div>'
      + '<div><i>After 20</i><b>' + f(every) + '</b></div></div>'
      + '<p class="pr-p">You are already doing the hard part &mdash; seeing clients, running the '
      + 'practice, making <b>' + f(t.profit) + '</b> of profit. This is the part that takes an '
      + 'afternoon once and pays every year after.</p>'
      + '<div class="pr-row">' + cta("Stop paying " + f(t.optional) + " a year →",
          "work out your tax strategy · free · nothing is saved · no account")
      + '<p class="pr-second">Everything from this page travels with you.</p></div>' + list()
      + '<p class="pr-fine">Compounded at 7%, before inflation and before tax on the way out. A '
      + 'return is an assumption, not a promise. Deferred means postponed, not cancelled &mdash; '
      + 'and the money is hard to reach before 59&frac12; without a penalty. This is a planning '
      + 'tool, not advice.</p>';
  }
  // The growth chapter gets the same treatment: a block that sells the page
  // rather than a calculator nobody has the inputs for yet.
  function grow(){
    var el = document.getElementById("growpromo"); if(!el) return;
    var S = window.__S || {}, t = window.TREE;
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
        + (worth > 0 ? f(worth) : "&mdash;")
        + '</b><u>' + (worth > 0 ? "your rate \u00d7 how long they stay"
            : "set your rate and average tenure") + '</u></div>'
      + '<div><i>Replace one lost client</i><b>' + (worth > 0 ? f(worth) : "&mdash;")
        + '</b><u>churn costs the same as growth pays</u></div>'
      + '<div><i>Ten more a year</i><b>' + (worth > 0 ? f(worth * 10) : "&mdash;")
        + '</b><u>on the same rate and hours</u></div>'
      + '</div>'
      + '<div class="pr-row">'
      + '<a class="pr-cta" href="' + growHref() + '"><strong>Grow your practice \u2192</strong>'
      + '<span>lead sources, conversion, and what a client is really worth</span></a>'
      + '<p class="pr-second">A projection, not a forecast. Nothing here changes the tax '
      + 'figures above.</p></div>'
      + '<div class="pr-list">'
      + [["What a client is actually worth","rate \u00d7 average tenure, not one session"],
         ["Where your clients come from","directories, referrals, search \u2014 priced separately"],
         ["Your conversion, honestly","views \u2192 enquiries \u2192 booked, at each step"],
         ["How many you need a month","just to stand still against churn"],
         ["What one more a month is worth","over a year, and over five"],
         ["Which channel to fix first","the one losing you the most, not the loudest"]
        ].map(function(x){ return '<div><i>&rarr;</i><span><b>' + x[0] + '</b> &mdash; '
          + x[1] + '</span></div>'; }).join("") + '</div>';
  }
  function growHref(){
    var S = window.__S || {}, q = [];
    ["rate","sessions","tenure","clients","churn"].forEach(function(k){
      if (S[k] !== "" && S[k] !== undefined && S[k] !== null) q.push(k + "=" + encodeURIComponent(S[k]));
    });
    return "grow-your-therapy-practice.html" + (q.length ? "#" + q.join("&") : "");
  }
  window.drawGrow = grow;
  window.drawPromo = function(){ draw(); grow(); };
  draw();
})();
"""

HOOK_ANCHOR = '''    row("Most you can redirect this year", "", fmt(optional), "tot");'''
HOOK = HOOK_ANCHOR + '''

  /* the promo block reads the same computation as everything else */
  window.TREE = {gross:c.gross, costs:runCost, profit:c.profit, tax:c.totalTax, net:c.net,
    room:c.room, contrib:c.contrib, optional:optional, fmt:fmt};
  window.__S = S;
  if (window.drawPromo) window.drawPromo();'''

GROW_A = SRC.index('<!-- ===================== 05 BONUS LEVEL')
GROW_B = SRC.index("</section>", SRC.index('<section class="bonus" id="grow">')) + len("</section>")
GROW_IDS = sorted(set(re.findall(r'id="([\w-]+)"', SRC[GROW_A:GROW_B])) - {"grow"})
GROW_PARK = "".join(
    ('<input id="%s">' % i) if i.startswith("i-") else
    ('<button id="%s"></button>' % i) if i.startswith("b-") else
    ('<span id="%s"></span>' % i)
    for i in GROW_IDS)

GROW = """
<section class="bonus" id="grow"><div class="in">
  <div class="ribbon">Bonus level</div>
  <div id="growpromo"></div>
  <div style="display:none" aria-hidden="true">GROWPARK</div>
</div></section>
""".replace("GROWPARK", GROW_PARK)

s = SRC[:KEEP_A] + PROMO + SRC[KEEP_B:GROW_A] + GROW + SRC[GROW_B:]
assert s.count(HOOK_ANCHOR) == 1
s = s.replace(HOOK_ANCHOR, HOOK, 1)
# The prototype binds $("b-max") with no null guard, and that control lived
# inside the chapter this mock-up moves to its own page. It threw, so render()
# was never wired and the promo sat in its empty state forever. Guard the
# listeners rather than keeping orphan controls on a page that no longer owns
# them.
s = re.sub(r'\$\("(b-max)"\)\.addEventListener',
           r'($("\1") || {addEventListener:function(){}}).addEventListener', s)
s = s.replace("</style>", CSS + "\n</style>", 1)
s = s.replace("</body>", "<script>\n" + JS + "\n</script>\n</body>", 1)
s = s.replace("<body>", '<body>\n<div style="background:#141712;color:#fff;padding:10px 0;'
              'font:600 12.5px/1.6 Inter,system-ui,sans-serif">'
              '<div style="max-width:1080px;margin:0 auto;padding:0 26px">'
              '<b style="color:#F6C560;letter-spacing:.12em;font-size:10px">MOCK-UP</b> &nbsp;'
              '<b style="font-family:Fraunces,Georgia,serif;font-size:15px">Home page with the '
              'tax chapter moved to its own page</b>'
              '<span style="color:rgba(255,255,255,.55);margin-left:10px">Chapter 04 is now a '
              'promo block. Three intensities &mdash; switch between them inside the block.'
              '</span></div></div>', 1)

open(os.path.join(HERE, "promo-home.html"), "w").write(s)
print("wrote promo-home.html", len(s) // 1024, "kB")
