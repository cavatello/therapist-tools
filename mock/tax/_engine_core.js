"use strict";
/* ==========================================================================
   ENGINE.  Constants lifted verbatim from the production tool so the numbers
   in this prototype are defensible rather than decorative.
   ========================================================================== */
var FED = {
  single:[[0,.10],[12400,.12],[50400,.22],[105700,.24],[201775,.32],[256225,.35],[640600,.37]],
  mfj:[[0,.10],[24800,.12],[100800,.22],[211400,.24],[403550,.32],[512450,.35],[768700,.37]],
  hoh:[[0,.10],[17700,.12],[67450,.22],[105700,.24],[201750,.32],[256200,.35],[640600,.37]]
};
/* Head of household corrected 2 Aug 2026 to FTB Schedule Z. Seven of the
   nine thresholds here were wrong - 52528/67699/83790/98974/505219/606329/
   1010718 against the published 52530/67716/83805/98990/505208/606251/
   1010417. It produced a wrong-but-plausible California tax for every
   head-of-household filer and nothing else, which is why it survived.
   ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf */
var CA = {
  single:[[0,.01],[11079,.02],[26264,.04],[41452,.06],[57542,.08],[72724,.093],[371479,.103],[445771,.113],[742953,.123]],
  mfj:[[0,.01],[22158,.02],[52528,.04],[82904,.06],[115084,.08],[145448,.093],[742958,.103],[891542,.113],[1485906,.123]],
  hoh:[[0,.01],[22173,.02],[52530,.04],[67716,.06],[83805,.08],[98990,.093],[505208,.103],[606251,.113],[1010417,.123]]
};
var FED_STD = {single:16100, mfj:32200, hoh:24150};
var CA_STD  = {single:5706,  mfj:11412, hoh:11412};
var QBI_PHASE = {single:[201750,276750], hoh:[201750,276750], mfj:[403500,553500]};
var ADDL_MED = {single:200000, hoh:200000, mfj:250000};
var SS_BASE = 184500, OASDI = .124, MEDI = .029, SE_FACTOR = .9235;
var UI_BASE = 7000, CA_UI = .034, CA_ETT = .001, FUTA = .006, FICA_EMP = .0765;
var K401_DEFERRAL = 24500, K401_CATCHUP = 8000, LIMIT_415 = 72000, COMP_CAP = 360000;
var WEEKS_FULL = 52;

function bracketTax(income, br){
  if (income <= 0) return 0;
  var t = 0;
  for (var i = 0; i < br.length; i++){
    var lo = br[i][0], rate = br[i][1];
    var hi = i + 1 < br.length ? br[i+1][0] : Infinity;
    if (income > lo) t += (Math.min(income, hi) - lo) * rate;
  }
  return t;
}
var fmt = function(n){
  n = Math.round(n || 0);
  return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US");
};

/* ---------- state ---------- */
var EXPENSES = [
  ["rent","Office rent",0], ["liability","Malpractice insurance",0],
  ["health","Health insurance",0], ["ehr","EHR & software",0],
  ["supervision","Supervision",0], ["marketing","Marketing & directories",0],
  ["phone","Phone, internet, tech",0], ["legal","Accounting & legal",0],
  ["license","Licensure & dues",0], ["ce","Continuing education",0],
  ["supplies","Office supplies",0], ["misc","Anything else",0]
];
var STARTER = {rent:1800, liability:33, health:540, ehr:89, supervision:150, marketing:60,
  phone:95, legal:120, license:35, ce:60, supplies:45, misc:0};
var CHANNELS = [["pt","Psychology Today"],["web","Your website"],["ref","Referrals"]];

function blank(){
  var s = {rate:"", sessions:"", weeksOff:2, billingPct:2.5,
    assocOn:false, assocCount:"", assocRate:"", assocSessions:"", assocVac:"", assocSplit:"",
    assocSup:"", assocLiab:"", assocOffice:"", assocEhr:"", assocWc:"", assocPayroll:"",
    retreatOn:false, retPeople:"", retRate:"", retPerYear:"",
    secondOn:false, secRate:"", secSessions:"",
    filing:"single", age:"", entity:"sole", contrib:"",
    tenure:"", clients:"", churn:"", exp:{}, chan:{}};
  EXPENSES.forEach(function(e){ s.exp[e[0]] = ""; });
  CHANNELS.forEach(function(c){ s.chan[c[0]] = {views:"", enq:"", got:""}; });
  return s;
}
var S = blank();

var EXAMPLE = {rate:200, sessions:25, weeksOff:2, billingPct:2.5,
  assocOn:false, assocCount:"", assocRate:"", assocSessions:"", assocVac:"", assocSplit:"",
  assocSup:"", assocLiab:"", assocOffice:"", assocEhr:"", assocWc:"", assocPayroll:"",
  retreatOn:false, retPeople:"", retRate:"", retPerYear:"",
  secondOn:false, secRate:"", secSessions:"",
  filing:"single", age:40, entity:"sole", contrib:"",
  tenure:21, clients:24, churn:2,
  exp:Object.assign({}, STARTER),
  chan:{pt:{views:210,enq:22,got:6}, web:{views:140,enq:11,got:3}, ref:{views:70,enq:29,got:5}}};

var num = function(v){ var n = parseFloat(v); return isFinite(n) ? n : 0; };

/* ---------- the model ---------- */
function compute(st, contribOverride){
  var weeks = Math.max(0, WEEKS_FULL - num(st.weeksOff));
  var own = num(st.rate) * num(st.sessions) * weeks;
  var second = st.secondOn ? num(st.secRate) * num(st.secSessions) * weeks : 0;
  var retreat = st.retreatOn
    ? num(st.retPeople) * num(st.retRate) * num(st.retPerYear) : 0;

  /* associates — revenue is yours, their pay is an employer cost */
  var aWeeks = Math.max(0, WEEKS_FULL - num(st.assocVac));
  var aN = num(st.assocCount), aSessWk = num(st.assocSessions);
  var aRev = st.assocOn ? aN * aSessWk * aWeeks * num(st.assocRate) : 0;
  var aSplit = num(st.assocSplit) / 100;
  var aSupHrs = aSessWk > 10 ? 2 : 1;
  var aSup = st.assocOn ? aN * aSupHrs * aWeeks * num(st.assocSup) : 0;
  var aWages = aRev * aSplit + aSup;
  var aWagesPer = aN > 0 ? aWages / aN : 0;
  var aUiBase = aN * Math.min(aWagesPer, UI_BASE);
  var aEmpTax = st.assocOn
    ? aWages * FICA_EMP + aUiBase * (CA_UI + CA_ETT + FUTA) + aWages * (num(st.assocWc) / 100)
    : 0;
  var aFixed = st.assocOn
    ? aN * (num(st.assocLiab) + (num(st.assocOffice) + num(st.assocEhr)) * 12)
      + num(st.assocPayroll) * 12
    : 0;
  var aCost = aWages + aEmpTax + aFixed;

  var gross = own + second + retreat + aRev;

  var expFlat = 0;
  EXPENSES.forEach(function(e){ expFlat += num(st.exp[e[0]]) * 12; });
  var expPct = gross * (num(st.billingPct) / 100);
  var sehi = num(st.exp.health) * 12;            /* Schedule 1, not C */
  var expenses = expFlat + expPct;

  var profit = gross - (expenses - sehi) - aCost;   /* health cover comes out later */

  /* self-employment tax */
  var seBase = Math.max(0, profit) * SE_FACTOR;
  var seSS = OASDI * Math.min(seBase, SS_BASE);
  var seMed = MEDI * seBase;
  var addl = Math.max(0, seBase - ADDL_MED[st.filing]) * .009;
  var seTax = seSS + seMed + addl;
  var halfSE = (seSS + seMed) / 2;

  /* retirement room, Solo 401(k) */
  var catchUp = num(st.age) >= 50 ? K401_CATCHUP : 0;
  var netSE = Math.max(0, profit - halfSE);
  var employer = Math.min(netSE, COMP_CAP) * .20;
  var room = Math.max(0, Math.min(K401_DEFERRAL + catchUp + employer, LIMIT_415 + catchUp));
  var contrib = contribOverride != null ? contribOverride
    : Math.min(num(st.contrib), room);

  /* federal */
  var agi = Math.max(0, profit - halfSE - contrib - sehi);
  var taxableBefore = Math.max(0, agi - FED_STD[st.filing]);
  var ph = QBI_PHASE[st.filing];
  var frac = taxableBefore <= ph[0] ? 1
    : taxableBefore >= ph[1] ? 0
    : 1 - (taxableBefore - ph[0]) / (ph[1] - ph[0]);
  var qbiBase = Math.max(0, profit - halfSE - contrib);
  var qbi = Math.min(qbiBase * .20, taxableBefore * .20) * frac;
  var fedTaxable = Math.max(0, taxableBefore - qbi);
  var fed = bracketTax(fedTaxable, FED[st.filing]);

  /* California — conforms on 401(k) deferrals, no QBI */
  var caTaxable = Math.max(0, profit - halfSE - contrib - sehi - CA_STD[st.filing]);
  var ca = bracketTax(caTaxable, CA[st.filing]);

  var totalTax = seTax + fed + ca;
  var net = profit - totalTax - contrib - sehi;

  return {weeks:weeks, own:own, second:second, retreat:retreat,
    aRev:aRev, aWages:aWages, aEmpTax:aEmpTax, aFixed:aFixed, aCost:aCost, aSup:aSup,
    gross:gross, expenses:expenses, expFlat:expFlat, expPct:expPct, sehi:sehi,
    profit:profit, seTax:seTax, fed:fed, ca:ca, totalTax:totalTax, qbi:qbi,
    room:room, contrib:contrib, net:net};
}

