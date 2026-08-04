#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""therapist-cost-of-living-california.html

The personal side of the site. Everything else here prices a PRACTICE; this
prices the person running it — what a month actually costs where they live,
what the student loan takes, and what is left.

Takes a hand-off from the simulator and the Job Advisor: arrive with `net` in
the hash and the income box is filled.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
import content as C

CH = os.path.join(HERE, "..", "amft")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
chrome_ftr = open(os.path.join(CH, "_chrome_ftr.txt")).read()
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r"\1", chrome_hdr)

CSS = """
.cl{--paper:#FBF9F3;--white:#fff;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
  --field:#FBF6E9;--fieldline:#E4D9BE;--pine:#2C6350;--gold:#B08430;--pop:#F6C560;
  --pos:#3F9577;--neg:#B5483F;--indigo:#4B3B93;
  background:var(--white);color:var(--ink);font-family:Inter,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
.cl *,.cl *::before,.cl *::after{box-sizing:border-box}
.clwrap{max-width:1000px;margin:0 auto;padding:0 24px}
.clnarrow{max-width:730px}
@media (max-width:520px){.clwrap{padding:0 18px}}
.cl h1,.cl h2,.cl h3{font-family:Fraunces,Georgia,serif;font-weight:700;
  letter-spacing:-.015em;line-height:1.12;margin:0 0 .45em}
.cl p{margin:0 0 1em}
.cl a{color:var(--pine)}
.cleyebrow{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;margin:0 0 13px;color:var(--muted)}

/* OPTION 3 - compact band, tool first.
   The hero was a full-height purple slab: up to 84px of padding above a 50px h1,
   everything in the left column, the right half empty, and no call to action
   anywhere in it. A reader arriving cold from search had to scroll past a whole
   screen of assertion before touching a single lever.
   It is now a BAND. Orientation still does its whole job - who it is for, where,
   what this computes, one action - but in about a third of the height, and the
   proof figures sit beside the copy instead of under it. */
.clhero{background:linear-gradient(160deg,#4B3B93 0%,#3A2D74 68%,#2E2460 100%);
  color:#EFEAFA;padding:clamp(20px,2.4vw,30px) 0 clamp(20px,2.4vw,30px)}
.clband{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(300px,.9fr);
  gap:clamp(22px,3.4vw,52px);align-items:center}
/* minmax(300px,...) is a FLOOR: on a 390px phone with the wrap's own padding the
   second column could not shrink below 300 and the page scrolled sideways by
   55-70px. Stacked, it has the full width and needs no floor at all. */
@media (max-width:900px){.clband{grid-template-columns:minmax(0,1fr);gap:18px}}

.clhero .cleyebrow{color:#F6C560;margin-bottom:8px}
.clhero h1{font-size:clamp(24px,2.6vw,34px);color:#FFFDF6;max-width:22ch;
  margin-bottom:.28em}
.clhero h1 em{font-style:normal;color:var(--pop)}
.cldeck{font-size:clamp(14.6px,1.05vw,16px);line-height:1.55;color:#C4BBE4;max-width:56ch;
  margin-bottom:14px}
/* the action the hero never had */
.clgo{display:inline-flex;align-items:center;min-height:46px;padding:0 20px;
  border-radius:999px;background:var(--pop);color:#2A2010;font-weight:700;
  font-size:15px;text-decoration:none}
.clgo:hover{background:#FFD57A}
.clwho{display:block;font-size:12.6px;line-height:1.55;color:#A79ACB;margin:12px 0 0;
  max-width:46em}
.clwho b{color:#DCD4F2;font-weight:600}
/* the figures move OUT of the flow and into the second column */
.clbig{display:grid;gap:2px 0;margin:0;padding:16px 20px;border-top:0;
  background:rgba(0,0,0,.22);border:1px solid rgba(255,255,255,.14);border-radius:14px}
.clbig div{min-width:0}
.clbig{min-width:0}
.clbig > div{display:flex;align-items:baseline;justify-content:space-between;gap:14px;min-width:0;
  padding:9px 0;border-bottom:1px solid rgba(255,255,255,.12)}
.clbig > div:last-of-type{border-bottom:0}
.clbig > div > b{font-family:Fraunces,Georgia,serif;font-size:clamp(22px,2.1vw,28px);
  line-height:1;color:var(--pop);white-space:nowrap;order:2}
.clbig > div > em{font-style:normal;font-size:12.6px;color:#C4BBE4;line-height:1.4;
  max-width:22ch;order:1}

/* MOVED: this block used to sit ABOVE the base .clbig rules, so at equal
   specificity the base rules won on source order and the whole mobile
   treatment was dead code. Nothing inside it changed. */
@media (max-width:560px){
  .clhero h1{font-size:23px;line-height:1.12}
  .cldeck{font-size:14.4px;margin-bottom:12px}
  /* the rows are flex with a `white-space:nowrap` figure and a 22ch caption, so
     their intrinsic minimum exceeded a 390px screen and the page scrolled
     sideways. Stacked, nothing has a floor. */
  .clbig{padding:12px 14px;min-width:0}
  .clbig > div{display:block;min-width:0}
  .clbig > div > b{white-space:normal;display:block;margin-bottom:2px}
  .clbig > div > em{max-width:none;display:block}
  /* one figure above the fold on a short phone; the other two are a scroll away */
  .clbig > div:nth-of-type(n+3){display:none}
  .clwho{display:none}
}

.clsec{padding:clamp(34px,4.5vw,62px) 0}
.clsec.clpaper{background:var(--paper);border-top:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.clh{display:flex;align-items:baseline;gap:12px;margin:0 0 .5em}
.clh span{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;
  color:var(--gold)}
.clsec h2{font-size:clamp(23px,2.5vw,32px);margin:0}
.cllede{font-size:16px;line-height:1.65;color:var(--muted);max-width:64ch;margin:0 0 22px}

.clgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:11px;
  margin:0 0 16px}
.clf{display:block;background:var(--field);border:1.5px solid var(--fieldline);
  border-radius:12px;padding:9px 13px 11px;min-height:60px}
.clf:focus-within{border-color:var(--gold);box-shadow:0 0 0 3px rgba(176,132,48,.16)}
.clf em{display:block;font-style:normal;font-size:9px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:#7C766A;margin-bottom:3px}
.clf span{display:flex;align-items:baseline;gap:3px;font-family:Fraunces,Georgia,serif;
  font-weight:600;font-size:18px}
.clf input,.clf select{width:100%;min-width:0;background:none;border:0;padding:0;
  font:inherit;color:inherit;outline:none;-moz-appearance:textfield}
.clf input::-webkit-outer-spin-button,.clf input::-webkit-inner-spin-button{
  -webkit-appearance:none;margin:0}
.clf input::placeholder{font-style:italic;font-weight:400;color:#BDB6A6;opacity:1}
.clf select{font-size:14.5px;cursor:pointer;font-family:Inter,sans-serif}
.clf i{font-style:normal;font-size:11px;color:#9A9384;font-family:Inter,sans-serif;
  font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.clwide{grid-column:1/-1}

.clrows{border-top:1px solid var(--line);margin:16px 0 0}
.clrow{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
  padding:10px 0;border-bottom:1px solid var(--line)}
.clrow b{font-size:15px}
.clrow em{font-style:normal;font-size:12.6px;color:var(--muted);flex:1}
.clrow span{font-family:Fraunces,Georgia,serif;font-size:17px;white-space:nowrap}
.clrow.tot{border-bottom:0;padding-top:14px;border-top:2px solid var(--ink);margin-top:4px}
.clrow.tot span{font-size:22px}
.clrow .neg{color:var(--neg)}
.clrow .pos{color:var(--pos)}

.clcard{background:var(--white);border:1px solid var(--line);border-top:3px solid var(--pine);
  border-radius:14px;padding:clamp(19px,2.2vw,26px);margin:0 0 16px}
.clcard[data-a="gold"]{border-top-color:var(--gold)}
.clcard[data-a="indigo"]{border-top-color:var(--indigo)}
.clcard h3{font-size:clamp(18px,1.8vw,22px)}
.clcard p{font-size:15.4px;line-height:1.64;color:#3A362E}
.clcard p:last-child{margin-bottom:0}

.clverdict{border-radius:12px;padding:16px 18px;margin:16px 0 0;font-size:15.4px;
  line-height:1.6}
.clverdict.ok{background:#F1F7F4;border-left:4px solid var(--pos);color:#245046}
.clverdict.tight{background:#FFFCF4;border-left:4px solid var(--gold);color:#6B5321}
.clverdict.short{background:#FBF1F0;border-left:4px solid var(--neg);color:#7A3A34}
.clverdict b{font-weight:700}

.clbar{height:30px;border-radius:8px;overflow:hidden;display:flex;margin:14px 0 8px;
  background:#EDEAE0}
.clbar i{display:block;height:100%}
.clkey{display:flex;gap:14px;flex-wrap:wrap;font-size:12.4px;color:var(--muted)}
.clkey s{text-decoration:none;display:inline-flex;align-items:center;gap:5px}
.clkey u{text-decoration:none;width:10px;height:10px;border-radius:3px;display:inline-block}

.clsteps{list-style:none;margin:0;padding:0}
.clsteps li{display:grid;grid-template-columns:34px minmax(0,1fr);gap:14px;
  padding:13px 0;border-top:1px solid var(--line)}
.clsteps li:first-child{border-top:0}
.clsteps b{display:block;font-size:15.6px;margin-bottom:3px}
.clsteps span{display:block;font-size:14.4px;line-height:1.6;color:var(--muted)}
.clsteps i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:12px;
  font-weight:600;color:var(--gold);padding-top:3px}
.clnote{background:var(--paper);border-left:4px solid var(--fieldline);
  border-radius:0 12px 12px 0;padding:16px 18px;margin:20px 0 0;font-size:14.6px;
  line-height:1.65;color:#3A362E}
.clfine{font-size:13.3px;line-height:1.6;color:var(--muted)}
.clcites{border-top:1px solid var(--line);padding-top:20px;margin-top:26px}
.clcite{display:grid;grid-template-columns:32px minmax(0,1fr);gap:6px;padding:9px 0;
  border-bottom:1px solid var(--line);font-size:13.4px;line-height:1.55}
.clcite b{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--gold)}
/* a.clcta, not .clcta. The generic `.cl a{color:var(--pine)}` above is
   specificity 0,2,0 and was beating this rule's 0,1,0 - so the CTA rendered
   pine-on-pine and was completely invisible. Caught by _dev/audit.mjs. */
a.clcta{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;
  border-radius:999px;background:var(--pine);color:#fff;font-weight:700;font-size:15.5px;
  text-decoration:none}
a.clcta:hover{background:#1F4C3C;color:#fff}
.cleg{grid-column:1/-1;margin:12px 0 0;font-size:12.4px;line-height:1.55;
  color:#9DBFB1}
.cleg b{color:#DCEAE3;font-weight:600}
.cleg[hidden]{display:none !important}
.cl :focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:6px}
"""

_bare = set(re.findall(r"^\.([A-Za-z][\w-]*)\s*\{", CSS, re.M))
_chrome = set(re.findall(r"\.([A-Za-z][\w-]*)", chrome_css))
assert not (_bare & _chrome), "collides with the chrome: %s" % sorted(_bare & _chrome)

JS = r"""
var AREAS = __AREAS__;
var CATS  = __CATS__;
var RAP_BANDS = __RAPBANDS__;
var RAP_MIN = __RAPMIN__, RAP_DEP = __RAPDEP__, RAP_MONTHS = __RAPM__;
var PSLF_MONTHS = __PSLF__;
var FPL_1 = __FPL__, FPL_EXTRA = __FPLX__, IBR_RATE = __IBR__, IBR_MONTHS = __IBRM__;

var S = {area:"ca", net:"", agi:"", deps:0, loan:"", rate:"6.5", plan:"rap",
         save:"", target:"3"};
CATS.forEach(function(c){ S["c_" + c[0]] = ""; });
var KEYS = Object.keys(S);

function $(id){ return document.getElementById(id); }
function num(v){ var n = parseFloat(v); return isFinite(n) ? n : 0; }
function money(v){ if (!isFinite(v)) return "—";
  var n = Math.round(v);
  return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US"); }

function areaDef(){
  for (var i = 0; i < AREAS.length; i++) if (AREAS[i][0] === S.area) return AREAS[i];
  return AREAS[0];
}
/* The picker PRE-FILLS. A category the reader has typed into always wins - the
   area is a starting point, not an answer, and overwriting a real rent with a
   county average would be the single most annoying thing this page could do. */
function catMonthly(k){
  if (String(S["c_" + k]) !== "") return num(S["c_" + k]);
  return Math.round(areaDef()[2][k] / 12);
}
function costTotal(){
  var t = 0;
  CATS.forEach(function(c){ t += catMonthly(c[0]); });
  return t;
}

/* ---------------------------------------------------------------- loans --
   Three formulas, each the published one.

   RAP  banded percentage of AGI, minus $50 a month per dependent, floor $10.
   IBR  10% of income above 150% of the poverty guideline for the household.
   STD  ten-year amortisation at the stated rate.

   PSLF is not a fourth formula - it is a horizon. You pay whatever your IDR
   plan says and the balance goes at 120 payments, so the monthly figure is
   RAP's and only the TOTAL differs. That is the whole point of showing both. */
function rapPayment(agi, deps){
  if (!(agi > 0)) return RAP_MIN;
  var pct = 0.10;
  for (var i = 0; i < RAP_BANDS.length; i++){
    if (agi <= RAP_BANDS[i][0]){ pct = RAP_BANDS[i][1]; break; }
  }
  return Math.max(RAP_MIN, agi * pct / 12 - deps * RAP_DEP);
}
function ibrPayment(agi, deps){
  var fpl = FPL_1 + deps * FPL_EXTRA;
  return Math.max(0, (agi - fpl * 1.5) * IBR_RATE / 12);
}
function stdPayment(bal, ratePct, months){
  if (!(bal > 0)) return 0;
  var r = ratePct / 100 / 12;
  if (r <= 0) return bal / months;
  return bal * r / (1 - Math.pow(1 + r, -months));
}
/* What a fixed monthly payment actually retires, at a given rate. Returns
   Infinity where the payment does not cover the interest - which is a real
   outcome on an income-driven plan and is worth saying out loud. */
function monthsToClear(bal, ratePct, pay){
  if (!(bal > 0)) return 0;
  var r = ratePct / 100 / 12;
  if (r <= 0) return bal / pay;
  if (pay <= bal * r) return Infinity;
  return -Math.log(1 - bal * r / pay) / Math.log(1 + r);
}

function loanCalc(){
  var bal = num(S.loan), rate = num(S.rate), agi = num(S.agi), deps = num(S.deps);
  if (!(bal > 0)) return null;
  var rap = rapPayment(agi, deps);
  var ibr = ibrPayment(agi, deps);
  var std = stdPayment(bal, rate, 120);
  var pay = S.plan === "std" ? std : S.plan === "ibr" ? ibr : rap;
  var horizon = S.plan === "pslf" ? PSLF_MONTHS
              : S.plan === "std" ? 120
              : S.plan === "ibr" ? IBR_MONTHS : RAP_MONTHS;
  if (S.plan === "pslf") pay = rap;      /* you are on an IDR plan while you wait */
  var clear = monthsToClear(bal, rate, pay);
  var months = Math.min(horizon, clear);
  var forgiven = clear > horizon;
  return {bal:bal, rate:rate, pay:pay, rap:rap, ibr:ibr, std:std,
          horizon:horizon, months:months, forgiven:forgiven,
          paid:pay * months, clear:clear};
}

function render(){
  var cost = costTotal(), net = num(S.net);
  var L = loanCalc();
  var loanPay = L ? L.pay : 0;
  var left = net - cost - loanPay;

  /* --- costs table */
  var rows = CATS.map(function(c){
    var typed = String(S["c_" + c[0]]) !== "";
    return '<div class="clrow"><b>' + c[1] + '</b><em>' + (typed ? "yours"
      : "from " + areaDef()[1]) + '</em><span>' + money(catMonthly(c[0]))
      + '</span></div>';
  }).join("");
  $("costrows").innerHTML = rows
    + '<div class="clrow tot"><b>A month, before loans</b><em></em><span>'
    + money(cost) + '</span></div>';

  /* --- loans */
  var lo = $("loanout");
  if (!L){
    lo.innerHTML = '<p class="clfine">Put a balance in and the plans price themselves '
      + 'against it.</p>';
  } else {
    var yrs = isFinite(L.months) ? (L.months / 12) : Infinity;
    lo.innerHTML =
        '<div class="clrow"><b>Monthly payment</b><em>on the plan selected</em><span>'
      + money(L.pay) + '</span></div>'
      + '<div class="clrow"><b>' + (L.forgiven ? "Forgiven after" : "Paid off in")
      + '</b><em>' + (L.forgiven
          ? (S.plan === "pslf"
              ? "120 qualifying payments, while you work for a qualifying employer"
              : "the plan&rsquo;s own horizon — the payment never clears the balance")
          : "at this payment and rate") + '</em><span>'
      + (isFinite(yrs) ? (Math.round(yrs * 10) / 10) + " yrs" : "—") + '</span></div>'
      + '<div class="clrow"><b>Total you would pay</b><em>'
      + (L.forgiven ? "and the rest is written off" : "principal and interest")
      + '</em><span>' + money(L.paid) + '</span></div>'
      + '<div class="clrow tot"><b>Against the standard ten-year plan</b><em>'
      + money(L.std) + ' a month, ' + money(L.std * 120) + ' in total</em><span class="'
      + (L.paid < L.std * 120 ? "pos" : "neg") + '">'
      + (L.paid < L.std * 120 ? "−" : "+") + money(Math.abs(L.paid - L.std * 120))
      + '</span></div>';
  }

  /* --- the answer */
  var v = $("verdict"), bar = $("bar"), key = $("key");
  if (!(net > 0)){
    v.className = "clverdict tight";
    v.innerHTML = "Put your monthly take-home in above. If you do not know it, the "
      + "<a href=\"practice-simulator.html\">practice simulator</a> and the "
      + "<a href=\"associate-mft-job-advisor.html\">Job Advisor</a> both work it out "
      + "and hand it over.";
    bar.innerHTML = ""; key.innerHTML = "";
    /* Was three em-dashes. The hero now opens on the worked example and this
       branch simply leaves it alone, so the figures above the fold are never
       empty - they are either the reader's or the example's, and the caption
       under them says which. */
    var eg = $("bigeg"); if (eg) eg.hidden = false;
    return;
  }
  var be = cost + loanPay;
  var eg2 = $("bigeg"); if (eg2) eg2.hidden = true;   /* these are the reader's now */
  $("bigcost").textContent = money(cost);
  $("bigbe").textContent = money(be);
  $("bigleft").textContent = money(left);

  var g = Math.max(net, be);
  bar.innerHTML =
      '<i style="width:' + (cost / g * 100) + '%;background:#8E4B45"></i>'
    + '<i style="width:' + (loanPay / g * 100) + '%;background:#B08430"></i>'
    + '<i style="width:' + (Math.max(0, left) / g * 100) + '%;background:#3F9577"></i>';
  key.innerHTML = '<s><u style="background:#8E4B45"></u>Living ' + money(cost) + '</s>'
    + '<s><u style="background:#B08430"></u>Loan ' + money(loanPay) + '</s>'
    + '<s><u style="background:#3F9577"></u>' + (left < 0 ? "Short " : "Left ")
    + money(Math.abs(left)) + '</s>';

  var months = num(S.target) || 3;
  var fund = be * months;
  var have = num(S.save);
  var pct = fund > 0 ? Math.min(100, have / fund * 100) : 0;
  var toGo = Math.max(0, fund - have);
  var perMonth = left > 0 ? toGo / left : Infinity;

  if (left < 0){
    v.className = "clverdict short";
    v.innerHTML = "<b>You are " + money(-left) + " a month short.</b> Your break-even is "
      + money(be) + " and this income is " + money(net)
      + ". That gap is the number to solve &mdash; by rate, by caseload, by cost, or by "
      + "moving one of them. Nothing below matters until it closes.";
  } else if (left < be * 0.1){
    v.className = "clverdict tight";
    v.innerHTML = "<b>" + money(left) + " a month left, on a break-even of " + money(be)
      + ".</b> That is under a tenth of what it costs you to exist, which is thin enough "
      + "that one quiet month undoes it. An emergency fund of " + money(fund)
      + " would take " + (isFinite(perMonth) ? Math.ceil(perMonth) + " months" : "—")
      + " at this rate.";
  } else {
    v.className = "clverdict ok";
    v.innerHTML = "<b>" + money(left) + " a month left</b>, on a break-even of "
      + money(be) + ". A " + months + "-month emergency fund is " + money(fund)
      + "; you are " + Math.round(pct) + "% of the way there, and the rest is "
      + (isFinite(perMonth) ? Math.ceil(perMonth) + " months" : "—")
      + " of putting this aside.";
  }
  writeHash();
}

function writeHash(){
  var q = [];
  KEYS.forEach(function(k){
    if (S[k] !== "" && S[k] != null) q.push(k + "=" + encodeURIComponent(S[k]));
  });
  history.replaceState(null, "", location.pathname + (q.length ? "#" + q.join("&") : ""));
}
function readHash(){
  var raw = location.hash.replace(/^#/, "");
  if (!raw || raw.indexOf("=") < 0) return;
  raw.split("&").forEach(function(p){
    var i = p.indexOf("="); if (i < 0) return;
    var k = p.slice(0, i), v = decodeURIComponent(p.slice(i + 1));
    if (KEYS.indexOf(k) >= 0) S[k] = v;
  });
}
function bind(id, key){
  var el = $(id); if (!el) return;
  el.value = S[key];
  var go = function(){ S[key] = el.value; if (key === "area") paint(); render(); };
  el.addEventListener("input", go);
  el.addEventListener("change", go);
}
/* When the area changes, the placeholders move with it - so an untouched field
   visibly follows the picker instead of sitting there looking typed-in. */
function paint(){
  CATS.forEach(function(c){
    var el = $("i-c_" + c[0]);
    if (el) el.placeholder = String(Math.round(areaDef()[2][c[0]] / 12));
  });
}
readHash();
KEYS.forEach(function(k){ bind("i-" + k, k); });
paint();
render();
"""


def field(fid, label, unit="", attrs='type="number" min="0"', wide=False):
    lead = '<i>$</i>' if unit == "$" else ""
    tail = ('<i>%s</i>' % unit) if unit and unit != "$" else ""
    return ('<label class="clf%s"><em>%s</em><span>%s<input id="i-%s" %s>%s</span></label>'
            % (" clwide" if wide else "", label, lead, fid, attrs, tail))


CITES = [
 (1, "MIT Living Wage Calculator &mdash; California",
  "https://livingwage.mit.edu/states/06",
  "Housing, transport, food, medical, civic, internet and other, for one adult with no "
  "children. Figures current as of 15 February 2026."),
 (2, "MIT Living Wage Calculator &mdash; Los Angeles County",
  "https://livingwage.mit.edu/counties/06037",
  "The same seven categories for Los Angeles County."),
 (3, "Repayment Assistance Plan",
  "https://www.fidelity.com/learning-center/personal-finance/repayment-assistance-plan",
  "RAP went live on 1 July 2026: 1&ndash;10% of adjusted gross income in bands, less $50 "
  "a month per dependent, minimum $10, forgiveness at 360 payments. PSLF remains at 120."),
 (4, "HHS poverty guidelines 2026, via the US Courts 150% table",
  "https://www.uscourts.gov/file/document/150-percent-hhs-poverty-guidelines",
  "$23,940 is 150% of the guideline for one person in the 48 contiguous states, rising "
  "$8,520 per additional person &mdash; the threshold income-based repayment measures "
  "discretionary income against."),
 (5, "Dave Ramsey, the Baby Steps", "https://www.ramseysolutions.com/dave-ramsey-7-baby-steps",
  "The seven-step framework summarised on this page."),
]

LD = {"@context": "https://schema.org", "@type": "WebApplication", "name": C.TITLE,
      "url": C.SITE + "/" + C.SLUG, "applicationCategory": "FinanceApplication",
      "operatingSystem": "Any web browser", "description": C.DESC,
      "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s" />
<link rel="canonical" href="%(site)s/%(slug)s" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:type" content="website" />
<meta property="og:url" content="%(site)s/%(slug)s" />
%(head)s
<style>%(chrome_css)s</style>
<style>%(css)s</style>
<script type="application/ld+json">%(ld)s</script>
</head><body>
%(hdr)s
<main class="cl">
%(body)s
</main>
%(ftr)s
<script>%(navjs)s</script>
<script>
%(js)s
</script>
</body></html>
"""


def build_body():
    B = []
    A = B.append

    A('<section class="clhero"><div class="clwrap"><div class="clband"><div>')
    A('<p class="cleyebrow">California &middot; for LMFTs, LCSWs, LPCCs and associates</p>')
    A('<h1>What a month actually costs you &mdash; and <em>what is left</em>.</h1>')
    A('<p class="cldeck">Every other tool here prices the practice. This one prices the '
      'person running it: what it costs to live where you live, what the student loan '
      'takes, and what remains.</p>')
    # The action the hero never had. AIDA broke at desire -> action: there was no
    # call to action anywhere in this hero at all.
    A('<a class="clgo" href="#where">Start with my county &darr;</a>')
    A('<p class="clwho">Housing, transport, food and medical <b>by county</b>; '
      '<b>RAP, IBR and PSLF</b> for the loan. Nothing is saved.</p>')
    A('</div>')          # end the copy column; the figures are the second one
    # NOT three em-dashes. A cold reader landing from search saw three captions
    # for numbers that were not there, which is the worst thing this page can do
    # above the fold. It opens on the page's own worked example - Los Angeles
    # County, one adult, MIT Living Wage - and every figure recomputes the
    # moment a field is touched. See paintBig() for the swap.
    A('<div class="clbig">'
      # These are STATEWIDE, because statewide is what the area picker below
      # defaults to - a Los Angeles example over a statewide form is an
      # inconsistency a careful reader will catch. MIT Living Wage, California,
      # one adult / no children: 23383+9528+4580+3876+3432+1625+4992 = 51,416/yr
      # = 4,285/mo. RAP at an $85,000 AGI is the 8% band: 85000*.08/12 = 567.
      '<div><b id="bigcost">$4,285</b><em>to live, a month</em></div>'
      '<div><b id="bigbe">$4,851</b><em>break-even, with the loan</em></div>'
      '<div><b id="bigleft">$1,149</b><em>left over</em></div>'
      '<p class="cleg" id="bigeg">Worked example: California statewide, one adult, '
      'an $85,000 AGI on RAP and a $6,000 monthly take-home. '
      '<b>Change anything below and all three move.</b></p></div>')
    A('</div></div></section>')

    # 01 where you live
    A('<section class="clsec" id="where"><div class="clwrap">')
    A('<div class="clh"><span>01</span><h2>Where you live</h2></div>')
    A('<p class="cllede">Pick an area and the seven categories fill in from the MIT '
      'Living Wage Calculator.<sup>[1][2]</sup> <b>Then change them.</b> These are '
      'county averages for one adult; your rent is your rent, and a typed figure always '
      'beats an average.</p>')
    A('<div class="clgrid">')
    A('<label class="clf clwide"><em>Area</em><span><select id="i-area">'
      + "".join('<option value="%s">%s</option>' % (k, n) for k, n, _, _ in C.AREAS)
      + '</select></span></label>')
    for k, lab in C.CATS:
        A(field("c_" + k, lab, "$/mo"))
    A('</div>')
    A('<div class="clrows" id="costrows"></div>')
    A('<p class="clfine" style="margin-top:14px">Only two areas are shipped as presets, '
      'because those are the two whose figures were checked directly. Anywhere else in '
      'California: start from the statewide numbers and type over them.</p>')
    A('</div></section>')

    # 02 what comes in
    A('<section class="clsec clpaper"><div class="clwrap">')
    A('<div class="clh"><span>02</span><h2>What comes in</h2></div>')
    A('<p class="cllede">Take-home, after tax &mdash; not what you bill and not your '
      'salary. If you do not know it, the '
      '<a href="practice-simulator.html">practice simulator</a> works it out for a '
      'practice and the <a href="associate-mft-job-advisor.html">Job Advisor</a> works '
      'it out for a job.</p>')
    A('<div class="clgrid">')
    A(field("net", "Take-home a month", "$/mo"))
    A(field("agi", "Adjusted gross income a year", "$/yr"))
    A(field("deps", "Dependents you claim", "", 'type="number" min="0" max="12"'))
    A('</div>')
    A('<p class="clfine">Adjusted gross income is what the loan plans are measured '
      'against, and it is not the same as take-home &mdash; it is roughly your profit or '
      'salary before tax, after the adjustments on your return.</p>')
    A('</div></section>')

    # 03 loans
    A('<section class="clsec"><div class="clwrap">')
    A('<div class="clh"><span>03</span><h2>The student loan</h2></div>')
    A('<p class="cllede">The rules changed on 1 July 2026. The <b>Repayment Assistance '
      'Plan</b> replaced SAVE, PAYE and ICR for new loans: 1&ndash;10% of adjusted gross '
      'income in bands, less $50 a month per dependent, forgiveness at 360 '
      'payments.<sup>[3]</sup> <b>Public Service Loan Forgiveness survived</b> &mdash; '
      'still 120 payments, still ten years, and most community mental health and '
      'non-profit work qualifies.</p>')
    A('<div class="clgrid">')
    A(field("loan", "Balance", "$"))
    A(field("rate", "Interest rate", "%", 'type="number" min="0" max="15" step="0.1"'))
    A('<label class="clf clwide"><em>Plan</em><span><select id="i-plan">'
      '<option value="rap">Repayment Assistance Plan (RAP)</option>'
      '<option value="pslf">RAP, working toward PSLF</option>'
      '<option value="ibr">Income-based repayment (IBR)</option>'
      '<option value="std">Standard, ten years</option>'
      '</select></span></label>')
    A('</div>')
    A('<div class="clrows" id="loanout"></div>')
    A('<div class="clnote"><b>Why PSLF is a different question, not a better rate.</b> '
      'On the forgiveness track the balance is written off after 120 qualifying payments '
      'whatever it has reached. Paying extra does not shorten that clock and does not '
      'increase what is forgiven &mdash; it just moves money from you to the loan for no '
      'return. Switch the plan above between the two and the total tells you what that '
      'is worth in your case.</div>')
    A('</div></section>')

    # 04 the answer
    A('<section class="clsec clpaper"><div class="clwrap">')
    A('<div class="clh"><span>04</span><h2>Break-even, and what is left</h2></div>')
    A('<div class="clbar" id="bar"></div><div class="clkey" id="key"></div>')
    A('<div class="clverdict tight" id="verdict"></div>')
    A('<div class="clgrid" style="margin-top:20px">')
    A(field("save", "Saved so far", "$"))
    A(field("target", "Months of cover you want", "mo",
            'type="number" min="1" max="12" step="1"'))
    A('</div>')
    A('</div></section>')

    # 05 principles
    A('<section class="clsec"><div class="clwrap clnarrow">')
    A('<div class="clh"><span>05</span><h2>%s</h2></div>' % C.RAMSEY_H)
    A('<p class="cllede">%s<sup>[5]</sup></p>' % C.RAMSEY_LEDE)
    A('<ol class="clsteps">')
    for n, title, body in C.RAMSEY_STEPS:
        A('<li><i>%s</i><div><b>%s</b><span>%s</span></div></li>' % (n, title, body))
    A('</ol>')
    A('<div class="clnote">%s</div>' % C.RAMSEY_NOTE)
    A('</div></section>')

    # next
    A('<section class="clsec clpaper"><div class="clwrap clnarrow">')
    A('<h2>Before any of this is real</h2>')
    A('<p class="cllede">Everything here starts from one figure: what actually reaches '
      'your account. If that is a guess, so is the rest of the page.</p>')
    A('<a class="clcta" href="practice-simulator.html">Work out your take-home &rarr;</a>')
    A('</div></section>')

    # sources
    A('<section class="clsec"><div class="clwrap clnarrow"><div class="clcites">')
    A("<h3>Sources</h3>")
    for n, cite, url, note in CITES:
        A('<div class="clcite"><b>[%d]</b><div><a href="%s" target="_blank" '
          'rel="noopener noreferrer">%s</a> &mdash; %s</div></div>' % (n, url, cite, note))
    A('<p class="clfine" style="margin-top:16px"><b>Estimates, not advice.</b> Cost '
      'figures are county averages for one adult with no children and will not match your '
      'life. Loan figures apply the published formulas to what you typed and ignore '
      'capitalised interest, forbearance history, consolidation, joint filing and every '
      'other fact particular to your loans. Check anything that matters with your '
      'servicer and with a professional who knows your situation.</p>')
    A('</div></div></section>')
    return "\n".join(B)


def main():
    # The JS body carries CSS percentages ("%;background:"), so % formatting on
    # it is a trap. Token substitution, with an assertion that none is left.
    js = JS
    for tok, val in [
            ("__AREAS__", json.dumps([[k, n, d, r] for k, n, d, r in C.AREAS])),
            ("__CATS__", json.dumps([[k, re.sub("&amp;", "&", l)] for k, l in C.CATS])),
            ("__RAPBANDS__", json.dumps(C.RAP_BANDS)),
            ("__RAPMIN__", str(C.RAP_MIN)), ("__RAPDEP__", str(C.RAP_DEPENDENT)),
            ("__RAPM__", str(C.RAP_MONTHS)), ("__PSLF__", str(C.PSLF_MONTHS)),
            ("__FPL__", str(C.FPL_1)), ("__FPLX__", str(C.FPL_EXTRA)),
            ("__IBR__", str(C.IBR_RATE)), ("__IBRM__", str(C.IBR_MONTHS))]:
        assert tok in js, "unused token " + tok
        js = js.replace(tok, val)
    assert "__" not in js, "a token was left unsubstituted"
    html = SHELL % dict(title=C.TITLE, desc=C.DESC, site=C.SITE, slug=C.SLUG,
                        head=chrome_head, chrome_css=chrome_css, css=CSS,
                        ld=json.dumps(LD, separators=(",", ":")), hdr=chrome_hdr,
                        body=build_body(), ftr=chrome_ftr, navjs=chrome_js, js=js)
    assert html.count("<h1") == 1
    assert html.count("<footer") == 1
    assert 'href="terms.html"' in html and 'href="privacy.html"' in html
    assert "</script>" not in js
    for n, _, _, _ in CITES:
        assert "[%d]</b>" % n in html
    open(os.path.join(HERE, C.SLUG), "w", encoding="utf-8").write(html)
    print("wrote %s  %d kB" % (C.SLUG, len(html) // 1024))


if __name__ == "__main__":
    main()
