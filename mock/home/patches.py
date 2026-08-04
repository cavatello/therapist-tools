#!/usr/bin/env python3
"""Edits proto5.py applies to the prototype's own engine before the designs run.

Kept in their own module because they are quoting JavaScript that itself quotes
strings, and nesting that inside proto5.py's heredocs is how escaping mistakes
get made.
"""

# --- two planner inputs the chapter needs and the prototype lacks -----------
STATE_O = '    filing:"single", age:"", entity:"sole", contrib:"",'
STATE_N = ('    filing:"single", age:"", entity:"sole", contrib:"",\n'
           '    retRet:7, retYrs:20,   /* assumed return %, and years left to invest */')

# There are two lists ending in "clients","churn": the one that WIRES the
# inputs, and the one that serialises state. The first patch hit the serialiser,
# so the selects changed value and nothing recomputed. Anchor on the .forEach
# that calls bind() so only the binder can match.
BIND_O = '"clients","churn"]\n.forEach(function(k){ bind("i-" + k, k); });'
BIND_N = ('"clients","churn","retRet","retYrs"]\n'
          '.forEach(function(k){ bind("i-" + k, k); });')

# --- an itemised S-corp comparison, replacing a bare net number -------------
CORP_FN = r"""
/* ---------- S-corp vs sole proprietor, itemised ----------------------------
   estimateCorp() returned a single net number with no working, which is not
   enough to decide anything. This returns the lines, so the chapter can show
   what is being traded and against what. The salary is the 50%-of-profit
   convention - a private-practice folk rule, NOT an IRS threshold - and the
   block says so out loud. */
function corpLines(c, salaryPct){
  if (!c || c.profit <= 0) return null;
  var salary    = Math.max(0, c.profit * (salaryPct || 0.5));
  var seBase    = c.profit * SE_FACTOR;
  var soleSE    = OASDI * Math.min(seBase, SS_BASE) + MEDI * seBase;
  var corpPay   = OASDI * Math.min(salary, SS_BASE) + MEDI * salary;
  var saved     = soleSE - corpPay;
  var franchise = Math.max(800, c.profit * 0.015);
  var filings   = 600 + 1000 + 25;   /* payroll service, 1120-S, Statement of Info */
  /* A wage is not qualified business income, so paying yourself one shrinks
     the 20% deduction on what is left. Estimated at a 24% bracket and
     labelled as an estimate wherever it is shown. */
  var qbiSole   = Math.max(0, c.profit - soleSE / 2 - (c.contrib || 0)) * 0.20;
  var qbiCorp   = Math.max(0, c.profit - salary - (c.contrib || 0)) * 0.20;
  var qbiCost   = Math.max(0, (qbiSole - qbiCorp) * 0.24);
  return {
    salary: salary,
    saved: saved, franchise: -franchise, filings: -filings, qbi: -qbiCost,
    net: saved - franchise - filings - qbiCost,
    creditedSole: seBase, creditedCorp: salary,
    creditedDrop: seBase > 0 ? (seBase - salary) / seBase : 0
  };
}
"""

# --- the chapter's own controls, moved to the top and extended --------------
# The prototype's drawer had filing / age / contribution. Planning also needs
# what return you assume and how long you have; without them "what it becomes"
# is a number somebody else picked.
PLANNER = """
<div class="plan" id="plan">
  <div class="plan-h"><em>Step one &middot; set up your plan</em>
    <h3>The most you can put away this year</h3></div>
  <div class="plan-max">
    <div class="pm big"><i>Maximum you can contribute</i><b id="pl-room">$0</b>
      <u>a Solo 401(k) on this profit</u></div>
    <div class="pm good"><i>Tax that removes</i><b id="pl-save">$0</b>
      <u>you would otherwise pay this April</u></div>
    <div class="pm"><i>So it costs you</i><b id="pl-own">$0</b>
      <u>of spendable cash</u></div>
  </div>
  <p class="plan-note" id="pl-note"></p>
  <div class="plan-in">
    <label class="f sm"><em>Filing status</em><span class="fv"><select id="i-filing">
      <option value="single">Single</option><option value="mfj">Married, joint</option>
      <option value="hoh">Head of household</option></select></span></label>
    <label class="f sm"><em>Your age</em><span class="fv"><input id="i-age" type="number"
      min="0" max="90" placeholder="40"></span></label>
    <label class="f sm"><em>Contribute this year</em><span class="fv">$<input id="i-contrib"
      type="number" min="0" max="80000" step="500" placeholder="0"></span></label>
    <label class="f sm"><em>Assumed return</em><span class="fv"><select id="i-retRet">
      <option value="4">4% &middot; cautious</option>
      <option value="7" selected>7% &middot; long-run average</option>
      <option value="9">9% &middot; optimistic</option>
      <option value="11">11% &middot; aggressive</option></select></span></label>
    <label class="f sm"><em>Years invested</em><span class="fv"><select id="i-retYrs">
      <option value="10">10 years</option>
      <option value="20" selected>20 years</option>
      <option value="25">25 years</option>
      <option value="30">30 years</option></select></span></label>
    <button class="maxbtn" id="b-max">Max it out</button>
  </div>
  <div class="plan-grow" id="pl-grow"></div>
</div>
"""

# --- the closing block: the structure question, in full --------------------
CORP_BLOCK = """
<div class="corpb" id="corpb">
  <div class="corp-h"><em>The last decision</em>
    <h3>Sole proprietor, or a professional corporation?</h3>
    <p>The other lever people are sold. It is worth comparing properly, because on most
    solo practices it is close &mdash; and because what it costs you is not only money.</p></div>
  <div id="corp-body"></div>
</div>
"""
