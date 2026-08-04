#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The page's whole engine. Plain ES5-ish JavaScript, no build step, no bundle.

Two calculations live here and they are deliberately kept apart:

  jobCalc()   turns an offer into money - gross, W-2 tax, benefits, and the two
              rates that actually decide between two jobs: what an hour of your
              life is worth after tax, and what a BBS hour costs you.

  hoursCalc() turns a weekly caseload into a licence date, against all four
              BBS gates at once rather than the 3,000 everybody quotes.

Both are pure. Rendering reads them and never recomputes.
"""

JS = r"""
(function(){
'use strict';

/* ---------------------------------------------------------------- constants
   2026 figures. Federal from Rev. Proc. 2025-32, the Social Security base from
   SSA, and California from the 2025 schedules, which is what the FTB's own 2026
   Form 540-ES tells filers to use because the 2026 tables are not published.
   Same numbers as the practice simulator on this site, on purpose: two tools
   that disagree about the tax on $60,000 are worse than one. */
var FED_STD = {single:16100, mfj:32200, hoh:24150};
var CA_STD  = {single:5706,  mfj:11412, hoh:11412};
var FED = {
  single:[[0,.10],[12400,.12],[50400,.22],[105700,.24],[201775,.32],[256225,.35],[640600,.37]],
  mfj:   [[0,.10],[24800,.12],[100800,.22],[211400,.24],[403550,.32],[512450,.35],[768700,.37]],
  hoh:   [[0,.10],[17700,.12],[67450,.22],[105700,.24],[201750,.32],[256200,.35],[640600,.37]]
};
var CAB = {
  single:[[0,.01],[11079,.02],[26264,.04],[41452,.06],[57542,.08],[72724,.093],
          [371479,.103],[445771,.113],[742953,.123]],
  mfj:   [[0,.01],[22158,.02],[52528,.04],[82904,.06],[115084,.08],[145448,.093],
          [742958,.103],[891542,.113],[1485906,.123]],
  hoh:   [[0,.01],[22173,.02],[52530,.04],[67716,.06],[83805,.08],[98990,.093],
          [505208,.103],[606251,.113],[1010417,.123]]
};
var SS_BASE = 184500, SS_RATE = .062, MED_RATE = .0145, SDI_RATE = .013;

/* BBS gates. Every one of these is in the Handbook; see the citations block. */
var NEED_TOTAL = 3000, NEED_DIRECT = 1750, NEED_REL = 500, NEED_WEEKS = 104;
var CAP_NONCLIN = 1250, CAP_WEEK = 40, CAP_SUP_WEEK = 6, SUP_TRIGGER = 10;

/* ---------------------------------------------------------------- helpers */
function num(v, d){ var n = parseFloat(v); return isFinite(n) ? n : (d || 0); }
function bracket(income, table){
  if (income <= 0) return 0;
  var t = 0;
  for (var i = 0; i < table.length; i++){
    var lo = table[i][0], rate = table[i][1];
    var hi = (i + 1 < table.length) ? table[i+1][0] : Infinity;
    if (income > lo) t += (Math.min(income, hi) - lo) * rate; else break;
  }
  return t;
}
function fmt(v){
  if (!isFinite(v)) return "—";
  var n = Math.round(v);
  return (n < 0 ? "-$" : "$") + Math.abs(n).toLocaleString("en-US");
}
function fmt2(v){
  if (!isFinite(v)) return "—";
  return (v < 0 ? "-$" : "$") + Math.abs(v).toFixed(2);
}
function n0(v){ return isFinite(v) ? Math.round(v).toLocaleString("en-US") : "—"; }
function n1(v){ return isFinite(v) ? (Math.round(v * 10) / 10).toLocaleString("en-US") : "—"; }
function esc(s){ return String(s == null ? "" : s)
  .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function $(id){ return document.getElementById(id); }

/* ------------------------------------------------------------------- state
   One flat object so the whole setup round-trips through the URL hash and a
   reader can send their comparison to a classmate without an account. */
/* Associate posts are advertised one of two ways and only two: an annual salary,
   or a rate per CLINICAL hour with a separate, usually lower, rate for admin,
   notes, training and supervision. Fee-per-session is the same shape as the
   second one and is not a third model.

   A THIRD model was added after the first version shipped: a share of the fee.
   Very common in California group practice - the practice bills $150 and the
   associate takes an agreed percentage of it, with nothing at all for admin.
   It is not the same shape as an hourly rate, because the split is quoted
   against a fee rather than against an hour, and because admin is unpaid by
   construction rather than by a second rate.

   The salary, the two hourly rates and the fee pair are SEPARATE state keys. They
   used to share one "the number in the offer" field, so switching from salary to
   hourly left 60000 sitting in a box now labelled a rate per hour - which is the
   bug this replaces. Nothing can carry over now, because there is nowhere for it
   to carry to. */
var S = {
  filing:"single", showB:0,
  a_name:"This placement", a_pay:"salary", a_amt:"", a_hr:"", a_adminhr:"",
  a_fee:"", a_split:"",
  a_client:"", a_show:85, a_admin:"",
  a_weeks:48, a_sup:"onclock", a_indiv:1, a_group:0, a_supcost:"", a_health:"", a_extra:"",
  b_name:"The other one", b_pay:"hourly", b_amt:"", b_hr:"", b_adminhr:"",
  b_fee:"", b_split:"",
  b_client:"", b_show:85, b_admin:"",
  b_weeks:48, b_sup:"youpay", b_indiv:1, b_group:0, b_supcost:"", b_health:"", b_extra:"",
  h_ind:"", h_rel:"", h_grp:"", h_non:"", h_sup:1, h_weeks:48,
  h_have:"", h_have_d:"", h_have_r:"", h_have_w:""
};

/* --------------------------------------------------------------- job maths
   Returns null when there is nothing to work with, so every caller has one
   empty state to handle rather than a screen of $0 that looks like an answer. */
var SUP_EXTRA_ABOVE = 10;   /* direct hours a week above which a second unit is due */
function jobCalc(p){
  var mode = S[p + "_pay"];
  var salaried = mode === "salary", split = mode === "split";
  var amt = num(S[p + "_amt"]);                 /* annual salary */
  var hr = num(S[p + "_hr"]);                   /* per clinical hour */
  var adminhr = num(S[p + "_adminhr"]);         /* per admin/supervision hour */
  var fee = num(S[p + "_fee"]);                 /* what the practice bills */
  var splitPct = num(S[p + "_split"]) / 100;    /* your share of it */
  var client = num(S[p + "_client"]);
  var headline = salaried ? amt : split ? fee * splitPct : hr;
  if (headline <= 0 && client <= 0) return null;

  var showRate = Math.min(100, Math.max(0, num(S[p + "_show"], 85))) / 100;
  var weeks = Math.min(52, Math.max(1, num(S[p + "_weeks"], 48)));
  var admin = num(S[p + "_admin"]);
  var indiv = num(S[p + "_indiv"]), group = num(S[p + "_group"]);
  var supHrs = indiv + group, supMode = S[p + "_sup"];

  /* The Board counts UNITS, not hours: one unit is one hour of individual or
     triadic supervision, OR two hours of group. At least one unit in any week
     experience is gained in a setting - and one ADDITIONAL unit in any week the
     associate provides more than ten hours of direct clinical counselling in
     that setting. (BBS, FAQs for supervisors.)

     The ten-hour test is on hours actually PROVIDED, so it runs on attended
     hours rather than booked ones - a week with twelve booked and nine kept is
     a one-unit week. */
  var supUnits = indiv + group / 2;

  /* Hours you sit with a client. A no-show costs you the hour whatever the pay
     model is; under fee-for-service it costs you the fee as well. */
  var kept = client * showRate;
  var supUnitsReq = kept > SUP_EXTRA_ABOVE ? 2 : kept > 0 ? 1 : 0;
  var onClock = (supMode === "onclock");
  var paidHrs = kept + (S[p + "_pay"] === "split" ? 0
                        : admin + (onClock ? supHrs : 0));
  /* Worked hours no longer carry a self-reported "unpaid" figure. Whether the
     admin hours are paid is decided by the pay model a few lines down, so
     asking the reader to split them was asking them to guess at something the
     model already knows - and the guess was then added on top, counting the
     same hour twice for anyone who read the two labels as overlapping. */
  var workedHrs = kept + admin + supHrs;

  /* A salary is paid whether or not the client showed. An hourly associate is
     paid for the clinical hours that actually happened, plus admin hours at the
     admin rate - which is the rate nobody puts in the advert. */
  /* On a fee split you are paid per session that happened and nothing for
     anything else - that is the model, not an oversight - so paidAdminHrs is
     zero and every admin hour is unpaid by construction. */
  var paidAdminHrs = split ? 0 : admin + (onClock ? supHrs : 0);
  var perClinical = split ? fee * splitPct : hr;
  var gross = salaried ? amt
            : (kept * perClinical + paidAdminHrs * adminhr) * weeks;

  /* W-2 withholding. Pre-tax deferrals are deliberately absent: an associate on
     $58,000 is not the reader this page is for, and a fake 401(k) line would
     flatter every offer equally without changing which one wins. */
  var ss = SS_RATE * Math.min(gross, SS_BASE);
  var med = MED_RATE * gross;
  var sdi = SDI_RATE * gross;
  var fed = bracket(Math.max(0, gross - FED_STD[S.filing]), FED[S.filing]);
  var ca  = bracket(Math.max(0, gross - CA_STD[S.filing]),  CAB[S.filing]);
  var tax = ss + med + sdi + fed + ca;
  var net = gross - tax;

  var health = num(S[p + "_health"]) * 12;
  var extra = num(S[p + "_extra"]);
  var supPaid = (supMode === "youpay") ? num(S[p + "_supcost"]) * 12 : 0;
  var value = net + health + extra - supPaid;

  /* BBS credit. Supervision is credited to a maximum of six hours in a week,
     and no week can be worth more than forty however long it was. */
  var nonclinWk = admin + Math.min(supHrs, CAP_SUP_WEEK);
  var creditWk = Math.min(kept + nonclinWk, CAP_WEEK);
  var bbsYear = creditWk * weeks;
  var directYear = kept * weeks;

  /* Two units of supervision are required in any week with more than ten
     face-to-face hours. Group counts half. */
  var units = indiv + group / 2;
  var unitsNeeded = kept > SUP_TRIGGER ? 2 : 1;

  return {
    label: S[p + "_name"] || (p === "a" ? "Job A" : "Job B"),
    salaried: salaried, split: split, hr: hr, adminhr: adminhr, fee: fee,
    splitPct: splitPct, perClinical: perClinical, paidAdminHrs: paidAdminHrs,
    gross: gross, ss: ss, med: med, sdi: sdi, fed: fed, ca: ca, tax: tax, net: net,
    health: health, extra: extra, supPaid: supPaid, value: value,
    weeks: weeks, kept: kept, client: client, admin: admin,
    supUnits: supUnits, supUnitsReq: supUnitsReq,
    supHrs: supHrs, onClock: onClock, paidHrs: paidHrs, workedHrs: workedHrs,
    grossHourly: paidHrs > 0 ? gross / (paidHrs * weeks) : NaN,
    realHourly: workedHrs > 0 ? value / (workedHrs * weeks) : NaN,
    bbsYear: bbsYear, directYear: directYear,
    perBbsHour: bbsYear > 0 ? value / bbsYear : NaN,
    yearsTo3000: bbsYear > 0 ? NEED_TOTAL / bbsYear : NaN,
    effRate: gross > 0 ? tax / gross : 0,
    units: units, unitsNeeded: unitsNeeded, supShort: units < unitsNeeded,
    overWeek: (kept + nonclinWk) > CAP_WEEK,
    lostWeek: Math.max(0, (kept + nonclinWk) - CAP_WEEK)
  };
}

/* ------------------------------------------------------------- hours maths
   The 3,000 is the headline and almost never the constraint. This works out
   every gate, then reports the last one to close, because that is the date. */
function hoursCalc(){
  /* Couples, families and children are ONE field. The BBS counts them together
     against the same 500, so splitting them into three boxes asked the reader
     for a distinction the requirement does not make. */
  var ind = num(S.h_ind), rel = num(S.h_rel), grp = num(S.h_grp);
  var directWk = ind + rel + grp;
  var relWk = rel;
  var non = num(S.h_non), sup = num(S.h_sup);
  if (directWk <= 0 && non <= 0) return null;

  var weeks = Math.min(52, Math.max(1, num(S.h_weeks, 48)));
  var nonclinWk = non + Math.min(sup, CAP_SUP_WEEK);
  var creditWk = Math.min(directWk + nonclinWk, CAP_WEEK);
  var nonclinCredited = Math.max(0, creditWk - directWk);

  var have = {total:num(S.h_have), direct:num(S.h_have_d), rel:num(S.h_have_r),
              weeks:num(S.h_have_w)};
  /* Non-clinical already banked, so the 1,250 ceiling is applied to the right
     running total rather than to this job in isolation. */
  var haveNon = Math.max(0, have.total - have.direct);
  var nonRoom = Math.max(0, CAP_NONCLIN - haveNon);

  function weeksFor(remaining, perWeek){
    if (remaining <= 0) return 0;
    if (perWeek <= 0) return Infinity;
    return remaining / perWeek;
  }
  /* Total is the awkward one: non-clinical stops counting at 1,250, so the
     weekly rate falls to direct-only once that ceiling is reached. */
  var wNonCap = nonclinCredited > 0 ? nonRoom / nonclinCredited : Infinity;
  var remTotal = Math.max(0, NEED_TOTAL - have.total);
  var wTotal;
  if (creditWk <= 0) {
    wTotal = Infinity;
  } else if (wNonCap === Infinity || creditWk * wNonCap >= remTotal) {
    wTotal = remTotal / creditWk;
  } else {
    var after = remTotal - creditWk * wNonCap;
    wTotal = wNonCap + weeksFor(after, directWk);
  }

  var gates = [
    {key:"total", label:"Total supervised hours", need:NEED_TOTAL, have:have.total,
     per:creditWk, weeksNeeded:wTotal, unit:"hours",
     note:"Clinical and non-clinical together, with non-clinical capped at 1,250."},
    {key:"direct", label:"Direct clinical counseling", need:NEED_DIRECT, have:have.direct,
     per:directWk, weeksNeeded:weeksFor(Math.max(0, NEED_DIRECT - have.direct), directWk),
     unit:"hours",
     note:"Face to face with clients. Notes, meetings and supervision are not this."},
    {key:"rel", label:"Couples, families and children", need:NEED_REL, have:have.rel,
     per:relWk, weeksNeeded:weeksFor(Math.max(0, NEED_REL - have.rel), relWk), unit:"hours",
     note:"A subset of the 1,750, not on top of it. Usually the last one to close."},
    {key:"weeks", label:"Weeks of supervised experience", need:NEED_WEEKS, have:have.weeks,
     per:1, weeksNeeded:Math.max(0, NEED_WEEKS - have.weeks), unit:"weeks",
     note:"A calendar floor of two years. No caseload gets you past it faster."}
  ];

  /* Weeks worked, converted to calendar weeks: 48 working weeks a year means a
     week of hours takes 52/48 of a calendar week to earn. The 104-week gate is
     calendar weeks of supervised experience, so it does not get the stretch. */
  var stretch = 52 / weeks;
  var maxCal = 0, binding = null;
  gates.forEach(function(g){
    g.calWeeks = (g.key === "weeks") ? g.weeksNeeded : g.weeksNeeded * stretch;
    g.pct = g.need > 0 ? Math.min(100, g.have / g.need * 100) : 0;
    if (isFinite(g.calWeeks) && g.calWeeks > maxCal){ maxCal = g.calWeeks; binding = g; }
    if (!isFinite(g.calWeeks)) binding = binding || g;
  });
  var stalled = gates.some(function(g){ return !isFinite(g.calWeeks); });
  if (stalled) binding = gates.filter(function(g){ return !isFinite(g.calWeeks); })[0];
  /* Every gate closed. maxCal is 0 and nothing was ever assigned to binding,
     which used to be read straight through and threw. Someone whose hours are
     already done is exactly the reader who should get a clean answer. */
  var finished = gates.every(function(g){ return g.have >= g.need; });
  gates.forEach(function(g){ g.blocking = (!finished && g === binding); });

  var done = new Date();
  done.setDate(done.getDate() + Math.ceil(maxCal * 7));

  return {
    gates: gates, binding: binding, stalled: stalled, finished: finished,
    calWeeks: maxCal, months: maxCal / (52 / 12), date: done,
    directWk: directWk, relWk: relWk, nonclinWk: nonclinWk,
    nonclinCredited: nonclinCredited, creditWk: creditWk, weeks: weeks,
    rawWk: directWk + nonclinWk, overWeek: (directWk + nonclinWk) > CAP_WEEK,
    supUnits: Math.min(sup, CAP_SUP_WEEK), supRaw: sup,
    unitsNeeded: directWk > SUP_TRIGGER ? 2 : 1,
    nonRoom: nonRoom, haveNon: haveNon,
    relShare: directWk > 0 ? relWk / directWk : 0,
    relShareNeeded: NEED_REL / NEED_DIRECT
  };
}

/* -------------------------------------------------------------- rendering */
function tile(lab, val, sub, hi){
  return '<div class="tile' + (hi ? ' hi' : '') + '"><em>' + lab + '</em><b>' + val
       + '</b>' + (sub ? '<u>' + sub + '</u>' : '') + '</div>';
}
function rec(lab, sub, val, cls){
  return '<div class="rec ' + (cls || '') + '"><div><b>' + lab + '</b>'
       + (sub ? '<i>' + sub + '</i>' : '') + '</div><div class="v '
       + (cls === 'neg' ? 'neg' : '') + '">' + val + '</div></div>';
}

function drawPanel(a, b, h){
  var el = $("apanel"); if (!el) return;
  var rows = "";
  if (a){
    rows += '<div class="arow"><span>'
          + (b ? "Take-home from " + esc(a.label) : "Your take-home")
          + '<br>after tax, plus benefits</span>'
          + '<b class="gold">' + fmt(a.value) + '</b></div>';
    rows += '<div class="arow"><span>What an hour of your life is worth<br>every hour you work, not just the billable ones</span>'
          + '<b>' + fmt2(a.realHourly) + '</b></div>';
  }
  if (h){
    rows += '<div class="arow"><span>Licensed by<br>at this caseload, all four BBS gates</span>'
          + '<b class="gold">' + (h.stalled ? "not on this mix"
              : h.date.toLocaleDateString("en-US",{month:"short",year:"numeric"})) + '</b></div>';
  }
  if (!rows){
    rows = '<div class="arow"><span>Put one offer in below and this fills in: what it pays '
         + 'after California tax, what an hour of your life is actually worth, and the date '
         + 'your 3,000 hours close.</span><b class="gold">&mdash;</b></div>';
  }
  el.innerHTML = rows
    + '<p class="anote">Nothing is saved and there is no account. Your setup lives in the '
    + 'address bar, so bookmarking the page keeps it.</p>';
}

function drawTake(a, b){
  var el = $("take"); if (!el) return;
  if (!a){
    el.innerHTML = '<p class="dek">Enter a salary or an hourly rate above and the whole '
      + 'withholding stack appears here — federal, California, Social Security, Medicare '
      + 'and SDI, each one separately, so you can see which line is taking what.</p>';
    return;
  }
  function block(c){
    var s = '<div class="job"><div class="jobhead"><span class="jobtag">'
      + (c === a ? 'A' : 'B') + '</span><b style="font-family:Fraunces,Georgia,serif;'
      + 'font-size:16px">' + esc(c.label) + '</b></div>';
    s += rec("Gross pay",
             c.salaried ? "the salary, before anything comes out"
             : c.split ? Math.round(c.splitPct * 100) + "% of a " + fmt(c.fee)
                 + " fee, " + n1(c.kept) + " sessions a week over " + c.weeks + " weeks"
             : fmt2(c.hr) + " a clinical hour and " + fmt2(c.adminhr)
               + " an admin hour, over " + c.weeks + " weeks",
             fmt(c.gross));
    s += rec("Federal income tax", "after the " + fmt(FED_STD[S.filing]) + " standard deduction",
             "−" + fmt(c.fed), "neg");
    s += rec("California income tax", "after the " + fmt(CA_STD[S.filing]) + " state standard deduction",
             "−" + fmt(c.ca), "neg");
    s += rec("Social Security", "6.2% of wages", "−" + fmt(c.ss), "neg");
    s += rec("Medicare", "1.45%, no ceiling", "−" + fmt(c.med), "neg");
    s += rec("California SDI", "1.3% of every dollar, no ceiling", "−" + fmt(c.sdi), "neg");
    s += rec("Take-home pay", Math.round(c.effRate * 1000) / 10 + "% of gross went to tax",
             fmt(c.net), "tot");
    if (c.health > 0) s += rec("Employer health contribution", "not pay, but it is money you "
             + "do not spend", "+" + fmt(c.health));
    if (c.extra > 0) s += rec("Match, stipends, reimbursements", "retirement match, licence "
             + "fees, CEUs, mileage", "+" + fmt(c.extra));
    if (c.supPaid > 0) s += rec("Supervision you pay for", "out of the take-home above",
             "−" + fmt(c.supPaid), "neg");
    s += rec("What the job is actually worth", "take-home plus benefits, less what you pay out",
             fmt(c.value), "tot");
    /* The number people actually plan around. An associate job pays on a real
       payroll cycle, so "what does this look like on a cheque" is a more useful
       question here than it is for a practice, where income arrives whenever
       clients pay. Both cadences are shown because employers use both. */
    if (c.net > 0){
      s += '<div class="biwk"><div class="bw"><em>Every two weeks</em><b>'
        + fmt(Math.round(c.net / 26)) + '</b><i>26 cheques</i></div>'
        + '<div class="bw"><em>Twice a month</em><b>' + fmt(Math.round(c.net / 24))
        + '</b><i>24 cheques</i></div>'
        + '<div class="bw"><em>A month</em><b>' + fmt(Math.round(c.net / 12))
        + '</b><i>if you smooth it yourself</i></div></div>'
        + '<p class="jobfoot">Take-home only &mdash; before supervision you pay for, and '
        + 'before anything you put away. Fortnightly and semi-monthly are not the same '
        + 'thing: 26 cheques against 24 means two months a year carry a third payday.</p>';
    }
    s += '</div>';
    return s;
  }
  el.innerHTML = '<div class="jobs">' + block(a) + (b ? block(b) : '') + '</div>';
}

function drawHour(a, b){
  var el = $("hour"); if (!el) return;
  if (!a){
    el.innerHTML = '<p class="dek">This is the section that changes minds. Fill in an offer '
      + 'above.</p>';
    return;
  }
  function set(c, letter){
    var unpaidShare = c.workedHrs > 0 ? (c.workedHrs - c.paidHrs) / c.workedHrs : 0;
    var s = '<div class="job"><div class="jobhead"><span class="jobtag">' + letter
      + '</span><b style="font-family:Fraunces,Georgia,serif;font-size:16px">'
      + esc(c.label) + '</b></div><div class="tiles">';
    /* For an hourly post the advertised number is the CLINICAL rate, and it is
       not what any hour pays once admin hours at a lower rate are mixed in.
       Showing both is the single most useful thing this section does. */
    if (c.split && c.perClinical > 0){
      s += tile("What a session pays you", fmt2(c.perClinical),
                Math.round(c.splitPct * 100) + "% of a " + fmt(c.fee) + " fee");
    } else if (!c.salaried && c.hr > 0){
      s += tile("The rate in the advert", fmt2(c.hr), "per clinical hour");
    }
    s += tile(c.salaried ? "Advertised, per paid hour" : "Blended, per paid hour",
              fmt2(c.grossHourly),
              c.salaried ? "gross ÷ the hours they pay you for"
              : c.split ? "you are only paid for sessions that happen"
              : "clinical and admin hours together");
    s += tile("What an hour is really worth", fmt2(c.realHourly),
              "after tax and benefits, ÷ every hour you actually work", true);
    s += tile("Per BBS hour earned", fmt2(c.perBbsHour),
              n0(c.bbsYear) + " countable hours a year");
    s += tile("Years to 3,000 here", isFinite(c.yearsTo3000)
              ? (Math.round(c.yearsTo3000 * 10) / 10) + " yrs" : "—",
              "on this caseload alone, ignoring the other three gates");
    s += '</div>';
    if (unpaidShare > 0.001){
      /* Under a fee split there IS no "rate for the rest" - grossHourly equals
         what a session pays, so valuing note-writing at it claimed $69,120 of
         unpaid admin on a $91,800 job. True arithmetic, nonsense as a number.
         The split case states the hours and lets the blended rate above carry
         the consequence; only salary and hourly get a dollar valuation, and
         theirs is at the BLENDED rate, which is what those hours would
         actually have been paid. */
      s += '<p class="jobfoot"><b>' + Math.round(unpaidShare * 100)
         + '% of the hours you work here are unpaid.</b> That is '
         + n0((c.workedHrs - c.paidHrs) * c.weeks) + ' hours a year'
         + (c.split ? ', which is the whole difference between what a session pays and '
             + 'what an hour of your life is worth.'
           : ', worth ' + fmt((c.workedHrs - c.paidHrs) * c.weeks * c.grossHourly)
             + ' at the rate they are paying you for the rest.') + '</p>';
    }
    if (c.client > 0 && c.kept < c.client){
      /* "At a 85%" and "At an 85%" are both wrong half the time, so the sentence
         is built to not need the article at all. */
      s += '<p class="jobfoot">With a show rate of ' + Math.round(c.kept / c.client * 100)
         + '% you sit with clients ' + n1(c.kept) + ' hours a week, not '
         + n1(c.client) + '. Over a year that is ' + n0((c.client - c.kept) * c.weeks)
         + ' BBS hours that never happen'
         + (c.salaried ? '.'
            : ' — and at ' + fmt2(c.perClinical) + ' a session, '
              + fmt((c.client - c.kept) * c.weeks * c.perClinical)
              + ' of pay you never see either.')
         + '</p>';
    }
    if (c.split && (c.admin + c.supHrs) > 0){
      s += '<p class="jobfoot"><b>A fee split pays you for sessions and nothing else.</b> '
         + 'Your ' + n1(c.admin + c.supHrs) + ' hours a week of notes, meetings '
         + 'and supervision are unpaid by construction — that is '
         + n0((c.admin + c.supHrs) * c.weeks) + ' hours a year, and it is why the '
         + 'blended figure sits so far below what a session pays.</p>';
    }
    if (!c.salaried && !c.split && c.hr > 0 && c.paidAdminHrs > 0 && c.adminhr < c.hr){
      s += '<p class="jobfoot">Your admin, notes and supervision hours pay '
         + fmt2(c.adminhr) + ', not ' + fmt2(c.hr) + '. That is '
         + n1(c.paidAdminHrs) + ' hours a week at '
         + Math.round(c.hr > 0 ? (1 - c.adminhr / c.hr) * 100 : 0)
         + '% less, which is why the blended figure sits below the advertised one.</p>';
    }
    if (c.overWeek){
      s += '<p class="jobfoot"><b>Over the weekly ceiling.</b> The BBS '
         + 'credits at most 40 hours in a week, so ' + n1(c.lostWeek)
         + ' hours a week here are worked and not counted.</p>';
    }
    if (c.supShort){
      s += '<p class="jobfoot"><b>Supervision looks short.</b> More than '
         + '10 face-to-face hours in a week requires two units, and this is '
         + n1(c.units) + '. One hour individual is a unit; two hours of group is a unit.</p>';
    }
    return s + '</div>';
  }
  el.innerHTML = '<div class="jobs">' + set(a, 'A') + (b ? set(b, 'B') : '') + '</div>';
}

function drawCompare(a, b){
  var el = $("cmp"); if (!el) return;
  if (!a || !b){
    el.innerHTML = '<p class="dek">Add a second offer above and the two land side by side '
      + 'here, with the differences priced. Comparing a salaried agency post against a '
      + 'fee-for-service group practice by their headline numbers is how people end up '
      + 'earning less for more work.</p>';
    return;
  }
  /* The fourth column is whether the row can be WON, not just compared.
     Gross pay, tax withheld and hours worked are context: a lower tax bill
     usually means a smaller salary, and badging it "better" would teach the
     opposite of what this page is for. Only the rows where more or less is
     unambiguously better for the reader carry a badge. */
  var ROWS = [
    ["Gross pay", "what the offer letter says — and the number that misleads",
     "gross", 0, fmt],
    ["Total tax withheld", "federal, CA, FICA and SDI. Lower here usually just means less pay",
     "tax", 0, fmt],
    ["What it is actually worth", "take-home plus benefits, less what you pay", "value", 1, fmt],
    ["Hours you work a week", "clinical, admin and supervision", "workedHrs", 0, n1],
    ["Real hourly", "value ÷ every hour worked", "realHourly", 1, fmt2],
    ["BBS hours a year", "after the 40-a-week and 6-supervision ceilings", "bbsYear", 1, n0],
    ["Per BBS hour", "what each hour towards your licence pays", "perBbsHour", 1, fmt2],
    ["Years to 3,000", "at this caseload alone", "yearsTo3000", -1, function(v){
      return isFinite(v) ? (Math.round(v * 10) / 10) + " yrs" : "—"; }]
  ];
  var s = '<div class="cmpwrap"><table class="cmp"><thead><tr><th>&nbsp;</th><th>'
        + esc(a.label) + '</th><th>' + esc(b.label) + '</th></tr></thead><tbody>';
  ROWS.forEach(function(r){
    var va = a[r[2]], vb = b[r[2]], dir = r[3], f = r[4];
    var cmpOk = dir !== 0 && isFinite(va) && isFinite(vb) && va !== vb;
    var aWins = cmpOk && (dir > 0 ? va > vb : va < vb);
    var bWins = cmpOk && (dir > 0 ? vb > va : vb < va);
    s += '<tr><td><span class="lab">' + r[0] + '</span><span class="sub">' + r[1]
       + '</span></td><td class="n' + (aWins ? ' win' : '') + '">' + f(va)
       + '</td><td class="n' + (bWins ? ' win' : '') + '">' + f(vb) + '</td></tr>';
  });
  s += '</tbody></table></div>';

  /* The verdict is written from the two rates that matter, not from gross pay,
     because gross pay is the number that misleads. */
  var dv = a.value - b.value, dh = a.realHourly - b.realHourly,
      db = a.perBbsHour - b.perBbsHour;
  var rich = dv >= 0 ? a : b, poor = dv >= 0 ? b : a;
  var hourWin = dh >= 0 ? a : b;
  var bbsWin = db >= 0 ? a : b;
  var agree = (rich === hourWin) && (rich === bbsWin);
  s += '<div class="verdict"><h3>' + (agree
      ? '<b>' + esc(rich.label) + '</b> wins on every measure that matters.'
      : '<b>' + esc(rich.label) + '</b> pays more. <b>' + esc(hourWin.label)
        + '</b> is worth more per hour of your life.') + '</h3>';
  s += '<p>' + esc(rich.label) + ' is worth ' + fmt(Math.abs(dv)) + ' more a year than '
     + esc(poor.label) + '. But ' + esc(rich.label) + ' asks for '
     + n1(rich.workedHrs * rich.weeks) + ' hours and ' + esc(poor.label) + ' asks for '
     + n1(poor.workedHrs * poor.weeks) + ', so per hour worked the gap is '
     + fmt2(Math.abs(dh)) + (agree ? ' the same way.' : ' the other way.') + '</p>';
  var dbbs = Math.abs(a.bbsYear - b.bbsYear);
  if (dbbs < 1){
    s += '<p>On licence progress they are level: both bank about ' + n0(a.bbsYear)
       + ' countable hours a year, so neither gets you to 3,000 sooner. Decide this one on '
       + 'the money and on who is signing your hours.</p>';
  } else {
    s += '<p>On licence progress, ' + esc(bbsWin.label) + ' banks ' + n0(dbbs)
       + ' more countable hours a year. Over the two years you are going to be doing this, '
       + 'that is ' + n0(dbbs * 2) + ' hours — '
       + (dbbs * 2 >= 300 ? 'months' : 'weeks') + ' off your licence date.</p>';
  }
  if (a.supPaid > 0 || b.supPaid > 0){
    var payer = a.supPaid > b.supPaid ? a : b;
    var share = Math.abs(dv) > 0 ? payer.supPaid / Math.abs(dv) : Infinity;
    s += '<p>' + esc(payer.label) + ' bills supervision back to you at '
       + fmt(payer.supPaid) + ' a year, which is entirely legal and entirely normal in group '
       + 'practice. It is also '
       + (share >= 1 ? 'more than the whole ' + fmt(Math.abs(dv)) + ' gap between these two '
            + 'offers, on its own'
          : Math.round(share * 100) + '% of the ' + fmt(Math.abs(dv))
            + ' gap between these two offers')
       + ' — so it belongs in the comparison rather than in the small print.</p>';
  }
  s += '</div>';
  el.innerHTML = s;
}

function drawHours(h){
  var el = $("plan"); if (!el) return;

  /* Which of the weekly boxes are still empty. A reader who filled in the
     banked hours and not the caseload saw four boxes showing 12 / 12 / 0 / 10
     and a section that would not compute - because those were placeholders. So
     the prompt now names the boxes it is waiting on and marks them, rather than
     saying "put your caseload in above" next to what looks like a caseload. */
  var WEEKLY = [["h_ind", "individual adults"], ["h_rel", "couples, families and children"],
                ["h_non", "notes, meetings and trainings"], ["h_weeks", "weeks a year"]];
  var missing = WEEKLY.filter(function(f){ return String(S[f[0]] || "") === ""; });
  /* Only the boxes the section is actually waiting on get marked. Groups and
     supervision are legitimately zero for plenty of associates, so an empty one
     does not block anything - marking it said "we need this" about a field the
     prompt then did not name, which is worse than not marking it at all. */
  WEEKLY.forEach(function(f){
    var inp = $("i-" + f[0]); if (!inp) return;
    var wrap = inp.closest(".f"); if (!wrap) return;
    wrap.classList.toggle("wait", !h && String(S[f[0]] || "") === "");
  });
  var wn = $("planwait");
  if (wn) wn.innerHTML = (!h && missing.length)
    ? "Waiting on " + (missing.length === 1 ? "one box" : missing.length + " boxes")
      + " above &mdash; <b>" + missing.map(function(f){ return f[1]; }).join("</b>, <b>")
      + "</b>. The faint italic numbers in the empty boxes are examples, not your figures."
    : "";

  if (!h){
    el.innerHTML = '<p class="dek">Splitting your week by client type is not fussiness '
      + '&mdash; 500 of the 1,750 direct hours have to be couples, families or children, '
      + 'and a caseload of adult individuals will finish the 3,000 and still not qualify '
      + 'you.</p>';
    return;
  }
  var s = '<div class="gates">';
  h.gates.forEach(function(g){
    s += '<div class="gate' + (g.blocking ? ' block' : '') + '"><div class="gatehead"><b>'
       + g.label + '</b><span class="num">' + n0(g.have) + ' / ' + n0(g.need) + ' '
       + g.unit + '</span></div>'
       + '<div class="gtrack"><i style="width:' + g.pct.toFixed(1) + '%"></i></div>';
    if (g.have >= g.need){
      s += '<p class="eta"><b>Done.</b> This gate is closed.</p>';
    } else if (!isFinite(g.calWeeks)){
      s += '<p class="eta"><b>Never, on this mix.</b> You are logging no hours of this kind, '
         + 'so this gate does not move.</p>';
    } else {
      s += '<p class="eta">' + n0(g.need - g.have) + ' to go at ' + n1(g.per) + ' a week &mdash; '
         + '<b>' + Math.ceil(g.calWeeks) + ' more calendar weeks</b>'
         + (g.blocking ? ', and this is the one holding the date.' : '.') + '</p>';
    }
    s += '<p>' + g.note + '</p></div>';
  });
  s += '</div>';

  s += '<div class="finish"><em>' + (h.finished ? 'On these numbers'
       : h.stalled ? 'On this caseload' : 'All four gates close on') + '</em><b>'
     + (h.finished ? 'All four gates are closed'
        : h.stalled ? 'One gate never closes'
        : h.date.toLocaleDateString("en-US",{month:"long", day:"numeric", year:"numeric"}))
     + '</b><p>';
  if (h.finished){
    s += 'Every requirement above is met, so the next step is the paperwork rather than more '
       + 'hours: the <b>Application for Licensure</b>, your experience verification signed by '
       + 'every supervisor you have had, and the clinical exam once the application is '
       + 'approved. You have one year from that approval to sit it. Check the totals against '
       + 'your own weekly log before you file — the Board audits, and a supervisor who has '
       + 'moved on is much harder to get a signature from.';
  } else if (h.stalled){
    s += 'You are logging nothing towards <b>' + h.binding.label.toLowerCase()
       + '</b>, so however many total hours you bank you will not be eligible. Change the '
       + 'caseload mix or change the job — this is a conversation to have with a '
       + 'supervisor now, not at hour 2,800.';
  } else {
    s += 'That is <b>' + Math.round(h.months) + ' months</b> from today, working '
       + h.weeks + ' weeks a year. The gate deciding it is <b>'
       + h.binding.label.toLowerCase() + '</b> — fix that one and the date moves; '
       + 'anything else you improve just banks hours you already have enough of.';
  }
  s += '</p></div>';

  /* The checks a weekly log would catch and a spreadsheet of totals will not. */
  s += '<div class="warns">';
  function warn(ok, ic, html){
    s += '<div class="warn' + (ok ? ' ok' : '') + '"><i class="ic">' + ic + '</i><div>'
       + html + '</div></div>';
  }
  if (h.overWeek){
    warn(false, "!", "<b>" + n1(h.rawWk) + " hours a week, and the BBS credits 40.</b> "
      + n1(h.rawWk - CAP_WEEK) + " hours a week are worked and thrown away, and they cannot "
      + "be carried into a quieter week. Log them anyway; just do not count on them.");
  }
  if (h.supRaw > CAP_SUP_WEEK){
    warn(false, "!", "<b>Supervision is credited to six hours a week.</b> You have put "
      + n1(h.supRaw) + " in, so " + n1(h.supRaw - CAP_SUP_WEEK) + " of it counts for nothing.");
  }
  if (h.directWk > SUP_TRIGGER){
    warn(true, "✓", "<b>More than ten face-to-face hours a week, so you need two units "
      + "of supervision.</b> One hour of individual or triadic supervision is a unit; two "
      + "hours of group is a unit. Associates cannot average this across weeks the way "
      + "trainees can — each week stands alone.");
  }
  if (h.relShare < h.relShareNeeded && h.directWk > 0){
    warn(false, "!", "<b>Your relational share is " + Math.round(h.relShare * 100)
      + "% and it needs to average " + Math.round(h.relShareNeeded * 100) + "%.</b> "
      + "500 of the 1,750 direct hours must be couples, families or children. On this mix "
      + "you finish the total first and then wait, seeing only the clients you need.");
  } else if (h.directWk > 0){
    warn(true, "✓", "<b>Relational hours are on track at " + Math.round(h.relShare * 100)
      + "% of your direct caseload.</b> The floor is 500 of 1,750, which is 29%.");
  }
  if (h.nonRoom <= 0){
    warn(false, "!", "<b>You are at the 1,250 non-clinical ceiling.</b> Notes, meetings, "
      + "supervision and testing stop counting from here. Only face-to-face hours move the "
      + "total now.");
  }
  warn(true, "i", "<b>Everything must fall inside six years.</b> Hours older than six years "
    + "at the date the Board receives your licensure application are gone, and a registration "
    + "renews five times before it expires for good.");
  s += '</div>';
  el.innerHTML = s;
}

/* --------------------------------------------------------------- the loop */
function render(){
  var a = jobCalc("a"), b = S.showB ? jobCalc("b") : null, h = hoursCalc();
  drawPanel(a, b, h);
  drawTake(a, b);
  drawHour(a, b);
  drawCompare(a, b);
  drawHours(h);
  var col = $("jobB"); if (col) col.hidden = !S.showB;
  /* Every .jobs grid is two equal columns. With the second job hidden that left
     a form pinned to the left half of a 1060px card and an empty right half.
     The page is single-job-first now, so the grid collapses. */
  document.querySelectorAll(".jobs").forEach(function(g){
    g.classList.toggle("solo", !S.showB);
  });
  var add = $("addB"); if (add) add.textContent = S.showB
    ? "✕  Remove the second offer" : "+  Compare a second offer";
  var CALC = {a: a, b: b};
  ["a","b"].forEach(function(p){
    var w = $(p + "_supcostwrap"); if (w) w.hidden = (S[p + "_sup"] !== "youpay");

    /* What the Board requires, against what this offer provides. A check, not
       an autofill - the reader is describing a real offer, and quietly
       correcting their entry would erase the shortfall worth seeing. */
    var sq = $(p + "_supreq"), c = CALC[p];
    if (sq){
      if (!c || c.supUnitsReq === 0){
        sq.textContent = "";
        sq.className = "supreq";
      } else {
        var have = c.supUnits, need = c.supUnitsReq;
        var unit = function(n){
          return (Math.round(n * 10) / 10) + (n === 1 ? " unit" : " units"); };
        var why = need === 2
          ? "you sit with clients " + (Math.round(c.kept * 10) / 10)
            + " hours in an average week, which is over the ten-hour line"
          : "at " + (Math.round(c.kept * 10) / 10) + " client hours a week";
        sq.className = "supreq " + (have + 1e-9 >= need ? "ok" : "short");
        sq.innerHTML = have + 1e-9 >= need
          ? "<b>Meets the Board&rsquo;s minimum.</b> " + unit(need)
            + " a week is required &mdash; " + why + " &mdash; and this offer gives "
            + unit(have) + "."
          : "<b>Below the Board&rsquo;s minimum.</b> " + unit(need)
            + " a week is required &mdash; " + why + " &mdash; but this offer gives "
            + unit(have) + ". One unit is one hour of individual or triadic "
            + "supervision, or two hours of group.";
      }
    }
    /* The salary box and the two rate boxes are never on screen together. The
       one that is hidden keeps its own value, so switching back and forth does
       not lose what was typed. */
    var m = S[p + "_pay"];
    var sw = $(p + "_amtwrap"); if (sw) sw.hidden = (m !== "salary");
    var hw = $(p + "_hrwrap"); if (hw) hw.hidden = (m !== "hourly");
    var aw = $(p + "_adminhrwrap"); if (aw) aw.hidden = (m !== "hourly");
    var fw = $(p + "_feewrap"); if (fw) fw.hidden = (m !== "split");
    var pw = $(p + "_splitwrap"); if (pw) pw.hidden = (m !== "split");
    var nt = $(p + "_paynote");
    if (nt) nt.textContent = m === "salary"
      ? "A salary is paid whether or not the client showed up, which is the single "
        + "biggest thing it buys you."
      : m === "split"
      ? "A fee split pays you a share of what the practice bills, per session that "
        + "actually happens. Nothing is paid for notes, meetings, training or "
        + "supervision — that is the model, and it is what the real hourly figure below "
        + "is going to show you."
      : "Most hourly associate posts pay one rate for clinical hours and a second, lower "
        + "one for everything else. If yours pays nothing for those, put 0 in and watch "
        + "what happens to the real rate.";
  });
  writeHash();
}

/* ------------------------------------------------------------- URL round-trip
   The whole setup, in the address bar. No storage API is used anywhere on this
   page, so there is nothing to clear and nothing to consent to. */
var lock = false;
function writeHash(){
  if (lock) return;
  var q = [];
  for (var k in S){
    if (!S.hasOwnProperty(k)) continue;
    var v = S[k];
    if (v === "" || v === null || v === undefined) continue;
    q.push(k + "=" + encodeURIComponent(v));
  }
  try { history.replaceState(null, "", "#" + q.join("&")); } catch (e) {}
}
function readHash(){
  var raw = location.hash.replace(/^#/, "");
  if (!raw) return;
  lock = true;
  raw.split("&").forEach(function(pair){
    var i = pair.indexOf("=");
    if (i < 0) return;
    var k = pair.slice(0, i), v = decodeURIComponent(pair.slice(i + 1));
    if (S.hasOwnProperty(k)) S[k] = v;
  });
  S.showB = (S.showB === "1" || S.showB === 1 || S.showB === true) ? 1 : 0;
  lock = false;
}

function bind(id, key){
  var el = $(id); if (!el) return;
  if (S[key] !== "" && S[key] !== null && S[key] !== undefined) el.value = S[key];
  var ev = (el.tagName === "SELECT") ? "change" : "input";
  el.addEventListener(ev, function(){ S[key] = el.value; render(); });
}

function boot(){
  readHash();
  Object.keys(S).forEach(function(k){
    if (k === "showB") return;
    bind("i-" + k, k);
  });
  var add = $("addB");
  if (add) add.addEventListener("click", function(){
    S.showB = S.showB ? 0 : 1;
    render();
    if (S.showB){
      var el = $("jobB"); if (el) el.scrollIntoView({behavior:"smooth", block:"center"});
    }
  });
  /* Copying the caseload over is the difference between this section being used
     and being skipped: nobody types their week twice. */
  var pf = $("prefill");
  if (pf) pf.addEventListener("click", function(){
    var client = num(S.a_client);
    if (client > 0){
      /* Split unknown, so it goes to individual adults and the reader corrects
         it. Guessing a relational share would be inventing the one number the
         whole section exists to check. */
      S.h_ind = Math.round(client * 10) / 10;
      S.h_rel = ""; S.h_grp = "";
    }
    S.h_non = S.a_admin; S.h_sup = num(S.a_indiv) + num(S.a_group);
    S.h_weeks = S.a_weeks;
    ["h_ind","h_rel","h_grp","h_non","h_sup","h_weeks"].forEach(function(k){
      var el = $("i-" + k); if (el) el.value = S[k];
    });
    render();
    var el = $("i-h_rel"); if (el) el.focus();
  });
  /* A shared link pasted into the address bar while this page is already open
     changes the fragment without reloading, so without this the reader sees
     their classmate's URL and their own numbers. In-anchor jumps (#hours,
     #rules) carry no "=" and are left to the browser. */
  window.addEventListener("hashchange", function(){
    if (location.hash.indexOf("=") < 0) return;
    readHash();
    Object.keys(S).forEach(function(k){
      var el = $("i-" + k);
      if (el && S[k] !== null && S[k] !== undefined) el.value = S[k];
    });
    render();
  });

  render();
}

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
})();
"""
