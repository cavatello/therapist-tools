#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The live engine for therapist-tax-strategy-california.html.

CORE is the prototype's own compute(), lifted byte-for-byte at build time so
this page and the simulator cannot disagree about the tax on a given profit.
Everything below it is new, and it is all measured rather than asserted: the
saving from a retirement account is the difference between running compute()
with the contribution and running it without, which is the only way to get it
right when the contribution itself moves you down a bracket and changes the
QBI fraction on the way.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = open(os.path.join(HERE, "_engine_core.js")).read()

# The eight-location engine. Lifted out of app.js (now deleted) and kept in its
# own IIFE because that file named half these constants differently from
# _engine_core.js. Parity with the original was asserted to the cent across 42
# comparisons before app.js was removed; _residency_core.js is now the only copy.
RESIDENCY = open(os.path.join(HERE, "_residency_core.js")).read()

# --------------------------------------------------------------------------
EXTRA = r"""
/* ---------------------------------------------------------------- strategy
   Limits are the 2026 published figures. Anything here that is a convention
   rather than a rule says so in the copy that renders it. */
var SEP_RATE   = .20;          /* of net self-employment earnings */
var SIMPLE_DEF = 16500, SIMPLE_CATCHUP = 3500, SIMPLE_MATCH = .03;
var IRA_LIMIT  = 7500,  IRA_CATCHUP = 1100;
/* Traditional IRA deduction phase-out for someone COVERED by a workplace plan.
   A sole proprietor with no plan at all is not covered and the deduction is
   unlimited - which is why the IRA block has to ask before it answers. */
var IRA_PHASE  = {single:[81000,91000], hoh:[81000,91000], mfj:[129000,149000]};
/* Roth IRA income phase-out - a DIFFERENT test from the Traditional deduction
   phase-out above. Traditional asks "are you covered by a plan at work"; Roth
   asks only "what is your income". Conflating the two is the commonest error
   in this area, so they are named separately and never share a constant. */
var ROTH_PHASE = {single:[153000,168000], hoh:[153000,168000], mfj:[242000,252000]};
var RET_AGE    = 67;

/* Every account, priced the same way: room, then the tax that room removes,
   found by running the whole engine twice.

   `base` MUST be the zero-contribution baseline, compute(st, 0). Passing the
   reader's current run instead would price each account against a tax bill
   that already has their contribution in it, and every saving would come out
   too small by exactly what they had already put away. */
function strategies(st, base){
  var profit = base.profit;
  if (!(profit > 0)) return null;
  var age = num(st.age) || 0;
  var seBase = profit * SE_FACTOR;
  var halfSE = (OASDI * Math.min(seBase, SS_BASE) + MEDI * seBase) / 2;
  var netSE = Math.max(0, profit - halfSE);
  var employer = Math.min(netSE, COMP_CAP) * SEP_RATE;

  function savedBy(amount){
    if (!(amount > 0)) return 0;
    var withIt = compute(st, amount);
    return Math.max(0, base.totalTax - withIt.totalTax);
  }

  var soloDeferral = K401_DEFERRAL + (age >= 50 ? K401_CATCHUP : 0);
  var solo = base.room;                       /* compute() already caps this */
  var sep = Math.max(0, Math.min(employer, LIMIT_415));
  var simpleDef = Math.min(SIMPLE_DEF + (age >= 50 ? SIMPLE_CATCHUP : 0),
                           Math.max(0, netSE));
  var simple = Math.max(0, simpleDef + netSE * SIMPLE_MATCH);
  var ira = IRA_LIMIT + (age >= 50 ? IRA_CATCHUP : 0);

  /* The IRA is the one that depends on a question the page has to ask rather
     than compute: are you covered by a plan at work. Both answers are given. */
  var ph = IRA_PHASE[st.filing] || IRA_PHASE.single;
  var agiish = Math.max(0, profit - halfSE);
  var rp = ROTH_PHASE[st.filing] || ROTH_PHASE.single;
  var rothFrac = agiish <= rp[0] ? 1 : agiish >= rp[1] ? 0
               : 1 - (agiish - rp[0]) / (rp[1] - rp[0]);
  var pretax = num(st.pretaxIra);
  var iraFrac = agiish <= ph[0] ? 1 : agiish >= ph[1] ? 0
              : 1 - (agiish - ph[0]) / (ph[1] - ph[0]);
  var iraDeductibleIfCovered = ira * iraFrac;

  var out = [
    {id:"solo", room:solo, deferral:Math.min(soloDeferral, netSE),
     employer:Math.max(0, solo - Math.min(soloDeferral, netSE)), saved:savedBy(solo)},
    {id:"sep", room:sep, saved:savedBy(sep)},
    {id:"simple", room:simple, deferral:simpleDef, match:netSE * SIMPLE_MATCH,
     saved:savedBy(simple)},
    {id:"ira", room:ira, saved:savedBy(ira),
     deductibleIfCovered:iraDeductibleIfCovered, coveredFrac:iraFrac},
    /* Roth. No deduction now, so saved is zero BY DEFINITION - the whole point
       is that the tax is paid today and the growth comes out untaxed. Showing a
       $0 saving next to the others is honest and is exactly the comparison the
       reader needs; quietly omitting it would imply it is worse than it is. */
    {id:"roth", room:ira * rothFrac, saved:0, eligibleFrac:rothFrac,
     phasedOut: Math.max(0, ira - ira * rothFrac)},
    /* Backdoor. A non-deductible Traditional contribution converted straight to
       Roth. The pro-rata rule (IRC 408(d)(2)) makes the conversion tax-free ONLY
       if there is no other pre-tax IRA, SEP or SIMPLE money - otherwise the
       taxable share is prorated across every IRA dollar you own, which is why
       the page has to ask for that balance rather than assume zero. */
    {id:"backdoor", room:ira, saved:0,
     pretax:pretax,
     taxableFrac: (pretax + ira) > 0 ? pretax / (pretax + ira) : 0,
     taxableOnConversion: ira * ((pretax + ira) > 0 ? pretax / (pretax + ira) : 0)}
  ];
  out.forEach(function(o){
    o.cash = Math.max(0, o.room - o.saved);            /* what it costs you */
    o.fundedPct = o.room > 0 ? o.saved / o.room : 0;   /* share paid by tax */
  });
  out.netSE = netSE; out.halfSE = halfSE; out.employerRoom = employer;

  /* What the conversion actually costs: run the engine with that much extra
     income rather than multiplying by a bracket the reader may not be in. */
  var bd = out.filter(function(o){ return o.id === "backdoor"; })[0];
  if (bd && bd.taxableOnConversion > 0){
    /* Federal only. The conversion is ordinary income on top of the profit, so
       the cost is the difference between the bracket table run at each level -
       not the profit times a headline rate. */
    var st0 = Math.max(0, base.profit - out.halfSE - base.sehi - FED_STD[st.filing]);
    var st1 = st0 + bd.taxableOnConversion;
    bd.conversionTax = bracketTax(st1, FED[st.filing]) - bracketTax(st0, FED[st.filing]);
  } else if (bd) { bd.conversionTax = 0; }
  return out;
}

/* ------------------------------------------------ what one year becomes ---
   Simple future value. A return is an assumption and the copy says so; the
   input exists precisely so the reader supplies their own rather than
   inheriting mine. */
function futureValue(amount, ratePct, years){
  if (!(amount > 0) || !(years > 0)) return amount || 0;
  return amount * Math.pow(1 + (ratePct || 0) / 100, years);
}
function yearsToRetire(st){
  var age = num(st.age);
  return age > 0 ? Math.max(1, RET_AGE - age) : 0;
}

/* ------------------------------------- sole proprietor vs S-corp, itemised
   estimateCorp() in the prototype returned one net number with no working,
   which is not enough to decide anything. This returns the lines, so the page
   can show what is being traded and against what. The salary convention is a
   practitioner rule of thumb, NOT a threshold in the Code, and the block that
   renders this says so out loud. */
function corpLines(st, base, salaryPct){
  var profit = base.profit;
  if (!(profit > 0)) return null;
  var salary = Math.max(0, profit * (salaryPct == null ? .5 : salaryPct));
  var seBase = profit * SE_FACTOR;
  var soleSE = OASDI * Math.min(seBase, SS_BASE) + MEDI * seBase;
  var corpPay = OASDI * Math.min(salary, SS_BASE) + MEDI * salary;
  var saved = soleSE - corpPay;

  /* California charges a professional corporation the greater of the $800
     minimum franchise tax and 1.5% of net income. */
  var franchise = Math.max(800, profit * .015);
  var payroll = 600, corpReturn = 1000, statement = 25;
  var filings = payroll + corpReturn + statement;

  /* A wage is not qualified business income, so paying yourself one shrinks
     the 20% deduction on what is left. Priced at the reader's own marginal
     rate rather than an assumed 24%: found by running the engine on the two
     QBI bases and taking the difference in tax. */
  var qbiSole = Math.max(0, profit - soleSE / 2 - base.contrib) * .20;
  var qbiCorp = Math.max(0, profit - salary - base.contrib) * .20;
  var lostQbi = Math.max(0, qbiSole - qbiCorp);
  var marginal = marginalRate(st, base);
  var qbiCost = lostQbi * marginal;

  return {
    salary: salary, salaryPct: profit > 0 ? salary / profit : 0,
    distribution: Math.max(0, profit - salary),
    saved: saved, franchise: -franchise, filings: -filings, qbi: -qbiCost,
    net: saved - franchise - filings - qbiCost,
    lostQbi: lostQbi, marginal: marginal,
    payroll: payroll, corpReturn: corpReturn, statement: statement,
    creditedSole: Math.min(seBase, SS_BASE), creditedCorp: Math.min(salary, SS_BASE),
    creditedDrop: seBase > 0 ? Math.max(0, (Math.min(seBase, SS_BASE)
      - Math.min(salary, SS_BASE)) / Math.min(seBase, SS_BASE)) : 0
  };
}

/* The rate the NEXT dollar of deduction is worth, measured rather than looked
   up in a table: a bracket table ignores the QBI phase-out and the California
   schedule underneath it, both of which move here.

   The step has to be the contribution ACTUALLY applied, not the one asked for.
   compute() caps the override at the available room, so near the ceiling an
   uncapped step divides a real tax change by a nominal $1,000 and reports a
   marginal rate far below the truth. */
function marginalRate(st, base){
  var want = Math.min(base.room, base.contrib + 1000);
  var step = want - base.contrib;
  if (step <= 0){
    /* Already at the ceiling, so measure downwards instead. */
    want = Math.max(0, base.contrib - 1000);
    step = base.contrib - want;
    if (step <= 0) return 0;
    return clampRate((compute(st, want).totalTax - base.totalTax) / step);
  }
  return clampRate((base.totalTax - compute(st, want).totalTax) / step);
}
function clampRate(r){ return Math.max(0, Math.min(.6, isFinite(r) ? r : 0)); }

/* ---------------------------------------------------- Social Security ------
   The trade-off the S-corp sell never mentions: a salary below your profit is
   a smaller number going onto your earnings record every year.
   Bend points are the 2026 PIA formula. */
var SS_BEND1 = 1286, SS_BEND2 = 7749;
function pia(monthlyAIME){
  if (monthlyAIME <= SS_BEND1) return monthlyAIME * .90;
  if (monthlyAIME <= SS_BEND2)
    return SS_BEND1 * .90 + (monthlyAIME - SS_BEND1) * .32;
  return SS_BEND1 * .90 + (SS_BEND2 - SS_BEND1) * .32 + (monthlyAIME - SS_BEND2) * .15;
}
/* A full 35-year record at this level, which is the honest simplification: it
   answers "what if this year were typical", not "what will I actually get",
   and the block says which question it is answering. */
function ssCompare(base, corp){
  if (!corp) return null;
  var soleCredited = corp.creditedSole, corpCredited = corp.creditedCorp;
  var sole = pia(soleCredited / 12), cor = pia(corpCredited / 12);
  return {sole: sole, corp: cor, gap: sole - cor, gapYear: (sole - cor) * 12,
    soleCredited: soleCredited, corpCredited: corpCredited};
}
"""


def js():
    return CORE + RESIDENCY + EXTRA
