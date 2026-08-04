#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Everything grow-your-therapy-practice.html draws.

The arithmetic is deliberately small, because the honest version of this page is
small: a client is worth your rate times how long they stay, a funnel is three
multiplications, and the only hard question is which of your channels is losing
you the most. Everything else on a growth page is decoration.
"""

JS = r"""
/* ------------------------------------------------------------------ state */
var S = blank();
S.tenure = ""; S.clients = ""; S.churn = "";
S.chan = {pt:{views:"",enq:"",got:""}, web:{views:"",enq:"",got:""},
          ref:{views:"",enq:"",got:""}};

var HASH_KEYS = ["rate","sessions","weeksOff","tenure","clients","churn"];
var CHAN = [["pt","Psychology Today", "or any paid directory"],
            ["web","Your own website", "search, your blog, word of mouth that lands there"],
            ["ref","Referrals", "GPs, past clients, other therapists"]];

function $(id){ return document.getElementById(id); }
function money(v){
  if (!isFinite(v)) return "—";
  var n = Math.round(v);
  return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US");
}
function n0(v){ return isFinite(v) ? Math.round(v).toLocaleString("en-US") : "—"; }
function plural(n, one, many){
  return n0(n) + " " + (Math.round(Math.abs(n)) === 1 ? one : (many || one + "s"));
}
function esc(s){ return String(s == null ? "" : s)
  .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }

function tile(lab, val, sub, cls){
  return '<div class="tl ' + (cls || "") + '"><em>' + lab + '</em><b>' + val + '</b>'
       + (sub ? '<u>' + sub + '</u>' : '') + '</div>';
}

/* ------------------------------------------------------------- the maths
   One place, pure, so nothing on the page can quietly compute its own version
   of "what a client is worth". */
/* ---------------------------------------------------------- seasonality ---
   Everything else on this page is an ANNUAL average, which is exactly why a
   caseload plan built from it fails in practice: the year is not flat. Enquiries
   collapse over the December holidays and again in high summer, and January is
   the single biggest intake month most private practices see.

   The model is deliberately simple and legible: twelve multipliers against the
   annual average enquiry rate, normalised so they always average 1.0. That
   normalisation matters - without it, picking a "spiky" shape would silently
   change the annual total and every figure elsewhere on the page would move for
   no reason the reader could see.

   These are SHAPES, not data. The site does not print unsourced figures as
   fact, so they are presented as editable starting points with the reasoning
   stated, and the reader can drag any month. */
var MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var SHAPES = {
  flat:    {name:"Flat", note:"no seasonality - the annual average, every month",
            v:[1,1,1,1,1,1,1,1,1,1,1,1]},
  typical: {name:"Typical private practice",
            note:"January surge, a summer dip, and December off a cliff",
            v:[1.45,1.20,1.10,1.05,1.00,0.85,0.70,0.80,1.15,1.10,0.95,0.55]},
  school:  {name:"Children and families",
            note:"follows the school year - dead in summer, heavy in September",
            v:[1.35,1.15,1.10,1.05,0.95,0.60,0.45,0.75,1.50,1.25,1.05,0.60]},
  steady:  {name:"Mostly steady",
            note:"a mild shape - some holiday softness, nothing dramatic",
            v:[1.15,1.05,1.05,1.00,1.00,0.95,0.90,0.90,1.05,1.05,1.00,0.80]}
};

function shapeOf(){
  var k = S.shape || "typical";
  var base = (SHAPES[k] || SHAPES.typical).v.slice();
  /* a reader-edited month overrides the preset for that month only */
  if (S.months) for (var i = 0; i < 12; i++)
    if (S.months[i] !== "" && S.months[i] != null && isFinite(+S.months[i]))
      base[i] = Math.max(0, +S.months[i] / 100);
  /* NORMALISE. Without this the annual total moves when the shape changes, and
     every other figure on the page shifts for a reason nobody can see. */
  var sum = base.reduce(function(a, b){ return a + b; }, 0);
  var mean = sum / 12;
  return mean > 0 ? base.map(function(x){ return x / mean; }) : base;
}

/* Month by month: how many clients arrive, how many leave, and where the
   caseload actually sits. Churn is treated as flat - people do not stop coming
   because it is July - which is exactly why a seasonal intake plus flat churn
   produces the summer trough this chart exists to show. */
function monthly(g){
  var shape = shapeOf();
  var perMonthIn = g.got / 12;          /* annual new clients, averaged */
  var perMonthOut = g.churn / 12;
  var load = g.clients, out = [], lo = Infinity, hi = -Infinity, loM = 0, hiM = 0;
  for (var i = 0; i < 12; i++){
    var arrive = perMonthIn * shape[i];
    load = Math.max(0, load + arrive - perMonthOut);
    out.push({m: MONTHS[i], mult: shape[i], arrive: arrive,
              leave: perMonthOut, load: load,
              /* the number the reader can act on: leads needed THIS month to
                 stand still, given this month's conversion reality */
              need: g.conv > 0 ? perMonthOut / g.conv : NaN});
    if (load < lo){ lo = load; loM = i; }
    if (load > hi){ hi = load; hiM = i; }
  }
  return {rows: out, low: lo, lowMonth: MONTHS[loM],
          high: hi, highMonth: MONTHS[hiM],
          swing: hi - lo,
          /* capacity is a weekly session count, so a month at capacity is the
             same ceiling every month - the trough and the peak are both
             measured against it */
          overMonths: out.filter(function(r){
            return g.capacity > 0 && r.load > g.capacity; }).length};
}

function grow(){
  var rate = num(S.rate), tenure = num(S.tenure);
  var worth = rate * tenure;                 /* one client, over their whole time */
  var clients = num(S.clients), churn = num(S.churn);
  var weeks = Math.max(1, 52 - num(S.weeksOff));
  var sessions = num(S.sessions);

  var chans = CHAN.map(function(c){
    var d = S.chan[c[0]] || {};
    var v = num(d.views), e = num(d.enq), g = num(d.got);
    return {
      key: c[0], name: c[1], note: c[2], views: v, enq: e, got: g,
      /* Two conversions, and they fail for different reasons. A low
         views-to-enquiry rate is a listing problem. A low enquiry-to-client
         rate is a first-contact problem. Averaging them hides which. */
      toEnq: v > 0 ? e / v : NaN,
      toClient: e > 0 ? g / e : NaN,
      overall: v > 0 ? g / v : NaN,
      value: g * worth,
      /* Enquiries you got and did not convert. This is the only "lost money"
         figure on the page that is actually countable. */
      missed: Math.max(0, e - g)
    };
  });
  var views = 0, enq = 0, got = 0;
  chans.forEach(function(c){ views += c.views; enq += c.enq; got += c.got; });
  var conv = enq > 0 ? got / enq : NaN;

  /* Standing still is not free: you need `churn` new clients a month simply to
     stay where you are, and at your conversion rate that is a number of
     enquiries, which is the number you can actually go and change. */
  var needClients = churn;
  var needEnq = isFinite(conv) && conv > 0 ? churn / conv : NaN;
  var needViews = views > 0 && enq > 0 ? needEnq / (enq / views) : NaN;

  var capacity = sessions > 0 && tenure > 0 ? sessions : 0;
  var fill = capacity > 0 ? Math.min(1, clients / capacity) : 0;

  return {
    rate: rate, tenure: tenure, worth: worth, clients: clients, churn: churn,
    weeks: weeks, sessions: sessions,
    chans: chans, views: views, enq: enq, got: got, conv: conv,
    net: got - churn,
    needClients: needClients, needEnq: needEnq, needViews: needViews,
    bookValue: worth * clients,
    capacity: capacity, fill: fill,
    /* what one more client a month is worth, which is the only growth number
       most people actually act on */
    onePerMonth: worth * 12,
    ready: views > 0 || enq > 0 || got > 0
  };
}

/* attach the monthly view to whatever grow() returned, so callers get one
   object and the seasonality cannot silently disagree with the annual figures
   it was derived from */
var _grow = grow;
grow = function(){ var g = _grow(); g.monthly = monthly(g); return g; };

/* ---------------------------------------------------------------- drawing */
function drawWorth(g){
  var el = $("worthout"); if (!el) return;
  if (!(g.worth > 0)){
    el.innerHTML = '<p class="empty">Put your session rate and how many sessions a client '
      + 'typically has above. Everything on this page is built from those two numbers '
      + 'multiplied together — that is what a client is worth, and almost nobody in private '
      + 'practice knows the figure.</p>';
    return;
  }
  el.innerHTML = '<div class="eq">'
    + '<div class="ei"><em>Your rate</em><b>' + money(g.rate) + '</b></div>'
    + '<div class="eo">×</div>'
    + '<div class="ei"><em>Sessions they stay for</em><b>' + n0(g.tenure) + '</b></div>'
    + '<div class="eo">=</div>'
    + '<div class="ei"><em>What one client is worth</em><b class="gold">'
      + money(g.worth) + '</b></div></div>'
    + '<div class="tiles">'
    + tile("Lose one client", money(g.worth), "that is the cost, not one session", "warn")
    + tile("Add one a month, for a year", money(g.onePerMonth),
           "same rate, same hours", "hi")
    + (g.clients > 0
       ? tile("Billing still to come", money(g.bookValue),
              n0(g.clients) + " current clients × " + money(g.worth) + " each")
       : tile("Your current caseload", "—", "enter how many clients you hold"))
    + '</div>'
    + '<p class="note">This is the number that makes marketing arithmetic instead of '
    + 'anxiety. A directory listing at ' + money(40) + ' a month is worth it if it brings you '
    + 'one client every ' + Math.max(1, Math.round(g.worth / 480)) + ' years. It almost '
    + 'certainly does better than that.</p>';
}

function drawFunnel(g){
  var el = $("funnel"); if (!el) return;
  if (!g.ready){
    el.innerHTML = '<p class="empty">Fill in last month for each place your clients come '
      + 'from. Rough numbers are fine — the point is which channel is losing you people, '
      + 'and that shows up even when the counts are approximate.</p>';
    return;
  }
  /* Which channel to fix first is NOT the one with the lowest conversion - it
     is the one where the most people fell out, because that is where the
     recoverable clients actually are. */
  var worst = null;
  g.chans.forEach(function(c){
    if (c.enq > 0 && (!worst || c.missed > worst.missed)) worst = c;
  });

  var s = '<div class="stages">';
  [["Saw you", g.views], ["Enquired", g.enq], ["Became clients", g.got]].forEach(
    function(st, i){
      var pct = g.views > 0 ? Math.max(6, st[1] / g.views * 100) : 100;
      s += '<div class="stg" style="--w:' + pct.toFixed(1) + '%"><em>' + st[0] + '</em>'
         + '<b>' + n0(st[1]) + '</b>'
         + (i > 0 && g.views > 0
            ? '<i>' + Math.round(st[1] / g.views * 100) + '% of the top</i>' : '')
         + '</div>';
    });
  s += '</div>';
  if (g.worth > 0){
    s += '<p class="barn">Those ' + n0(g.got) + ' clients are worth <b>'
       + money(g.got * g.worth) + '</b> over their time with you — from one month of a '
       + 'funnel you can change.</p>';
  }

  s += '<div class="chans">' + g.chans.map(function(c){
    var flag = worst && c.key === worst.key && c.missed > 0;
    return '<div class="ch' + (flag ? ' fix' : '') + '">'
      + '<div class="chh"><b>' + c.name + '</b>'
      + (flag ? '<span class="gpill">fix this one first</span>' : '') + '</div>'
      + '<p class="chn2">' + c.note + '</p>'
      + '<div class="chrow"><span>Saw you</span><b>' + n0(c.views) + '</b></div>'
      + '<div class="chrow"><span>Enquired</span><b>' + n0(c.enq) + '</b>'
      + (isFinite(c.toEnq) ? '<i>' + Math.round(c.toEnq * 100) + '%</i>' : '<i>—</i>')
      + '</div>'
      + '<div class="chrow"><span>Became clients</span><b>' + n0(c.got) + '</b>'
      + (isFinite(c.toClient) ? '<i>' + Math.round(c.toClient * 100) + '%</i>' : '<i>—</i>')
      + '</div>'
      + (c.got > 0 && g.worth > 0
         ? '<p class="chv">Worth <b>' + money(c.value) + '</b> over their time with you</p>'
         : '<p class="chv">Not scored yet</p>')
      + (c.missed > 0 && g.worth > 0
         ? '<p class="chm">' + n0(c.missed) + ' enquired and did not become clients. At '
           + money(g.worth) + ' each that is <b>' + money(c.missed * g.worth)
           + '</b> that walked past the door.</p>' : '')
      + '</div>';
  }).join("") + '</div>';

  s += '<p class="fine">The two percentages are different problems. <b>Saw you → enquired</b> '
    + 'is your listing, your photo and your first paragraph. <b>Enquired → became a client</b> '
    + 'is what happens in the next 48 hours: how fast you reply, whether there is a real '
    + 'time on offer, and whether the fee was a surprise. The second one is nearly always '
    + 'cheaper to fix.</p>';
  el.innerHTML = s;
}

function drawNeed(g){
  var el = $("needout"); if (!el) return;
  if (!(g.churn > 0)){
    el.innerHTML = '<p class="empty">Put in how many clients you lose in a typical month — '
      + 'people finish, move, or stop. Every practice has the number and almost nobody '
      + 'writes it down. It is what decides how much marketing you actually need.</p>';
    return;
  }
  var s = '<div class="tiles">'
    + tile("Clients you lose a month", n0(g.churn), "people get better; that is the job")
    + tile("New clients just to stand still", n0(g.needClients),
           "before any growth at all", "warn")
    + (isFinite(g.needEnq)
       ? tile("Enquiries that takes", n0(Math.ceil(g.needEnq)),
              "at your " + Math.round(g.conv * 100) + "% enquiry-to-client rate", "hi")
       : tile("Enquiries that takes", "—", "fill in your funnel above"))
    + (isFinite(g.needViews)
       ? tile("People who need to see you", n0(Math.ceil(g.needViews)),
              "a month, at your current listing performance")
       : "")
    + '</div>';

  if (g.got > 0){
    var net = g.net;
    /* A naive net x 12 is how a growth page ends up promising a 25-session week
       144 new clients a year. Growth stops at capacity - past that the arrivals
       are a waiting list, not income - so the projection is capped and the
       sentence says which of the two it is. */
    var room = g.capacity > 0 ? Math.max(0, g.capacity - g.clients) : Infinity;
    var monthsToFull = (net > 0 && isFinite(room)) ? room / net : Infinity;
    var realYear = net > 0 ? Math.min(net * 12, isFinite(room) ? room : net * 12) : net * 12;
    s += '<div class="verdict ' + (net > 0 ? "good" : net === 0 ? "flat" : "bad") + '">'
      + '<em>Last month, arrivals against departures</em><b>'
      + (net > 0 ? "+" + plural(net, "client") : net === 0 ? "Level"
         : plural(net, "client"))
      + '</b><p>' + (net > 0
        ? (isFinite(monthsToFull) && monthsToFull <= 12
           ? 'You are growing faster than your week can hold. There is room for '
             + plural(room, "more client") + ', so at this rate you are <b>full in '
             + (monthsToFull < 1 ? 'under a month'
                : plural(Math.ceil(monthsToFull), "month")) + '</b>'
             + (g.worth > 0 ? ' — worth ' + money(realYear * g.worth)
                 + ', and then the arrivals become a waiting list rather than income' : '')
             + '. That is a good problem, and it is a capacity problem, not a marketing one.'
           : 'You are growing. At this rate you add ' + plural(net * 12, "client")
             + ' over a year'
             + (g.worth > 0 ? ', worth ' + money(net * 12 * g.worth)
                 + ' over their time with you' : '') + '.')
        : net === 0
        ? 'You are exactly replacing what you lose. That is a stable practice and it is also '
          + 'a practice that does not grow — every new client is covering a departure.'
        : 'You are shrinking by ' + plural(-net, "client") + ' a month. Over a year that is '
          + plural(-net * 12, "client")
          + (g.worth > 0 ? ', or ' + money(-net * 12 * g.worth)
             + ' of billing that does not arrive' : '') + '. This is the number to fix '
          + 'before anything else on this page.') + '</p></div>';
  }
  el.innerHTML = s;
}

function drawCapacity(g){
  var el = $("capout"); if (!el) return;
  if (!(g.clients > 0 && g.sessions > 0)){
    el.innerHTML = '<p class="empty">Set your sessions a week and how many clients you '
      + 'currently hold, and this works out how full your week actually is — and what the '
      + 'ceiling is before growth stops being a marketing question and starts being a '
      + 'capacity one.</p>';
    return;
  }
  var room = Math.max(0, g.capacity - g.clients);
  var pct = Math.round(g.fill * 100);
  el.innerHTML = '<div class="fillbar"><i style="width:' + pct + '%"></i>'
      + '<span>' + pct + '% full</span></div>'
    + '<div class="tiles">'
    + tile("Clients you hold", n0(g.clients), "seen weekly or thereabouts")
    + tile("What your week carries", n0(g.capacity),
           n0(g.sessions) + " sessions a week")
    + (room > 0
       ? tile("Room left", plural(room, "client"),
              g.worth > 0 ? "worth " + money(room * g.worth) + " if you filled it" : "", "hi")
       : tile("Room left", "None", "you are full", "warn"))
    + '</div>'
    + '<p class="note">' + (room > 0
      ? 'Filling the week is the cheapest growth there is — no new rate, no new hours, no '
        + 'new anything. Past that point the levers change: raise the rate, add a group, or '
        + 'take on an associate. The simulator prices all three.'
      : 'You are at capacity, so more marketing will not make you more money — it will make '
        + 'you a waiting list. From here the levers are the rate, a group, or an associate.')
    + '</p>';
}

function render(){
  var g = grow();
  drawWorth(g); drawFunnel(g); drawNeed(g); drawCapacity(g);
  /* NOT em-dashes. Two 38px figures above the fold rendering as dashes is a
     caption for a number that is not there, at the exact moment a cold reader
     is deciding whether to stay. The zero state shows the page's own worked
     example - a $200 hour over 24 sessions, so one client is worth $4,800 and
     one more a month over a year is twelve of them - and the tag under them
     says which. Both swap to the reader's the instant a field is touched. */
  var real = g.worth > 0;
  var hw = $("heroworth");
  if (hw) hw.textContent = real ? money(g.worth) : "$4,800";
  var hy = $("heroyear");
  if (hy) hy.textContent = real ? money(g.onePerMonth) : "$57,600";
  var eg = $("heroeg"); if (eg) eg.hidden = real;
  writeHash();
}

/* ---------------------------------------------------- URL round-trip ----- */
var lock = false;
function writeHash(){
  if (lock) return;
  var q = [];
  HASH_KEYS.forEach(function(k){
    if (S[k] === "" || S[k] == null) return;
    q.push(k + "=" + encodeURIComponent(S[k]));
  });
  CHAN.forEach(function(c){
    ["views","enq","got"].forEach(function(f){
      var v = S.chan[c[0]][f];
      if (v !== "" && v != null) q.push(c[0] + "_" + f + "=" + encodeURIComponent(v));
    });
  });
  try { history.replaceState(null, "", "#" + q.join("&")); } catch (e) {}
}
function readHash(){
  var raw = location.hash.replace(/^#/, "");
  if (!raw || raw.indexOf("=") < 0) return;
  lock = true;
  raw.split("&").forEach(function(p){
    var i = p.indexOf("="); if (i < 0) return;
    var k = p.slice(0, i), v = decodeURIComponent(p.slice(i + 1));
    if (HASH_KEYS.indexOf(k) >= 0){ S[k] = v; return; }
    var m = k.match(/^(pt|web|ref)_(views|enq|got)$/);
    if (m) S.chan[m[1]][m[2]] = v;
  });
  lock = false;
}
function bind(id, get, set){
  var el = $(id); if (!el) return;
  var v = get();
  if (v !== "" && v != null) el.value = v;
  el.addEventListener("input", function(){ set(el.value); render(); });
}
function boot(){
  readHash();
  HASH_KEYS.forEach(function(k){
    bind("i-" + k, function(){ return S[k]; }, function(v){ S[k] = v; });
  });
  CHAN.forEach(function(c){
    ["views","enq","got"].forEach(function(f){
      bind("i-" + c[0] + "_" + f, chanGet(c[0], f), chanSet(c[0], f));
    });
  });
  window.addEventListener("hashchange", function(){
    if (location.hash.indexOf("=") < 0) return;
    readHash();
    HASH_KEYS.forEach(function(k){ var e = $("i-" + k); if (e) e.value = S[k]; });
    CHAN.forEach(function(c){ ["views","enq","got"].forEach(function(f){
      var e = $("i-" + c[0] + "_" + f); if (e) e.value = S.chan[c[0]][f]; }); });
    render();
  });
  render();
}
/* Closures, not a loop variable: three channels x three fields all binding to
   the same `f` is the classic way this silently wires nine inputs to one. */
function chanGet(k, f){ return function(){ return S.chan[k][f]; }; }
function chanSet(k, f){ return function(v){ S.chan[k][f] = v; }; }

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
"""
