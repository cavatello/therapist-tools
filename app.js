const {
  useState,
  useMemo,
  useEffect
} = React;
const {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  Cell,
  ReferenceLine
} = Recharts;
const STORE_KEY = 'practice_planner_v3';
function encodeShareState(obj) {
  try {
    return btoa(encodeURIComponent(JSON.stringify(obj))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  } catch (e) {
    return null;
  }
}
function decodeShareState(str) {
  try {
    const b64 = str.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(decodeURIComponent(atob(b64)));
  } catch (e) {
    return null;
  }
}
function loadSaved() {
  try {
    const hash = window.location.hash || '';
    const m = hash.match(/[#&]s=([^&]+)/);
    if (m) {
      const shared = decodeShareState(m[1]);
      if (shared && typeof shared === 'object') return shared;
    }
  } catch (e) {}
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY)) || {};
  } catch (e) {
    return {};
  }
}
const SAVED = loadSaved();
const OPENED_FROM_SHARE_LINK = /[#&]s=/.test(window.location.hash || '');
// Older saved/shared setups predate the "intake" stage. Anyone who reached the
// 10th session must have completed an intake, so backfill it from converted.
function normalizeFunnel(f) {
  const base = { visits: 0, calls: 0, consults: 0, intake: 0, converted: 0 };
  const out = {};
  ["pt", "web", "ref"].forEach(k => {
    const d = (f && f[k]) || {};
    out[k] = Object.assign({}, base, d);
    if (d.intake === undefined) out[k].intake = Math.max(0, +d.converted || 0);
  });
  return out;
}
const VARIANT = (() => { try { const v = new URLSearchParams(window.location.search).get('v');
  return ['01','02','03','04'].indexOf(v) > -1 ? v : ''; } catch (e) { return ''; } })();
const PAGE_RE = /(^|[#&])grow(&|$)/;
const pageFromHash = () => PAGE_RE.test(window.location.hash || '') ? 'grow' : 'sim';
const INITIAL_PAGE = pageFromHash();

// ----------------------------------------------------------------------------
// 2026 CA SINGLE-FILER TAX ENGINE
// Practice income modeled as 1099 / self-employed (Schedule C): business expenses
// are deductible pre-tax, self-employment tax applies, QBI deduction included.
// Secondary income source modeled as additional 1099 self-employment income, combined with practice revenue.
// ----------------------------------------------------------------------------
const SESSIONS = Array.from({
  length: 16
}, (_, i) => 15 + i);
const FED_STD = 15750,
  CA_STD = 5540;
const FED_STD_BY_STATUS = {
  single: 15750,
  mfj: 31500,
  mfj_dependents: 31500,
  hoh: 23625
};
const CA_STD_BY_STATUS = {
  single: 5540,
  mfj: 11080,
  mfj_dependents: 11080,
  hoh: 11080
};
const FED_BRACKETS_BY_STATUS = {
  single: [[0, 0.10], [12400, 0.12], [50400, 0.22], [105700, 0.24], [201775, 0.32], [256225, 0.35], [640600, 0.37]],
  mfj: [[0, 0.10], [25700, 0.12], [104600, 0.22], [223000, 0.24], [425800, 0.32], [540600, 0.35], [811200, 0.37]],
  mfj_dependents: [[0, 0.10], [25700, 0.12], [104600, 0.22], [223000, 0.24], [425800, 0.32], [540600, 0.35], [811200, 0.37]],
  hoh: [[0, 0.10], [18450, 0.12], [70450, 0.22], [112050, 0.24], [214300, 0.32], [271650, 0.35], [678100, 0.37]]
};
const CA_BRACKETS_BY_STATUS = {
  single: [[0, 0.01], [11080, 0.02], [26268, 0.04], [41468, 0.06], [57568, 0.08], [72716, 0.093], [371510, 0.103], [445830, 0.113], [743100, 0.123]],
  mfj: [[0, 0.01], [22160, 0.02], [52536, 0.04], [82936, 0.06], [115136, 0.08], [145432, 0.093], [743020, 0.103], [891660, 0.113], [1486200, 0.123]],
  mfj_dependents: [[0, 0.01], [22160, 0.02], [52536, 0.04], [82936, 0.06], [115136, 0.08], [145432, 0.093], [743020, 0.103], [891660, 0.113], [1486200, 0.123]],
  hoh: [[0, 0.01], [22160, 0.02], [52536, 0.04], [82936, 0.06], [115136, 0.08], [145432, 0.093], [743020, 0.103], [891660, 0.113], [1486200, 0.123]]
};
const QBI_PHASE_BY_STATUS = {
  single: [197300, 247300],
  hoh: [197300, 247300],
  mfj: [394600, 494600],
  mfj_dependents: [394600, 494600]
};
const CTC_PER_CHILD = 2000;
const SS_WAGE_BASE = 184500;
const SS_BEND1 = 1286,
  SS_BEND2 = 7749;
function computePIA(monthlyAIME) {
  let pia = 0;
  if (monthlyAIME <= SS_BEND1) {
    pia = monthlyAIME * 0.90;
  } else if (monthlyAIME <= SS_BEND2) {
    pia = SS_BEND1 * 0.90 + (monthlyAIME - SS_BEND1) * 0.32;
  } else {
    pia = SS_BEND1 * 0.90 + (SS_BEND2 - SS_BEND1) * 0.32 + (monthlyAIME - SS_BEND2) * 0.15;
  }
  return pia;
}
const RETIRE_2026 = {
  ira: {
    under50: 7500,
    over50: 8600
  },
  solo401k: {
    employeeUnder50: 24000,
    employee50to59: 31500,
    employee60to63: 34500,
    employee64plus: 31500,
    overallCapUnder50: 71000,
    overallCap50plus: 78500,
    overallCap60to63: 81750,
    employerPct: 0.20
  },
  traditionalIraPhaseOut: {
    single: [81000, 91000],
    hoh: [81000, 91000],
    mfj: [129000, 149000],
    mfj_dependents: [129000, 149000]
  },
  rothIraPhaseOut: {
    single: [153000, 168000],
    hoh: [153000, 168000],
    mfj: [241000, 251000],
    mfj_dependents: [241000, 251000]
  }
};
const ADDL_MED_THRESH = 200000,
  ADDL_MED_RATE = 0.009;
const QBI_RATE = 0.20,
  QBI_PHASE_START = 197300,
  QBI_PHASE_END = 247300;
const FED_BRACKETS = [[0, 0.10], [12400, 0.12], [50400, 0.22], [105700, 0.24], [201775, 0.32], [256225, 0.35], [640600, 0.37]];
const CA_BRACKETS = [[0, 0.01], [11080, 0.02], [26268, 0.04], [41468, 0.06], [57568, 0.08], [72716, 0.093], [371510, 0.103], [445830, 0.113], [743100, 0.123]];
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

// Full-year computation. practiceGross = 1099 therapy revenue, expenses = Schedule C
// deductions (INCLUDING any city business-license fee), w2Wages = second-job W-2 income.
function citeList(items) {
  return /*#__PURE__*/React.createElement("div", {
    className: "cite-refs"
  }, items.map((it, i) => /*#__PURE__*/React.createElement("div", {
    className: "cite-ref",
    key: i
  }, /*#__PURE__*/React.createElement("span", {
    className: "cite-num"
  }, "[", it.n, "]"), it.url ? /*#__PURE__*/React.createElement("a", {
    href: it.url,
    target: "_blank",
    rel: "noopener noreferrer"
  }, it.cite) : /*#__PURE__*/React.createElement("b", null, it.cite), it.note ? " \u2014 " + it.note : "")));
}

// ---------- S-corp salary risk guidance ----------
// Bands are practitioner rules of thumb, NOT statute. There is no safe-harbour
// percentage in the Code -- the test is what the work is actually worth.
const SALARY_BANDS = [
  {min: 1.00, key: "none",  label: "No exposure",   color: "#3F9577",
   what: "Every dollar of profit is salary, so there is no distribution left to recharacterise.",
   cost: "You also give up the entire reason to elect S-corp treatment."},
  {min: 0.60, key: "low",   label: "Conservative",  color: "#3F9577",
   what: "Well above the figure most practitioners treat as defensible.",
   cost: "Leaves some saving on the table, buys a quiet life."},
  {min: 0.50, key: "bench", label: "Benchmark",     color: "#3F9577",
   what: "At or above the 50%-of-profit rule of thumb most CPAs start from.",
   cost: "Commonly cited, but it is a convention -- not a rule you can point at in an audit."},
  {min: 0.35, key: "aggr",  label: "Aggressive",    color: "#C98B4B",
   what: "Defensible for some practices, but you would need to show your working.",
   cost: "Keep evidence: comparable LMFT salaries, your hours, your duties."},
  {min: 0.001, key: "high", label: "High risk",     color: "#B5483F",
   what: "This is the pattern the IRS looks for -- small salary, large distributions.",
   cost: "If recharacterised you owe the back payroll tax, plus penalties and interest."},
  {min: 0,     key: "zero", label: "Not an option", color: "#B5483F",
   what: "A corporate officer who performs services is a statutory employee and must be paid wages.",
   cost: "There is no version of this that survives scrutiny."}
];
function salaryBandFor(salary, netProfit) {
  if (!(netProfit > 0)) return null;
  const r = salary / netProfit;
  for (let i = 0; i < SALARY_BANDS.length; i++) {
    if (r >= SALARY_BANDS[i].min) return Object.assign({}, SALARY_BANDS[i], {ratio: r});
  }
  return Object.assign({}, SALARY_BANDS[SALARY_BANDS.length - 1], {ratio: r});
}
function extLink(href, text) {
  return /*#__PURE__*/React.createElement("a", {
    href: href, target: "_blank", rel: "noopener noreferrer", className: "extlink"
  }, text);
}


// ---------- "What I keep" opener + payroll mechanics ----------
const SS_WAGE_BASE_2026 = 184500;   // ssa.gov/oact/cola/cbb.html
const OASDI_RATE = 0.124;           // 6.2% employee + 6.2% employer
const MEDICARE_RATE = 0.029;        // 1.45% + 1.45%
const SE_FACTOR = 0.9235;

function payrollSplit(profit, salary) {
  const seBase = Math.max(0, profit) * SE_FACTOR;
  const soleSS = OASDI_RATE * Math.min(seBase, SS_WAGE_BASE_2026);
  const soleMed = MEDICARE_RATE * seBase;
  const sal = Math.max(0, salary);
  const corpSS = OASDI_RATE * Math.min(sal, SS_WAGE_BASE_2026);
  const corpMed = MEDICARE_RATE * sal;
  return {
    seBase: seBase, soleSS: soleSS, soleMed: soleMed, soleTotal: soleSS + soleMed,
    corpSS: corpSS, corpMed: corpMed, corpTotal: corpSS + corpMed,
    savedSS: soleSS - corpSS, savedMed: soleMed - corpMed,
    saved: (soleSS + soleMed) - (corpSS + corpMed),
    distribution: Math.max(0, profit - sal), aboveCap: sal >= SS_WAGE_BASE_2026
  };
}

function keepBar(grossYr, expYr, taxYr, netYr, rate) {
  if (!(grossYr > 0)) return null;
  const pct = n => Math.max(0, (n / grossYr) * 100);
  const keepPct = Math.round((netYr / grossYr) * 100);
  const unit = (h, v, s2) => /*#__PURE__*/React.createElement("div", {className: "keep-unit", key: h},
    /*#__PURE__*/React.createElement("h4", null, h),
    /*#__PURE__*/React.createElement("div", {className: "keep-unit-v"}, v),
    /*#__PURE__*/React.createElement("span", null, s2));
  return /*#__PURE__*/React.createElement("div", {className: "keepwrap"},
    /*#__PURE__*/React.createElement("div", {className: "keephero"},
      /*#__PURE__*/React.createElement("div", {className: "keep-eyebrow"}, "Of the " + fmt(grossYr) + " you bill this year"),
      /*#__PURE__*/React.createElement("div", {className: "keep-big"}, fmt(netYr)),
      /*#__PURE__*/React.createElement("div", {className: "keep-sub"}, "is actually yours — ",
        /*#__PURE__*/React.createElement("b", null, keepPct + "¢ of every dollar you charge"))),
    /*#__PURE__*/React.createElement("div", {className: "keep-bar"},
      /*#__PURE__*/React.createElement("i", {className: "kb-exp", style: {width: pct(expYr) + "%"}}),
      /*#__PURE__*/React.createElement("i", {className: "kb-tax", style: {width: pct(taxYr) + "%"}}, pct(taxYr) > 12 ? "TAX " + Math.round(pct(taxYr)) + "%" : ""),
      /*#__PURE__*/React.createElement("i", {className: "kb-net", style: {width: pct(netYr) + "%"}}, pct(netYr) > 18 ? "YOU KEEP " + keepPct + "%" : "")),
    /*#__PURE__*/React.createElement("div", {className: "keep-legend"},
      /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {className: "kdot kb-exp"}), "Running costs ", fmt(expYr)),
      /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {className: "kdot kb-tax"}), "Federal + CA + self-employment tax ", fmt(taxYr)),
      /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {className: "kdot kb-net"}), "Yours ", fmt(netYr))),
    /*#__PURE__*/React.createElement("div", {className: "keep-chain"},
      /*#__PURE__*/React.createElement("b", null, fmt(grossYr)), " billed − ",
      /*#__PURE__*/React.createElement("b", null, fmt(expYr)), " costs = ",
      /*#__PURE__*/React.createElement("b", null, fmt(grossYr - expYr)), " profit − ",
      /*#__PURE__*/React.createElement("b", null, fmt(taxYr)), " tax = ",
      /*#__PURE__*/React.createElement("b", {className: "pos"}, fmt(netYr)), " yours"),
    /*#__PURE__*/React.createElement("div", {className: "keep-units"},
      rate > 0 ? unit("Per session", fmt(rate * (netYr / grossYr)), "of your " + fmt(rate) + " fee") : null,
      unit("Per month", fmt(netYr / 12), "after tax"),
      unit("Per week", fmt(netYr / 52), "take-home"),
      unit("Effective tax rate", Math.round((taxYr / Math.max(1, grossYr - expYr)) * 100) + "%", "of profit, all taxes")));
}

function computeYear(practiceGross, expenses, w2Wages, filingStatus, numDependents, employerRetirement, employeeRetirement, entityType, sCorpSalary) {
  filingStatus = filingStatus || "single";
  numDependents = numDependents || 0;
  employerRetirement = employerRetirement || 0;
  employeeRetirement = employeeRetirement || 0;
  entityType = entityType || "sole_prop";
  sCorpSalary = entityType === "s_corp" ? sCorpSalary || 0 : 0;
  const fedStd = FED_STD_BY_STATUS[filingStatus];
  const caStd = CA_STD_BY_STATUS[filingStatus];
  const fedBrackets = FED_BRACKETS_BY_STATUS[filingStatus];
  const caBrackets = CA_BRACKETS_BY_STATUS[filingStatus];
  const [qbiStart, qbiEnd] = QBI_PHASE_BY_STATUS[filingStatus];
  const profitBeforeSalary = Math.max(0, practiceGross - expenses - employerRetirement);
  const salary = Math.min(sCorpSalary, profitBeforeSalary);
  const employerPayrollTax = entityType === "s_corp" ? Math.min(salary, SS_WAGE_BASE) * 0.062 + salary * 0.0145 : 0;
  const kDistribution = entityType === "s_corp" ? Math.max(0, profitBeforeSalary - salary - employerPayrollTax) : 0;
  const caEntityTax = entityType === "s_corp" ? Math.max(800, kDistribution * 0.015) : 0;
  const schedC = entityType === "s_corp" ? 0 : profitBeforeSalary;
  const seBase = schedC * 0.9235;
  const ssRoom = Math.max(0, SS_WAGE_BASE - w2Wages);
  const seTax = Math.min(seBase, ssRoom) * 0.124 + seBase * 0.029;
  const halfSE = seTax / 2;
  const totalW2 = w2Wages + salary;
  const ssW2 = Math.min(totalW2, SS_WAGE_BASE) * 0.062;
  const medW2 = totalW2 * 0.0145;
  const sdi = totalW2 * 0.012;
  const addlMed = Math.max(0, totalW2 + seBase - ADDL_MED_THRESH) * ADDL_MED_RATE;
  const agi = Math.max(0, schedC + kDistribution + totalW2 - halfSE - employeeRetirement);
  const taxableBeforeQBI = Math.max(0, agi - fedStd);
  const qbiIncome = entityType === "s_corp" ? Math.max(0, kDistribution) : Math.max(0, schedC - halfSE);
  let pct;
  if (taxableBeforeQBI <= qbiStart) pct = 1;else if (taxableBeforeQBI >= qbiEnd) pct = 0;else pct = 1 - (taxableBeforeQBI - qbiStart) / (qbiEnd - qbiStart);
  const qbiDed = Math.min(QBI_RATE * qbiIncome, QBI_RATE * taxableBeforeQBI) * pct;
  const fedTaxBeforeCredits = bracketTax(Math.max(0, taxableBeforeQBI - qbiDed), fedBrackets);
  const ctc = filingStatus === "mfj_dependents" ? Math.min(numDependents * CTC_PER_CHILD, fedTaxBeforeCredits) : 0;
  const fedTax = Math.max(0, fedTaxBeforeCredits - ctc);
  const caTax = bracketTax(Math.max(0, agi - caStd), caBrackets);
  const totalTax = fedTax + caTax + seTax + ssW2 + medW2 + sdi + addlMed + employerPayrollTax + caEntityTax;
  const grossAll = practiceGross + w2Wages;
  return {
    practiceGross,
    expenses,
    w2Wages,
    schedC,
    kDistribution,
    salary,
    employerPayrollTax,
    caEntityTax,
    grossAll,
    seTax,
    ssW2,
    medW2,
    sdi,
    addlMed,
    qbiDed,
    fedTax,
    ctc,
    caTax,
    payrollW2: ssW2 + medW2 + sdi,
    totalTax,
    employerRetirement,
    employeeRetirement,
    net: grossAll - expenses - totalTax - employerRetirement - employeeRetirement
  };
}

const NY_STD = 8000;
const NY_BRACKETS = [[0, 0.039], [8500, 0.044], [11700, 0.0515], [13900, 0.054], [80650, 0.059], [215400, 0.0685], [1077550, 0.0965], [5000000, 0.103], [25000000, 0.109]];
const NYC_BRACKETS = [[0, 0.03078], [12000, 0.03762], [25000, 0.03819], [50000, 0.03876]];
// Generic version of computeYear parameterized by state (+ optional city) tax
// layer, used only for the residency "home" picker (California vs. New York
// City). Federal SE tax, FICA, and QBI logic are identical to computeYear.
function computeYearState(practiceGross, expenses, w2Wages, stateStd, stateBrackets, cityBrackets) {
  const schedC = Math.max(0, practiceGross - expenses);
  const seBase = schedC * 0.9235;
  const ssRoom = Math.max(0, SS_WAGE_BASE - w2Wages);
  const seTax = Math.min(seBase, ssRoom) * 0.124 + seBase * 0.029;
  const halfSE = seTax / 2;
  const ssW2 = Math.min(w2Wages, SS_WAGE_BASE) * 0.062;
  const medW2 = w2Wages * 0.0145;
  const addlMed = Math.max(0, w2Wages + seBase - ADDL_MED_THRESH) * ADDL_MED_RATE;
  const agi = schedC + w2Wages - halfSE;
  const taxableBeforeQBI = Math.max(0, agi - FED_STD);
  const qbiIncome = Math.max(0, schedC - halfSE);
  let pct;
  if (taxableBeforeQBI <= QBI_PHASE_START) pct = 1;else if (taxableBeforeQBI >= QBI_PHASE_END) pct = 0;else pct = 1 - (taxableBeforeQBI - QBI_PHASE_START) / (QBI_PHASE_END - QBI_PHASE_START);
  const qbiDed = Math.min(QBI_RATE * qbiIncome, QBI_RATE * taxableBeforeQBI) * pct;
  const fedTax = bracketTax(Math.max(0, taxableBeforeQBI - qbiDed), FED_BRACKETS);
  const stateTaxableIncome = Math.max(0, agi - stateStd);
  const stateTax = bracketTax(stateTaxableIncome, stateBrackets);
  const cityTax = cityBrackets ? bracketTax(stateTaxableIncome, cityBrackets) : 0;
  const totalTax = fedTax + stateTax + cityTax + seTax + ssW2 + medW2 + addlMed;
  const grossAll = practiceGross + w2Wages;
  return {
    net: grossAll - expenses - totalTax,
    totalTax,
    fedTax,
    stateTax,
    cityTax,
    seTax
  };
}

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
const MCTMT_THRESHOLD = 50000,
  MCTMT_RATE = 0.0034;
function computeNYC(revenueUSD, expensesUSD) {
  const schedC = Math.max(0, revenueUSD - expensesUSD);
  const seBase = schedC * 0.9235;
  const seTax = Math.min(seBase, SS_WAGE_BASE) * 0.124 + seBase * 0.029;
  const halfSE = seTax / 2;
  const agi = schedC - halfSE;
  const taxableBeforeQBI = Math.max(0, agi - FED_STD);
  const qbiIncome = Math.max(0, schedC - halfSE);
  let pct;
  if (taxableBeforeQBI <= QBI_PHASE_START) pct = 1;else if (taxableBeforeQBI >= QBI_PHASE_END) pct = 0;else pct = 1 - (taxableBeforeQBI - QBI_PHASE_START) / (QBI_PHASE_END - QBI_PHASE_START);
  const qbiDed = Math.min(QBI_RATE * qbiIncome, QBI_RATE * taxableBeforeQBI) * pct;
  const fedTax = bracketTax(Math.max(0, taxableBeforeQBI - qbiDed), FED_BRACKETS);
  const nyTaxable = Math.max(0, agi - NY_STD);
  const nyTax = bracketTax(nyTaxable, NY_BRACKETS);
  const nycTax = bracketTax(nyTaxable, NYC_BRACKETS);
  const mctmt = schedC > MCTMT_THRESHOLD ? schedC * MCTMT_RATE : 0;
  const totalTax = fedTax + seTax + nyTax + nycTax + mctmt;
  return {
    netUSD: schedC - totalTax,
    taxUSD: totalTax,
    fedTaxUSD: fedTax,
    seTaxUSD: seTax,
    nyTaxUSD: nyTax,
    nycTaxUSD: nycTax,
    mctmtUSD: mctmt
  };
}
const PA_FLAT_RATE = 0.0307;
const PITTSBURGH_EIT_RATE = 0.03;
const PITTSBURGH_LST = 52;
function computePittsburgh(revenueUSD, expensesUSD) {
  const schedC = Math.max(0, revenueUSD - expensesUSD);
  const seBase = schedC * 0.9235;
  const seTax = Math.min(seBase, SS_WAGE_BASE) * 0.124 + seBase * 0.029;
  const halfSE = seTax / 2;
  const agi = schedC - halfSE;
  const taxableBeforeQBI = Math.max(0, agi - FED_STD);
  const qbiIncome = Math.max(0, schedC - halfSE);
  let pct;
  if (taxableBeforeQBI <= QBI_PHASE_START) pct = 1;else if (taxableBeforeQBI >= QBI_PHASE_END) pct = 0;else pct = 1 - (taxableBeforeQBI - QBI_PHASE_START) / (QBI_PHASE_END - QBI_PHASE_START);
  const qbiDed = Math.min(QBI_RATE * qbiIncome, QBI_RATE * taxableBeforeQBI) * pct;
  const fedTax = bracketTax(Math.max(0, taxableBeforeQBI - qbiDed), FED_BRACKETS);
  const paTax = schedC * PA_FLAT_RATE;
  const eitTax = schedC * PITTSBURGH_EIT_RATE;
  const lst = PITTSBURGH_LST;
  const totalTax = fedTax + seTax + paTax + eitTax + lst;
  return {
    netUSD: schedC - totalTax,
    taxUSD: totalTax,
    fedTaxUSD: fedTax,
    seTaxUSD: seTax,
    paTaxUSD: paTax,
    eitTaxUSD: eitTax,
    lstUSD: lst
  };
}
const FR_BRACKETS = [[0, 0], [11600, 0.11], [29579, 0.30], [84577, 0.41], [181917, 0.45]];
const FR_COTISATION_RATE = 0.40;
function computeFrance(revenueUSD, expensesUSD) {
  const revenueEUR = revenueUSD * USD_TO_EUR;
  const expensesEUR = expensesUSD * USD_TO_EUR;
  const profitEUR = Math.max(0, revenueEUR - expensesEUR);
  const cotisationsEUR = profitEUR * FR_COTISATION_RATE;
  const taxableEUR = Math.max(0, profitEUR - cotisationsEUR);
  const incomeTaxEUR = bracketTax(taxableEUR, FR_BRACKETS);
  const netEUR = profitEUR - cotisationsEUR - incomeTaxEUR;
  return {
    netUSD: netEUR * EUR_TO_USD,
    netEUR,
    taxUSD: (cotisationsEUR + incomeTaxEUR) * EUR_TO_USD,
    cotisationsUSD: cotisationsEUR * EUR_TO_USD,
    incomeTaxUSD: incomeTaxEUR * EUR_TO_USD
  };
}
const USD_TO_AED = 3.6725;
function computeUAE(revenueUSD, expensesUSD) {
  const revenueAED = revenueUSD * USD_TO_AED;
  const expensesAED = expensesUSD * USD_TO_AED;
  const profitAED = Math.max(0, revenueAED - expensesAED);
  const corpTax = revenueAED > 1000000 ? Math.max(0, profitAED - 375000) * 0.09 : 0;
  const netAED = profitAED - corpTax;
  return {
    netUSD: netAED / USD_TO_AED,
    netAED,
    taxUSD: corpTax / USD_TO_AED
  };
}
const AU_BRACKETS = [[0, 0], [18200, 0.16], [45000, 0.30], [135000, 0.37], [190000, 0.45]];
const USD_TO_AUD = 1.43;
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
const PT_BRACKETS = [[0, 0.1325], [7703, 0.165], [11623, 0.22], [16472, 0.25], [21321, 0.32], [27146, 0.355], [39791, 0.435], [51997, 0.45], [81199, 0.48]];
function portugalSolidarity(taxable) {
  let s = 0;
  if (taxable > 250000) s += (taxable - 250000) * 0.05;
  if (taxable > 80000) s += (Math.min(taxable, 250000) - 80000) * 0.025;
  return s;
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
  const nyc = computeYearState(revenueUSD, realExpensesUSD, 0, NY_STD, NY_BRACKETS, NYC_BRACKETS);
  return {
    nyc: {
      netUSD: nyc.net,
      taxUSD: nyc.totalTax
    },
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

// ----------------------------------------------------------------------------
// CITY BUSINESS-LICENSE TAX
// California has no city/county INCOME tax — state tax is identical everywhere in
// CA. What *does* vary by city is a local business license tax, usually tiered on
// annual gross receipts. Menlo Park's schedule below is the actual published rate
// table (Menlo Park Municipal Code Ch. 5.12.020). Other Bay Area cities are
// commonly-cited ballpark structures for comparison — always confirm current
// rates with the city, since these schedules change.
// ----------------------------------------------------------------------------
const CITY_LICENSE = {
  none: {
    label: "\u2014 Select a city \u2014",
    kind: "flat_estimate",
    flatAnnual: 0,
    source: "No city selected yet \u2014 $0 assumed"
  },
  menlo_park: {
    label: "Menlo Park",
    kind: "table",
    brackets: [[0, 25000, 50], [25000, 50000, 75], [50000, 75000, 100], [75000, 100000, 125], [100000, 200000, 160], [200000, 300000, 200], [300000, 400000, 240], [400000, 500000, 275], [500000, 600000, 310], [600000, 700000, 350], [700000, 800000, 390], [800000, 900000, 425], [900000, 1000000, 460], [1000000, 2000000, 750]],
    over2m: g => 750 + 250 * Math.ceil((g - 2000000) / 1000000),
    source: "Menlo Park Municipal Code \u00A7 5.12.020"
  },
  palo_alto: {
    label: "Palo Alto",
    kind: "flat_estimate",
    flatAnnual: 155,
    source: "flat per-employee business registration, approximate"
  },
  redwood_city: {
    label: "Redwood City",
    kind: "flat_estimate",
    flatAnnual: 100,
    source: "flat business license fee, approximate"
  },
  san_mateo: {
    label: "San Mateo",
    kind: "flat_estimate",
    flatAnnual: 195,
    source: "flat business license fee, approximate"
  },
  san_francisco: {
    label: "San Francisco",
    kind: "gross_receipts_pct",
    pct: 0.001,
    source: "SF gross receipts tax, small-business rate varies by category"
  },
  other: {
    label: "Other / not sure",
    kind: "manual",
    source: ""
  }
};
function cityLicenseFee(cityKey, grossReceipts, manualOverride) {
  return 0;
}
function cityLicenseFee_UNUSED(cityKey, grossReceipts, manualOverride) {
  return 0;
}
function cityLicenseFeeDISABLED(cityKey, grossReceipts, manualOverride) {
  const c = CITY_LICENSE[cityKey];
  if (!c) return 0;
  if (c.kind === "manual") return manualOverride || 0;
  if (c.kind === "flat_estimate") return c.flatAnnual;
  if (c.kind === "gross_receipts_pct") return Math.round(grossReceipts * c.pct);
  if (c.kind === "table") {
    if (grossReceipts > 2000000) return c.over2m(grossReceipts);
    for (const [lo, hi, fee] of c.brackets) {
      if (grossReceipts > lo && grossReceipts <= hi) return fee;
    }
    return c.brackets[0][2];
  }
  return 0;
}

// ----------------------------------------------------------------------------
function lerpHex(hexA, hexB, t) {
  const a = [1, 3, 5].map(i => parseInt(hexA.slice(i, i + 2), 16));
  const b = [1, 3, 5].map(i => parseInt(hexB.slice(i, i + 2), 16));
  const c = a.map((v, i) => Math.round(v + (b[i] - v) * t));
  return "#" + c.map(v => v.toString(16).padStart(2, "0")).join("");
}
const RATE_STOPS = [[50, "#6B8F9C"], [90, "#5C9CA8"], [130, "#4A9A86"], [170, "#3F9577"], [210, "#C98B4B"], [250, "#C26B4A"], [300, "#B5483F"]];
function colorForRate(r) {
  const v = Math.max(50, Math.min(300, r));
  for (let i = 0; i < RATE_STOPS.length - 1; i++) {
    const [r0, c0] = RATE_STOPS[i],
      [r1, c1] = RATE_STOPS[i + 1];
    if (v >= r0 && v <= r1) return lerpHex(c0, c1, (v - r0) / (r1 - r0));
  }
  return RATE_STOPS[RATE_STOPS.length - 1][1];
}
const RATES = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300];

// Typical private-practice expense categories (monthly defaults, editable)
const DEFAULT_EXPENSES = [{
  id: 'rent',
  label: 'Office rent',
  monthly: 0,
  note: 'suite or shared space'
}, {
  id: 'liability',
  label: 'Malpractice / liability ins.',
  monthly: 0,
  note: '$400/yr'
}, {
  id: 'health',
  label: 'Health insurance',
  monthly: 0,
  note: 'self-employed premium'
}, {
  id: 'ehr',
  label: 'EHR / practice software',
  monthly: 0,
  note: 'SimplePractice, TherapyNotes'
}, {
  id: 'billing',
  label: 'Billing / merchant fees',
  monthly: 0,
  pct: 0.025,
  note: '2.5% of gross \u2014 card processing surcharge'
}, {
  id: 'super',
  label: 'Supervision / consultation',
  monthly: 0,
  note: 'peer or clinical consult'
}, {
  id: 'marketing',
  label: 'Marketing & directories',
  monthly: 0,
  note: 'Psychology Today, website'
}, {
  id: 'phone',
  label: 'Phone, internet, tech',
  monthly: 0,
  note: 'business lines, hardware'
}, {
  id: 'legal',
  label: 'Accounting & legal',
  monthly: 0,
  note: 'CPA, bookkeeping'
}, {
  id: 'license',
  label: 'Licensure & dues',
  monthly: 0,
  note: 'BBS renewal, CAMFT/APA'
}, {
  id: 'ce',
  label: 'Continuing education',
  monthly: 0,
  note: 'CEUs, trainings'
}, {
  id: 'office',
  label: 'Office supplies & misc.',
  monthly: 0,
  note: 'materials, furnishings'
}];
const RATE_DATA = Object.fromEntries(RATES.map(r => [r, {
  color: colorForRate(r)
}]));

// Therapy-only gross helpers
const grossWk = (rate, s) => rate * s;
const grossYr = (rate, s) => rate * s * 52;
const grossMo = (rate, s) => Math.round(rate * s * 52 / 12);
const fmt = n => (n < 0 ? "\u2212$" : "$") + Math.abs(Math.round(n)).toLocaleString();
const fmtK = n => "$" + Math.round(n / 1000) + "k";

// ----------------------------------------------------------------------------
function LandingPage({
  onSelect
}) {
  const doors = [{
    key: "current",
    label: "Current Design",
    tag: "Familiar",
    desc: "Six tabs across the top, jump to any section directly.",
    icon: "\u2637",
    tile: "tile-current"
  }, {
    key: "guided",
    label: "Guided Scroll",
    tag: "See it all at once",
    desc: "One continuous page, in order \u2014 bill, spend, keep, optimize, compare, grow.",
    icon: "\u2193",
    tile: "tile-guided"
  }, {
    key: "wizard",
    label: "Step by Step",
    tag: "One thing at a time",
    desc: "A guided walkthrough, one question per screen, ending in your full picture.",
    icon: "\u2192",
    tile: "tile-wizard"
  }];
  const character = /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 160 180",
    className: "doc-avatar"
  }, /*#__PURE__*/React.createElement("ellipse", {
    cx: "80",
    cy: "168",
    rx: "58",
    ry: "10",
    fill: "rgba(0,0,0,.25)"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M28 176 Q28 118 80 118 Q132 118 132 176 Z",
    fill: "#3B4A6B"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M50 122 L80 150 L110 122 L98 116 L80 132 L62 116 Z",
    fill: "#F4F1EA"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M62 116 L50 122 L58 138 L66 128 Z",
    fill: "#2C3856"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M98 116 L110 122 L102 138 L94 128 Z",
    fill: "#2C3856"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "80",
    cy: "134",
    r: "7",
    fill: "#C9622A"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M38 68 Q38 20 80 20 Q122 20 122 68 L122 92 Q122 116 80 116 Q38 116 38 92 Z",
    fill: "#E8B98A"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M38 60 Q34 60 34 72 Q34 84 40 84 L42 68 Z",
    fill: "#E8B98A"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M122 60 Q126 60 126 72 Q126 84 120 84 L118 68 Z",
    fill: "#E8B98A"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M36 62 Q30 30 80 24 Q130 30 124 62 Q120 40 80 38 Q40 40 36 62 Z",
    fill: "#D9D4C9"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M40 96 Q38 118 40 132 Q52 146 80 148 Q108 146 120 132 Q122 118 120 96 Q116 122 80 124 Q44 122 40 96 Z",
    fill: "#EDEAE2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M62 92 Q80 100 98 92 Q98 100 80 106 Q62 100 62 92 Z",
    fill: "#B5483F"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "62",
    cy: "66",
    r: "15",
    fill: "none",
    stroke: "#26241E",
    strokeWidth: "3.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "98",
    cy: "66",
    r: "15",
    fill: "none",
    stroke: "#26241E",
    strokeWidth: "3.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "77",
    y1: "66",
    x2: "83",
    y2: "66",
    stroke: "#26241E",
    strokeWidth: "3.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "47",
    y1: "60",
    x2: "38",
    y2: "56",
    stroke: "#26241E",
    strokeWidth: "3"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "113",
    y1: "60",
    x2: "122",
    y2: "56",
    stroke: "#26241E",
    strokeWidth: "3"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M52 58 Q62 52 72 58",
    fill: "none",
    stroke: "#8A8577",
    strokeWidth: "2.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M88 58 Q98 52 108 58",
    fill: "none",
    stroke: "#8A8577",
    strokeWidth: "2.5",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M66 86 Q80 92 94 86 Q86 82 80 84 Q74 82 66 86Z",
    fill: "#EDEAE2"
  }));
  return /*#__PURE__*/React.createElement("div", {
    className: "landing landing-game"
  }, /*#__PURE__*/React.createElement("style", null, CSS), /*#__PURE__*/React.createElement("div", {
    className: "game-sky"
  }, /*#__PURE__*/React.createElement("div", {
    className: "game-stars"
  })), /*#__PURE__*/React.createElement("div", {
    className: "landing-wrap game-wrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "game-hud"
  }, /*#__PURE__*/React.createElement("span", {
    className: "game-pixel"
  }, "\uD83E\uDDE0 PRACTICE QUEST"), /*#__PURE__*/React.createElement("span", {
    className: "game-hud-chip"
  }, "\uD83D\uDCB0 2026 EDITION")), /*#__PURE__*/React.createElement("div", {
    className: "doc-scene"
  }, character, /*#__PURE__*/React.createElement("div", {
    className: "speech-bubble"
  }, /*#__PURE__*/React.createElement("p", null, "\u201CTell me\u2014how would you like to explore your practice today?\u201D"), /*#__PURE__*/React.createElement("span", {
    className: "speech-sub"
  }, "Same real numbers, three different paths. Switch anytime."))), /*#__PURE__*/React.createElement("h1", {
    className: "landing-h1 game-title"
  }, "THERAPY PRACTICE SIMULATOR"), /*#__PURE__*/React.createElement("div", {
    className: "landing-doors game-doors"
  }, doors.map((d, i) => /*#__PURE__*/React.createElement("button", {
    key: d.key,
    className: "landing-door game-door " + d.tile,
    onClick: () => onSelect(d.key)
  }, /*#__PURE__*/React.createElement("div", {
    className: "game-door-level"
  }, "LEVEL ", i + 1), /*#__PURE__*/React.createElement("div", {
    className: "landing-door-icon"
  }, d.icon), /*#__PURE__*/React.createElement("div", {
    className: "landing-door-tag"
  }, d.tag), /*#__PURE__*/React.createElement("h3", null, d.label), /*#__PURE__*/React.createElement("p", null, d.desc), /*#__PURE__*/React.createElement("span", {
    className: "landing-door-cta game-door-cta"
  }, "PLAY \u25B6")))), /*#__PURE__*/React.createElement("p", {
    className: "landing-foot game-foot"
  }, "Estimates only \u2014 not tax advice. 2026 CA single-filer model.")));
}

function PracticeIncomePlanner() {
  const [tab, setTab] = useState(SAVED.tab || "income");
  const [rate, setRate] = useState(SAVED.rate != null ? SAVED.rate : 0);
  const [funnelRateOverride, setFunnelRateOverride] = useState(null);
  const funnelRateOverridden = funnelRateOverride !== null && funnelRateOverride !== "";
  const funnelRate = funnelRateOverridden ? funnelRateOverride : rate;
  const [sessions, setSessions] = useState(SAVED.sessions != null ? SAVED.sessions : 0);
  const [funnelSessionsOverride, setFunnelSessionsOverride] = useState(null);
  const funnelSessionsOverridden = funnelSessionsOverride !== null && funnelSessionsOverride !== "";
  const funnelSessions = funnelSessionsOverridden ? funnelSessionsOverride : sessions;
  const [goal, setGoal] = useState(SAVED.goal != null ? SAVED.goal : 120000);
  const [chartMode, setChartMode] = useState(SAVED.chartMode || "both");
  const [secondaryOn, setSecondaryOn] = useState(SAVED.secondaryOn != null ? SAVED.secondaryOn : false);
  const [usLocation, setUsLocation] = useState(SAVED.usLocation || "ca");
  const [rateDraft, setRateDraft] = useState(String(SAVED.rate != null ? SAVED.rate : 150));
  const [sessionsDraft, setSessionsDraft] = useState(String(SAVED.sessions != null ? SAVED.sessions : 22));
  const [avgTenure, setAvgTenure] = useState(SAVED.avgTenure != null ? SAVED.avgTenure : "");
  const [currentClients, setCurrentClients] = useState(SAVED.currentClients != null ? SAVED.currentClients : 0);
  const [sessionsPerClientWk, setSessionsPerClientWk] = useState(SAVED.sessionsPerClientWk != null ? SAVED.sessionsPerClientWk : 0);
  const [monthlyChurn, setMonthlyChurn] = useState(SAVED.monthlyChurn != null ? SAVED.monthlyChurn : 0);
  const [monthsToTarget, setMonthsToTarget] = useState(SAVED.monthsToTarget != null ? SAVED.monthsToTarget : 0);
  const [funnel, setFunnel] = useState(normalizeFunnel(SAVED.funnel));
  const [filingStatus, setFilingStatus] = useState(SAVED.filingStatus || "single");
  const [numDependents, setNumDependents] = useState(SAVED.numDependents != null ? SAVED.numDependents : 1);
  const [entityType, setEntityType] = useState(SAVED.entityType || "sole_prop");
  const [justPulsed, setJustPulsed] = useState(false);
  const [fbType, setFbType] = useState("Bug");
  const [fbName, setFbName] = useState("");
  const [fbMessage, setFbMessage] = useState("");
  const [fbSent, setFbSent] = useState(false);
  const [showSaveMenu, setShowSaveMenu] = useState(false);
  const [widgetCollapsed, setWidgetCollapsed] = useState(false);
  useEffect(() => {
    setJustPulsed(true);
    const t = setTimeout(() => setJustPulsed(false), 1200);
    return () => clearTimeout(t);
  }, [entityType, filingStatus]);
  const [sCorpSalaryInput, setSCorpSalaryInput] = useState(SAVED.sCorpSalaryInput != null ? SAVED.sCorpSalaryInput : 0);
  const [payrollSvcCost, setPayrollSvcCost] = useState(SAVED.payrollSvcCost != null ? SAVED.payrollSvcCost : 0);
  const [corpReturnCost, setCorpReturnCost] = useState(SAVED.corpReturnCost != null ? SAVED.corpReturnCost : 0);
  const [statementOfInfoCost, setStatementOfInfoCost] = useState(SAVED.statementOfInfoCost != null ? SAVED.statementOfInfoCost : 0);
  const [existingPretaxIRA, setExistingPretaxIRA] = useState(SAVED.existingPretaxIRA != null ? SAVED.existingPretaxIRA : 0);
  const [copyFeedback, setCopyFeedback] = useState("");
  const [viewMode, setViewMode] = useState("guided");
  const [page, setPage] = useState(INITIAL_PAGE);
  useEffect(() => {
    const onHash = () => {
      const next = pageFromHash();
      setPage(prev => {
        if (prev !== next) window.scrollTo(0, 0);
        return next;
      });
    };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);
  const [wizardStep, setWizardStep] = useState(SAVED.wizardStep || 1);
  const TAB_ORDER = ["income", "expenses", "profit", "taxstrategy", "residency", "funnel"];
  const WIZARD_ORDER = ["income", "income-addons", "expenses", "profit", "taxstrategy", "residency", "funnel"];
  const isVisible = key => VARIANT === "04" && !(rate > 0 || sessions > 0) && key !== "income" && key !== "funnel" ? false : key === "funnel" ? page === "grow" : page === "sim" && (viewMode === "guided" ? true : viewMode === "wizard" ? (key === "income" ? WIZARD_ORDER[wizardStep - 1] === "income" || WIZARD_ORDER[wizardStep - 1] === "income-addons" : WIZARD_ORDER[wizardStep - 1] === key) : tab === key);
  const SECTION_INTROS = {
    income: {
      n: 1,
      title: "Income",
      blurb: "What you bill before anything comes out. Set your rate and caseload here \u2014 every number further down is built from these two.",
      stat: () => fmt(cur.grossYr) + " gross a year"
    },
    expenses: {
      n: 2,
      title: "Expenses",
      blurb: "What it costs to keep the doors open. These are Schedule C deductions, so each dollar also lowers your taxable income \u2014 the real cost is less than the sticker price.",
      stat: () => fmt(cur.expYr) + " a year"
    },
    profit: {
      n: 3,
      title: "Profit",
      blurb: "What is actually left once expenses and every tax are taken out, and where each dollar of your gross ends up.",
      stat: () => fmt(cur.netYr) + " net a year"
    },
    taxstrategy: {
      n: 4,
      title: "Tax strategy",
      blurb: "The levers that change what you keep: filing status, business structure, and retirement accounts. Everything here is an estimate, not personalised advice.",
      stat: () => Math.round(cur.takeHomePct * 100) + "% take-home"
    }
  };
  const sectionIntro = key => {
    const d = SECTION_INTROS[key];
    if (!d) return null;
    return /*#__PURE__*/React.createElement("div", {
      className: "sec-intro"
    }, /*#__PURE__*/React.createElement("div", {
      className: "sec-intro-top"
    }, /*#__PURE__*/React.createElement("span", {
      className: "sec-intro-kicker"
    }, d.n + " of 4 \u00B7 Your finances"), /*#__PURE__*/React.createElement("span", {
      className: "sec-intro-stat"
    }, d.stat())), /*#__PURE__*/React.createElement("h2", {
      className: "sec-intro-title"
    }, d.title), /*#__PURE__*/React.createElement("p", {
      className: "sec-intro-blurb"
    }, d.blurb));
  };
  const showIncomePrimary = !(viewMode === "wizard") || WIZARD_ORDER[wizardStep - 1] === "income";
  const showIncomeAddons = !(viewMode === "wizard") || WIZARD_ORDER[wizardStep - 1] === "income-addons";
  const wizardSteps = viewMode === "wizard" ? WIZARD_ORDER : TAB_ORDER;
  const [shareFeedback, setShareFeedback] = useState("");
  const [showShareBanner, setShowShareBanner] = useState(OPENED_FROM_SHARE_LINK);
  const [activeSection, setActiveSection] = useState("sec-income");
  useEffect(() => {
    if (viewMode !== "guided") return;
    const ids = ["sec-income", "sec-expenses", "sec-profit", "sec-taxstrategy", "sec-residency", "sec-funnel"];
    const els = ids.map(id => document.getElementById(id)).filter(Boolean);
    if (!els.length) return;
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) setActiveSection(entry.target.id === "sec-residency" ? "sec-taxstrategy" : entry.target.id);
      });
    }, {
      rootMargin: "-15% 0px -70% 0px",
      threshold: 0
    });
    els.forEach(el => obs.observe(el));
    return () => obs.disconnect();
  }, [viewMode, tab]);
  const [taxAge, setTaxAge] = useState(SAVED.taxAge != null ? SAVED.taxAge : 0);
  const [retireAge, setRetireAge] = useState(SAVED.retireAge != null ? SAVED.retireAge : 0);
  const [investReturn, setInvestReturn] = useState(SAVED.investReturn != null ? SAVED.investReturn : 0);
  const [secondaryRate, setSecondaryRate] = useState(SAVED.secondaryRate != null ? SAVED.secondaryRate : "");
  const [secondarySessions, setSecondarySessions] = useState(SAVED.secondarySessions != null ? SAVED.secondarySessions : "");
  const [retreatOn, setRetreatOn] = useState(SAVED.retreatOn != null ? SAVED.retreatOn : false);
  const [retreatParticipants, setRetreatParticipants] = useState(SAVED.retreatParticipants != null ? SAVED.retreatParticipants : "");
  const [retreatRate, setRetreatRate] = useState(SAVED.retreatRate != null ? SAVED.retreatRate : "");
  const [retreatPerMonth, setRetreatPerMonth] = useState(SAVED.retreatPerMonth != null ? SAVED.retreatPerMonth : "");
  const [expenses, setExpenses] = useState(SAVED.expenses && SAVED.expenses.length ? SAVED.expenses : DEFAULT_EXPENSES.map(function (e) {
    return Object.assign({}, e);
  }));
  const [cityKey, setCityKey] = useState(SAVED.cityKey || "none");
  const [manualCityFee, setManualCityFee] = useState(SAVED.manualCityFee != null ? SAVED.manualCityFee : 150);
  useEffect(function () {
    setRateDraft(String(rate));
  }, [rate]);
  useEffect(function () {
    setSessionsDraft(String(sessions));
  }, [sessions]);
  useEffect(function () {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        tab: tab,
        rate: rate,
        sessions: sessions,
        goal: goal,
        chartMode: chartMode,
        secondaryOn: secondaryOn,
        secondaryRate: secondaryRate,
        secondarySessions: secondarySessions,
        retreatOn: retreatOn,
        retreatParticipants: retreatParticipants,
        retreatRate: retreatRate,
        retreatPerMonth: retreatPerMonth,
        usLocation: usLocation,
        avgTenure: avgTenure,
        currentClients: currentClients,
        sessionsPerClientWk: sessionsPerClientWk,
        monthlyChurn: monthlyChurn,
        monthsToTarget: monthsToTarget,
        funnel: funnel,
        filingStatus: filingStatus,
        numDependents: numDependents,
        entityType: entityType,
        sCorpSalaryInput: sCorpSalaryInput,
        existingPretaxIRA: existingPretaxIRA,
        taxAge: taxAge,
        retireAge: retireAge,
        investReturn: investReturn,
        expenses: expenses,
        cityKey: cityKey,
        manualCityFee: manualCityFee,
        viewMode: viewMode,
        wizardStep: wizardStep
      }));
    } catch (e) {}
  }, [tab, rate, sessions, goal, chartMode, secondaryOn, secondaryRate, secondarySessions, retreatOn, retreatParticipants, retreatRate, retreatPerMonth, usLocation, avgTenure, currentClients, sessionsPerClientWk, monthlyChurn, monthsToTarget, funnel, filingStatus, numDependents, entityType, sCorpSalaryInput, existingPretaxIRA, taxAge, retireAge, investReturn, expenses, cityKey, manualCityFee, viewMode, wizardStep]);
  const d = {
    color: colorForRate(rate)
  };
  const nearestRate = RATES.reduce((best, r) => Math.abs(r - rate) < Math.abs(best - rate) ? r : best, RATES[0]);
  const job2Yr = 0;
  const secondaryYr = secondaryOn ? (parseFloat(secondaryRate) || 0) * (parseFloat(secondarySessions) || 0) * 52 : 0;
  const retreatYr = retreatOn ? (parseFloat(retreatParticipants) || 0) * (parseFloat(retreatRate) || 0) * (parseFloat(retreatPerMonth) || 0) * 12 : 0;
  const otherIncomeYr = secondaryYr + retreatYr;
  const grossMoForExp = (grossYr(rate, sessions) + otherIncomeYr) / 12;
  const expMo = expenses.reduce((a, e) => a + (e.pct != null ? grossMoForExp * e.pct : +e.monthly || 0), 0);
  const expYrBase = expMo * 12;
  const setExpense = (id, val) => setExpenses(xs => xs.map(e => e.id === id ? {
    ...e,
    monthly: val
  } : e));
  const addExpense = () => setExpenses(xs => [...xs, {
    id: "custom" + Date.now(),
    label: "New expense",
    monthly: 0,
    note: "",
    custom: true
  }]);
  const removeExpense = id => setExpenses(xs => xs.filter(e => e.id !== id));
  const renameExpense = (id, label) => setExpenses(xs => xs.map(e => e.id === id ? {
    ...e,
    label
  } : e));

  // City business-license fee is based on practice gross receipts only (not the
  // W-2 second job), and is itself a deductible business expense.
  const bizFeeAt = (r, s) => cityLicenseFee(cityKey, grossYr(r, s) + otherIncomeYr, manualCityFee);
  const bizFee = bizFeeAt(rate, sessions);
  const expYr = expYrBase + bizFee;

  // Year computation at any rate/sessions, using current expenses + secondary source + second job
  const yearAt = (r, s) => computeYear(grossYr(r, s) + otherIncomeYr, expYrBase + bizFeeAt(r, s), job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
  const netYr = (r, s) => Math.round(yearAt(r, s).net);

  // Current scenario, fully broken out
  const cur = useMemo(() => {
    const y = computeYear(grossYr(rate, sessions) + otherIncomeYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    const noExp = computeYear(grossYr(rate, sessions) + otherIncomeYr, 0, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    const withoutSecondary = computeYear(grossYr(rate, sessions) + retreatYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    const withoutRetreat = computeYear(grossYr(rate, sessions) + secondaryYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    return {
      ...y,
      netYr: Math.round(y.net),
      netMo: Math.round(y.net / 12),
      netWk: Math.round(y.net / 52),
      grossYr: y.grossAll,
      grossMo: Math.round(y.grossAll / 12),
      grossWk: Math.round(y.grossAll / 52),
      grossTherYr: grossYr(rate, sessions),
      secondaryYr,
      retreatYr,
      otherIncomeYr,
      secondaryNet: secondaryOn ? Math.round(y.net - withoutSecondary.net) : 0,
      retreatNet: retreatOn ? Math.round(y.net - withoutRetreat.net) : 0,
      job2Yr,
      job2Net: 0,
      expYr,
      expMo: expYr / 12,
      bizFee,
      trueCostOfExpenses: Math.round(noExp.net - y.net),
      taxShield: Math.round(expYr - (noExp.net - y.net)),
      takeHomePct: y.grossAll > 0 ? y.net / y.grossAll : 0,
      marginPct: y.grossAll > 0 ? y.net / y.grossAll : 0
    };
  }, [rate, sessions, expYr, job2Yr, secondaryYr, secondaryOn, retreatYr, retreatOn, filingStatus, numDependents, entityType, sCorpSalaryInput]);

  // Residency comparison: same practice revenue and running costs, taxed
  // under California, New York City, Berlin (Germany), Portugal, and
  // Bordeaux (France) rules respectively.
  const residency = useMemo(() => ({
    ...computeResidency(cur.grossYr, expYr),
    nyc: computeNYC(cur.grossYr, expYr),
    pittsburgh: computePittsburgh(cur.grossYr, expYr),
    france: computeFrance(cur.grossYr, expYr),
    uae: computeUAE(cur.grossYr, expYr),
    brisbane: computeBrisbane(cur.grossYr, expYr)
  }), [cur.grossYr, expYr]);
  const usBaseline = usLocation === "nyc" ? residency.nyc.netUSD : cur.netYr;

  // Sales funnel: turn last month's marketing numbers into a caseload-growth plan.
  const funnelCalc = useMemo(() => {
    const clientValue = funnelRate * avgTenure;
    const channels = [{
      key: "pt",
      label: "Psychology Today",
      d: funnel.pt
    }, {
      key: "web",
      label: "Website / email",
      d: funnel.web
    }, {
      key: "ref",
      label: "Direct referrals",
      d: funnel.ref
    }].map(c => {
      const visits = Math.max(0, +c.d.visits || 0);
      const calls = Math.max(0, +c.d.calls || 0);
      const consults = Math.max(0, +c.d.consults || 0);
      const intake = Math.max(0, +c.d.intake || 0);
      const converted = Math.max(0, +c.d.converted || 0);
      return {
        ...c,
        visits,
        calls,
        consults,
        intake,
        converted,
        overallRate: visits > 0 ? converted / visits : 0,
        stageRates: {
          v2c: visits > 0 ? calls / visits : 0,
          c2q: calls > 0 ? consults / calls : 0,
          q2i: consults > 0 ? intake / consults : 0,
          i2w: intake > 0 ? converted / intake : 0
        },
        value: converted * clientValue
      };
    });
    const totalVisits = channels.reduce((a, c) => a + c.visits, 0);
    const totalConverted = channels.reduce((a, c) => a + c.converted, 0);
    const totalValue = channels.reduce((a, c) => a + c.value, 0);
    const blendedRate = totalVisits > 0 ? totalConverted / totalVisits : 0;
    const netChangeLastMonth = totalConverted - monthlyChurn;
    const targetClients = Math.ceil(funnelSessions / (sessionsPerClientWk > 0 ? sessionsPerClientWk : 1));
    const clientGap = Math.max(0, targetClients - currentClients);
    const monthsSafe = Math.max(1, monthsToTarget);
    const newClientsPerMonthRamp = Math.ceil(clientGap / monthsSafe) + monthlyChurn;
    const newClientsPerMonthSteady = monthlyChurn;
    const visitsNeededRamp = blendedRate > 0 ? Math.ceil(newClientsPerMonthRamp / blendedRate) : null;
    const visitsNeededSteady = blendedRate > 0 ? Math.ceil(newClientsPerMonthSteady / blendedRate) : null;
    const channelTargets = channels.map(c => {
      const share = totalConverted > 0 ? c.converted / totalConverted : 1 / channels.length;
      const neededConverted = newClientsPerMonthRamp * share;
      return {
        key: c.key,
        label: c.label,
        neededConverted: Math.ceil(neededConverted),
        neededVisits: c.overallRate > 0 ? Math.ceil(neededConverted / c.overallRate) : null
      };
    });
    const onTrack = netChangeLastMonth >= 0 && currentClients >= targetClients * 0.9;
    let healthScore = 50;
    healthScore += Math.min(25, blendedRate * 300);
    healthScore += netChangeLastMonth >= 0 ? 15 : -15;
    healthScore += currentClients >= targetClients ? 10 : Math.round((currentClients / Math.max(1, targetClients)) * 10) - 10;
    healthScore = Math.max(4, Math.min(98, Math.round(healthScore)));
    return {
      clientValue,
      channels,
      totalVisits,
      totalConverted,
      totalValue,
      blendedRate,
      netChangeLastMonth,
      targetClients,
      clientGap,
      newClientsPerMonthRamp,
      newClientsPerMonthSteady,
      visitsNeededRamp,
      visitsNeededSteady,
      channelTargets,
      onTrack,
      healthScore
    };
  }, [funnelRate, avgTenure, funnel, currentClients, sessionsPerClientWk, monthlyChurn, monthsToTarget, funnelSessions]);

  // USA Tax Strategy: retirement account simulation (Solo 401k, Traditional & Roth IRA)
  const computeRetireStrategyFor = entityTypeArg => {
    const entityForRetirement = computeYear(cur.grossTherYr + cur.otherIncomeYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityTypeArg, sCorpSalaryInput);
    const soleForSSCompare = computeYear(cur.grossTherYr + cur.otherIncomeYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, "sole_prop", 0);
    const soleNetSEEarnings = Math.max(0, soleForSSCompare.schedC - soleForSSCompare.seTax / 2);
    const netSEEarnings = entityTypeArg === "s_corp" ? Math.max(0, entityForRetirement.salary) : Math.max(0, entityForRetirement.schedC - entityForRetirement.seTax / 2);
    const employerPctForEntity = entityTypeArg === "s_corp" ? 0.25 : RETIRE_2026.solo401k.employerPct;
    const magi = Math.max(0, cur.schedC + cur.kDistribution + cur.w2Wages + cur.salary - cur.seTax / 2);
    const marginalRate = Math.max(0, Math.min(0.55, (entityForRetirement.totalTax - computeYear(cur.grossTherYr + cur.otherIncomeYr, expYr + 1000, job2Yr, filingStatus, numDependents, 0, 0, entityTypeArg, sCorpSalaryInput).totalTax) / 1000));
    const yearsToRetire = Math.max(1, retireAge - taxAge);
    const r = investReturn / 100;
    const fvAnnuity = amt => amt <= 0 ? 0 : r === 0 ? amt * yearsToRetire : amt * ((Math.pow(1 + r, yearsToRetire) - 1) / r);

    // Solo 401(k)
    const employeeCap = taxAge >= 60 && taxAge <= 63 ? RETIRE_2026.solo401k.employee60to63 : taxAge >= 50 ? RETIRE_2026.solo401k.employee50to59 : RETIRE_2026.solo401k.employeeUnder50;
    const overallCap = taxAge >= 60 && taxAge <= 63 ? RETIRE_2026.solo401k.overallCap60to63 : taxAge >= 50 ? RETIRE_2026.solo401k.overallCap50plus : RETIRE_2026.solo401k.overallCapUnder50;
    const employeeContrib = Math.min(employeeCap, netSEEarnings);
    const employerContrib = Math.max(0, Math.min(employerPctForEntity * netSEEarnings, overallCap - employeeContrib));
    const solo401kTotal = employeeContrib + employerContrib;
    const solo401k = {
      employeeContrib,
      employerContrib,
      total: solo401kTotal,
      taxSavings: solo401kTotal * marginalRate,
      futureValue: fvAnnuity(solo401kTotal),
      employerBasis: entityTypeArg === "s_corp" ? "25% of W-2 salary" : "20% of net self-employment earnings",
      employerPctLabel: entityTypeArg === "s_corp" ? "25%" : "20%"
    };

    // Traditional IRA
    const iraCap = taxAge >= 50 ? RETIRE_2026.ira.over50 : RETIRE_2026.ira.under50;
    const [tStart, tEnd] = RETIRE_2026.traditionalIraPhaseOut[filingStatus];
    let tDeductPct = magi <= tStart ? 1 : magi >= tEnd ? 0 : 1 - (magi - tStart) / (tEnd - tStart);
    const traditionalIra = {
      cap: iraCap,
      deductibleAmount: iraCap * tDeductPct,
      deductPct: tDeductPct,
      taxSavings: iraCap * tDeductPct * marginalRate,
      futureValue: fvAnnuity(iraCap)
    };

    // Roth IRA
    const [rStart, rEnd] = RETIRE_2026.rothIraPhaseOut[filingStatus];
    let rEligiblePct = magi <= rStart ? 1 : magi >= rEnd ? 0 : 1 - (magi - rStart) / (rEnd - rStart);
    const rothIra = {
      cap: iraCap,
      eligibleAmount: iraCap * rEligiblePct,
      eligiblePct: rEligiblePct,
      taxSavings: 0,
      futureValue: fvAnnuity(iraCap * rEligiblePct)
    };

    // Backdoor Roth: nondeductible Traditional IRA contribution, immediately
    // converted to Roth. The pro-rata rule (IRC §408(d)(2)) means the
    // conversion is only tax-free if you have NO other pre-tax IRA/SEP/SIMPLE
    // money — otherwise the taxable share is prorated across all IRA dollars.
    const phasedOutRoom = Math.max(0, iraCap - iraCap * rEligiblePct);
    const totalIraAfterContrib = existingPretaxIRA + iraCap;
    const taxableFraction = totalIraAfterContrib > 0 ? existingPretaxIRA / totalIraAfterContrib : 0;
    const taxableOnConversion = iraCap * taxableFraction;
    const backdoorRoth = {
      contribution: iraCap,
      phasedOutRoom,
      existingPretaxIRA,
      taxableFraction,
      taxableOnConversion,
      conversionTax: taxableOnConversion * marginalRate,
      futureValue: fvAnnuity(iraCap)
    };
    // Social Security impact: only wages (not distributions) earn SS credit.
    // Simplified steady-state projection: assumes this earnings pattern for
    // up to 35 years (SSA always divides by 420 months, even with fewer
    // years worked) — does not reflect your actual past earnings history.
    const soleCreditedEarnings = Math.min(soleNetSEEarnings, SS_WAGE_BASE);
    const scorpCreditedEarnings = Math.min(sCorpSalaryInput, SS_WAGE_BASE);
    const yearsForAIME = Math.min(35, yearsToRetire);
    const soleAIME = soleCreditedEarnings * yearsForAIME / 420;
    const scorpAIME = scorpCreditedEarnings * yearsForAIME / 420;
    const solePIA = computePIA(soleAIME);
    const scorpPIA = computePIA(scorpAIME);
    const socialSecurity = {
      soleCreditedEarnings,
      scorpCreditedEarnings,
      yearsForAIME,
      soleMonthlyPIA: solePIA,
      scorpMonthlyPIA: scorpPIA,
      soleAnnualPIA: solePIA * 12,
      scorpAnnualPIA: scorpPIA * 12,
      monthlyGap: solePIA - scorpPIA,
      annualGap: (solePIA - scorpPIA) * 12
    };
    return {
      netSEEarnings,
      magi,
      marginalRate: marginalRate,
      yearsToRetire,
      solo401k,
      traditionalIra,
      rothIra,
      backdoorRoth,
      socialSecurity
    };
  };
  const taxStrategy = useMemo(() => computeRetireStrategyFor(entityType), [cur, expYr, job2Yr, filingStatus, numDependents, entityType, sCorpSalaryInput, existingPretaxIRA, taxAge, retireAge, investReturn]);
  const taxStrategySoleProp = useMemo(() => computeRetireStrategyFor("sole_prop"), [cur, expYr, job2Yr, filingStatus, numDependents, sCorpSalaryInput, existingPretaxIRA, taxAge, retireAge, investReturn]);
  const taxStrategySCorp = useMemo(() => computeRetireStrategyFor("s_corp"), [cur, expYr, job2Yr, filingStatus, numDependents, sCorpSalaryInput, existingPretaxIRA, taxAge, retireAge, investReturn]);


  // Goal solver against net profit
  const goalSolve = useMemo(() => {
    for (let s = 15; s <= 30; s++) {
      if (netYr(rate, s) >= goal) return {
        sessions: s,
        net: netYr(rate, s),
        reached: true
      };
    }
    return {
      sessions: 30,
      net: netYr(rate, 30),
      reached: false
    };
  }, [rate, goal, expYrBase, job2Yr, cityKey, manualCityFee, secondaryYr, retreatYr, filingStatus, numDependents]);

  // Chart 1: yearly across sessions, one line per rate (combined incl. 2nd job)
  const lineData = SESSIONS.map(s => {
    const row = {
      s
    };
    RATES.forEach(r => {
      row[`net_${r}`] = netYr(r, s);
      row[`gross_${r}`] = grossYr(r, s) + job2Yr + otherIncomeYr;
    });
    return row;
  });

  // Chart 2: marginal gain — extra annual net from each added session at current rate
  const marginalData = SESSIONS.slice(1).map(s => ({
    s: `${s - 1}\u2192${s}`,
    gain: netYr(rate, s) - netYr(rate, s - 1),
    session: s
  }));

  // Chart 3: take-home efficiency — net as % of gross (combined)
  const effData = SESSIONS.map(s => {
    const g = grossYr(rate, s) + job2Yr;
    return {
      s,
      pct: +(netYr(rate, s) / g * 100).toFixed(1)
    };
  });

  // Biweekly pay schedule — anchored to a payday of Fri July 3, 2026.
  // Net per check = annual net / 26 (26 biweekly periods per year).
  const payPerCheck = netYr(rate, sessions) / 26;
  const paydays = useMemo(() => {
    const anchor = new Date(2026, 6, 3); // months are 0-indexed: 6 = July
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    // walk backward to the first payday on/after today
    let first = new Date(anchor);
    while (first > today) first = new Date(first.getTime() - 14 * 86400000);
    while (first < today) first = new Date(first.getTime() + 14 * 86400000);
    const list = [];
    let cursor = new Date(first);
    let cumulative = 0;
    for (let i = 0; i < 12; i++) {
      cumulative += payPerCheck;
      list.push({
        date: new Date(cursor),
        amount: payPerCheck,
        cumulative,
        isAnchor: cursor.getTime() === anchor.getTime()
      });
      cursor = new Date(cursor.getTime() + 14 * 86400000);
    }
    return list;
  }, [payPerCheck]);
  const fmtDate = d => d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric"
  });
  const residBreakdown = (gross, tax, net, accent, expensesAmt) => {
    const hasExp = expensesAmt != null && expensesAmt > 0;
    const maxVal = Math.max(tax, net, hasExp ? expensesAmt : 0, 1);
    const row = (label, val, barColor) => /*#__PURE__*/React.createElement("div", {
      className: "resid-bar-row",
      key: label
    }, /*#__PURE__*/React.createElement("span", {
      className: "resid-bar-label"
    }, label), /*#__PURE__*/React.createElement("div", {
      className: "resid-bar-track"
    }, /*#__PURE__*/React.createElement("div", {
      className: "resid-bar",
      style: {
        width: Math.max(3, val / maxVal * 100) + "%",
        background: barColor
      }
    })), /*#__PURE__*/React.createElement("span", {
      className: "resid-bar-val"
    }, fmt(val)));

  return /*#__PURE__*/React.createElement("div", {
      className: "resid-bars"
    }, hasExp && row("Expenses", expensesAmt, "#B98A4E"), row("Tax", tax, "#B5483F"), row("Net", net, accent));
  };
  const buildFullSummary = () => {
    const lines = [];
    lines.push("THERAPY PRACTICE SIMULATOR \u2014 FULL SUMMARY");
    lines.push("Generated " + new Date().toLocaleDateString());
    lines.push("");
    lines.push("=== SETUP ===");
    lines.push("Rate: $" + rate + "/hr, " + sessions + " sessions/week");
    lines.push("Filing status: " + filingStatus.replace(/_/g, " "));
    lines.push("Entity: " + (entityType === "s_corp" ? "Professional Corp, S-corp election (salary $" + sCorpSalaryInput.toLocaleString() + ")" : "Sole Proprietorship"));
    if (secondaryOn) lines.push("Secondary source: " + fmt(cur.secondaryYr) + "/yr");
    if (retreatOn) lines.push("Retreats/events: " + fmt(cur.retreatYr) + "/yr");
    lines.push("");
    lines.push("=== INCOME (California) ===");
    lines.push("Gross / year: " + fmt(cur.grossYr));
    lines.push("Expenses / year: " + fmt(cur.expYr));
    lines.push("Tax / year: " + fmt(cur.totalTax));
    lines.push("Net / year: " + fmt(cur.netYr));
    lines.push("Take-home rate: " + Math.round(cur.takeHomePct * 100) + "%");
    lines.push("Net / month: " + fmt(cur.netMo) + ", Net / week: " + fmt(cur.netWk));
    lines.push("");
    lines.push("=== RESIDENCY COMPARISON (same income, different location) ===");
    lines.push("California: " + fmt(cur.netYr) + " net");
    lines.push("New York City: " + fmt(residency.nyc.netUSD) + " net");
    lines.push("Berlin, Germany: " + fmt(residency.berlin.netUSD) + " net");
    lines.push("Portugal: " + fmt(residency.portugal.netUSD) + " net");
    lines.push("Bordeaux, France: " + fmt(residency.france.netUSD) + " net");
    lines.push("United Arab Emirates: " + fmt(residency.uae.netUSD) + " net");
    lines.push("Brisbane, Australia: " + fmt(residency.brisbane.netUSD) + " net");
    lines.push("");
    lines.push("=== USA TAX STRATEGY ===");
    lines.push("Net self-employment earnings: " + fmt(taxStrategy.netSEEarnings));
    lines.push("Marginal tax rate: " + (taxStrategy.marginalRate * 100).toFixed(1) + "%");
    lines.push("Solo 401(k) max contribution: " + fmt(taxStrategy.solo401k.total) + " (saves " + fmt(taxStrategy.solo401k.taxSavings) + " in tax)");
    lines.push("Traditional IRA: " + fmt(taxStrategy.traditionalIra.deductibleAmount) + " deductible of " + fmt(taxStrategy.traditionalIra.cap) + " cap");
    lines.push("Roth IRA eligible: " + fmt(taxStrategy.rothIra.eligibleAmount) + " of " + fmt(taxStrategy.rothIra.cap) + " cap");
    lines.push("Backdoor Roth taxable fraction: " + (taxStrategy.backdoorRoth.taxableFraction * 100).toFixed(0) + "%");
    lines.push("Est. Social Security, sole prop path: " + fmt(taxStrategy.socialSecurity.soleMonthlyPIA) + "/mo");
    lines.push("Est. Social Security, S-corp path: " + fmt(taxStrategy.socialSecurity.scorpMonthlyPIA) + "/mo");
    if (funnelCalc.totalConverted > 0 || funnelCalc.currentClients > 0 || currentClients > 0) {
      lines.push("");
      lines.push("=== SALES FUNNEL ===");
      lines.push("Current clients: " + currentClients + " of " + funnelCalc.targetClients + " target");
      lines.push("Client lifetime value: " + fmt(funnelCalc.clientValue));
      lines.push("Funnel health score: " + funnelCalc.healthScore + "/100");
      lines.push("New clients last month: " + funnelCalc.totalConverted + ", lost: " + monthlyChurn);
    }
    lines.push("");
    lines.push("Full interactive tool: https://cavatello.github.io/therapist-tools/");
    lines.push("(Estimates only, not tax advice \u2014 see the tool for full disclaimers.)");
    return lines.join("\n");
  };
  const resetToZero = () => {
    setRate(0);
    setSessions(0);
    setSecondaryOn(false);
    setSecondaryRate("");
    setSecondarySessions("");
    setRetreatOn(false);
    setRetreatParticipants("");
    setRetreatRate("");
    setRetreatPerMonth("");
    setExpenses(DEFAULT_EXPENSES.map(e => ({
      ...e,
      monthly: 0
    })));
    setCityKey("none");
    setManualCityFee(null);
    setSCorpSalaryInput(0);
    setEntityType("sole_prop");
    setExistingPretaxIRA(0);
    setTaxAge(0);
    setRetireAge(0);
    setInvestReturn(0);
    setAvgTenure("");
    setCurrentClients(0);
    setSessionsPerClientWk(0);
    setMonthlyChurn(0);
    setMonthsToTarget(0);
    setFunnel({
      pt: {
        visits: 0,
        calls: 0,
        consults: 0,
        converted: 0
      },
      web: {
        visits: 0,
        calls: 0,
        consults: 0,
        converted: 0
      },
      ref: {
        visits: 0,
        calls: 0,
        consults: 0,
        converted: 0
      }
    });
  };
  const buildShareURL = () => {
    const state = {
      rate, sessions, goal, chartMode,
      secondaryOn, secondaryRate, secondarySessions,
      retreatOn, retreatParticipants, retreatRate, retreatPerMonth,
      usLocation, avgTenure, currentClients, sessionsPerClientWk, monthlyChurn, monthsToTarget, funnel,
      filingStatus, numDependents, entityType, sCorpSalaryInput, existingPretaxIRA,
      taxAge, retireAge, investReturn,
      expenses, cityKey, manualCityFee, viewMode, wizardStep
    };
    const encoded = encodeShareState(state);
    const base = window.location.origin + window.location.pathname;
    return encoded ? base + "#s=" + encoded : base;
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "planner" + (viewMode === "guided" ? " guided-mode" : "") + (page === "grow" ? " grow-mode" : "") + (VARIANT ? " v" + VARIANT : "") + (VARIANT === "04" && !(rate > 0 || sessions > 0) ? " v04-empty" : "")
  }, /*#__PURE__*/React.createElement("style", null, CSS), /*#__PURE__*/React.createElement("div", {
    className: "sitenav"
  }, /*#__PURE__*/React.createElement("a", {
    className: "sitenav-mark",
    href: "index.html"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sitenav-mono"
  }, "CA"), /*#__PURE__*/React.createElement("span", {
    className: "sitenav-wordmark"
  }, "Therapy Practice"), VARIANT === "01" && /*#__PURE__*/React.createElement("span", {
    className: "v01-tagline"
  }, "California \u00B7 2026 net estimates")), /*#__PURE__*/React.createElement("nav", {
    className: "sitenav-links",
    "aria-label": "Site"
  }, [["#sim", "Simulator", "run your numbers", page === "sim"], ["#grow", "Grow Your Practice", "marketing and sales", page === "grow"], ["rates.html", "Field Notes", "what CA actually pays", false], ["https://cavatello.github.io/therapist-tycoon/tycoon.html", "Tycoon", "the practice, as a game", false]].map(([href, t, dsc, on]) => /*#__PURE__*/React.createElement("a", {
    key: href,
    href: href,
    className: "sitenav-item" + (on ? " sitenav-on" : ""),
    "aria-current": on ? "page" : null
  }, /*#__PURE__*/React.createElement("span", {
    className: "sitenav-t"
  }, t), /*#__PURE__*/React.createElement("span", {
    className: "sitenav-d"
  }, dsc))))), showShareBanner && /*#__PURE__*/React.createElement("div", {
    className: "share-banner"
  }, /*#__PURE__*/React.createElement("span", null, "\uD83D\uDD17 ", /*#__PURE__*/React.createElement("b", null, "You're viewing a shared setup"), " \u2014 every number below reflects the rates, expenses, and choices someone saved into this link. Change anything and it's yours to explore; click "), /*#__PURE__*/React.createElement("b", null, "Share"), /*#__PURE__*/React.createElement("span", null, " anytime (top right) to save your own version as a new link."), /*#__PURE__*/React.createElement("button", {
    className: "share-banner-close",
    onClick: () => setShowShareBanner(false),
    "aria-label": "Dismiss"
  }, "\u00D7")), page === "grow" && /*#__PURE__*/React.createElement("header", {
    className: "growhero"
  }, /*#__PURE__*/React.createElement("div", {
    className: "hero-eyebrow"
  }, "Marketing & sales"), /*#__PURE__*/React.createElement("h1", {
    className: "hero-title"
  }, "Grow your ", /*#__PURE__*/React.createElement("span", {
    className: "accent"
  }, "practice")), /*#__PURE__*/React.createElement("p", {
    className: "hero-sub"
  }, "How many enquiries it takes to keep a caseload full \u2014 and what each client is actually worth to you."), /*#__PURE__*/React.createElement("div", {
    className: "growrate"
  }, /*#__PURE__*/React.createElement("div", {
    className: "growrate-fields"
  }, /*#__PURE__*/React.createElement("div", {
    className: "growrate-field"
  }, /*#__PURE__*/React.createElement("label", {
    className: "growrate-lbl",
    htmlFor: "growrate-input"
  }, "Session rate"), /*#__PURE__*/React.createElement("div", {
    className: "growrate-row"
  }, /*#__PURE__*/React.createElement("span", {
    className: "growrate-cur"
  }, "$"), /*#__PURE__*/React.createElement("input", {
    id: "growrate-input",
    type: "number",
    min: 0,
    className: "growrate-input",
    value: funnelRate,
    onChange: e => setFunnelRateOverride(e.target.value === "" ? "" : Number(e.target.value))
  }), /*#__PURE__*/React.createElement("span", {
    className: "growrate-unit"
  }, "/hr"))), /*#__PURE__*/React.createElement("div", {
    className: "growrate-field"
  }, /*#__PURE__*/React.createElement("label", {
    className: "growrate-lbl",
    htmlFor: "growsess-input"
  }, "Target sessions / week"), /*#__PURE__*/React.createElement("div", {
    className: "growrate-row"
  }, /*#__PURE__*/React.createElement("input", {
    id: "growsess-input",
    type: "number",
    min: 0,
    className: "growrate-input",
    value: funnelSessions,
    onChange: e => setFunnelSessionsOverride(e.target.value === "" ? "" : Number(e.target.value))
  }), /*#__PURE__*/React.createElement("span", {
    className: "growrate-unit"
  }, "/wk")))), /*#__PURE__*/React.createElement("div", {
    className: "growrate-derived"
  }, "That's a target caseload of ", /*#__PURE__*/React.createElement("b", null, funnelCalc.targetClients), funnelCalc.targetClients === 1 ? " client" : " clients", sessionsPerClientWk > 0 ? " \u2014 " + funnelSessions + " sessions \u00F7 " + sessionsPerClientWk + " per client per week." : " \u2014 set sessions per client per week below to refine this."), (funnelRateOverridden || funnelSessionsOverridden) && /*#__PURE__*/React.createElement("button", {
    className: "growrate-reset",
    onClick: () => { setFunnelRateOverride(null); setFunnelSessionsOverride(null); }
  }, "\u21BA Use my Simulator numbers"), /*#__PURE__*/React.createElement("p", {
    className: "growrate-note"
  }, (funnelRateOverridden || funnelSessionsOverridden) ? "Just for this page \u2014 your Simulator figures (" + fmt(rate) + "/hr, " + sessions + " sessions/wk) are unchanged." : (rate > 0 || sessions > 0) ? "Pulled from your Simulator numbers. Editing them here won't change them there." : "Nothing set on the Simulator yet \u2014 type your numbers here, or set them there."))), page === "grow" && /*#__PURE__*/React.createElement("section", {
    className: "growlanding"
  }, /*#__PURE__*/React.createElement("h2", {
    className: "growlanding-h"
  }, "Why a clinician needs this"), /*#__PURE__*/React.createElement("p", {
    className: "growlanding-lede"
  }, "Nobody trains you in this. You train in theory, ethics and clinical practice \u2014 and then you are handed a business whose only revenue depends on strangers finding you and choosing to stay. Three things make that different from a salaried post."), /*#__PURE__*/React.createElement("div", {
    className: "growcards"
  }, /*#__PURE__*/React.createElement("div", {
    className: "growcard"
  }, /*#__PURE__*/React.createElement("span", {
    className: "growcard-n"
  }, "01"), /*#__PURE__*/React.createElement("h3", null, "A caseload leaks"), /*#__PURE__*/React.createElement("p", null, "Therapy works. People finish, move, or stop \u2014 so a full caseload is not a state you arrive at, it is a level you hold. Every month you need arrivals just to stand still."), monthlyChurn > 0 && funnelCalc.clientValue > 0 ? /*#__PURE__*/React.createElement("p", {
    className: "growcard-calc"
  }, "At ", /*#__PURE__*/React.createElement("b", null, monthlyChurn + (monthlyChurn === 1 ? " client" : " clients")), " lost a month, you need ", /*#__PURE__*/React.createElement("b", null, monthlyChurn * 12 + " new clients a year"), " to stay level \u2014 about ", /*#__PURE__*/React.createElement("b", null, fmt(monthlyChurn * 12 * funnelCalc.clientValue)), " of work you have to win before you grow at all.") : /*#__PURE__*/React.createElement("p", {
    className: "growcard-calc growcard-calc-empty"
  }, "Fill in \u201Cclients lost last month\u201D below and this becomes your own number.")), /*#__PURE__*/React.createElement("div", {
    className: "growcard"
  }, /*#__PURE__*/React.createElement("span", {
    className: "growcard-n"
  }, "02"), /*#__PURE__*/React.createElement("h3", null, "A client is not one session"), /*#__PURE__*/React.createElement("p", null, "Most therapists picture a single appointment when they think about a new enquiry, and so treat marketing as an expense. Priced over the whole course of therapy it reads very differently."), funnelCalc.clientValue > 0 ? /*#__PURE__*/React.createElement("p", {
    className: "growcard-calc"
  }, "One client is worth ", /*#__PURE__*/React.createElement("b", null, fmt(funnelCalc.clientValue)), " to you. That is the figure to hold in mind when you weigh a directory listing, a website, or an afternoon spent meeting referrers.") : /*#__PURE__*/React.createElement("p", {
    className: "growcard-calc growcard-calc-empty"
  }, "Set your rate and average sessions per client below to see your figure.")), /*#__PURE__*/React.createElement("div", {
    className: "growcard"
  }, /*#__PURE__*/React.createElement("span", {
    className: "growcard-n"
  }, "03"), /*#__PURE__*/React.createElement("h3", null, "Enquiries arrive late"), /*#__PURE__*/React.createElement("p", null, "Someone who finds you today may sit with it for a fortnight before making contact, and longer again before a first session. The work you do this month shows up in next month's diary."), /*#__PURE__*/React.createElement("p", {
    className: "growcard-calc"
  }, "Which is why marketing during a quiet spell rarely rescues it \u2014 by the time the enquiries convert, the quiet month has already been and gone."))), /*#__PURE__*/React.createElement("h2", {
    className: "growlanding-h growlanding-h2"
  }, "The therapy year is not flat"), /*#__PURE__*/React.createElement("p", {
    className: "growlanding-lede"
  }, "Private practice runs in a rhythm, and it is consistent enough to plan around. The exact shape varies by client mix and region \u2014 treat this as the pattern to check your own diary against, not a forecast."), /*#__PURE__*/React.createElement("div", {
    className: "season"
  }, [["Jan\u2013Mar", "busy", "New-year momentum and returning routines. Insurance-based practices can see the opposite early on, as reset deductibles push costs onto clients for a few weeks."], ["Apr\u2013Jun", "steady", "The most predictable stretch of the year. The right time to build the pipeline for summer rather than spend it."], ["Jul\u2013Aug", "quiet", "Holidays, childcare, travel \u2014 yours and theirs. Cancellations rise and new enquiries thin out."], ["Sep\u2013Oct", "busy", "The strongest rebound of the year. Terms restart, routines return, and postponed problems get addressed."], ["Nov\u2013Dec", "quiet", "Enquiries fall away through the holidays even as existing clients keep attending. Recovery lands in January."]].map(([period, tone, note]) => /*#__PURE__*/React.createElement("div", {
    key: period,
    className: "season-row season-" + tone
  }, /*#__PURE__*/React.createElement("span", {
    className: "season-period"
  }, period), /*#__PURE__*/React.createElement("span", {
    className: "season-tag"
  }, tone), /*#__PURE__*/React.createElement("span", {
    className: "season-note"
  }, note)))), funnelRate > 0 && funnelSessions > 0 ? /*#__PURE__*/React.createElement("p", {
    className: "growlanding-cost"
  }, /*#__PURE__*/React.createElement("b", null, "What a quiet month costs you: "), "at ", fmt(funnelRate), "/hr and ", funnelSessions, " sessions a week, a month running a fifth below target is about ", /*#__PURE__*/React.createElement("b", null, fmt(funnelRate * funnelSessions * 4.33 * 0.2)), " of billing \u2014 and two such months a year is ", /*#__PURE__*/React.createElement("b", null, fmt(funnelRate * funnelSessions * 4.33 * 0.2 * 2)), ". The point of the tools below is to make that a decision rather than a surprise.") : /*#__PURE__*/React.createElement("p", {
    className: "growlanding-cost growcard-calc-empty"
  }, "Enter a rate and target sessions above to see what a quiet month would cost you."), /*#__PURE__*/React.createElement("p", {
    className: "growlanding-bridge"
  }, "So: work out what a client is worth, how many enquiries it takes to land one, and how far ahead you need to start. That is what the rest of this page does.")), /*#__PURE__*/React.createElement("header", {
    className: "hero"
  }, /*#__PURE__*/React.createElement("div", {
    className: "hero-eyebrow"
  }, "2026 net estimates"), /*#__PURE__*/React.createElement("h1", {
    className: "hero-title"
  }, "California Therapy Practice", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("span", {
    className: "accent"
  }, "Simulator")), /*#__PURE__*/React.createElement("p", {
    className: "hero-sub"
  }, "What your practice actually pays \u2014 from your session rate to your entity structure to your retirement, worked out together for a California license."), VARIANT === "02" && /*#__PURE__*/React.createElement("div", {
    className: "v02-kpi"
  }, [["Gross", fmt(cur.grossYr), ""], ["\u2212 Expenses", fmt(cur.expYr), "neg"], ["\u2212 Tax", fmt(cur.totalTax), "neg"]].map(([k, v, cls]) => /*#__PURE__*/React.createElement("div", {
    key: k,
    className: "v02-kpi-row"
  }, /*#__PURE__*/React.createElement("span", {
    className: "k"
  }, k), /*#__PURE__*/React.createElement("span", {
    className: "v" + (cls ? " " + cls : "")
  }, v))), /*#__PURE__*/React.createElement("div", {
    className: "v02-kpi-row net"
  }, /*#__PURE__*/React.createElement("span", {
    className: "k"
  }, "= Net"), /*#__PURE__*/React.createElement("span", {
    className: "v"
  }, fmt(cur.netYr))), rate > 0 ? /*#__PURE__*/React.createElement("p", {
    className: "v02-kpi-note"
  }, fmt(rate) + "/hr \u00B7 " + sessions + " sessions/wk") : /*#__PURE__*/React.createElement("p", {
    className: "v02-kpi-note"
  }, "Enter a rate below and this fills in."))), (widgetCollapsed ? /*#__PURE__*/React.createElement("button", {
  className: "sticky-summary-tab",
  onClick: () => setWidgetCollapsed(false),
  title: "Show gross / expenses / tax / net"
}, /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-tab-val",
  style: {
    color: d.color
  }
}, fmt(cur.netYr)), /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-tab-lbl"
}, "net \u25C2")) : /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary" + (justPulsed ? " pulsing" : ""),
  style: {
    borderColor: d.color
  }
}, /*#__PURE__*/React.createElement("button", {
  className: "sticky-summary-close",
  onClick: () => setWidgetCollapsed(true),
  title: "Hide this widget"
}, "\u2715"), /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary-row"
}, /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-label"
}, "Gross"), /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-val"
}, fmt(cur.grossYr))), /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary-row"
}, /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-label"
}, "\u2212 Expenses"), /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-val neg"
}, fmt(cur.expYr))), /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary-row"
}, /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-label"
}, "\u2212 Tax"), /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-val neg"
}, fmt(cur.totalTax))), /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary-row sticky-summary-net"
}, /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-label"
}, "= Net"), /*#__PURE__*/React.createElement("span", {
  className: "sticky-summary-val",
  style: {
    color: d.color
  }
}, fmt(cur.netYr))), /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary-sub"
}, "$", rate, "/hr \u00B7 ", sessions, " sessions/wk"), /*#__PURE__*/React.createElement("div", {
  style: {
    position: "relative"
  }
}, /*#__PURE__*/React.createElement("button", {
  className: "summary-btn summary-btn-primary",
  style: {
    width: "100%"
  },
  onClick: () => setShowSaveMenu(v => !v)
}, shareFeedback || "\uD83D\uDCBE Save \u25BE"), showSaveMenu && /*#__PURE__*/React.createElement("div", {
  className: "save-menu"
}, /*#__PURE__*/React.createElement("button", {
  onClick: () => {
    const url = buildShareURL();
    window.history.replaceState(null, "", url);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(() => {
        setShareFeedback("Link copied!");
        setTimeout(() => setShareFeedback(""), 2500);
      }).catch(() => {
        setShareFeedback("Copy failed");
        setTimeout(() => setShareFeedback(""), 2500);
      });
    }
    setShowSaveMenu(false);
  }
}, "\uD83D\uDD17 Copy URL"), /*#__PURE__*/React.createElement("button", {
  onClick: () => {
    const url = buildShareURL();
    const subject = encodeURIComponent("Therapy Practice Simulator \u2014 my setup");
    const body = encodeURIComponent("Here's my current setup: " + url);
    window.location.href = "mailto:?subject=" + subject + "&body=" + body;
    setShowSaveMenu(false);
  }
}, "\u2709\uFE0F Email URL"), /*#__PURE__*/React.createElement("button", {
  onClick: () => {
    setShowSaveMenu(false);
    setTimeout(() => window.print(), 100);
  }
}, "\uD83D\uDDA8\uFE0F Print entire simulation"))), /*#__PURE__*/React.createElement("button", {
  className: "summary-btn",
  style: {
    width: "100%",
    marginTop: 8
  },
  onClick: () => {
    if (window.confirm("Reset every field back to zero? This clears your current setup.")) resetToZero();
  },
  title: "Clear every input back to zero"
}, "\u21BA Reset to zero"), /*#__PURE__*/React.createElement("div", {
  className: "sticky-summary-hint"
}, "\uD83D\uDCBE Save copies, emails, or prints this exact setup."))), viewMode === "current" && /*#__PURE__*/React.createElement("nav", {
    className: "tabs"
  }, [["income", "Income", "what you bill"], ["expenses", "Expenses", "what it costs"], ["profit", "Profit", "before tax"], ["taxstrategy", "USA Tax Strategy", "keep more of it"], ["residency", "Residency", "compare locations"], ["funnel", "Sales Funnel", "grow your caseload"]].map(([k, lbl, sub]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    className: "tab" + (tab === k ? " tab-on" : ""),
    style: tab === k ? {
      borderColor: d.color
    } : {},
    onClick: () => setTab(k)
  }, /*#__PURE__*/React.createElement("span", {
    className: "tab-lbl"
  }, lbl), /*#__PURE__*/React.createElement("span", {
    className: "tab-sub"
  }, sub)))), viewMode === "guided" && /*#__PURE__*/React.createElement("nav", {
    className: "guided-jumpnav"
  }, /*#__PURE__*/React.createElement("div", {
    className: "jumpnav-group"
  }, /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-group-lbl"
  }, "Your finances"), [["sec-income", "Income", fmt(cur.grossYr)], ["sec-expenses", "Expenses", "\u2212" + fmt(cur.expYr)], ["sec-profit", "Profit", fmt(cur.netYr)], ["sec-taxstrategy", "Tax Strategy", Math.round(cur.takeHomePct * 100) + "%"]].map(([id, lbl, val]) => /*#__PURE__*/React.createElement("a", {
    key: id,
    href: "#" + id,
    className: "jumpnav-pill" + (activeSection === id ? " jumpnav-active" : "")
  }, /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-lbl"
  }, lbl), /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-val"
  }, val))))), viewMode === "wizard" && /*#__PURE__*/React.createElement("div", {
    className: "wizard-stepper"
  }, wizardSteps.map((k, i) => /*#__PURE__*/React.createElement(React.Fragment, {
    key: k
  }, /*#__PURE__*/React.createElement("div", {
    className: "wizard-dot" + (i + 1 < wizardStep ? " done" : i + 1 === wizardStep ? " now" : "")
  }, i + 1 < wizardStep ? "\u2713" : i + 1), i < wizardSteps.length - 1 && /*#__PURE__*/React.createElement("div", {
    className: "wizard-line"
  })))), isVisible("income") && /*#__PURE__*/React.createElement("div", {id:"sec-income"}, sectionIntro("income"), /*#__PURE__*/React.createElement(React.Fragment, null, showIncomePrimary && /*#__PURE__*/React.createElement("section", {
    className: "controls"
  }, /*#__PURE__*/React.createElement("span", {
    className: "controls-badge"
  }, "Start here"), /*#__PURE__*/React.createElement("div", {
    className: "control-block"
  }, /*#__PURE__*/React.createElement("div", {
    className: "control-label"
  }, "Hourly rate \u00A0", /*#__PURE__*/React.createElement("span", {
    className: "control-val-wrap"
  }, "$", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: "control-val-input",
    min: 50,
    max: 300,
    step: 1,
    value: rateDraft,
    onChange: e => setRateDraft(e.target.value),
    onBlur: () => setRate(Math.max(50, Math.min(300, +rateDraft || 50))),
    onKeyDown: e => {
      if (e.key === "Enter") e.target.blur();
    }
  }), "/hr")), /*#__PURE__*/React.createElement("input", {
    type: "range",
    min: 50,
    max: 300,
    step: 5,
    value: rate,
    onChange: e => setRate(+e.target.value),
    className: "slider",
    style: {
      accentColor: d.color
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "slider-ends"
  }, /*#__PURE__*/React.createElement("span", null, "$50"), /*#__PURE__*/React.createElement("span", null, "$300"))), /*#__PURE__*/React.createElement("div", {
    className: "control-block"
  }, /*#__PURE__*/React.createElement("div", {
    className: "control-label"
  }, "Sessions / week ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: "control-val-input",
    min: 0,
    max: 60,
    step: 1,
    value: sessionsDraft,
    onChange: e => setSessionsDraft(e.target.value),
    onBlur: () => setSessions(Math.max(0, Math.min(60, +sessionsDraft || 0))),
    onKeyDown: e => {
      if (e.key === "Enter") e.target.blur();
    }
  })), /*#__PURE__*/React.createElement("input", {
    type: "range",
    min: 15,
    max: 30,
    value: sessions,
    onChange: e => setSessions(+e.target.value),
    className: "slider",
    style: {
      accentColor: d.color
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "slider-ends"
  }, /*#__PURE__*/React.createElement("span", null, "15"), /*#__PURE__*/React.createElement("span", null, "30")))), showIncomeAddons && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    className: "job2"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-head"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-title"
  }, /*#__PURE__*/React.createElement("h3", null, "Secondary source"), /*#__PURE__*/React.createElement("span", {
    className: "job2-tag"
  }, "different rate, e.g. insurance-reimbursement clients at a different rate")), null), /*#__PURE__*/React.createElement("button", {
    className: "toggle" + (secondaryOn ? " toggle-on" : ""),
    onClick: () => setSecondaryOn(v => !v),
    "aria-pressed": secondaryOn
  }, /*#__PURE__*/React.createElement("span", {
    className: "toggle-knob"
  }), /*#__PURE__*/React.createElement("span", {
    className: "toggle-lbl"
  }, secondaryOn ? "Included" : "Off")), secondaryOn && /*#__PURE__*/React.createElement("div", {
    className: "job2-body"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-field"
  }, /*#__PURE__*/React.createElement("label", null, "Rate per session"), /*#__PURE__*/React.createElement("div", {
    className: "job2-input"
  }, /*#__PURE__*/React.createElement("span", null, "$"), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 90",
    value: secondaryRate,
    onChange: e => setSecondaryRate(e.target.value)
  }), /*#__PURE__*/React.createElement("span", {
    className: "job2-unit"
  }, "/session"))), /*#__PURE__*/React.createElement("div", {
    className: "job2-field"
  }, /*#__PURE__*/React.createElement("label", null, "Sessions / week"), /*#__PURE__*/React.createElement("div", {
    className: "job2-input"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 5",
    value: secondarySessions,
    onChange: e => setSecondarySessions(e.target.value)
  }), /*#__PURE__*/React.createElement("span", {
    className: "job2-unit"
  }, "/wk"))), /*#__PURE__*/React.createElement("div", {
    className: "job2-summary"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-sum-row"
  }, /*#__PURE__*/React.createElement("span", null, "Adds gross"), /*#__PURE__*/React.createElement("strong", null, fmt(cur.secondaryYr), "/yr")), /*#__PURE__*/React.createElement("div", {
    className: "job2-sum-row"
  }, /*#__PURE__*/React.createElement("span", null, "Net after tax*"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: d.color
    }
  }, fmt(cur.secondaryNet), "/yr")), /*#__PURE__*/React.createElement("div", {
    className: "job2-sum-note"
  }, "*marginal — taxed together with your primary rate at the combined self-employment rate, so this is what the secondary source actually adds to take-home")))), /*#__PURE__*/React.createElement("section", {
    className: "job2"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-head"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-title"
  }, /*#__PURE__*/React.createElement("h3", null, "Retreats / Special Events"), /*#__PURE__*/React.createElement("span", {
    className: "job2-tag"
  }, "workshops, group intensives, or one-off events")), /*#__PURE__*/React.createElement("button", {
    className: "toggle" + (retreatOn ? " toggle-on" : ""),
    onClick: () => setRetreatOn(v => !v),
    "aria-pressed": retreatOn
  }, /*#__PURE__*/React.createElement("span", {
    className: "toggle-knob"
  }), /*#__PURE__*/React.createElement("span", {
    className: "toggle-lbl"
  }, retreatOn ? "Included" : "Off"))), retreatOn && /*#__PURE__*/React.createElement("div", {
    className: "job2-body"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-field"
  }, /*#__PURE__*/React.createElement("label", null, "Participants per event"), /*#__PURE__*/React.createElement("div", {
    className: "job2-input"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 8",
    value: retreatParticipants,
    onChange: e => setRetreatParticipants(e.target.value)
  }))), /*#__PURE__*/React.createElement("div", {
    className: "job2-field"
  }, /*#__PURE__*/React.createElement("label", null, "Rate per participant"), /*#__PURE__*/React.createElement("div", {
    className: "job2-input"
  }, /*#__PURE__*/React.createElement("span", null, "$"), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 1,
    placeholder: "e.g. 150",
    value: retreatRate,
    onChange: e => setRetreatRate(e.target.value)
  }))), /*#__PURE__*/React.createElement("div", {
    className: "job2-field"
  }, /*#__PURE__*/React.createElement("label", null, "Events per month"), /*#__PURE__*/React.createElement("div", {
    className: "job2-input"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 0.5,
    placeholder: "e.g. 1",
    value: retreatPerMonth,
    onChange: e => setRetreatPerMonth(e.target.value)
  }))), /*#__PURE__*/React.createElement("div", {
    className: "job2-summary"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-sum-row"
  }, /*#__PURE__*/React.createElement("span", null, "Adds gross"), /*#__PURE__*/React.createElement("strong", null, fmt(cur.retreatYr), "/yr")), /*#__PURE__*/React.createElement("div", {
    className: "job2-sum-row"
  }, /*#__PURE__*/React.createElement("span", null, "Net after tax*"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: d.color
    }
  }, fmt(cur.retreatNet), "/yr")), /*#__PURE__*/React.createElement("div", {
    className: "job2-sum-note"
  }, "*marginal — taxed together with your primary rate at the combined self-employment rate, so this is what retreats/events actually add to take-home")))), /*#__PURE__*/React.createElement("p", {
    className: "term-clarify"
  }, /*#__PURE__*/React.createElement("b", null, "Gross"), " = what you bill, before anything is taken out. ", /*#__PURE__*/React.createElement("b", null, "Expenses"), " = what it costs to run the practice. ", /*#__PURE__*/React.createElement("b", null, "Profit"), " (sometimes called net practice income) = gross minus expenses, before tax. ", /*#__PURE__*/React.createElement("b", null, "Net"), " = what actually lands in your bank account, after tax too."), /*#__PURE__*/React.createElement("section", {
    className: "stats"
  }, /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: secondaryOn || retreatOn ? "Combined gross / year" : "Gross per year",
    value: fmt(cur.grossYr),
    accent: "#26241E",
    note: secondaryOn || retreatOn ? [`therapy ${fmt(cur.grossTherYr)}`, secondaryOn ? `secondary ${fmt(cur.secondaryYr)}` : null, retreatOn ? `retreats ${fmt(cur.retreatYr)}` : null].filter(Boolean).join(" + ") : `at $${rate}/hr · ${sessions} sessions/wk`
  }), /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: secondaryOn || retreatOn ? "Combined net / year" : "Net per year",
    value: fmt(cur.netYr),
    accent: d.color,
    note: `take-home ${fmt(cur.netMo)}/mo · ${fmt(cur.netWk)}/wk`
  }), /*#__PURE__*/React.createElement("div", {
    className: "stat-col"
  }, /*#__PURE__*/React.createElement(Stat, {
    label: "Expenses / year",
    value: "\u2212" + fmt(cur.expYr),
    neg: true,
    note: `${fmt(cur.expMo)}/mo \u00B7 Schedule C deductions`
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Tax & withholding",
    value: "\u2212" + fmt(cur.totalTax),
    neg: true,
    note: "federal · CA · FICA · SDI"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Take-home rate",
    value: Math.round(cur.takeHomePct * 100) + "%",
    note: "of gross, after tax"
  }))), /*#__PURE__*/React.createElement("section", {
    className: "strip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Gross / week"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.grossWk)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "net ", fmt(cur.netWk))), /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Gross / month"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.grossMo)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "net ", fmt(cur.netMo))), /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Gross / year"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.grossYr)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "net ", fmt(cur.netYr)))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Side by side, at ", sessions, " sessions a week"), /*#__PURE__*/React.createElement("p", null, "Holding your caseload fixed, here's what each therapy rate delivers", secondaryOn ? ", with your other income sources included in gross, net, and tax" : "", ". The jump from one row to the next is pure pricing power — same hours, more money kept.")), /*#__PURE__*/React.createElement("div", {
    className: "table-wrap"
  }, /*#__PURE__*/React.createElement("table", null, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Rate"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, "Gross / year"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, "Net / year"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, "Tax"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, "Keeps"), /*#__PURE__*/React.createElement("th", null, "vs. current net"), /*#__PURE__*/React.createElement("th", null))), /*#__PURE__*/React.createElement("tbody", null, RATES.map(r => {
    const gy = grossYr(r, sessions) + job2Yr + otherIncomeYr;
    const ny = netYr(r, sessions);
    const tax = gy - ny;
    const keepPct = Math.round(ny / gy * 100);
    const delta = ny - cur.netYr;
    const isCur = r === nearestRate;
    return /*#__PURE__*/React.createElement("tr", {
      key: r,
      className: isCur ? "row-on" : "",
      onClick: () => setRate(r)
    }, /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
      className: "tdot",
      style: {
        background: RATE_DATA[r].color
      }
    }), "$", r, "/hr"), /*#__PURE__*/React.createElement("td", {
      className: "num-head"
    }, fmt(gy)), /*#__PURE__*/React.createElement("td", {
      className: "num-head strong"
    }, fmt(ny)), /*#__PURE__*/React.createElement("td", {
      className: "num-head muted"
    }, "\u2212" + fmt(tax)), /*#__PURE__*/React.createElement("td", {
      className: "num-head muted"
    }, keepPct, "%"), /*#__PURE__*/React.createElement("td", {
      className: delta === 0 ? "muted" : delta > 0 ? "pos" : "neg"
    }, delta === 0 ? "—" : (delta > 0 ? "+" : "\u2212") + fmt(Math.abs(delta))), /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("div", {
      className: "bar-cell"
    }, /*#__PURE__*/React.createElement("div", {
      className: "bar-fill",
      style: {
        width: ny / netYr(200, 30) * 100 + "%",
        background: RATE_DATA[r].color
      }
    }))));
  }))))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head card-head-row"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", null, "Biweekly take-home calendar"), /*#__PURE__*/React.createElement("p", null, "Net pay split across 26 checks a year, anchored to a payday of ", /*#__PURE__*/React.createElement("strong", null, "Fri, Jul 3 2026"), " and every other Friday after. Each check is your annual net ÷ 26 at $", rate, "/hr · ", sessions, " sessions/wk.")), /*#__PURE__*/React.createElement("div", {
    className: "paycheck-badge",
    style: {
      borderColor: d.color
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "paycheck-k"
  }, "Per check"), /*#__PURE__*/React.createElement("span", {
    className: "paycheck-v",
    style: {
      color: d.color
    }
  }, fmt(payPerCheck)), /*#__PURE__*/React.createElement("span", {
    className: "paycheck-sub"
  }, "every 2 weeks"))), /*#__PURE__*/React.createElement("div", {
    className: "pay-grid"
  }, paydays.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "pay-cell" + (p.isAnchor ? " pay-anchor" : ""),
    style: p.isAnchor ? {
      borderColor: d.color
    } : {}
  }, p.isAnchor && /*#__PURE__*/React.createElement("span", {
    className: "pay-flag",
    style: {
      background: d.color
    }
  }, "anchor"), /*#__PURE__*/React.createElement("span", {
    className: "pay-date"
  }, fmtDate(p.date)), /*#__PURE__*/React.createElement("span", {
    className: "pay-amt"
  }, fmt(p.amount)), /*#__PURE__*/React.createElement("span", {
    className: "pay-cum"
  }, fmt(p.cumulative), " ytd")))), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "Shows the next 12 paydays. A biweekly schedule lands 26 checks a year, so two months each year carry a third check — those are the bonus-feeling paydays."))))), isVisible("expenses") && /*#__PURE__*/React.createElement("div", {id:"sec-expenses"}, sectionIntro("expenses"), /*#__PURE__*/React.createElement(ExpensesTab, {
    expenses: expenses,
    expMo: expMo,
    expYr: expYr,
    cur: cur,
    color: d.color,
    setExpense: setExpense,
    setExpenses: setExpenses,
    addExpense: addExpense,
    removeExpense: removeExpense,
    renameExpense: renameExpense,
    rate: rate,
    sessions: sessions,
    cityKey: cityKey,
    setCityKey: setCityKey,
    manualCityFee: manualCityFee,
    setManualCityFee: setManualCityFee,
    bizFee: bizFee,
    grossTherYr: grossYr(rate, sessions) + otherIncomeYr
  })), isVisible("profit") && /*#__PURE__*/React.createElement("div", {id:"sec-profit"}, sectionIntro("profit"), /*#__PURE__*/React.createElement(ProfitTab, {
    cur: cur,
    color: d.color,
    rate: rate,
    sessions: sessions,
    rates: RATES,
    rateData: RATE_DATA,
    sessionsList: SESSIONS,
    expYr: expYr,
    expYrBase: expYrBase,
    job2Yr: job2Yr,
    setRate: setRate,
    job2On: false,
    cityKey: cityKey,
    manualCityFee: manualCityFee,
    filingStatus: filingStatus,
    numDependents: numDependents,
    entityType: entityType,
    sCorpSalaryInput: sCorpSalaryInput,
    taxStrategy: taxStrategy
  })), isVisible("funnel") && /*#__PURE__*/React.createElement("div", {id:"sec-funnel"}, /*#__PURE__*/React.createElement(FunnelTab, {
    color: d.color,
    rate: funnelRate,
    sessions: funnelSessions,
    avgTenure: avgTenure,
    setAvgTenure: setAvgTenure,
    currentClients: currentClients,
    setCurrentClients: setCurrentClients,
    sessionsPerClientWk: sessionsPerClientWk,
    setSessionsPerClientWk: setSessionsPerClientWk,
    monthlyChurn: monthlyChurn,
    setMonthlyChurn: setMonthlyChurn,
    monthsToTarget: monthsToTarget,
    setMonthsToTarget: setMonthsToTarget,
    funnel: funnel,
    setFunnel: setFunnel,
    calc: funnelCalc
  })), isVisible("taxstrategy") && /*#__PURE__*/React.createElement("div", {id:"sec-taxstrategy"}, sectionIntro("taxstrategy"), /*#__PURE__*/React.createElement(TaxStrategyTab, {
    color: d.color,
    cur: cur,
    filingStatus: filingStatus,
    setFilingStatus: setFilingStatus,
    numDependents: numDependents,
    setNumDependents: setNumDependents,
    entityType: entityType,
    setEntityType: setEntityType,
    sCorpSalaryInput: sCorpSalaryInput,
    setSCorpSalaryInput: setSCorpSalaryInput,
    sessionRate: rate,
    payrollSvcCost: payrollSvcCost,
    setPayrollSvcCost: setPayrollSvcCost,
    corpReturnCost: corpReturnCost,
    setCorpReturnCost: setCorpReturnCost,
    statementOfInfoCost: statementOfInfoCost,
    setStatementOfInfoCost: setStatementOfInfoCost,
    existingPretaxIRA: existingPretaxIRA,
    setExistingPretaxIRA: setExistingPretaxIRA,
    expYrBase: expYrBase,
    job2Yr: job2Yr,
    taxAge: taxAge,
    setTaxAge: setTaxAge,
    retireAge: retireAge,
    setRetireAge: setRetireAge,
    investReturn: investReturn,
    setInvestReturn: setInvestReturn,
    strategy: taxStrategy,
    strategySoleProp: taxStrategySoleProp,
    strategySCorp: taxStrategySCorp
  })), isVisible("residency") && /*#__PURE__*/React.createElement("div", {id:"sec-residency"}, /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sub-eyebrow"
  }, "Still your tax strategy \u2014 one more lever"), /*#__PURE__*/React.createElement("h2", null, "If you practiced somewhere else"), /*#__PURE__*/React.createElement("p", null, "Same practice revenue and running costs (", fmt(cur.grossYr), "/yr gross, ", fmt(expYr), "/yr expenses), estimated as a self-employed therapist based in each location instead. Each card lists exactly what's counted.")), /*#__PURE__*/React.createElement("div", {
    className: "residency-grid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat",
    style: {
      borderColor: d.color
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "California, USA"), /*#__PURE__*/React.createElement("div", {
    className: "stat-sub"
  }, "gross ", fmt(cur.grossYr), "/yr"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value",
    style: {
      color: d.color
    }
  }, fmt(cur.netYr)), /*#__PURE__*/React.createElement("div", {
    className: "stat-sub"
  }, "net / year \u00B7 current setup"), /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, fmt(cur.totalTax), " total tax"), residBreakdown(cur.grossYr, cur.totalTax, cur.netYr, d.color, cur.expYr), /*#__PURE__*/React.createElement("div", {
    className: "resid-invest-note"
  }, /*#__PURE__*/React.createElement("b", null, "If you max your Solo 401(k) "), "(see USA Tax Strategy): ", fmt(taxStrategy.solo401k.total), " moves to your investment account, ", fmt(cur.netYr - taxStrategy.solo401k.total + taxStrategy.solo401k.taxSavings), " lands in your bank account \u2014 ", fmt(taxStrategy.solo401k.taxSavings), " of the contribution is tax you'd have paid anyway."), /*#__PURE__*/React.createElement("div", {
    className: "residency-includes"
  }, /*#__PURE__*/React.createElement("b", null, "Includes: "), "federal income tax, self-employment tax, and CA state income tax (progressive to 13.3%), with the same QBI deduction and expense treatment used throughout this tool.")), [{
    key: "nyc",
    label: "New York City, USA",
    net: residency.nyc.netUSD,
    tax: residency.nyc.taxUSD,
    taxNote: "tax (fed + SE + NY + NYC)",
    sub: null,
    includes: "federal income tax, self-employment tax, NY State income tax (9 brackets, 3.9%\u201310.9%), NYC resident tax (3.078%\u20133.876%), and the MCTMT (0.34% on self-employment earnings over $50k). Excludes: NY disability/paid-family-leave employee contribution (small)."
  }, {
    key: "berlin",
    label: "Berlin, Germany",
    net: residency.berlin.netUSD,
    tax: residency.berlin.taxUSD,
    taxNote: "tax + health/care insurance",
    sub: "\u2248\u20AC" + Math.round(residency.berlin.netEUR).toLocaleString(),
    includes: "German 2026 income tax (\u00A732a EStG formula), statutory health + long-term-care insurance (\u224819.6%, capped at \u20AC69,750), and the solidarity surcharge once income tax exceeds its exemption threshold. Assumes Freiberufler (liberal-profession) status \u2014 no trade tax. Excludes: church tax (assumes opted out), a mandatory professional pension fund some healthcare licenses require."
  }, {
    key: "portugal",
    label: "Portugal",
    net: residency.portugal.netUSD,
    tax: residency.portugal.taxUSD,
    taxNote: "tax + social security",
    sub: "\u2248\u20AC" + Math.round(residency.portugal.netEUR).toLocaleString(),
    includes: "2026 IRS (9 brackets, 13.25%\u201348%) applied to 75% of gross revenue (the simplified Categoria B coefficient \u2014 actual expenses aren't separately deducted for tax purposes), the solidarity surcharge above \u20AC80k, and \u224815% independent-worker social security on gross revenue. Excludes: municipal surcharge (0\u20131.5%), and the now-closed NHR/IFICI regimes."
  }, {
    key: "france",
    label: "Bordeaux, France",
    net: residency.france.netUSD,
    tax: residency.france.taxUSD,
    taxNote: "tax + cotisations sociales",
    sub: "\u2248\u20AC" + Math.round(residency.france.netEUR).toLocaleString(),
    includes: "French 2026 bar\u00E8me progressif (0/11/30/41/45%) applied to profit after cotisations sociales, and a \u224840% blended self-employed social-charge rate (URSSAF, retirement, CSG-CRDS) for a profession lib\u00E9rale under d\u00E9claration contr\u00F4l\u00E9e. Excludes: the micro-BNC alternative regime, Madelin-law supplemental deductions, and wealth tax."
  }, {
    key: "uae",
    label: "United Arab Emirates",
    net: residency.uae.netUSD,
    tax: residency.uae.taxUSD,
    taxNote: "corporate tax (0% below AED 1M turnover)",
    sub: "\u2248AED " + Math.round(residency.uae.netAED).toLocaleString(),
    includes: "0% personal income tax (the UAE has none). 0% corporate tax on the first AED 375,000 of profit, 9% above it \u2014 but only once a natural person's business turnover exceeds the AED 1,000,000 registration threshold in a year. No self-employment or social-security tax applies to foreign residents. Excludes: Small Business Relief (can zero out corporate tax below AED 3M turnover through 2026 if elected), VAT, freelance-permit and visa costs."
  }, {
    key: "pittsburgh",
    label: "Pittsburgh, PA (15232)",
    net: residency.pittsburgh.netUSD,
    tax: residency.pittsburgh.taxUSD,
    taxNote: "tax (fed + SE + PA + Pittsburgh EIT + LST)",
    sub: null,
    includes: /*#__PURE__*/React.createElement(React.Fragment, null, "Pennsylvania's flat 3.07% state income tax (no standard deduction, no brackets), Pittsburgh's combined 3% local Earned Income Tax (2% city + 1% school district, per Act 32), and the $52/yr Local Services Tax (occupational privilege tax, split between city and school district). Federal income tax, self-employment tax, and QBI deduction calculated the same way as every other location in this tool. Excludes: PA has no separate business-entity-level tax comparable to CA's, and does not tax retirement income for residents 60+.", /*#__PURE__*/React.createElement("sup", null, "[12]"))
  }, {
    key: "brisbane",
    label: "Brisbane, Australia",
    net: residency.brisbane.netUSD,
    tax: residency.brisbane.taxUSD,
    taxNote: "tax + Medicare levy",
    sub: "\u2248A$" + Math.round(residency.brisbane.netAUD).toLocaleString(),
    includes: "2025\u201326 resident income tax (0/16/30/37/45%), the 2% Medicare levy, and the small business income tax offset (8% of tax, capped at A$1,000). Sole traders use the same brackets as employees \u2014 no separate state income tax anywhere in Australia. Excludes: compulsory superannuation (optional for the self-employed), Medicare Levy Surcharge, GST (a pass-through on client billings, not an income tax)."
  }].map(c => /*#__PURE__*/React.createElement("div", {
    key: c.key,
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, c.label), /*#__PURE__*/React.createElement("div", {
    className: "stat-sub"
  }, "gross ", fmt(cur.grossYr), "/yr"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value"
  }, fmt(c.net)), /*#__PURE__*/React.createElement("div", {
    className: "stat-sub"
  }, "net / year (est.)", c.sub ? " \u00B7 " + c.sub : ""), /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, fmt(c.tax), " ", c.taxNote), residBreakdown(cur.grossYr, c.tax, c.net, "#6F6A5E", cur.expYr), /*#__PURE__*/React.createElement("div", {
    className: c.net - cur.netYr === 0 ? "stat-note" : c.net - cur.netYr > 0 ? "pos" : "neg"
  }, c.net - cur.netYr >= 0 ? "+" : "\u2212", fmt(Math.abs(c.net - cur.netYr)), " vs. California"), /*#__PURE__*/React.createElement("div", {
    className: "residency-includes"
  }, /*#__PURE__*/React.createElement("b", null, "Includes: "), c.includes))), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "Estimates only, not tax or immigration advice. Converts at \u22481 EUR = $1.14 (July 2026), which moves with the market. Assumes the same running costs are portable and unchanged. None of these models account for local licensing to practice therapy, work-visa or right-to-work requirements, or double-taxation treaty mechanics for a U.S. citizen abroad \u2014 talk to a cross-border tax advisor before acting on this.")), /*#__PURE__*/React.createElement("details", {
    className: "card collapsible"
  }, /*#__PURE__*/React.createElement("summary", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "How US retirement strategies interact with each location"), /*#__PURE__*/React.createElement("p", null, "Maxing a Solo 401(k) or IRA (from the USA Tax Strategy tab) still works the same on the ", /*#__PURE__*/React.createElement("i", null, "US"), " side no matter where you live \u2014 as a US citizen, contribution eligibility depends on having US-taxable self-employment income, not on your country of residence.", /*#__PURE__*/React.createElement("sup", null, "[1]"), " What changes by location is whether ", /*#__PURE__*/React.createElement("i", null, "that country"), " respects the account's tax-advantaged status. Click to expand \u2014 directional, not a substitute for a cross-border tax advisor.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "\uD83C\uDDE9\uD83C\uDDEA Berlin, Germany")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "Germany does ", /*#__PURE__*/React.createElement("b", null, "not"), " give a German tax deduction for contributing \u2014 the deduction only reduces your US tax. A 2024 German tax-law reform (effective 2025) means Germany now taxes the ", /*#__PURE__*/React.createElement("b", null, "entire"), " payout (contributions plus growth) of a Traditional 401(k)/IRA when withdrawn by a German tax resident, not just the growth as under the old rule.", /*#__PURE__*/React.createElement("sup", null, "[2]"), " Germany also does ", /*#__PURE__*/React.createElement("b", null, "not"), " honor Roth tax-free status \u2014 it taxes the gain portion of Roth withdrawals as ordinary income.", /*#__PURE__*/React.createElement("sup", null, "[3]"), " A US foreign tax credit can offset double taxation, but the German tax bill on withdrawal is real either way.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "\uD83C\uDDF5\uD83C\uDDF9 Portugal")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "Same pattern: no Portuguese deduction for contributing. On withdrawal, Portugal generally taxes 401(k)/IRA distributions as foreign pension income at your regular progressive IRS rates.", /*#__PURE__*/React.createElement("sup", null, "[4]"), " The old NHR regime used to offer a flat 10% rate on foreign pension income, but NHR closed to new applicants in 2024 \u2014 don't count on it.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "\uD83C\uDDEB\uD83C\uDDF7 Bordeaux, France")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "Follows the general pattern most non-US countries use: no French deduction on the way in, and distributions are generally taxed as income on the way out regardless of Traditional-vs-Roth status \u2014 France doesn't have a domestic concept matching the Roth's after-tax structure, so it doesn't automatically exempt it.", /*#__PURE__*/React.createElement("sup", null, "[5]"))), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "\uD83C\uDDE6\uD83C\uDDEA United Arab Emirates")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, /*#__PURE__*/React.createElement("b", null, "This is the one clean case."), " Since the UAE has no personal income tax at all, there's no foreign tax to conflict with \u2014 your Solo 401(k)/IRA contribution, deferral, and eventual Roth tax-free withdrawal all work exactly as US law intends, with zero UAE-side complication.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "\uD83C\uDDE6\uD83C\uDDFA Brisbane, Australia")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "The ATO treats US 401(k)/IRA accounts as foreign trusts, not as the equivalent of Australian superannuation \u2014 private rulings have specifically rejected classifying them as a \"foreign superannuation fund.\"", /*#__PURE__*/React.createElement("sup", null, "[6]"), " Traditional distributions are taxed at your Australian marginal rate on withdrawal (foreign income tax offset available); Roth withdrawals are generally treated as tax-free in Australia since the contributions were already after-tax.", /*#__PURE__*/React.createElement("sup", null, "[7]"))), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "\uD83C\uDDFA\uD83C\uDDF8 New York City")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "No cross-border issue \u2014 same US federal rules as California. Solo 401(k)/IRA contributions, deductions, and Roth tax-free growth all work exactly as modeled on the USA Tax Strategy tab; state and city taxes don't change how the account itself is taxed.")), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, citeList([
    {n:1, cite:"IRC \u00A7401(c)", url:"https://www.law.cornell.edu/uscode/text/26/401", note:"contributions require US-taxable compensation \u2014 income excluded via the Foreign Earned Income Exclusion (Form 2555) cannot support a contribution."},
    {n:2, cite:"Jahressteuergesetz 2024", url:"https://www.bundesfinanzministerium.de", note:"German Annual Tax Act, effective 2025, reforming taxation of foreign pension plans including US 401(k)/IRA; see also Bundesfinanzhof ruling X R 29/18 (Oct. 28, 2020) on the prior rule."},
    {n:3, cite:"Germany \u2014 Roth treatment", note:"does not recognize the Roth's after-tax contribution structure as tax-exempt; gains are taxed as other income on distribution."},
    {n:4, cite:"Portugal Categoria H", url:"https://www.portaldasfinancas.gov.pt", note:"under general Portuguese IRS rules for foreign pension income; NHR (Non-Habitual Resident) regime closed to new applicants starting 2024."},
    {n:5, cite:"Cross-border retirement-account principle", note:"most countries without a specific Roth-equivalent vehicle tax distributions as ordinary income; confirm current treaty position with a French-qualified advisor."},
    {n:6, cite:"ITAA 1936 \u00A799B", url:"https://www.legislation.gov.au/Details/C2023C00251", note:"US-Australia private rulings on 401(k)/IRA classification under the Superannuation Industry (Supervision) Act; treated instead as foreign trust distributions."},
    {n:7, cite:"Foreign Income Tax Offset (FITO)", url:"https://www.ato.gov.au/individuals-and-families/investments-and-assets/foreign-income", note:"available for Australian tax paid; consult a cross-border advisor for Roth-specific treatment, which is not explicitly legislated."}
  ])), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "None of this is personalized tax advice \u2014 cross-border retirement taxation depends heavily on treaty elections, timing of withdrawals, and whether you keep or renounce US citizenship."))
))), viewMode === "wizard" && /*#__PURE__*/React.createElement("div", {
    className: "wizard-nav"
  }, /*#__PURE__*/React.createElement("button", {
    className: "wizard-btn",
    disabled: wizardStep === 1,
    onClick: () => setWizardStep(s => Math.max(1, s - 1))
  }, "\u2190 Back"), /*#__PURE__*/React.createElement("span", {
    className: "wizard-nav-label"
  }, "Step ", wizardStep, " of ", wizardSteps.length), wizardStep < wizardSteps.length ? /*#__PURE__*/React.createElement("button", {
    className: "wizard-btn primary",
    onClick: () => setWizardStep(s => Math.min(wizardSteps.length, s + 1))
  }, "Continue \u2192") : /*#__PURE__*/React.createElement("button", {
    className: "wizard-btn primary",
    onClick: () => setViewMode("current")
  }, "Done \u2014 see full dashboard \u2192")), /*#__PURE__*/React.createElement("section", {
    className: "card feedback-section"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Found a bug? Have an idea?"), /*#__PURE__*/React.createElement("p", null, "This tool is actively maintained \u2014 tell me what's broken, what's confusing, or what you'd like to see next. Goes straight to my inbox.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-grid",
    style: {
      gridTemplateColumns: "160px 1fr"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field"
  }, /*#__PURE__*/React.createElement("label", null, "Type"), /*#__PURE__*/React.createElement("select", {
    value: fbType,
    onChange: e => setFbType(e.target.value),
    style: {
      width: "100%",
      height: 44,
      border: "1.5px solid #E4D9BE",
      borderRadius: 9,
      background: "#FBF6E9",
      fontFamily: "'Fraunces', serif",
      fontSize: 15,
      fontWeight: 600,
      color: "#26241E",
      padding: "0 10px"
    }
  }, /*#__PURE__*/React.createElement("option", null, "Bug"), /*#__PURE__*/React.createElement("option", null, "Suggestion"), /*#__PURE__*/React.createElement("option", null, "Question"))), /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field"
  }, /*#__PURE__*/React.createElement("label", null, "Your name (optional)"), /*#__PURE__*/React.createElement("input", {
    type: "text",
    value: fbName,
    onChange: e => setFbName(e.target.value),
    placeholder: "So I know who to reply to"
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14
    }
  }, /*#__PURE__*/React.createElement("label", {
    style: {
      fontSize: 11,
      fontWeight: 600,
      color: "var(--muted)",
      display: "block",
      marginBottom: 6
    }
  }, "Message"), /*#__PURE__*/React.createElement("textarea", {
    value: fbMessage,
    onChange: e => setFbMessage(e.target.value),
    rows: 4,
    placeholder: "What happened, what you'd change, or what you're wondering about\u2026",
    style: {
      width: "100%",
      border: "1.5px solid #E4D9BE",
      borderRadius: 9,
      background: "#FBF6E9",
      fontFamily: "inherit",
      fontSize: 14,
      color: "#26241E",
      padding: 12,
      resize: "vertical"
    }
  })), /*#__PURE__*/React.createElement("button", {
    className: "summary-btn summary-btn-primary",
    style: {
      marginTop: 14,
      flexBasis: "auto",
      display: "inline-block",
      padding: "11px 24px"
    },
    onClick: () => {
      if (!fbMessage.trim()) return;
      const subject = encodeURIComponent("[" + fbType + "] Therapy Practice Simulator feedback");
      const bodyLines = [fbName ? "From: " + fbName : null, "Type: " + fbType, "", fbMessage, "", "\u2014\u2014\u2014", "Current setup: $" + rate + "/hr, " + sessions + " sessions/week", buildShareURL()].filter(Boolean);
      const body = encodeURIComponent(bodyLines.join("\n"));
      window.location.href = "mailto:shawn@shawnwalters.com?subject=" + subject + "&body=" + body;
      setFbSent(true);
      setTimeout(() => setFbSent(false), 3000);
    }
  }, fbSent ? "Opening your email app\u2026" : "Send feedback"), /*#__PURE__*/React.createElement("p", {
    className: "pay-note",
    style: {
      marginTop: 10
    }
  }, "Opens your email app with everything filled in, including a link back to your exact setup so I can see what you're seeing. Nothing is sent automatically \u2014 you'll see the draft before it goes anywhere.")), /*#__PURE__*/React.createElement("footer", {
    className: "foot"
  }, /*#__PURE__*/React.createElement("strong", null, "Estimates only — not tax advice."), " 2026 CA single-filer model. Practice income is treated as ", /*#__PURE__*/React.createElement("strong", null, "1099 / self-employed"), ": business expenses are deducted on Schedule\xA0C, self-employment tax (15.3% on 92.35% of net earnings) applies, and the QBI deduction is included with the SSTB phase-out that affects therapists at higher incomes. California has no city or county ", /*#__PURE__*/React.createElement("em", null, "income"), " tax — state tax is identical everywhere in CA. The second job is treated as W-2 wages with employee FICA and CA SDI; its wages share the Social Security wage base with your self-employment income. Federal and CA tax use standard deductions and projected 2026 brackets. Real figures depend on your entity type (sole prop vs. S-corp), retirement contributions, home-office and mileage deductions, quarterly estimated payments, and actual filing status — talk to a CPA before making decisions on these numbers."), /*#__PURE__*/React.createElement("div", {
    className: "sitefoot"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sitefoot-mark"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sitenav-mono"
  }, "CA"), /*#__PURE__*/React.createElement("span", {
    className: "sitenav-wordmark"
  }, "Therapy Practice")), /*#__PURE__*/React.createElement("nav", {
    className: "sitefoot-links",
    "aria-label": "Site, footer"
  }, [["#sim", "Simulator"], ["#grow", "Grow Your Practice"], ["rates.html", "Field Notes"], ["https://cavatello.github.io/therapist-tycoon/tycoon.html", "Tycoon"]].map(([href, t]) => /*#__PURE__*/React.createElement("a", {
    key: href,
    href: href
  }, t))), /*#__PURE__*/React.createElement("div", {
    className: "sitefoot-meta"
  }, "Last updated: July 25, 2026")));
}

// ---------- small components ----------
function Stat({
  label,
  value,
  note,
  sub,
  big,
  accent,
  neg
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "stat" + (big ? " stat-big" : "")
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, label), /*#__PURE__*/React.createElement("div", {
    className: "stat-value",
    style: big && accent ? {
      color: accent
    } : neg ? {
      color: "#B5483F"
    } : {}
  }, value), sub && /*#__PURE__*/React.createElement("div", {
    className: "stat-sub"
  }, sub), note && /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, note));
}
function RateTip({
  active,
  payload,
  label,
  rate,
  mode
}) {
  if (!active || !payload?.length) return null;
  // Group by rate so net + gross for the same rate sit together
  const byRate = {};
  payload.forEach(p => {
    const [kind, r] = p.dataKey.split("_");
    byRate[r] = byRate[r] || {
      r: +r,
      stroke: p.stroke
    };
    byRate[r][kind] = p.value;
  });
  const rows = Object.values(byRate).sort((a, b) => (b.net ?? b.gross) - (a.net ?? a.gross));
  return /*#__PURE__*/React.createElement("div", {
    className: "tip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tip-head"
  }, label, " sessions / week"), rows.map(row => /*#__PURE__*/React.createElement("div", {
    key: row.r,
    className: "tip-row" + (row.r === rate ? " tip-on" : "")
  }, /*#__PURE__*/React.createElement("span", {
    className: "tip-dot",
    style: {
      background: row.stroke
    }
  }), /*#__PURE__*/React.createElement("span", {
    className: "tip-name"
  }, "$", row.r, "/hr"), /*#__PURE__*/React.createElement("span", {
    className: "tip-val"
  }, mode === "both" ? `${fmt(row.net)} · ${fmt(row.gross)}g` : fmt(row.net ?? row.gross)))), mode === "both" && /*#__PURE__*/React.createElement("div", {
    className: "tip-foot"
  }, "net · gross"));
}
function MarginTip({
  active,
  payload
}) {
  if (!active || !payload?.length) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "tip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tip-head"
  }, "Adding session ", payload[0].payload.s), /*#__PURE__*/React.createElement("div", {
    className: "tip-row"
  }, /*#__PURE__*/React.createElement("span", {
    className: "tip-name"
  }, "extra net / yr"), /*#__PURE__*/React.createElement("span", {
    className: "tip-val"
  }, fmt(payload[0].value))));
}
function EffTip({
  active,
  payload,
  label
}) {
  if (!active || !payload?.length) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "tip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tip-head"
  }, label, " sessions / week"), /*#__PURE__*/React.createElement("div", {
    className: "tip-row"
  }, /*#__PURE__*/React.createElement("span", {
    className: "tip-name"
  }, "kept after tax"), /*#__PURE__*/React.createElement("span", {
    className: "tip-val"
  }, payload[0].value, "%")));
}

// ----------------------------------------------------------------------------

// ---------- EXPENSES TAB ----------
function TaxStrategyTab({
  color,
  cur,
  filingStatus,
  setFilingStatus,
  numDependents,
  setNumDependents,
  entityType,
  setEntityType,
  sCorpSalaryInput,
  setSCorpSalaryInput,
  sessionRate,
  payrollSvcCost,
  setPayrollSvcCost,
  corpReturnCost,
  setCorpReturnCost,
  statementOfInfoCost,
  setStatementOfInfoCost,
  existingPretaxIRA,
  setExistingPretaxIRA,
  expYrBase,
  job2Yr,
  taxAge,
  setTaxAge,
  retireAge,
  setRetireAge,
  investReturn,
  setInvestReturn,
  strategy,
  strategySoleProp,
  strategySCorp
}) {
  const fmt0 = n => (n < 0 ? "\u2212$" : "$") + Math.abs(Math.round(n)).toLocaleString();
  const pct1 = n => (n * 100).toFixed(1) + "%";
  const inputField = (label, value, onChange, min, max) => /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field",
    key: label
  }, /*#__PURE__*/React.createElement("label", null, label), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: min,
    max: max,
    value: value,
    onChange: e => onChange(+e.target.value || 0)
  }));

  const introSection = /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "USA tax strategy"), /*#__PURE__*/React.createElement("p", null, "Retirement accounts are the main legal lever a self-employed therapist has to reduce this year's taxable income while building long-term savings. This tab simulates each option against your actual practice income \u2014 estimates only, not personalized advice.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-grid"
  }, inputField("Your current age", taxAge, setTaxAge, 18, 80), inputField("Planned retirement age", retireAge, setRetireAge, 40, 80), inputField("Expected annual return %", investReturn, setInvestReturn, 0, 15)));

  const taxProfileSection = /*#__PURE__*/React.createElement("section", {
    className: "job2 decision-impact"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-head"
  }, /*#__PURE__*/React.createElement("div", {
    className: "job2-title"
  }, /*#__PURE__*/React.createElement("h3", null, "Tax profile"), /*#__PURE__*/React.createElement("span", {
    className: "job2-tag"
  }, "filing status drives your federal + CA brackets below")), null), /*#__PURE__*/React.createElement("div", {
    className: "residency-toggle",
    style: {
      marginTop: "14px"
    }
  }, [["single", "Single"], ["mfj", "Married filing jointly"], ["mfj_dependents", "Married + dependents"], ["hoh", "Head of household"]].map(([k, lbl]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    className: "pill" + (filingStatus === k ? " pill-on" : ""),
    style: filingStatus === k ? {
      background: color,
      borderColor: color
    } : {},
    onClick: () => setFilingStatus(k)
  }, lbl))), filingStatus === "mfj_dependents" && /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-grid",
    style: {
      gridTemplateColumns: "220px",
      marginTop: "14px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field"
  }, /*#__PURE__*/React.createElement("label", null, "Number of dependent children"), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    max: 10,
    value: numDependents,
    onChange: e => setNumDependents(+e.target.value || 0)
  }))));
  const statsRow = /*#__PURE__*/React.createElement("section", {
    className: "stats"
  }, /*#__PURE__*/React.createElement(Stat, {
    label: "Net self-employment earnings",
    value: fmt0(strategy.netSEEarnings),
    note: "after half of self-employment tax"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Your marginal tax rate",
    value: pct1(strategy.marginalRate),
    note: "fed + CA + SE, on the next dollar"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Years to retirement",
    value: strategy.yearsToRetire,
    note: `at ${retireAge}, assuming ${investReturn}%/yr growth`
  }));

  const strategyCard = (title, tag, body, badge) => /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel",
    key: title
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, title), badge && /*#__PURE__*/React.createElement("span", {
    className: "funnel-channel-value",
    style: {
      color: color
    }
  }, badge)), /*#__PURE__*/React.createElement("p", {
    className: "pay-note",
    style: {
      marginTop: 0
    }
  }, tag), body);

  const traditionalBody = /*#__PURE__*/React.createElement("div", {
    className: "funnel-mini-stats",
    style: {
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("div", null, "Contribution limit ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.traditionalIra.cap))), /*#__PURE__*/React.createElement("div", null, "Deductible this year ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.traditionalIra.deductibleAmount), " (", Math.round(strategy.traditionalIra.deductPct * 100), "%)")), /*#__PURE__*/React.createElement("div", {
    className: "pos"
  }, "Tax savings ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.traditionalIra.taxSavings))), /*#__PURE__*/React.createElement("div", null, "Future value ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.traditionalIra.futureValue))));

  const rothBody = /*#__PURE__*/React.createElement("div", {
    className: "funnel-mini-stats",
    style: {
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("div", null, "Contribution limit ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.rothIra.cap))), /*#__PURE__*/React.createElement("div", null, "Eligible this year ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.rothIra.eligibleAmount), " (", Math.round(strategy.rothIra.eligiblePct * 100), "%)")), /*#__PURE__*/React.createElement("div", null, "Tax savings now ", /*#__PURE__*/React.createElement("b", null, "$0 (after-tax)")), /*#__PURE__*/React.createElement("div", {
    className: "pos"
  }, "Future value, tax-free ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.rothIra.futureValue))));

  const backdoorBody = /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-grid",
    style: {
      gridTemplateColumns: "260px",
      margin: "8px 0"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field"
  }, /*#__PURE__*/React.createElement("label", null, "Existing pre-tax IRA/SEP/SIMPLE balance"), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 1000,
    value: existingPretaxIRA,
    onChange: e => setExistingPretaxIRA(+e.target.value || 0)
  }))), /*#__PURE__*/React.createElement("div", {
    className: "funnel-mini-stats"
  }, /*#__PURE__*/React.createElement("div", null, "Contribute (nondeductible) ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.backdoorRoth.contribution))), /*#__PURE__*/React.createElement("div", null, "Captures phased-out Roth room ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.backdoorRoth.phasedOutRoom))), /*#__PURE__*/React.createElement("div", {
    className: strategy.backdoorRoth.taxableFraction > 0 ? "neg" : "pos"
  }, "Taxable on conversion (pro-rata) ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.backdoorRoth.taxableOnConversion), " (", (strategy.backdoorRoth.taxableFraction * 100).toFixed(0), "%)")), /*#__PURE__*/React.createElement("div", null, "Conversion tax owed ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.backdoorRoth.conversionTax))), /*#__PURE__*/React.createElement("div", {
    className: "pos"
  }, "Future value, tax-free ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.backdoorRoth.futureValue)))));

  const solo401kBody = /*#__PURE__*/React.createElement("div", {
    className: "funnel-mini-stats",
    style: {
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("div", null, "Employee deferral ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.solo401k.employeeContrib))), /*#__PURE__*/React.createElement("div", null, "Employer profit-share (", strategy.solo401k.employerPctLabel, " of ", strategy.solo401k.employerBasis.replace(/^\d+% of /, ""), ") ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.solo401k.employerContrib))), /*#__PURE__*/React.createElement("div", null, "Combined total ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.solo401k.total))), /*#__PURE__*/React.createElement("div", {
    className: "pos"
  }, "Tax savings ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.solo401k.taxSavings))), /*#__PURE__*/React.createElement("div", null, "Future value ", /*#__PURE__*/React.createElement("b", null, fmt0(strategy.solo401k.futureValue))));

  const strategiesSection = /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Your options, simulated")), strategyCard("Solo 401(k)", "You wear two hats: as \u201Cemployee\u201D you can defer income directly from pay, and as \u201Cemployer\u201D your practice can contribute up to 20% of net self-employment earnings on top \u2014 both reduce this year's taxable income, and both grow tax-deferred until withdrawal. Usually the largest contribution room available to a solo owner, and the one to max first.", solo401kBody, "Highest capacity"), strategyCard("Traditional IRA", "A separate, simpler account funded with pre-tax dollars (if your income is under the deduction phase-out) or after-tax dollars (if over it \u2014 still useful as a \u201Cbackdoor Roth\u201D building block). Grows tax-deferred; withdrawals in retirement are taxed as ordinary income. Because you're an active participant in a Solo 401(k), the deduction phases out at a lower income than someone with no workplace plan.", traditionalBody, strategy.traditionalIra.deductPct <= 0 ? "Fully phased out \u2014 nondeductible" : strategy.traditionalIra.deductPct < 1 ? "Partially phased out" : "Fully deductible"), strategyCard("Roth IRA", "Funded with after-tax dollars \u2014 no deduction today \u2014 but grows completely tax-free, and qualified withdrawals in retirement owe nothing at all. The direct contribution phases out at higher income levels than you might expect; above the top of that range, a \u201Cbackdoor Roth\u201D (nondeductible Traditional IRA contribution, immediately converted) is the common workaround.", rothBody, strategy.rothIra.eligiblePct < 1 ? "Phased out \u2014 consider backdoor" : "Fully eligible"), strategyCard("Backdoor Roth IRA", "If you're phased out of a direct Roth contribution, you can still get Roth-equivalent tax-free growth: contribute to a Traditional IRA without claiming a deduction (no income limit on nondeductible contributions), then convert it to Roth right away (no income limit on conversions either, since 2010). The catch is the IRC \u00A7408(d)(2) \u201Cpro-rata rule\u201D: if you hold "+"any"+" other pre-tax Traditional/SEP/SIMPLE IRA money, the conversion isn't treated as 100% basis \u2014 it's taxed in proportion to your "+"total"+" IRA balance, pre-tax and after-tax combined. Enter your existing pre-tax IRA balance below to see the real tax cost.", backdoorBody, strategy.backdoorRoth.taxableFraction > 0.05 ? "Pro-rata rule applies \u2014 partially taxable" : "Clean \u2014 minimal pro-rata drag"), strategyCard("SIMPLE IRA", "Designed for small businesses with employees: it requires the owner to make matching or fixed contributions on behalf of every eligible employee, in exchange for lower administrative cost than a 401(k). With no employees on your payroll, it offers no advantage over a Solo 401(k) \u2014 which has meaningfully higher contribution limits and no matching obligation to anyone else. Revisit this only if you hire staff.", null, "Not applicable \u2014 solo practice"));

  const compareRows = [{
    label: "Solo 401(k)",
    contrib: strategy.solo401k.total,
    savings: strategy.solo401k.taxSavings,
    fv: strategy.solo401k.futureValue
  }, {
    label: "Traditional IRA",
    contrib: strategy.traditionalIra.cap,
    savings: strategy.traditionalIra.taxSavings,
    fv: strategy.traditionalIra.futureValue
  }, {
    label: "Roth IRA",
    contrib: strategy.rothIra.eligibleAmount,
    savings: 0,
    fv: strategy.rothIra.futureValue
  }].map(row => /*#__PURE__*/React.createElement("tr", {
    key: row.label
  }, /*#__PURE__*/React.createElement("td", null, row.label), /*#__PURE__*/React.createElement("td", {
    className: "num-head strong"
  }, fmt0(row.contrib)), /*#__PURE__*/React.createElement("td", {
    className: "num-head strong"
  }, fmt0(row.savings)), /*#__PURE__*/React.createElement("td", {
    className: "num-head muted"
  }, fmt0(row.fv))));

  const totalMaxSavings = strategy.solo401k.taxSavings + strategy.traditionalIra.taxSavings;
  const totalMaxContrib = strategy.solo401k.total + (strategy.traditionalIra.deductPct > 0 ? 0 : strategy.rothIra.eligibleAmount);
  const compareSection = /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Side by side")), /*#__PURE__*/React.createElement("div", {
    className: "table-wrap"
  }, /*#__PURE__*/React.createElement("table", null, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Strategy"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, "Contribution this year"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, "Immediate tax savings"), /*#__PURE__*/React.createElement("th", {
    className: "num-head"
  }, retireAge > taxAge ? `Value at ${retireAge}` : "Value at retirement"))), /*#__PURE__*/React.createElement("tbody", null, compareRows))));


  const recommendation = strategy.solo401k.total >= strategy.netSEEarnings * 0.15 ? `With ${fmt0(strategy.netSEEarnings)} in net self-employment earnings and a ${pct1(strategy.marginalRate)} marginal rate, maxing the Solo 401(k) employee deferral first (${fmt0(strategy.solo401k.employeeContrib)}) gives you the single biggest deduction available \u2014 it comes off your taxable income regardless of income level. Layering the employer profit-share on top (${fmt0(strategy.solo401k.employerContrib)}) brings total tax savings to roughly ${fmt0(strategy.solo401k.taxSavings)} this year alone.` : `Your practice income leaves room to contribute more than the Solo 401(k) alone captures \u2014 consider using ${strategy.traditionalIra.deductPct > 0 ? "a Traditional IRA for the additional deduction" : "a Roth IRA, since your income is past the Traditional deduction phase-out"} to extend your tax-advantaged savings further.`;
  const rothNote = strategy.rothIra.eligiblePct < 1 ? ` Since your income phases out ${strategy.rothIra.eligiblePct <= 0 ? "all of" : "part of"} direct Roth IRA eligibility, a backdoor Roth (nondeductible Traditional IRA \u2192 immediate conversion) is worth asking your CPA about \u2014 it's not modeled here as a separate number since it uses the same contribution room as the Traditional IRA above.` : " You're still under the Roth IRA income limit, so a direct contribution works without any extra steps.";

const seEducation = (function () {
    const seBase92 = cur.schedC * 0.9235;
    const underCap = Math.min(seBase92, SS_WAGE_BASE);
    const overCap = Math.max(0, seBase92 - SS_WAGE_BASE);
    const ssPortion = underCap * 0.124;
    const medicarePortion = seBase92 * 0.029;
    const addlMedFlag = cur.addlMed > 0;
    return /*#__PURE__*/React.createElement("details", {
      className: "card collapsible"
    }, /*#__PURE__*/React.createElement("summary", {
      className: "card-head"
    }, /*#__PURE__*/React.createElement("h2", null, "How self-employment tax actually works"), /*#__PURE__*/React.createElement("p", null, "Before strategies for reducing it, here's the mechanism itself \u2014 most of what feels confusing about SE tax is really just four separate moving pieces stacked on top of each other. Click to expand.")), /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel"
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel-head"
    }, /*#__PURE__*/React.createElement("h3", null, "1. Why 92.35%, not 100%")), /*#__PURE__*/React.createElement("p", {
      style: {
        margin: "6px 0 0",
        fontSize: 14,
        lineHeight: 1.6
      }
    }, "A W-2 employee's FICA tax is only charged on their wages \u2014 the employer's matching half isn't treated as the employee's income at all. Since you're both employer and employee as a sole proprietor, the SE tax formula approximates that same exclusion by first multiplying your net profit by 92.35% (i.e., knocking off 7.65%, which mirrors the employer-side FICA rate) before applying the SE tax rate to what's left.", /*#__PURE__*/React.createElement("sup", null, "[1]"))), /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel"
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel-head"
    }, /*#__PURE__*/React.createElement("h3", null, "2. Two different rates, stacked")), /*#__PURE__*/React.createElement("p", {
      style: {
        margin: "6px 0 10px",
        fontSize: 14,
        lineHeight: 1.6
      }
    }, "The 15.3% headline rate is actually two separate taxes with different rules: 12.4% for Social Security, and 2.9% for Medicare.", /*#__PURE__*/React.createElement("sup", null, "[2]"), " Only the Social Security portion has a cap \u2014 the Medicare portion applies to every dollar, no matter how much you earn."), /*#__PURE__*/React.createElement("div", {
      className: "funnel-mini-stats"
    }, /*#__PURE__*/React.createElement("div", null, "92.35% of net profit ", /*#__PURE__*/React.createElement("b", null, fmt0(seBase92))), /*#__PURE__*/React.createElement("div", null, "Social Security (12.4%, capped at ", fmt0(SS_WAGE_BASE), ") ", /*#__PURE__*/React.createElement("b", null, fmt0(ssPortion))), /*#__PURE__*/React.createElement("div", null, "Medicare (2.9%, uncapped) ", /*#__PURE__*/React.createElement("b", null, fmt0(medicarePortion))), overCap > 0 && /*#__PURE__*/React.createElement("div", {
      className: "pos"
    }, fmt0(overCap), " of your earnings owe ", /*#__PURE__*/React.createElement("b", null, "no"), " Social Security tax \u2014 already over the cap"))), /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel"
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel-head"
    }, /*#__PURE__*/React.createElement("h3", null, "3. The Additional Medicare Tax (a separate 0.9%)")), /*#__PURE__*/React.createElement("p", {
      style: {
        margin: "6px 0 0",
        fontSize: 14,
        lineHeight: 1.6
      }
    }, "Above $200,000 in combined wages and self-employment earnings (single filer), an extra 0.9% Medicare surtax kicks in \u2014 added by the ACA in 2013, it's not part of the traditional 15.3% rate and isn't split with an employer even if you have one.", /*#__PURE__*/React.createElement("sup", null, "[3]"), addlMedFlag ? " Based on your current numbers, this applies to you \u2014 it's already included in your total tax." : " Your current numbers are under that threshold, so it doesn't apply yet.")), /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel"
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel-head"
    }, /*#__PURE__*/React.createElement("h3", null, "4. The half-SE-tax deduction")), /*#__PURE__*/React.createElement("p", {
      style: {
        margin: "6px 0 0",
        fontSize: 14,
        lineHeight: 1.6
      }
    }, "You get to deduct half of your SE tax from your income (not your tax bill directly \u2014 from the income the rest of your taxes are calculated on).", /*#__PURE__*/React.createElement("sup", null, "[4]"), " This isn't a special break; it's the same logic as point 1 \u2014 the \u201Cemployer half\u201D of the tax was never supposed to be taxed as your personal income twice, so this deduction backs it back out. It reduces your income tax bill, but does ", /*#__PURE__*/React.createElement("b", null, "not"), " reduce the SE tax itself.")), /*#__PURE__*/React.createElement("p", {
      className: "pay-note"
    }, citeList([{
      n: 1,
      cite: "IRC \u00A71402(a)(12)",
      url: "https://www.law.cornell.edu/uscode/text/26/1402",
      note: "the 92.35% factor (100% \u2212 7.65%) approximates excluding the employer-equivalent share from the SE tax base."
    }, {
      n: 2,
      cite: "IRC \u00A71401(a) and \u00A71401(b)",
      url: "https://www.law.cornell.edu/uscode/text/26/1401",
      note: "12.4% OASDI and 2.9% Medicare (HI)."
    }, {
      n: 3,
      cite: "IRC \u00A71401(b)(2)",
      url: "https://www.law.cornell.edu/uscode/text/26/1401",
      note: "added by the Affordable Care Act (2010), effective 2013; 0.9% on combined wages/SE income above $200,000 single / $250,000 MFJ (not indexed for inflation)."
    }, {
      n: 4,
      cite: "IRC \u00A7164(f)",
      url: "https://www.law.cornell.edu/uscode/text/26/164",
      note: "deduction for one-half of self-employment tax, taken as an adjustment to income on Schedule 1, not an itemized deduction."
    }])));
  })();
  const scorpGrossBasis = cur.grossTherYr + (cur.otherIncomeYr || 0);
  const scorpExpBasis = expYrBase + cur.bizFee;
  const soleFullYear = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "sole_prop", 0);
  const sCorpFullYear = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "s_corp", sCorpSalaryInput);
  const runCostTotal = (payrollSvcCost || 0) + (corpReturnCost || 0) + (statementOfInfoCost || 0);
  const structureRows = [{
    grp: "The tax side \u2014 this year"
  }, {
    label: "Net take-home",
    hint: "After every tax and the CA entity fee",
    sole: soleFullYear.net,
    scorp: sCorpFullYear.net,
    big: true
  }, {
    label: "Total tax",
    hint: "Federal + CA + payroll, all in",
    sole: soleFullYear.totalTax,
    scorp: sCorpFullYear.totalTax,
    lowerBetter: true
  }, {
    label: "Self-employment + payroll tax",
    hint: "SE tax plus FICA on any salary, employer half included \u2014 the piece an S-corp split targets",
    sole: soleFullYear.seTax + soleFullYear.ssW2 + soleFullYear.medW2 + soleFullYear.employerPayrollTax,
    scorp: sCorpFullYear.seTax + sCorpFullYear.ssW2 + sCorpFullYear.medW2 + sCorpFullYear.employerPayrollTax,
    lowerBetter: true
  }, {
    label: "CA entity fee",
    hint: "$800 minimum franchise tax, corporations only",
    sole: soleFullYear.caEntityTax,
    scorp: sCorpFullYear.caEntityTax,
    lowerBetter: true
  }, {
    grp: "Running the corporation \u2014 what it costs to operate"
  }, {
    label: "Payroll service",
    hint: "Filing your own W-2 and the quarterly returns. Zero until you enter a figure above.",
    sole: 0,
    scorp: payrollSvcCost || 0,
    lowerBetter: true
  }, {
    label: "Corporate return prep",
    hint: "Form 1120-S and CA Form 100S \u2014 a return a sole proprietor does not file at all",
    sole: 0,
    scorp: corpReturnCost || 0,
    lowerBetter: true
  }, {
    label: "Statement of Information",
    hint: "$25 a year to the CA Secretary of State, corporations only",
    sole: 0,
    scorp: statementOfInfoCost || 0,
    lowerBetter: true
  }, {
    label: "Net take-home after running costs",
    hint: runCostTotal > 0
      ? "The figure that actually reaches you, once the paperwork is paid for"
      : "Same as above until you enter your running costs \u2014 so this currently flatters the corporation",
    sole: soleFullYear.net,
    scorp: sCorpFullYear.net - runCostTotal,
    big: true
  }, {
    grp: "Retirement room it unlocks"
  }, {
    label: "Solo 401(k) \u2014 total contribution",
    hint: "20% of SE earnings vs. 25% of W-2 salary",
    sole: strategySoleProp.solo401k.total,
    scorp: strategySCorp.solo401k.total
  }, {
    label: "Solo 401(k) \u2014 immediate tax savings",
    sole: strategySoleProp.solo401k.taxSavings,
    scorp: strategySCorp.solo401k.taxSavings
  }, {
    label: "Traditional IRA \u2014 deductible amount",
    sole: strategySoleProp.traditionalIra.deductibleAmount,
    scorp: strategySCorp.traditionalIra.deductibleAmount
  }, {
    label: "Roth IRA \u2014 eligible amount",
    sole: strategySoleProp.rothIra.eligibleAmount,
    scorp: strategySCorp.rothIra.eligibleAmount
  }, {
    label: "Backdoor Roth \u2014 taxable on conversion",
    hint: "Lower is better here",
    sole: strategySoleProp.backdoorRoth.taxableOnConversion,
    scorp: strategySCorp.backdoorRoth.taxableOnConversion,
    lowerBetter: true
  }];
  const structureColHead = (val, title, sub) => /*#__PURE__*/React.createElement("th", {
    className: "struct-col" + (entityType === val ? " struct-col-on" : ""),
    scope: "col"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "struct-colbtn",
    "aria-pressed": entityType === val,
    onClick: () => setEntityType(val)
  }, /*#__PURE__*/React.createElement("span", {
    className: "struct-coltitle"
  }, title), /*#__PURE__*/React.createElement("span", {
    className: "struct-colsub"
  }, sub), /*#__PURE__*/React.createElement("span", {
    className: "struct-colpick"
  }, entityType === val ? "\u2713 planning as this" : "Plan as this")));
  const structureBody = structureRows.map(r => r.grp ? /*#__PURE__*/React.createElement("tr", {
    key: r.grp,
    className: "struct-grp"
  }, /*#__PURE__*/React.createElement("td", {
    colSpan: 4
  }, r.grp)) : /*#__PURE__*/React.createElement("tr", {
    key: r.label,
    className: r.big ? "struct-big" : ""
  }, /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
    className: "struct-lbl"
  }, r.label), r.hint && /*#__PURE__*/React.createElement("span", {
    className: "struct-hint"
  }, r.hint)), /*#__PURE__*/React.createElement("td", {
    className: "num-head" + (entityType === "sole_prop" ? " struct-cell-on" : "")
  }, fmt0(r.sole)), /*#__PURE__*/React.createElement("td", {
    className: "num-head" + (entityType === "s_corp" ? " struct-cell-on" : "")
  }, fmt0(r.scorp)), /*#__PURE__*/React.createElement("td", {
    className: "num-head " + (r.scorp - r.sole === 0 ? "" : (r.lowerBetter ? r.scorp < r.sole : r.scorp > r.sole) ? "pos" : "neg")
  }, r.scorp - r.sole === 0 ? "\u2014" : (r.scorp - r.sole > 0 ? "+" : "\u2212") + fmt0(Math.abs(r.scorp - r.sole)))));
  const entityCompareSection = /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Both structures, side by side"), /*#__PURE__*/React.createElement("p", null, "Tax and retirement for Sole Proprietorship and a Professional Corp with an S-corp election, always both, on the same income. Picking one only highlights a column \u2014 the other stays visible so you can see what the choice costs or gains. The S-corp salary above drives the right-hand column.")), /*#__PURE__*/React.createElement("div", {
    className: "table-wrap"
  }, /*#__PURE__*/React.createElement("table", {
    className: "struct-table"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", {
    scope: "col"
  }, ""), structureColHead("sole_prop", "Sole Proprietorship", "no payroll, no entity fee"), structureColHead("s_corp", "Professional Corp", "S-corp election"), /*#__PURE__*/React.createElement("th", {
    className: "num-head",
    scope: "col"
  }, "Difference"))), /*#__PURE__*/React.createElement("tbody", null, structureBody))), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "\u201CDifference\u201D is the Professional Corp column measured against Sole Proprietorship \u2014 green where the corp is ahead, red where it costs more. Solo 401(k) room is computed differently by entity (20% of net self-employment earnings vs. 25% of W-2 salary), which is why those two rows can diverge before any SE-tax saving is counted."))
  const entityToggle = /*#__PURE__*/React.createElement("div", {
    className: "residency-toggle",
    style: {
      marginBottom: 4
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "pill" + (entityType === "sole_prop" ? " pill-on" : ""),
    style: entityType === "sole_prop" ? {
      background: color,
      borderColor: color
    } : {},
    onClick: () => setEntityType("sole_prop")
  }, "Sole Proprietorship"), /*#__PURE__*/React.createElement("button", {
    className: "pill" + (entityType === "s_corp" ? " pill-on" : ""),
    style: entityType === "s_corp" ? {
      background: color,
      borderColor: color
    } : {},
    onClick: () => setEntityType("s_corp")
  }, "Professional Corp (S-corp election)"));
  const salaryInputRow = /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-grid",
    style: {
      gridTemplateColumns: "260px",
      margin: "10px 0 16px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field"
  }, /*#__PURE__*/React.createElement("label", null, "S-corp salary (W-2 wages)"), /*#__PURE__*/React.createElement("span", {
    className: "funnel-input-hint"
  }, "Drives the Professional Corp column on both comparisons below \u2014 editable whichever structure you've picked."), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    step: 1000,
    value: sCorpSalaryInput,
    onChange: e => setSCorpSalaryInput(+e.target.value || 0)
  })));
const netDiff = sCorpFullYear.net - soleFullYear.net;
  // An S-corp paying $0 salary is not a lawful option, so it must never be "recommended".
  const salaryUnset = !(sCorpSalaryInput > 0);
  const recNetProfit = Math.max(1, scorpGrossBasis - scorpExpBasis);
  const recMinSalary = Math.ceil(recNetProfit * 0.5 / 1000) * 1000;
  const salaryBand = salaryBandFor(sCorpSalaryInput, recNetProfit);
  const salaryGuidance = /*#__PURE__*/React.createElement("div", {
    className: "salguide"
  },
    /*#__PURE__*/React.createElement("h4", null, "How much salary is defensible?"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "There is no percentage in the law. The IRS asks what your work is actually worth — the “50% of profit” figure everyone repeats is a practitioner convention, not a safe harbour you can point at. Below is where your current salary sits, and what each position costs you."),
    salaryBand && /*#__PURE__*/React.createElement("div", {className: "salguide-now"},
      /*#__PURE__*/React.createElement("div", {className: "salguide-meter"},
        SALARY_BANDS.slice().reverse().map(b => /*#__PURE__*/React.createElement("i", {
          key: b.key,
          className: "salguide-seg" + (b.key === salaryBand.key ? " on" : ""),
          style: {background: b.color}
        }))),
      /*#__PURE__*/React.createElement("div", {className: "salguide-verdict"},
        /*#__PURE__*/React.createElement("span", {
          className: "salguide-badge",
          style: {background: salaryBand.color}
        }, salaryBand.label),
        /*#__PURE__*/React.createElement("b", null,
          sCorpSalaryInput > 0
            ? fmt0(sCorpSalaryInput) + " is " + Math.floor(salaryBand.ratio * 100) + "% of your " + fmt0(recNetProfit) + " net profit"
            : "No salary set — nothing below is a real option yet")),
      /*#__PURE__*/React.createElement("p", {className: "salguide-what"}, salaryBand.what),
      /*#__PURE__*/React.createElement("p", {className: "salguide-cost"}, salaryBand.cost)),
    /*#__PURE__*/React.createElement("div", {className: "salguide-scale"},
      SALARY_BANDS.slice().reverse().map(b => {
        const lo = Math.round(b.min * 100);
        const hi = b.key === "none" ? null : Math.round(SALARY_BANDS[SALARY_BANDS.indexOf(b) - 1].min * 100) - 1;
        const range = b.key === "zero" ? "0%" : b.key === "none" ? "100%" : lo + "–" + hi + "%";
        return /*#__PURE__*/React.createElement("div", {
          key: b.key,
          className: "salguide-row" + (salaryBand && b.key === salaryBand.key ? " on" : "")
        },
          /*#__PURE__*/React.createElement("span", {className: "salguide-range", style: {color: b.color}}, range),
          /*#__PURE__*/React.createElement("span", {className: "salguide-name"}, b.label),
          /*#__PURE__*/React.createElement("span", {className: "salguide-amt"},
            !(recNetProfit > 0) || b.key === "zero" ? "—"
              : b.key === "high" ? "under " + fmt0(Math.round(recNetProfit * 0.35))
              : fmt0(Math.round(recNetProfit * b.min)) + "+"));
      })),
    /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
      "Bands are how accountants commonly talk about this, not law. The two ends are the only ones that are certain: pay 100% as salary and there is nothing to challenge, pay 0% and there is no defence."),
    /*#__PURE__*/React.createElement("details", {className: "salguide-deep"},
      /*#__PURE__*/React.createElement("summary", null, "What the IRS actually weighs, and what happened to someone who got it wrong"),
      /*#__PURE__*/React.createElement("p", null,
        "A corporate officer who performs services is a statutory employee — that is in the statute itself, ",
        extLink("https://www.law.cornell.edu/uscode/text/26/3121", "26 U.S.C. §3121(d)(1)"),
        ", and the regulation ", extLink("https://www.law.cornell.edu/cfr/text/26/31.3121(d)-1", "26 CFR §31.3121(d)-1(b)"),
        ". “I am the owner, not an employee” is not a position available to you."),
      /*#__PURE__*/React.createElement("p", null,
        "The IRS lists the factors it weighs on its ",
        extLink("https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-compensation-and-medical-insurance-issues", "S corporation compensation guidance"),
        " — your training and experience, duties and responsibilities, the time you actually devote, what comparable practices pay for the same work, your history of distributions, and what you pay anyone else. Notice that none of them is a percentage."),
      /*#__PURE__*/React.createElement("p", null,
        "Where a distribution is really wages in disguise, it gets recharacterised as wages. That is the holding of Rev. Rul. 74-44, quoted in ",
        extLink("https://www.irs.gov/pub/irs-wd/03-0026.pdf", "IRS INFO 2003-0026"),
        ", and the plain-language version is IRS fact sheet ",
        extLink("https://www.irs.gov/pub/irs-news/fs-08-25.pdf", "FS-2008-25, Wage Compensation for S Corporation Officers"),
        "."),
      /*#__PURE__*/React.createElement("div", {className: "salguide-case"},
        /*#__PURE__*/React.createElement("b", null, "What this looks like in practice."),
        " In ", extLink("https://ecf.ca8.uscourts.gov/opndir/12/02/111589P.pdf", "David E. Watson, P.C. v. United States"),
        " (8th Cir. 2012, 668 F.3d 1008) an accountant paid himself a ",
        /*#__PURE__*/React.createElement("b", null, "$24,000"), " salary while taking ",
        /*#__PURE__*/React.createElement("b", null, "$203,651"), " in distributions. The court accepted the government's valuation of his services at ",
        /*#__PURE__*/React.createElement("b", null, "$91,044"),
        " and recharacterised the difference as wages — with the back payroll tax, penalties and interest that follow. He was not accused of hiding income. The salary was simply too low for the work."),
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        "This tool is not tax advice. What is reasonable for your practice depends on your hours, your caseload and what comparable clinicians earn — that is a conversation with a CPA, and the figure you agree on is the one to enter above.")));
  const costRow = (label, hint, val, setter, typical) => /*#__PURE__*/React.createElement("div", {
    className: "runcost-row"
  },
    /*#__PURE__*/React.createElement("div", {className: "runcost-lbl"},
      /*#__PURE__*/React.createElement("b", null, label),
      /*#__PURE__*/React.createElement("span", null, hint)),
    /*#__PURE__*/React.createElement("input", {
      type: "number", min: 0, step: 25, value: val,
      onChange: e => setter(Math.max(0, +e.target.value || 0))
    }),
    /*#__PURE__*/React.createElement("button", {
      type: "button", className: "runcost-use",
      onClick: () => setter(typical)
    }, "use " + fmt0(typical)));
  const complianceGuide = /*#__PURE__*/React.createElement("div", {
    className: "compliance"
  },
    /*#__PURE__*/React.createElement("h4", null, "What running a corporation actually requires"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "A sole proprietor files none of the following — practice income goes on Schedule C inside the personal return you already file. Electing S-corp treatment makes you your own employer, and that creates real, recurring paperwork. Every link opens in a new tab."),
    /*#__PURE__*/React.createElement("div", {className: "compliance-cols"},
      /*#__PURE__*/React.createElement("div", {className: "compliance-col"},
        /*#__PURE__*/React.createElement("h5", null, "Federal"),
        /*#__PURE__*/React.createElement("ul", null,
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-941", "Form 941"), " — every quarter. Reports the income tax, Social Security and Medicare withheld from your own wages, plus the employer half."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-940", "Form 940"), " — once a year, federal unemployment tax. Paid by the employer only."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-w-2", "Form W-2"), " and a W-3 — every January, issued by you, to you."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-1120-s", "Form 1120-S"), " plus a Schedule K-1 — the corporation's own tax return, separate from your 1040."))),
      /*#__PURE__*/React.createElement("div", {className: "compliance-col"},
        /*#__PURE__*/React.createElement("h5", null, "California"),
        /*#__PURE__*/React.createElement("ul", null,
          /*#__PURE__*/React.createElement("li", null, extLink("https://edd.ca.gov/en/payroll_taxes/Am_I_Required_to_Register_as_an_Employer/", "Register with the EDD"), " — required once you pay more than $100 in wages in a calendar quarter, within 15 days. Any officer salary trips this immediately."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://edd.ca.gov/en/payroll_taxes/required_filings_and_due_dates/", "DE 9 and DE 9C"), " — every quarter, wage reconciliation and per-employee detail."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.ftb.ca.gov/file/business/types/corporations/s-corporations.html", "Form 100S"), " — the CA S-corp return. 1.5% of net income, with an $800 minimum."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.sos.ca.gov/business-programs/business-entities/forms/corporations-statement-information", "Statement of Information"), " — $25, every year, to the Secretary of State.")))),
    /*#__PURE__*/React.createElement("div", {className: "compliance-goodnews"},
      /*#__PURE__*/React.createElement("b", null, "Two things that are less painful than they look. "),
      "As the sole shareholder of a professional corporation you are excluded from the definition of “employee” for workers' compensation outright, with no waiver to file — ",
      extLink("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=3352.&lawCode=LAB", "Cal. Labor Code §3352(a)(18)(B)"),
      ". And a newly formed corporation is not subject to the $800 minimum franchise tax in its first taxable year — ",
      extLink("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=23153.&lawCode=RTC", "Cal. Rev. & Tax. Code §23153(f)"),
      " — a waiver that applies to corporations and expressly not to LLCs. First-year net income is still taxed at 1.5%; it simply is not floored at $800."),
    /*#__PURE__*/React.createElement("h4", {style: {marginTop: 22}}, "What it costs you"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "Running payroll for one person is cheap — the expensive part is the corporate return, which is a filing you do not have as a sole proprietor. These start at zero because the only figure worth planning on is the one your own accountant quotes you. Enter it and the comparison below becomes yours."),
    /*#__PURE__*/React.createElement("div", {className: "runcost"},
      costRow("Payroll service", "Patriot self-service ≈$126/yr · Square ≈$492 · Gusto or OnPay ≈$660 · QuickBooks ≈$1,134", payrollSvcCost, setPayrollSvcCost, 492),
      costRow("Corporate return prep", "1120-S for a clean single-shareholder corp typically $800–$1,200, plus $200–$500 for the CA 100S", corpReturnCost, setCorpReturnCost, 1200),
      costRow("Statement of Information", "Fixed statutory fee, $25 a year for a stock corporation", statementOfInfoCost, setStatementOfInfoCost, 25)),
    runCostTotal > 0 && /*#__PURE__*/React.createElement("p", {className: "runcost-total"},
      "Adding ", /*#__PURE__*/React.createElement("b", null, fmt0(runCostTotal)), " a year that a sole proprietor does not pay. This is carried into the comparison below."),
    !(runCostTotal > 0) && /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
      "While these are zero the comparison below shows the tax difference only, which will overstate what an S-corp is worth to you."));
  const psplit = payrollSplit(recNetProfit, sCorpSalaryInput);
  const keepOpener = keepBar(cur.grossYr, cur.expYr, cur.totalTax, cur.netYr, sessionRate);
  const payrollMechanic = /*#__PURE__*/React.createElement("div", {className: "mechanic"},
    /*#__PURE__*/React.createElement("h4", null, "Where the saving actually comes from"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "Moving a dollar from salary to distribution does not dodge income tax — it dodges ",
      /*#__PURE__*/React.createElement("b", null, "payroll tax"), ". That is the entire mechanism."),
    /*#__PURE__*/React.createElement("div", {className: "mech-cols"},
      /*#__PURE__*/React.createElement("div", {className: "mech-col"},
        /*#__PURE__*/React.createElement("h5", null, "One dollar as W-2 salary"),
        /*#__PURE__*/React.createElement("div", {className: "mech-stack"},
          /*#__PURE__*/React.createElement("i", {className: "m-ss"}, /*#__PURE__*/React.createElement("span", null, "Social Security — 6.2% you + 6.2% the corp"), /*#__PURE__*/React.createElement("b", null, "12.4¢")),
          /*#__PURE__*/React.createElement("i", {className: "m-med"}, /*#__PURE__*/React.createElement("span", null, "Medicare — 1.45% + 1.45%"), /*#__PURE__*/React.createElement("b", null, "2.9¢")),
          /*#__PURE__*/React.createElement("i", {className: "m-sdi"}, /*#__PURE__*/React.createElement("span", null, "CA SDI (employee)"), /*#__PURE__*/React.createElement("b", null, "1.2¢")),
          /*#__PURE__*/React.createElement("i", {className: "m-inc"}, /*#__PURE__*/React.createElement("span", null, "Income tax — federal + CA"), /*#__PURE__*/React.createElement("b", null, "varies"))),
        /*#__PURE__*/React.createElement("p", {className: "mech-foot"}, /*#__PURE__*/React.createElement("b", null, "16.5¢ of payroll tax"), " before income tax is even considered.")),
      /*#__PURE__*/React.createElement("div", {className: "mech-col"},
        /*#__PURE__*/React.createElement("h5", null, "One dollar as a distribution"),
        /*#__PURE__*/React.createElement("div", {className: "mech-stack"},
          /*#__PURE__*/React.createElement("i", {className: "m-none"}, "No Social Security · No Medicare · No SDI"),
          /*#__PURE__*/React.createElement("i", {className: "m-inc"}, /*#__PURE__*/React.createElement("span", null, "Income tax — federal + CA"), /*#__PURE__*/React.createElement("b", null, "varies"))),
        /*#__PURE__*/React.createElement("p", {className: "mech-foot"}, /*#__PURE__*/React.createElement("b", null, "0¢ of payroll tax."),
          " Income tax is identical to the salary dollar — that part never changes."))),
    /*#__PURE__*/React.createElement("div", {className: "compliance-goodnews", style: {borderLeftColor: "#C98B4B", background: "#FBF1E2"}},
      /*#__PURE__*/React.createElement("b", null, "A distribution is not tax-free. "),
      "You still pay federal and California income tax on every dollar of it, at the same rate as salary. What you skip is Social Security and Medicare — nothing else."),
    sCorpSalaryInput > 0 && recNetProfit > 0 ? /*#__PURE__*/React.createElement("div", {className: "mech-yours"},
      /*#__PURE__*/React.createElement("h5", null, "Your numbers — where the ", fmt0(psplit.saved), " comes from"),
      /*#__PURE__*/React.createElement("div", {className: "mech-row"},
        /*#__PURE__*/React.createElement("span", null, "Sole proprietor pays self-employment tax on 92.35% of ", fmt0(recNetProfit), " = ", fmt0(psplit.seBase)),
        /*#__PURE__*/React.createElement("b", null, fmt0(psplit.soleTotal))),
      /*#__PURE__*/React.createElement("div", {className: "mech-row"},
        /*#__PURE__*/React.createElement("span", null, "Corporation pays payroll tax on the ", fmt0(sCorpSalaryInput), " salary only — the ", fmt0(psplit.distribution), " distribution is not payroll"),
        /*#__PURE__*/React.createElement("b", null, fmt0(psplit.corpTotal))),
      /*#__PURE__*/React.createElement("div", {className: "mech-row mech-tot"},
        /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("b", null, "Payroll tax avoided")),
        /*#__PURE__*/React.createElement("b", {className: "pos"}, fmt0(psplit.saved))),
      psplit.saved > 0 ? /*#__PURE__*/React.createElement("div", {className: "mech-bar"},
        /*#__PURE__*/React.createElement("i", {className: "m-ss", style: {width: (psplit.savedSS / psplit.saved * 100) + "%"}}, "SOCIAL SECURITY " + fmt0(psplit.savedSS)),
        /*#__PURE__*/React.createElement("i", {className: "m-med", style: {width: (psplit.savedMed / psplit.saved * 100) + "%"}}, "MEDICARE " + fmt0(psplit.savedMed))) : null,
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        "Most of that is Social Security you are choosing not to pay into — which is the same money as the benefit you give up later. Two views of one decision.")) : null,
    /*#__PURE__*/React.createElement("div", {className: "mech-cliff-wrap"},
      /*#__PURE__*/React.createElement("h5", null, "The catch nobody explains — the cap"),
      /*#__PURE__*/React.createElement("div", {className: "mech-cliff"},
        /*#__PURE__*/React.createElement("i", {className: "cliff-hi"}, "15.3¢ saved per dollar"),
        /*#__PURE__*/React.createElement("i", {className: "cliff-lo"}, "2.9¢")),
      /*#__PURE__*/React.createElement("div", {className: "mech-cliff-lab"},
        /*#__PURE__*/React.createElement("span", null, "salary below ", fmt0(SS_WAGE_BASE_2026)),
        /*#__PURE__*/React.createElement("span", null, "above the Social Security cap")),
      /*#__PURE__*/React.createElement("p", {style: {fontSize: 13.5, marginTop: 12}},
        "Below the Social Security cap every dollar shifted out of salary saves the full ",
        /*#__PURE__*/React.createElement("b", null, "15.3%"), ". Above it you have already stopped paying Social Security, so shifting more only dodges Medicare — ",
        /*#__PURE__*/React.createElement("b", null, "2.9%"), ". ",
        psplit.aboveCap
          ? /*#__PURE__*/React.createElement("b", {className: "neg"}, "Your salary is above the cap, so extra distribution is working at the weaker 2.9% rate.")
          : /*#__PURE__*/React.createElement("b", null, "Your salary is below the cap, so the split is working at full strength."))));
  const recGood = !salaryUnset && netDiff > 2000;
  const recBad = !salaryUnset && netDiff < -500;
  const recColor = salaryUnset ? "#C98B4B" : recGood ? "#3F9577" : recBad ? "#B5483F" : "#C98B4B";
  const recLabel = salaryUnset ? "Set a salary before comparing" : recGood ? "Recommended: S-corp election" : recBad ? "Recommended: stay a Sole Proprietor" : "Close call \u2014 marginal either way";
  const recBody = salaryUnset ? `An S-corp paying a $0 salary isn't a real option \u2014 the IRS requires reasonable compensation before any distribution, so the saving shown here would not survive scrutiny. Enter a salary to compare properly; ${fmt0(recMinSalary)} (50% of your net profit) is the usual starting benchmark.` : recGood ? `Saves \u2248${fmt0(netDiff)}/yr at your current $${sCorpSalaryInput.toLocaleString()} salary, even after the added payroll tax, CA entity fee, and smaller QBI deduction.` : recBad ? `At this salary level, S-corp actually costs \u2248${fmt0(Math.abs(netDiff))}/yr more once the extra payroll tax and CA $800 minimum entity fee are counted \u2014 the salary may be set too high relative to profit for the split to pay off.` : `Only \u2248${fmt0(Math.abs(netDiff))}/yr difference \u2014 S-corp's added paperwork (payroll runs, Form 1120-S, more bookkeeping) may not be worth it for a gain this small yet.`;
  const netProfitForRatio = Math.max(1, scorpGrossBasis - scorpExpBasis);
  const salaryRatio = sCorpSalaryInput / netProfitForRatio;
  const lowSalaryWarning = entityType === "s_corp" && salaryRatio < 0.35 && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 10,
      color: "#B5483F",
      fontWeight: 600
    }
  }, "\u26A0\uFE0F This salary is only ", Math.round(salaryRatio * 100), "% of net profit \u2014 well below what's typically defensible as \u201Creasonable compensation.\u201D The tax savings above assume the IRS never questions it; see the audit-risk section further down before setting a number this low.");
  const minSalary = Math.round(netProfitForRatio * 0.5 / 1000) * 1000;
  const aggressiveSalary = Math.round(netProfitForRatio * 0.35 / 1000) * 1000;
  const minSalaryYear = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "s_corp", minSalary);
  const aggressiveSalaryYear = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "s_corp", aggressiveSalary);
  const educationBlock = /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 20
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      lineHeight: 1.7,
      margin: "0 0 12px"
    }
  }, "As a sole proprietor, ", /*#__PURE__*/React.createElement("b", null, "all"), " of your profit is taxed at the 15.3% self-employment rate. A Professional Corp lets you split profit into a ", /*#__PURE__*/React.createElement("b", null, "salary"), " (taxed at 15.3%, same as before) and a ", /*#__PURE__*/React.createElement("b", null, "distribution"), " (taxed at 0% self-employment tax). That split is the whole reason this choice exists."), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      lineHeight: 1.7,
      margin: "0 0 12px"
    }
  }, "The IRS requires that salary be \u201Creasonable\u201D for the work you actually do \u2014 not an arbitrary low number picked to dodge tax.", /*#__PURE__*/React.createElement("sup", null, "[a]"), " Set it too low and the whole strategy carries real audit risk (full mechanics further down this page)."), /*#__PURE__*/React.createElement("div", {
    className: "a-subhead"
  }, "Two salary strategies, same practice income"), /*#__PURE__*/React.createElement("div", {
    className: "funnel-target-grid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "Minimum suggested \u2014 salary ", fmt0(minSalary)), /*#__PURE__*/React.createElement("div", {
    className: "stat-value sm"
  }, fmt0(minSalaryYear.net)), /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, "50% of net profit \u2014 a commonly cited safer benchmark")), /*#__PURE__*/React.createElement("div", {
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "Most aggressive \u2014 salary ", fmt0(aggressiveSalary)), /*#__PURE__*/React.createElement("div", {
    className: "stat-value sm neg"
  }, fmt0(aggressiveSalaryYear.net)), /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, "35% of net profit \u2014 right at this tool's audit-risk warning line"))), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "\u201CAggressive\u201D means higher audit risk, not higher take-home guaranteed \u2014 it usually does produce more cash now, at the cost of a weaker position if the IRS ever asks you to justify the number. Neither figure is personalized advice; a CPA can price your specific role against comparable clinical wages."), citeList([{
    n: "a",
    cite: "IRS Fact Sheet FS-2008-25",
    url: "https://www.irs.gov/pub/irs-news/fs-08-25.pdf",
    note: "\u201CWage Compensation for S Corporation Officers\u201D \u2014 shareholder-employees performing more than minor services must be paid reasonable compensation before any distribution."
  }]));
  const businessStructureSection = /*#__PURE__*/React.createElement("section", {
    className: "card decision-impact"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Business structure"), /*#__PURE__*/React.createElement("p", null, "Sole Proprietorship vs. Professional Corp with an S-corp election \u2014 this choice is global and changes the tax math on every tab.")), educationBlock, entityToggle, salaryInputRow, salaryGuidance, payrollMechanic, complianceGuide, /*#__PURE__*/React.createElement("div", {
    className: "resid-invest-note",
    style: {
      borderLeft: "4px solid " + recColor,
      background: "#fff"
    }
  }, /*#__PURE__*/React.createElement("b", {
    style: {
      color: recColor
    }
  }, recLabel), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4
    }
  }, recBody), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      fontStyle: "italic"
    }
  }, "One thing this recommendation doesn't weigh: a lower S-corp salary also means less Social Security credit for the year \u2014 see \u201CThe trade-off nobody mentions\u201D further down before deciding."), lowSalaryWarning));
const ssSection = (function () {
    var ss = strategy.socialSecurity;
    return /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel"
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel-head"
    }, /*#__PURE__*/React.createElement("h3", null, "The trade-off nobody mentions: Social Security")), /*#__PURE__*/React.createElement("p", {
      style: {
        margin: "6px 0 14px",
        fontSize: 14,
        lineHeight: 1.6
      }
    }, "Only ", /*#__PURE__*/React.createElement("b", null, "wages"), " earn Social Security credit \u2014 S-corp distributions earn ", /*#__PURE__*/React.createElement("b", null, "zero"), ". Your future benefit is based on your highest 35 years of covered earnings (SSA always divides by 420 months, filling in $0 for any missing years), run through a progressive formula: 90% of the first $1,286/mo of average indexed earnings, 32% of the next $1,286\u2013$7,749, and 15% above that.", /*#__PURE__*/React.createElement("sup", null, "[7]"), " Lowering your salary to reduce this year's SE/payroll tax also lowers what counts toward that formula \u2014 permanently, for whichever years you do it."), /*#__PURE__*/React.createElement("div", {
      className: "a-subhead"
    }, "SS-credited earnings this year"), /*#__PURE__*/React.createElement("div", {
      className: "funnel-target-grid"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat-label"
    }, "Sole prop path"), /*#__PURE__*/React.createElement("div", {
      className: "stat-value sm"
    }, fmt0(ss.soleCreditedEarnings))), /*#__PURE__*/React.createElement("div", {
      className: "stat"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat-label"
    }, "S-corp salary path"), /*#__PURE__*/React.createElement("div", {
      className: "stat-value sm"
    }, fmt0(ss.scorpCreditedEarnings)))), ss.scorpCreditedEarnings < ss.soleCreditedEarnings && /*#__PURE__*/React.createElement("div", {
      className: "resid-invest-note",
      style: {
        marginTop: 12,
        borderLeft: "4px solid #B5483F",
        background: "#fff"
      }
    }, /*#__PURE__*/React.createElement("b", {
      style: {
        color: "#B5483F"
      }
    }, fmt0(ss.soleCreditedEarnings - ss.scorpCreditedEarnings), " less credited this year"), " going the S-corp route."), /*#__PURE__*/React.createElement("div", {
      className: "a-subhead",
      style: {
        marginTop: 20
      }
    }, "If this holds for your remaining ", ss.yearsForAIME, " working years"), /*#__PURE__*/React.createElement("p", {
      style: {
        margin: "0 0 10px",
        fontSize: 12.5,
        color: "var(--muted)"
      }
    }, "Simplified \u2014 assumes a full 35-year career at this level, not your actual earnings history."), /*#__PURE__*/React.createElement("div", {
      className: "funnel-target-grid"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat-label"
    }, "Est. monthly benefit, sole prop"), /*#__PURE__*/React.createElement("div", {
      className: "stat-value sm"
    }, fmt0(ss.soleMonthlyPIA), "/mo")), /*#__PURE__*/React.createElement("div", {
      className: "stat"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat-label"
    }, "Est. monthly benefit, S-corp"), /*#__PURE__*/React.createElement("div", {
      className: "stat-value sm"
    }, fmt0(ss.scorpMonthlyPIA), "/mo"))), ss.monthlyGap > 0 && /*#__PURE__*/React.createElement("div", {
      className: "resid-invest-note",
      style: {
        marginTop: 12,
        borderLeft: "4px solid #B5483F",
        background: "#fff"
      }
    }, /*#__PURE__*/React.createElement("b", {
      style: {
        color: "#B5483F",
        fontSize: 16
      }
    }, "Monthly gap: ", fmt0(ss.monthlyGap), "/mo (", fmt0(ss.annualGap), "/yr)"), /*#__PURE__*/React.createElement("div", {
      style: {
        marginTop: 4,
        color: "#B5483F"
      }
    }, "Over a 20-year retirement, roughly ", /*#__PURE__*/React.createElement("b", null, fmt0(ss.annualGap * 20)), " less lifetime benefit.")), (function () {
      const yearsWork = ss.yearsForAIME;
      const r = investReturn / 100;
      const cumulativeSavingsNominal = netDiff * yearsWork;
      const fvSavingsInvested = netDiff > 0 && r > 0 ? netDiff * ((Math.pow(1 + r, yearsWork) - 1) / r) : cumulativeSavingsNominal;
      const ssLifetimeLoss = ss.annualGap * 20;
      const verdict = fvSavingsInvested - ssLifetimeLoss;
      return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
        className: "a-subhead",
        style: {
          marginTop: 20
        }
      }, "Net verdict: tax savings vs. Social Security given up"), /*#__PURE__*/React.createElement("div", {
        className: "funnel-target-grid"
      }, /*#__PURE__*/React.createElement("div", {
        className: "stat"
      }, /*#__PURE__*/React.createElement("div", {
        className: "stat-label"
      }, "S-corp tax savings, ", yearsWork, " yrs (nominal)"), /*#__PURE__*/React.createElement("div", {
        className: "stat-value sm"
      }, fmt0(cumulativeSavingsNominal))), /*#__PURE__*/React.createElement("div", {
        className: "stat"
      }, /*#__PURE__*/React.createElement("div", {
        className: "stat-label"
      }, "Invested at ", investReturn, "%/yr until retirement"), /*#__PURE__*/React.createElement("div", {
        className: "stat-value sm"
      }, fmt0(fvSavingsInvested)))), /*#__PURE__*/React.createElement("div", {
        className: "stat",
        style: {
          marginTop: 10
        }
      }, /*#__PURE__*/React.createElement("div", {
        className: "stat-label"
      }, "Social Security given up, 20-yr retirement"), /*#__PURE__*/React.createElement("div", {
        className: "stat-value sm neg"
      }, "\u2212", fmt0(ssLifetimeLoss))), /*#__PURE__*/React.createElement("div", {
        className: "resid-invest-note",
        style: {
          marginTop: 12,
          borderLeft: "4px solid " + (verdict >= 0 ? "#3F9577" : "#B5483F"),
          background: "#fff"
        }
      }, /*#__PURE__*/React.createElement("b", {
        style: {
          color: verdict >= 0 ? "#3F9577" : "#B5483F",
          fontSize: 16
        }
      }, verdict >= 0 ? "Net: S-corp still ahead by " : "Net: S-corp actually behind by ", fmt0(Math.abs(verdict)))), /*#__PURE__*/React.createElement("p", {
        className: "pay-note"
      }, "This compares two very different kinds of dollars: tax savings arrive every year, starting now, and can be invested; the Social Security gap is a future monthly check, reduced for as long as you live in retirement (modeled here as a flat 20 years, with no inflation adjustment on either side). Investing 100% of the tax savings every year is optimistic \u2014 treat this as the ", /*#__PURE__*/React.createElement("i", null, "best case"), " for the S-corp side, not a guarantee."));
    })(), /*#__PURE__*/React.createElement("p", {
      className: "pay-note"
    }, "This is a simplified, steady-state projection \u2014 not a benefit estimate. It ignores your actual earnings history, cost-of-living adjustments between now and retirement, spousal/survivor benefits, and assumes claiming at full retirement age. Get your real earnings record and estimate at ssa.gov/myaccount before making any decision based on this."));
  })();
  const scorpSection = /*#__PURE__*/React.createElement("details", {
    className: "card collapsible"
  }, /*#__PURE__*/React.createElement("summary", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Reduce self-employment tax: the S-corp election"), /*#__PURE__*/React.createElement("p", null, "Retirement accounts reduce taxable ", /*#__PURE__*/React.createElement("i", null, "income"), " tax. This is the main lever for reducing ", /*#__PURE__*/React.createElement("i", null, "self-employment"), " tax itself \u2014 a different, often larger, savings. Change your election in the ", /*#__PURE__*/React.createElement("b", null, "Business structure"), " card near the top of this page \u2014 click to expand the full mechanics, the catch, and the audit risk.")), /*#__PURE__*/React.createElement("p", null, "As a sole proprietor, all of your net practice profit is subject to the 15.3% self-employment tax. Electing S-corp tax status (as a professional corporation) lets you split that profit into two pieces: a ", /*#__PURE__*/React.createElement("b", null, "salary"), " (subject to payroll tax, same 15.3% split between employer and employee) and a ", /*#__PURE__*/React.createElement("b", null, "distribution"), " (not subject to payroll or self-employment tax at all).", /*#__PURE__*/React.createElement("sup", null, "[1]")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "Full comparison, using your actual numbers")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat",
    style: {
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "Net practice profit"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value"
  }, fmt0(scorpGrossBasis - scorpExpBasis))), /*#__PURE__*/React.createElement("div", {
    className: "funnel-target-grid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "As sole proprietor"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value"
  }, fmt0(soleFullYear.net)), /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, fmt0(soleFullYear.totalTax), " total tax")), /*#__PURE__*/React.createElement("div", {
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "As S-corp"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value"
  }, fmt0(sCorpFullYear.net)), /*#__PURE__*/React.createElement("div", {
    className: "stat-note"
  }, fmt0(sCorpFullYear.totalTax), " total tax"))), /*#__PURE__*/React.createElement("div", {
    className: "a-subhead",
    style: {
      marginTop: 18
    }
  }, "S-corp breakdown"), /*#__PURE__*/React.createElement("div", {
    className: "funnel-target-grid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "Salary + distribution"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value sm"
  }, fmt0(sCorpFullYear.salary), " + ", fmt0(sCorpFullYear.kDistribution))), /*#__PURE__*/React.createElement("div", {
    className: "stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "stat-label"
  }, "Employer payroll tax + CA entity tax"), /*#__PURE__*/React.createElement("div", {
    className: "stat-value sm neg"
  }, fmt0(sCorpFullYear.employerPayrollTax + sCorpFullYear.caEntityTax)))), /*#__PURE__*/React.createElement("div", {
    className: sCorpFullYear.net >= soleFullYear.net ? "resid-invest-note" : "resid-invest-note",
    style: {
      marginTop: 18,
      borderLeft: "4px solid " + (sCorpFullYear.net >= soleFullYear.net ? "#3F9577" : "#B5483F"),
      background: "#fff"
    }
  }, /*#__PURE__*/React.createElement("b", {
    style: {
      color: sCorpFullYear.net >= soleFullYear.net ? "#3F9577" : "#B5483F",
      fontSize: 16
    }
  }, "Net difference (S-corp \u2212 sole prop): ", sCorpFullYear.net - soleFullYear.net >= 0 ? "+" : "\u2212", fmt0(Math.abs(sCorpFullYear.net - soleFullYear.net))))), /*#__PURE__*/React.createElement("p", {

    className: "pay-note"
  }, "This full comparison accounts for the employer-side payroll tax match (a real cost) and the fact that S-corp K-1 distributions get a smaller QBI deduction than sole-proprietor income, since wages are excluded from the QBI base.", /*#__PURE__*/React.createElement("sup", null, "[2]"), " S-corp status also adds costs this simulator doesn't model: payroll processing, a separate business return (Form 1120-S), and generally more bookkeeping.")), ssSection, /*#__PURE__*/React.createElement("h3", {
    style: {
      marginTop: 24,
      fontFamily: "'Fraunces', serif"
    }
  }, "The catch: \u201Creasonable compensation\u201D"), /*#__PURE__*/React.createElement("p", null, "The IRS requires an S-corp shareholder who performs substantial services to be paid a fair-market salary ", /*#__PURE__*/React.createElement("b", null, "before"), " taking any distribution.", /*#__PURE__*/React.createElement("sup", null, "[3]"), " Salary set too low relative to distributions is exactly the pattern the IRS looks for. Reasonableness is judged on facts and circumstances, not a formula \u2014 the factors that show up consistently in court decisions and IRS guidance are:", /*#__PURE__*/React.createElement("sup", null, "[4]")), /*#__PURE__*/React.createElement("ul", {
    className: "cite-list"
  }, /*#__PURE__*/React.createElement("li", null, "Training, experience, and licensure"), /*#__PURE__*/React.createElement("li", null, "Duties and responsibilities actually performed"), /*#__PURE__*/React.createElement("li", null, "Time and effort devoted to the practice (full-time vs. part-time)"), /*#__PURE__*/React.createElement("li", null, "What comparable businesses pay for similar clinical work"), /*#__PURE__*/React.createElement("li", null, "Dividend/distribution history \u2014 a pattern of high distributions and minimal salary is a specific red flag"), /*#__PURE__*/React.createElement("li", null, "What you pay any non-owner employees for similar work")), /*#__PURE__*/React.createElement("p", null, "Getting this wrong is a real, citable audit risk, not a theoretical one: in ", /*#__PURE__*/React.createElement("a", {href: "https://ecf.ca8.uscourts.gov/opndir/12/02/111589P.pdf", target: "_blank", rel: "noopener noreferrer", className: "extlink"}, /*#__PURE__*/React.createElement("i", null, "David E. Watson, P.C. v. United States")), ", a CPA who paid himself a $24,000 salary against $203,651 in distributions had his compensation reclassified upward to $91,044 by the Eighth Circuit; in ", /*#__PURE__*/React.createElement("i", null, "Nu-Look Design v. Commissioner"), ", shareholder-employees taking $0 salary lost similarly at the Third Circuit.", /*#__PURE__*/React.createElement("sup", null, "[5]"), " When the IRS reclassifies a distribution as wages, it comes with back payroll taxes, penalties, and interest \u2014 without any offsetting new deduction to soften it.", /*#__PURE__*/React.createElement("sup", null, "[6]")), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, citeList([
    {n:1, cite:"IRC \u00A71373", url:"https://www.law.cornell.edu/uscode/text/26/1373", note:"Rev. Rul. 59-221, 1959-1 C.B. 225 \u2014 S-corp flow-through profit distributed as such is not subject to self-employment tax; compensation for services is."},
    {n:2, cite:"IRC \u00A7199A(c)(4)", url:"https://www.law.cornell.edu/uscode/text/26/199A", note:"excludes reasonable compensation from qualified business income."},
    {n:3, cite:"Treas. Reg. \u00A731.3121(d)-1(b)", url:"https://www.law.cornell.edu/cfr/text/26/31.3121(d)-1", note:"treats more-than-minor services for remuneration as employment; see also IRS Fact Sheet FS-2008-25, \u201CWage Compensation for S Corporation Officers.\u201D"},
    {n:4, cite:"Davis v. United States", url:"https://scholar.google.com/scholar?q=Davis+v.+United+States+reasonable+compensation+S+corporation", note:"and subsequent reasonable-compensation case law as summarized in IRS training materials."},
    {n:5, cite:"David E. Watson, P.C. v. United States, 668 F.3d 1008 (8th Cir. 2012)", url:"https://ecf.ca8.uscourts.gov/opndir/12/02/111589P.pdf", note:"a $24,000 salary alongside $203,651 in distributions was recharacterised to $91,044 of wages."},
    {n:6, cite:"Nu-Look Design, Inc. v. Commissioner, 356 F.3d 290 (3d Cir. 2004)", url:"https://scholar.google.com/scholar?q=Nu-Look+Design+v.+Commissioner+356+F.3d+290", note:null},
    {n:7, cite:"IRC \u00A76651 and \u00A76656", url:"https://www.law.cornell.edu/uscode/text/26/6651", note:"standard IRS penalty and interest provisions on reclassified back payroll tax assessments."},
    {n:8, cite:"Social Security Act \u00A7215(a)(1)(A)", url:"https://www.ssa.gov/OP_Home/ssact/title02/0215.htm", note:"2026 bend points ($1,286 / $7,749) and wage base ($184,500) per SSA/Congressional Research Service published figures \u2014 AIME divides your highest 35 years of indexed earnings by 420 months."}
  ])), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "None of this is personalized legal or tax advice \u2014 reasonable-compensation determinations are fact-specific; work with a CPA before electing S-corp status or setting a salary."));

  const llcFeeSchedule = [[0, 0], [250000, 900], [500000, 2500], [1000000, 6000], [5000000, 11790]];
  const caGrossReceipts = scorpGrossBasis;
  const llcFee = (function () {
    var fee = 0;
    for (var i = 0; i < llcFeeSchedule.length; i++) {
      if (caGrossReceipts >= llcFeeSchedule[i][0]) fee = llcFeeSchedule[i][1];
    }
    return fee;
  })();
  const llcAnnualCost = 800 + llcFee;
  const soleNoLLCTax = soleFullYear.totalTax;
  const caSection = /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Choosing a structure in California"), /*#__PURE__*/React.createElement("p", null, "California taxes business entities at the state level on top of everything above \u2014 a cost that doesn't exist for a plain sole proprietorship. This changes where the S-corp break-even actually sits for a California-based solo practice.")), /*#__PURE__*/React.createElement("div", {
    className: "resid-invest-note",
    style: {
      borderLeft: "4px solid #B5483F",
      background: "#fff",
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("b", {
    style: {
      color: "#B5483F"
    }
  }, "\u26A0\uFE0F If you're a CA-licensed MFT, LCSW, LPCC, or psychologist: LLC is not a legal option for your practice."), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6
    }
  }, "California Corporations Code \u00A717701.04(e) specifically blocks LLCs from rendering licensed professional services in this state.", /*#__PURE__*/React.createElement("sup", null, "[10]"), " Your actual choice is a plain ", /*#__PURE__*/React.createElement("b", null, "Sole Proprietorship"), " versus a ", /*#__PURE__*/React.createElement("b", null, "California Professional Corporation"), " (for MFTs, specifically a \u201CMarriage and Family Therapy Corporation\u201D \u2014 51% of shares must be held by a licensed MFT, per Corp. Code \u00A713401.5).", /*#__PURE__*/React.createElement("sup", null, "[11]"), " That Professional Corporation can then elect S-corp ", /*#__PURE__*/React.createElement("i", null, "federal tax treatment"), " with the IRS \u2014 that election is exactly what this tool models as \u201CS-corp.\u201D The LLC comparison below is shown for completeness (it's the standard option in most other states/professions) but does not apply to your licensed practice \u2014 skip straight to the Professional Corp numbers.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-mini-stats",
    style: {
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, "Sole proprietor: CA entity tax ", /*#__PURE__*/React.createElement("b", null, "$0")), /*#__PURE__*/React.createElement("div", null, "LLC (no S-election): CA cost ", /*#__PURE__*/React.createElement("b", null, fmt0(llcAnnualCost)), "/yr"), /*#__PURE__*/React.createElement("div", null, "S-corp: CA cost ", /*#__PURE__*/React.createElement("b", null, fmt0(sCorpFullYear.caEntityTax)), "/yr")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "Sole Proprietor")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "No separate legal entity, no CA franchise tax, no LLC fee, no extra tax return. Full self-employment tax on all profit. This is the default for most solo therapists just starting out, and stays cost-competitive until the S-corp's SE-tax savings clear the extra CA entity-level cost below.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "LLC, no S-election (not available to CA-licensed therapists)")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "Every California LLC owes an $800/yr minimum franchise tax from year one \u2014 the old first-year waiver expired \u2014 plus a gross-receipts fee once revenue crosses $250k: $900 at $250k\u2013$499k, $2,500 at $500k\u2013$999k, $6,000 at $1M\u2013$4.99M, $11,790 above that.", /*#__PURE__*/React.createElement("sup", null, "[8]"), " Taxed identically to a sole proprietor otherwise \u2014 ", /*#__PURE__*/React.createElement("b", null, "no SE-tax savings"), ". The LLC wrapper buys legal liability separation for business debts and contracts, not a tax break; for a solo therapist, malpractice insurance already covers the dominant risk (clinical liability) regardless of entity choice.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "S-corp (via Professional Corporation)")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, "California taxes S-corps at the greater of 1.5% of net income or $800/yr \u2014 charged ", /*#__PURE__*/React.createElement("b", null, "in addition to"), " federal tax, and it applies even in a loss year.", /*#__PURE__*/React.createElement("sup", null, "[9]"), " Salary is deductible before that 1.5% is computed, so the tax mostly falls on the distribution slice \u2014 the same dollars generating your federal SE-tax savings. That's why the real S-corp break-even in California sits higher than the federal-only math suggests.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel",
    style: {
      background: "#F3F0E7"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-channel-head"
  }, /*#__PURE__*/React.createElement("h3", null, "Based on your numbers")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      lineHeight: 1.6
    }
  }, sCorpFullYear.net > soleFullYear.net ? /*#__PURE__*/React.createElement(React.Fragment, null, "At your current profit, S-corp still nets ", /*#__PURE__*/React.createElement("b", null, fmt0(sCorpFullYear.net - soleFullYear.net)), " more per year than staying a sole proprietor, ", /*#__PURE__*/React.createElement("b", null, "even after"), " California's ", fmt0(sCorpFullYear.caEntityTax), "/yr entity tax and the employer-side payroll tax. The federal SE-tax savings are large enough to clear California's extra cost at this income level.") : /*#__PURE__*/React.createElement(React.Fragment, null, "At your current profit, staying a sole proprietor nets ", /*#__PURE__*/React.createElement("b", null, fmt0(soleFullYear.net - sCorpFullYear.net)), " more than S-corp once California's entity-level tax and payroll costs are included \u2014 the SE-tax savings haven't caught up to the extra overhead yet. Common CPA guidance for California solo practitioners is to wait until net profit is comfortably above the ", /*#__PURE__*/React.createElement("b", null, "$80k\u2013$100k range"), " before the S-corp election reliably pays for itself, though the real break-even depends on your specific salary/distribution split."))), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, citeList([
    {n:8, cite:"Cal. Rev. & Tax. Code \u00A717941 and \u00A717942", url:"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17941.&lawCode=RTC", note:"$800 minimum franchise tax (no first-year exemption for LLCs since the AB 85 waiver expired) and the gross-receipts fee schedule, reported on FTB Form 3536/568."},
    {n:9, cite:"Cal. Rev. & Tax. Code \u00A723153", url:"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=23153.&lawCode=RTC", note:"S-corp franchise tax, greater of 1.5% of net income or $800 minimum, reported on FTB Form 100S; first-year exemption available for newly incorporated corporations (not LLCs) under \u00A723153(f)."},
    {n:10, cite:"Cal. Corp. Code \u00A717701.04(e)", url:"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17701.04.&lawCode=CORP", note:"\u201CNothing in this title shall be construed to permit a domestic or foreign limited liability company to render professional services...in this state.\u201D"},
    {n:11, cite:"Cal. Corp. Code \u00A713401.5 and \u00A713406", url:"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=13401.5.&lawCode=CORP", note:"permitted shareholders of a marriage and family therapy corporation, and the majority-ownership requirement."}
  ])), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "Figures are 2026 estimates \u2014 confirm current thresholds with a California-licensed CPA and, for the choice of entity itself, an attorney familiar with the Moscone-Knox Professional Corporation Act, before choosing or changing entity structure; this isn't personalized legal or tax advice."));

  const analysisSection = /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "What this means for you")), /*#__PURE__*/React.createElement("p", null, recommendation, rothNote), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, "Figures use projected 2026 IRS contribution limits and income phase-out ranges, and a simplified compounding model (same contribution repeated every year at a flat return, no fees or taxes on withdrawal modeled). Solo 401(k) employer contributions assume a sole proprietorship / single-member LLC (20% of net self-employment earnings); an S-corp election changes this calculation to 25% of W-2 wages instead. This isn't personalized investment or tax advice \u2014 a CPA or fee-only fiduciary advisor can confirm what's actually deductible and suitable for you."));

  return /*#__PURE__*/React.createElement(React.Fragment, null, keepOpener, introSection, taxProfileSection, businessStructureSection, statsRow, strategiesSection, compareSection, entityCompareSection, seEducation, scorpSection, caSection, analysisSection);
}

function FunnelTab({
  color,
  rate,
  sessions,
  avgTenure,
  setAvgTenure,
  currentClients,
  setCurrentClients,
  sessionsPerClientWk,
  setSessionsPerClientWk,
  monthlyChurn,
  setMonthlyChurn,
  monthsToTarget,
  setMonthsToTarget,
  funnel,
  setFunnel,
  calc
}) {
  const setStage = (chanKey, stage, val) => setFunnel(f => ({
    ...f,
    [chanKey]: {
      ...f[chanKey],
      [stage]: val
    }
  }));
  const progressPct = Math.max(2, Math.min(100, Math.round(currentClients / Math.max(1, calc.targetClients) * 100)));
  const scoreColor = calc.healthScore >= 70 ? "#3F9577" : calc.healthScore >= 45 ? "#C98B4B" : "#B5483F";
  const inputField = (label, value, onChange, suffix) => /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field",
    key: label
  }, /*#__PURE__*/React.createElement("label", null, label), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    value: value,
    onChange: e => onChange(e.target.value)
  }), suffix && /*#__PURE__*/React.createElement("span", {
    className: "funnel-input-suffix"
  }, suffix));
  const stageField = (chanKey, stage, label, value, hint) => /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-field",
    key: stage
  }, /*#__PURE__*/React.createElement("label", null, label), hint && /*#__PURE__*/React.createElement("span", {
    className: "funnel-input-hint"
  }, hint), /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: 0,
    value: value,
    onChange: e => setStage(chanKey, stage, e.target.value)
  }));
const channelBlock = c => {
    const max = Math.max(1, c.visits);
    const evAt = n => n > 0 ? Math.min(calc.clientValue, c.converted / n * calc.clientValue) : 0;
    const stages = [{
      k: "visits",
      label: c.key === "ref" ? "Referred" : "Profile visits",
      v: c.visits,
      ev: evAt(c.visits)
    }, {
      k: "calls",
      label: "Calls / emails",
      v: c.calls,
      ev: evAt(c.calls)
    }, {
      k: "consults",
      label: "Consult call",
      v: c.consults,
      ev: evAt(c.consults)
    }, {
      k: "intake",
      label: "Intake",
      v: c.intake,
      ev: evAt(c.intake)
    }, {
      k: "converted",
      label: "Converted client (10th session)",
      v: c.converted,
      ev: c.converted > 0 ? calc.clientValue : 0
    }];
    const svgW = 200,
      segH = 42,
      svgH = segH * stages.length,
      cx = svgW / 2,
      maxV = Math.max(1, stages[0].v);
    const segWidth = v => Math.max(22, Math.min(svgW - 4, svgW * (v / maxV)));
    const opacities = [1, 0.84, 0.68, 0.52, 0.4];
    const sizes = [12, 12.8, 13.8, 15, 17];
    const weights = [500, 600, 650, 700, 800];
    const funnelShape = /*#__PURE__*/React.createElement("svg", {
      viewBox: `0 0 ${svgW} ${svgH}`,
      width: "100%",
      style: {
        maxWidth: 200,
        display: "block"
      }
    }, stages.map((s, i) => {
      const wTop = segWidth(s.v);
      const wBottom = i < stages.length - 1 ? segWidth(stages[i + 1].v) : wTop * 0.86;
      const yTop = i * segH;
      const yBottom = yTop + segH - 2;
      const points = `${cx - wTop / 2},${yTop} ${cx + wTop / 2},${yTop} ${cx + wBottom / 2},${yBottom} ${cx - wBottom / 2},${yBottom}`;
      return /*#__PURE__*/React.createElement("polygon", {
        key: s.k,
        points: points,
        fill: color,
        fillOpacity: opacities[i]
      });
    }));
    const stageList = /*#__PURE__*/React.createElement("div", {
      className: "funnel-stage-list"
    }, stages.map((s, i) => /*#__PURE__*/React.createElement("div", {
      className: "funnel-stage-row",
      key: s.k
    }, /*#__PURE__*/React.createElement("span", {
      className: "funnel-stage-dot",
      style: {
        background: color,
        opacity: opacities[i]
      }
    }), /*#__PURE__*/React.createElement("span", {
      className: "funnel-stage-name"
    }, s.label), /*#__PURE__*/React.createElement("span", {
      className: "funnel-stage-num"
    }, s.v), /*#__PURE__*/React.createElement("span", {
      className: "funnel-stage-conv"
    }, i === 0 ? "\u2014" : stages[i - 1].v > 0 ? Math.round(s.v / stages[i - 1].v * 100) + "%" : "\u2014"), /*#__PURE__*/React.createElement("span", {
      className: "funnel-stage-value",
      style: {
        fontSize: sizes[i],
        fontWeight: weights[i],
        color: s.v > 0 ? color : "#C6BFAD",
        opacity: s.v > 0 ? Math.max(0.55, opacities[i]) : 0.5
      }
    }, s.v > 0 ? "\u2248$" + Math.round(s.ev).toLocaleString() : "\u2014"))));
    return /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel",
      key: c.key
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-channel-head"
    }, /*#__PURE__*/React.createElement("h3", null, c.label), /*#__PURE__*/React.createElement("span", {
      className: "funnel-channel-value"
    }, "$", Math.round(c.value).toLocaleString(), " in lifetime value")), /*#__PURE__*/React.createElement("div", {
      className: "funnel-input-grid funnel-stage-grid"
    }, stageField(c.key, "visits", c.key === "ref" ? "Referred" : "Profile visits", c.visits, c.key === "ref" ? "People sent your way" : c.key === "web" ? "People who landed on your site" : "People who opened your listing"), stageField(c.key, "calls", "Calls / emails", c.calls, "Of those, how many got in touch"), stageField(c.key, "consults", "Consult call", c.consults, "Actually had the intro call"), stageField(c.key, "intake", "Intake", c.intake, "Booked and attended a first session"), stageField(c.key, "converted", "Converted client", c.converted, "Still with you at session 10")), /*#__PURE__*/React.createElement("div", {
      className: "funnel-viz"
    }, /*#__PURE__*/React.createElement("div", {
      className: "funnel-viz-shape"
    }, funnelShape), stageList), /*#__PURE__*/React.createElement("div", {
      className: "funnel-stage-note"
    }, "Overall visit \u2192 client rate: ", /*#__PURE__*/React.createElement("b", null, (c.overallRate * 100).toFixed(1), "%")));
  };
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Sales funnel"), /*#__PURE__*/React.createElement("p", null, "Turn last month's marketing numbers into a plan for the year ahead: how many leads keep your caseload full, and how many you need to reach your target caseload. What a client is worth, below, uses your current rate (", "$", rate, "/hr) \u00D7 the average sessions a client stays with you.")), /*#__PURE__*/React.createElement("div", {
    className: "ltv-formula"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ltv-formula-term"
  }, /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-label"
  }, "Your rate"), /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-val"
  }, "$", rate, "/hr")), /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-op"
  }, "\u00D7"), /*#__PURE__*/React.createElement("div", {
    className: "ltv-formula-term"
  }, /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-label"
  }, "Avg. lifetime sessions/client"), /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-val"
  }, avgTenure)), /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-op"
  }, "="), /*#__PURE__*/React.createElement("div", {
    className: "ltv-formula-term ltv-formula-result"
  }, /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-label"
  }, "What a client is worth"), /*#__PURE__*/React.createElement("span", {
    className: "ltv-formula-val",
    style: {
      color: color
    }
  }, "$", Math.round(calc.clientValue).toLocaleString()))), /*#__PURE__*/React.createElement("div", {
    className: "funnel-input-grid"
  }, inputField("Avg. lifetime sessions/client", avgTenure, v => setAvgTenure(+v || 0)), inputField("Sessions per client per week", sessionsPerClientWk, v => setSessionsPerClientWk(+v || 0)), inputField("Current active clients", currentClients, v => setCurrentClients(+v || 0)), inputField("Clients lost last month", monthlyChurn, v => setMonthlyChurn(+v || 0)), inputField("Months to reach target", monthsToTarget, v => setMonthsToTarget(+v || 0)))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-score-row"
  }, /*#__PURE__*/React.createElement("div", {
    className: "health-gauge"
  }, /*#__PURE__*/React.createElement("div", {
    className: "health-ring",
    style: {
      background: `conic-gradient(${scoreColor} ${calc.healthScore * 3.6}deg, #EFEAE0 0deg)`
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "health-ring-inner"
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: scoreColor
    }
  }, calc.healthScore))), /*#__PURE__*/React.createElement("div", {
    className: "health-label"
  }, "Funnel health score"), /*#__PURE__*/React.createElement("div", {
    className: "health-sub"
  }, calc.onTrack ? "\uD83C\uDFAF On track" : calc.netChangeLastMonth < 0 ? "\u26A0\uFE0F Losing clients faster than gaining" : "\uD83D\uDCC8 Building toward target")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-progress-block"
  }, /*#__PURE__*/React.createElement("div", {
    className: "funnel-progress-head"
  }, /*#__PURE__*/React.createElement("span", null, "Caseload: ", /*#__PURE__*/React.createElement("b", null, currentClients), " of ", /*#__PURE__*/React.createElement("b", null, calc.targetClients), " target clients"), /*#__PURE__*/React.createElement("span", null, progressPct, "%")), /*#__PURE__*/React.createElement("div", {
    className: "progress-track"
  }, /*#__PURE__*/React.createElement("div", {
    className: "progress-fill",
    style: {
      width: progressPct + "%",
      background: color
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "funnel-progress-note"
  }, calc.clientGap > 0 ? `${calc.clientGap} more clients needed to hit your ${sessions}-session/week target (${calc.targetClients} clients at ${sessionsPerClientWk > 0 ? sessionsPerClientWk : 1}/wk each)` : "You're at or above your target caseload — focus on replacing churn to hold steady."), /*#__PURE__*/React.createElement("div", {
    className: "funnel-mini-stats"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, calc.totalConverted), " new clients last month"), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, monthlyChurn), " lost last month"), /*#__PURE__*/React.createElement("div", {
    className: calc.netChangeLastMonth >= 0 ? "pos" : "neg"
  }, calc.netChangeLastMonth >= 0 ? "+" : "", calc.netChangeLastMonth, " net change"))))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Last month's leads, by channel"), /*#__PURE__*/React.createElement("p", null, "Enter what actually happened last month. Each channel's own visit-to-client rate is used to size next month's targets."), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, /*#__PURE__*/React.createElement("b", null, "A converted client"), " means someone still in therapy at their 10th session \u2014 not just anyone who booked. People drop off at every step, and the two biggest drops are usually the consult call and the intake, which is why each gets its own row.")), calc.channels.map(channelBlock), /*#__PURE__*/React.createElement("div", {
    className: "funnel-leak"
  }, /*#__PURE__*/React.createElement("span", {
    className: "funnel-leak-icon"
  }, "\uD83D\uDCA7"), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, "Leaky part of the funnel: ", monthlyChurn, " client", monthlyChurn === 1 ? "" : "s", " lost last month."), " That's ", "$", Math.round(monthlyChurn * calc.clientValue).toLocaleString(), " in lifetime value walking out the door every month it continues \u2014 replacing it is the first job of your marketing, before any growth on top.")), /*#__PURE__*/React.createElement("div", {
    className: "funnel-total-value"
  }, /*#__PURE__*/React.createElement("span", null, "Total lifetime value generated last month across all channels"), /*#__PURE__*/React.createElement("strong", {
    style: {
      color: color
    }
  }, "$", Math.round(calc.totalValue).toLocaleString()))), (function () {
    const leadTargetCards = /*#__PURE__*/React.createElement("div", {
      className: "funnel-target-grid"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat"
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat-label"
    }, "To maintain (replace churn only)"), /*#__PURE__*/React.createElement("div", {
      className: "stat-value"
    }, calc.newClientsPerMonthSteady, " new clients/mo"), /*#__PURE__*/React.createElement("div", {
      className: "stat-note"
    }, calc.visitsNeededSteady != null ? `\u2248 ${calc.visitsNeededSteady} visits/inquiries per month` : "enter visit data above to estimate")), /*#__PURE__*/React.createElement("div", {
      className: "stat",
      style: {
        borderColor: color
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "stat-label"
    }, "To reach target in ", monthsToTarget, " mo"), /*#__PURE__*/React.createElement("div", {
      className: "stat-value",
      style: {
        color: color
      }
    }, calc.newClientsPerMonthRamp, " new clients/mo"), /*#__PURE__*/React.createElement("div", {
      className: "stat-note"
    }, calc.visitsNeededRamp != null ? `\u2248 ${calc.visitsNeededRamp} visits/inquiries per month` : "enter visit data above to estimate")));
    const targetRows = calc.channelTargets.map(t => /*#__PURE__*/React.createElement("tr", {
      key: t.key
    }, /*#__PURE__*/React.createElement("td", null, t.label), /*#__PURE__*/React.createElement("td", {
      className: "num-head strong"
    }, t.neededConverted), /*#__PURE__*/React.createElement("td", {
      className: "num-head muted"
    }, t.neededVisits != null ? t.neededVisits : "\u2014")));
    const targetTable = /*#__PURE__*/React.createElement("div", {
      className: "table-wrap"
    }, /*#__PURE__*/React.createElement("table", null, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Channel"), /*#__PURE__*/React.createElement("th", {
      className: "num-head"
    }, "New clients needed/mo"), /*#__PURE__*/React.createElement("th", {
      className: "num-head"
    }, "Visits/inquiries needed"))), /*#__PURE__*/React.createElement("tbody", null, targetRows)));
    return /*#__PURE__*/React.createElement("section", {
      className: "card"
    }, /*#__PURE__*/React.createElement("div", {
      className: "card-head"
    }, /*#__PURE__*/React.createElement("h2", null, "What you need next month"), /*#__PURE__*/React.createElement("p", null, "Based on last month's blended conversion rate (", /*#__PURE__*/React.createElement("b", null, (calc.blendedRate * 100).toFixed(1), "%"), " visit \u2192 client), here's the lead volume that keeps you afloat versus gets you to target.")), leadTargetCards, targetTable, /*#__PURE__*/React.createElement("p", {
      className: "pay-note"
    }, "Channel split assumes the same mix of where clients came from last month. If you plan to lean harder into one channel (e.g. more Psychology Today spend), adjust your expectations accordingly \u2014 this isn't a guarantee, just this month's math projected forward."));
  })());
}

function ExpensesTab({
  expenses,
  expMo,
  expYr,
  cur,
  color,
  setExpense,
  setExpenses,
  addExpense,
  removeExpense,
  renameExpense,
  rate,
  sessions,
  cityKey,
  setCityKey,
  manualCityFee,
  setManualCityFee,
  bizFee,
  grossTherYr
}) {
  const max = Math.max(...expenses.map(e => e.pct != null ? cur.grossMo * e.pct : +e.monthly || 0), 1);
  const expenseRows = expenses.map(function (e) {
    var effMonthly = e.pct != null ? cur.grossMo * e.pct : +e.monthly || 0;
    var inputEl;
    if (e.pct != null) {
      inputEl = /*#__PURE__*/React.createElement("div", {
        className: "exp-input exp-input-locked"
      }, /*#__PURE__*/React.createElement("span", {
        className: "exp-locked-val"
      }, (e.pct * 100).toFixed(1), "%"), /*#__PURE__*/React.createElement("span", {
        className: "exp-per"
      }, "of gross"));
    } else {
      inputEl = /*#__PURE__*/React.createElement("div", {
        className: "exp-input"
      }, /*#__PURE__*/React.createElement("span", null, "$"), /*#__PURE__*/React.createElement("input", {
        type: "number",
        min: 0,
        step: 5,
        value: e.monthly,
        onChange: function (ev) {
          setExpense(e.id, Math.max(0, +ev.target.value));
        }
      }), /*#__PURE__*/React.createElement("span", {
        className: "exp-per"
      }, "/mo"));
    }
    return /*#__PURE__*/React.createElement("div", {
      className: "exp-row",
      key: e.id
    }, /*#__PURE__*/React.createElement("div", {
      className: "exp-name"
    }, e.custom ? /*#__PURE__*/React.createElement("input", {
      className: "exp-rename",
      value: e.label,
      onChange: function (ev) {
        renameExpense(e.id, ev.target.value);
      }
    }) : /*#__PURE__*/React.createElement("span", {
      className: "exp-lbl"
    }, e.label), e.note && /*#__PURE__*/React.createElement("span", {
      className: "exp-note"
    }, e.note)), /*#__PURE__*/React.createElement("div", {
      className: "exp-bar"
    }, /*#__PURE__*/React.createElement("div", {
      className: "exp-bar-fill",
      style: {
        width: effMonthly / max * 100 + "%",
        background: color
      }
    })), inputEl, /*#__PURE__*/React.createElement("div", {
      className: "exp-yr"
    }, fmt(effMonthly * 12), /*#__PURE__*/React.createElement("span", null, "/yr")), e.custom ? /*#__PURE__*/React.createElement("button", {
      className: "exp-del",
      onClick: function () {
        removeExpense(e.id);
      },
      title: "Remove"
    }, "\u00D7") : /*#__PURE__*/React.createElement("span", {
      className: "exp-del-spacer"
    }));
  });
  const perSession = sessions > 0 ? expYr / (sessions * 52) : 0;
  const cityInfo = CITY_LICENSE[cityKey];
  const resetRow = /*#__PURE__*/React.createElement("div", {
    className: "residency-toggle",
    style: {
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "pill",
    onClick: () => setExpenses(xs => xs.map(e => ({
      ...e,
      monthly: 0,
      pct: e.pct != null ? 0 : e.pct
    })))
  }, "Set all to zero"), /*#__PURE__*/React.createElement("button", {
    className: "pill",
    onClick: () => setExpenses(DEFAULT_EXPENSES.map(e => ({
      ...e
    })))
  }, "Reset to starter estimates"));
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    className: "stats"
  }, /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: "Expenses / month",
    value: fmt(expMo),
    accent: "#26241E",
    note: `${expenses.length} categories`
  }), /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: "Expenses / year",
    value: fmt(expYr),
    accent: "#B5483F",
    note: `${fmt(perSession)} of every session hour`
  }), /*#__PURE__*/React.createElement("div", {
    className: "stat-col"
  }, /*#__PURE__*/React.createElement(Stat, {
    label: "True cost after deduction",
    value: fmt(cur.trueCostOfExpenses),
    note: "what it actually reduces take-home by"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Tax shield",
    value: "+" + fmt(cur.taxShield),
    note: "returned via lower taxable income"
  }))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "What it costs to keep the practice open"), /*#__PURE__*/React.createElement("p", null, "Enter monthly amounts. These are Schedule\xA0C deductions, so every dollar here lowers your taxable income — which is why the true cost is less than the sticker price.")), resetRow, /*#__PURE__*/React.createElement("div", {
    className: "exp-list"
  }, expenseRows), /*#__PURE__*/React.createElement("div", {
    className: "exp-foot"
  }, /*#__PURE__*/React.createElement("button", {
    className: "exp-add",
    onClick: addExpense
  }, "+ Add expense"), /*#__PURE__*/React.createElement("div", {
    className: "exp-total"
  }, /*#__PURE__*/React.createElement("span", null, "Total"), /*#__PURE__*/React.createElement("strong", null, fmt(expMo), /*#__PURE__*/React.createElement("em", null, "/mo")), /*#__PURE__*/React.createElement("strong", {
    style: {
      color
    }
  }, fmt(expYr), /*#__PURE__*/React.createElement("em", null, "/yr"))))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Why a $1 expense doesn't cost you $1"), /*#__PURE__*/React.createElement("p", null, "Business expenses come off your income before tax is calculated. At your current numbers, spending ", fmt(expYr), " reduces take-home by only ", fmt(cur.trueCostOfExpenses), " — the rest comes back as tax you no longer owe.")), /*#__PURE__*/React.createElement("div", {
    className: "shield"
  }, /*#__PURE__*/React.createElement("div", {
    className: "shield-bar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "shield-cost",
    style: {
      width: cur.trueCostOfExpenses / Math.max(expYr, 1) * 100 + "%"
    }
  }, /*#__PURE__*/React.createElement("span", null, fmt(cur.trueCostOfExpenses), " real cost")), /*#__PURE__*/React.createElement("div", {
    className: "shield-back",
    style: {
      width: cur.taxShield / Math.max(expYr, 1) * 100 + "%"
    }
  }, /*#__PURE__*/React.createElement("span", null, fmt(cur.taxShield), " tax shield"))), /*#__PURE__*/React.createElement("p", {
    className: "shield-note"
  }, "Effective: about ", Math.round(cur.taxShield / Math.max(expYr, 1) * 100), "% of every business dollar you spend is offset by reduced federal, CA, and self-employment tax."))));
}

// ---------- PROFIT TAB ----------
function ProfitTab({
  cur,
  color,
  rate,
  sessions,
  rates,
  rateData,
  sessionsList,
  expYr,
  expYrBase,
  job2Yr,
  setRate,
  job2On,
  cityKey,
  manualCityFee,
  filingStatus,
  numDependents,
  entityType,
  sCorpSalaryInput,
  taxStrategy
}) {
  const hypoBaseline = computeYear(cur.grossTherYr + (cur.otherIncomeYr || 0), expYrBase + cur.bizFee, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
  const hypoSolo401k = taxStrategy ? computeYear(cur.grossTherYr + (cur.otherIncomeYr || 0), expYrBase + cur.bizFee, job2Yr, filingStatus, numDependents, taxStrategy.solo401k.employerContrib, taxStrategy.solo401k.employeeContrib, entityType, sCorpSalaryInput) : null;
  const hypoSolo401kIra = taxStrategy ? computeYear(cur.grossTherYr + (cur.otherIncomeYr || 0), expYrBase + cur.bizFee, job2Yr, filingStatus, numDependents, taxStrategy.solo401k.employerContrib, taxStrategy.solo401k.employeeContrib + taxStrategy.traditionalIra.deductibleAmount, entityType, sCorpSalaryInput) : null;
  const waterfall = [{
    k: "Practice revenue",
    v: cur.grossTherYr,
    type: "in"
  }, {
    k: "Business expenses",
    v: -Math.round(expYrBase),
    type: "out"
  }, {
    k: "Self-employment tax",
    v: -Math.round(cur.seTax),
    type: "out"
  }, {
    k: "Federal income tax",
    v: -Math.round(cur.fedTax),
    type: "out"
  }, {
    k: "CA income tax",
    v: -Math.round(cur.caTax),
    type: "out"
  }];
  const maxAbs = Math.max(...waterfall.map(w => Math.abs(w.v)));
  const profitByRate = rates.map(r => {
    const g = r * sessions * 52;
    const fee = cityLicenseFee(cityKey, g, manualCityFee);
    return {
      rate: r,
      profit: Math.round(computeYear(g, expYrBase + fee, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput).net)
    };
  });
  const profitBySessions = sessionsList.map(s => {
    const g = rate * s * 52;
    const fee = cityLicenseFee(cityKey, g, manualCityFee);
    return {
      s,
      profit: Math.round(computeYear(g, expYrBase + fee, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput).net)
    };
  });
  const breakEven = (() => {
    for (let s = 1; s <= 60; s++) {
      const g = rate * s * 52;
      const fee = cityLicenseFee(cityKey, g, manualCityFee);
      if (computeYear(g, expYrBase + fee, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput).net > 0) return s;
    }
    return null;
  })();
  const fmtH = n => (n < 0 ? "\u2212$" : "$") + Math.abs(Math.round(n)).toLocaleString();
  const hypotheticalsSection = taxStrategy ? (function () {
    const rows = [{
      label: "Baseline (no retirement contribution)",
      contrib: 0,
      tax: hypoBaseline.totalTax,
      net: hypoBaseline.net
    }, {
      label: "Max Solo 401(k)",
      contrib: taxStrategy.solo401k.total,
      tax: hypoSolo401k.totalTax,
      net: hypoSolo401k.net
    }, {
      label: "Max Solo 401(k) + Traditional IRA",
      contrib: taxStrategy.solo401k.total + taxStrategy.traditionalIra.deductibleAmount,
      tax: hypoSolo401kIra.totalTax,
      net: hypoSolo401kIra.net
    }].map(row => /*#__PURE__*/React.createElement("tr", {
      key: row.label
    }, /*#__PURE__*/React.createElement("td", null, row.label), /*#__PURE__*/React.createElement("td", {
      className: "num-head strong"
    }, row.contrib === 0 ? "\u2014" : fmtH(row.contrib)), /*#__PURE__*/React.createElement("td", {
      className: "num-head neg"
    }, fmtH(row.tax)), /*#__PURE__*/React.createElement("td", {
      className: "num-head strong"
    }, fmtH(row.net)), /*#__PURE__*/React.createElement("td", {
      className: "num-head " + (row.net - hypoBaseline.net >= 0 ? "pos" : "neg")
    }, row.net - hypoBaseline.net === 0 ? "\u2014" : (row.net - hypoBaseline.net > 0 ? "+" : "\u2212") + fmtH(Math.abs(row.net - hypoBaseline.net)))));
    const table = /*#__PURE__*/React.createElement("div", {
      className: "table-wrap"
    }, /*#__PURE__*/React.createElement("table", null, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Scenario"), /*#__PURE__*/React.createElement("th", {
      className: "num-head"
    }, "Invested"), /*#__PURE__*/React.createElement("th", {
      className: "num-head"
    }, "Taxes paid"), /*#__PURE__*/React.createElement("th", {
      className: "num-head"
    }, "Bank account"), /*#__PURE__*/React.createElement("th", {
      className: "num-head"
    }, "vs. baseline"))), /*#__PURE__*/React.createElement("tbody", null, rows)));
    return /*#__PURE__*/React.createElement("section", {
      className: "card"
    }, /*#__PURE__*/React.createElement("div", {
      className: "card-head"
    }, /*#__PURE__*/React.createElement("h2", null, "If you maxed your tax strategy"), /*#__PURE__*/React.createElement("p", null, "Same practice profit (after expenses), three ways to split it: what moves into ", /*#__PURE__*/React.createElement("b", null, "tax-advantaged investments"), ", what goes to ", /*#__PURE__*/React.createElement("b", null, "taxes"), ", and what actually lands as ", /*#__PURE__*/React.createElement("b", null, "spendable cash"), " in your bank account. Invested + Taxes paid + Bank account always adds back up to your profit after expenses.")), table, /*#__PURE__*/React.createElement("p", {
      className: "pay-note"
    }, "Maxing both costs ", fmtH(taxStrategy.solo401k.total + taxStrategy.traditionalIra.deductibleAmount), " out of pocket this year, but ", fmtH(hypoBaseline.totalTax - hypoSolo401kIra.totalTax), " of that is tax you'd have paid anyway \u2014 so the real cash trade-off is smaller than the sticker price on the contribution."));
  })() : null;
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    className: "stats"
  }, /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: "Net profit / year",
    value: fmt(cur.netYr),
    accent: color,
    note: `after ${fmt(cur.expYr)} expenses and ${fmt(Math.round(cur.totalTax))} tax`
  }), /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: "Net profit / month",
    value: fmt(cur.netMo),
    accent: "#26241E",
    note: `${fmt(cur.netWk)} per week`
  }), /*#__PURE__*/React.createElement("div", {
    className: "stat-col"
  }, /*#__PURE__*/React.createElement(Stat, {
    label: "Profit margin",
    value: Math.round(cur.marginPct * 100) + "%",
    note: "of every gross dollar"
  }), /*#__PURE__*/React.createElement(Stat, {
    label: "Break-even caseload",
    value: breakEven ? breakEven + " / wk" : "—",
    note: `sessions to clear costs at $${rate}/hr`
  }))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Where every dollar goes"), /*#__PURE__*/React.createElement("p", null, "Starting from what you bill, subtracting what you spend and what you owe. What's left is yours.")), /*#__PURE__*/React.createElement("div", {
    className: "wf"
  }, waterfall.map((w, i) => /*#__PURE__*/React.createElement("div", {
    className: "wf-row",
    key: i
  }, /*#__PURE__*/React.createElement("span", {
    className: "wf-k"
  }, w.k), /*#__PURE__*/React.createElement("div", {
    className: "wf-track"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wf-bar " + (w.type === "in" ? "wf-in" : "wf-out"),
    style: {
      width: Math.abs(w.v) / maxAbs * 100 + "%",
      background: w.type === "in" ? color : undefined
    }
  })), /*#__PURE__*/React.createElement("span", {
    className: "wf-v " + (w.type === "in" ? "pos" : "neg")
  }, w.v > 0 ? "+" : "\u2212", fmt(Math.abs(w.v))))), /*#__PURE__*/React.createElement("div", {
    className: "wf-row wf-final"
  }, /*#__PURE__*/React.createElement("span", {
    className: "wf-k"
  }, "Net profit"), /*#__PURE__*/React.createElement("div", {
    className: "wf-track"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wf-bar",
    style: {
      width: cur.netYr / maxAbs * 100 + "%",
      background: color
    }
  })), /*#__PURE__*/React.createElement("span", {
    className: "wf-v",
    style: {
      color
    }
  }, fmt(cur.netYr))))), /*#__PURE__*/React.createElement("section", {
    className: "two-up"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Profit by rate"), /*#__PURE__*/React.createElement("p", null, "At ", sessions, " sessions a week, holding expenses fixed.")), /*#__PURE__*/React.createElement(ResponsiveContainer, {
    width: "100%",
    height: 260
  }, /*#__PURE__*/React.createElement(BarChart, {
    data: profitByRate,
    margin: {
      top: 6,
      right: 8,
      left: 8,
      bottom: 4
    }
  }, /*#__PURE__*/React.createElement(CartesianGrid, {
    stroke: "#E7E2D6",
    vertical: false
  }), /*#__PURE__*/React.createElement(XAxis, {
    dataKey: "rate",
    tickFormatter: v => "$" + v,
    tick: {
      fill: "#6F6A5E",
      fontSize: 11
    },
    tickLine: false,
    axisLine: {
      stroke: "#D8D2C4"
    }
  }), /*#__PURE__*/React.createElement(YAxis, {
    tickFormatter: fmtK,
    tick: {
      fill: "#6F6A5E",
      fontSize: 11
    },
    tickLine: false,
    axisLine: false,
    width: 48
  }), /*#__PURE__*/React.createElement(Tooltip, {
    content: /*#__PURE__*/React.createElement(ProfitTip, {
      label1: "rate"
    })
  }), /*#__PURE__*/React.createElement(Bar, {
    dataKey: "profit",
    radius: [3, 3, 0, 0]
  }, profitByRate.map((p, i) => /*#__PURE__*/React.createElement(Cell, {
    key: i,
    fill: p.rate === rate ? rateData[p.rate].color : rateData[p.rate].color + "55"
  })))))), /*#__PURE__*/React.createElement("div", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Profit by caseload"), /*#__PURE__*/React.createElement("p", null, "At $", rate, "/hr. The line crosses zero at your break-even point.")), /*#__PURE__*/React.createElement(ResponsiveContainer, {
    width: "100%",
    height: 260
  }, /*#__PURE__*/React.createElement(AreaChart, {
    data: profitBySessions,
    margin: {
      top: 6,
      right: 8,
      left: 8,
      bottom: 4
    }
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: "profFill",
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0%",
    stopColor: color,
    stopOpacity: 0.35
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "100%",
    stopColor: color,
    stopOpacity: 0.02
  }))), /*#__PURE__*/React.createElement(CartesianGrid, {
    stroke: "#E7E2D6",
    vertical: false
  }), /*#__PURE__*/React.createElement(XAxis, {
    dataKey: "s",
    tick: {
      fill: "#6F6A5E",
      fontSize: 11
    },
    tickLine: false,
    axisLine: {
      stroke: "#D8D2C4"
    },
    interval: 2
  }), /*#__PURE__*/React.createElement(YAxis, {
    tickFormatter: fmtK,
    tick: {
      fill: "#6F6A5E",
      fontSize: 11
    },
    tickLine: false,
    axisLine: false,
    width: 48
  }), /*#__PURE__*/React.createElement(Tooltip, {
    content: /*#__PURE__*/React.createElement(ProfitTip, {
      label1: "sessions"
    })
  }), /*#__PURE__*/React.createElement(ReferenceLine, {
    y: 0,
    stroke: "#B5483F",
    strokeDasharray: "4 3"
  }), /*#__PURE__*/React.createElement(ReferenceLine, {
    x: sessions,
    stroke: color,
    strokeDasharray: "5 4"
  }), /*#__PURE__*/React.createElement(Area, {
    type: "monotone",
    dataKey: "profit",
    stroke: color,
    strokeWidth: 2.5,
    fill: "url(#profFill)",
    dot: false
  }))))), /*#__PURE__*/React.createElement("section", {
    className: "card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Monthly profit at a glance"), /*#__PURE__*/React.createElement("p", null, "Your net profit divided across the year, and what it means per session hour actually worked.")), /*#__PURE__*/React.createElement("div", {
    className: "strip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Profit / month"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v",
    style: {
      color
    }
  }, fmt(cur.netMo)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, fmt(cur.netYr), " per year")), /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Profit / week"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.netWk)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "across ", sessions, " sessions")), /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Per session hour"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(sessions > 0 ? cur.netYr / (sessions * 52) : 0)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "of your $", rate, " billed rate")))), hypotheticalsSection);
}
function ProfitTip({
  active,
  payload,
  label,
  label1
}) {
  if (!active || !payload?.length) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "tip"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tip-head"
  }, label1 === "rate" ? "$" + label + "/hr" : label + " sessions / week"), /*#__PURE__*/React.createElement("div", {
    className: "tip-row"
  }, /*#__PURE__*/React.createElement("span", {
    className: "tip-name"
  }, "net profit"), /*#__PURE__*/React.createElement("span", {
    className: "tip-val"
  }, fmt(payload[0].value))));
}
const CSS = `
.planner{
  --bg:#FBF9F3; --ink:#26241E; --muted:#7C766A; --line:#E7E2D6;
  --card:#FFFFFF; --pos:#3F9577; --neg:#B5483F;
  background:var(--bg); color:var(--ink);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  max-width:1080px; margin:0 auto; padding:32px 24px 60px;
  -webkit-font-smoothing:antialiased;
}
.planner *{box-sizing:border-box;}

/* hero */
.hero{padding:14px 0 18px; border-bottom:1px solid var(--line); margin-bottom:18px;}
.hero-eyebrow{font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); font-weight:600; margin-bottom:8px;}
.hero-title{
  font-family:'Fraunces','Georgia',serif; font-weight:600;
  font-size:clamp(26px,3.2vw,38px); line-height:1.06; letter-spacing:-.02em; margin:0 0 9px;
}
.hero-title .accent{color:#B5483F;}
.hero-sub{font-size:14.5px; line-height:1.5; color:var(--muted); max-width:640px; margin:0;}

/* controls */
.controls{
  display:grid; grid-template-columns:1.3fr 1fr; gap:28px; align-items:end;
  background:var(--card); border:2px solid var(--line); border-radius:16px;
  padding:26px 24px 22px; margin-bottom:28px; position:relative;
  box-shadow:0 2px 10px rgba(40,36,30,.06);
}
.controls-badge{position:absolute; top:-12px; left:22px; background:#26241E; color:#fff; font-size:10.5px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; padding:4px 11px; border-radius:20px;}
.control-label{font-size:13px; font-weight:600; color:var(--muted); margin-bottom:12px; display:flex; justify-content:space-between; align-items:baseline;}
.control-val{font-family:'Fraunces',serif; font-size:22px; color:var(--ink); font-weight:600;}
.control-val-wrap{font-family:'Fraunces',serif; font-size:22px; color:var(--ink); font-weight:600; display:inline-flex; align-items:baseline; gap:2px;}
.control-val-input{font-family:'Fraunces',serif; font-size:22px; color:var(--ink); font-weight:600; border:1.5px solid #E4D9BE; border-radius:6px; width:100px; text-align:right; padding:4px 8px; background:#FBF6E9; -moz-appearance:textfield;}
.control-val-input:hover{border-color:var(--line);}
.control-val-input:focus{outline:none; border-color:#B5483F; background:#fff;}
.control-val-input::-webkit-inner-spin-button,.control-val-input::-webkit-outer-spin-button{opacity:0.4;}
.rate-pills{display:flex; gap:7px; flex-wrap:wrap;}
.pill{
  font:inherit; font-weight:600; font-size:14px; padding:8px 14px; cursor:pointer;
  background:#fff; border:1.5px solid var(--line); border-radius:10px; color:var(--ink);
  transition:all .14s ease;
}
.pill:hover{border-color:#C7C0AF;}
.pill-on{color:#fff !important;}
.slider{width:100%; height:6px; cursor:pointer;}
.slider-ends{display:flex; justify-content:space-between; font-size:11px; color:var(--muted); margin-top:6px;}

/* second job module */
.job2{background:var(--card); border:1px solid var(--line); border-radius:16px; padding:20px 24px; margin-bottom:28px; box-shadow:0 1px 2px rgba(40,36,30,.03);}
.job2-head{display:flex; justify-content:space-between; align-items:center;}
.job2-title{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;}
.job2-title h3{font-family:'Fraunces',serif; font-weight:600; font-size:19px; margin:0;}
.job2-tag{font-size:12px; color:var(--muted);}
.toggle{display:inline-flex; align-items:center; gap:9px; border:1px solid var(--line); background:#FAF7F0; border-radius:22px; padding:5px 12px 5px 6px; cursor:pointer; font:inherit; font-size:12px; font-weight:600; color:var(--muted); transition:all .16s;}
.toggle-knob{width:16px; height:16px; border-radius:50%; background:#C7C0AF; transition:all .16s;}
.toggle-on{background:#EFF5F0; border-color:#9FC4AF; color:#3F9577;}
.toggle-on .toggle-knob{background:#3F9577;}
.job2-body{display:grid; grid-template-columns:1fr 1.2fr 1.4fr; gap:24px; margin-top:20px; align-items:start;}
.job2-field label{font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); display:flex; justify-content:space-between; align-items:baseline; margin-bottom:10px;}
.job2-val{font-family:'Fraunces',serif; font-size:18px; color:var(--ink);}
.job2-input{display:flex; align-items:center; gap:3px; border:1.5px solid #E4D9BE; border-radius:10px; padding:9px 13px; font-family:'Fraunces',serif; font-size:20px; font-weight:600; background:#FBF6E9; transition:border-color .15s;}
.job2-input:hover{border-color:#C9A876;}
.job2-input:focus-within{border-color:#B5483F;}
.job2-input span{color:var(--muted);}
.job2-input input{border:none; outline:none; font:inherit; width:100%; background:transparent; color:var(--ink);}
.job2-unit{font-size:13px !important; font-family:'Inter',sans-serif;}
.job2-summary{background:#FCFAF4; border:1px solid var(--line); border-radius:12px; padding:14px 16px;}
.job2-sum-row{display:flex; justify-content:space-between; align-items:baseline; padding:4px 0; font-size:14px; color:var(--muted);}
.job2-sum-row strong{font-family:'Fraunces',serif; font-size:17px; color:var(--ink);}
.job2-sum-note{font-size:11px; color:var(--muted); line-height:1.4; margin-top:8px; padding-top:8px; border-top:1px solid var(--line);}

/* stats */
.stats{display:grid; grid-template-columns:1.3fr 1.3fr 1fr; gap:14px; margin-bottom:14px; align-items:stretch;}
.residency-grid{display:grid; grid-template-columns:repeat(auto-fill, minmax(220px, 1fr)); gap:14px; align-items:start;}
.residency-toggle{display:flex; gap:8px; margin-bottom:16px; flex-wrap:wrap;}
.residency-includes{font-size:11px; color:var(--muted); line-height:1.5; margin-top:10px; padding-top:10px; border-top:1px solid var(--line);}
.residency-includes b{color:var(--ink); font-weight:600;}
.resid-bars{margin:12px 0; padding-top:10px; border-top:1px solid var(--line);}
.resid-bar-row{display:flex; align-items:center; gap:8px; margin-bottom:6px;}
.resid-bar-label{width:60px; font-size:11px; color:var(--muted); flex-shrink:0;}
.resid-bar-track{flex:1; background:#EFEAE0; border-radius:5px; overflow:hidden; height:14px;}
.resid-bar{height:100%; border-radius:5px; min-width:6px; box-sizing:border-box; transition:width .3s;}
.resid-bar-val{width:76px; text-align:right; flex-shrink:0; font-family:'Fraunces',serif; font-weight:700; font-size:13px; color:var(--ink);}
.resid-invest-note{font-size:12px; color:var(--muted); line-height:1.5; margin-bottom:10px; padding:8px 10px; background:#F3F0E7; border-radius:8px;}
.resid-invest-note b{color:var(--ink);}
/* ---- Grow Your Practice page ---- */
.planner.grow-mode .hero,
.planner.grow-mode .guided-jumpnav,
.planner.grow-mode .sticky-summary,
.planner.grow-mode .sticky-summary-tab{display:none !important;}
.growhero{padding:14px 0 20px; border-bottom:1px solid var(--line); margin-bottom:20px;}
.growrate{margin-top:24px; background:#FBF6E9; border:1px solid #E4D9BE; border-radius:12px;
  padding:14px 16px; max-width:560px;}
.growrate-lbl{display:block; font-size:10.5px; font-weight:700; text-transform:uppercase;
  letter-spacing:.06em; color:var(--muted); margin-bottom:8px;}
.growrate-fields{display:flex; gap:26px; flex-wrap:wrap;}
.growrate-field{display:flex; flex-direction:column;}
.growrate-row{display:flex; align-items:center; gap:7px; flex-wrap:wrap;}
.growrate-derived{font-size:13px; color:var(--ink); margin-top:13px; padding-top:11px;
  border-top:1px dashed #E4D9BE; line-height:1.5;}
.growrate-derived b{font-family:'Fraunces',serif; font-size:15px;}
.growrate-cur{font-family:'Fraunces',serif; font-size:20px; font-weight:700;}
.growrate-input{width:110px; font-family:'Fraunces',serif; font-size:20px; font-weight:700;
  padding:6px 9px; border-radius:8px; border:1.5px solid #E4D9BE; background:#fff; color:var(--ink);}
.growrate-unit{font-size:14px; color:var(--muted); margin-right:4px;}
.growrate-reset{margin-top:12px; font-family:inherit; font-size:11.5px; font-weight:600; color:#8A5A26;
  background:#FAEEDA; border:1px solid #E8D3A8; border-radius:8px; padding:6px 11px; cursor:pointer;}
.growrate-reset:hover{background:#F3E0B8;}
.growrate-note{font-size:12px; color:var(--muted); margin:9px 0 0; line-height:1.5;}
@media (max-width:640px){ .growrate-input{width:92px;} }

/* ===== Grow Your Practice — editorial landing ===== */
.growlanding{margin:0 0 30px;}
.growlanding-h{font-family:'Fraunces',serif; font-weight:700; font-size:26px; letter-spacing:-.015em;
  margin:0 0 9px;}
.growlanding-h2{margin-top:38px;}
.growlanding-lede{font-size:15px; line-height:1.65; color:var(--muted); max-width:660px; margin:0 0 20px;}
.growcards{display:grid; grid-template-columns:repeat(3,1fr); gap:16px;}
.growcard{background:#fff; border:1px solid var(--line); border-radius:12px; padding:18px 20px;
  display:flex; flex-direction:column;}
.growcard-n{font-family:'Fraunces',serif; font-weight:700; font-size:12px; color:var(--amber);
  letter-spacing:.06em; margin-bottom:7px;}
.growcard h3{font-family:'Fraunces',serif; font-weight:700; font-size:17px; letter-spacing:-.01em;
  margin:0 0 8px; line-height:1.2;}
.growcard p{font-size:13.5px; line-height:1.6; color:var(--muted); margin:0 0 10px;}
.growcard-calc{margin:auto 0 0 !important; padding-top:11px; border-top:1px dashed var(--line);
  color:var(--ink) !important; font-size:13px !important;}
.growcard-calc b{font-family:'Fraunces',serif;}
.growcard-calc-empty{color:var(--muted) !important; font-style:italic;}

/* the therapy year */
.season{border:1px solid var(--line); border-radius:12px; overflow:hidden; background:#fff;}
.season-row{display:grid; grid-template-columns:96px 74px 1fr; gap:14px; align-items:baseline;
  padding:12px 18px; border-top:1px solid var(--line);}
.season-row:first-child{border-top:none;}
.season-period{font-family:'Fraunces',serif; font-weight:700; font-size:14px;}
.season-tag{font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:.06em;
  padding:3px 8px; border-radius:20px; text-align:center;}
.season-busy .season-tag{background:#E6F1EB; color:var(--pos);}
.season-quiet .season-tag{background:#FBEAE8; color:var(--neg);}
.season-steady .season-tag{background:#F1EDE3; color:var(--muted);}
.season-note{font-size:13.5px; line-height:1.55; color:var(--muted);}
.growlanding-cost{background:#FDF8EF; border-left:3px solid var(--amber); border-radius:0 8px 8px 0;
  padding:14px 17px; margin:18px 0 0; font-size:14px; line-height:1.6;}
.growlanding-cost b{font-family:'Fraunces',serif;}
.growlanding-bridge{font-size:14.5px; line-height:1.6; color:var(--muted); margin:22px 0 0;
  padding-top:18px; border-top:1px solid var(--line); max-width:680px;}
@media (max-width:820px){ .growcards{grid-template-columns:1fr;} }
@media (max-width:560px){
  .season-row{grid-template-columns:1fr; gap:5px;}
  .season-tag{justify-self:start;}
  .growlanding-h{font-size:22px;}
}

/* ===== Section landing headers ===== */
/* jumps must clear the sticky nav, or you arrive underneath it */
.planner #sec-income,.planner #sec-expenses,.planner #sec-profit,
.planner #sec-taxstrategy,.planner #sec-residency,.planner #sec-funnel{scroll-margin-top:86px;}
.sec-intro{border-top:2px solid var(--ink); padding:18px 0 4px; margin:34px 0 18px;}
.sec-intro-top{display:flex; align-items:baseline; justify-content:space-between; gap:16px;
  flex-wrap:wrap; margin-bottom:7px;}
.sec-intro-kicker{font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:.08em;
  color:var(--muted);}
.sec-intro-stat{font-family:'Fraunces',serif; font-weight:700; font-size:14px; color:var(--ink);}
.sec-intro-title{font-family:'Fraunces',serif; font-weight:700; font-size:30px; line-height:1.05;
  letter-spacing:-.02em; margin:0 0 8px;}
.sec-intro-blurb{font-size:14.5px; line-height:1.6; color:var(--muted); max-width:640px; margin:0;}
/* the first section shouldn't push the page down */
.planner #sec-income .sec-intro{margin-top:0;}

/* arrival feedback: the jumped-to section announces itself briefly */
@keyframes secArrive{
  0%{background:#FBF3E2; border-top-color:var(--amber);}
  70%{background:#FBF3E2; border-top-color:var(--amber);}
  100%{background:transparent; border-top-color:var(--ink);}
}
#sec-income:target .sec-intro,#sec-expenses:target .sec-intro,
#sec-profit:target .sec-intro,#sec-taxstrategy:target .sec-intro{
  animation:secArrive 1.6s ease-out;}
@media (prefers-reduced-motion:reduce){
  #sec-income:target .sec-intro,#sec-expenses:target .sec-intro,
  #sec-profit:target .sec-intro,#sec-taxstrategy:target .sec-intro{animation:none;}
}
@media (max-width:640px){
  .sec-intro-title{font-size:24px;}
  .sec-intro{margin:26px 0 14px;}
}

/* ===== What I keep opener ===== */
.keepwrap{background:#fff; border:1px solid #E7E2D6; border-radius:12px; padding:26px 24px; margin:0 0 18px;}
.keephero{text-align:center;}
.keep-eyebrow{font-size:11px; letter-spacing:.09em; text-transform:uppercase; color:#7C766A; font-weight:600;}
.keep-big{font-family:Fraunces,Georgia,serif; font-size:58px; line-height:1.02; font-weight:600; color:#3F9577; margin:6px 0 0;}
.keep-sub{color:#7C766A; font-size:15px; margin-top:6px;}
.keep-bar{display:flex; height:48px; border-radius:10px; overflow:hidden; margin:22px 0 10px; border:1px solid #E7E2D6;}
.keep-bar i{display:flex; align-items:center; justify-content:center; font-size:11.5px; font-weight:600; color:#fff; letter-spacing:.03em; white-space:nowrap; overflow:hidden;}
.kb-exp{background:#B99A63;} .kb-tax{background:#B5483F;} .kb-net{background:#3F9577;}
.keep-legend{display:flex; gap:18px; flex-wrap:wrap; font-size:13px; color:#4A463D;}
.keep-legend span{display:flex; align-items:center; gap:7px;}
.kdot{width:11px; height:11px; border-radius:3px; display:inline-block; flex:0 0 11px;}
.keep-chain{font-size:14px; color:#4A463D; margin-top:16px; line-height:2;}
.keep-chain b{font-family:Fraunces,Georgia,serif; font-variant-numeric:tabular-nums;}
.keep-units{display:flex; gap:12px; flex-wrap:wrap; margin-top:18px;}
.keep-unit{flex:1 1 140px; border:1px solid #E7E2D6; border-radius:10px; padding:13px;}
.keep-unit h4{margin:0 0 5px; font-size:11px; letter-spacing:.07em; text-transform:uppercase; color:#7C766A;}
.keep-unit-v{font-family:Fraunces,Georgia,serif; font-size:24px; font-weight:600; font-variant-numeric:tabular-nums;}
.keep-unit span{font-size:12.5px; color:#7C766A;}
/* ===== payroll mechanic ===== */
.mechanic{border:1px solid #E7E2D6; border-radius:12px; background:#fff; padding:18px 20px; margin:0 0 16px;}
.mechanic h4{font-family:Fraunces,Georgia,serif; font-size:18px; margin:0 0 8px;}
.mechanic h5{font-family:Fraunces,Georgia,serif; font-size:15px; margin:0 0 8px;}
.mech-cols{display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:14px 0;}
.mech-stack{border:1px solid #E7E2D6; border-radius:10px; overflow:hidden;}
.mech-stack i{display:flex; align-items:center; justify-content:space-between; gap:10px; padding:9px 12px; font-size:12.5px; color:#fff; font-style:normal;}
.mech-stack i b{font-variant-numeric:tabular-nums; white-space:nowrap;}
.m-ss{background:#B5483F;} .m-med{background:#C97F63;} .m-sdi{background:#D8A98F;} .m-inc{background:#7C766A;}
.m-none{background:#EAF3EE; color:#2C6B53 !important; font-weight:600; justify-content:center !important; padding:20px 12px !important; text-align:center;}
.mech-foot{font-size:12.5px; color:#7C766A; margin:8px 0 0;}
.mech-yours{border-top:1px solid #E7E2D6; margin-top:16px; padding-top:14px;}
.mech-row{display:flex; justify-content:space-between; gap:14px; align-items:flex-start; padding:9px 0; border-bottom:1px solid #F1EDE3; font-size:13.5px;}
.mech-row b{font-family:Fraunces,Georgia,serif; font-variant-numeric:tabular-nums; white-space:nowrap;}
.mech-tot{border-top:2px solid #26241E; border-bottom:2px solid #26241E; font-size:15px;}
.mech-bar{display:flex; height:40px; border-radius:9px; overflow:hidden; border:1px solid #E7E2D6; margin:14px 0 6px;}
.mech-bar i{display:flex; align-items:center; justify-content:center; color:#fff; font-size:12px; font-weight:600; font-style:normal; white-space:nowrap; overflow:hidden;}
.mech-cliff-wrap{border-top:1px solid #E7E2D6; margin-top:16px; padding-top:14px;}
.mech-cliff{display:flex; align-items:flex-end; height:96px; gap:3px;}
.mech-cliff i{display:flex; align-items:center; justify-content:center; color:#fff; font-size:12px; font-weight:600; font-style:normal; border-radius:6px 6px 0 0;}
.cliff-hi{flex:0 0 60%; height:100%; background:#B5483F;}
.cliff-lo{flex:1; height:19%; background:#C97F63; font-size:11px !important;}
.mech-cliff-lab{display:flex; justify-content:space-between; font-size:11.5px; color:#7C766A; margin-top:6px;}
@media (max-width:700px){
  .keep-big{font-size:40px;}
  .mech-cols{grid-template-columns:1fr;}
  .keep-chain{font-size:13px;}
}

/* ===== S-corp salary guidance + compliance ===== */
.extlink{color:#26241E; text-decoration:underline; text-underline-offset:2px; text-decoration-color:#C0B9A6;}
.extlink:hover{text-decoration-color:#26241E;}
.salguide,.compliance{border:1px solid #E7E2D6; border-radius:12px; background:#fff; padding:18px 20px; margin:0 0 16px;}
.salguide h4,.compliance h4{font-family:Fraunces,Georgia,serif; font-size:18px; margin:0 0 8px;}
.salguide-lede{margin:0 0 14px; color:#5C574C; font-size:14px; line-height:1.6;}
.salguide-meter{display:flex; gap:3px; margin-bottom:12px;}
.salguide-seg{flex:1; height:8px; border-radius:4px; opacity:.28;}
.salguide-seg.on{opacity:1; height:12px; margin-top:-2px;}
.salguide-verdict{display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:8px;}
.salguide-badge{color:#fff; font-size:11px; font-weight:600; letter-spacing:.05em; text-transform:uppercase; padding:4px 10px; border-radius:20px;}
.salguide-verdict b{font-family:Fraunces,Georgia,serif; font-size:15px;}
.salguide-what{margin:0 0 4px; font-size:14px;}
.salguide-cost{margin:0 0 14px; font-size:13.5px; color:#7C766A;}
.salguide-scale{border-top:1px solid #E7E2D6; margin-top:6px;}
.salguide-row{display:flex; align-items:center; gap:12px; padding:7px 8px; border-bottom:1px solid #F1EDE3; font-size:13.5px; border-radius:6px;}
.salguide-row.on{background:#F6F2E8;}
.salguide-range{flex:0 0 82px; font-family:Fraunces,Georgia,serif; font-weight:600; font-variant-numeric:tabular-nums;}
.salguide-name{flex:1;}
.salguide-amt{color:#7C766A; font-variant-numeric:tabular-nums;}
.salguide-fine{font-size:12.5px; color:#7C766A; margin:12px 0 0; line-height:1.55;}
.salguide-deep{margin-top:14px; border-top:1px solid #E7E2D6; padding-top:12px;}
.salguide-deep summary{cursor:pointer; font-weight:600; font-size:14px;}
.salguide-deep p{font-size:13.5px; line-height:1.65; color:#3D3A33;}
.salguide-case{background:#FBF1E2; border-left:3px solid #C98B4B; border-radius:0 8px 8px 0; padding:12px 14px; font-size:13.5px; line-height:1.65; margin:12px 0;}
.compliance-cols{display:grid; grid-template-columns:1fr 1fr; gap:20px;}
.compliance-col h5{font-family:Fraunces,Georgia,serif; font-size:14px; margin:0 0 6px; text-transform:uppercase; letter-spacing:.06em; color:#7C766A;}
.compliance-col ul{margin:0; padding-left:18px;}
.compliance-col li{font-size:13.5px; line-height:1.6; margin-bottom:7px;}
.compliance-goodnews{background:#EAF3EE; border-left:3px solid #3F9577; border-radius:0 8px 8px 0; padding:12px 14px; font-size:13.5px; line-height:1.65; margin:16px 0 0;}
.runcost{border-top:1px solid #E7E2D6;}
.runcost-row{display:flex; align-items:center; gap:12px; padding:10px 0; border-bottom:1px solid #F1EDE3; flex-wrap:wrap;}
.runcost-lbl{flex:1 1 260px; min-width:200px;}
.runcost-lbl b{display:block; font-size:14px;}
.runcost-lbl span{display:block; font-size:12.5px; color:#7C766A; line-height:1.5;}
.runcost-row input{width:110px; font-family:Fraunces,Georgia,serif; font-size:16px; font-weight:600; padding:7px 10px; border:1px solid #E4D9BE; background:#FBF6E9; border-radius:8px; color:#26241E;}
.runcost-use{font-size:12px; font-weight:600; padding:7px 10px; border-radius:7px; border:1px solid #E7E2D6; background:#fff; cursor:pointer; color:#5C574C; white-space:nowrap;}
.runcost-use:hover{border-color:#C98B4B; color:#26241E;}
.runcost-total{font-size:13.5px; margin:12px 0 0; color:#3D3A33;}
@media (max-width:700px){
  .compliance-cols{grid-template-columns:1fr; gap:14px;}
  .salguide-range{flex:0 0 66px; font-size:12.5px;}
  .runcost-row input{width:100%;}
}

/* ===== Both structures, side by side ===== */
.struct-table{width:100%; border-collapse:collapse;}
.struct-table th{padding:0 0 10px; vertical-align:bottom;}
.struct-col{width:22%; padding:0 4px !important;}
.struct-colbtn{display:flex; flex-direction:column; gap:2px; width:100%; text-align:left;
  font-family:inherit; cursor:pointer; background:#fff; border:1.5px solid var(--line);
  border-radius:10px; padding:9px 12px; transition:border-color .15s, background .15s;}
.struct-colbtn:hover{background:#FCFAF4; border-color:#C9A876;}
.struct-col-on .struct-colbtn{background:#F3F7F4; border-color:var(--pos); border-width:2px;}
.struct-coltitle{font-family:'Fraunces',serif; font-weight:700; font-size:14px; color:var(--ink); line-height:1.15;}
.struct-colsub{font-size:10px; color:var(--muted); line-height:1.25;}
.struct-colpick{font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:.05em;
  color:var(--muted); margin-top:3px;}
.struct-col-on .struct-colpick{color:var(--pos);}
.struct-table tbody td{padding:10px 8px; border-top:1px solid var(--line); font-size:14px; vertical-align:top;}
.struct-lbl{display:block; font-weight:600; font-size:13.5px;}
.struct-hint{display:block; font-size:11px; color:var(--muted); margin-top:2px; line-height:1.35;}
.struct-grp td{background:#F6F2E8; font-size:10px; font-weight:700; text-transform:uppercase;
  letter-spacing:.07em; color:var(--muted); padding:7px 10px !important; border-top:1px solid var(--line);}
.struct-cell-on{background:#F3F7F4;}
.struct-big td{font-size:15px;}
.struct-big .num-head{font-family:'Fraunces',serif; font-weight:700; font-size:19px;}
.struct-table .num-head.pos{color:var(--pos);}
.struct-table .num-head.neg{color:var(--neg);}
@media (max-width:720px){
  .struct-table{font-size:12.5px;}
  .struct-coltitle{font-size:12px;}
  .struct-colsub,.struct-colpick{display:none;}
  .struct-table tbody td{padding:8px 5px;}
  .struct-big .num-head{font-size:16px;}
}

/* ================= LAYOUT VARIANTS (?v=01..04) ================= */

/* --- 01 · title lives in the masthead, hero deleted --- */
.planner.v01 .hero{padding:10px 0 0; border-bottom:none; margin-bottom:8px;}
.planner.v01 .hero-eyebrow,.planner.v01 .hero-title{display:none;}
.planner.v01 .hero-sub{font-size:14px; max-width:640px;}
.planner.v01 .sitenav{justify-content:space-between;}
.planner.v01 .sitenav-mark{flex-direction:column; align-items:flex-start; gap:1px;}
.planner.v01 .sitenav-mark{display:grid; grid-template-columns:auto auto; column-gap:9px; align-items:center;}
.planner.v01 .sitenav-mono{grid-row:1 / span 2;}
.v01-tagline{font-size:9.5px; color:#A39C8E; line-height:1.2;}

/* --- 02 · hero holds the running total instead of a floating panel --- */
.planner.v02 .hero{display:grid; grid-template-columns:1fr 208px; column-gap:26px; align-items:start;}
.planner.v02 .hero-eyebrow,.planner.v02 .hero-title,.planner.v02 .hero-sub{grid-column:1;}
.planner.v02 .sticky-summary,.planner.v02 .sticky-summary-tab{display:none !important;}
.v02-kpi{grid-column:2; grid-row:1 / span 3; background:#fff; border:1px solid var(--line);
  border-radius:12px; padding:13px 15px; align-self:start;}
.v02-kpi-row{display:flex; justify-content:space-between; align-items:baseline; gap:12px; padding:2px 0;}
.v02-kpi-row .k{font-size:10.5px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em;}
.v02-kpi-row .v{font-family:'Fraunces',serif; font-weight:700; font-size:14px;}
.v02-kpi-row .v.neg{color:var(--neg);}
.v02-kpi-row.net{border-top:1px solid var(--line); margin-top:6px; padding-top:7px;}
.v02-kpi-row.net .v{font-size:19px; color:#5B7C99;}
.v02-kpi-note{font-size:11px; color:var(--muted); margin:9px 0 0; line-height:1.4;}

/* --- 03 · sections become a vertical rail --- */
.planner.v03{padding-left:212px;}
.planner.v03 .sitenav{margin-left:-212px; padding-left:24px;}
.planner.v03 .guided-jumpnav{position:fixed; left:0; top:64px; bottom:0; width:190px;
  flex-direction:column; align-items:stretch; gap:3px; overflow-y:auto;
  background:#FCFAF4; border-right:1px solid var(--line); border-bottom:none;
  padding:14px 12px; z-index:30;}
.planner.v03 .jumpnav-group{flex-direction:column; align-items:stretch; gap:3px; width:100%;}
.planner.v03 .jumpnav-group-lbl{margin:0 0 7px 8px;}
.planner.v03 .jumpnav-divider{display:none;}
.planner.v03 .jumpnav-pill{flex-direction:row; justify-content:space-between; align-items:baseline;
  border-radius:8px; border:none; background:transparent; padding:7px 9px;}
.planner.v03 .jumpnav-pill:hover{background:#F1EDE3;}
.planner.v03 .jumpnav-pill.jumpnav-active{background:var(--ink);}
.planner.v03 .sticky-summary{top:auto; bottom:18px; right:18px;}
@media (max-width:900px){
  .planner.v03{padding-left:24px;}
  .planner.v03 .sitenav{margin-left:-24px;}
  .planner.v03 .guided-jumpnav{position:static; width:auto; flex-direction:row; border-right:none;
    border-bottom:1px solid var(--line); background:rgba(251,249,243,.95);}
  .planner.v03 .jumpnav-group{flex-direction:row; width:auto;}
  .planner.v03 .jumpnav-pill{flex-direction:column; justify-content:flex-start;}
}

/* --- 04 · ask first, reveal after --- */
.planner.v04-empty .guided-jumpnav,
.planner.v04-empty .sticky-summary,
.planner.v04-empty .sticky-summary-tab,
.planner.v04-empty .feedback-section{display:none !important;}
.planner.v04-empty .hero{border-bottom:none; margin-bottom:6px; padding-bottom:6px;}
.planner.v04-empty .hero-title{font-size:clamp(24px,3vw,31px);}
.planner.v04 .v04-hint{font-size:12px; color:var(--muted); margin:14px 0 0;}

/* site masthead (top) */
.sitenav{display:flex; align-items:center; justify-content:flex-start; gap:30px; flex-wrap:wrap;
  background:#F6F2E8; border-bottom:1px solid var(--line);
  margin:-32px -24px 20px; padding:7px 24px;}
.sitenav-mark{display:flex; align-items:center; gap:9px; text-decoration:none; color:var(--ink);}
.sitenav-mono{width:22px; height:22px; border-radius:6px; background:var(--ink); color:#fff;
  font-family:'Fraunces',serif; font-weight:700; font-size:11px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;}
.sitenav-wordmark{font-family:'Fraunces',serif; font-weight:700; font-size:13.5px; letter-spacing:-.01em;}
.sitenav-links{display:flex; align-items:stretch; gap:4px; flex-wrap:wrap;}
.sitenav-item{display:flex; flex-direction:column; gap:1px; padding:5px 13px; border-radius:8px;
  text-decoration:none; border:1px solid transparent; white-space:nowrap;
  transition:background .15s, border-color .15s;}
.sitenav-item:hover{background:#FCFAF4; border-color:var(--line);}
.sitenav-t{font-size:12.5px; font-weight:600; color:var(--muted); line-height:1.25;}
.sitenav-d{font-size:9.5px; color:#A39C8E; line-height:1.25;}
.sitenav-on{background:#fff; border-color:var(--line);}
.sitenav-on .sitenav-t{color:var(--ink); font-weight:700;}
.sitenav-on .sitenav-d{color:var(--muted);}
.sitenav-item:focus-visible,.sitenav-mark:focus-visible{outline:2px solid var(--amber-focus,#C98B4B); outline-offset:2px;}

/* site footer (bottom) — mirrors the masthead */
.sitefoot{display:flex; align-items:center; justify-content:flex-start; gap:26px; flex-wrap:wrap;
  background:#F6F2E8; border-top:1px solid var(--line);
  margin:34px -24px -60px; padding:13px 24px 20px;}
.sitefoot-meta{margin-left:auto;}
.sitefoot-mark{display:flex; align-items:center; gap:9px; color:var(--ink);}
.sitefoot-links{display:flex; gap:16px; flex-wrap:wrap;}
.sitefoot-links a{font-size:12px; color:var(--muted); text-decoration:none;}
.sitefoot-links a:hover{color:var(--ink); text-decoration:underline;}
.sitefoot-links a:focus-visible{outline:2px solid #C98B4B; outline-offset:2px;}
.sitefoot-meta{font-size:11px; color:#9C968A;}

/* subsection eyebrow (residency inside tax strategy) */
.sub-eyebrow{font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.06em;
  color:#8A5A26; margin-bottom:7px;}

@media (max-width:640px){
  .sitenav{flex-direction:column; align-items:flex-start; gap:9px; margin-bottom:20px;}
  .sitenav-links{gap:2px;}
  .sitenav-item{padding:5px 9px;}
  .sitefoot{flex-direction:column; align-items:flex-start; gap:11px;}
}
.sticky-summary{position:fixed; top:78px; right:20px; z-index:50; background:#fff; border:1.5px solid; border-radius:12px; padding:27px 13px 12px; box-shadow:0 4px 20px rgba(38,36,30,.10); width:150px; transition:box-shadow .3s;}
.sticky-summary-close{position:absolute; top:6px; right:7px; width:18px; height:18px; border-radius:50%; border:none; background:#F3F0E7; color:var(--muted); font-size:10px; line-height:1; cursor:pointer; display:flex; align-items:center; justify-content:center; padding:0;}
.sticky-summary-close:hover{background:#E7E2D6; color:var(--ink);}
.sticky-summary-tab{position:fixed; top:78px; right:0; z-index:50; background:#fff; border:1.5px solid var(--line); border-right:none; border-radius:10px 0 0 10px; padding:8px 12px; box-shadow:-2px 2px 10px rgba(38,36,30,.08); cursor:pointer; display:flex; flex-direction:column; align-items:flex-end; gap:0; font-family:inherit;}
.sticky-summary-tab-val{font-family:'Fraunces',serif; font-weight:700; font-size:15px; line-height:1.1;}
.sticky-summary-tab-lbl{font-size:9.5px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em;}
.sticky-summary.pulsing{box-shadow:0 4px 20px rgba(38,36,30,.10), 0 0 0 4px rgba(181,72,63,.18);}
.sticky-summary.pulsing .sticky-summary-val{animation:pulseVal 1.1s ease-out;}
@keyframes pulseVal{0%{color:#B5483F; transform:scale(1.08);} 100%{transform:scale(1);}}
.sticky-summary-row{display:flex; justify-content:space-between; align-items:baseline; gap:14px; margin-bottom:3px;}
.sticky-summary-label{font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.03em;}
.sticky-summary-val{font-family:'Fraunces',serif; font-weight:700; font-size:15px;}
.sticky-summary-val.neg{color:#B5483F;}
.sticky-summary-net{margin-top:5px; padding-top:6px; border-top:1px solid var(--line);}
.sticky-summary-net .sticky-summary-val{font-size:19px;}
.sticky-summary-sub{font-size:10px; color:var(--muted); margin-top:6px; text-align:right;}
.sticky-summary-actions{display:flex; gap:6px; margin-top:10px; padding-top:10px; border-top:1px solid var(--line); flex-wrap:wrap;}
.summary-btn-primary{background:#26241E; color:#fff; border-color:#26241E; flex-basis:100%;}
.summary-btn-primary:hover{background:#3A362C;}
.sticky-summary-hint{font-size:9.5px; color:var(--muted); line-height:1.4; margin-top:8px;}
.landing{min-height:100vh; background:var(--cream); display:flex; align-items:center; justify-content:center; padding:40px 24px; position:relative; overflow:hidden;}

.landing-game{background:linear-gradient(180deg,#1B1035,#3A1E5C 55%,#2E7D4F);}
.game-sky{position:absolute; inset:0; z-index:0; pointer-events:none;}
.game-stars{position:absolute; inset:0; background-image:radial-gradient(1.5px 1.5px at 20px 30px, rgba(255,255,255,.5) 50%, transparent), radial-gradient(1.5px 1.5px at 120px 80px, rgba(255,255,255,.4) 50%, transparent), radial-gradient(1px 1px at 200px 150px, rgba(255,255,255,.5) 50%, transparent), radial-gradient(1.5px 1.5px at 300px 40px, rgba(255,255,255,.35) 50%, transparent), radial-gradient(1px 1px at 60px 200px, rgba(255,255,255,.4) 50%, transparent), radial-gradient(1.5px 1.5px at 380px 250px, rgba(255,255,255,.45) 50%, transparent); background-size:420px 320px; background-repeat:repeat;}
.game-wrap{position:relative; z-index:1; max-width:920px;}
.game-hud{display:flex; align-items:center; justify-content:center; gap:12px; margin-bottom:22px; flex-wrap:wrap;}
.game-pixel{font-family:'Press Start 2P',monospace; font-size:11px; color:#FFC542; text-shadow:2px 2px 0 rgba(0,0,0,.4);}
.game-hud-chip{font-family:'Press Start 2P',monospace; font-size:9px; color:#4DD9E8; background:#241640; border:2px solid #4A2E7A; border-radius:8px; padding:6px 10px;}
.game-title{font-family:'Press Start 2P',monospace; font-size:20px; color:#fff; text-align:center; line-height:1.7; margin:0 0 30px; text-shadow:3px 3px 0 rgba(0,0,0,.35); letter-spacing:-.02em;}

.doc-scene{display:flex; align-items:center; justify-content:center; gap:24px; margin-bottom:30px; flex-wrap:wrap;}
.doc-avatar{width:120px; height:135px; flex-shrink:0; filter:drop-shadow(0 8px 14px rgba(0,0,0,.35));}
.speech-bubble{background:#fff; border:3px solid #26241E; border-radius:16px; padding:16px 20px; max-width:320px; position:relative; box-shadow:0 6px 0 rgba(0,0,0,.2);}
.speech-bubble::before{content:''; position:absolute; left:-14px; top:50%; transform:translateY(-50%); border:10px solid transparent; border-right-color:#26241E;}
.speech-bubble::after{content:''; position:absolute; left:-10px; top:50%; transform:translateY(-50%); border:9px solid transparent; border-right-color:#fff;}
.speech-bubble p{margin:0 0 6px; font-family:'Fraunces',serif; font-size:15px; font-weight:600; color:#26241E; line-height:1.5;}
.speech-sub{font-size:11px; color:#8A8577;}

.game-doors{gap:20px;}
.game-door{background:#2B1B4D; border:3px solid #5A3B8C; border-radius:16px; box-shadow:0 6px 0 #1a0f33; color:#fff; position:relative; transition:transform .12s, box-shadow .12s;}
.game-door:hover{transform:translateY(-4px); box-shadow:0 10px 0 #1a0f33; border-color:#FFC542;}
.game-door-level{font-family:'Press Start 2P',monospace; font-size:8px; color:#FFC542; margin-bottom:10px;}
.game-door .landing-door-tag{color:#B685FF;}
.game-door h3{color:#fff;}
.game-door p{color:#C9BEE0;}
.game-door-cta{font-family:'Press Start 2P',monospace; font-size:10px; color:#8BE04D;}
.tile-current .landing-door-icon{color:#4DD9E8;}
.tile-guided .landing-door-icon{color:#FFC542;}
.tile-wizard .landing-door-icon{color:#FF5C93;}
.game-foot{color:#9686C4;}

@media (max-width:760px){
  .game-title{font-size:15px;}
  .doc-scene{flex-direction:column; text-align:center;}
  .speech-bubble::before, .speech-bubble::after{display:none;}
}

.planner.guided-mode{display:flex; flex-direction:column;}
.planner.guided-mode #sec-income{order:10;}
.planner.guided-mode #sec-expenses{order:20;}
.planner.guided-mode #sec-profit{order:30;}
.planner.guided-mode #sec-taxstrategy{order:40;}
.planner.guided-mode #sec-residency{order:50;}
.planner.guided-mode #sec-funnel{order:60;}
.planner.guided-mode .foot{order:100;}
.planner.guided-mode .sitefoot{order:110;}
.planner.guided-mode .sitenav{order:-1;}
.planner.guided-mode .feedback-section{order:70;}
.section-divider{display:flex; align-items:center; gap:16px; margin:36px 0 20px; color:var(--muted); font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.06em;}
.section-divider::before, .section-divider::after{content:""; flex:1; height:1.5px; background:linear-gradient(90deg, transparent, var(--line) 20%, var(--line) 80%, transparent);}
.section-divider span{white-space:nowrap; color:#8A5A26; background:#FAEEDA; padding:6px 16px; border-radius:20px;}
.guided-jumpnav{position:sticky; top:0; z-index:15; order:5; background:rgba(251,249,243,.95); backdrop-filter:blur(6px); display:flex; gap:8px; padding:12px 0; margin-bottom:8px; flex-wrap:wrap; border-bottom:1px solid var(--line);}
.jumpnav-group{display:flex; align-items:center; gap:7px; flex-wrap:wrap;}
.jumpnav-group-lbl{font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin-right:2px;}
.jumpnav-group-lbl-growth{color:#27500A;}
.jumpnav-divider{width:1.5px; align-self:stretch; background:var(--line); margin:2px 4px;}
.jumpnav-pill-growth{background:#EAF3DE; border-color:#C4DDA8;}
.jumpnav-pill-growth .jumpnav-lbl{color:#27500A;}
.jumpnav-pill-growth.jumpnav-active{background:#27500A; border-color:#27500A;}
.jumpnav-pill{display:flex; flex-direction:column; gap:1px; padding:6px 13px; border-radius:12px; background:#fff; border:1.5px solid var(--line); text-decoration:none; transition:border-color .15s, background .15s;}
.jumpnav-pill:hover{border-color:#C9A876;}
.jumpnav-lbl{font-size:10.5px; font-weight:600; color:var(--muted);}
.jumpnav-val{font-family:'Fraunces',serif; font-size:13px; font-weight:700; color:var(--ink);}
.jumpnav-active{border-color:#26241E; background:#26241E;}
.jumpnav-active .jumpnav-lbl{color:#C9BEE0;}
.jumpnav-active .jumpnav-val{color:#fff;}
.guided-section-num{display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border-radius:50%; background:#26241E; color:#fff; font-size:12px; font-weight:700; margin-right:10px; flex-shrink:0;}
.wizard-stepper{display:flex; align-items:center; justify-content:center; gap:4px; margin:0 0 24px; padding:4px 0;}
.wizard-dot{width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; background:#fff; border:1.5px solid var(--line); color:var(--muted); flex-shrink:0;}
.wizard-dot.done{background:#3F9577; border-color:#3F9577; color:#fff;}
.wizard-dot.now{background:#B5483F; border-color:#B5483F; color:#fff;}
.wizard-line{width:20px; height:1.5px; background:var(--line); flex-shrink:0;}
.wizard-nav{display:flex; align-items:center; justify-content:space-between; gap:12px; max-width:640px; margin:0 auto 32px; padding:18px 4px;}
.wizard-btn{font:inherit; font-size:14px; font-weight:600; padding:11px 22px; border-radius:10px; border:1.5px solid var(--line); background:#fff; color:var(--muted); cursor:pointer;}
.wizard-btn:disabled{opacity:.4; cursor:default;}
.wizard-btn.primary{background:#26241E; color:#fff; border-color:#26241E;}
.wizard-nav-label{font-size:12px; color:var(--muted); font-weight:600;}
.mode-switch{font-size:11px; color:var(--muted); text-decoration:underline; cursor:pointer; background:none; border:none; padding:0; font-family:inherit;}
.landing-wrap{max-width:900px; margin:0 auto; text-align:center;}
.landing-eyebrow{font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--accent, #B5483F); margin-bottom:14px;}
.landing-h1{font-family:'Fraunces',serif; font-size:44px; font-weight:700; letter-spacing:-.01em; color:var(--ink); margin-bottom:16px;}
.landing-sub{font-size:16px; color:var(--muted); max-width:560px; margin:0 auto 40px; line-height:1.6;}
.landing-doors{display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-bottom:28px;}
.landing-door{background:#fff; border:1.5px solid var(--line); border-radius:16px; padding:28px 22px; text-align:left; cursor:pointer; transition:.15s; box-shadow:0 1px 3px rgba(38,36,30,.04);}
.landing-door:hover{border-color:#B5483F; box-shadow:0 8px 24px rgba(38,36,30,.10); transform:translateY(-2px);}
.landing-door-icon{font-size:26px; color:#B5483F; margin-bottom:14px;}
.landing-door-tag{font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin-bottom:6px;}
.landing-door h3{font-family:'Fraunces',serif; font-size:19px; margin:0 0 8px;}
.landing-door p{font-size:13px; color:var(--muted); line-height:1.6; margin:0 0 16px;}
.landing-door-cta{font-size:13px; font-weight:700; color:#B5483F;}
.landing-foot{font-size:12px; color:var(--muted);}
@media (max-width:760px){
  .landing-doors{grid-template-columns:1fr;}
  .landing-h1{font-size:32px;}
}
.share-banner{display:flex; align-items:center; gap:6px; flex-wrap:wrap; background:#EAF2ED; border:1.5px solid #A9CBB6; border-radius:12px; padding:12px 16px; margin:0 0 20px; font-size:13px; line-height:1.5; color:#2B4A38;}
.share-banner b{color:#1F3A2C;}
.share-banner-close{margin-left:auto; background:none; border:none; font-size:20px; line-height:1; color:#5A7A68; cursor:pointer; padding:0 4px;}
.summary-btn{flex:1; font:inherit; font-size:11px; font-weight:600; color:var(--ink); background:#F3F0E7; border:1px solid var(--line); border-radius:8px; padding:6px 4px; cursor:pointer; transition:background .15s;}
.save-menu{position:absolute; top:calc(100% + 4px); left:0; right:0; background:#fff; border:1px solid var(--line); border-radius:10px; box-shadow:0 6px 18px rgba(38,36,30,.15); z-index:60; overflow:hidden;}
.save-menu button{display:block; width:100%; text-align:left; font:inherit; font-size:12px; font-weight:600; color:var(--ink); background:#fff; border:none; padding:10px 14px; cursor:pointer;}
.save-menu button:hover{background:#F7F3E9;}
.save-menu button + button{border-top:1px solid var(--line);}
.summary-btn:hover{background:#EAE4D6;}
@media print{
  .sticky-summary,.tabs,.control-val-input,input[type=range],.toggle,.pill,.residency-toggle,.summary-btn,.sticky-summary-actions,.exp-del,.funnel-input-field input,.job2-body input{-webkit-print-color-adjust:exact; print-color-adjust:exact;}
  .sticky-summary{display:none;}
  .sitenav-links,.sitefoot-links{display:none;}
  .sitenav{margin:0 0 14px; padding:0 0 10px; background:none; border-bottom:1px solid var(--line);}
  .sitefoot{margin:18px 0 0; padding:10px 0 0; background:none;}
  .tabs button:not(.tab-on){display:none;}
  .tabs{grid-template-columns:1fr; box-shadow:none;}
  .tab{border-bottom-width:1.5px;}
  body{background:#fff;}
  .planner{max-width:100%;}
  * {-webkit-print-color-adjust:exact !important; print-color-adjust:exact !important;}
}
@media (max-width:900px){
  .sticky-summary{position:static; margin:0 0 20px; width:100%; box-sizing:border-box;}
}
.cite-list{margin:10px 0 16px; padding-left:20px; font-size:14px; line-height:1.7; color:var(--ink);}
.cite-list li{margin-bottom:4px;}
sup{font-size:10px; color:var(--muted); margin-left:1px;}
.funnel-input-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:14px;}
.funnel-stage-grid{grid-template-columns:repeat(5,1fr); gap:10px;}
@media (max-width:900px){ .funnel-stage-grid{grid-template-columns:repeat(2,1fr);} }
@media (max-width:560px){ .funnel-stage-grid{grid-template-columns:1fr;} .funnel-input-hint{min-height:0;} }
.funnel-input-field label{font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.03em; display:block; margin-bottom:2px;}
.funnel-input-hint{display:block; font-size:10.5px; line-height:1.35; color:#A39C8E; margin-bottom:6px; min-height:28px;}
.funnel-input-field input{width:100%; border:1.5px solid #E4D9BE; border-radius:9px; padding:9px 11px; font-family:'Fraunces',serif; font-size:16px; font-weight:600; color:var(--ink); background:#FBF6E9; transition:border-color .15s;}
.funnel-input-field input:hover{border-color:#C9A876;}
.funnel-input-field input:focus{outline:none; border-color:#B5483F;}
.funnel-input-suffix{font-size:11px; color:var(--muted); margin-top:3px; display:block;}
.funnel-channel{border:1px solid var(--line); border-radius:14px; padding:18px 20px; margin-top:16px; background:#FBF9F4;}
.funnel-channel-head{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px; flex-wrap:wrap; gap:6px;}
.funnel-channel-head h3{font-family:'Fraunces',serif; font-size:18px; margin:0;}
.funnel-channel-value{font-size:12px; color:var(--muted); font-weight:600;}
.funnel-viz{display:flex; align-items:center; gap:24px; margin-top:16px; flex-wrap:wrap;}
.funnel-viz-shape{flex-shrink:0; width:200px;}
.funnel-stage-list{flex:1; min-width:220px; display:flex; flex-direction:column; gap:9px;}
.funnel-stage-row{display:flex; align-items:baseline; gap:9px;}
.funnel-stage-dot{width:9px; height:9px; border-radius:50%; flex-shrink:0;}
.funnel-stage-name{flex:1; font-size:13px; color:var(--muted); min-width:0;}
.funnel-stage-num{font-family:'Fraunces',serif; font-weight:700; font-size:16px; color:var(--ink); min-width:36px; text-align:right;}
.funnel-stage-conv{width:40px; text-align:right; font-size:11px; color:var(--muted); flex-shrink:0;}
.funnel-stage-value{width:76px; text-align:right; font-family:'Fraunces',serif; flex-shrink:0; transition:font-size .2s, color .2s;}
.ltv-formula{display:flex; align-items:center; gap:14px; margin:16px 0 20px; padding:16px 18px; background:#FBF6E9; border:1.5px solid #E4D9BE; border-radius:12px; flex-wrap:wrap;}
.ltv-formula-term{display:flex; flex-direction:column; gap:3px;}
.ltv-formula-label{font-size:10.5px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted);}
.ltv-formula-val{font-family:'Fraunces',serif; font-size:19px; font-weight:700; color:var(--ink);}
.ltv-formula-op{font-size:18px; color:var(--muted); font-weight:300;}
.ltv-formula-result .ltv-formula-val{font-size:24px;}
@media (max-width:520px){
  .ltv-formula{justify-content:center;}
}
.funnel-stage-note{margin-top:14px; font-size:12px; color:var(--muted); padding-top:12px; border-top:1px solid var(--line);}
.funnel-stage-note b{color:var(--ink);}
@media (max-width:520px){
  .funnel-viz{flex-direction:column; align-items:stretch;}
  .funnel-viz-shape{width:100%; max-width:160px; margin:0 auto;}
}
.funnel-leak{display:flex; gap:12px; align-items:flex-start; background:#FCEEEA; border:1px solid #E8B9AE; border-radius:12px; padding:14px 16px; margin-top:20px; font-size:13px; color:#7A3A2D; line-height:1.5;}
.funnel-leak-icon{font-size:22px; flex-shrink:0;}
.funnel-total-value{display:flex; justify-content:space-between; align-items:center; margin-top:16px; padding-top:16px; border-top:1px solid var(--line); font-size:13px; color:var(--muted);}
.funnel-total-value strong{font-family:'Fraunces',serif; font-size:22px;}
.funnel-score-row{display:grid; grid-template-columns:220px 1fr; gap:24px; align-items:center;}
.health-gauge{display:flex; flex-direction:column; align-items:center; text-align:center;}
.health-ring{width:120px; height:120px; border-radius:50%; display:flex; align-items:center; justify-content:center; padding:8px; box-sizing:border-box;}
.health-ring-inner{width:100%; height:100%; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; font-family:'Fraunces',serif; font-size:34px; font-weight:700;}
.health-label{margin-top:10px; font-weight:600; font-size:14px;}
.health-sub{font-size:12px; color:var(--muted); margin-top:2px;}
.funnel-progress-block{padding:4px 0;}
.funnel-progress-head{display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;}
.funnel-progress-note{font-size:12px; color:var(--muted); margin-top:2px;}
.funnel-mini-stats{display:flex; gap:22px; margin-top:14px; font-size:13px; flex-wrap:wrap;}
.funnel-target-grid{display:grid; grid-template-columns:1fr 1fr; gap:14px; margin:16px 0;}
.stat-col{display:flex; flex-direction:column; gap:14px;}
.stat-col .stat{flex:1;}
.stat{background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px 20px;}
.stat-big{background:linear-gradient(160deg,#fff,#FCFAF4); display:flex; flex-direction:column; justify-content:center;}
.stat-label{font-size:12px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:var(--muted); margin-bottom:10px;}
.stat-value{font-family:'Fraunces',serif; font-weight:600; font-size:26px; letter-spacing:-.02em; line-height:1;}
.stat-big .stat-value{font-size:42px;}
.stat-sub{font-size:12px; color:var(--muted); margin-top:7px; font-weight:500;}
.stat-note{font-size:12px; color:var(--muted); margin-top:8px;}
.stat-value.sm{font-size:18px;}
.a-subhead{font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin:16px 0 8px;}

/* gross/net strip */
.strip{display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; margin-bottom:28px;}
.strip-cell{background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 20px; display:flex; flex-direction:column;}
.strip-k{font-size:11px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:var(--muted);}
.strip-v{font-family:'Fraunces',serif; font-weight:600; font-size:24px; letter-spacing:-.02em; margin-top:8px; line-height:1;}
.strip-sub{font-size:12.5px; color:var(--muted); margin-top:6px; font-weight:500;}

/* segmented toggle */
.card-head-row{display:flex; justify-content:space-between; align-items:flex-start; gap:20px;}
.seg{display:inline-flex; background:#F1ECE1; border-radius:10px; padding:3px; flex-shrink:0;}
.seg-btn{font:inherit; font-size:13px; font-weight:600; color:var(--muted); border:none; background:transparent; padding:6px 14px; border-radius:8px; cursor:pointer; transition:all .14s;}
.seg-on{background:#fff; color:var(--ink); box-shadow:0 1px 2px rgba(40,36,30,.08);}
.leg-hint{font-size:11px; color:var(--muted); font-style:italic; margin-right:6px; align-self:center;}
.tip-foot{font-size:10px; color:var(--muted); margin-top:6px; text-align:right; font-style:italic;}

/* cards */
.card{background:var(--card); border:1px solid var(--line); border-radius:16px; padding:24px; margin-bottom:24px; box-shadow:0 1px 2px rgba(40,36,30,.03);}
.collapsible{cursor:pointer;}
.collapsible summary{list-style:none; cursor:pointer; position:relative; padding-right:32px;}
.collapsible summary::-webkit-details-marker{display:none;}
.collapsible summary::after{content:"\u2304"; position:absolute; top:2px; right:0; font-size:20px; color:var(--muted); transition:transform .2s;}
.collapsible[open] summary::after{transform:rotate(180deg);}
.collapsible summary p{margin-bottom:0;}
.collapsible[open] summary{margin-bottom:18px; border-bottom:1px solid var(--line); padding-bottom:18px;}
.decision-impact{border-left:4px solid var(--amber, #C98B4B) !important; background:linear-gradient(90deg, rgba(201,139,75,.06), transparent 40%);}
.decision-impact::before{content:"Affects every tab"; display:inline-block; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:#8A5A26; background:#FAEEDA; padding:3px 9px; border-radius:20px; margin-bottom:10px;}
.badge{display:inline-block; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; padding:3px 9px; border-radius:20px;}
.badge.green{background:#EAF3DE; color:#27500A;}
.current-pick-tag{display:inline-block; font-size:9.5px; font-weight:600; text-transform:none; letter-spacing:0; color:var(--muted); background:#F1ECE1; border-radius:20px; padding:2px 8px; margin-left:8px; vertical-align:middle;}
.card-head{margin-bottom:18px;}
.card-head h2{font-family:'Fraunces',serif; font-weight:600; font-size:22px; letter-spacing:-.01em; margin:0 0 6px;}
.card-head p{font-size:14px; line-height:1.5; color:var(--muted); margin:0; max-width:680px;}

/* goal */
.goal-body{display:grid; grid-template-columns:1.4fr 1fr; gap:22px; align-items:stretch;}
.goal-input label{font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); display:block; margin-bottom:8px;}
.goal-field{display:flex; align-items:center; gap:4px; border:1.5px solid var(--line); border-radius:10px; padding:10px 14px; margin-bottom:14px; font-family:'Fraunces',serif; font-size:24px; font-weight:600;}
.goal-field span{color:var(--muted);}
.goal-field input{border:none; outline:none; font:inherit; width:100%; background:transparent; color:var(--ink);}
.goal-result{border:2px solid; border-radius:14px; padding:20px; display:flex; flex-direction:column; justify-content:center; text-align:center; background:#FCFAF4;}
.goal-result-num{font-family:'Fraunces',serif; font-weight:600; font-size:54px; line-height:1;}
.goal-result-lbl{font-size:13px; font-weight:600; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); margin-top:4px;}
.goal-result-note{font-size:13px; color:var(--muted); line-height:1.45; margin-top:12px;}

/* legend */
.legend{display:flex; flex-wrap:wrap; gap:6px; margin-top:14px; justify-content:center;}
.leg{font:inherit; font-size:12px; font-weight:600; color:var(--muted); background:#FAF7F0; border:1px solid var(--line); border-radius:20px; padding:5px 12px; cursor:pointer; display:flex; align-items:center; gap:7px; transition:all .14s;}
.leg-on{color:var(--ink); background:#fff; border-color:#C7C0AF;}
.leg-dot{width:9px; height:9px; border-radius:50%;}

/* two-up */
.two-up{display:grid; grid-template-columns:1fr 1fr; gap:24px;}
.two-up .card{margin-bottom:24px;}

/* table */
.table-wrap{overflow-x:auto;}
table{width:100%; border-collapse:collapse; font-size:14px;}
th{text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); font-weight:600; padding:0 14px 12px; border-bottom:1px solid var(--line);}
.num-head{text-align:right;}
td{padding:13px 14px; border-bottom:1px solid #F1ECE1;}
tr{cursor:pointer; transition:background .12s;}
tbody tr:hover{background:#FCFAF4;}
.row-on{background:#FAF6EC !important;}
.row-on td{font-weight:600;}
.tdot{display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:9px; vertical-align:middle;}
td.num-head{text-align:right;}
.strong{font-family:'Fraunces',serif; font-size:15px;}
.pos{color:var(--pos); font-weight:600;}
.neg{color:var(--neg); font-weight:600;}
.muted{color:var(--muted);}
.bar-cell{width:90px; height:8px; background:#F1ECE1; border-radius:4px; overflow:hidden;}
.bar-fill{height:100%; border-radius:4px;}

/* tooltip */
.tip{background:#fff; border:1px solid var(--line); border-radius:10px; padding:10px 12px; box-shadow:0 4px 14px rgba(40,36,30,.1); font-size:12px;}
.tip-head{font-weight:600; margin-bottom:7px; color:var(--ink);}
.tip-row{display:flex; align-items:center; gap:8px; padding:2px 0;}
.tip-on{font-weight:700;}
.tip-dot{width:8px; height:8px; border-radius:50%;}
.tip-name{color:var(--muted); min-width:54px;}
.tip-val{margin-left:auto; font-weight:600; color:var(--ink);}


/* tabs */
.tabs{display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin-bottom:28px;}
.tab{font:inherit; text-align:left; background:var(--card); border:1.5px solid var(--line); border-bottom-width:3px; border-radius:12px; padding:14px 18px; cursor:pointer; transition:all .15s; display:flex; flex-direction:column; gap:3px;}
.tab:hover{border-color:#C7C0AF;}
.tab-lbl{font-family:'Fraunces',serif; font-weight:600; font-size:17px; color:var(--muted);}
.tab-sub{font-size:11.5px; color:var(--muted); opacity:.8;}
.tab-on{background:#fff; box-shadow:0 2px 6px rgba(40,36,30,.06);}
.tab-on .tab-lbl{color:var(--ink);}

/* city picker */
.city-picker{display:grid; grid-template-columns:1.3fr 1fr; gap:20px; align-items:end;}
.city-select label, .city-manual label{font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); display:block; margin-bottom:8px;}
.city-select select{width:100%; font:inherit; font-size:15px; font-weight:600; color:var(--ink); border:1.5px solid var(--line); border-radius:10px; padding:11px 13px; background:#fff; cursor:pointer;}
.city-source{font-size:11.5px; color:var(--muted); display:block; margin-top:7px; font-style:italic;}
.city-result{border:2px solid; border-radius:12px; padding:14px 18px; background:#FCFAF4; display:flex; flex-direction:column; align-items:center; text-align:center;}
.city-result-k{font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; color:var(--muted);}
.city-result-v{font-family:'Fraunces',serif; font-size:26px; font-weight:600; margin-top:4px;}
.city-result-v em{font-family:'Inter',sans-serif; font-size:12px; font-style:normal; font-weight:500; color:var(--muted); margin-left:3px;}
.city-result-sub{font-size:11.5px; color:var(--muted); margin-top:5px;}
.city-manual{display:flex; flex-direction:column;}

/* expenses */
.exp-list{display:flex; flex-direction:column;}
.exp-row{display:grid; grid-template-columns:1.5fr 1fr 130px 90px 28px; gap:14px; align-items:center; padding:11px 0; border-bottom:1px solid #F1ECE1;}
.exp-row-city{background:#FAF7F0; margin:0 -24px; padding:11px 24px; border-bottom:none; border-top:2px solid var(--line);}
.exp-name{display:flex; flex-direction:column; gap:2px; min-width:0;}
.exp-lbl{font-size:14px; font-weight:600; color:var(--ink);}
.exp-rename{font:inherit; font-size:14px; font-weight:600; color:var(--ink); border:1px solid var(--line); border-radius:7px; padding:5px 8px; background:#FCFAF4; outline:none; width:100%;}
.exp-note{font-size:11.5px; color:var(--muted);}
.exp-bar{height:7px; background:#F1ECE1; border-radius:4px; overflow:hidden;}
.exp-bar-fill{height:100%; border-radius:4px; opacity:.75; transition:width .2s;}
.exp-input{display:flex; align-items:center; gap:3px; border:1.5px solid #E4D9BE; border-radius:9px; padding:7px 11px; background:#FBF6E9; transition:border-color .15s;}
.exp-input:hover{border-color:#C9A876;}
.exp-input:focus-within{border-color:#B5483F;}
.exp-input-locked{background:#F3F0E7; border-style:dashed;}
.exp-locked-val{font-family:'Fraunces',serif; font-size:16px; font-weight:600; color:var(--ink);}
.exp-input span{color:var(--muted); font-size:13px;}
.exp-input input{border:none; outline:none; font:inherit; font-family:'Fraunces',serif; font-size:16px; font-weight:600; width:100%; background:transparent; color:var(--ink);}
.exp-input-locked{background:#F1ECE1; border-style:dashed;}
.exp-locked-val{font-family:'Fraunces',serif; font-size:16px; font-weight:600; color:var(--ink);}
.exp-per{font-size:11px !important;}
.exp-yr{font-family:'Fraunces',serif; font-size:15px; font-weight:600; color:var(--muted); text-align:right;}
.exp-yr span{font-family:'Inter',sans-serif; font-size:10.5px; font-weight:500; margin-left:2px;}
.exp-del{font:inherit; font-size:20px; line-height:1; color:#C7C0AF; background:transparent; border:none; cursor:pointer; padding:2px 6px; border-radius:6px;}
.exp-del:hover{color:#B5483F; background:#FBF0EE;}
.exp-del-spacer{display:block; width:28px;}
.exp-foot{display:flex; justify-content:space-between; align-items:center; margin-top:18px; flex-wrap:wrap; gap:14px;}
.exp-add{font:inherit; font-size:13px; font-weight:600; color:var(--muted); background:#FAF7F0; border:1.5px dashed var(--line); border-radius:10px; padding:9px 16px; cursor:pointer;}
.exp-add:hover{border-color:#C7C0AF; color:var(--ink);}
.exp-total{display:flex; align-items:baseline; gap:18px;}
.exp-total span{font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; color:var(--muted);}
.exp-total strong{font-family:'Fraunces',serif; font-size:22px; font-weight:600;}
.exp-total em{font-family:'Inter',sans-serif; font-size:11px; font-style:normal; font-weight:500; color:var(--muted); margin-left:2px;}

/* tax shield */
.shield-bar{display:flex; height:52px; border-radius:12px; overflow:hidden; border:1px solid var(--line);}
.shield-cost,.shield-back{display:flex; align-items:center; justify-content:center; font-size:12.5px; font-weight:600; color:#fff; min-width:0; overflow:hidden; white-space:nowrap;}
.shield-cost{background:#B5483F;}
.shield-back{background:#3F9577;}
.shield-note{font-size:13px; color:var(--muted); margin:14px 0 0; line-height:1.5;}

/* waterfall */
.wf{display:flex; flex-direction:column; gap:9px;}
.wf-row{display:grid; grid-template-columns:180px 1fr 120px; gap:14px; align-items:center;}
.wf-k{font-size:13.5px; color:var(--muted); font-weight:500;}
.wf-track{height:22px; background:#F7F3EA; border-radius:6px; overflow:hidden;}
.wf-bar{height:100%; border-radius:6px; transition:width .2s;}
.wf-out{background:#D9A9A2;}
.wf-v{font-family:'Fraunces',serif; font-size:15px; font-weight:600; text-align:right;}
.wf-final{border-top:2px solid var(--line); padding-top:13px; margin-top:6px;}
.wf-final .wf-k{color:var(--ink); font-weight:700; font-size:15px;}
.wf-final .wf-v{font-size:19px;}

/* footer */
.foot{font-size:12px; line-height:1.6; color:var(--muted); border-top:1px solid var(--line); padding-top:20px; margin-top:8px;}
.foot strong{color:var(--ink);}

/* biweekly pay calendar */
.paycheck-badge{border:2px solid; border-radius:14px; padding:12px 20px; display:flex; flex-direction:column; align-items:center; background:#FCFAF4; flex-shrink:0;}
.paycheck-k{font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; color:var(--muted);}
.paycheck-v{font-family:'Fraunces',serif; font-weight:600; font-size:30px; line-height:1; margin:5px 0;}
.paycheck-sub{font-size:11px; color:var(--muted);}
.pay-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:12px;}
.pay-cell{position:relative; background:#FCFAF4; border:1px solid var(--line); border-radius:12px; padding:14px 16px; display:flex; flex-direction:column; gap:4px;}
.pay-anchor{border-width:2px; background:#fff;}
.pay-flag{position:absolute; top:-9px; left:14px; font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; color:#fff; padding:2px 8px; border-radius:20px;}
.pay-date{font-size:12.5px; font-weight:600; color:var(--ink);}
.pay-amt{font-family:'Fraunces',serif; font-weight:600; font-size:22px; letter-spacing:-.01em; line-height:1;}
.pay-cum{font-size:11px; color:var(--muted);}
.pay-note{font-size:12.5px; color:var(--muted); line-height:1.5; margin:16px 0 0;}
.cite-refs{font-size:12.5px; color:var(--muted); line-height:1.6; margin:16px 0 0; display:flex; flex-direction:column; gap:5px;}
.cite-num{color:var(--ink); font-weight:600; margin-right:4px;}
.cite-ref a{color:#8A5A26; text-decoration:underline; text-underline-offset:2px;}
.cite-ref a:hover{color:#B5483F;}
.term-clarify{font-size:12.5px; color:var(--muted); line-height:1.7; background:#F7F3E9; border-radius:10px; padding:12px 16px; margin:0 0 20px;}
.term-clarify b{color:var(--ink);}

@media(max-width:780px){
  .controls,.stats,.two-up,.goal-body,.strip,.job2-body,.residency-grid,.funnel-input-grid,.funnel-score-row,.funnel-target-grid{grid-template-columns:1fr;}
  .tabs{grid-template-columns:1fr 1fr;}
  .tab{padding:12px 14px;}
  .city-picker{grid-template-columns:1fr;}
  .exp-row{grid-template-columns:1fr 110px 28px; gap:10px;}
  .exp-bar{display:none;}
  .exp-yr{display:none;}
  .wf-row{grid-template-columns:130px 1fr 100px; gap:9px;}
  .wf-k{font-size:12px;}
  .stat-col{flex-direction:column;}
  .card-head-row{flex-direction:column;}
  .pay-grid{grid-template-columns:repeat(2,1fr);}
  .stats .stat-big{order:-1;}
  /* larger tap targets on touch screens */
  .pill{padding:12px 16px; min-height:44px;}
  .toggle{padding:9px 16px 9px 8px; min-height:40px;}
  .toggle-knob{width:20px; height:20px;}
  .tab{padding:16px 18px; min-height:44px;}
  .exp-del{min-width:36px; min-height:36px; font-size:24px;}
  .city-select select{min-height:46px;}
  .slider{height:28px; margin:-11px 0;}
  .leg{padding:8px 13px; min-height:36px;}
}
`;