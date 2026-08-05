#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Everything the page draws. Reads the engine, never recomputes.

Section order is the one the reader asked for and it is not arbitrary:
profit is recapped first, then deferral is explained and sold, then the plan is
made, and only then does the structure question appear. Leading with
sole-prop-versus-S-corp is how every other tool does it and it is backwards -
it is the smaller lever, it is the one that depends on the retirement decision,
and it is the one a reader cannot evaluate until they know what deferral is
worth to them.
"""

JS = r"""
/* ------------------------------------------------------------------ state */
var S = blank();
S.weeksOff = 2; S.filing = "single";
/* The engine defaults card/billing fees to 2.5% of collections. On this page
   the reader is asked for ONE monthly total, so adding a percentage on top of
   it would silently inflate their costs. It stays in the hash so a hand-off
   from the simulator keeps the real figure. */
S.billingPct = 0;
S.retRet = 7; S.retYrs = "";        /* assumed return, and years to invest */
S.expMonth = "";                    /* one bucket, mapped into exp.misc */
S.salPct = 50;                      /* S-corp salary, as a share of profit */
S.a_spare = "most"; S.a_staff = "none"; S.a_admin = "low"; S.a_age = "far";
/* Pre-tax IRA, SEP and SIMPLE balances. The backdoor Roth card cannot answer
   honestly without it: with a balance the conversion is partly taxable, and
   assuming zero would tell most readers it is free when it is not. Blank is a
   real answer here and is treated as zero. */
S.pretaxIra = "";

var HASH_KEYS = ["rate","sessions","weeksOff","billingPct","expMonth","filing","age",
                 "contrib","retRet","retYrs","salPct","a_spare","a_staff","a_admin","a_age",
                 "pretaxIra"];

function $(id){ return document.getElementById(id); }
function money(v){
  if (!isFinite(v)) return "—";
  var n = Math.round(v);
  return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US");
}
function pc(v){ return Math.round(v * 100) + "%"; }
function esc(s){ return String(s == null ? "" : s)
  .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }

/* The single monthly-costs field is mapped onto the engine's expense object so
   compute() is used completely unmodified. A reader who arrived from the
   simulator already has a real twelve-category breakdown; this page only needs
   the total, and asking for twelve fields again would lose them.

   BUT the two are not interchangeable, and flattening the detail into one
   bucket silently changed the answer. compute() treats HEALTH INSURANCE as a
   Schedule 1 deduction, not a Schedule C expense - it does not reduce practice
   profit, it comes off later. Rolled into `misc` it did reduce profit, so a
   reader arriving from the home page with $520/mo of cover saw their profit
   fall by $6,240 crossing the link. Same inputs, two answers, no error.

   So: if the twelve categories arrived, they are kept and the single field is
   display-only. The moment the reader edits that field they have chosen the
   simple model, and the detail is dropped. */
function syncExpenses(){
  if (S._detail) return;
  EXPENSES.forEach(function(e){ S.exp[e[0]] = ""; });
  S.exp.misc = num(S.expMonth);
}

/* ----------------------------------------------------------------- drawing */
function tile(lab, val, sub, cls){
  return '<div class="tl ' + (cls || "") + '"><em>' + lab + '</em><b>' + val + '</b>'
       + (sub ? '<u>' + sub + '</u>' : '') + '</div>';
}
function row(lab, note, amt, cls){
  return '<div class="rw ' + (cls || "") + '"><div><b>' + lab + '</b>'
       + (note ? '<i>' + note + '</i>' : '') + '</div><div class="v">' + amt + '</div></div>';
}

/* ---------------------------------------------------------------- 01 recap */
function drawRecap(c){
  var el = $("recap"); if (!el) return;
  if (!c || c.profit <= 0){
    el.innerHTML = '<p class="empty">Put your rate and caseload in above. Everything on this '
      + 'page is built from your profit, so until there is some, there is nothing here to '
      + 'plan with.</p>';
    return;
  }
  el.innerHTML = '<div class="eq">'
    + '<div class="ei"><em>What you bill</em><b>' + money(c.gross) + '</b></div>'
    + '<div class="eo">−</div>'
    + '<div class="ei"><em>What it costs to run</em><b class="neg">' + money(c.expenses)
      + '</b></div>'
    + '<div class="eo">=</div>'
    + '<div class="ei"><em>Profit</em><b class="gold">' + money(c.profit) + '</b></div>'
    + '</div>'
    + (S._detail
       ? '<p class="note">Your twelve expense categories came across from the simulator, '
         + 'health insurance included &mdash; which is why this profit matches the figure '
         + 'you saw there exactly. Type in the monthly total above and this page switches '
         + 'to that single number instead.</p>' : '')
    + '<p class="note">' + Math.round(c.weeks * num(S.sessions)).toLocaleString("en-US") + ' sessions over ' + c.weeks
    + ' working weeks, at ' + money(num(S.rate)) + ' each. This is the number every figure '
    + 'below is built from — change anything above and the whole page moves.</p>';
}

/* ------------------------------------------------------- 02 what deferral is
   The sell. Three-way split of every dollar billed, then the same money
   compounded, at a return and a horizon the reader chose rather than inherited. */
function drawSell(c0, best){
  var el = $("sell"); if (!el) return;
  if (!c0 || c0.profit <= 0){ el.innerHTML = ""; return; }
  var optional = best ? best.saved : 0;
  var fixed = Math.max(0, c0.totalTax - optional);
  var keep = Math.max(0, c0.profit - c0.totalTax);
  var tot = Math.max(1, keep + fixed + optional);
  var yrs = num(S.retYrs) || yearsToRetire(S) || 20;
  var r = num(S.retRet) || 7;
  var becomes = futureValue(best ? best.room : 0, r, yrs);

  el.innerHTML =
      '<div class="bar">'
    + '<div class="a" style="width:' + Math.round(keep / tot * 100) + '%">yours either way'
      + '<strong>' + money(keep) + '</strong></div>'
    + '<div class="b" style="width:' + Math.round(fixed / tot * 100) + '%">tax you owe'
      + '<strong>' + money(fixed) + '</strong></div>'
    + '<div class="c" style="width:' + Math.round(optional / tot * 100) + '%">your call'
      + '<strong>' + money(optional) + '</strong></div></div>'
    + '<p class="barn">Every dollar of profit, split three ways. The gold slice is the part '
    + 'you decide.</p>'
    + '<div class="tiles">'
    + tile("Tax on this profit", money(c0.totalTax), "if you do nothing at all")
    + tile("Of that, optional", money(optional), "deferred, not avoided", "hi")
    + tile("Max it out and it becomes", money(becomes),
           "at " + r + "% over " + yrs + " years, before inflation")
    + '</div>'
    + '<p class="fine"><b>Deferred is postponed, not cancelled.</b> You pay the tax when you '
    + 'withdraw — usually decades later, usually at a lower rate, and on money that has '
    + 'been compounding the whole time. What it actually costs you is liquidity: getting at '
    + 'it before 59½ generally means a 10% penalty on top of the tax. That is the trade, '
    + 'stated plainly, and it is the reason this is a decision rather than a trick.</p>';
}

/* ------------------------------------------------------------- 03 the plan */
function drawPlan(c0, cNow, strat){
  var el = $("planout"); if (!el) return;
  if (!c0 || c0.profit <= 0){ el.innerHTML = ""; return; }
  var room = c0.room;
  var maxRun = compute(S, room);
  var maxSaved = Math.max(0, c0.totalTax - maxRun.totalTax);
  var contrib = Math.min(num(S.contrib), room);
  var saved = Math.max(0, c0.totalTax - cNow.totalTax);
  var yrs = num(S.retYrs) || yearsToRetire(S) || 20;
  var r = num(S.retRet) || 7;

  el.innerHTML = '<div class="tiles">'
    + tile("The most you can put away", money(room),
           "a Solo 401(k) on this profit", "big")
    + tile("Tax that removes", money(maxSaved), "you would otherwise pay this April", "good")
    + tile("So it costs you", money(Math.max(0, room - maxSaved)),
           "of spendable cash, not " + money(room))
    + '</div>'
    + '<p class="note">' + pc(room > 0 ? maxSaved / room : 0) + ' of the maximum contribution '
    + 'is funded by tax you were going to pay anyway. That is the whole idea: the government '
    + 'is a minority shareholder in your retirement account whether you use it or not.</p>'
    + (contrib > 0
      ? '<div class="cur"><b>At the ' + money(contrib) + ' you have entered</b>'
        + '<span>tax falls by ' + money(saved) + ', it costs you '
        + money(Math.max(0, contrib - saved)) + ', and in ' + yrs + ' years at ' + r + '% it '
        + 'is ' + money(futureValue(contrib, r, yrs)) + '.</span>'
        + (contrib < room
           ? '<span class="gap">You are leaving ' + money(room - contrib) + ' of room unused, '
             + 'which is ' + money(Math.max(0, maxSaved - saved)) + ' of tax you have chosen '
             + 'to pay.</span>' : '<span class="gap done">Maxed out.</span>')
        + '</div>'
      : '<div class="cur"><b>Nothing entered yet</b><span>Put a figure in, or press '
        + '“Max it out”, and this line prices it.</span></div>');
}

/* ------------------------------------------------------- 04 the sorting bar
   Not a wizard. Four answers at the top; every account stays on the page and
   re-orders around them. A ruled-out option is greyed rather than removed,
   because the REASON it is out is the useful part. */
var QS = [
  {k:"a_spare", lab:"Spare profit",
   opts:[["most","Most of it"],["some","Some"],["none","None"]]},
  {k:"a_staff", lab:"Employees", opts:[["none","Just me"],["some","I have staff"]]},
  {k:"a_admin", lab:"Admin appetite",
   opts:[["low","Keep it simple"],["ok","Payroll is fine"]]},
  {k:"a_age", lab:"Years to 67", opts:[["far","20 or more"],["near","Under 10"]]}
];

function accountCards(strat){
  var by = {};
  strat.forEach(function(o){ by[o.id] = o; });
  var spare = S.a_spare, staff = S.a_staff;
  /* A share of profit the reader says is actually spare. "Some" is read as
     half, and the block says so rather than quietly halving the number. */
  var share = spare === "most" ? 1 : spare === "some" ? .5 : 0;

  return [
    {id:"solo", title:"Solo 401(k)",
     sub:"Your deferral plus an employer contribution, out of the same profit",
     o:by.solo, share:share,
     inPlay: spare !== "none" && staff === "none",
     out: staff !== "none"
       ? "You have staff. A Solo 401(k) is only for a practice with no employees other than a spouse — hiring one associate closes it."
       : "You said there is no spare profit, so there is nothing to shelter.",
     detail: function(o){
       return '<p>Room of <b>' + money(o.room) + '</b>: ' + money(o.deferral)
         + ' as the employee, plus ' + money(o.employer) + ' as the employer — 20% of '
         + money(strat.netSE) + ' of net self-employment earnings. Both halves are your money; '
         + 'the plan simply counts them separately.</p>'
         + '<ul><li>The plan has to <b>exist</b> before you can fund it. That is the deadline '
         + 'that catches people, not the contribution date.</li>'
         + '<li>The employee and employer halves have different cut-offs.</li>'
         + '<li>Hire anyone who is not your spouse and this stops being available.</li></ul>';
     }},
    {id:"sep", title:"SEP IRA",
     sub:"Employer-funded only, and it can be opened after the year has ended",
     o:by.sep, share:share,
     inPlay: spare !== "none",
     out:"You said there is no spare profit, so there is nothing to shelter.",
     detail: function(o){
       return '<p>20% of ' + money(strat.netSE) + ' is <b>' + money(o.room) + '</b>. Less room '
         + 'than the Solo 401(k), because there is no employee half — but it can be '
         + 'opened <b>and</b> funded right up to your filing deadline, extensions included. '
         + 'That is what makes it the usual answer when the year is already over.</p>'
         + '<ul><li>No annual filing and nothing to set up in advance.</li>'
         + '<li>Hire anyone later and you generally owe them the same percentage.</li></ul>';
     }},
    {id:"simple", title:"SIMPLE IRA",
     sub:"A deferral plus a mandatory 3% match, built for a practice with staff",
     o:by.simple, share:share,
     inPlay: staff === "some" && spare !== "none",
     out: spare === "none" ? "No spare profit to shelter."
       : "With no employees the Solo 401(k) beats it on room at the same effort, so it is only worth a look once you have staff.",
     detail: function(o){
       return '<p>' + money(o.deferral) + ' as your deferral plus a 3% match of '
         + money(o.match) + ', giving <b>' + money(o.room) + '</b>. The match is mandatory and '
         + 'you owe it to every eligible employee, not only yourself — which is the cost '
         + 'that makes this the right answer for some practices and the wrong one for others.</p>'
         + '<ul><li>A SIMPLE and a Solo 401(k) cannot share a year.</li>'
         + '<li>Must generally be set up by 1 October for that year.</li></ul>';
     }},
    {id:"ira", title:"Traditional IRA",
     sub:"Available to everyone, and at this profit usually the smallest lever",
     o:by.ira, share:share,
     inPlay: spare !== "none",
     out:"No spare profit to shelter.",
     detail: function(o){
       var covered = o.coveredFrac;
       return '<p>' + money(o.room) + ' of room. Whether it is <b>deductible</b> is the part '
         + 'people get wrong, and it turns on one question: are you covered by a retirement '
         + 'plan at work?</p><ul>'
         + '<li><b>No plan at all</b> — fully deductible, whatever you earn. Worth '
         + money(o.saved) + ' to you.</li>'
         + '<li><b>You also have a Solo 401(k) or SEP</b> — you are covered, and at this '
         + 'income the deduction is '
         + (covered <= 0 ? 'gone entirely.'
            : covered >= 1 ? 'still whole.'
            : 'phased down to about ' + money(o.deductibleIfCovered) + '.')
         + '</li>'
         + '<li>A non-deductible contribution is not worthless — it is the first step of '
         + 'a backdoor Roth — but it is not a deduction this year.</li></ul>';
     }},
    /* Roth and the backdoor arrive last because they are the two the reader is
       most likely to have heard of and least likely to have priced. Neither
       saves tax this year, which is the point, and the card says so first so
       nobody reads a $0 saving as a broken calculation. */
    {id:"roth", title:"Roth IRA",
     sub:"No deduction now — the trade is tax-free growth instead",
     o:by.roth, share:share,
     inPlay: spare !== "none" && by.roth.room > 0,
     out: by.roth && by.roth.room <= 0
       ? "At this profit you are over the income limit for a direct Roth contribution. The backdoor below is the route that stays open."
       : "No spare profit to shelter.",
     detail: function(o){
       return '<p><b>This saves you nothing this April, and that is the whole idea.</b> '
         + 'You pay the tax now so the growth and the withdrawals come out untaxed later. '
         + 'Every other account on this page does the opposite.</p>'
         + '<p>Room of <b>' + money(o.room) + '</b>'
         + (o.eligibleFrac >= 1
            ? ', the full limit — your income is under the phase-out.'
            : o.eligibleFrac <= 0
              ? '. Your income is above the phase-out, so a direct contribution is closed.'
              : ' — the limit phased down, because your income sits inside the range where '
                + 'eligibility tapers. ' + money(o.phasedOut) + ' of the limit is unavailable '
                + 'directly.')
         + '</p><ul>'
         + '<li>The Roth income test is <b>not</b> the Traditional deduction test. That one '
         + 'asks whether you have a plan at work; this one asks only what you earn.</li>'
         + '<li>Whether it beats a deduction is a bet on your tax rate in retirement '
         + 'against your rate today. Nobody on this page can settle that for you.</li></ul>';
     }},
    {id:"backdoor", title:"Backdoor Roth",
     sub:"The route that stays open when the front door closes",
     o:by.backdoor, share:share,
     inPlay: spare !== "none",
     out:"No spare profit to shelter.",
     detail: function(o){
       var clean = o.taxableOnConversion <= 0.5;
       return '<p>A non-deductible contribution to a Traditional IRA, converted to a Roth '
         + 'straight afterwards. There is no income limit on the conversion, which is why '
         + 'it works when a direct Roth does not.</p>'
         + '<p><b>The catch is the pro-rata rule</b>, and it is the reason this goes wrong '
         + 'for people. The IRS does not let you convert only the after-tax dollars. It '
         + 'looks at <em>every</em> Traditional, SEP and SIMPLE IRA you own and taxes the '
         + 'same proportion of your conversion.</p>'
         + (clean
            ? '<p class="pay-note"><b>On the balance you entered, the conversion is tax-free.</b> '
              + 'With no other pre-tax IRA money there is nothing to prorate against.</p>'
            : '<p class="pay-note"><b>' + Math.round(o.taxableFrac * 100) + '% of your '
              + 'conversion would be taxable</b> — ' + money(o.taxableOnConversion)
              + ' of income, costing roughly ' + money(o.conversionTax) + ' in federal tax — '
              + 'because you hold ' + money(o.pretax) + ' of pre-tax IRA money.</p>')
         + '<ul><li>A SEP or SIMPLE balance counts. A Solo 401(k) balance does '
         + '<b>not</b> — which is one practical reason to prefer the 401(k) here.</li>'
         + '<li>The balance that matters is measured on 31 December, not on the day you '
         + 'convert.</li></ul>';
     }}
  ];
}

function drawSorting(strat){
  var bar = $("sbar"), out = $("blocks");
  if (!bar || !out) return;
  if (!strat){
    bar.innerHTML = ""; out.innerHTML = '<p class="empty">Once there is profit above, every '
      + 'account you could use is priced here and sorted by what it is worth to you.</p>';
    return;
  }
  var cards = accountCards(strat);
  cards.forEach(function(c){ c.value = c.inPlay ? c.o.saved * c.share : 0; });
  cards.sort(function(x, y){
    if (x.inPlay !== y.inPlay) return x.inPlay ? -1 : 1;
    return y.value - x.value;
  });
  var best = cards.filter(function(c){ return c.inPlay; })[0];

  /* The bar is built ONCE and then only has classes and the readout updated.
     Re-writing its innerHTML on every render destroyed and recreated the very
     button being pressed, which is a lost tap on a phone and an unclickable
     element under automation. */
  if (!bar.dataset.built){
    bar.innerHTML = QS.map(function(q){
      return '<div class="tsr"><b>' + q.lab + '</b>' + q.opts.map(function(o){
        return '<button type="button" class="sb" data-k="' + q.k + '" data-v="' + o[0]
          + '" aria-pressed="false">' + o[1] + '</button>';
      }).join("") + '</div>';
    }).join("") + '<div class="sout">Best single route<b id="sbest">—</b>'
      + '<span id="sbestlab">—</span></div>';
    bar.dataset.built = "1";
  }
  bar.querySelectorAll("button[data-k]").forEach(function(b){
    var on = S[b.dataset.k] === b.dataset.v;
    b.classList.toggle("on", on);
    b.setAttribute("aria-pressed", on ? "true" : "false");
  });
  $("sbest").textContent = best ? money(best.value) : "—";
  $("sbestlab").textContent = best ? best.title : "nothing in play";

  out.innerHTML = cards.map(function(c, i){
    if (!c.inPlay){
      return '<div class="blk out"><div class="blkh"><span class="rank">—</span>'
        + '<div class="bt"><b>' + c.title + '</b><i>' + c.out + '</i></div>'
        + '<div class="bv">ruled out</div></div></div>';
    }
    return '<details class="blk in' + (i === 0 ? " top" : "") + '"' + (i === 0 ? " open" : "")
      + '><summary class="blkh"><span class="rank">' + (i + 1) + '</span>'
      + '<div class="bt"><b>' + c.title + '</b><i>' + c.sub + '</i></div>'
      + '<div class="bv">' + money(c.value) + '<small>less tax this year</small></div>'
      + '</summary><div class="blkb">' + c.detail(c.o)
      + (c.share < 1 && c.share > 0
         ? '<p class="half">You said only <b>some</b> of the profit is spare, so the figure in '
           + 'the header is half the full saving of ' + money(c.o.saved)
           + '. Open the room up and it is worth the larger number.</p>' : "")
      + '</div></details>';
  }).join("");
}

/* ------------------------------------------------- 06 working remotely -----
   Eight places, the reader's own profit, one bar each. The engine is app.js's,
   lifted whole (see _residency_core.js) and asserted equal to the cent, so this
   block and the simulator cannot quietly disagree about Berlin.

   Ranked by what is left, and California is marked rather than pinned to the
   top: the point of the section is that most of the list is WORSE, which only
   lands if the reader sees where their own line falls. */
var REMOTE_PAGE = "therapist-working-remotely-california.html";
var REMOTE = [
  {k:"uae",        name:"Dubai, UAE",         note:"9% corporate tax above AED 375,000; no personal income tax — and the US bill it does not shelter"},
  {k:"pittsburgh", name:"Pittsburgh, PA",     note:"PA flat 3.07%, city and school EIT 3%, $52 local services tax"},
  {k:"california", name:"California",         note:"where you are now"},
  {k:"brisbane",   name:"Brisbane, Australia",note:"resident rates plus the 2% Medicare levy"},
  {k:"nyc",        name:"New York City",      note:"state and city income tax, the unincorporated business tax, and the MCTMT"},
  {k:"berlin",     name:"Berlin, Germany",    note:"§32a EStG income tax, statutory health cover, solidarity surcharge"},
  {k:"portugal",   name:"Lisbon, Portugal",   note:"Categoria B simplified regime — taxed on 75% of GROSS, expenses not separately deducted"},
  {k:"france",     name:"Bordeaux, France",   note:"cotisations sociales plus the income tax scale"}
];

function drawRemote(c0){
  var el = $("remoteout"); if (!el) return;
  if (!c0 || !(c0.profit > 0)){
    el.innerHTML = '<p class="dek">Put a rate and a caseload in at the top and the '
      + 'eight places price themselves against your own practice.</p>';
    return;
  }
  /* Schedule C expenses, health cover excluded - it is a Schedule 1 adjustment,
     and every one of these functions expects the same base compute() uses. */
  var expC = Math.max(0, c0.expenses - c0.sehi);
  var gross = c0.gross;
  var r = RESID.computeResidency(gross, expC);
  var net = {
    california: c0.net,
    nyc:        RESID.computeNYC(gross, expC, 0, S.filing, c0.sehi).netUSD,
    pittsburgh: RESID.computePittsburgh(gross, expC, 0, S.filing, c0.sehi).netUSD,
    france:     RESID.computeFrance(gross, expC).netUSD,
    uae:        RESID.computeUAE(gross, expC, S.filing).netUSD,
    brisbane:   RESID.computeBrisbane(gross, expC).netUSD,
    berlin:     r.berlin.netUSD,
    portugal:   r.portugal.netUSD
  };
  var all = REMOTE.map(function(p){
    return {k:p.k, name:p.name, note:p.note, net:net[p.k],
            delta:net[p.k] - net.california};
  }).sort(function(a, b){ return b.net - a.net; });
  var top = Math.max.apply(null, all.map(function(x){ return x.net; }));
  var better = all.filter(function(x){ return x.delta > 0; }).length;
  /* A TEASER, not the table. The full eight live on
     therapist-working-remotely-california.html; running the same eight rows on
     two pages is near-duplicate content and splits whatever ranking either
     earns. Three rows plus California is enough to make the point and create
     the reason to click. */
  var idx = all.findIndex(function(x){ return x.k === "california"; });
  var keep = {};
  all.slice(0, 3).forEach(function(x){ keep[x.k] = 1; });
  keep.california = 1;
  if (all[all.length - 1]) keep[all[all.length - 1].k] = 1;   /* and the worst */
  var rows = all.filter(function(x){ return keep[x.k]; });
  var hidden = all.length - rows.length;

  el.innerHTML = rows.map(function(x){
    var home = x.k === "california";
    var w = top > 0 ? Math.max(4, x.net / top * 100) : 4;
    return '<div class="rrow' + (home ? " rhome" : "") + '">'
      + '<div class="rname"><b>' + esc(x.name) + (home ? ' <i>you are here</i>' : '')
      + '</b><em>' + esc(x.note) + '</em></div>'
      + '<div class="rbar"><span style="width:' + w.toFixed(1) + '%"></span></div>'
      + '<div class="rfig"><b>' + money(x.net) + '</b><em class="'
      + (home ? "rz" : x.delta > 0 ? "rup" : "rdn") + '">'
      + (home ? "your baseline"
             : (x.delta > 0 ? "+" : "−") + money(Math.abs(x.delta)) + " a year")
      + '</em></div></div>';
  }).join("")
  + '<p class="barn">Same practice, same clients, same ' + money(c0.profit)
  + ' of profit before tax. <b>' + (better === 0
      ? "Not one of the seven leaves you better off."
      : better === 1
        ? "One of the seven leaves you better off."
        : better + " of the seven leave you better off.")
  + '</b> ' + (hidden > 0
      ? hidden + ' more places, the licensing answer in full and the reason Dubai is '
        + 'a smaller win than it looks are on the <a href="'
        + REMOTE_PAGE + '">working-remotely page</a>.'
      : 'The full comparison is on the <a href="' + REMOTE_PAGE
        + '">working-remotely page</a>.')
  + '</p>';
}

/* --------------------------------------------------- 05 the structure block
   Last, on purpose. It is the smaller lever, it depends on the retirement
   decision above it, and it is the one that costs something other than money. */
function drawCorp(c0, corp, ss, strat){
  var el = $("corpout"); if (!el) return;
  if (!corp){ el.innerHTML = ""; return; }
  var verdictGood = corp.net > 0;
  var yrs = num(S.retYrs) || yearsToRetire(S) || 20;
  var r = num(S.retRet) || 7;
  /* The comparison the S-corp pitch never makes: if the saving is real, it is
     only worth having if it is invested. Priced at the same return and horizon
     the reader chose upstairs, so the page cannot flatter one side. */
  var invested = corp.net > 0 ? futureValue(corp.net, r, yrs) : 0;

  el.innerHTML =
      '<div class="verdict ' + (verdictGood ? "good" : "bad") + '">'
    + '<em>On your numbers, at a salary of ' + money(corp.salary) + ' ('
      + Math.round(corp.salaryPct * 100) + '% of profit)</em>'
    + '<b>' + (verdictGood ? money(corp.net) + " a year better" : money(-corp.net) + " a year worse")
    + '</b><p>' + (verdictGood
        ? 'Real, and smaller than the pitch. Before you act on it, read what it costs below '
          + 'the money — and note that the figure collapses if the salary has to rise.'
        : 'The payroll-tax saving does not cover what the structure costs at this profit and '
          + 'this salary. That changes as profit grows; it is a question worth asking again '
          + 'every year, not a door that is closed.') + '</p></div>'

    + '<div class="rws">'
    + row("Self-employment tax you stop paying",
          "Social Security and Medicare on the distribution, not on the salary",
          "+" + money(corp.saved))
    + row("California franchise tax", "the greater of $800 and 1.5% of net income",
          money(corp.franchise), "neg")
    + row("Payroll service, 1120-S and Statement of Information",
          "$" + corp.payroll + " + $" + corp.corpReturn + " + $" + corp.statement + " a year",
          money(corp.filings), "neg")
    + row("The QBI deduction you give up",
          "a wage is not qualified business income, so " + money(corp.lostQbi)
          + " of deduction goes, at your measured marginal rate of "
          + Math.round(corp.marginal * 100) + "%",
          money(corp.qbi), "neg")
    + row("California payroll tax on your own wage",
          "SDI at 1.3% of the whole salary (" + money(corp.caSdi)
          + ", no cap since 2024) plus UI, ETT and FUTA on the first $7,000 ("
          + money(corp.caEmployer) + "). A sole proprietor pays none of it. SDI "
          + "alone can be waived with form DE 459 if you are the sole shareholder, "
          + "which also gives up your State Disability and Paid Family Leave cover",
          money(corp.caPayroll), "neg")
    + row("Net", "what the structure is actually worth this year", money(corp.net), "tot")
    + '</div>'

    + '<div class="tiles">'
    + tile("Earnings credited to Social Security, as a sole proprietor",
           money(corp.creditedSole), "every year")
    + tile("Credited as an S-corp at this salary", money(corp.creditedCorp),
           Math.round(corp.creditedDrop * 100) + "% less on your record", "warn")
    + (ss ? tile("What that costs you at 67", money(ss.gapYear) + "/yr",
           "if this year were typical of a 35-year record", "warn") : "")
    + '</div>'

    + '<div class="two">'
    + '<div class="side"><em>Take the saving</em><b>' + money(corp.net > 0 ? corp.net : 0)
      + '</b><span>a year, and if you invest every dollar of it at ' + r + '% for ' + yrs
      + ' years it becomes <b>' + money(invested) + '</b>.</span></div>'
    + '<div class="side"><em>Keep the Social Security</em><b>'
      + money(ss ? ss.gapYear : 0) + '</b><span>a year in benefit you would otherwise give up '
      + '— for life, inflation-adjusted, and it does not run out.</span></div>'
    + '</div>'
    + '<p class="fine">The two columns are not directly comparable and it would be dishonest '
    + 'to pretend otherwise: one is a pot you own and can lose, the other is an income you '
    + 'cannot outlive but cannot leave to anyone. What the comparison does show is that the '
    + 'S-corp saving is not free money — it is a trade, and at a salary well below your '
    + 'profit it is a trade you are making for thirty years.</p>'

    + '<p class="fine"><b>The salary is the whole argument, and there is no safe number.</b> '
    + 'The 50% convention above is a practitioner rule of thumb, not a threshold in the Code. '
    + 'The test is what the work is actually worth — what you would have to pay a '
    + 'licensed therapist to do your clinical hours, plus something for running the business. '
    + 'Move the slider and watch how fast the verdict changes; that sensitivity is the risk, '
    + 'stated as a number.</p>';
}

/* --------------------------------------------------------------- the loop */
function render(){
  syncExpenses();
  var haveProfit = num(S.rate) > 0 && num(S.sessions) > 0;
  var c0 = haveProfit ? compute(S, 0) : null;          /* the do-nothing baseline */
  var cNow = haveProfit ? compute(S, Math.min(num(S.contrib), c0.room)) : null;
  var strat = c0 ? strategies(S, c0) : null;
  var corp = c0 ? corpLines(S, cNow, num(S.salPct) / 100) : null;
  var ss = ssCompare(c0, corp);

  var best = null;
  if (strat){
    var cards = accountCards(strat).filter(function(c){ return c.inPlay; });
    cards.forEach(function(c){
      var v = c.o.saved * (S.a_spare === "most" ? 1 : S.a_spare === "some" ? .5 : 0);
      if (!best || v > best.saved) best = {saved:v, room:c.o.room, id:c.id};
    });
  }

  drawRecap(c0);
  drawSell(c0, best);
  drawPlan(c0, cNow, strat);
  drawSorting(strat);
  drawCorp(c0, corp, ss, strat);
  drawRemote(c0);

  var sl = $("salout");
  if (sl && corp) sl.textContent = money(corp.salary) + "  ·  "
    + Math.round(corp.salaryPct * 100) + "% of profit";
  /* NOT em-dashes. Two 38px figures above the fold with captions and nothing
     under them is the worst thing this page can show a cold landing. The zero
     state carries the site's own worked example - a $250,000 practice with
     $41,650 of running costs, which the simulator computes as $217,350 of
     profit with $18,244 of the tax on it still optional - and the tag below
     says so. Both become the reader's the moment anything is typed. */
  var haveProfit = !!(c0 && c0.profit > 0);
  var hp = $("heroprofit");
  if (hp) hp.textContent = haveProfit ? money(c0.profit) : "$217,350";
  var ho = $("herooptional");
  if (ho) ho.textContent = best ? money(best.saved) : "$18,244";
  var teg = $("heroeg"); if (teg) teg.hidden = haveProfit;
  writeHash();
}

/* -------------------------------------------------------- URL round-trip */
var lock = false;
function writeHash(){
  if (lock) return;
  var q = [];
  HASH_KEYS.forEach(function(k){
    var v = S[k];
    if (v === "" || v === null || v === undefined) return;
    q.push(k + "=" + encodeURIComponent(v));
  });
  try { history.replaceState(null, "", "#" + q.join("&")); } catch (e) {}
}
function readHash(){
  var raw = location.hash.replace(/^#/, "");
  if (!raw || raw.indexOf("=") < 0) return;
  lock = true;
  raw.split("&").forEach(function(p){
    var i = p.indexOf("=");
    if (i < 0) return;
    var k = p.slice(0, i), v = decodeURIComponent(p.slice(i + 1));
    if (HASH_KEYS.indexOf(k) >= 0) S[k] = v;
    /* The simulator serialises its twelve expense categories individually. If
       they arrive, they win over the single monthly figure, and the single
       field is back-filled so the reader sees a number rather than a blank. */
    else if (k.indexOf("exp_") === 0){ S.exp[k.slice(4)] = v; S._detail = true; }
  });
  var t = 0, any = false;
  EXPENSES.forEach(function(e){
    if (S.exp[e[0]] !== "" && S.exp[e[0]] != null){ t += num(S.exp[e[0]]); any = true; }
  });
  if (any && !S.expMonth) S.expMonth = Math.round(t);
  lock = false;
}

function bind(id, key){
  var el = $(id); if (!el) return;
  if (S[key] !== "" && S[key] !== null && S[key] !== undefined) el.value = S[key];
  el.addEventListener(el.tagName === "SELECT" ? "change" : "input", function(){
    S[key] = el.value; render();
  });
}

function boot(){
  readHash();
  ["rate","sessions","weeksOff","expMonth","filing","age","contrib","retRet","retYrs","pretaxIra"]
    .forEach(function(k){ bind("i-" + k, k); });
  /* Typing in the monthly total is the reader choosing the simple model over
     the twelve categories they arrived with. */
  var em = $("i-expMonth");
  if (em) em.addEventListener("input", function(){ S._detail = false; });

  var sal = $("i-salPct");
  if (sal){
    sal.value = S.salPct;
    sal.addEventListener("input", function(){ S.salPct = sal.value; render(); });
  }
  var mx = $("b-max");
  if (mx) mx.addEventListener("click", function(){
    var c0 = compute(S, 0);
    S.contrib = Math.round(c0.room);
    var el = $("i-contrib"); if (el) el.value = S.contrib;
    render();
  });
  /* The sorting bar is delegated rather than bound per button, because the bar
     is re-rendered on every keystroke and per-button listeners would be
     re-attached to elements that no longer exist. */
  var bar = $("sbar");
  if (bar) bar.addEventListener("click", function(e){
    var b = e.target.closest ? e.target.closest("button[data-k]") : null;
    if (!b) return;
    S[b.dataset.k] = b.dataset.v;
    render();
  });
  window.addEventListener("hashchange", function(){
    if (location.hash.indexOf("=") < 0) return;
    readHash();
    HASH_KEYS.forEach(function(k){ var el = $("i-" + k); if (el) el.value = S[k]; });
    render();
  });
  render();
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
"""
