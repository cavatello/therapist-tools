/* ==========================================================================
   RESIDENCY ENGINE.  THIS FILE IS NOW THE SOURCE OF TRUTH.

   It was lifted out of app.js by lift_residency.py - every block below is a
   byte-for-byte substring of that file, comments included - and app.js has
   since been deleted. Edit here. lift_residency.py is kept for the record of
   how the lift was done, but it can no longer be run.

   It lives inside an IIFE because app.js and _engine_core.js use DIFFERENT
   NAMES for the same quantities, and in two places slightly different bracket
   tables. Sharing a scope would be a redeclaration error at best and a silent
   disagreement about which table applied at worst. In here, the residency
   functions see exactly the constants app.js gives them and nothing else.
   ========================================================================== */
var RESID = (function(){
"use strict";
const FED_STD = 16100,
  CA_STD = 5540;

const FED_BRACKETS = [[0, 0.10], [12400, 0.12], [50400, 0.22], [105700, 0.24], [201775, 0.32], [256225, 0.35], [640600, 0.37]];

const CA_BRACKETS = [[0, 0.01], [11079, 0.02], [26264, 0.04], [41452, 0.06], [57542, 0.08], [72724, 0.093], [371479, 0.103], [445771, 0.113], [742953, 0.123]];

const FED_STD_BY_STATUS = {
  single: 16100,
  mfj: 32200,
  mfj_dependents: 32200,
  hoh: 24150
};

const CA_STD_BY_STATUS = {
  single: 5706,
  mfj: 11412,
  mfj_dependents: 11412,
  hoh: 11412
};

const FED_BRACKETS_BY_STATUS = {
  single: [[0, 0.10], [12400, 0.12], [50400, 0.22], [105700, 0.24], [201775, 0.32], [256225, 0.35], [640600, 0.37]],
  mfj: [[0, 0.10], [24800, 0.12], [100800, 0.22], [211400, 0.24], [403550, 0.32], [512450, 0.35], [768700, 0.37]],
  mfj_dependents: [[0, 0.10], [24800, 0.12], [100800, 0.22], [211400, 0.24], [403550, 0.32], [512450, 0.35], [768700, 0.37]],
  hoh: [[0, 0.10], [17700, 0.12], [67450, 0.22], [105700, 0.24], [201750, 0.32], [256200, 0.35], [640600, 0.37]]
};

const CA_BRACKETS_BY_STATUS = {
  single: [[0, 0.01], [11079, 0.02], [26264, 0.04], [41452, 0.06], [57542, 0.08], [72724, 0.093], [371479, 0.103], [445771, 0.113], [742953, 0.123]],
  mfj: [[0, 0.01], [22158, 0.02], [52528, 0.04], [82904, 0.06], [115084, 0.08], [145448, 0.093], [742958, 0.103], [891542, 0.113], [1485906, 0.123]],
  mfj_dependents: [[0, 0.01], [22158, 0.02], [52528, 0.04], [82904, 0.06], [115084, 0.08], [145448, 0.093], [742958, 0.103], [891542, 0.113], [1485906, 0.123]],
  hoh: [[0, 0.01], [22173, 0.02], [52530, 0.04], [67716, 0.06], [83805, 0.08], [98990, 0.093], [505208, 0.103], [606251, 0.113], [1010417, 0.123]]
};

const QBI_PHASE_BY_STATUS = {
  single: [201750, 276750],
  hoh: [201750, 276750],
  mfj: [403500, 553500],
  mfj_dependents: [403500, 553500]
};

// IRC s.1401(b)(2): $200k single/HOH, $250k joint, $125k MFS. Not indexed.
const ADDL_MED_THRESH_BY_STATUS = {
  single: 200000,
  hoh: 200000,
  mfj: 250000,
  mfj_dependents: 250000
};

const QBI_RATE = 0.20,
  QBI_PHASE_START = 201750,
  QBI_PHASE_END = 276750;

const ADDL_MED_THRESH = 200000,
  ADDL_MED_RATE = 0.009;

// CA Prop 63 mental health services tax: 1% on taxable income over $1,000,000.
// RTC s.17043 - the threshold is NOT indexed and is $1m for joint filers too.
const CA_MHS_THRESH = 1000000, CA_MHS_RATE = 0.01;

const OASDI_RATE = 0.124;

const MEDICARE_RATE = 0.029;

const SE_FACTOR = 0.9235;

const SS_WAGE_BASE = 184500;

const NY_STD = 8000;

const NY_BRACKETS = [[0, 0.039], [8500, 0.044], [11700, 0.0515], [13900, 0.054], [80650, 0.059], [215400, 0.0685], [1077550, 0.0965], [5000000, 0.103], [25000000, 0.109]];

const NYC_BRACKETS = [[0, 0.03078], [12000, 0.03762], [25000, 0.03819], [50000, 0.03876]];

// ----------------------------------------------------------------------------
// RESIDENCY COMPARISON — simplified 2026 estimates for a self-employed therapist
// comparing California vs. Berlin, Germany vs. Portugal on the same practice
// revenue. Currency: 1 EUR ≈ 1.14 USD (July 2026 reference rate); real running
// costs (rent, insurance, EHR, etc.) are assumed portable and unchanged.
// Germany: assumes "Freiberufler" (liberal-profession) status — no trade tax —
// with statutory health + long-term-care insurance (~19.6%, capped at the 2026
// contribution ceiling), income tax per the official §32a EStG 2026 formula,
// and the solidarity surcharge above its exemption threshold. Excludes church
// tax (assumes opted out) and any mandatory professional pension fund
// (Versorgungswerk) that some healthcare professions are required to join.
// Portugal: Categoria B, simplified regime — IRS is charged on 75% of gross
// revenue (the standard services coefficient; actual expenses aren't
// separately deducted under this regime), using the 2026 nine-bracket IRS
// table plus the solidarity surcharge, and an independent-worker social
// security contribution (~15% effective on gross revenue). Excludes the
// municipal surcharge (0-1.5%, varies by city) and NHR/IFICI special regimes
// (mostly closed to new applicants since 2024).
// ----------------------------------------------------------------------------
const EUR_TO_USD = 1.14;

const USD_TO_EUR = 1 / EUR_TO_USD;

// Metropolitan Commuter Transportation Mobility Tax, self-employed, Zone 1
// (Bronx, Kings, New York, Queens, Richmond - so Brooklyn is Zone 1). Rate and
// threshold both changed for tax years beginning on or after 1 Jan 2026: the
// old 0.34% above $50,000 was Zone-2-era and is wrong for a Brooklyn practice
// in both directions - it charged someone at $100k who owes nothing, and
// undercharged everyone above $150k by nearly half.
// tax.ny.gov/legal/2025/pit-corp-changes.htm
const MCTMT_THRESHOLD = 150000,
  MCTMT_RATE = 0.0060;

// NYC Unincorporated Business Tax. The tax a self-employed New Yorker is most
// likely never to have heard of until they owe it: 4% on business income, and
// a sole proprietorship practising a profession is squarely inside it. Figures
// from the 2025 Form NYC-202S:
//   allowance for the taxpayer's own services  lesser of 20% of income or $10,000
//   specific exemption                         $5,000
//   rate                                       4%
//   business tax credit  full at or below $3,400 of tax, none at or above
//                        $5,400, and tax x (5,400 - tax) / 2,000 in between
// nyc.gov/site/finance/business/business-unincorporated-business-tax-ubt.page
const UBT_RATE = 0.04,
  UBT_SERVICES_PCT = 0.20,
  UBT_SERVICES_CAP = 10000,
  UBT_EXEMPTION = 5000,
  UBT_CREDIT_FULL = 3400,
  UBT_CREDIT_NONE = 5400;

// A NYC resident can then credit part of the UBT against their city income tax
// (Form IT-219): 100% at or below $42,000 of city taxable income, sliding to
// 23% at $142,000 and flat 23% above. Capped at the city tax itself.
const UBT_PIT_LOW = 42000, UBT_PIT_HIGH = 142000, UBT_PIT_FLOOR = 0.23;

const PA_FLAT_RATE = 0.0307;

const PITTSBURGH_EIT_RATE = 0.03;

const PITTSBURGH_LST = 52;

const FR_BRACKETS = [[0, 0], [11600, 0.11], [29579, 0.30], [84577, 0.41], [181917, 0.45]];

const FR_COTISATION_RATE = 0.40;

// CSG (9.2%) + CRDS (0.5%) on 98.25% of activity income. Carved out of the
// blended rate above only so the foreign-tax-credit maths below can name it.
const FR_CSG_RATE = 0.097;

const USD_TO_AED = 3.6725;

// 2026 foreign earned income exclusion, Rev. Proc. 2025-32 (up from $130,000).
// irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026
const FEIE_2026 = 132900;

const AU_BRACKETS = [[0, 0], [18200, 0.16], [45000, 0.30], [135000, 0.37], [190000, 0.45]];

const USD_TO_AUD = 1.43;

const PT_BRACKETS = [[0, 0.1325], [7703, 0.165], [11623, 0.22], [16472, 0.25], [21321, 0.32], [27146, 0.355], [39791, 0.435], [51997, 0.45], [81199, 0.48]];

function bracketTax(income, brackets) {
  if (income <= 0) return 0;
  let t = 0;
  for (let i = 0; i < brackets.length; i++) {
    const lo = brackets[i][0],
      rate = brackets[i][1];
    const hi = i + 1 < brackets.length ? brackets[i + 1][0] : Infinity;
    if (income > lo) t += (Math.min(income, hi) - lo) * rate;else break;
  }
  return t;
}

// Every US residency card sits on an identical federal layer: same deductible
// half of SE tax, same standard deduction, same QBI rules. That block used to
// be copy-pasted into each location function and every copy was hardcoded to
// the single-filer constants - so a married user compared a status-aware
// California against a single-filer New York and a single-filer Pittsburgh,
// and the gap between the cards was partly just the filing status changing
// underneath them. One helper now, status-aware, shared by all of them.
//
// personalRetirement carries the same meaning as in computeYear: the slice of
// retireDed that is a personal IRA rather than a business plan, and so reduces
// AGI without reducing QBI. No US card passes a non-zero value today; the
// parameter is here so a future one cannot silently get it wrong.
function fedLayer(schedC, w2Wages, halfSE, retireDed, filingStatus, personalRetirement) {
  filingStatus = filingStatus || "single";
  retireDed = retireDed || 0;
  w2Wages = w2Wages || 0;
  const fedStd = FED_STD_BY_STATUS[filingStatus] || FED_STD;
  const fedBrackets = FED_BRACKETS_BY_STATUS[filingStatus] || FED_BRACKETS;
  const qbiWindow = QBI_PHASE_BY_STATUS[filingStatus] || [QBI_PHASE_START, QBI_PHASE_END];
  const qbiStart = qbiWindow[0], qbiEnd = qbiWindow[1];
  const agi = Math.max(0, schedC + w2Wages - halfSE - retireDed);
  const taxableBeforeQBI = Math.max(0, agi - fedStd);
  // Treas. Reg. s.1.199A-3(b)(1)(vi) - see the longer note in computeYear.
  const bizRetireDed = Math.max(0, retireDed - (personalRetirement || 0));
  const qbiIncome = Math.max(0, schedC - halfSE - bizRetireDed);
  let pct;
  if (taxableBeforeQBI <= qbiStart) pct = 1;else if (taxableBeforeQBI >= qbiEnd) pct = 0;else pct = 1 - (taxableBeforeQBI - qbiStart) / (qbiEnd - qbiStart);
  const qbiDed = Math.min(QBI_RATE * qbiIncome, QBI_RATE * taxableBeforeQBI) * pct;
  return {
    agi,
    taxableBeforeQBI,
    qbiDed,
    fedTax: bracketTax(Math.max(0, taxableBeforeQBI - qbiDed), fedBrackets)
  };
}

// IRC s.1401(b)(2). California's own path has always charged this; the NYC and
// Pittsburgh cards never did, which quietly favoured them at high income by up
// to 0.9% of everything over the threshold.
function addlMedFor(seBase, w2Wages, filingStatus) {
  const thresh = ADDL_MED_THRESH_BY_STATUS[filingStatus || "single"] || ADDL_MED_THRESH;
  return Math.max(0, seBase + (w2Wages || 0) - thresh) * ADDL_MED_RATE;
}

function computeUBT(businessIncome, nycTaxableIncome, nycTax) {
  if (!(businessIncome > 0)) return {gross: 0, credit: 0, net: 0, pitCredit: 0, afterPit: 0};
  const allowance = Math.min(UBT_SERVICES_PCT * businessIncome, UBT_SERVICES_CAP);
  const taxable = Math.max(0, businessIncome - allowance - UBT_EXEMPTION);
  const gross = taxable * UBT_RATE;
  const credit = gross <= UBT_CREDIT_FULL ? gross
    : gross >= UBT_CREDIT_NONE ? 0
    : gross * (UBT_CREDIT_NONE - gross) / (UBT_CREDIT_NONE - UBT_CREDIT_FULL);
  const net = Math.max(0, gross - credit);
  const pct = nycTaxableIncome <= UBT_PIT_LOW ? 1
    : nycTaxableIncome >= UBT_PIT_HIGH ? UBT_PIT_FLOOR
    : 1 - (nycTaxableIncome - UBT_PIT_LOW) / (UBT_PIT_HIGH - UBT_PIT_LOW) * (1 - UBT_PIT_FLOOR);
  const pitCredit = Math.min(net * pct, Math.max(0, nycTax));
  return {gross, credit, net, pitCredit, afterPit: net - pitCredit};
}

// What a US citizen abroad would owe Washington on this profit if no foreign
// tax credit applied. No self-employment tax - the US has totalization
// agreements with Germany, Portugal, France and Australia - and no QBI, since
// 199A needs a US trade or business. This exists so the section can *show*
// that the credit covers the US bill rather than asserting it.
function usFedAbroad(profitUSD, filingStatus) {
  const std = FED_STD_BY_STATUS[filingStatus] || FED_STD_BY_STATUS.single;
  const br = FED_BRACKETS_BY_STATUS[filingStatus] || FED_BRACKETS_BY_STATUS.single;
  return bracketTax(Math.max(0, profitUSD - std), br);
}

function germanIncomeTax(zve) {
  if (zve <= 12348) return 0;
  if (zve <= 17799) {
    const y = (zve - 12348) / 10000;
    return (914.51 * y + 1400) * y;
  }
  if (zve <= 69878) {
    const z = (zve - 17799) / 10000;
    return (173.10 * z + 2397) * z + 1034.87;
  }
  if (zve <= 277825) return 0.42 * zve - 11135.63;
  return 0.45 * zve - 19470.38;
}

function portugalSolidarity(taxable) {
  let s = 0;
  if (taxable > 250000) s += (taxable - 250000) * 0.05;
  if (taxable > 80000) s += (Math.min(taxable, 250000) - 80000) * 0.025;
  return s;
}

// retireDed is a maxed Solo 401(k)/IRA deduction. It is an above-the-line
// federal adjustment (Schedule 1), NOT a Schedule C expense, which decides
// exactly which of New York's five taxes it touches:
//   NY State PIT   yes - NY starts from federal AGI and has no addback for it
//   NYC resident   yes - same base, per NYC Admin Code s.11-1712(a)
//   NYC UBT        NO  - s.11-507 allows only deductions allowable federally
//                        and "directly connected with the business", and
//                        s.11-507(3) bars amounts paid to a proprietor. The
//                        deduction is simply never in the UBT base.
//   MCTMT          NO  - base is net earnings from self-employment (s.1402),
//                        a Schedule SE figure the adjustment never reaches
//   SE tax         NO  - same reason
function computeNYC(revenueUSD, expensesUSD, retireDed, filingStatus, sehi) {
  retireDed = retireDed || 0;
  const sehiPremium = Math.max(0, sehi || 0);
  // IRC s.162(l) again - the premium is inside expensesUSD but belongs on
  // Schedule 1, so add it back before Schedule C and take it above the line.
  // cashProfit is what actually reaches the bank and keeps the premium
  // subtracted; schedC is the tax figure and does not.
  const cashProfit = Math.max(0, revenueUSD - expensesUSD);
  const schedC = Math.max(0, revenueUSD - expensesUSD + sehiPremium);
  const seBase = schedC * 0.9235;
  const seTax = Math.min(seBase, SS_WAGE_BASE) * 0.124 + seBase * 0.029;
  const halfSE = seTax / 2;
  // sehiDed rides in alongside retireDed: both cut AGI without touching
  // Schedule C and both come out of the QBI base, so fedLayer treats them
  // identically. New York starts from federal AGI, so the deduction reaches
  // the NY and NYC income taxes automatically - and reaches neither the UBT
  // (s.11-507(3) bars amounts paid to a proprietor) nor the MCTMT nor SE tax,
  // all three of which run off the business figure below.
  const sehiDed = Math.min(sehiPremium, Math.max(0, schedC - halfSE));
  const fed = fedLayer(schedC, 0, halfSE, retireDed + sehiDed, filingStatus);
  const agi = fed.agi;
  const fedTax = fed.fedTax;
  const addlMed = addlMedFor(seBase, 0, filingStatus);
  const nyTaxable = Math.max(0, agi - NY_STD);
  const nyTax = bracketTax(nyTaxable, NY_BRACKETS);
  const nycTax = bracketTax(nyTaxable, NYC_BRACKETS);
  const mctmt = schedC > MCTMT_THRESHOLD ? schedC * MCTMT_RATE : 0;
  const ubt = computeUBT(schedC, nyTaxable, nycTax);
  const totalTax = fedTax + seTax + addlMed + nyTax + nycTax + mctmt + ubt.afterPit;
  return {
    netUSD: cashProfit - totalTax,
    taxUSD: totalTax,
    fedTaxUSD: fedTax,
    seTaxUSD: seTax,
    addlMedUSD: addlMed,
    nyTaxUSD: nyTax,
    nycTaxUSD: nycTax,
    mctmtUSD: mctmt,
    ubtGrossUSD: ubt.gross,
    ubtCreditUSD: ubt.credit,
    ubtNetUSD: ubt.net,
    ubtPitCreditUSD: ubt.pitCredit,
    ubtUSD: ubt.afterPit
  };
}

// retireDed here buys far less than it does in California or New York, and
// that is the point of showing it. Pennsylvania does not start from federal
// AGI: it computes net profits under its own rules, and 61 Pa. Code s.101.6(c)(8)
// says contributions "by, on behalf of or attributable to a self-employed
// person are not excludable from either compensation or net profits". Both
// halves of a Solo 401(k) - the deferral and the employer profit share - are
// therefore fully taxable by PA in the year contributed. The Local Tax
// Enabling Act defines the local EIT base by reference to that same PA
// figure, so Pittsburgh's 3% follows it. Only the federal tax moves.
function computePittsburgh(revenueUSD, expensesUSD, retireDed, filingStatus, sehi) {
  retireDed = retireDed || 0;
  const sehiPremium = Math.max(0, sehi || 0);
  const cashProfit = Math.max(0, revenueUSD - expensesUSD);
  const schedC = Math.max(0, revenueUSD - expensesUSD + sehiPremium);
  const seBase = schedC * 0.9235;
  const seTax = Math.min(seBase, SS_WAGE_BASE) * 0.124 + seBase * 0.029;
  const halfSE = seTax / 2;
  const sehiDed = Math.min(sehiPremium, Math.max(0, schedC - halfSE));
  const fedTax = fedLayer(schedC, 0, halfSE, retireDed + sehiDed, filingStatus).fedTax;
  const addlMed = addlMedFor(seBase, 0, filingStatus);
  // PA deliberately keeps the premium deducted (cashProfit, not schedC).
  // Pennsylvania computes net profits under its own rules and there is no
  // citable PA source either way on a proprietor's OWN health premium. Two PA
  // Department of Revenue PIT Guide chapters were read in full and both are
  // silent on it:
  //   "Net Income (Loss) from the Operation of a Business, Profession or Farm"
  //     - covers retirement contributions explicitly, health insurance not at all
  //   "Gross Compensation"
  //     - says PA allows no deduction for "personal expenses, federal itemized
  //       deductions, or federal standard deductions", which implies PA would
  //       not honour the federal s.162(l) ADJUSTMENT - but that chapter is about
  //       employee compensation, and it does not answer whether the premium is
  //       an allowable business expense on PA Schedule C, which is the actual
  //       question here and the mechanism this code uses.
  // So: genuinely unresolved, not merely unchecked. Leaving PA's treatment
  // exactly as it was is the honest default. Do not "fix" this to match the
  // federal add-back without a citation, and do not re-run the same search -
  // it needs a PA-40 Schedule C instruction or a Department ruling, not a
  // general PIT Guide chapter.
  const paTax = cashProfit * PA_FLAT_RATE;
  const eitTax = cashProfit * PITTSBURGH_EIT_RATE;
  const lst = PITTSBURGH_LST;
  const totalTax = fedTax + seTax + addlMed + paTax + eitTax + lst;
  return {
    netUSD: cashProfit - totalTax,
    taxUSD: totalTax,
    fedTaxUSD: fedTax,
    seTaxUSD: seTax,
    addlMedUSD: addlMed,
    paTaxUSD: paTax,
    eitTaxUSD: eitTax,
    lstUSD: lst
  };
}

function computeFrance(revenueUSD, expensesUSD) {
  const revenueEUR = revenueUSD * USD_TO_EUR;
  const expensesEUR = expensesUSD * USD_TO_EUR;
  const profitEUR = Math.max(0, revenueEUR - expensesEUR);
  const cotisationsEUR = profitEUR * FR_COTISATION_RATE;
  const taxableEUR = Math.max(0, profitEUR - cotisationsEUR);
  const incomeTaxEUR = bracketTax(taxableEUR, FR_BRACKETS);
  const netEUR = profitEUR - cotisationsEUR - incomeTaxEUR;
  // CSG + CRDS sit inside the blended cotisation rate above, but they are the
  // one part of it a US citizen can claim as a foreign tax credit: the US and
  // France memorialised in 2019 that CSG/CRDS are NOT social taxes covered by
  // the totalization agreement, and the IRS no longer challenges the credit.
  // France is the only card where the no-residual-US-tax conclusion depends on
  // this - without it, roughly $8,500 a year would still be owed at $253,500
  // of profit. rsmus.com/insights/tax-alerts/2019/irs-allows-credit-for-certain-french-social-taxes.html
  const csgEUR = profitEUR * FR_CSG_RATE;
  return {
    netUSD: netEUR * EUR_TO_USD,
    netEUR,
    taxUSD: (cotisationsEUR + incomeTaxEUR) * EUR_TO_USD,
    cotisationsUSD: cotisationsEUR * EUR_TO_USD,
    incomeTaxUSD: incomeTaxEUR * EUR_TO_USD,
    csgUSD: csgEUR * EUR_TO_USD
  };
}

// The UAE is the only card here where "local tax" is not a fair proxy for what
// a US citizen actually pays, and it was wrong for two compounding reasons:
//
//   1. The FEIE does not touch self-employment tax. The IRS is explicit: "You
//      must take all your self-employment income into account in figuring your
//      net earnings from self-employment, even if all, or a portion of, gross
//      income was excluded." Only a totalization agreement removes it - and
//      the UAE has none, a fact this app already states two paragraphs above
//      the card while the arithmetic ignored it.
//   2. Everywhere else on this list, the foreign tax credit roughly cancels
//      the US income tax, because Germany, France, Portugal and Australia all
//      tax more heavily than the US does. The UAE taxes almost nothing, so
//      there is no credit to claim and the US bill lands in full above the
//      exclusion.
//
// Net effect: this card used to show pre-tax profit as though it were
// take-home, which made the single most eye-catching option on the page also
// the least true. Stacking follows IRC 911(f): the non-excluded income is
// taxed at the rate it would have faced had the excluded income been counted,
// so tax the whole amount and subtract the tax on the exclusion. No QBI -
// 199A needs a US trade or business.
function computeUAE(revenueUSD, expensesUSD, filingStatus) {
  const revenueAED = revenueUSD * USD_TO_AED;
  const expensesAED = expensesUSD * USD_TO_AED;
  const profitAED = Math.max(0, revenueAED - expensesAED);
  const corpTax = revenueAED > 1000000 ? Math.max(0, profitAED - 375000) * 0.09 : 0;
  const profitUSD = profitAED / USD_TO_AED;
  const uaeTax = corpTax / USD_TO_AED;

  const seBase = profitUSD * 0.9235;
  const seTax = Math.min(seBase, SS_WAGE_BASE) * 0.124 + seBase * 0.029;
  // Additional Medicare tax rides along with SE tax and, like it, is untouched
  // by the exclusion. Included so this card models US federal tax the same way
  // every other US location on this page does.
  const addlMedThresh = ADDL_MED_THRESH_BY_STATUS[filingStatus] || ADDL_MED_THRESH_BY_STATUS.single;
  const addlMed = Math.max(0, seBase - addlMedThresh) * ADDL_MED_RATE;

  const fedStd = FED_STD_BY_STATUS[filingStatus] || FED_STD_BY_STATUS.single;
  const brackets = FED_BRACKETS_BY_STATUS[filingStatus] || FED_BRACKETS_BY_STATUS.single;
  const taxableAll = Math.max(0, profitUSD - seTax / 2 - fedStd);
  const excluded = Math.min(profitUSD, FEIE_2026);
  const fedTax = Math.max(0, bracketTax(taxableAll, brackets)
    - bracketTax(Math.min(excluded, taxableAll), brackets));

  const usTax = seTax + addlMed + fedTax;
  const netUSD = profitUSD - uaeTax - usTax;
  return {
    netUSD,
    netAED: netUSD * USD_TO_AED,
    taxUSD: uaeTax + usTax,
    uaeTax, usTax, seTax, addlMed, fedTax, excluded
  };
}

function computeBrisbane(revenueUSD, expensesUSD) {
  const revenueAUD = revenueUSD * USD_TO_AUD;
  const expensesAUD = expensesUSD * USD_TO_AUD;
  const profitAUD = Math.max(0, revenueAUD - expensesAUD);
  const incomeTax = bracketTax(profitAUD, AU_BRACKETS);
  const medicare = profitAUD * 0.02;
  const sbOffset = Math.min(incomeTax * 0.08, 1000);
  const totalTax = Math.max(0, incomeTax - sbOffset) + medicare;
  const netAUD = profitAUD - totalTax;
  return {
    netUSD: netAUD / USD_TO_AUD,
    netAUD,
    taxUSD: totalTax / USD_TO_AUD
  };
}

function computeResidency(revenueUSD, realExpensesUSD, homeJurisdiction) {
  const revenueEUR = revenueUSD * USD_TO_EUR;
  const realExpensesEUR = realExpensesUSD * USD_TO_EUR;
  const deProfit = Math.max(0, revenueEUR - realExpensesEUR);
  const deHealthCare = Math.min(deProfit, 69750) * 0.196;
  const deZve = Math.max(0, deProfit - deHealthCare);
  const deIncomeTax = germanIncomeTax(deZve);
  const deSoli = deIncomeTax > 20350 ? deIncomeTax * 0.055 : 0;
  const deNetEUR = deProfit - deHealthCare - deIncomeTax - deSoli;
  const ptTaxable = revenueEUR * 0.75;
  const ptIrs = bracketTax(ptTaxable, PT_BRACKETS);
  const ptSolidarity = portugalSolidarity(ptTaxable);
  const ptSocialSecurity = revenueEUR * 0.15;
  const ptNetEUR = revenueEUR - realExpensesEUR - ptIrs - ptSolidarity - ptSocialSecurity;
  // No `nyc` key here. It used to be computed by a generic computeYearState()
  // that knew nothing about the UBT, the MCTMT or the filing status - and the
  // caller overwrote it one line later with computeNYC(), so the figure was
  // never once rendered. The function and its call are gone rather than fixed;
  // a dead second opinion on New York is worse than none.
  return {
    berlin: {
      netUSD: deNetEUR * EUR_TO_USD,
      netEUR: deNetEUR,
      taxUSD: (deHealthCare + deIncomeTax + deSoli) * EUR_TO_USD,
      healthCareUSD: deHealthCare * EUR_TO_USD,
      incomeTaxUSD: deIncomeTax * EUR_TO_USD,
      soliUSD: deSoli * EUR_TO_USD
    },
    portugal: {
      netUSD: ptNetEUR * EUR_TO_USD,
      netEUR: ptNetEUR,
      taxUSD: (ptIrs + ptSolidarity + ptSocialSecurity) * EUR_TO_USD,
      irsUSD: ptIrs * EUR_TO_USD,
      solidarityUSD: ptSolidarity * EUR_TO_USD,
      ssUSD: ptSocialSecurity * EUR_TO_USD
    }
  };
}

return {computeNYC: computeNYC, computePittsburgh: computePittsburgh, computeFrance: computeFrance, computeUAE: computeUAE, computeBrisbane: computeBrisbane, computeResidency: computeResidency};
})();
