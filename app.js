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
// Feedback endpoint. GitHub Pages is static and cannot process a form, so the
// form POSTs somewhere else. Two options, both free — paste either URL here:
//
//   Google Apps Script  https://script.google.com/macros/s/.../exec
//     Sheet + email. See _dev/feedback-endpoint.gs. Sent no-cors, so the
//     browser cannot read the reply and success is reported optimistically.
//
//   Formspree           https://formspree.io/f/xxxxxxxx
//     Email + a dashboard, no Google OAuth. Answers CORS properly, so we get
//     a real success or failure back and can tell the user the truth.
//
// While this is empty the form opens a mail draft, exactly as it always has.
const FEEDBACK_ENDPOINT = "https://formspree.io/f/xzdnyabp";
const FEEDBACK_IS_FORMSPREE = /formspree\.io/.test(FEEDBACK_ENDPOINT);
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
const FED_STD = 16100,
  CA_STD = 5540;
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
const CTC_PER_CHILD = 2200;
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
// ---------------------------------------------------------------------------
// Column identity. Every place in the Tax Strategy section that compares the
// two structures uses these two colours and nothing else, so a reader can tell
// which column they are looking at without reading the header again. Neither
// colour may be green or red - those stay reserved for better/worse verdicts.
// ---------------------------------------------------------------------------
const ENT_A = {
  key: "sole_prop",
  name: "Sole Proprietorship",
  short: "Sole Prop",
  ch: "S",
  slug: "a",
  ink: "#3B5A7A",
  tint: "#EFF4F9",
  tintOn: "#E1ECF6",
  line: "#BFD3E5"
};
const ENT_B = {
  key: "s_corp",
  name: "Professional Corp",
  short: "Prof Corp",
  ch: "C",
  slug: "b",
  ink: "#6A4A78",
  tint: "#F5EFF8",
  tintOn: "#EDE1F3",
  line: "#D4C3DD"
};
const ENT_OF = { sole_prop: ENT_A, s_corp: ENT_B };
// A small colour-coded name tag. Used inline in prose, on cards, in headings -
// anywhere a structure is named outside the table itself.
function entTag(e, opts) {
  opts = opts || {};
  return /*#__PURE__*/React.createElement("span", {
    className: "enttag" + (opts.solid ? " enttag-solid" : "") + (opts.sm ? " enttag-sm" : ""),
    style: opts.solid
      ? { background: e.ink, borderColor: e.ink }
      : { color: e.ink, background: e.tint, borderColor: e.line }
  }, /*#__PURE__*/React.createElement("i", {
    style: opts.solid ? null : { background: e.ink }
  }, e.ch), opts.full ? e.name : e.short);
}

// BLS Occupational Employment and Wage Statistics, Marriage and Family
// Therapists (SOC 21-1013), May 2023. Annual mean wage for EMPLOYED MFTs -
// which is exactly the comparison the reasonable-compensation test calls for,
// and a far better anchor than any percentage of profit.
const MFT_WAGES = [
  {p: "San Francisco–Oakland", v: 92370},
  {p: "San Jose–Sunnyvale", v: 86710},
  {p: "Sacramento", v: 81080},
  {p: "California, all metros", v: 69780, state: true},
  {p: "Los Angeles–Long Beach", v: 63420},
  {p: "San Diego–Carlsbad", v: 62980},
  {p: "Riverside–San Bernardino", v: 59120},
  {p: "Oxnard–Ventura", v: 57820}
];
const MFT_NAT_P90 = 104710, MFT_NAT_MEDIAN = 58510, MFT_CA_MEAN = 69780;

// US Census, County Business Patterns 2023, California, NAICS 621330,
// S-corporation establishments in the 1-4 employee class: 4,201 establishments,
// 4,963 employees, $294,021,000 total annual payroll. That is $69,988 of payroll
// per establishment and $59,243 per employee - a federal administrative figure
// for what California solo-ish therapy S-corps actually run through payroll,
// and a much stronger anchor than any percentage-of-profit convention.
const CENSUS_SCORP_PAYROLL = 69988, CENSUS_SCORP_PER_EMP = 59243,
      CENSUS_SCORP_ESTABS = 4201;

const SS_FRA_AGE = 67; // full retirement age, everyone born 1960 or later
// SSA's published maximum benefit at full retirement age, 2026. A simplified
// PIA built from flat capped earnings can exceed this, because SSA indexes
// past earnings by the Average Wage Index and historical caps were lower in
// real terms. Bounding to the published maximum keeps the estimate honest.
const SS_MAX_PIA_AT_FRA = 4152;

const RETIRE_2026 = {
  ira: {
    under50: 7500,
    over50: 8600
  },
  solo401k: {
    employeeUnder50: 24500,
    employee50to59: 32500,
    employee60to63: 35750,
    employee64plus: 32500,
    overallCapUnder50: 72000,
    overallCap50plus: 80000,
    overallCap60to63: 83250,
    employerPct: 0.20
  },
  // IRS Notice 2025-67. 415(c) annual additions $72,000; 401(a)(17) comp cap $360,000.
  sep: {
    dcCap: 72000,
    compCap: 360000,
    corpPct: 0.25,
    solePct: 0.20
  },
  // Notice 2025-67: general SIMPLE deferral $17,000; $18,100 for employers with
  // 25 or fewer employees (SECURE 2.0 s.117) - which a solo practice always is.
  simple: {
    deferral: 17000,
    deferralSmallEmployer: 18100,
    catchUp50: 4000,
    catchUp60to63: 5250,
    matchPct: 0.03
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
const FED_BRACKETS = [[0, 0.10], [12400, 0.12], [50400, 0.22], [105700, 0.24], [201775, 0.32], [256225, 0.35], [640600, 0.37]];
// CA Prop 63 mental health services tax: 1% on taxable income over $1,000,000.
// RTC s.17043 - the threshold is NOT indexed and is $1m for joint filers too.
const CA_MHS_THRESH = 1000000, CA_MHS_RATE = 0.01;
const CA_BRACKETS = [[0, 0.01], [11079, 0.02], [26264, 0.04], [41452, 0.06], [57542, 0.08], [72724, 0.093], [371479, 0.103], [445771, 0.113], [742953, 0.123]];
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
  if (!(grossYr > 0)) {
    return /*#__PURE__*/React.createElement("div", {className: "keepwrap keepwrap-empty"},
      /*#__PURE__*/React.createElement("div", {className: "keep-eyebrow"}, "What you actually keep"),
      /*#__PURE__*/React.createElement("p", null,
        "Enter your ", /*#__PURE__*/React.createElement("b", null, "hourly rate"), " and ",
        /*#__PURE__*/React.createElement("b", null, "sessions per week"),
        " in the Income section and this fills in — what you bill, what tax takes, and what lands in your account, down to the cents you keep per session."),
      /*#__PURE__*/React.createElement("a", {href: "#sec-income", className: "keep-cta"}, "Go to Income →"));
  }
  const pct = n => Math.max(0, (n / grossYr) * 100);
  const keepPct = Math.round((netYr / grossYr) * 100);
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
      /*#__PURE__*/React.createElement("b", {className: "pos"}, fmt(netYr)), " yours"));
}

// Fold a heavy block on phones only. Desktop keeps it open; a narrow viewport
// gets a one-line summary and one tap. The open state is set ONCE on mount via a
// ref - never as a controlled `open` prop, which React re-applies on every render
// so the panel snaps shut while the user is typing.
function mobileFold(key, title, sub, content) {
  return /*#__PURE__*/React.createElement("details", {
    key: key, className: "card collapsible mfold",
    ref: el => {
      if (el && !el.dataset.autoinit) {
        el.dataset.autoinit = "1";
        el.open = !(typeof window !== "undefined" && window.innerWidth < 760);
      }
    }
  }, /*#__PURE__*/React.createElement("summary", {className: "mfold-s"},
      /*#__PURE__*/React.createElement("b", null, title),
      sub ? /*#__PURE__*/React.createElement("span", null, sub) : null),
    content);
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
  const sdi = totalW2 * 0.013;   // EDD 2026 rate; no wage cap since SB 951
  const addlMedThresh = ADDL_MED_THRESH_BY_STATUS[filingStatus] || ADDL_MED_THRESH;
  const addlMed = Math.max(0, totalW2 + seBase - addlMedThresh) * ADDL_MED_RATE;
  const agi = Math.max(0, schedC + kDistribution + totalW2 - halfSE - employeeRetirement);
  const taxableBeforeQBI = Math.max(0, agi - fedStd);
  const qbiIncome = entityType === "s_corp" ? Math.max(0, kDistribution) : Math.max(0, schedC - halfSE);
  let pct;
  if (taxableBeforeQBI <= qbiStart) pct = 1;else if (taxableBeforeQBI >= qbiEnd) pct = 0;else pct = 1 - (taxableBeforeQBI - qbiStart) / (qbiEnd - qbiStart);
  const qbiDed = Math.min(QBI_RATE * qbiIncome, QBI_RATE * taxableBeforeQBI) * pct;
  const fedTaxBeforeCredits = bracketTax(Math.max(0, taxableBeforeQBI - qbiDed), fedBrackets);
  const ctc = filingStatus === "mfj_dependents" ? Math.min(numDependents * CTC_PER_CHILD, fedTaxBeforeCredits) : 0;
  const fedTax = Math.max(0, fedTaxBeforeCredits - ctc);
  const caTaxableIncome = Math.max(0, agi - caStd);
  // Prop 63 mental health services tax, RTC s.17043 - 1% over $1m, threshold
  // not indexed and not doubled for joint filers. This is what makes the
  // often-quoted "13.3% top rate" true rather than 12.3%.
  const caTax = bracketTax(caTaxableIncome, caBrackets)
    + Math.max(0, caTaxableIncome - CA_MHS_THRESH) * CA_MHS_RATE;
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
  const addlMed = Math.max(0, w2Wages + seBase - ADDL_MED_THRESH) * ADDL_MED_RATE;   // single-filer model
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
// Weeks worked is a real input, not a constant. The tool used to hardcode 52
// everywhere, which quietly assumed a therapist takes no holiday at all and
// overstated every downstream figure - tax, profit, the S-corp comparison and
// the retirement projections all inherit it. Default stays 52 so any caller
// that has not been updated behaves exactly as before.
const WEEKS_FULL = 52;
const grossWk = (rate, s) => rate * s;
const grossYr = (rate, s, w) => rate * s * (w > 0 ? w : WEEKS_FULL);
const grossMo = (rate, s, w) => Math.round(rate * s * (w > 0 ? w : WEEKS_FULL) / 12);
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
      blurb: "The two levers that change what you keep: where you put money before it is taxed, and how your practice is structured \u2014 in that order, because that is the order they are worth. Everything here is an estimate, not personalised advice.",
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
  // Progress for the Tax Strategy nav pill. Mirrors the stepper inside the
  // section: about-you, salary, running costs, and the long-horizon inputs.
  const taxStepsDone = (taxAge > 0 && retireAge > 0 && investReturn > 0 ? 1 : 0)
    + (sCorpSalaryInput > 0 ? 1 : 0)
    + ((payrollSvcCost || 0) + (corpReturnCost || 0) + (statementOfInfoCost || 0) > 0 ? 1 : 0)
    + (filingStatus ? 1 : 0);
  const [secondaryRate, setSecondaryRate] = useState(SAVED.secondaryRate != null ? SAVED.secondaryRate : "");
  const [secondarySessions, setSecondarySessions] = useState(SAVED.secondarySessions != null ? SAVED.secondarySessions : "");
  const [careerStart, setCareerStart] = useState(SAVED.careerStart != null ? SAVED.careerStart : 0);
  const [wageMetro, setWageMetro] = useState(SAVED.wageMetro != null ? SAVED.wageMetro : 3);
  const [vacationOn, setVacationOn] = useState(SAVED.vacationOn != null ? SAVED.vacationOn : false);
  const [vacationWeeks, setVacationWeeks] = useState(SAVED.vacationWeeks != null ? SAVED.vacationWeeks : 0);
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
        careerStart: careerStart,
        wageMetro: wageMetro,
        vacationOn: vacationOn,
        vacationWeeks: vacationWeeks,
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
  }, [tab, rate, sessions, goal, chartMode, secondaryOn, secondaryRate, secondarySessions, retreatOn, retreatParticipants, retreatRate, retreatPerMonth, vacationOn, vacationWeeks, wageMetro, careerStart, usLocation, avgTenure, currentClients, sessionsPerClientWk, monthlyChurn, monthsToTarget, funnel, filingStatus, numDependents, entityType, sCorpSalaryInput, existingPretaxIRA, taxAge, retireAge, investReturn, expenses, cityKey, manualCityFee, viewMode, wizardStep]);
  const d = {
    color: colorForRate(rate)
  };
  const nearestRate = RATES.reduce((best, r) => Math.abs(r - rate) < Math.abs(best - rate) ? r : best, RATES[0]);
  const job2Yr = 0;
  const weeksWorked = vacationOn ? Math.max(1, WEEKS_FULL - (parseFloat(vacationWeeks) || 0)) : WEEKS_FULL;
  const secondaryYr = secondaryOn ? (parseFloat(secondaryRate) || 0) * (parseFloat(secondarySessions) || 0) * weeksWorked : 0;
  const retreatYr = retreatOn ? (parseFloat(retreatParticipants) || 0) * (parseFloat(retreatRate) || 0) * (parseFloat(retreatPerMonth) || 0) * 12 : 0;
  const otherIncomeYr = secondaryYr + retreatYr;
  const grossMoForExp = (grossYr(rate, sessions, weeksWorked) + otherIncomeYr) / 12;
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
  const bizFeeAt = (r, s) => cityLicenseFee(cityKey, grossYr(r, s, weeksWorked) + otherIncomeYr, manualCityFee);
  const bizFee = bizFeeAt(rate, sessions);
  const expYr = expYrBase + bizFee;

  // Year computation at any rate/sessions, using current expenses + secondary source + second job
  const yearAt = (r, s) => computeYear(grossYr(r, s, weeksWorked) + otherIncomeYr, expYrBase + bizFeeAt(r, s), job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
  const netYr = (r, s) => Math.round(yearAt(r, s).net);

  // Current scenario, fully broken out
  const cur = useMemo(() => {
    const y = computeYear(grossYr(rate, sessions, weeksWorked) + otherIncomeYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    const noExp = computeYear(grossYr(rate, sessions, weeksWorked) + otherIncomeYr, 0, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    const withoutSecondary = computeYear(grossYr(rate, sessions, weeksWorked) + retreatYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    const withoutRetreat = computeYear(grossYr(rate, sessions, weeksWorked) + secondaryYr, expYr, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
    return {
      ...y,
      netYr: Math.round(y.net),
      netMo: Math.round(y.net / 12),
      netWk: Math.round(y.net / 52),
      grossYr: y.grossAll,
      grossMo: Math.round(y.grossAll / 12),
      grossWk: Math.round(y.grossAll / 52),
      grossTherYr: grossYr(rate, sessions, weeksWorked),
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
    // ---- SEP IRA -----------------------------------------------------
    // Employer-funded only: no employee deferral, no catch-up at any age.
    // A corporation contributes 25% of W-2 wages; a sole proprietor's 25% of
    // post-contribution profit works out to 20% of net SE earnings, which is
    // why the same plan gives the two structures different room.
    const sepCompBase = Math.min(netSEEarnings, RETIRE_2026.sep.compCap);
    const sepPct = entityTypeArg === "s_corp" ? RETIRE_2026.sep.corpPct : RETIRE_2026.sep.solePct;
    const sepContrib = Math.max(0, Math.min(sepPct * sepCompBase, RETIRE_2026.sep.dcCap));
    const sepIra = {
      compBase: sepCompBase,
      pct: sepPct,
      pctLabel: entityTypeArg === "s_corp" ? "25% of W-2 wages" : "20% of net self-employment earnings",
      total: sepContrib,
      taxSavings: sepContrib * marginalRate,
      futureValue: fvAnnuity(sepContrib),
      vsSolo: sepContrib - solo401kTotal
    };

    // ---- SIMPLE IRA --------------------------------------------------
    // A solo practice always has 25 or fewer employees, so the higher
    // SECURE 2.0 s.117 deferral applies. Employer must match 3% of pay.
    // Cannot be run in the same year as a Solo 401(k) - it is one or the other.
    const simpleDeferralCap = RETIRE_2026.simple.deferralSmallEmployer
      + (taxAge >= 60 && taxAge <= 63 ? RETIRE_2026.simple.catchUp60to63
         : taxAge >= 50 ? RETIRE_2026.simple.catchUp50 : 0);
    const simpleCompBase = netSEEarnings;
    const simpleDeferral = Math.max(0, Math.min(simpleDeferralCap, simpleCompBase));
    const simpleMatch = Math.max(0, RETIRE_2026.simple.matchPct * simpleCompBase);
    const simpleTotal = simpleDeferral + simpleMatch;
    const simpleIra = {
      deferralCap: simpleDeferralCap,
      deferral: simpleDeferral,
      match: simpleMatch,
      compBase: simpleCompBase,
      total: simpleTotal,
      taxSavings: simpleTotal * marginalRate,
      futureValue: fvAnnuity(simpleTotal),
      vsSolo: simpleTotal - solo401kTotal
    };

    // Social Security impact: only wages (not distributions) earn SS credit.
    // Simplified steady-state projection: assumes this earnings pattern for
    // up to 35 years (SSA always divides by 420 months, even with fewer
    // years worked) — does not reflect your actual past earnings history.
    const soleCreditedEarnings = Math.min(soleNetSEEarnings, SS_WAGE_BASE);
    const scorpCreditedEarnings = Math.min(sCorpSalaryInput, SS_WAGE_BASE);
    // Years of covered work across the whole career, past and future - not
    // years remaining. Falls back to years-remaining only if the user has not
    // said when they started, and the UI labels that case as an underestimate.
    const careerYears = careerStart > 0 && retireAge > careerStart
      ? retireAge - careerStart
      : yearsToRetire;
    const yearsForAIME = Math.min(35, Math.max(1, careerYears));
    const soleAIME = soleCreditedEarnings * yearsForAIME / 420;
    const scorpAIME = scorpCreditedEarnings * yearsForAIME / 420;
    const solePIA = Math.min(computePIA(soleAIME), SS_MAX_PIA_AT_FRA);
    const scorpPIA = Math.min(computePIA(scorpAIME), SS_MAX_PIA_AT_FRA);
    // The other half of the trade-off: the payroll tax you did not pay is real
    // money you could have invested. Model it honestly - contribute the annual
    // saving every year until retirement at the user's own assumed return, then
    // draw it down at 4% a year, and compare that draw with the benefit given up.
    const ssPayroll = payrollSplit(Math.max(0, soleForSSCompare.schedC), sCorpSalaryInput);
    const annualPayrollSaved = Math.max(0, ssPayroll.saved);
    const investedFV = fvAnnuity(annualPayrollSaved);
    const investedDrawAnnual = investedFV * 0.04;
    const annualGapV = (solePIA - scorpPIA) * 12;
    const ssRetireYears = Math.max(0, 90 - SS_FRA_AGE);
    const socialSecurity = {
      soleCreditedEarnings,
      scorpCreditedEarnings,
      yearsForAIME,
      careerKnown: careerStart > 0 && retireAge > careerStart,
      soleMonthlyPIA: solePIA,
      scorpMonthlyPIA: scorpPIA,
      soleAnnualPIA: solePIA * 12,
      scorpAnnualPIA: scorpPIA * 12,
      monthlyGap: solePIA - scorpPIA,
      annualGap: annualGapV,
      fraAge: SS_FRA_AGE,
      lifetimeYears: ssRetireYears,
      soleLifetime: solePIA * 12 * ssRetireYears,
      scorpLifetime: scorpPIA * 12 * ssRetireYears,
      lifetimeGap: annualGapV * ssRetireYears,
      annualPayrollSaved,
      investedFV,
      investedDrawAnnual,
      investWins: investedDrawAnnual > annualGapV,
      investMargin: investedDrawAnnual - annualGapV
    };
    return {
      netSEEarnings,
      magi,
      marginalRate: marginalRate,
      yearsToRetire,
      solo401k,
      sepIra,
      simpleIra,
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
      row[`gross_${r}`] = grossYr(r, s, weeksWorked) + job2Yr + otherIncomeYr;
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
    const g = grossYr(rate, s, weeksWorked) + job2Yr;
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
      vacationOn, vacationWeeks, wageMetro, careerStart,
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
    target: /^https?:/.test(href) ? "_blank" : null,
    rel: /^https?:/.test(href) ? "noopener noreferrer" : null,
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
  }, "Your finances"), [["sec-income", "Income", fmt(cur.grossYr), 0, "1", rate > 0 && sessions > 0],
    ["sec-expenses", "Expenses", "\u2212" + fmt(cur.expYr), 0, "2", cur.expYr > 0],
    ["sec-profit", "Profit", fmt(cur.netYr), 0, "=", null],
    ["sec-taxstrategy", "Tax Strategy", taxStepsDone < 4 ? taxStepsDone + " of 4" : Math.round(cur.takeHomePct * 100) + "%", taxStepsDone < 4 ? taxStepsDone / 4 : 0, "3", taxStepsDone >= 4]
   ].map(([id, lbl, val, prog, n, done]) => /*#__PURE__*/React.createElement("a", {
    key: id,
    href: "#" + id,
    className: "jumpnav-pill" + (activeSection === id ? " jumpnav-active" : "")
      + (done === null ? " jumpnav-derived" : done ? " jumpnav-done" : "")
  }, /*#__PURE__*/React.createElement("i", {
    className: "jumpnav-n"
  }, done === true ? "\u2713" : n), /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-txt"
  }, /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-lbl"
  }, lbl), /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-val"
  }, val), prog ? /*#__PURE__*/React.createElement("span", {
    className: "jumpnav-prog"
  }, /*#__PURE__*/React.createElement("i", {style: {width: (prog * 100) + "%"}})) : null))))), viewMode === "wizard" && /*#__PURE__*/React.createElement("div", {
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
  }, /*#__PURE__*/React.createElement("span", null, "15"), /*#__PURE__*/React.createElement("span", null, "30"))),
    /*#__PURE__*/React.createElement("div", {className: "timeoff" + (vacationOn ? " on" : "")},
      /*#__PURE__*/React.createElement("button", {
        type: "button",
        className: "toggle" + (vacationOn ? " toggle-on" : ""),
        onClick: () => setVacationOn(!vacationOn)
      }, /*#__PURE__*/React.createElement("span", {className: "toggle-knob"}), "Time off"),
      vacationOn
        ? /*#__PURE__*/React.createElement("span", {className: "timeoff-body"},
            /*#__PURE__*/React.createElement("input", {
              type: "number", min: 0, max: 20, step: 1,
              value: vacationWeeks === 0 ? "" : vacationWeeks,
              placeholder: "0",
              onChange: e => setVacationWeeks(Math.max(0, Math.min(20, +e.target.value || 0)))
            }),
            "weeks a year not working")
        : /*#__PURE__*/React.createElement("span", {className: "timeoff-off"},
            "Off \u2014 the year below assumes you work all 52 weeks"),
      /*#__PURE__*/React.createElement("span", {className: "timeoff-out"},
        /*#__PURE__*/React.createElement("b", null, weeksWorked), " working weeks \u00B7 ",
        /*#__PURE__*/React.createElement("b", null, (sessions * weeksWorked).toLocaleString()), " sessions")),
    /*#__PURE__*/React.createElement("div", {className: "inc-eq"},
      /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("b", null, fmt(rate)), " a session"),
      /*#__PURE__*/React.createElement("i", null, "\u00D7"),
      /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("b", null, sessions), " a week"),
      /*#__PURE__*/React.createElement("i", null, "\u00D7"),
      /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("b", null, weeksWorked), " weeks"),
      /*#__PURE__*/React.createElement("i", null, "="),
      /*#__PURE__*/React.createElement("span", {className: "inc-eq-res"}, fmt(grossYr(rate, sessions, weeksWorked))))), showIncomeAddons && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {className: "income-mods"}, /*#__PURE__*/React.createElement("section", {
    className: "job2" + (secondaryOn ? " job2-open" : ""),
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
    className: "job2" + (retreatOn ? " job2-open" : ""),
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
  }, "*marginal — taxed together with your primary rate at the combined self-employment rate, so this is what retreats/events actually add to take-home"))))), /*#__PURE__*/React.createElement("p", {
    className: "term-clarify"
  }, /*#__PURE__*/React.createElement("b", null, "Gross"), " = what you bill, before anything is taken out. ", /*#__PURE__*/React.createElement("b", null, "Expenses"), " = what it costs to run the practice. ", /*#__PURE__*/React.createElement("b", null, "Profit"), " (sometimes called net practice income) = gross minus expenses, before tax. ", /*#__PURE__*/React.createElement("b", null, "Net"), " = what actually lands in your bank account, after tax too."), /*#__PURE__*/React.createElement("section", {
    className: "strip strip-lede"
  }, /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Gross / week"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.grossWk)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "$", rate, " \u00d7 ", sessions, " sessions")), /*#__PURE__*/React.createElement("div", {
    className: "strip-cell"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, "Gross / month"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.grossMo)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, sessions * 4.33 >= 1 ? Math.round(sessions * 4.33) + " sessions" : "")),
    /*#__PURE__*/React.createElement("div", {
    className: "strip-cell strip-year"
  }, /*#__PURE__*/React.createElement("span", {
    className: "strip-k"
  }, secondaryOn || retreatOn ? "Combined gross / year" : "Gross / year"), /*#__PURE__*/React.createElement("span", {
    className: "strip-v"
  }, fmt(cur.grossYr)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, secondaryOn || retreatOn
      ? [`therapy ${fmt(cur.grossTherYr)}`, secondaryOn ? `secondary ${fmt(cur.secondaryYr)}` : null,
         retreatOn ? `retreats ${fmt(cur.retreatYr)}` : null].filter(Boolean).join(" + ")
      : `${weeksWorked} working weeks`))), (function () {
    const rateRow = r => {
      const gy = grossYr(r, sessions, weeksWorked) + job2Yr + otherIncomeYr;
      const ny = netYr(r, sessions);
      return {r: r, gy: gy, ny: ny, tax: gy - ny, keepPct: Math.round(ny / Math.max(1, gy) * 100),
        delta: ny - cur.netYr, isCur: r === nearestRate};
    };
    const all = RATES.map(rateRow);
    const curIdx = Math.max(0, all.findIndex(x => x.isCur));
    const focus = all.slice(curIdx, curIdx + 3);
    const next = focus[1] || null;
    const scale = Math.max(1, ...focus.map(x => x.ny));
    return /*#__PURE__*/React.createElement("section", {className: "card"},
      /*#__PURE__*/React.createElement("div", {className: "card-head"},
        /*#__PURE__*/React.createElement("h2", null, "What a rate rise is worth"),
        /*#__PURE__*/React.createElement("p", null,
          "Same caseload, same hours, ", sessions, " sessions a week",
          secondaryOn ? ", with your other income sources included" : "",
          ". This is pure pricing power \u2014 the only lever here that costs you nothing.")),
      /*#__PURE__*/React.createElement("div", {className: "uro-list"},
        focus.map(x => /*#__PURE__*/React.createElement("div", {
          key: x.r, className: "uro" + (x.isCur ? " on" : ""),
          role: "button", tabIndex: 0, onClick: () => setRate(x.r),
          onKeyDown: e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setRate(x.r); } }
        }, /*#__PURE__*/React.createElement("span", {className: "uro-l"},
            "$", x.r, "/hr",
            x.isCur ? /*#__PURE__*/React.createElement("em", null, "yours") : null),
          /*#__PURE__*/React.createElement("span", {className: "uro-b"},
            /*#__PURE__*/React.createElement("i", {style: {
              width: (x.ny / scale * 100) + "%", background: RATE_DATA[x.r].color}})),
          /*#__PURE__*/React.createElement("b", {className: "uro-v"}, fmt(x.ny),
            /*#__PURE__*/React.createElement("em", null, x.keepPct, "% kept")),
          /*#__PURE__*/React.createElement("b", {
            className: "uro-d " + (x.delta === 0 ? "muted" : x.delta > 0 ? "pos" : "neg")
          }, x.delta === 0 ? "\u2014" : (x.delta > 0 ? "+" : "\u2212") + fmt(Math.abs(x.delta)))))),
      next && next.delta > 0 ? /*#__PURE__*/React.createElement("div", {className: "sec-point"},
        /*#__PURE__*/React.createElement("b", null, "+", fmt(next.delta), " a year"),
        " for charging $", next.r - focus[0].r, " more a session \u2014 no extra hours, no new clients, nothing to file. You would keep ",
        next.keepPct, "\u00a2 of each extra dollar instead of ", focus[0].keepPct, "\u00a2, because the bracket above takes a little more.") : null,
      /*#__PURE__*/React.createElement("details", {className: "ratefold"},
        /*#__PURE__*/React.createElement("summary", null,
          /*#__PURE__*/React.createElement("b", null, "Every rate from $", RATES[0], " to $", RATES[RATES.length - 1]),
          /*#__PURE__*/React.createElement("span", null, "gross, net, tax and keep-rate \u00b7 tap a row to set it"),
          /*#__PURE__*/React.createElement("i", null, "Show")),
        /*#__PURE__*/React.createElement("div", {className: "table-wrap"},
          /*#__PURE__*/React.createElement("table", null,
            /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null,
              /*#__PURE__*/React.createElement("th", null, "Rate"),
              /*#__PURE__*/React.createElement("th", {className: "num-head"}, "Gross / year"),
              /*#__PURE__*/React.createElement("th", {className: "num-head"}, "Net / year"),
              /*#__PURE__*/React.createElement("th", {className: "num-head"}, "Tax"),
              /*#__PURE__*/React.createElement("th", {className: "num-head"}, "Keeps"),
              /*#__PURE__*/React.createElement("th", null, "vs. current net"),
              /*#__PURE__*/React.createElement("th", null))),
            /*#__PURE__*/React.createElement("tbody", null, all.map(x =>
              /*#__PURE__*/React.createElement("tr", {
                key: x.r, className: x.isCur ? "row-on" : "", onClick: () => setRate(x.r)
              }, /*#__PURE__*/React.createElement("td", null,
                  /*#__PURE__*/React.createElement("span", {className: "tdot",
                    style: {background: RATE_DATA[x.r].color}}), "$", x.r, "/hr"),
                /*#__PURE__*/React.createElement("td", {className: "num-head"}, fmt(x.gy)),
                /*#__PURE__*/React.createElement("td", {className: "num-head strong"}, fmt(x.ny)),
                /*#__PURE__*/React.createElement("td", {className: "num-head muted"}, "\u2212" + fmt(x.tax)),
                /*#__PURE__*/React.createElement("td", {className: "num-head muted"}, x.keepPct, "%"),
                /*#__PURE__*/React.createElement("td", {
                  className: x.delta === 0 ? "muted" : x.delta > 0 ? "pos" : "neg"
                }, x.delta === 0 ? "\u2014" : (x.delta > 0 ? "+" : "\u2212") + fmt(Math.abs(x.delta))),
                /*#__PURE__*/React.createElement("td", null,
                  /*#__PURE__*/React.createElement("div", {className: "bar-cell"},
                    /*#__PURE__*/React.createElement("div", {className: "bar-fill", style: {
                      width: x.ny / netYr(200, 30) * 100 + "%", background: RATE_DATA[x.r].color}}))))))))));
  })(), (function () {
    const payCell = (p, i) => /*#__PURE__*/React.createElement("div", {
      key: i, className: "pay-cell" + (p.isAnchor ? " pay-anchor" : ""),
      style: p.isAnchor ? {borderColor: d.color} : {}
    }, p.isAnchor ? /*#__PURE__*/React.createElement("span", {
      className: "pay-flag", style: {background: d.color}}, "anchor") : null,
      /*#__PURE__*/React.createElement("span", {className: "pay-date"}, fmtDate(p.date)),
      /*#__PURE__*/React.createElement("span", {className: "pay-amt"}, fmt(p.amount)),
      /*#__PURE__*/React.createElement("span", {className: "pay-cum"}, fmt(p.cumulative), " ytd"));
    return /*#__PURE__*/React.createElement("section", {className: "card"},
      /*#__PURE__*/React.createElement("div", {className: "card-head"},
        /*#__PURE__*/React.createElement("h2", null, "Biweekly take-home"),
        /*#__PURE__*/React.createElement("p", null,
          "Your annual net split across 26 checks, anchored to a payday of ",
          /*#__PURE__*/React.createElement("strong", null, "Fri, Jul 3 2026"),
          " and every other Friday after, at $", rate, "/hr \u00b7 ", sessions, " sessions/wk.")),
      /*#__PURE__*/React.createElement("div", {className: "paylede"},
        /*#__PURE__*/React.createElement("b", {style: {color: d.color}}, fmt(payPerCheck)),
        /*#__PURE__*/React.createElement("span", null, "every 2 weeks \u00b7 26 checks a year \u00b7 ",
          fmt(payPerCheck * 26), " in total")),
      /*#__PURE__*/React.createElement("div", {className: "pay-grid pay-next"},
        paydays.slice(0, 3).map(payCell)),
      paydays.length > 3 ? /*#__PURE__*/React.createElement("details", {className: "payfold"},
        /*#__PURE__*/React.createElement("summary", null,
          /*#__PURE__*/React.createElement("b", null, "The next ", paydays.length, " paydays"),
          /*#__PURE__*/React.createElement("span", null, "with a running year-to-date"),
          /*#__PURE__*/React.createElement("i", null, "Show")),
        /*#__PURE__*/React.createElement("div", {className: "pay-grid"}, paydays.map(payCell)),
        /*#__PURE__*/React.createElement("p", {className: "pay-note"},
          "A biweekly schedule lands 26 checks a year, so two months each year carry a third check \u2014 those are the bonus-feeling paydays.")) : null);
  })()))), isVisible("expenses") && /*#__PURE__*/React.createElement("div", {id:"sec-expenses"}, sectionIntro("expenses"), /*#__PURE__*/React.createElement(ExpensesTab, {
    weeksWorked: weeksWorked,
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
    grossTherYr: grossYr(rate, sessions, weeksWorked) + otherIncomeYr
  })), isVisible("profit") && /*#__PURE__*/React.createElement("div", {id:"sec-profit"}, sectionIntro("profit"), /*#__PURE__*/React.createElement(ProfitTab, {
    weeksWorked: weeksWorked,
    cur: cur,
    color: d.color,
    rate: rate,
    sessions: sessions,
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
    weeksWorkedProp: weeksWorked,
    careerStart: careerStart,
    setCareerStart: setCareerStart,
    wageMetro: wageMetro,
    setWageMetro: setWageMetro,
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
  }, "Still your tax strategy \u2014 one more lever"), /*#__PURE__*/React.createElement("h2", null, "If you practiced somewhere else"), /*#__PURE__*/React.createElement("p", null, "Same practice revenue and running costs (", fmt(cur.grossYr), "/yr gross, ", fmt(expYr), "/yr expenses), estimated as a self-employed therapist based in each location instead. Each card lists exactly what's counted."), /*#__PURE__*/React.createElement("p", {className: "resid-retnote"}, /*#__PURE__*/React.createElement("b", null, "Retirement accounts are not a California feature. "), "A Solo 401(k), SEP or SIMPLE is federal \u2014 the same limits apply in New York, Pennsylvania or anywhere else you would practise in the US, and the deduction comes off state taxable income too. Which means the same contribution is ", /*#__PURE__*/React.createElement("b", null, "worth more where the tax rate is higher"), ": sheltering a dollar in California or New York City saves more than sheltering it where there is no state income tax. Outside the US these accounts stop making sense and local pension rules take over \u2014 not modelled here."), /*#__PURE__*/React.createElement("div", {className: "medcost"}, /*#__PURE__*/React.createElement("b", null, "Not counted in any figure below: health cover once you retire abroad. "), "Social Security follows a US citizen almost anywhere \u2014 Germany, Portugal, France and Australia all have totalization agreements with the US, and the UAE does not, though payments still reach you there. ", /*#__PURE__*/React.createElement("b", null, "Medicare does not travel at all"), ". It covers essentially nothing outside the United States, so every non-US card below quietly omits a lifelong private or local insurance premium that a California retiree would not pay. Treat the overseas net figures as better than they will feel.")), /*#__PURE__*/React.createElement("div", {
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
  }, (function () {
    const c = taxStrategy.solo401k.total, sv = taxStrategy.solo401k.taxSavings;
    const bank = cur.netYr - c + sv, tot = Math.max(1, cur.totalTax + cur.netYr);
    if (!(c > 0)) return /*#__PURE__*/React.createElement("span", null,
      /*#__PURE__*/React.createElement("b", null, "Retirement accounts apply here too. "),
      "Fill in Tax Strategy and this shows what a Solo 401(k) would move out of tax and into your own account.");
    return /*#__PURE__*/React.createElement("div", {className: "locret"},
      /*#__PURE__*/React.createElement("div", {className: "locret-lab"}, "If you max your Solo 401(k)"),
      /*#__PURE__*/React.createElement("div", {className: "locret-bar"},
        /*#__PURE__*/React.createElement("i", {style: {width: (Math.max(0, cur.totalTax - sv) / tot * 100) + "%", background: "#B5483F"}}),
        /*#__PURE__*/React.createElement("i", {style: {width: (c / tot * 100) + "%", background: "#3F9577"}}),
        /*#__PURE__*/React.createElement("i", {style: {width: (Math.max(0, bank) / tot * 100) + "%", background: "#26241E"}})),
      /*#__PURE__*/React.createElement("div", {className: "locret-sp"},
        /*#__PURE__*/React.createElement("span", null, "Invested ", /*#__PURE__*/React.createElement("b", null, fmt(c))),
        /*#__PURE__*/React.createElement("span", null, "Bank ", /*#__PURE__*/React.createElement("b", null, fmt(bank)))),
      /*#__PURE__*/React.createElement("div", {className: "locret-why"},
        "Costs you ", /*#__PURE__*/React.createElement("b", null, fmt(c - sv)), " of spending money \u2014 the other ",
        /*#__PURE__*/React.createElement("b", null, fmt(sv)), " was tax leaving anyway."));
  })()), /*#__PURE__*/React.createElement("div", {
    className: "residency-includes"
  }, /*#__PURE__*/React.createElement("b", null, "Includes: "), "federal income tax, self-employment tax, and CA state income tax (progressive to 12.3%, plus the 1% Prop 63 mental health surcharge above $1m taxable \u2014 which is where the often-quoted 13.3% comes from), with the same QBI deduction and expense treatment used throughout this tool.")), [{
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
  }, "Done \u2014 see full dashboard \u2192")), (function () {
    // The year on one page, in the language of a pay statement. Everything
    // above is a decision; this is the receipt for the decisions you made.
    const wk = weeksWorked, sess = sessions * wk;
    const ent = entityType === "s_corp" ? "Professional Corp (S-corp election)" : "Sole Proprietorship";
    const entInk = entityType === "s_corp" ? "#6A4A78" : "#3B5A7A";
    const contrib = taxStrategy && taxStrategy.solo401k ? taxStrategy.solo401k.total : 0;
    const line = (k, v, o) => /*#__PURE__*/React.createElement("div", {
      className: "yr-line" + (o && o.sub ? " sub" : "") + (o && o.tot ? " tot" : "") + (o && o.neg ? " neg" : ""),
      key: k
    }, /*#__PURE__*/React.createElement("span", null, k), /*#__PURE__*/React.createElement("b", null, v));
    return /*#__PURE__*/React.createElement("section", {className: "card yrstmt", id: "sec-statement"},
      /*#__PURE__*/React.createElement("div", {className: "yr-head"},
        /*#__PURE__*/React.createElement("div", null,
          /*#__PURE__*/React.createElement("span", {className: "yr-kicker"}, "Your year, on one page"),
          /*#__PURE__*/React.createElement("h2", null, "The statement")),
        /*#__PURE__*/React.createElement("div", {className: "yr-ent", style: {borderColor: entInk, color: entInk}},
          "Planning as ", /*#__PURE__*/React.createElement("b", null, ent))),
      /*#__PURE__*/React.createElement("div", {className: "yr-cols"},
        /*#__PURE__*/React.createElement("div", {className: "yr-col"},
          /*#__PURE__*/React.createElement("h4", null, "What you billed"),
          line("Rate a session", fmt(rate)),
          line("Sessions a week", String(sessions)),
          line("Weeks worked", wk + (vacationOn ? " (" + (52 - wk) + " off)" : " (no time off set)")),
          line("Sessions a year", sess.toLocaleString()),
          secondaryOn ? line("Secondary income", fmt(cur.secondaryYr)) : null,
          retreatOn ? line("Retreats and events", fmt(cur.retreatYr)) : null,
          line("Gross a year", fmt(cur.grossYr), {tot: true})),
        /*#__PURE__*/React.createElement("div", {className: "yr-col"},
          /*#__PURE__*/React.createElement("h4", null, "What came out"),
          line("Running the practice", "\u2212" + fmt(cur.expYr), {neg: true}),
          line("Profit before tax", fmt(cur.grossYr - cur.expYr), {sub: true}),
          line("Federal, CA and payroll tax", "\u2212" + fmt(cur.totalTax), {neg: true}),
          line("Effective rate on profit", Math.round(cur.totalTax / Math.max(1, cur.grossYr - cur.expYr) * 100) + "%", {sub: true}),
          line("Net for the year", fmt(cur.netYr), {tot: true}))),
      /*#__PURE__*/React.createElement("div", {className: "yr-strip"},
        [["Per session", fmt(sess > 0 ? cur.netYr / sess : 0), "after everything"],
         ["Per week", fmt(cur.netWk), "over " + wk + " working weeks"],
         ["Per month", fmt(cur.netMo), "averaged"],
         ["You keep", Math.round(cur.takeHomePct * 100) + "\u00A2", "of every dollar billed"]
        ].map(([k, v, n]) => /*#__PURE__*/React.createElement("div", {className: "yr-cell", key: k},
          /*#__PURE__*/React.createElement("span", {className: "k"}, k),
          /*#__PURE__*/React.createElement("b", null, v),
          /*#__PURE__*/React.createElement("span", {className: "n"}, n)))),
      contrib > 0 ? /*#__PURE__*/React.createElement("div", {className: "yr-note"},
        /*#__PURE__*/React.createElement("b", null, "Not shown above: retirement. "),
        "Maxing a Solo 401(k) would move ", /*#__PURE__*/React.createElement("b", null, fmt(contrib)),
        " out of this statement and into an account that is still yours \u2014 lowering the net figure while raising your total for the year. See the Tax Strategy section for what that actually costs.") : null,
      /*#__PURE__*/React.createElement("p", {className: "yr-fine"},
        "Every figure here is the same calculation used throughout the tool, on the choices you have made: ",
        fmt(rate), " a session, ", sessions, " a week, ", wk, " weeks, ",
        vacationOn ? (52 - wk) + " weeks off, " : "no time off, ",
        ent.toLowerCase(), ", ", filingStatus === "mfj" ? "married filing jointly" : filingStatus === "mfj_dependents" ? "married with dependants" : filingStatus === "hoh" ? "head of household" : "filing single",
        ". Estimates, not a filing."));
  })(), /*#__PURE__*/React.createElement("section", {
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
    disabled: fbSent === "sending",
    onClick: () => {
      if (!fbMessage.trim()) return;
      const share = buildShareURL();
      const setupLine = "$" + rate + "/hr, " + sessions + " sessions/week";
      if (FEEDBACK_ENDPOINT) {
        setFbSent("sending");
        const payload = {
          name: fbName || "", type: fbType, message: fbMessage,
          setup: setupLine, share: share,
          page: (typeof location !== "undefined" ? location.href : ""),
          agent: (typeof navigator !== "undefined" ? navigator.userAgent : "")
        };
        const ok = () => {
          setFbSent("done"); setFbName(""); setFbMessage("");
          setTimeout(() => setFbSent(false), 6000);
        };
        const bad = () => { setFbSent("error"); setTimeout(() => setFbSent(false), 8000); };
        if (FEEDBACK_IS_FORMSPREE) {
          // Formspree answers CORS, so we can report a real result.
          fetch(FEEDBACK_ENDPOINT, {
            method: "POST",
            headers: {"Content-Type": "application/json", "Accept": "application/json"},
            body: JSON.stringify(payload)
          }).then(r => r.ok ? ok() : bad()).catch(bad);
        } else {
          // Apps Script does not answer a CORS preflight, so the request has
          // to stay a "simple" one: no-cors plus a text/plain content type.
          // The reply is opaque, so success here means "sent", not "stored".
          fetch(FEEDBACK_ENDPOINT, {
            method: "POST",
            mode: "no-cors",
            headers: {"Content-Type": "text/plain;charset=utf-8"},
            body: JSON.stringify(payload)
          }).then(ok).catch(bad);
        }
        return;
      }
      const subject = encodeURIComponent("[" + fbType + "] Therapy Practice Simulator feedback");
      const bodyLines = [fbName ? "From: " + fbName : null, "Type: " + fbType, "", fbMessage, "", "\u2014\u2014\u2014", "Current setup: " + setupLine, share].filter(Boolean);
      window.location.href = "mailto:shawn@shawnwalters.com?subject=" + subject + "&body=" + encodeURIComponent(bodyLines.join("\n"));
      setFbSent("mail");
      setTimeout(() => setFbSent(false), 3000);
    }
  }, fbSent === "sending" ? "Sending\u2026" : fbSent === "done" ? "\u2713 Sent \u2014 thank you"
     : fbSent === "error" ? "Didn\u0027t send \u2014 try again" : fbSent === "mail" ? "Opening your email app\u2026" : "Send feedback"), /*#__PURE__*/React.createElement("p", {
    className: "pay-note",
    style: {
      marginTop: 10
    }
  }, FEEDBACK_ENDPOINT
      ? "Sends straight through \u2014 no email app needed. A link back to your exact setup goes with it so I can see what you're seeing. Nothing else is collected."
      : "Opens your email app with everything filled in, including a link back to your exact setup so I can see what you're seeing. Nothing is sent automatically \u2014 you'll see the draft before it goes anywhere.")), /*#__PURE__*/React.createElement("footer", {
    className: "foot"
  }, /*#__PURE__*/React.createElement("strong", null, "Estimates only — not tax advice."), " 2026 CA single-filer model. Practice income is treated as ", /*#__PURE__*/React.createElement("strong", null, "1099 / self-employed"), ": business expenses are deducted on Schedule\xA0C, self-employment tax (15.3% on 92.35% of net earnings) applies, and the QBI deduction is included with the SSTB phase-out that affects therapists at higher incomes. California has no city or county ", /*#__PURE__*/React.createElement("em", null, "income"), " tax — state tax is identical everywhere in CA. The second job is treated as W-2 wages with employee FICA and CA SDI; its wages share the Social Security wage base with your self-employment income. Federal figures are the final 2026 amounts from IRS Rev. Proc. 2025-32, including the wider \u00A7199A phase-out and the $2,200 child tax credit enacted by the One Big Beautiful Bill Act (Pub. L. 119-21). California has not published 2026 rate schedules yet \u2014 the FTB\u0027s own 2026 Form 540-ES instructs filers to use the 2025 tables, so that is what this uses, together with the 2026 SDI rate of 1.3% and no wage cap. Real figures depend on your entity type (sole prop vs. S-corp), retirement contributions, home-office and mileage deductions, quarterly estimated payments, and actual filing status — talk to a CPA before making decisions on these numbers."), /*#__PURE__*/React.createElement("div", {
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
    href: href,
    target: /^https?:/.test(href) ? "_blank" : null,
    rel: /^https?:/.test(href) ? "noopener noreferrer" : null
  }, t))), /*#__PURE__*/React.createElement("div", {
    className: "sitefoot-meta"
  }, "Last updated: July 27, 2026")));
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
  weeksWorkedProp,
  careerStart,
  setCareerStart,
  wageMetro,
  setWageMetro,
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
  // Two gates, not one. The this-year comparison needs only income, expenses
  // and a salary - all already entered - so withholding it behind a retirement
  // date was never defensible. Only the long-horizon rows genuinely need these.
  // Declared here, at the top of the component: structureRows is evaluated
  // early and anything it references must exist before it. (TDZ, again.)
  const horizonReady = taxAge > 0 && retireAge > 0 && investReturn > 0;
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

  // A 0 in a number field looks like an answer. These render blank with a
  // placeholder until the user actually types something, which is what makes
  // the "2 of 4 answered" counter and the gate below honest.
  const stepField = (label, value, onChange, min, max, ph, hint) => /*#__PURE__*/React.createElement("div", {
    className: "sfield" + (value > 0 ? " ok" : ""),
    key: label
  }, /*#__PURE__*/React.createElement("label", null,
      /*#__PURE__*/React.createElement("i", {className: "sfield-tick" + (value > 0 ? " on" : "")},
        value > 0 ? "\u2713" : "\u25CB"), label),
    /*#__PURE__*/React.createElement("input", {
      type: "number", min: min, max: max, placeholder: ph,
      value: value > 0 ? value : "",
      onChange: e => onChange(+e.target.value || 0)
    }),
    hint ? /*#__PURE__*/React.createElement("span", {className: "sfield-hint"}, hint) : null);

  const step1Count = (taxAge > 0 ? 1 : 0) + (careerStart > 0 ? 1 : 0) + (retireAge > 0 ? 1 : 0)
    + (investReturn > 0 ? 1 : 0);
  const introSection = /*#__PURE__*/React.createElement("section", {
    id: "taxstep1",
    className: "card stepcard" + (step1Count >= 4 ? " stepcard-done" : "")
  }, /*#__PURE__*/React.createElement("div", {className: "stepcard-head"},
      /*#__PURE__*/React.createElement("div", {className: "stepcard-n"}, step1Count >= 4 ? "\u2713" : "1"),
      /*#__PURE__*/React.createElement("div", null,
        /*#__PURE__*/React.createElement("h2", null, "About you"),
        /*#__PURE__*/React.createElement("p", null,
          "Four answers. They set the contribution limits you qualify for, how long your money has to grow, and how many years of earnings Social Security will average \u2014 the long-range projections further down are impossible without them.")),
      /*#__PURE__*/React.createElement("div", {className: "stepcard-count"},
        /*#__PURE__*/React.createElement("b", null, step1Count + " / 4"),
        /*#__PURE__*/React.createElement("span", null, "answered"))),
    /*#__PURE__*/React.createElement("div", {className: "sfields"},
      stepField("Your age", taxAge, setTaxAge, 18, 80, "e.g. 40", "Sets which catch-up limits you qualify for"),
      stepField("Earning since age", careerStart, setCareerStart, 14, 70, "e.g. 26", "Social Security averages your highest 35 years \u2014 without this the estimate counts only the years you have left, and understates badly"),
      stepField("Retiring at", retireAge, setRetireAge, 40, 80, "e.g. 67", "67 is full retirement age if you were born after 1960"),
      stepField("Expected annual return %", investReturn, setInvestReturn, 0, 15, "pick below", "Or choose a starting point from the presets")));

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
  }, /*#__PURE__*/React.createElement("h2", null, "Your options, simulated")), strategyCard("Solo 401(k)", "You wear two hats: as \u201Cemployee\u201D you can defer income directly from pay, and as \u201Cemployer\u201D your practice can contribute up to 20% of net self-employment earnings on top \u2014 both reduce this year's taxable income, and both grow tax-deferred until withdrawal. Usually the largest contribution room available to a solo owner, and the one to max first.", solo401kBody, "Highest capacity"), strategyCard("Traditional IRA", "A separate, simpler account funded with pre-tax dollars (if your income is under the deduction phase-out) or after-tax dollars (if over it \u2014 still useful as a \u201Cbackdoor Roth\u201D building block). Grows tax-deferred; withdrawals in retirement are taxed as ordinary income. Because you're an active participant in a Solo 401(k), the deduction phases out at a lower income than someone with no workplace plan.", traditionalBody, strategy.traditionalIra.deductPct <= 0 ? "Fully phased out \u2014 nondeductible" : strategy.traditionalIra.deductPct < 1 ? "Partially phased out" : "Fully deductible"), strategyCard("Roth IRA", "Funded with after-tax dollars \u2014 no deduction today \u2014 but grows completely tax-free, and qualified withdrawals in retirement owe nothing at all. The direct contribution phases out at higher income levels than you might expect; above the top of that range, a \u201Cbackdoor Roth\u201D (nondeductible Traditional IRA contribution, immediately converted) is the common workaround.", rothBody, strategy.rothIra.eligiblePct < 1 ? "Phased out \u2014 consider backdoor" : "Fully eligible"), strategyCard("Backdoor Roth IRA", "If you're phased out of a direct Roth contribution, you can still get Roth-equivalent tax-free growth: contribute to a Traditional IRA without claiming a deduction (no income limit on nondeductible contributions), then convert it to Roth right away (no income limit on conversions either, since 2010). The catch is the IRC \u00A7408(d)(2) \u201Cpro-rata rule\u201D: if you hold "+"any"+" other pre-tax Traditional/SEP/SIMPLE IRA money, the conversion isn't treated as 100% basis \u2014 it's taxed in proportion to your "+"total"+" IRA balance, pre-tax and after-tax combined. Enter your existing pre-tax IRA balance below to see the real tax cost.", backdoorBody, strategy.backdoorRoth.taxableFraction > 0.05 ? "Pro-rata rule applies \u2014 partially taxable" : "Clean \u2014 minimal pro-rata drag"), strategyCard("SEP IRA", "Employer money only \u2014 there is no employee deferral and no catch-up at any age, which is what separates it from the Solo 401(k). A corporation contributes 25% of your W-2 wages; a sole proprietor's equivalent works out to 20% of net self-employment earnings, capped either way at the $72,000 annual-additions limit. Simpler to open and to run than a Solo 401(k), with no annual Form 5500 until the balance is large \u2014 but because it has no deferral, it usually gives a solo owner less room. Its real cost is downstream: a SEP balance is pre-tax IRA money, so it makes a backdoor Roth conversion partly taxable under the pro-rata rule.", null, "Simplest to run \u2014 usually less room"), strategyCard("SIMPLE IRA", "Built for small businesses with staff: you defer up to $18,100 (a solo practice always qualifies for the higher small-employer limit), and the business must add a 3% matching contribution. It cannot run alongside a Solo 401(k) in the same year \u2014 it is one or the other. For a solo owner the ceiling is simply lower than either alternative, as the comparison table above shows with your own numbers, and the balance carries the same pro-rata problem as a SEP. Worth a look mainly if you hire staff and want lower administration than a 401(k).", null, "Lowest ceiling of the three"));

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
  const recNetProfit = Math.max(1, scorpGrossBasis - scorpExpBasis);
  const psplit = payrollSplit(recNetProfit, sCorpSalaryInput);
  const runCostTotal = (payrollSvcCost || 0) + (corpReturnCost || 0) + (statementOfInfoCost || 0);
  // -------------------------------------------------------------------------
  // THE COMPARISON. One table, two structures, always both, always the same
  // two colours. Sole Prop is ENT_A (blue), Professional Corp is ENT_B (plum).
  // Green and red are never used for a column - only for the Difference verdict.
  // -------------------------------------------------------------------------
  const ssCmp = strategySoleProp.socialSecurity;   // entity-independent by construction
  const soleSep = strategySoleProp.sepIra, corpSep = strategySCorp.sepIra;
  const soleSimple = strategySoleProp.simpleIra, corpSimple = strategySCorp.simpleIra;

  const structureRows = [{
    label: "Net practice profit",
    hint: "Where both paths start — your structure cannot change what you billed",
    sole: recNetProfit,
    scorp: recNetProfit,
    big: true
  }, {
    grp: "How the money reaches you",
    grpSub: "the whole difference, in one place"
  }, {
    label: "Owner's draw",
    hint: "Not a wage. No W-2, no payroll — a sole proprietor cannot employ themselves.",
    sole: recNetProfit,
    scorp: 0
  }, {
    label: "W-2 salary",
    hint: "Only a corporation can do this. Earns Social Security; payroll tax applies.",
    sole: 0,
    scorp: sCorpSalaryInput
  }, {
    label: "Distribution",
    hint: "No payroll tax — and earns no Social Security credit",
    sole: 0,
    scorp: psplit.distribution
  }, {
    grp: "Tax this year",
    grpSub: "federal, California and payroll"
  }, {
    label: "Net take-home",
    hint: "After every tax and the CA entity fee",
    sole: soleFullYear.net,
    scorp: sCorpFullYear.net,
    big: true,
    cmp: true
  }, {
    label: "Total tax",
    hint: "Federal + CA + payroll, all in",
    sole: soleFullYear.totalTax,
    scorp: sCorpFullYear.totalTax,
    lowerBetter: true,
    cmp: true
  }, {
    label: "Self-employment + payroll tax",
    hint: "SE tax plus FICA on any salary, employer half included — the piece an S-corp split targets",
    sole: soleFullYear.seTax + soleFullYear.ssW2 + soleFullYear.medW2 + soleFullYear.employerPayrollTax,
    scorp: sCorpFullYear.seTax + sCorpFullYear.ssW2 + sCorpFullYear.medW2 + sCorpFullYear.employerPayrollTax,
    lowerBetter: true,
    cmp: true
  }, {
    label: "CA entity fee",
    hint: "California charges an S-corp the greater of $800 or 1.5% of net income. A sole proprietor pays neither.",
    sole: soleFullYear.caEntityTax,
    scorp: sCorpFullYear.caEntityTax,
    lowerBetter: true
  }, {
    grp: "Running the corporation",
    grpSub: "what the paperwork costs — zero on the left, by definition"
  }, {
    label: "Payroll service",
    hint: "Filing your own W-2 and the quarterly returns. Zero until you enter a figure above.",
    sole: 0,
    scorp: payrollSvcCost || 0,
    lowerBetter: true
  }, {
    label: "Corporate return prep",
    hint: "Form 1120-S and CA Form 100S — a return a sole proprietor does not file at all",
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
      : "Same as above until you enter your running costs — so this currently flatters the corporation",
    sole: soleFullYear.net,
    scorp: sCorpFullYear.net - runCostTotal,
    big: true,
    cmp: true
  }, {
    grp: "Retirement room it unlocks",
    grpSub: "all five plans, both structures — you pick one plan, not all of them"
  }, {
    label: "Solo 401(k) — total contribution",
    hint: "Employee deferral either way; the employer share is 20% of net SE earnings vs. 25% of W-2 salary",
    sole: strategySoleProp.solo401k.total,
    scorp: strategySCorp.solo401k.total,
    cmp: true
  }, {
    label: "Solo 401(k) — immediate tax savings",
    sole: strategySoleProp.solo401k.taxSavings,
    scorp: strategySCorp.solo401k.taxSavings
  }, {
    label: "SEP IRA — total contribution",
    hint: "Employer money only — no deferral, no catch-up at any age. 20% of net SE earnings vs. 25% of W-2 wages, capped at $72,000.",
    sole: soleSep.total,
    scorp: corpSep.total,
    cmp: true
  }, {
    label: "SEP IRA — immediate tax savings",
    sole: soleSep.taxSavings,
    scorp: corpSep.taxSavings
  }, {
    label: "SIMPLE IRA — total contribution",
    hint: "Deferral up to $18,100 plus a mandatory 3% employer match. Lower ceiling than the other two, and it cannot run alongside a Solo 401(k) in the same year — though since 2024 a SIMPLE can be swapped for a safe-harbour 401(k) mid-year.",
    sole: soleSimple.total,
    scorp: corpSimple.total,
    cmp: true
  }, {
    label: "SIMPLE IRA — immediate tax savings",
    sole: soleSimple.taxSavings,
    scorp: corpSimple.taxSavings
  }, {
    label: "Traditional IRA — deductible amount",
    hint: "Stacks on top of a workplace plan, but the deduction phases out sooner because you have one",
    sole: strategySoleProp.traditionalIra.deductibleAmount,
    scorp: strategySCorp.traditionalIra.deductibleAmount
  }, {
    label: "Roth IRA — eligible amount",
    sole: strategySoleProp.rothIra.eligibleAmount,
    scorp: strategySCorp.rothIra.eligibleAmount
  }, {
    label: "Backdoor Roth — taxable on conversion",
    hint: "Lower is better here. A SEP or SIMPLE balance counts as pre-tax IRA money and makes this worse.",
    sole: strategySoleProp.backdoorRoth.taxableOnConversion,
    scorp: strategySCorp.backdoorRoth.taxableOnConversion,
    lowerBetter: true
  }, {
    horizon: true,
    grp: "Social Security you are earning",
    grpSub: "only wages and self-employment earnings count — distributions earn nothing"
  }, {
    horizon: true,
    label: "Earnings credited this year",
    hint: "Capped at the " + fmt0(SS_WAGE_BASE_2026) + " wage base. For the corporation this is your salary and nothing else.",
    sole: ssCmp.soleCreditedEarnings,
    scorp: ssCmp.scorpCreditedEarnings,
    cmp: true
  }, {
    horizon: true,
    label: "Estimated monthly benefit at 67",
    hint: "If this year's earnings pattern held for " + ssCmp.yearsForAIME + " years. An approximation, not an SSA statement.",
    sole: ssCmp.soleMonthlyPIA,
    scorp: ssCmp.scorpMonthlyPIA,
    cmp: true
  }, {
    horizon: true,
    label: "A year of benefit at 67",
    sole: ssCmp.soleAnnualPIA,
    scorp: ssCmp.scorpAnnualPIA,
    cmp: true
  }, {
    horizon: true,
    label: "Lifetime benefit, 67 to 90",
    hint: "Today's dollars, not discounted, and before any cost-of-living increases",
    sole: ssCmp.soleLifetime,
    scorp: ssCmp.scorpLifetime,
    big: true,
    cmp: true
  }, {
    horizon: true,
    grp: "The other side of that trade",
    grpSub: "the payroll tax you skipped is real money — what if you invested it instead?"
  }, {
    horizon: true,
    label: "Payroll tax not paid, this year",
    hint: "The saving the whole strategy exists to capture",
    sole: 0,
    scorp: ssCmp.annualPayrollSaved,
    cmp: true
  }, {
    horizon: true,
    label: "That saving invested every year to retirement",
    hint: "At your " + investReturn + "% assumed return, for " + strategySoleProp.yearsToRetire + " years",
    sole: 0,
    scorp: ssCmp.investedFV
  }, {
    horizon: true,
    label: "What that pot pays out, per year at 4%",
    hint: "Compare this with the benefit two rows above. Morningstar's 2026 safe starting rate is actually 3.9%, on a 30-year horizon and a 30–50% equity mix — 4% is the familiar shorthand, not a promise.",
    sole: 0,
    scorp: ssCmp.investedDrawAnnual,
    big: true
  }];

  const COLS = [ENT_A, ENT_B];
  const structureColHead = e => /*#__PURE__*/React.createElement("th", {
    className: "cmp-h cmp-side-" + e.slug + (entityType === e.key ? " cmp-on" : ""),
    scope: "col",
    style: {background: entityType === e.key ? e.tintOn : e.tint, borderTopColor: e.ink}
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "cmp-hbtn",
    "aria-pressed": entityType === e.key,
    onClick: () => setEntityType(e.key)
  }, /*#__PURE__*/React.createElement("span", {
    className: "cmp-hname",
    style: {color: e.ink}
  }, /*#__PURE__*/React.createElement("i", {
    className: "cmp-chip",
    style: {background: e.ink}
  }, e.ch), e.name), /*#__PURE__*/React.createElement("span", {
    className: "cmp-hsub"
  }, e.key === "sole_prop" ? "no payroll, no entity fee, no extra return" : "S-corp election, salary + distribution"), /*#__PURE__*/React.createElement("span", {
    className: "cmp-hpick",
    style: entityType === e.key ? {color: "#fff", background: e.ink, borderColor: e.ink} : {color: e.ink, borderColor: e.line}
  }, entityType === e.key ? "✓ planning as this" : "Plan as this")));

  const cellFor = (e, r, val, isWin) => /*#__PURE__*/React.createElement("td", {
    className: "cmp-cell cmp-side-" + e.slug + (entityType === e.key ? " cmp-on" : "") + (isWin ? " cmp-win" : ""),
    "data-lab": e.name,
    style: {background: entityType === e.key ? e.tintOn : e.tint, borderLeftColor: e.line}
  }, isWin ? /*#__PURE__*/React.createElement("i", {className: "cmp-wintick", title: "the better of the two on this row"}, "▸") : null,
     /*#__PURE__*/React.createElement("span", {className: "cmp-v"}, fmt0(val)));

  const visibleRows = structureRows.filter(r => horizonReady || !r.horizon);
  const structureBody = visibleRows.map(r => {
    if (r.grp) {
      return /*#__PURE__*/React.createElement("tr", {key: r.grp, className: "cmp-grp"},
        /*#__PURE__*/React.createElement("td", null,
          /*#__PURE__*/React.createElement("b", null, r.grp),
          r.grpSub ? /*#__PURE__*/React.createElement("span", null, r.grpSub) : null),
        COLS.map(e => /*#__PURE__*/React.createElement("td", {
          key: e.ch,
          className: "cmp-grpcol cmp-side-" + e.slug,
          style: {color: e.ink, background: e.tint, borderLeftColor: e.line}
        }, /*#__PURE__*/React.createElement("i", {style: {background: e.ink}}, e.ch), e.short)),
        /*#__PURE__*/React.createElement("td", {className: "cmp-grpdiff"}, "vs"));
    }
    const d = r.scorp - r.sole;
    const corpAhead = r.lowerBetter ? r.scorp < r.sole : r.scorp > r.sole;
    const showWin = !!r.cmp && Math.abs(d) > 0.5;
    return /*#__PURE__*/React.createElement("tr", {
      key: r.label,
      className: "cmp-row" + (r.big ? " cmp-big" : "")
    }, /*#__PURE__*/React.createElement("td", {className: "cmp-l"},
      /*#__PURE__*/React.createElement("span", {className: "cmp-lbl"}, r.label),
      r.hint ? /*#__PURE__*/React.createElement("span", {className: "cmp-hint"}, r.hint) : null),
      cellFor(ENT_A, r, r.sole, showWin && !corpAhead),
      cellFor(ENT_B, r, r.scorp, showWin && corpAhead),
      /*#__PURE__*/React.createElement("td", {
        className: "cmp-d " + (Math.abs(d) < 0.5 ? "" : corpAhead ? "pos" : "neg"),
        "data-lab": "Difference"
      }, Math.abs(d) < 0.5 ? "—" : (d > 0 ? "+" : "−") + fmt0(Math.abs(d))));
  });

  const cmpLegend = /*#__PURE__*/React.createElement("div", {className: "cmp-legend"},
    COLS.map(e => /*#__PURE__*/React.createElement("button", {
      key: e.ch,
      type: "button",
      className: "cmp-legcard" + (entityType === e.key ? " on" : ""),
      onClick: () => setEntityType(e.key),
      style: {borderColor: entityType === e.key ? e.ink : e.line, background: entityType === e.key ? e.tintOn : e.tint}
    }, /*#__PURE__*/React.createElement("span", {className: "cmp-legtop"},
        /*#__PURE__*/React.createElement("i", {className: "cmp-chip", style: {background: e.ink}}, e.ch),
        /*#__PURE__*/React.createElement("b", {style: {color: e.ink}}, e.name)),
       /*#__PURE__*/React.createElement("span", {className: "cmp-legsub"},
         e.key === "sole_prop"
           ? "One person, no payroll, no separate return. The default until you file to change it."
           : "A California professional corporation that has elected S-corp tax treatment. Pays you a salary."),
       /*#__PURE__*/React.createElement("span", {className: "cmp-legnum"},
         e.key === "sole_prop" ? fmt0(soleFullYear.net) : fmt0(sCorpFullYear.net - runCostTotal),
         /*#__PURE__*/React.createElement("small", null, "take-home after everything")),
       /*#__PURE__*/React.createElement("span", {
         className: "cmp-legpick",
         style: entityType === e.key ? {background: e.ink, color: "#fff", borderColor: e.ink} : {color: e.ink, borderColor: e.line}
       }, entityType === e.key ? "✓ planning as this" : "Plan as this"))));

  const ssVerdict = /*#__PURE__*/React.createElement("div", {
    className: "cmp-verdict",
    style: {borderLeftColor: ssCmp.investWins ? "#3F9577" : "#C98B4B"}
  }, /*#__PURE__*/React.createElement("b", null,
      ssCmp.annualPayrollSaved <= 0
        ? "Set a salary above to see this trade-off with your own numbers."
        : ssCmp.investWins
          ? "On your assumptions, investing the saving beats the Social Security you give up."
          : "On your assumptions, the Social Security you give up is worth more than investing the saving."),
    ssCmp.annualPayrollSaved > 0 ? /*#__PURE__*/React.createElement("span", null,
      " Skipping ", /*#__PURE__*/React.createElement("b", null, fmt0(ssCmp.annualPayrollSaved)),
      " of payroll tax a year and investing it at ", investReturn, "% for ",
      strategySoleProp.yearsToRetire, " years builds ", /*#__PURE__*/React.createElement("b", null, fmt0(ssCmp.investedFV)),
      ", which draws ", /*#__PURE__*/React.createElement("b", null, fmt0(ssCmp.investedDrawAnnual)),
      " a year at 4%. The benefit you gave up is ", /*#__PURE__*/React.createElement("b", null, fmt0(ssCmp.annualGap)),
      " a year — a difference of ", /*#__PURE__*/React.createElement("b", {className: ssCmp.investWins ? "pos" : "neg"},
        fmt0(Math.abs(ssCmp.investMargin))), ssCmp.investWins ? " in favour of investing." : " in favour of the benefit.",
      " Change the return at the top of this section and this can flip — that sensitivity is the honest answer.") : null);

  const horizonNeeds = [["Your age", taxAge > 0], ["Earning since", careerStart > 0], ["Retirement age", retireAge > 0], ["Expected return", investReturn > 0]];
  const horizonMissing = horizonNeeds.filter(n => !n[1]).length;
  const horizonPeek = /*#__PURE__*/React.createElement("div", {className: "peek"},
    /*#__PURE__*/React.createElement("div", {className: "peek-blur", "aria-hidden": "true"},
      ["Earnings credited this year", "Estimated monthly benefit at 67", "Lifetime benefit, 67 to 90",
       "Payroll tax not paid, this year", "What that pot pays out, per year at 4%"].map(t =>
        /*#__PURE__*/React.createElement("div", {className: "peek-row", key: t},
          /*#__PURE__*/React.createElement("span", null, t),
          /*#__PURE__*/React.createElement("i", {style: {background: ENT_A.tintOn, color: ENT_A.ink}}, "$000,000"),
          /*#__PURE__*/React.createElement("i", {style: {background: ENT_B.tintOn, color: ENT_B.ink}}, "$000,000")))),
    /*#__PURE__*/React.createElement("div", {className: "peek-over"},
      /*#__PURE__*/React.createElement("h4", null,
        "Nine more rows, waiting on " + horizonMissing + " answer" + (horizonMissing === 1 ? "" : "s")),
      /*#__PURE__*/React.createElement("p", null,
        "Social Security, the lifetime comparison and the invest-the-difference maths all need to know how long your money has to grow. Everything above needs none of it \u2014 which is why it is already showing."),
      /*#__PURE__*/React.createElement("div", {className: "peek-need"},
        horizonNeeds.map(([lbl, ok]) => /*#__PURE__*/React.createElement("span", {
          key: lbl, className: ok ? "ok" : ""
        }, ok ? "\u2713 " : "\u25CB ", lbl))),
      /*#__PURE__*/React.createElement("button", {
        type: "button", className: "peek-go",
        onClick: () => { const el = document.getElementById("taxstep1"); if (el) el.scrollIntoView({behavior: "smooth", block: "center"}); }
      }, "Answer them \u2191")));

  const entityCompareSection = /*#__PURE__*/React.createElement("section", {
    className: "card cmp"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Both structures, side by side"),
     /*#__PURE__*/React.createElement("p", null, "Every figure below is shown for both structures on the same practice income. Blue is always Sole Proprietorship, plum is always the Professional Corp — the same two colours everywhere in this section. Picking one only highlights its column; the other stays visible so you can see what the choice costs or gains.")),
    cmpLegend,
    /*#__PURE__*/React.createElement("div", {className: "cmp-wrap"},
      /*#__PURE__*/React.createElement("table", {className: "cmp-table"},
        /*#__PURE__*/React.createElement("colgroup", null,
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-l"}),
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-a"}),
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-b"}),
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-d"})),
        /*#__PURE__*/React.createElement("thead", null,
          /*#__PURE__*/React.createElement("tr", null,
            /*#__PURE__*/React.createElement("th", {scope: "col", className: "cmp-h-l"}, ""),
            structureColHead(ENT_A),
            structureColHead(ENT_B),
            /*#__PURE__*/React.createElement("th", {className: "cmp-h-d", scope: "col"},
              /*#__PURE__*/React.createElement("span", null, "Difference"),
              /*#__PURE__*/React.createElement("small", null, "corp vs. sole")))),
        /*#__PURE__*/React.createElement("tbody", null, structureBody))),
    horizonReady ? ssVerdict : horizonPeek,
    /*#__PURE__*/React.createElement("p", {className: "pay-note"},
      "“Difference” is the Professional Corp column measured against Sole Proprietorship — green where the corp is ahead, red where it costs more, and ▲ marks the better of the two on rows where one genuinely is better. Retirement rows show what each plan would allow, not a recommendation to open all of them: a Solo 401(k) and a SIMPLE IRA cannot both run in the same year, and a SEP or SIMPLE balance is pre-tax IRA money that makes a backdoor Roth worse. Social Security figures assume this year's earnings pattern repeats and use 2026 bend points, which in reality lock in at age 62 — treat them as an approximation of the gap, not a benefit statement."))

  const entityToggle = /*#__PURE__*/React.createElement("div", {
    className: "entpick"
  }, /*#__PURE__*/React.createElement("span", {className: "entpick-lab"}, "Planning as"),
     [ENT_A, ENT_B].map(e => /*#__PURE__*/React.createElement("button", {
       key: e.key,
       type: "button",
       className: "entpick-btn" + (entityType === e.key ? " on" : ""),
       "aria-pressed": entityType === e.key,
       style: entityType === e.key
         ? {background: e.ink, borderColor: e.ink, color: "#fff"}
         : {background: e.tint, borderColor: e.line, color: e.ink},
       onClick: () => setEntityType(e.key)
     }, /*#__PURE__*/React.createElement("i", {
       className: "cmp-chip",
       style: {background: entityType === e.key ? "rgba(255,255,255,.3)" : e.ink}
     }, e.ch), e.key === "sole_prop" ? "Sole Proprietorship" : "Professional Corp (S-corp election)")));
  // One physical control for the whole strategy: drag salary left for more
  // distribution (more saving, more exposure), right for more salary (safer,
  // less saving). Both ends are labelled with what that direction costs.
  const salaryPct = recNetProfit > 0 ? Math.min(1, Math.max(0, sCorpSalaryInput / recNetProfit)) : 0;
  // A sole proprietor has no split to make, and an S-corp paying $0 salary is
  // not a lawful option - so neither state may display a "saving".
  const splitLive = sCorpSalaryInput > 0;
  const isSole = entityType === "sole_prop";
  const realSaved = splitLive ? psplit.saved : 0;
  const sliderBand = salaryBandFor(sCorpSalaryInput, recNetProfit);
  const salaryInputRow = /*#__PURE__*/React.createElement("div", {
    className: "salsplit" + (isSole ? " salsplit-inert" : ""),
    style: {borderColor: ENT_B.line, background: ENT_B.tint}
  }, /*#__PURE__*/React.createElement("div", {className: "salsplit-head"},
      /*#__PURE__*/React.createElement("span", {className: "salsplit-title"},
        entTag(ENT_B, {sm: true}), " How you split the profit"),
      /*#__PURE__*/React.createElement("span", {className: "salsplit-note"},
        isSole
          ? "You are planning as a sole proprietor, so this does not apply to you — there is no salary to set. It drives the Professional Corp column of the comparison below, so you can still see what the choice would be worth."
          : "Only a corporation has a salary. This drives every plum figure on the page.")),
    isSole ? /*#__PURE__*/React.createElement("div", {className: "salsplit-na"},
      /*#__PURE__*/React.createElement("b", null, "Not your decision as a sole proprietor. "),
      "All ", fmt0(recNetProfit), " of profit is self-employment income — there is no wage, no payroll and no distribution. Switch structure to make this control yours.",
      /*#__PURE__*/React.createElement("button", {
        type: "button", className: "salsplit-switch",
        style: {background: ENT_B.ink},
        onClick: () => setEntityType("s_corp")
      }, "Plan as a Professional Corp →")) : null,
    /*#__PURE__*/React.createElement("div", {className: "salsplit-bar"},
      /*#__PURE__*/React.createElement("i", {
        className: "salsplit-w2",
        style: {width: (salaryPct * 100) + "%", background: ENT_B.ink}
      }, salaryPct > 0.14 ? /*#__PURE__*/React.createElement("span", null, "W-2 SALARY ", fmt0(sCorpSalaryInput)) : null),
      /*#__PURE__*/React.createElement("i", {
        className: "salsplit-dist",
        style: {width: ((1 - salaryPct) * 100) + "%"}
      }, (1 - salaryPct) > 0.14 ? /*#__PURE__*/React.createElement("span", null, "DISTRIBUTION ", fmt0(Math.max(0, recNetProfit - sCorpSalaryInput))) : null)),
    /*#__PURE__*/React.createElement("input", {
      className: "salsplit-range",
      type: "range",
      min: 0,
      max: Math.max(1000, Math.round(recNetProfit)),
      step: 1000,
      value: Math.min(sCorpSalaryInput, Math.max(1000, Math.round(recNetProfit))),
      "aria-label": "W-2 salary",
      onChange: e => setSCorpSalaryInput(+e.target.value || 0)
    }),
    /*#__PURE__*/React.createElement("div", {className: "salsplit-ends"},
      /*#__PURE__*/React.createElement("span", null,
        /*#__PURE__*/React.createElement("b", null, "← more distribution"),
        "saves more payroll tax · harder to defend · less Social Security"),
      /*#__PURE__*/React.createElement("span", {className: "r"},
        /*#__PURE__*/React.createElement("b", null, "more salary →"),
        "safer if audited · costs 15.3% · earns Social Security")),
    /*#__PURE__*/React.createElement("div", {className: "salsplit-foot"},
      /*#__PURE__*/React.createElement("label", null, "Or type it:",
        /*#__PURE__*/React.createElement("input", {
          type: "number",
          min: 0,
          step: 1000,
          value: sCorpSalaryInput,
          onChange: e => setSCorpSalaryInput(+e.target.value || 0)
        })),
      sliderBand ? /*#__PURE__*/React.createElement("span", {
        className: "salsplit-band",
        style: {background: sliderBand.color}
      }, sliderBand.label, sCorpSalaryInput > 0 ? " · " + Math.floor(salaryPct * 100) + "% of profit" : "") : null,
      /*#__PURE__*/React.createElement("span", {className: "salsplit-saving" + (splitLive ? "" : " none")},
        splitLive
          ? fmt0(realSaved) + " of payroll tax avoided"
          : "No saving — a $0 salary is not a lawful S-corp")),
    /*#__PURE__*/React.createElement("div", {className: "salsplit-counters"},
      /*#__PURE__*/React.createElement("div", {className: "sc" + (splitLive ? " up" : " nil")},
        /*#__PURE__*/React.createElement("i", null, splitLive ? "↑" : "–"),
        /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, fmt0(realSaved)),
          splitLive ? "payroll tax avoided" : "nothing avoided until a salary is set")),
      /*#__PURE__*/React.createElement("div", {className: "sc" + (splitLive ? " dn" : " nil")},
        /*#__PURE__*/React.createElement("i", null, splitLive ? "↓" : "–"),
        /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, fmt0(splitLive ? strategySCorp.solo401k.total : 0)),
          "Solo 401(k) room — the employer share is 25% of salary")),
      /*#__PURE__*/React.createElement("div", {className: "sc" + (splitLive ? " dn" : " nil")},
        /*#__PURE__*/React.createElement("i", null, splitLive ? "↓" : "–"),
        /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, fmt0(splitLive ? ssCmp.scorpMonthlyPIA : 0), "/mo"),
          "Social Security at 67 — only wages earn credit"))),
    /*#__PURE__*/React.createElement("p", {className: "salsplit-warn"},
      "Dragging left saves payroll tax and costs you the other two. Those effects are the same order of magnitude — moving from the 50% benchmark to the 35% line saves roughly ",
      fmt0(recNetProfit * 0.15 * 0.153), " of payroll tax while destroying about ",
      fmt0(recNetProfit * 0.15 * 0.25), " of pre-tax retirement room. At any plausible marginal rate those very nearly cancel."));

const netDiff = sCorpFullYear.net - soleFullYear.net;
  // An S-corp paying $0 salary is not a lawful option, so it must never be "recommended".
  const salaryUnset = !(sCorpSalaryInput > 0);
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
    /*#__PURE__*/React.createElement("h4", null, "First, how you actually become one"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "None of the numbers on this page are true until these are done. The S-corp election in particular is a single form with a hard deadline — miss it and you have a C corporation, which is taxed quite differently."),
    /*#__PURE__*/React.createElement("div", {className: "setuptl"},
      [["1", "Articles of Incorporation",
        "Filed with the California Secretary of State, $100. The name must contain “marriage”, “family” or “child” together with “counseling”, “counselor”, “therapy” or “therapist”, plus a corporate designator — that is a statutory naming rule, not a style choice.", null],
       ["2", "Bylaws, shares and first minutes",
        "Shares may only ever be issued to licensed professionals, and a marriage and family therapy corporation must be at least 51% MFT-owned. A buy-sell agreement matters: if a shareholder dies or is disciplined, the shares must be repurchased rather than pass to someone unlicensed.",
        ["https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=13401.5.&lawCode=CORP", "Cal. Corp. Code §13401.5"]],
       ["3", "EIN, a separate bank account, a payroll account",
        "The separate account is not a formality. Commingling personal and corporate money is the fastest way to lose the liability separation you incorporated for.", null],
       ["4", "Form 2553 — the S election itself",
        "The form the entire strategy depends on. Generally due within 2 months and 15 days of the beginning of the tax year it is to take effect. Without it you have a C corporation and none of the figures on this page apply to you.",
        ["https://www.irs.gov/forms-pubs/about-form-2553", "IRS Form 2553"]],
       ["5", "Register as an employer with the EDD",
        "Within 15 days of paying more than $100 in wages in a calendar quarter. Any officer salary trips this immediately.", null]
      ].map(([n, t, d, lk]) => /*#__PURE__*/React.createElement("div", {className: "stl", key: n},
        /*#__PURE__*/React.createElement("i", null, n),
        /*#__PURE__*/React.createElement("div", null,
          /*#__PURE__*/React.createElement("b", null, t),
          /*#__PURE__*/React.createElement("p", null, d, lk ? " " : null, lk ? extLink(lk[0], lk[1]) : null))))),
    /*#__PURE__*/React.createElement("h4", {style: {marginTop: 22}}, "Then, every year, forever"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "A sole proprietor files none of the following — practice income goes on Schedule C inside the personal return you already file. Electing S-corp treatment makes you your own employer, and that creates real, recurring paperwork. Every link opens in a new tab."),
    /*#__PURE__*/React.createElement("div", {className: "compliance-cols"},
      /*#__PURE__*/React.createElement("div", {className: "compliance-col"},
        /*#__PURE__*/React.createElement("h5", null, "Federal"),
        /*#__PURE__*/React.createElement("ul", null,
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-941", "Form 941"), " — every quarter. Reports the income tax, Social Security and Medicare withheld from your own wages, plus the employer half."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-940", "Form 940"), " — once a year, federal unemployment tax. Paid by the employer only."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-w-2", "Form W-2"), " and a W-3 — by ", /*#__PURE__*/React.createElement("b", null, "31 January"), ", issued by you, to you."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.irs.gov/forms-pubs/about-form-1120-s", "Form 1120-S"), " plus a Schedule K-1 — due ", /*#__PURE__*/React.createElement("b", null, "15 March"), ", a month before your personal return. This is the deadline people miss in year one."))),
      /*#__PURE__*/React.createElement("div", {className: "compliance-col"},
        /*#__PURE__*/React.createElement("h5", null, "California"),
        /*#__PURE__*/React.createElement("ul", null,
          /*#__PURE__*/React.createElement("li", null, extLink("https://edd.ca.gov/en/payroll_taxes/Am_I_Required_to_Register_as_an_Employer/", "Register with the EDD"), " — required once you pay more than $100 in wages in a calendar quarter, within 15 days. Any officer salary trips this immediately."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://edd.ca.gov/en/payroll_taxes/required_filings_and_due_dates/", "DE 9 and DE 9C"), " — every quarter, wage reconciliation and per-employee detail."),
          /*#__PURE__*/React.createElement("li", null, extLink("https://www.ftb.ca.gov/file/business/types/corporations/s-corporations.html", "Form 100S"), " — the CA S-corp return, also due ", /*#__PURE__*/React.createElement("b", null, "15 March"), ". 1.5% of net income, with an $800 minimum — waived in the first year only."),
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
      "While these are zero the comparison below shows the tax difference only, which will overstate what an S-corp is worth to you."),
    /*#__PURE__*/React.createElement("div", {className: "habit"},
      /*#__PURE__*/React.createElement("h5", null, "And two things that are habit rather than cost"),
      /*#__PURE__*/React.createElement("p", null,
        /*#__PURE__*/React.createElement("b", null, "Run payroll on a real schedule. "),
        "“I'll true it up in December” is how reasonable-compensation arguments are lost. Keep separate books, and keep a written file supporting your salary — the wage data for your metro, your hours, the roles you perform. Cheap to keep as you go, near-impossible to reconstruct three years later under examination."),
      /*#__PURE__*/React.createElement("p", null,
        /*#__PURE__*/React.createElement("b", null, "Keep the annual minutes. "),
        "Nobody enforces them until something goes wrong, at which point their absence becomes the argument against you.")),
    /*#__PURE__*/React.createElement("div", {className: "exitnote"},
      /*#__PURE__*/React.createElement("b", null, "The door out, which most write-ups skip. "),
      "Dissolving a California corporation takes its own filings, a final return and a final Statement of Information — and the $800 minimum applies for any year the entity exists, including a year you barely trade. If your income falls back under six figures, unwinding is not free. Worth knowing before you walk in."));
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
  const leversPanel = (function () {
    if (!(cur.grossYr > 0) || !(sessionRate > 0)) {
      return /*#__PURE__*/React.createElement("section", {className: "card levers levers-empty"},
        /*#__PURE__*/React.createElement("div", {className: "card-head"},
          /*#__PURE__*/React.createElement("h2", null, "What actually moves the number"),
          /*#__PURE__*/React.createElement("p", null,
            "Once your rate and caseload are in, this ranks every lever you have \u2014 raising your rate, adding sessions, electing S-corp, cutting costs \u2014 by what each one adds to what you keep. The ranking is often surprising.")));
    }
    const keepRate = cur.netYr / cur.grossYr;
    const sess = cur.grossYr / sessionRate;                       // sessions a year at the current fee
    const rows = [
      {k: "rate", label: "Raise your rate " + fmt0(sessionRate) + " → " + fmt0(sessionRate + 25),
       sub: "same caseload, same hours", v: 25 * sess * keepRate},
      {k: "sess", label: "Add 2 sessions a week",
       sub: fmt0(sessionRate * 2 * weeksWorkedProp) + " more billed", v: sessionRate * 2 * weeksWorkedProp * keepRate},
      {k: "scorp", label: "Elect S-corp treatment",
       sub: "after payroll, filings and the CA entity fee", v: Math.max(0, netDiff - runCostTotal)},
      {k: "exp", label: "Cut running costs 10%",
       sub: "on " + fmt0(cur.expYr) + " of expenses", v: cur.expYr * 0.10 * keepRate}
    ].sort((a, b) => b.v - a.v);
    const top = Math.max(1, rows[0].v);
    return /*#__PURE__*/React.createElement("section", {className: "card levers"},
      /*#__PURE__*/React.createElement("div", {className: "card-head"},
        /*#__PURE__*/React.createElement("h2", null, "What actually moves the number"),
        /*#__PURE__*/React.createElement("p", null,
          "Every lever below, measured the same way — what it adds to what you keep in a year. Ranked honestly, including when that ranking is inconvenient for the tax advice above.")),
      rows.map(r => /*#__PURE__*/React.createElement("div", {className: "lever", key: r.k},
        /*#__PURE__*/React.createElement("span", {className: "lever-name"},
          /*#__PURE__*/React.createElement("b", null, r.label),
          /*#__PURE__*/React.createElement("span", null, r.sub)),
        /*#__PURE__*/React.createElement("span", {className: "lever-bar"},
          /*#__PURE__*/React.createElement("i", {style: {width: Math.max(2, r.v / top * 100) + "%", background: r.k === "scorp" ? "#C98B4B" : "#3F9577"}})),
        /*#__PURE__*/React.createElement("span", {className: "lever-val"}, "+" + fmt0(r.v)))),
      rows[0].k !== "scorp" && netDiff > 0 ? /*#__PURE__*/React.createElement("p", {className: "lever-note"},
        /*#__PURE__*/React.createElement("b", null, "Worth sitting with: "),
        "the entity decision is worth ", /*#__PURE__*/React.createElement("b", null, fmt0(Math.max(0, netDiff - runCostTotal))),
        " a year. “", rows[0].label, "” is worth ", /*#__PURE__*/React.createElement("b", null, fmt0(rows[0].v)),
        " — roughly ", /*#__PURE__*/React.createElement("b", null, Math.max(1, Math.round(rows[0].v / Math.max(1, netDiff - runCostTotal))) + "×"),
        " as much, with no filings, no payroll and no audit exposure. Incorporating is a real lever, but it is rarely the biggest one on this page.") : null,
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        "Rate and caseload figures apply your current take-home rate of ", Math.round(keepRate * 100),
        "% to the extra billing — a simplification, since more income can push you into a higher bracket. The S-corp figure is net of the running costs you entered."));
  })();
  // What people who do this for a living actually say. Named sources, real
  // links, plus the federal Census data on how CA practices are actually
  // structured - the number everybody asks for and nobody in this space uses.
  const expertSection = /*#__PURE__*/React.createElement("details", {
    className: "card collapsible expert"
  }, /*#__PURE__*/React.createElement("summary", {className: "card-head"},
      /*#__PURE__*/React.createElement("h2", null, "What the lawyers and accountants actually say"),
      /*#__PURE__*/React.createElement("p", null,
        "Three named sources who work with California therapists specifically — where they agree, where they disagree with each other — plus federal data on how California practices are actually structured.")),
    /*#__PURE__*/React.createElement("div", {className: "expert-q"},
      /*#__PURE__*/React.createElement("div", {className: "expert-who"},
        /*#__PURE__*/React.createElement("b", null, "Michael J. Leonard, Esq."),
        /*#__PURE__*/React.createElement("span", null, "San Diego Corporate Law · California business attorney")),
      /*#__PURE__*/React.createElement("p", null,
        "Comes down firmly on the corporation: a Professional Marriage and Family Therapy Corporation electing S-corp treatment is, in his words, ",
        /*#__PURE__*/React.createElement("i", null, "“the California business entity of choice for marriage and family therapists”"),
        " — on the strength of both the payroll-tax split and the separation of business debts from personal assets."),
      /*#__PURE__*/React.createElement("div", {className: "expert-caveat"},
        /*#__PURE__*/React.createElement("b", null, "The part people skip: "),
        "he is equally clear that incorporating does ", /*#__PURE__*/React.createElement("b", null, "not"),
        " shield you from your own malpractice. California therapists remain ",
        /*#__PURE__*/React.createElement("i", null, "“personally liable for their own malpractice or professional misconduct, which liability cannot be shielded by any business entity”"),
        ". A corporation protects you from the landlord, not from a licensing board complaint. Malpractice insurance is what covers the clinical risk, and it does that whichever structure you pick."),
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        extLink("https://sdcorporatelaw.com/business-newsletter/sole-proprietorship-vs-professional-marriage-and-family-therapy-corporation-in-california/",
          "Sole Proprietorship vs Professional Marriage and Family Therapy Corporation in California"))),
    /*#__PURE__*/React.createElement("div", {className: "expert-q"},
      /*#__PURE__*/React.createElement("div", {className: "expert-who"},
        /*#__PURE__*/React.createElement("b", null, "Heard"),
        /*#__PURE__*/React.createElement("span", null, "accounting firm working only with therapists")),
      /*#__PURE__*/React.createElement("p", null,
        "Sets a floor rather than a rule: on the basis of doing the books for thousands of therapy practices they recommend ",
        /*#__PURE__*/React.createElement("b", null, "$100,000 of annual net income"),
        " before an S-corp election is worth making, and put the ongoing cost of running one at roughly ",
        /*#__PURE__*/React.createElement("b", null, "$4,400 a year"),
        " in extra bookkeeping, payroll and filing fees. Their worked California example — $150,000 of income — nets about ",
        /*#__PURE__*/React.createElement("b", null, "$6,310 a year"),
        " after those costs. Their Georgia example at $80,000 ", /*#__PURE__*/React.createElement("b", {className: "neg"}, "loses $1,340"), "."),
      /*#__PURE__*/React.createElement("div", {className: "expert-yours"},
        recNetProfit > 1
          ? /*#__PURE__*/React.createElement("span", null,
              "Your net profit is ", /*#__PURE__*/React.createElement("b", null, fmt0(recNetProfit)), " — ",
              recNetProfit >= 100000
                ? /*#__PURE__*/React.createElement("b", {className: "pos"}, "above their threshold.")
                : /*#__PURE__*/React.createElement("b", {className: "neg"}, "below their threshold."),
              " This tool puts the election at ", /*#__PURE__*/React.createElement("b", null, fmt0(Math.max(0, netDiff - runCostTotal))),
              " a year net of the running costs you entered",
              runCostTotal <= 0 ? " — and you have entered none, so that figure is currently the best case, not the likely one." : ".")
          : /*#__PURE__*/React.createElement("span", null, "Enter your income and expenses to see where you sit against that threshold.")),
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        extLink("https://www.joinheard.com/articles/how-much-do-therapists-really-save-by-switching-to-an-s-corp",
          "How Much Do Therapists Really Save With an S Corp?"), " · ",
        extLink("https://www.joinheard.com/articles/the-complete-guide-to-s-corporations-for-therapists",
          "The Complete S Corp Guide for Private Practice Therapists"))),
    /*#__PURE__*/React.createElement("div", {className: "expert-q"},
      /*#__PURE__*/React.createElement("div", {className: "expert-who"},
        /*#__PURE__*/React.createElement("b", null, "The IRS"),
        /*#__PURE__*/React.createElement("span", null, "the only opinion that is binding")),
      /*#__PURE__*/React.createElement("p", null,
        "Publishes no percentage and never has. The requirement is that an officer performing more than minor services be paid ",
        /*#__PURE__*/React.createElement("b", null, "reasonable compensation"),
        " for the work actually done, before any distribution. The “50% of profit” figure repeated across every private-practice blog is a practitioner convention that has no standing in an audit — what gets defended is a salary you can tie to what a comparable clinician is paid."),
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        extLink("https://www.irs.gov/pub/irs-news/fs-08-25.pdf", "IRS Fact Sheet FS-2008-25 — Wage Compensation for S Corporation Officers"))),
    /*#__PURE__*/React.createElement("div", {className: "expert-nodata census"},
      /*#__PURE__*/React.createElement("h4", null, "What California therapists actually do"),
      /*#__PURE__*/React.createElement("p", null,
        "Nobody surveys this. CAMFT's last demographic survey was 2015 and never asked about legal form; the BBS licenses therapists without asking how they are taxed; the one national survey that does ask reports “LLC/PLLC” as its largest category — a form California-licensed therapists ",
        /*#__PURE__*/React.createElement("i", null, "cannot legally use"), " for licensed services. So the figures below come from somewhere else: federal business statistics built from tax filings, not from a questionnaire. No self-selection, no response bias."),
      /*#__PURE__*/React.createElement("p", null,
        "The answer flips depending on which universe you count, and that turns out to be the whole point."),
      /*#__PURE__*/React.createElement("div", {className: "cendual"},
        [{k: "all", lab: "All CA mental-health practices", n: "33,660 establishments",
          you: isSole,
          seg: [{p: 78.0, c: ENT_A.ink, t: "Sole prop", v: "78%"},
                {p: 18.1, c: ENT_B.ink, t: "S corp", v: "18%"},
                {p: 3.9, c: "#B7B0A2", t: "Other", v: "4%"}]},
         {k: "pay", lab: "CA practices large enough to run payroll", n: "6,953 establishments",
          you: !isSole,
          seg: [{p: 11.1, c: ENT_A.ink, t: "Sole prop", v: "11%"},
                {p: 72.4, c: ENT_B.ink, t: "S corp", v: "72%"},
                {p: 16.5, c: "#B7B0A2", t: "Other", v: "17%"}]}
        ].map(r => /*#__PURE__*/React.createElement("div", {className: "cenrow" + (r.you ? " you" : ""), key: r.k},
          /*#__PURE__*/React.createElement("div", {className: "cenhead"},
            /*#__PURE__*/React.createElement("b", null, r.lab),
            /*#__PURE__*/React.createElement("span", null, r.n),
            r.you ? /*#__PURE__*/React.createElement("em", null, "the group you are in") : null),
          /*#__PURE__*/React.createElement("div", {className: "cenbar"},
            r.seg.map(g => /*#__PURE__*/React.createElement("i", {
              key: g.t, style: {width: g.p + "%", background: g.c}
            }, g.p >= 6 ? /*#__PURE__*/React.createElement("span", null, g.v) : null))),
          /*#__PURE__*/React.createElement("div", {className: "cenkey"},
            r.seg.map(g => /*#__PURE__*/React.createElement("span", {key: g.t},
              /*#__PURE__*/React.createElement("i", {style: {background: g.c}}), g.t, " ", g.v)))))),
      /*#__PURE__*/React.createElement("p", null,
        /*#__PURE__*/React.createElement("b", null, "Why the two rows disagree. "),
        "A sole proprietor has no payroll, so she is counted in the nonemployer file. A professional corporation that pays its owner a W-2 salary has payroll by definition, so it is counted in the employer file. The two universes are near-mutually-exclusive ",
        /*#__PURE__*/React.createElement("i", null, "on exactly the axis being measured"),
        " — which is why “78% are sole proprietors” and “72% are S corps” are both true and neither settles anything on its own. The first row is dominated by very small and part-time practices: nationally, 43% of nonemployer practices in this category bill under $25,000 a year."),
      /*#__PURE__*/React.createElement("div", {className: "cenflag"},
        /*#__PURE__*/React.createElement("b", null, "1,049"),
        /*#__PURE__*/React.createElement("span", null,
          "California S corporations in this category run ", /*#__PURE__*/React.createElement("b", null, "zero payroll"),
          " — shareholders taking distributions and paying themselves no salary at all. That is the reasonable-compensation exposure this section warns about, as a counted number rather than a hypothetical. Their average receipts are $89,112, against $60,563 for sole proprietors.")),
      /*#__PURE__*/React.createElement("p", null,
        /*#__PURE__*/React.createElement("b", null, "What this does not say. "),
        "The industry code covers all non-physician mental health practitioners — LMFTs, LCSWs, LPCCs, psychologists — with no licence-level cut. It counts establishments, not therapists, so a group practice with two offices counts twice. And because the classification follows the tax filing, a single-member LLC that has not elected corporate treatment is coded “sole proprietorship” — which matters little in California, where licensed therapists cannot use an LLC anyway, but means the label reads as “files Schedule C.”"),
      /*#__PURE__*/React.createElement("p", null,
        "For income rather than structure, the useful survey is Heard's ", /*#__PURE__*/React.createElement("b", null, "Financial State of Private Practice"),
        " — median practice revenue of ", /*#__PURE__*/React.createElement("b", null, "$80,412"),
        " in 2025, up 18% year over year; about ", /*#__PURE__*/React.createElement("b", null, "$105"),
        " a session on insurance against roughly ", /*#__PURE__*/React.createElement("b", null, "$150"),
        " private pay; only ", /*#__PURE__*/React.createElement("b", null, "33%"),
        " raised their fees at all in 2025; taxes named the number-one headache by ",
        /*#__PURE__*/React.createElement("b", null, "53.6%"), ". Hold that ", /*#__PURE__*/React.createElement("b", null, "$80,412"),
        " median next to Heard's own $100,000 S-corp threshold: for most therapists in the country, on that evidence, the answer to this entire section is “not yet.”"),
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
        extLink("https://www.census.gov/programs-surveys/cbp.html",
          "US Census Bureau, County Business Patterns"), " and ",
        extLink("https://www.census.gov/programs-surveys/nonemployer-statistics.html",
          "Nonemployer Statistics"),
        ", 2023 reference year, NAICS 621330 (Offices of Mental Health Practitioners, except Physicians), California. Legal form of organization derived from tax filings. · ",
        extLink("https://www.joinheard.com/resources/downloads/the-heard-2026-financial-state-of-private-practice-report",
          "The Heard 2026 Financial State of Private Practice Report"))),
    /*#__PURE__*/React.createElement("p", {className: "pay-note"},
      "These are other people's published views, quoted because they are named, findable and specific — not endorsements, and not advice about your situation. Two of the three sell a service related to the answer they give, which is worth holding in mind. A California CPA or business attorney looking at your actual numbers is the only way to settle it."));

  // =====================================================================
  // The opener, the stepper, the money flow and Social Security in full.
  // All four are pure output - every variable they touch is declared above.
  // =====================================================================
  const secOpener = /*#__PURE__*/React.createElement("section", {className: "card opener"},
    /*#__PURE__*/React.createElement("div", {className: "opener-eyebrow"}, "Section 4 of 4 · about 5 minutes"),
    /*#__PURE__*/React.createElement("h2", null, "What you keep, and the two decisions that change it"),
    /*#__PURE__*/React.createElement("p", null,
      "Your income and expenses are settled by now. This section is about the part you still control: ",
      /*#__PURE__*/React.createElement("b", null, "how your practice is structured"), ", and ",
      /*#__PURE__*/React.createElement("b", null, "where you put money before it is taxed"),
      ". Those are the only two legal levers most solo therapists have, and together they can move your take-home by five figures a year."),
    /*#__PURE__*/React.createElement("p", null,
      "It works by running your real numbers twice — once as a Sole Proprietorship, once as a Professional Corp with an S-corp election — and showing every figure side by side. Nothing here is a rule of thumb; each number traces back to your own rate and caseload."),
    /*#__PURE__*/React.createElement("div", {className: "opener-qs"},
      [["Should I incorporate?", "What the election is worth on your income, net of what it costs to run."],
       ["What salary do I pay myself?", "Where your number sits against published wages for your licence — and against the percentage conventions."],
       ["Which retirement account?", "All five, both structures, with your actual contribution room."],
       ["What am I giving up?", "The Social Security you do not earn — and whether investing the difference beats it."]
      ].map(([q, a]) => /*#__PURE__*/React.createElement("div", {className: "opener-q", key: q},
        /*#__PURE__*/React.createElement("b", null, q), /*#__PURE__*/React.createElement("span", null, a)))),
    /*#__PURE__*/React.createElement("div", {className: "opener-cant"},
      /*#__PURE__*/React.createElement("b", null, "What this cannot do"),
      "It does not know your past earnings, a spouse's income, where you will live next year, or anything about your clinical risk. It is a model to argue with and to take to a CPA — not a filing."));

  const stepStates = [
    {n: "1", t: "About you", s: step1Count >= 4 ? "age " + taxAge + " · retiring " + retireAge + " · " + investReturn + "%" : step1Count + " of 4 answered", done: step1Count >= 4},
    {n: "2", t: "Structure & salary", s: sCorpSalaryInput > 0 ? "salary " + fmt0(sCorpSalaryInput) : "no salary set", done: sCorpSalaryInput > 0},
    {n: "3", t: "Running costs", s: runCostTotal > 0 ? fmt0(runCostTotal) + " a year" : "optional — zero flatters the corp", done: runCostTotal > 0, opt: true},
    {n: "→", t: "Compare & decide", s: horizonReady ? "all 28 rows open" : "9 rows need step 1", done: horizonReady, out: true}
  ];
  const stepsDone = stepStates.filter(x => x.done).length;
  const stepperRail = /*#__PURE__*/React.createElement("div", {className: "rail-wrap"},
    /*#__PURE__*/React.createElement("div", {className: "rail"},
      stepStates.map(x => /*#__PURE__*/React.createElement("div", {
        key: x.t,
        className: "rail-step" + (x.done ? " done" : x.opt ? " opt" : "") + (x.out ? " out" : "")
      }, /*#__PURE__*/React.createElement("span", {className: "rail-top"},
          /*#__PURE__*/React.createElement("i", {className: "rail-n"}, x.done ? "✓" : x.n),
          /*#__PURE__*/React.createElement("b", null, x.t)),
        /*#__PURE__*/React.createElement("span", {className: "rail-s"}, x.s)))),
    /*#__PURE__*/React.createElement("div", {className: "rail-bar"},
      /*#__PURE__*/React.createElement("i", {style: {width: (stepsDone / 4 * 100) + "%"}})),
    /*#__PURE__*/React.createElement("div", {className: "rail-meta"},
      /*#__PURE__*/React.createElement("b", null, stepsDone + " of 4 done"),
      /*#__PURE__*/React.createElement("span", null, "everything saves as you type")));

  // ---- where the money actually goes ----------------------------------
  // Computed by running the engine twice, WITH and WITHOUT the contribution.
  // The old version multiplied the contribution by the *marginal* rate, which
  // overstated the saving badly: the marginal rate at the top of the range is
  // ~55% (the SSTB QBI phase-out amplifies it) but it falls away as income
  // drops, so the true effective rate across a $72k deduction is nearer 38%.
  const mfEmp = strategy.solo401k.employeeContrib || 0;
  const mfEr = strategy.solo401k.employerContrib || 0;
  const mfContrib = mfEmp + mfEr;
  const mfNone = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput);
  const mfWith = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, mfEr, mfEmp, entityType, sCorpSalaryInput);
  const mfTaxNone = mfNone.totalTax, mfBankNone = mfNone.net;
  const mfTaxWith = mfWith.totalTax, mfBankWith = mfWith.net;
  const mfProfit = Math.max(1, mfTaxNone + mfBankNone);
  const mfSaved = mfTaxNone - mfTaxWith;
  const mfTotalWith = mfBankWith + mfContrib;
  const mfCost = mfBankNone - mfBankWith;
  const mfEffRate = mfContrib > 0 ? mfSaved / mfContrib : 0;
  const mfYears = Math.max(0, retireAge - taxAge);
  const mfGrown = horizonReady ? mfContrib * Math.pow(1 + investReturn / 100, mfYears) : 0;

  const MF_A = {k: "none", name: "Contribute nothing", ink: "#7C766A", tint: "#F6F3EC", tintOn: "#EFEAE0", line: "#DCD5C6"};
  const MF_B = {k: "max", name: "Max the Solo 401(k)", ink: "#2F7A61", tint: "#F1F7F4", tintOn: "#E4F0EA", line: "#B7D6C7"};
  const mfBar = (tax, inv, bank) => /*#__PURE__*/React.createElement("span", {className: "mfmini"},
    /*#__PURE__*/React.createElement("i", {style: {width: (tax / mfProfit * 100) + "%", background: "#B5483F"}}),
    inv > 0 ? /*#__PURE__*/React.createElement("i", {style: {width: (inv / mfProfit * 100) + "%", background: "#3F9577"}}) : null,
    /*#__PURE__*/React.createElement("i", {style: {width: (Math.max(0, bank) / mfProfit * 100) + "%", background: "#26241E"}}));

  const mfRows = [
    {label: "Tax — to the IRS and California", hint: "Gone for good either way. This is the only figure the contribution actually changes.",
     a: mfTaxNone, b: mfTaxWith, lowerBetter: true, cmp: true},
    {label: "Into your investment account", hint: "Still yours. Locked until 59½ with narrow exceptions.",
     a: 0, b: mfContrib, cmp: true},
    {label: "Into your bank account", hint: "Spendable this year — this is the number that goes down",
     a: mfBankNone, b: mfBankWith, cmp: true},
    {label: "Total you end up with", hint: "Bank account plus investment account. Both are yours; only one is liquid.",
     a: mfBankNone, b: mfTotalWith, big: true, cmp: true}
  ];

  const moneyFlow = mfContrib <= 0 ? null : /*#__PURE__*/React.createElement("section", {className: "card cmp mfc"},
    /*#__PURE__*/React.createElement("div", {className: "card-head"},
      /*#__PURE__*/React.createElement("h2", null, "Contribute nothing, or max the Solo 401(k)"),
      /*#__PURE__*/React.createElement("p", null,
        "The same ", fmt0(mfProfit), " of profit, split two ways, side by side — grey is doing nothing, green is contributing ",
        fmt0(mfContrib), ". Read down a column to see where that profit lands; read across a row to see what changes.")),
    /*#__PURE__*/React.createElement("div", {className: "fkey"},
      [["#B5483F", "Tax", "gone, to the IRS and California"],
       ["#3F9577", "Invested", "still yours, locked until 59½"],
       ["#26241E", "Bank account", "yours, spendable now"]
      ].map(([c, t, d]) => /*#__PURE__*/React.createElement("span", {key: t},
        /*#__PURE__*/React.createElement("i", {style: {background: c}}), /*#__PURE__*/React.createElement("b", null, t),
        /*#__PURE__*/React.createElement("em", null, "— " + d)))),
    /*#__PURE__*/React.createElement("div", {className: "cmp-wrap"},
      /*#__PURE__*/React.createElement("table", {className: "cmp-table mftable"},
        /*#__PURE__*/React.createElement("colgroup", null,
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-l"}),
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-a"}),
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-b"}),
          /*#__PURE__*/React.createElement("col", {className: "cmp-col-d"})),
        /*#__PURE__*/React.createElement("thead", null,
          /*#__PURE__*/React.createElement("tr", null,
            /*#__PURE__*/React.createElement("th", {className: "cmp-h-l", scope: "col"}, ""),
            [MF_A, MF_B].map(e => /*#__PURE__*/React.createElement("th", {
              key: e.k, scope: "col", className: "cmp-h mfh",
              style: {background: e.tint, borderTopColor: e.ink}
            }, /*#__PURE__*/React.createElement("span", {className: "mfh-in"},
                /*#__PURE__*/React.createElement("b", {style: {color: e.ink}}, e.name),
                /*#__PURE__*/React.createElement("small", null, e.k === "none" ? "the default" : fmt0(mfContrib) + " a year"),
                e.k === "none" ? mfBar(mfTaxNone, 0, mfBankNone) : mfBar(mfTaxWith, mfContrib, mfBankWith)))),
            /*#__PURE__*/React.createElement("th", {className: "cmp-h-d", scope: "col"},
              /*#__PURE__*/React.createElement("span", null, "Difference"),
              /*#__PURE__*/React.createElement("small", null, "max vs. nothing")))),
        /*#__PURE__*/React.createElement("tbody", null, mfRows.map(r => {
          const d = r.b - r.a;
          const bAhead = r.lowerBetter ? r.b < r.a : r.b > r.a;
          const win = r.cmp && Math.abs(d) > 0.5;
          return /*#__PURE__*/React.createElement("tr", {key: r.label, className: "cmp-row" + (r.big ? " cmp-big" : "")},
            /*#__PURE__*/React.createElement("td", {className: "cmp-l"},
              /*#__PURE__*/React.createElement("span", {className: "cmp-lbl"}, r.label),
              r.hint ? /*#__PURE__*/React.createElement("span", {className: "cmp-hint"}, r.hint) : null),
            [[MF_A, r.a, win && !bAhead], [MF_B, r.b, win && bAhead]].map(([e, v, isWin]) =>
              /*#__PURE__*/React.createElement("td", {
                key: e.k, className: "cmp-cell mf-" + e.k + (isWin ? " cmp-win" : ""),
                "data-lab": e.name, style: {background: e.tint, borderLeftColor: e.line}
              }, isWin ? /*#__PURE__*/React.createElement("i", {className: "cmp-wintick"}, "▸") : null,
                 /*#__PURE__*/React.createElement("span", {className: "cmp-v"}, fmt0(v)))),
            /*#__PURE__*/React.createElement("td", {
              className: "cmp-d " + (Math.abs(d) < 0.5 ? "" : bAhead ? "pos" : "neg"), "data-lab": "Difference"
            }, Math.abs(d) < 0.5 ? "—" : (d > 0 ? "+" : "−") + fmt0(Math.abs(d))));
        })))),
    /*#__PURE__*/React.createElement("div", {className: "mfpunch"},
      /*#__PURE__*/React.createElement("b", null, "You end up ", fmt0(mfSaved), " ahead — and ", fmt0(mfCost), " less liquid."),
      "Both are true at once, and confusing them is why this feels harder than it is. Your ",
      /*#__PURE__*/React.createElement("b", null, "spendable cash"), " falls from ", fmt0(mfBankNone), " to ", fmt0(mfBankWith),
      ". Your ", /*#__PURE__*/React.createElement("b", null, "total for the year"), " rises from ", fmt0(mfBankNone),
      " to ", fmt0(mfTotalWith), ". The gap between those two sentences is exactly the ", fmt0(mfSaved),
      " of tax you did not pay — money that was leaving your hands either way. The only question was whether the IRS got it or you did."),
    /*#__PURE__*/React.createElement("div", {className: "mftrade"},
      /*#__PURE__*/React.createElement("div", {className: "mft cost"},
        /*#__PURE__*/React.createElement("b", null, "What it costs — ", fmt0(mfCost)),
        "Cash that does not reach your bank this year, locked until 59½ with narrow exceptions. If you need it for a deposit or a thin year, that is a real cost, not a technicality."),
      /*#__PURE__*/React.createElement("div", {className: "mft gain"},
        /*#__PURE__*/React.createElement("b", null, "What you gain — ", fmt0(mfSaved)),
        "Tax you would have paid, working for you instead. Across the whole ", fmt0(mfContrib),
        " that is an effective ", (mfEffRate * 100).toFixed(0), "% — the first dollars you shelter save more than the last, because your rate falls as your taxable income comes down.")),
    horizonReady && mfGrown > 0 ? /*#__PURE__*/React.createElement("div", {className: "mflater"},
      /*#__PURE__*/React.createElement("div", {className: "mflater-h"}, "And then it grows — this one year's contribution, held to ", retireAge),
      /*#__PURE__*/React.createElement("div", {className: "mflater-b"},
        /*#__PURE__*/React.createElement("span", {className: "n"}, fmt0(mfGrown)),
        /*#__PURE__*/React.createElement("span", {className: "d"},
          /*#__PURE__*/React.createElement("b", null, fmt0(mfContrib) + " compounding at " + investReturn + "% for " + mfYears + " years."),
          " That is a single year's contribution. Repeat it annually and the comparison table's projection applies instead."))) : null,
    /*#__PURE__*/React.createElement("div", {className: "mfwarn"},
      /*#__PURE__*/React.createElement("b", null, "The honest asterisk: "),
      "a Solo 401(k) is tax-", /*#__PURE__*/React.createElement("i", null, "deferred"),
      ", not tax-free. You will pay ordinary income tax when you draw it down — the bet is that your rate in retirement is lower than the ",
      (mfEffRate * 100).toFixed(0), "% you are avoiding today. A Roth version reverses that bet. Neither is free money; both are timing."));

  // ---- Social Security, in the units people actually think in ----------
  const ssClaim = [
    {age: 62, f: 0.70, note: "permanently reduced 30%"},
    {age: SS_FRA_AGE, f: 1.00, note: "everyone born 1960 or later"},
    {age: 70, f: 1.24, note: "+8% a year of delayed credit"}
  ];
  const ssDetail = !horizonReady ? null : /*#__PURE__*/React.createElement("section", {className: "card ssd"},
    /*#__PURE__*/React.createElement("div", {className: "card-head"},
      /*#__PURE__*/React.createElement("h2", null, "What you would actually receive each month"),
      /*#__PURE__*/React.createElement("p", null, "Claiming age is your choice too — and on these numbers it moves the cheque by more than the structure does.")),
    /*#__PURE__*/React.createElement("div", {className: "table-wrap"},
      /*#__PURE__*/React.createElement("table", {className: "ssd-tbl"},
        /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null,
          /*#__PURE__*/React.createElement("th", null, "If you claim at…"),
          /*#__PURE__*/React.createElement("th", {className: "cA", style: {color: ENT_A.ink}}, ENT_A.short),
          /*#__PURE__*/React.createElement("th", {className: "cB", style: {color: ENT_B.ink}}, ENT_B.short),
          /*#__PURE__*/React.createElement("th", null, "Monthly gap"))),
        /*#__PURE__*/React.createElement("tbody", null, ssClaim.map(c => {
          const a = ssCmp.soleMonthlyPIA * c.f, b = ssCmp.scorpMonthlyPIA * c.f;
          return /*#__PURE__*/React.createElement("tr", {key: c.age, className: c.age === SS_FRA_AGE ? "hi" : ""},
            /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("b", null, c.age),
              c.age === SS_FRA_AGE ? " — full retirement age" : c.age === 62 ? " — earliest possible" : " — latest worth waiting for",
              /*#__PURE__*/React.createElement("span", null, c.note)),
            /*#__PURE__*/React.createElement("td", {className: "cA", style: {background: ENT_A.tint, color: ENT_A.ink}}, fmt0(a)),
            /*#__PURE__*/React.createElement("td", {className: "cB", style: {background: ENT_B.tint, color: ENT_B.ink}}, fmt0(b)),
            /*#__PURE__*/React.createElement("td", {className: "gap"}, b - a === 0 ? "—" : "−" + fmt0(Math.abs(a - b))));
        })))),
    /*#__PURE__*/React.createElement("div", {className: "ssd-ass"},
      /*#__PURE__*/React.createElement("b", null, "What this projection assumes — read before trusting a figure"),
      /*#__PURE__*/React.createElement("ul", null,
        /*#__PURE__*/React.createElement("li", null, "That ", /*#__PURE__*/React.createElement("b", null, "this year's earnings repeat for " + ssCmp.yearsForAIME + " years"), ", until you turn ", SS_FRA_AGE, ". One good year does not produce these numbers."),
        /*#__PURE__*/React.createElement("li", null, "Benefits use your ", /*#__PURE__*/React.createElement("b", null, "highest 35 years"), ". Fewer than 35 working years and SSA fills the gaps with zeros, pulling the average down."),
        /*#__PURE__*/React.createElement("li", null, "Lifetime totals run ", /*#__PURE__*/React.createElement("b", null, SS_FRA_AGE + " to 90"), " — ", ssCmp.lifetimeYears, " years of payments. Live longer and Social Security wins by more; die earlier and it wins by less. That is what an annuity is."),
        /*#__PURE__*/React.createElement("li", null, "Figures are in ", /*#__PURE__*/React.createElement("b", null, "today's dollars"), ", before cost-of-living increases, and use ", /*#__PURE__*/React.createElement("b", null, "2026 bend points"), " — which in reality lock in at age 62, not today."),
        /*#__PURE__*/React.createElement("li", null, "Capped at SSA's published maximum at full retirement age, ", /*#__PURE__*/React.createElement("b", null, "$4,152 a month"), " for 2026. A simplified model built from flat earnings can otherwise exceed what anyone can actually receive."),
        /*#__PURE__*/React.createElement("li", null, "You need ", /*#__PURE__*/React.createElement("b", null, "40 credits"), " — about 10 years of covered work — to qualify at all. A corporation paying you nothing earns none."),
        /*#__PURE__*/React.createElement("li", null, "The only official figure is your own ", extLink("https://www.ssa.gov/myaccount/", "my Social Security"), " statement, which uses your real earnings history. This tool has never seen it."))),
    /*#__PURE__*/React.createElement("div", {className: "ssd-port"},
      /*#__PURE__*/React.createElement("div", {className: "ssd-port-h"},
        /*#__PURE__*/React.createElement("b", null, "Does it follow you abroad?"),
        /*#__PURE__*/React.createElement("span", null, "Relevant because this tool also asks you to compare five other places to live")),
      [["United States", "Paid normally. Medicare available.", "Full", true],
       ["Berlin", "Payments continue. Totalization agreement with Germany — work in both countries can be combined to qualify.", "Paid + treaty", true],
       ["Portugal", "Payments continue. Totalization agreement in force.", "Paid + treaty", true],
       ["Bordeaux", "Payments continue. Totalization agreement with France.", "Paid + treaty", true],
       ["Brisbane", "Payments continue. Totalization agreement with Australia.", "Paid + treaty", true],
       ["UAE", "Payments still reach you as a US citizen — but there is no totalization agreement, so years worked there build no US credit and cannot be combined.", "Paid, no treaty", false],
       ["Cuba · North Korea", "SSA cannot send payments at all. Restrictions also apply in Azerbaijan, Belarus, Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan and Uzbekistan.", "Blocked", false]
      ].map(([pl, ex, st, ok]) => /*#__PURE__*/React.createElement("div", {className: "ssd-row", key: pl},
        /*#__PURE__*/React.createElement("b", null, pl),
        /*#__PURE__*/React.createElement("span", null, ex),
        /*#__PURE__*/React.createElement("i", {className: ok ? "yes" : "no"}, st)))),
    /*#__PURE__*/React.createElement("div", {className: "ssd-med"},
      /*#__PURE__*/React.createElement("b", null, "Medicare does not travel — and this is the one that catches people."),
      "Social Security follows you almost anywhere; Medicare generally covers nothing outside the United States. Retiring abroad means buying local or private cover for the rest of your life, which is a real annual cost rather than a footnote."),
    /*#__PURE__*/React.createElement("p", {className: "pay-note"},
      "Sources: ", extLink("https://www.ssa.gov/pubs/EN-05-10137.pdf", "SSA, Your Payments While You Are Outside the United States"),
      " · ", extLink("https://www.ssa.gov/international/agreement_descriptions.html", "SSA, International Agreements"), "."));

  // =====================================================================
  // THE VERDICT. Everything below this used to be the answer; now it is the
  // working. Computed at a DEFENSIBLE 50% salary rather than whatever the
  // user has set, because that is the honest basis for a recommendation -
  // the election only turns positive at 35-40%, which is the audit-risk band.
  // =====================================================================
  const vSalary = Math.ceil(recNetProfit * 0.5 / 1000) * 1000;
  const vAggr = Math.ceil(recNetProfit * 0.35 / 1000) * 1000;
  const vSole = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "sole_prop", 0);
  const vCorp = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "s_corp", vSalary);
  const vCorpAggr = computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus, numDependents, 0, 0, "s_corp", vAggr);
  const vRun = runCostTotal > 0 ? runCostTotal : 4400;   // Heard's published average
  const vRunIsDefault = !(runCostTotal > 0);
  const vGain = vCorp.net - vSole.net;
  const vNet = vGain - vRun;
  const vNetAggr = (vCorpAggr.net - vSole.net) - vRun;
  const vReady = recNetProfit > 1000;

  // the receipt lines, reconciled to the penny against the engine
  const vPayroll = (vSole.seTax + vSole.ssW2 + vSole.medW2 + vSole.employerPayrollTax)
    - (vCorp.seTax + vCorp.ssW2 + vCorp.medW2 + vCorp.employerPayrollTax);
  const vCaFee = vCorp.caEntityTax - vSole.caEntityTax;
  const vQbiCost = Math.max(0, vSole.qbiDed - vCorp.qbiDed) * Math.max(0.2, strategy.marginalRate);
  const vElse = vGain - (vPayroll - vCaFee - vQbiCost);

  const vVerdict = !vReady ? {t: "Enter your income first", c: "#7C766A",
      d: "Once your rate and caseload are in, this answers the incorporation question before you read anything else."}
    : vNet < -500 ? {t: "Stay a sole proprietor.", c: "#26241E", good: false,
      d: "On a salary you could actually defend, incorporating would leave you worse off."}
    : vNet < 1500 ? {t: "Too close to call — and that is the answer.", c: "#C98B4B", good: false,
      d: "The gain is smaller than the hassle. A payroll run every fortnight and a second tax return every March, for this."}
    : {t: "Worth a conversation with a CPA.", c: "#3F9577", good: true,
      d: "On a defensible salary the election clears its own running costs, which is not true for most practices."};

  const verdictCard = /*#__PURE__*/React.createElement("section", {
    className: "card vcard" + (vVerdict.good ? " vcard-yes" : "")
  }, /*#__PURE__*/React.createElement("div", {className: "vc-k"}, "Our read on your numbers"),
    /*#__PURE__*/React.createElement("h2", {style: {color: vVerdict.c}}, vVerdict.t),
    vReady ? /*#__PURE__*/React.createElement("p", {className: "vc-p"},
      vVerdict.d, " At a salary of ", /*#__PURE__*/React.createElement("b", null, fmt0(vSalary)),
      " — half your ", fmt0(recNetProfit), " profit, the figure most accountants will defend — the election is worth ",
      /*#__PURE__*/React.createElement("b", null, fmt0(vGain)), " in tax and costs about ",
      /*#__PURE__*/React.createElement("b", null, fmt0(vRun)), " a year to run. Net: ",
      /*#__PURE__*/React.createElement("b", {className: vNet > 0 ? "pos" : "neg"},
        (vNet > 0 ? "+" : "−") + fmt0(Math.abs(vNet)) + " a year"), ".")
      : /*#__PURE__*/React.createElement("p", {className: "vc-p"}, vVerdict.d),
    vReady && vNetAggr > vNet + 500 ? /*#__PURE__*/React.createElement("p", {className: "vc-aggr"},
      /*#__PURE__*/React.createElement("b", null, "The number that changes this is not your income — it is your salary. "),
      "Drop it to ", fmt0(vAggr), " (35% of profit) and the election is worth ",
      /*#__PURE__*/React.createElement("b", null, fmt0(vNetAggr)), " a year instead. That is the audit-risk band. The saving is bought with exposure, not with earnings.") : null,
    vRunIsDefault && vReady ? /*#__PURE__*/React.createElement("p", {className: "vc-fine"},
      "Running cost assumed at ", fmt0(4400), " — the average across the therapy practices Heard does the books for. Enter your own accountant's quote further down and this recalculates.") : null);

  const receiptCard = !vReady ? null : /*#__PURE__*/React.createElement("section", {className: "card vrec"},
    /*#__PURE__*/React.createElement("div", {className: "card-head"},
      /*#__PURE__*/React.createElement("h2", null, "Where that number comes from"),
      /*#__PURE__*/React.createElement("p", null, "Four lines, at a ", fmt0(vSalary), " salary. Everything further down this page is the working behind them.")),
    /*#__PURE__*/React.createElement("div", {className: "vrec-b"},
      [["Payroll tax you would avoid", vPayroll, true,
        "Self-employment tax on all your profit, versus payroll tax on the salary only"],
       ["California franchise tax", -vCaFee, false,
        "The greater of $800 or 1.5% of net income — a sole proprietor pays neither"],
       ["Smaller QBI deduction", -vQbiCost, false,
        "Paying yourself a wage shrinks the 20% deduction on what is left. The line most write-ups leave out."],
       ["Payroll service, 1120-S, Form 100S, Statement of Information", -vRun, false,
        vRunIsDefault ? "Heard's published average — replace it with your own quote below" : "Your own figures, entered below"]
      ].map(([lbl, val, good, hint]) => /*#__PURE__*/React.createElement("div", {
        className: "vrec-r" + (val < 0 ? " neg" : ""), key: lbl
      }, /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, lbl),
          /*#__PURE__*/React.createElement("i", null, hint)),
        /*#__PURE__*/React.createElement("b", {className: "v"}, (val >= 0 ? "+" : "−") + fmt0(Math.abs(val))))),
      Math.abs(vElse) > 50 ? /*#__PURE__*/React.createElement("div", {
        className: "vrec-r" + (vElse < 0 ? " neg" : "")
      }, /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, "Everything else"),
          /*#__PURE__*/React.createElement("i", null, "bracket effects and the half-SE-tax deduction, which move in both directions")),
        /*#__PURE__*/React.createElement("b", {className: "v"}, (vElse >= 0 ? "+" : "−") + fmt0(Math.abs(vElse)))) : null,
      /*#__PURE__*/React.createElement("div", {className: "vrec-r tot"},
        /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("b", null, "Net, per year")),
        /*#__PURE__*/React.createElement("b", {className: "v " + (vNet > 0 ? "pos" : "neg")},
          (vNet >= 0 ? "+" : "−") + fmt0(Math.abs(vNet))))),
    /*#__PURE__*/React.createElement("div", {className: "vrec-say"},
      vNet < 0
        ? ["Incorporating would cost you about ", fmt0(Math.abs(vNet) / 12), " a month, plus a payroll run every fortnight and a second tax return every March."]
        : ["That is about ", fmt0(vNet / 12), " a month, in exchange for a payroll run every fortnight and a second tax return every March."]));

  const leverCard = !vReady ? null : (function () {
    const cheap = Math.max(0, vRun - 2500);
    const upTo = Math.max(0, 200000 - recNetProfit);
    const rows = [
      {n: 1, good: vNetAggr > vNet, t: "Pay yourself 35% instead of 50%",
       s: "The only lever that reliably flips the answer — and the one that carries audit risk",
       v: vNetAggr - vNet},
      {n: 2, good: cheap > 0, t: "Find a cheaper accountant",
       s: vRunIsDefault ? "$4,400 is the average; a clean single-shareholder return can be done for about $2,500"
                        : "You have entered " + fmt0(vRun) + "; a clean single-shareholder return can be done for about $2,500",
       v: cheap},
      {n: 3, good: upTo > 0, t: upTo > 0 ? "Earn " + fmt0(upTo) + " more profit" : "You are already past the sweet spot",
       s: upTo > 0
          ? "About " + Math.round(upTo / Math.max(1, sessionRate)) + " more sessions a year, or a rate rise of " + fmt0(upTo / Math.max(1, (cur.grossYr / Math.max(1, sessionRate))))
          : "Past roughly $200,000 the CA franchise tax outgrows the payroll saving",
       v: null},
      {n: 4, good: false, t: "Keep growing well past that",
       s: "Above about $250,000 it gets worse again — California's 1.5% keeps scaling while the payroll saving stops at the " + fmt0(SS_WAGE_BASE_2026) + " wage base",
       v: null}
    ];
    return /*#__PURE__*/React.createElement("section", {className: "card vlev"},
      /*#__PURE__*/React.createElement("div", {className: "card-head"},
        /*#__PURE__*/React.createElement("h2", null, "What would have to change"),
        /*#__PURE__*/React.createElement("p", null, "A verdict that only says no is a dead end. Here is every lever, and what each is actually worth.")),
      rows.map(r => /*#__PURE__*/React.createElement("div", {
        className: "vlev-r" + (r.good ? " good" : " bad"), key: r.n
      }, /*#__PURE__*/React.createElement("i", null, r.n),
        /*#__PURE__*/React.createElement("span", {className: "t"},
          /*#__PURE__*/React.createElement("b", null, r.t),
          /*#__PURE__*/React.createElement("span", null, r.s)),
        r.v != null ? /*#__PURE__*/React.createElement("b", {className: "v"},
          (r.v >= 0 ? "+" : "−") + fmt0(Math.abs(r.v))) : null)),
      /*#__PURE__*/React.createElement("p", {className: "vlev-note"},
        vNetAggr - vNet > Math.max(0, vRun - 2500)
          ? "Notice that changing your salary is worth more than changing anything about your practice. That is worth sitting with — most of what is written about S-corps assumes the saving scales with success, and on these numbers it does not. It scales with how much risk you are willing to carry."
          : "Notice that changing your accountant is worth more than raising your rate. Most of what is written about S-corps assumes the saving scales with success; on these numbers it mostly scales with what you pay in fees."));
  })();

  const workingToggle = !vReady ? null : /*#__PURE__*/React.createElement("div", {className: "vwork"},
    /*#__PURE__*/React.createElement("span", null, "Everything below is the working — the full comparison, the compliance calendar, the retirement plans and the Social Security trade-off. Almost nobody needs it. If you want to check my arithmetic, it is all here."));

  // =====================================================================
  // THE BIGGER LEVER. This runs FIRST in the rendered order, above the
  // structure question, because on almost every set of numbers this tool
  // has been run against it is worth an order of magnitude more - and it
  // needs no filings, no payroll and carries no audit exposure.
  //
  // Every figure here comes from running the engine twice (mfNone / mfWith)
  // rather than multiplying a contribution by a marginal rate. That mistake
  // overstated this block by $12,200 once already; do not reintroduce it.
  // =====================================================================
  const rReady = mfContrib > 0 && recNetProfit > 1000;
  // Honesty guard: the copy below asserts this is the bigger lever. On every
  // set of numbers this tool has been swept across it is, by a wide margin -
  // but assert it from the arithmetic rather than from the assumption.
  const rBigger = mfSaved > vNet;
  // True saving for each alternative account, engine-run rather than rate-multiplied.
  const rRun = (er, emp) => computeYear(scorpGrossBasis, scorpExpBasis, job2Yr, filingStatus,
    numDependents, er, emp, entityType, sCorpSalaryInput);
  const rSepTotal = strategy.sepIra ? strategy.sepIra.total || 0 : 0;
  const rSimpleDef = strategy.simpleIra ? strategy.simpleIra.deferral || 0 : 0;
  const rSimpleMatch = strategy.simpleIra ? strategy.simpleIra.match || 0 : 0;
  const rIraDed = strategy.traditionalIra ? strategy.traditionalIra.deductibleAmount || 0 : 0;
  const rSepSaved = rSepTotal > 0 ? mfTaxNone - rRun(rSepTotal, 0).totalTax : 0;
  const rSimpleSaved = rSimpleDef + rSimpleMatch > 0 ? mfTaxNone - rRun(rSimpleMatch, rSimpleDef).totalTax : 0;
  const rIraSaved = rIraDed > 0 ? mfTaxNone - rRun(0, rIraDed).totalTax : 0;

  const retVerdict = /*#__PURE__*/React.createElement("section", {
    className: "card vcard rcard" + (rReady ? " vcard-yes" : "")
  }, /*#__PURE__*/React.createElement("div", {className: "vc-k"},
      rBigger ? "Your biggest lever" : "The lever with no paperwork"),
    rReady
      ? /*#__PURE__*/React.createElement(React.Fragment, null,
          /*#__PURE__*/React.createElement("h2", {style: {color: "#2F7A61"}},
            fmt0(mfSaved), " of tax, redirected into an account you own."),
          /*#__PURE__*/React.createElement("p", {className: "vc-p"},
            "Nothing about your business has to change. Opening a Solo 401(k) and contributing the full ",
            /*#__PURE__*/React.createElement("b", null, fmt0(mfContrib)),
            " cuts this year's tax from ", /*#__PURE__*/React.createElement("b", null, fmt0(mfTaxNone)),
            " to ", /*#__PURE__*/React.createElement("b", null, fmt0(mfTaxWith)), " — a saving of ",
            /*#__PURE__*/React.createElement("b", {className: "pos"}, fmt0(mfSaved)),
            ", which is ", /*#__PURE__*/React.createElement("b", null, Math.round(mfEffRate * 100) + "%"),
            " of everything you put in. That money was never going to be yours to spend; the only question was whether it went to the IRS or into your own account."),
          /*#__PURE__*/React.createElement("div", {className: "rcomp"},
            /*#__PURE__*/React.createElement("div", {className: "rcomp-r"},
              /*#__PURE__*/React.createElement("span", {className: "l"}, "This lever — fund a Solo 401(k)"),
              /*#__PURE__*/React.createElement("span", {className: "b"},
                /*#__PURE__*/React.createElement("i", {style: {width: "100%", background: "#2F7A61"}})),
              /*#__PURE__*/React.createElement("b", {className: "v pos"}, "+" + fmt0(mfSaved))),
            /*#__PURE__*/React.createElement("div", {className: "rcomp-r"},
              /*#__PURE__*/React.createElement("span", {className: "l"}, "The structure question, below"),
              /*#__PURE__*/React.createElement("span", {className: "b"},
                /*#__PURE__*/React.createElement("i", {style: {
                  width: (Math.min(100, Math.abs(vNet) / Math.max(1, mfSaved) * 100)) + "%",
                  background: vNet > 0 ? "#8AA98F" : "#C99A93"
                }})),
              /*#__PURE__*/React.createElement("b", {className: "v " + (vNet > 0 ? "pos" : "neg")},
                (vNet >= 0 ? "+" : "−") + fmt0(Math.abs(vNet)))),
            /*#__PURE__*/React.createElement("span", {className: "rcomp-n"},
              !rBigger
                ? "On your numbers the structure question is worth more than the retirement one — unusual, and worth opening the full comparison below. This block still comes first because it needs no filings and no payroll."
                : mfSaved > Math.abs(vNet) * 3
                ? "Same profit, same year. This is why the retirement question comes first on this page and the incorporation question comes second."
                : "Both are worth reading, but only one of them needs a payroll service.")),
          /*#__PURE__*/React.createElement("p", {className: "vc-fine"},
            "The cost is liquidity, not money: ", /*#__PURE__*/React.createElement("b", null, fmt0(mfCost)),
            " less lands in your bank account this year, and the balance is locked until 59½ with narrow exceptions. What you ",
            /*#__PURE__*/React.createElement("i", null, "own"), " at the end of the year rises by ",
            /*#__PURE__*/React.createElement("b", null, fmt0(mfSaved)), "."))
      : /*#__PURE__*/React.createElement(React.Fragment, null,
          /*#__PURE__*/React.createElement("h2", {style: {color: "#7C766A"}}, "Enter your income first"),
          /*#__PURE__*/React.createElement("p", {className: "vc-p"},
            "Once your rate and caseload are in, this shows what a retirement account is worth on your numbers — before you read a word about incorporating.")));

  const retReceipt = !rReady ? null : /*#__PURE__*/React.createElement("section", {className: "card vrec rvrec"},
    /*#__PURE__*/React.createElement("div", {className: "card-head"},
      /*#__PURE__*/React.createElement("h2", null, "Where the ", fmt0(mfContrib), " comes from"),
      /*#__PURE__*/React.createElement("p", null, "Two lines. Only one of them is money you would otherwise have spent.")),
    /*#__PURE__*/React.createElement("div", {className: "vrec-b"},
      /*#__PURE__*/React.createElement("div", {className: "vrec-r"},
        /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, "Tax you would have paid anyway"),
          /*#__PURE__*/React.createElement("i", null, "Federal, California and self-employment tax that the contribution removes. Not yours today under either choice — this simply changes who ends up holding it.")),
        /*#__PURE__*/React.createElement("b", {className: "v"}, "+" + fmt0(mfSaved))),
      /*#__PURE__*/React.createElement("div", {className: "vrec-r"},
        /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, "Your own spendable cash, moved across"),
          /*#__PURE__*/React.createElement("i", null, "The real cost. This leaves your bank account and cannot come back until 59½ without a penalty.")),
        /*#__PURE__*/React.createElement("b", {className: "v"}, "+" + fmt0(mfCost))),
      /*#__PURE__*/React.createElement("div", {className: "vrec-r tot"},
        /*#__PURE__*/React.createElement("span", null,
          /*#__PURE__*/React.createElement("b", null, "Into the account")),
        /*#__PURE__*/React.createElement("b", {className: "v pos"}, fmt0(mfContrib)))),
    /*#__PURE__*/React.createElement("div", {className: "vrec-say"},
      "So ", fmt0(mfSaved), " of the ", fmt0(mfContrib), " — ",
      Math.round(mfEffRate * 100), "% of it — is funded by tax you would have paid regardless. You are out of pocket ",
      fmt0(mfCost), " this year and up ", fmt0(mfContrib), " in assets.",
      horizonReady && mfGrown > 0
        ? " Left alone at " + investReturn + "% for the " + mfYears + " years to " + retireAge + ", this one year's contribution is worth " + fmt0(mfGrown) + "."
        : " Fill in your age and retirement age in step 1 below to see what one year of this compounds to."));

  const retLever = !rReady ? null : (function () {
    const opts = [
      {t: "Solo 401(k)", room: mfContrib, saved: mfSaved,
       s: "Employee deferral plus an employer contribution from the same profit. The most room of any plan available to a solo practice."},
      {t: "SEP IRA", room: rSepTotal, saved: rSepSaved,
       s: strategy.sepIra ? strategy.sepIra.pctLabel + ". Employer-funded only — no deferral, and no catch-up at any age." : ""},
      {t: "SIMPLE IRA", room: rSimpleDef + rSimpleMatch, saved: rSimpleSaved,
       s: "Deferral plus a mandatory 3% employer match. Cannot be run in the same year as a Solo 401(k)."},
      {t: "Traditional IRA", room: rIraDed, saved: rIraSaved,
       s: rIraDed > 0 ? "Deductible portion at your income. Small, but it stacks on top of an employer plan."
                      : "Fully phased out at your income — the contribution is allowed, the deduction is not."}
    ].sort((a, b) => b.room - a.room);
    const top = opts[0].room || 1;
    return /*#__PURE__*/React.createElement("section", {className: "card vlev rlev"},
      /*#__PURE__*/React.createElement("div", {className: "card-head"},
        /*#__PURE__*/React.createElement("h2", null, "How much room each account gives you"),
        /*#__PURE__*/React.createElement("p", null,
          "Your own profit, run through all four. These are alternatives, not a shopping list — the tax saved is what the engine actually computes, not a contribution multiplied by a rate.")),
      opts.map((o, i) => /*#__PURE__*/React.createElement("div", {
        className: "rlev-r" + (i === 0 ? " best" : ""), key: o.t
      }, /*#__PURE__*/React.createElement("i", null, i + 1),
        /*#__PURE__*/React.createElement("span", {className: "t"},
          /*#__PURE__*/React.createElement("b", null, o.t, i === 0 ? /*#__PURE__*/React.createElement("em", null, "most room") : null),
          /*#__PURE__*/React.createElement("span", null, o.s)),
        /*#__PURE__*/React.createElement("span", {className: "bar"},
          /*#__PURE__*/React.createElement("i", {style: {width: (o.room / top * 100) + "%"}})),
        /*#__PURE__*/React.createElement("b", {className: "v"}, fmt0(o.room),
          /*#__PURE__*/React.createElement("em", null, o.saved > 0 ? fmt0(o.saved) + " tax saved" : "no deduction")))),
      /*#__PURE__*/React.createElement("p", {className: "vlev-note"},
        taxAge >= 50
          ? "Your catch-up contributions are already included above" + (taxAge >= 60 && taxAge <= 63 ? " — you are in the 60–63 band, which is the highest one there is." : ".")
          : "Catch-up contributions start at 50 and step up again for ages 60–63, so this ceiling rises twice more before you retire."));
  })();

  const retWorking = !rReady ? null : /*#__PURE__*/React.createElement("div", {className: "vwork"},
    /*#__PURE__*/React.createElement("span", null, rBigger
      ? "The second decision — whether to incorporate — is below. On these numbers it is worth far less, so it is folded away; open it if you want the full comparison."
      : "The second decision — whether to incorporate — is below, and on your numbers it is the larger of the two. It is opened for you."));

  // The structure question, folded to one line. It used to open the section;
  // it now sits under the retirement block because on virtually every set of
  // numbers this tool has been run against it is worth an order of magnitude
  // less. The full verdict, receipt and levers are all still here, unchanged.
  const scorpAutoOpen = vReady && (vNet > 1500 || !rBigger);
  const scorpFold = /*#__PURE__*/React.createElement("details", {
    className: "card collapsible vfold",
    ref: el => { if (el && !el.dataset.autoinit) { el.dataset.autoinit = "1"; el.open = scorpAutoOpen; } }},
    /*#__PURE__*/React.createElement("summary", {className: "vfold-s"},
      /*#__PURE__*/React.createElement("span", {className: "vfold-k"}, "The second decision"),
      /*#__PURE__*/React.createElement("span", {className: "vfold-q"}, "Should you incorporate?"),
      /*#__PURE__*/React.createElement("b", {className: "vfold-a", style: {color: vVerdict.c}}, vVerdict.t),
      vReady ? /*#__PURE__*/React.createElement("span", {className: "vfold-v"},
        /*#__PURE__*/React.createElement("b", {className: vNet > 0 ? "pos" : "neg"},
          (vNet >= 0 ? "+" : "−") + fmt0(Math.abs(vNet))),
        /*#__PURE__*/React.createElement("i", null, "a year, at a salary you could defend")) : null,
      /*#__PURE__*/React.createElement("span", {className: "vfold-o"},
        /*#__PURE__*/React.createElement("em", {className: "o"}, "Open the full comparison"),
        /*#__PURE__*/React.createElement("em", {className: "c"}, "Close"))),
    verdictCard, receiptCard, leverCard);

  const step1Done = true;
  const returnPresets = /*#__PURE__*/React.createElement("div", {className: "retpresets"},
    /*#__PURE__*/React.createElement("span", {className: "retpresets-lab"}, "Expected return — pick a starting point:"),
    [{v: 11, t: "11% — S&P 500, 20yr to 2025", s: "what the market actually did"},
     {v: 8.3, t: "8.3% — same, after inflation", s: "what it bought"},
     {v: 5.9, t: "5.9% — Schwab 10yr forecast", s: "what the houses expect next"}
    ].map(o => /*#__PURE__*/React.createElement("button", {
      key: o.v, type: "button",
      className: "retchip" + (Math.abs(investReturn - o.v) < 0.05 ? " on" : ""),
      onClick: () => setInvestReturn(o.v)
    }, /*#__PURE__*/React.createElement("b", null, o.t), /*#__PURE__*/React.createElement("span", null, o.s))),
    /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
      "The last 20 years returned 11% a year. Looking forward, Schwab publishes 5.9% for US large-cap over 2026–35, and Vanguard 4.2–6.2% as of 30 June 2026. The gap matters: over 25 years, 11% against 5.9% is roughly 3.4× the final pot. Projecting decades at 11% is the optimistic case, not the expected one — which is why this is yours to set, and why the verdict further down can flip."));
  const step1Lock = /*#__PURE__*/React.createElement("section", {className: "card steplock"},
    /*#__PURE__*/React.createElement("div", {className: "steplock-n"}, "2"),
    /*#__PURE__*/React.createElement("div", null,
      /*#__PURE__*/React.createElement("h2", null, "Sole Proprietorship vs Professional Corp"),
      /*#__PURE__*/React.createElement("p", null,
        "Locked until Step 1 is filled in. Everything in this comparison — the retirement projections, the Social Security estimate, the invest-the-difference maths — depends on your age, when you plan to retire, and what return you assume. Without them the figures would be invented."),
      /*#__PURE__*/React.createElement("div", {className: "steplock-need"},
        [["Your current age", taxAge > 0], ["Planned retirement age", retireAge > 0], ["Expected annual return", investReturn > 0]]
          .map(([lbl, ok]) => /*#__PURE__*/React.createElement("span", {
            key: lbl, className: "steplock-item" + (ok ? " ok" : "")
          }, ok ? "✓ " : "○ ", lbl))),
      /*#__PURE__*/React.createElement("p", {className: "salguide-fine"}, "Fill those in just above and this section opens.")));
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
  }, "As a ", entTag(ENT_A, {sm: true}), " there is ", /*#__PURE__*/React.createElement("b", null, "no salary to set"), " — you cannot employ yourself, so ", /*#__PURE__*/React.createElement("b", null, "every dollar of profit"), " is self-employment income and self-employment tax applies to all of it: 12.4% for Social Security up to ", fmt0(SS_WAGE_BASE_2026), " of earnings, then 2.9% for Medicare on everything above. Nothing to decide, and nothing to defend. A ", entTag(ENT_B, {sm: true}), " is the only structure that creates a choice, because a corporation ", /*#__PURE__*/React.createElement("b", null, "can"), " employ you: it pays part of the profit as a ", /*#__PURE__*/React.createElement("b", null, "W-2 salary"), " (payroll tax applies, exactly as before) and the rest as a ", /*#__PURE__*/React.createElement("b", null, "distribution"), " (no payroll tax). That split is the whole reason this choice exists."), /*#__PURE__*/React.createElement("p", {
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
  // The IRS test is what the work is worth, not a share of profit. Watson was
  // decided on comparable professional wages. So anchor to published wage data
  // and show BOTH tests, because they disagree in opposite directions at the
  // two ends of the income range.
  const myMetro = MFT_WAGES[Math.min(Math.max(0, wageMetro | 0), MFT_WAGES.length - 1)];
  const wageMax = Math.max(MFT_NAT_P90, CENSUS_SCORP_PAYROLL, sCorpSalaryInput, 1);
  const wageRatio = myMetro.v > 0 ? sCorpSalaryInput / myMetro.v : 0;
  const wageVerdict = sCorpSalaryInput <= 0 ? null
    : sCorpSalaryInput >= MFT_NAT_P90 ? {t: "Above the national 90th percentile", c: "#3F9577",
        d: "Higher than nine in ten employed MFTs anywhere in the country, and " + Math.round(wageRatio * 100) + "% of the " + myMetro.p + " mean. On a wage-comparability argument this is about as strong as it gets."}
    : sCorpSalaryInput >= myMetro.v ? {t: "Above the " + myMetro.p + " mean", c: "#3F9577",
        d: "You are paying yourself " + Math.round(wageRatio * 100) + "% of what an employed MFT earns on average where you practise. A strong position to defend."}
    : sCorpSalaryInput >= myMetro.v * 0.8 ? {t: "Close to the " + myMetro.p + " mean", c: "#C98B4B",
        d: Math.round(wageRatio * 100) + "% of the local mean. Arguable, but document your hours and the roles you perform \u2014 the gap is what an examiner would ask about."}
    : {t: "Well below the " + myMetro.p + " mean", c: "#B5483F",
        d: "Only " + Math.round(wageRatio * 100) + "% of what an employed MFT earns where you practise. Hard to argue a practice generating " + fmt0(recNetProfit) + " of profit is worth less than a salaried post."};
  const pctOfProfitNow = recNetProfit > 0 ? sCorpSalaryInput / recNetProfit : 0;
  const wageAnchor = /*#__PURE__*/React.createElement("div", {className: "wagea"},
    /*#__PURE__*/React.createElement("h4", null, "What the work is actually worth"),
    /*#__PURE__*/React.createElement("p", {className: "salguide-lede"},
      "The bands above use a percentage of profit, because that is how the internet talks about this. It is not the test. The IRS asks what your services are worth, and in ",
      /*#__PURE__*/React.createElement("i", null, "Watson"),
      " the court accepted a figure built from comparable professional wages — not a share of profit. Published wage data for your licence is free, and it is the stronger argument."),
    /*#__PURE__*/React.createElement("div", {className: "metropick"},
      /*#__PURE__*/React.createElement("span", {className: "metropick-lab"}, "Where you practise"),
      /*#__PURE__*/React.createElement("select", {
        value: wageMetro, onChange: e => setWageMetro(+e.target.value)
      }, MFT_WAGES.map((w, i) => /*#__PURE__*/React.createElement("option", {key: w.p, value: i},
        w.p + " \u2014 " + fmt0(w.v)))),
      /*#__PURE__*/React.createElement("span", {className: "metropick-note"},
        "Sets which figure your salary is judged against. All eight stay visible below.")),
    /*#__PURE__*/React.createElement("div", {className: "wagebars"},
      MFT_WAGES.map((w, i) => /*#__PURE__*/React.createElement("div", {className: "wrow" + (w.state ? " st" : "") + (i === (wageMetro | 0) ? " mine" : ""), key: w.p},
        /*#__PURE__*/React.createElement("span", {className: "nm"}, w.p, i === (wageMetro | 0) ? /*#__PURE__*/React.createElement("em", null, "yours") : null),
        /*#__PURE__*/React.createElement("span", {className: "tr"},
          /*#__PURE__*/React.createElement("i", {style: {width: (w.v / wageMax * 100) + "%", background: i === (wageMetro | 0) ? "#3B5A7A" : "#A9BFD3"}})),
        /*#__PURE__*/React.createElement("span", {className: "vl"}, fmt0(w.v)))),
      /*#__PURE__*/React.createElement("div", {className: "wrow", key: "p90"},
        /*#__PURE__*/React.createElement("span", {className: "nm"}, "National 90th percentile"),
        /*#__PURE__*/React.createElement("span", {className: "tr"},
          /*#__PURE__*/React.createElement("i", {style: {width: (MFT_NAT_P90 / wageMax * 100) + "%", background: "#B9CBE0"}})),
        /*#__PURE__*/React.createElement("span", {className: "vl"}, fmt0(MFT_NAT_P90))),
      /*#__PURE__*/React.createElement("div", {className: "wrow peer", key: "census"},
        /*#__PURE__*/React.createElement("span", {className: "nm"}, "CA therapy S-corps \u2014 actual payroll",
          /*#__PURE__*/React.createElement("em", null, "census")),
        /*#__PURE__*/React.createElement("span", {className: "tr"},
          /*#__PURE__*/React.createElement("i", {style: {width: (CENSUS_SCORP_PAYROLL / wageMax * 100) + "%", background: "#8AA98F"}})),
        /*#__PURE__*/React.createElement("span", {className: "vl"}, fmt0(CENSUS_SCORP_PAYROLL))),
      sCorpSalaryInput > 0 ? /*#__PURE__*/React.createElement("div", {className: "wrow you", key: "you"},
        /*#__PURE__*/React.createElement("span", {className: "nm"}, "Your salary"),
        /*#__PURE__*/React.createElement("span", {className: "tr"},
          /*#__PURE__*/React.createElement("i", {style: {width: (sCorpSalaryInput / wageMax * 100) + "%", background: ENT_B.ink}})),
        /*#__PURE__*/React.createElement("span", {className: "vl", style: {color: ENT_B.ink}}, fmt0(sCorpSalaryInput))) : null),
    /*#__PURE__*/React.createElement("div", {className: "wagetests"},
      /*#__PURE__*/React.createElement("div", {className: "wt", style: {borderColor: wageVerdict ? wageVerdict.c : "#E7E2D6"}},
        /*#__PURE__*/React.createElement("span", {className: "l"}, "The wage test — what the IRS actually asks"),
        /*#__PURE__*/React.createElement("b", {style: {color: wageVerdict ? wageVerdict.c : "inherit"}},
          wageVerdict ? wageVerdict.t : "Set a salary to see this"),
        /*#__PURE__*/React.createElement("span", {className: "n"},
          wageVerdict ? wageVerdict.d : "Your salary is compared against published wages for employed MFTs in California.")),
      /*#__PURE__*/React.createElement("div", {className: "wt"},
        /*#__PURE__*/React.createElement("span", {className: "l"}, "The peer test — what CA therapy S-corps actually pay"),
        /*#__PURE__*/React.createElement("b", null, fmt0(CENSUS_SCORP_PAYROLL)),
        /*#__PURE__*/React.createElement("span", {className: "n"},
          "Average annual payroll per California therapy S-corp with one to four employees — ",
          CENSUS_SCORP_ESTABS.toLocaleString(), " of them, straight from federal tax filings. ",
          sCorpSalaryInput > 0
            ? /*#__PURE__*/React.createElement("b", null, "Yours is " +
                Math.round(sCorpSalaryInput / CENSUS_SCORP_PAYROLL * 100) + "% of that.")
            : "Set a salary to see how yours compares.")),
      /*#__PURE__*/React.createElement("div", {className: "wt"},
        /*#__PURE__*/React.createElement("span", {className: "l"}, "The percentage convention — what blogs repeat"),
        /*#__PURE__*/React.createElement("b", null, fmt0(recNetProfit * 0.35), " – ", fmt0(recNetProfit * 0.5)),
        /*#__PURE__*/React.createElement("span", {className: "n"},
          "35% to 50% of your ", fmt0(recNetProfit), " profit. Yours is ",
          /*#__PURE__*/React.createElement("b", null, Math.floor(pctOfProfitNow * 100) + "%"),
          recNetProfit * 0.5 > MFT_WAGES[0].v
            ? ". Note the 50% convention here asks for more than any California employer pays an MFT."
            : "."))),
    /*#__PURE__*/React.createElement("div", {className: "wagenote"},
      /*#__PURE__*/React.createElement("b", null, "Why this matters more as you earn more. "),
      "A percentage scales with profit; a wage does not. At $100,000 of profit, 50% is $50,000 — below the California mean, so the percentage is the lenient test. At $400,000 of profit, 50% is $200,000 — roughly double any published clinician wage, so the percentage becomes the punitive one. Both tests are shown because they disagree, and which one you fail changes the conversation."),
    /*#__PURE__*/React.createElement("div", {className: "wagenote counter"},
      /*#__PURE__*/React.createElement("b", null, "The honest counter-argument. "),
      "You are not only a clinician — you also run the practice, and the IRS values every role you perform, not just the clinical hours. A defensible file usually adds a management component on top of the clinical wage. It also matters that you generate this revenue yourself; an employed MFT on ",
      fmt0(MFT_WAGES[0].v), " is not carrying a practice. Treat the wage figure as the floor of the argument, not the answer."),
    /*#__PURE__*/React.createElement("div", {className: "wagenote peer"},
      /*#__PURE__*/React.createElement("b", null, "The peer figure, and what it is not. "),
      "The ", fmt0(CENSUS_SCORP_PAYROLL), " row is not a published salary recommendation — it is total payroll divided by establishments, taken from federal tax filings for the ",
      CENSUS_SCORP_ESTABS.toLocaleString(), " California therapy S-corps with one to four employees. Two things pull it around: employment is counted at a single point in time (12 March) while payroll is counted for the whole year, so part-year staff drag the ",
      fmt0(CENSUS_SCORP_PER_EMP), "-per-employee figure down; and payroll covers ",
      /*#__PURE__*/React.createElement("i", null, "everyone"),
      " on the books, not just the owner-shareholder, so a practice with an admin on staff splits that total. Read it as evidence of what your peers actually run through payroll — not as a target, and not as a safe harbour."),
    /*#__PURE__*/React.createElement("p", {className: "salguide-fine"},
      extLink("https://www.bls.gov/oes/2023/may/oes211013.htm",
        "BLS Occupational Employment and Wage Statistics — Marriage and Family Therapists, May 2023"),
      ". Annual mean wages for employed MFTs; self-employed practitioners are excluded, which is the comparison the reasonable-compensation test calls for. · ",
      extLink("https://www.census.gov/programs-surveys/cbp.html",
        "US Census Bureau, County Business Patterns 2023"),
      " — California, NAICS 621330, S-corporation establishments with 1–4 employees: ",
      CENSUS_SCORP_ESTABS.toLocaleString(), " establishments, 4,963 employees, $294,021,000 of annual payroll."));

  const businessStructureSection = /*#__PURE__*/React.createElement("section", {
    className: "card decision-impact"
  }, /*#__PURE__*/React.createElement("div", {
    className: "card-head"
  }, /*#__PURE__*/React.createElement("h2", null, "Business structure"), /*#__PURE__*/React.createElement("p", null, "Sole Proprietorship vs. Professional Corp with an S-corp election \u2014 this choice is global and changes the tax math on every tab.")), educationBlock, entityToggle, salaryInputRow, salaryGuidance, wageAnchor, payrollMechanic, complianceGuide, /*#__PURE__*/React.createElement("div", {
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
  }, /*#__PURE__*/React.createElement("li", null, "Training, experience, and licensure"), /*#__PURE__*/React.createElement("li", null, "Duties and responsibilities actually performed"), /*#__PURE__*/React.createElement("li", null, "Time and effort devoted to the practice (full-time vs. part-time)"), /*#__PURE__*/React.createElement("li", null, "What comparable businesses pay for similar clinical work"), /*#__PURE__*/React.createElement("li", null, "Dividend/distribution history \u2014 a pattern of high distributions and minimal salary is a specific red flag"), /*#__PURE__*/React.createElement("li", null, "What you pay any non-owner employees for similar work")), /*#__PURE__*/React.createElement("p", null, "Getting this wrong is a real, citable audit risk, not a theoretical one: in ", /*#__PURE__*/React.createElement("a", {href: "https://ecf.ca8.uscourts.gov/opndir/12/02/111589P.pdf", target: "_blank", rel: "noopener noreferrer", className: "extlink"}, /*#__PURE__*/React.createElement("i", null, "David E. Watson, P.C. v. United States")), ", a CPA who paid himself a $24,000 salary against $203,651 in distributions had his compensation reclassified upward to $91,044 by the Eighth Circuit; in ", /*#__PURE__*/React.createElement("i", null, "Nu-Look Design, Inc. v. Commissioner"), ", 356 F.3d 290 (3d Cir. 2004), a sole shareholder-officer taking $0 salary lost the same argument.", /*#__PURE__*/React.createElement("sup", null, "[5]"), " When the IRS reclassifies a distribution as wages, it comes with back payroll taxes, penalties, and interest \u2014 without any offsetting new deduction to soften it.", /*#__PURE__*/React.createElement("sup", null, "[6]")), /*#__PURE__*/React.createElement("p", {
    className: "pay-note"
  }, citeList([
    {n:1, cite:"IRC \u00A71373", url:"https://www.law.cornell.edu/uscode/text/26/1373", note:"Rev. Rul. 59-221, 1959-1 C.B. 225 \u2014 S-corp flow-through profit distributed as such is not subject to self-employment tax; compensation for services is."},
    {n:2, cite:"IRC \u00A7199A(c)(4)", url:"https://www.law.cornell.edu/uscode/text/26/199A", note:"excludes reasonable compensation from qualified business income."},
    {n:3, cite:"Treas. Reg. \u00A731.3121(d)-1(b)", url:"https://www.law.cornell.edu/cfr/text/26/31.3121(d)-1", note:"treats more-than-minor services for remuneration as employment; see also IRS Fact Sheet FS-2008-25, \u201CWage Compensation for S Corporation Officers.\u201D"},
    {n:4, cite:"IRS \u2014 S corporation employees, shareholders and corporate officers", url:"https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-employees-shareholders-and-corporate-officers", note:"the IRS\u0027s current live guidance on officer compensation, which supersedes the 2008 fact sheet as the primary statement of its position."},
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
  }, "Figures use projected 2026 IRS contribution limits and income phase-out ranges, and a simplified compounding model (same contribution repeated every year at a flat return, no fees or taxes on withdrawal modeled). Solo 401(k) employer contributions assume a sole proprietorship (20% of net self-employment earnings); an S-corp election changes this calculation to 25% of W-2 wages instead. This isn't personalized investment or tax advice \u2014 a CPA or fee-only fiduciary advisor can confirm what's actually deductible and suitable for you."));

  return /*#__PURE__*/React.createElement(React.Fragment, null, keepOpener, retVerdict, retReceipt, retLever, retWorking, scorpFold, workingToggle, secOpener, stepperRail, introSection, returnPresets, taxProfileSection,
    mobileFold("bs", "Business structure", isSole ? "Sole Proprietorship \u00b7 tap to change" : "Professional Corp \u00b7 tap to change", businessStructureSection),
    mobileFold("cmp", "Both structures, side by side", horizonReady ? "all 28 rows" : "21 rows now, 9 more after step 1", entityCompareSection),
    ssDetail ? mobileFold("ssd", "Social Security, in full", "monthly at 62, 67 and 70 \u00b7 what travels abroad", ssDetail) : null,
    moneyFlow, expertSection, leversPanel, step1Done && /*#__PURE__*/React.createElement("details", {className: "card collapsible taxdetail"}, /*#__PURE__*/React.createElement("summary", {className: "card-head"}, /*#__PURE__*/React.createElement("h2", null, "The same numbers, broken out"), /*#__PURE__*/React.createElement("p", null, "Headline stats, each retirement account on its own, and the single-structure view. Everything here also appears in the table above — open it if you want a figure isolated rather than compared.")), statsRow, strategiesSection, compareSection), step1Done && /*#__PURE__*/React.createElement("details", {className: "card collapsible taxdetail"}, /*#__PURE__*/React.createElement("summary", {className: "card-head"}, /*#__PURE__*/React.createElement("h2", null, "How the rules actually work"), /*#__PURE__*/React.createElement("p", null, "Self-employment tax mechanics, the S-corp election and audit risk, choosing a structure in California, and the Social Security trade-off in full. Reference material \u2014 read it once, then ignore it.")), seEducation, scorpSection, caSection, analysisSection));
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
  weeksWorked,
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
  const perSession = sessions > 0 ? expYr / (sessions * weeksWorked) : 0;
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
  weeksWorked,
  cur,
  color,
  rate,
  sessions,
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
  const profitBySessions = sessionsList.map(s => {
    const g = rate * s * weeksWorked;
    const fee = cityLicenseFee(cityKey, g, manualCityFee);
    return {
      s,
      profit: Math.round(computeYear(g, expYrBase + fee, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput).net)
    };
  });
  const breakEven = (() => {
    for (let s = 1; s <= 60; s++) {
      const g = rate * s * weeksWorked;
      const fee = cityLicenseFee(cityKey, g, manualCityFee);
      if (computeYear(g, expYrBase + fee, job2Yr, filingStatus, numDependents, 0, 0, entityType, sCorpSalaryInput).net > 0) return s;
    }
    return null;
  })();
  const fmtH = n => (n < 0 ? "\u2212$" : "$") + Math.abs(Math.round(n)).toLocaleString();
  const retirePointer = !(taxStrategy && hypoBaseline && hypoSolo401k) ? null : (function () {
    const saved = Math.round(hypoBaseline.totalTax - hypoSolo401k.totalTax);
    const room = Math.round(taxStrategy.solo401k.total);
    if (!(saved > 0 && room > 0)) return null;
    return /*#__PURE__*/React.createElement("div", {className: "sec-point"},
      /*#__PURE__*/React.createElement("b", null, fmtH(saved), " of that tax is optional."),
      " A Solo 401(k) has room for ", /*#__PURE__*/React.createElement("b", null, fmtH(room)),
      " of your profit this year, and roughly ",
      /*#__PURE__*/React.createElement("b", null, Math.round(saved / room * 100) + "%"),
      " of that contribution is funded by tax you would have paid anyway. The full receipt \u2014 and what it costs you in spendable cash \u2014 opens the ",
      /*#__PURE__*/React.createElement("a", {href: "#sec-taxstrategy"}, "Tax strategy"), " section below.");
  })();
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("section", {
    className: "stats"
  }, /*#__PURE__*/React.createElement(Stat, {
    big: true,
    label: "Net profit / year",
    value: fmt(cur.netYr),
    accent: color,
    note: `after ${fmt(cur.expYr)} expenses and ${fmt(Math.round(cur.totalTax))} tax`
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
    className: "one-up"
  }, /*#__PURE__*/React.createElement("div", {
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
  }, fmt(sessions > 0 ? cur.netYr / (sessions * weeksWorked) : 0)), /*#__PURE__*/React.createElement("span", {
    className: "strip-sub"
  }, "of your $", rate, " billed rate")))), retirePointer);
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

.keepwrap-empty{text-align:center; padding:30px 24px;}
.keepwrap-empty p{max-width:520px; margin:10px auto 16px; color:#5C574C; font-size:14.5px; line-height:1.65;}
.keep-cta{display:inline-block; background:#3F9577; color:#fff; text-decoration:none; font-size:13.5px; font-weight:600; padding:9px 18px; border-radius:8px;}
.keep-cta:hover{background:#357F65;}
.levers-empty .card-head p{color:#7C766A;}

/* ===== step 1 gate ===== */
.retpresets{border:1px solid #E7E2D6; border-radius:12px; background:#fff; padding:16px 18px; margin:0 0 16px;}
.retpresets-lab{display:block; font-size:11px; letter-spacing:.07em; text-transform:uppercase; color:#7C766A; font-weight:600; margin-bottom:10px;}
.retchip{display:inline-block; text-align:left; border:1px solid #E7E2D6; background:#fff; border-radius:9px; padding:9px 13px; margin:0 8px 8px 0; cursor:pointer; font-family:Inter,sans-serif; color:#26241E;}
.retchip b{display:block; font-size:13.5px;}
.retchip span{display:block; font-size:12px; color:#7C766A;}
.retchip:hover{border-color:#C98B4B;}
.retchip.on{border:2px solid #3F9577; background:#F7FBF9;}
.retchip.on span{color:#2C6B53;}
.steplock{display:flex; gap:16px; align-items:flex-start;
  background:repeating-linear-gradient(45deg,#FCFAF4,#FCFAF4 12px,#F7F3EA 12px,#F7F3EA 24px);
  border:1px dashed #D9D1BE;}
.steplock-n{flex:0 0 34px; height:34px; border-radius:50%; background:#F6F2E8; border:1px solid #E7E2D6;
  display:flex; align-items:center; justify-content:center; font-family:Fraunces,Georgia,serif; font-weight:600;}
.steplock h2{font-family:Fraunces,Georgia,serif; font-size:20px; margin:2px 0 8px;}
.steplock p{margin:0 0 12px; color:#5C574C; font-size:14px; line-height:1.6; max-width:640px;}
.steplock-need{display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px;}
.steplock-item{font-size:13px; padding:6px 12px; border-radius:20px; border:1px solid #E7E2D6; background:#fff; color:#7C766A;}
.steplock-item.ok{border-color:#3F9577; color:#2C6B53; background:#EAF3EE; font-weight:600;}

/* ===== levers ===== */
.levers .lever{display:flex; align-items:center; gap:14px; padding:11px 0; border-bottom:1px solid #F1EDE3; flex-wrap:wrap;}
.levers .lever:last-of-type{border-bottom:0;}
.lever-name{flex:1 1 240px; min-width:200px; font-size:14px;}
.lever-name b{display:block;}
.lever-name span{display:block; font-size:12.5px; color:#7C766A;}
.lever-bar{flex:2 1 180px; height:12px; background:#F1EDE3; border-radius:6px; overflow:hidden; min-width:120px;}
.lever-bar i{display:block; height:100%; border-radius:6px;}
.lever-val{flex:0 0 96px; text-align:right; font-family:Fraunces,Georgia,serif; font-weight:600; font-variant-numeric:tabular-nums;}
.lever-note{background:#FBF1E2; border-left:3px solid #C98B4B; border-radius:0 8px 8px 0; padding:12px 14px; font-size:13.5px; line-height:1.65; margin:16px 0 8px;}
@media (max-width:640px){ .lever-bar{flex:1 1 100%; order:3;} .lever-val{flex:0 0 auto;} }

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

/* =========================================================================
   THE SOLE PROP vs PROFESSIONAL CORP COMPARISON
   Two column identities, used identically everywhere in the Tax Strategy
   section. Blue = Sole Proprietorship. Plum = Professional Corp.
   Green and red are reserved exclusively for better/worse verdicts, so a
   column colour can never be mistaken for a judgement about that column.
   ========================================================================= */

.statpend{background:#FCFAF4 !important; border-style:dashed !important;}
.statpend .stat-value{color:var(--muted) !important; font-style:italic;}
.statpend .stat-note{line-height:1.5;}

/* named-source commentary */
.expert-q{border-top:1px solid var(--line); padding:16px 0 4px;}
.expert-q:first-of-type{border-top:none;}
.expert-who{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:7px;}
.expert-who b{font-family:'Fraunces',serif; font-size:16px;}
.expert-who span{font-size:11.5px; color:var(--muted);}
.expert-q p{font-size:14px; line-height:1.65; margin:0 0 10px;}
.expert-q i{color:var(--ink);}
.expert-caveat{background:#FBF1E2; border-left:4px solid #C98B4B; border-radius:0 8px 8px 0;
  padding:11px 14px; font-size:13.5px; line-height:1.6; margin:0 0 10px;}
.expert-yours{background:#FCFAF4; border:1px dashed var(--line); border-radius:8px;
  padding:10px 13px; font-size:13.5px; line-height:1.6; margin:0 0 10px;}
.expert-nodata{background:#F6F2E8; border-radius:12px; padding:16px 18px; margin-top:16px;}
.expert-nodata h4{font-family:'Fraunces',serif; font-size:16px; margin:0 0 9px;}
.expert-nodata p{font-size:13.5px; line-height:1.65; margin:0 0 10px;}
.expert-nodata p:last-of-type{margin-bottom:0;}
.cendual{display:flex; flex-direction:column; gap:14px; margin:14px 0 16px;}
.cenrow{background:#FFFDF8; border:1px solid #E7E2D6; border-radius:10px; padding:11px 13px 10px;}
.cenrow.you{border-color:#C98B4B; box-shadow:0 0 0 2px rgba(201,139,75,.13);}
.cenhead{display:flex; align-items:baseline; flex-wrap:wrap; gap:8px; margin:0 0 8px;}
.cenhead b{font-size:13.5px;}
.cenhead span{font-size:11.5px; color:#8A8375; font-variant-numeric:tabular-nums;}
.cenhead em{font-style:normal; font-size:10.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:#8A5B24; background:#F7EBDA; border-radius:99px; padding:2px 8px; margin-left:auto;}
.cenbar{display:flex; height:26px; border-radius:6px; overflow:hidden;}
.cenbar i{display:flex; align-items:center; justify-content:center; min-width:0;}
.cenbar i span{font-size:11.5px; font-weight:700; color:#fff; white-space:nowrap; overflow:hidden; text-shadow:0 1px 1px rgba(0,0,0,.18);}
.cenkey{display:flex; flex-wrap:wrap; gap:4px 15px; margin-top:7px;}
.cenkey span{display:flex; align-items:center; gap:5px; font-size:11.5px; color:#5F594E;}
.cenkey span i{width:9px; height:9px; border-radius:2px; flex:none;}
.cenflag{display:flex; align-items:flex-start; gap:13px; background:#FBF1EE; border-left:4px solid #B5483F; border-radius:0 8px 8px 0; padding:12px 14px; margin:0 0 12px;}
.cenflag>b{font-family:'Fraunces',serif; font-size:24px; line-height:1; color:#B5483F; flex:none; font-variant-numeric:tabular-nums;}
.cenflag>span{font-size:13px; line-height:1.6;}
@media (max-width:560px){
  .cenbar i span{font-size:10.5px;}
  .cenhead em{margin-left:0;}
}

/* the salary / distribution split, as one draggable control */
.salsplit{border:2px solid; border-radius:14px; padding:15px 17px 14px; margin:14px 0 18px;}
.salsplit-head{display:flex; justify-content:space-between; align-items:baseline; gap:14px;
  flex-wrap:wrap; margin-bottom:12px;}
.salsplit-title{display:inline-flex; align-items:center; gap:8px; font-family:'Fraunces',serif;
  font-weight:700; font-size:15.5px;}
.salsplit-note{font-size:11.5px; color:var(--muted); line-height:1.4;}
.salsplit-bar{display:flex; height:36px; border-radius:9px; overflow:hidden; border:1px solid #D4C3DD;}
.salsplit-bar i{display:flex; align-items:center; justify-content:center; font-style:normal;
  transition:width .12s ease; min-width:0;}
.salsplit-w2 span{color:#fff; font-size:10.5px; font-weight:800; letter-spacing:.05em; white-space:nowrap;}
.salsplit-dist{background:repeating-linear-gradient(135deg,#EDE1F3 0 7px,#E3D3EC 7px 14px);}
.salsplit-dist span{color:#6A4A78; font-size:10.5px; font-weight:800; letter-spacing:.05em; white-space:nowrap;}
.salsplit-range{width:100%; margin:11px 0 3px; accent-color:#6A4A78; cursor:pointer;}
.salsplit-ends{display:flex; justify-content:space-between; gap:18px; font-size:11px;
  color:var(--muted); line-height:1.4;}
.salsplit-ends span{display:flex; flex-direction:column; max-width:47%;}
.salsplit-ends span.r{text-align:right; align-items:flex-end;}
.salsplit-ends b{color:#6A4A78; font-size:11.5px; margin-bottom:1px;}
.salsplit-foot{display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-top:13px;
  padding-top:12px; border-top:1px solid #D4C3DD;}
.salsplit-foot label{display:inline-flex; align-items:center; gap:7px; font-size:12px;
  font-weight:600; color:var(--muted);}
.salsplit-foot input{font:inherit; font-family:'Fraunces',serif; font-size:17px; font-weight:600;
  width:118px; text-align:right; border:1.5px solid #E4D9BE; background:#FBF6E9; border-radius:8px;
  padding:5px 9px; color:var(--ink);}
.salsplit-band{color:#fff; font-size:10.5px; font-weight:800; text-transform:uppercase;
  letter-spacing:.05em; border-radius:20px; padding:4px 11px;}
.salsplit-saving{margin-left:auto; font-family:'Fraunces',serif; font-weight:700; font-size:14px;
  color:#3F9577;}
@media (max-width:760px){
  .salsplit-saving{margin-left:0;}
  .salsplit-ends{font-size:10px;}
}

/* ---- the year, as a statement ---- */
.yrstmt{border:2px solid var(--ink) !important;}
.yr-head{display:flex; justify-content:space-between; align-items:flex-start; gap:16px; flex-wrap:wrap;
  padding-bottom:14px; margin-bottom:4px; border-bottom:2px solid var(--ink);}
.yr-kicker{font-size:10.5px; font-weight:800; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted); display:block; margin-bottom:4px;}
.yr-head h2{margin:0 !important;}
.yr-ent{border:1.5px solid; border-radius:22px; padding:6px 14px; font-size:12px; white-space:nowrap;}
.yr-cols{display:grid; grid-template-columns:1fr 1fr; gap:0 34px; margin-top:18px;}
.yr-col h4{font-size:10.5px; font-weight:800; letter-spacing:.07em; text-transform:uppercase;
  color:var(--muted); margin:0 0 4px;}
.yr-line{display:flex; justify-content:space-between; align-items:baseline; gap:14px;
  padding:9px 0; border-bottom:1px dotted var(--line); font-size:13.5px;}
.yr-line span{color:var(--muted);}
.yr-line b{font-variant-numeric:tabular-nums; font-weight:600; white-space:nowrap;}
.yr-line.neg b{color:var(--neg);}
.yr-line.sub{background:#FCFAF4; margin:0 -8px; padding-left:8px; padding-right:8px;}
.yr-line.tot{border-bottom:0; border-top:2px solid var(--ink); margin-top:4px; padding-top:12px;}
.yr-line.tot span{color:var(--ink); font-weight:600;}
.yr-line.tot b{font-family:'Fraunces',serif; font-weight:700; font-size:24px;}
.yr-strip{display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:20px; padding-top:18px;
  border-top:1px solid var(--line);}
.yr-cell{background:#FCFAF4; border:1px solid var(--line); border-radius:11px; padding:12px 14px;
  display:flex; flex-direction:column;}
.yr-cell .k{font-size:9.5px; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted);}
.yr-cell b{font-family:'Fraunces',serif; font-weight:700; font-size:22px; margin:4px 0 2px;}
.yr-cell .n{font-size:11px; color:var(--muted); line-height:1.4;}
.yr-note{margin-top:16px; background:#F4F8F6; border:1px solid #9FC4AF; border-radius:11px;
  padding:13px 16px; font-size:13px; line-height:1.65;}
.yr-fine{font-size:11.5px; color:var(--muted); line-height:1.6; margin:14px 0 0;}
@media (max-width:760px){
  .yr-cols{grid-template-columns:1fr; gap:0;}
  .yr-col + .yr-col{margin-top:20px;}
  .yr-strip{grid-template-columns:1fr 1fr;}
  .yr-ent{white-space:normal;}
}

/* the metro picker for the wage anchor */
.metropick{display:flex; align-items:center; gap:11px; flex-wrap:wrap; margin:14px 0 4px;
  background:#FCFAF4; border:1px solid var(--line); border-radius:11px; padding:11px 14px;}
.metropick-lab{font-size:10.5px; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted);}
.metropick select{font:inherit; font-size:13.5px; font-weight:600; color:var(--ink); padding:7px 10px;
  border:1.5px solid #E4D9BE; background:#FBF6E9; border-radius:8px; cursor:pointer;}
.metropick select:focus{outline:none; border-color:#B5483F;}
.metropick-note{font-size:11.5px; color:var(--muted); flex:1; min-width:200px;}
.wrow.mine{background:#EFF4F9; margin:3px -8px; padding:7px 8px; border-radius:8px;}
.wrow.mine .nm{color:var(--ink); font-weight:700;}
.wrow .nm em{font-style:normal; font-size:9.5px; font-weight:800; letter-spacing:.06em;
  text-transform:uppercase; color:#3B5A7A; background:#DCE8F3; border-radius:20px;
  padding:2px 7px; margin-left:7px;}

/* Medicare does not travel - this belongs with the residency cards, not in a footnote */
.medcost{margin:14px 0 0; background:#F7E7E5; border-left:4px solid #B5483F; border-radius:0 10px 10px 0;
  padding:13px 16px; font-size:13px; line-height:1.65; color:var(--muted); max-width:820px;}
.medcost b{color:var(--ink);}

/* ---- per-location retirement callout ---- */
.locret-lab{font-size:9.5px; font-weight:800; letter-spacing:.07em; text-transform:uppercase;
  color:#3F9577; margin-bottom:7px;}
.locret-bar{display:flex; height:22px; border-radius:6px; overflow:hidden; margin-bottom:7px;}
.locret-bar i{display:block;}
.locret-sp{display:flex; justify-content:space-between; font-size:11.5px; color:var(--muted);}
.locret-sp b{font-family:'Fraunces',serif; font-size:13.5px; color:var(--ink); margin-left:3px;}
.locret-why{font-size:11.5px; color:var(--muted); line-height:1.5; margin-top:7px;}
.locret-why b{color:var(--ink);}
.resid-retnote{font-size:13px; line-height:1.65; color:var(--muted); max-width:760px; margin:10px 0 0;}
.resid-retnote b{color:var(--ink);}

/* a sole proprietor has no split to make - say so, and look inert */
.salsplit-inert{opacity:.72;}
.salsplit-inert .salsplit-bar,.salsplit-inert .salsplit-range,
.salsplit-inert .salsplit-ends{filter:grayscale(.55);}
.salsplit-na{display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:14px;
  background:#fff; border:1px dashed #D4C3DD; border-radius:11px; padding:12px 15px;
  font-size:13px; line-height:1.6; color:var(--muted);}
.salsplit-na b{color:var(--ink);}
.salsplit-switch{margin-left:auto; border:0; border-radius:22px; color:#fff; font:inherit;
  font-weight:700; font-size:12.5px; padding:8px 15px; cursor:pointer; white-space:nowrap;}
.salsplit-saving.none{color:var(--neg); font-family:'Inter',sans-serif; font-weight:600; font-size:12.5px;}
.sc.nil{opacity:.6;}
.sc.nil i{background:#EFEAE0; color:var(--muted);}
.sc.nil b{color:var(--muted);}

/* ---- the wage anchor: what the work is worth ---- */
.wagea{margin-top:22px; padding-top:20px; border-top:1px solid var(--line);}
.wagea h4{font-family:'Fraunces',serif; font-size:17px; margin:0 0 7px;}
.wagebars{margin:14px 0 0;}
.wrow{display:flex; align-items:center; gap:11px; padding:6px 0; font-size:13px;}
.wrow .nm{width:186px; flex-shrink:0; color:var(--muted);}
.wrow.st .nm{color:var(--ink); font-weight:600;}
.wrow .tr{flex:1; background:#F1EDE3; border-radius:5px; height:19px; overflow:hidden;}
.wrow .tr i{display:block; height:100%; border-radius:5px;}
.wrow .vl{width:80px; text-align:right; font-family:'Fraunces',serif; font-weight:700; font-size:14px;
  flex-shrink:0;}
.wrow.you{background:#FBF6E9; margin:6px -8px; padding:9px 8px; border-radius:8px;}
.wrow.you .nm{font-weight:700; color:var(--ink);}
.wrow.peer{margin-top:4px; padding-top:9px; border-top:1px dashed #DED7C7;}
.wrow.peer .nm{color:#4C6B52; font-weight:600;}
.wrow.peer .nm em{background:#E7EFE6; color:#4C6B52;}
.wagetests{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:16px;}
@media (max-width:900px){.wagetests{grid-template-columns:1fr 1fr;}}
.wt{border:1.5px solid var(--line); border-radius:12px; padding:13px 15px;}
.wt .l{display:block; font-size:9.5px; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted); margin-bottom:4px;}
.wt > b{display:block; font-family:'Fraunces',serif; font-weight:700; font-size:17px; line-height:1.2;
  margin-bottom:5px;}
.wt .n{font-size:12px; color:var(--muted); line-height:1.55;}
.wagenote{margin-top:14px; background:#FBF1E2; border-left:4px solid #C98B4B; border-radius:0 9px 9px 0;
  padding:12px 15px; font-size:12.5px; line-height:1.65;}
.wagenote.counter{background:#F5EFF8; border-left-color:#6A4A78;}
.wagenote.peer{background:#EEF4EE; border-left-color:#4C6B52;}

/* ---- salary slider: three counters, not one ---- */
.salsplit-counters{display:grid; grid-template-columns:repeat(3,1fr); gap:9px; margin-top:13px;
  padding-top:13px; border-top:1px solid #D4C3DD;}
.sc{display:flex; align-items:flex-start; gap:8px; background:#fff; border:1px solid var(--line);
  border-radius:10px; padding:10px 12px;}
.sc i{font-style:normal; font-weight:800; font-size:13px; width:19px; height:19px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;}
.sc.up i{background:#E7F1EC; color:var(--pos);}
.sc.dn i{background:#F7E7E5; color:var(--neg);}
.sc span{font-size:11px; color:var(--muted); line-height:1.45;}
.sc b{display:block; font-family:'Fraunces',serif; font-size:16px; color:var(--ink); margin-bottom:1px;}
.salsplit-warn{font-size:11.5px; color:var(--muted); line-height:1.6; margin:11px 0 0;}

/* ---- setup timeline, habit, exit ---- */
.setuptl{margin:14px 0 4px;}
.stl{display:flex; gap:13px; align-items:flex-start; padding:11px 0; border-top:1px solid var(--line);}
.stl:first-child{border-top:0;}
.stl > i{display:flex; align-items:center; justify-content:center; width:24px; height:24px; flex-shrink:0;
  border-radius:50%; background:#6A4A78; color:#fff; font-style:normal; font-weight:800; font-size:11px;}
.stl b{display:block; font-size:14px; margin-bottom:3px;}
.stl p{margin:0; font-size:12.5px; color:var(--muted); line-height:1.6;}
.habit{margin-top:18px; background:#FCFAF4; border:1px solid var(--line); border-radius:11px;
  padding:14px 16px;}
.habit h5{font-family:'Fraunces',serif; font-size:15px; margin:0 0 8px;}
.habit p{font-size:12.5px; line-height:1.65; color:var(--muted); margin:0 0 9px;}
.habit p:last-child{margin-bottom:0;}
.habit b{color:var(--ink);}
.exitnote{margin-top:13px; background:#F7E7E5; border-left:4px solid #B5483F; border-radius:0 9px 9px 0;
  padding:12px 15px; font-size:12.5px; line-height:1.65;}

@media (max-width:820px){
  .wagetests,.salsplit-counters{grid-template-columns:1fr;}
  .wrow{flex-wrap:wrap;}
  .wrow .nm{width:100%; font-size:12px;}
  .wrow .vl{width:auto;}
}

/* ---- the two optional income modules ---- */
/* Off by default and rarely used - so when they are off they get one quiet
   row, not a full card competing with the control that actually matters. */
.planner .job2{transition:background .15s, border-color .15s;}
.planner .job2:not(.decision-impact):not(.job2-open){
  padding:13px 20px; box-shadow:none; background:#FCFAF4; border-color:#EDE8DC;}
.planner .job2:not(.decision-impact):not(.job2-open) .job2-head{gap:12px;}
.planner .job2:not(.decision-impact):not(.job2-open) .job2-title h3{font-size:15.5px;}
.planner .job2:not(.decision-impact):not(.job2-open) .job2-tag{font-size:11.5px;}
.planner .job2:not(.decision-impact):not(.job2-open):hover{background:#FBF6E9; border-color:#E4D9BE;}
.planner .job2.job2-open{border-color:#C9A876; background:#fff;}
.income-mods{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:28px;}
.income-mods > .job2{margin-bottom:0 !important;}
.income-mods > .job2.job2-open{grid-column:1 / -1;}
@media (max-width:760px){ .income-mods{grid-template-columns:1fr;} }

/* ---- Income: time off, and the arithmetic made visible ---- */
.controls{grid-template-columns:1fr 1fr !important;}
.timeoff{grid-column:1 / -1; display:flex; align-items:center; gap:13px; flex-wrap:wrap;
  padding:13px 0 0; margin-top:4px; border-top:1px dashed var(--line);}
.timeoff-body{display:flex; align-items:center; gap:8px; font-size:13px; color:var(--muted);}
.timeoff-body input{font-family:'Fraunces',serif; font-weight:700; font-size:17px; width:58px;
  text-align:center; border:1.5px solid #E4D9BE; background:#FBF6E9; border-radius:8px; padding:5px 6px;
  color:var(--ink);}
.timeoff-body input:focus{outline:none; border-color:#B5483F; background:#fff;}
.timeoff-off{font-size:12.5px; color:var(--muted);}
.timeoff-out{margin-left:auto; font-size:12.5px; color:var(--muted);}
.timeoff-out b{font-family:'Fraunces',serif; font-size:15px; color:var(--ink);}
.inc-eq{grid-column:1 / -1; display:flex; align-items:baseline; justify-content:center; gap:10px;
  flex-wrap:wrap; margin-top:14px; padding-top:14px; border-top:1px solid var(--line);
  font-size:13.5px; color:var(--muted);}
.inc-eq b{font-family:'Fraunces',serif; font-size:17px; color:var(--ink);}
.inc-eq i{font-style:normal; color:#BDB6A6;}
.inc-eq-res b,.inc-eq-res{font-family:'Fraunces',serif; font-weight:700; font-size:26px; color:var(--ink);}

/* ---- jump nav: numbered track, with derived sections marked as derived ---- */
.jumpnav-pill{display:flex; align-items:center; gap:8px;}
.jumpnav-n{display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px;
  border-radius:50%; font-style:normal; font-size:10.5px; font-weight:800; flex-shrink:0;
  background:#E4DED0; color:var(--muted);}
.jumpnav-done .jumpnav-n{background:var(--pos); color:#fff;}
.jumpnav-derived .jumpnav-n{background:transparent; color:#BDB6A6; font-family:'Fraunces',serif;
  font-size:14px; border:1px dashed #D8D2C4;}
.jumpnav-txt{display:flex; flex-direction:column; min-width:0;}
.jumpnav-active .jumpnav-n{background:#fff; color:var(--ink);}
.jumpnav-active.jumpnav-done .jumpnav-n{background:var(--pos); color:#fff;}
@media (max-width:760px){
  .timeoff-out{margin-left:0; width:100%;}
  .inc-eq{font-size:12px; gap:7px;}
  .inc-eq b{font-size:15px;}
  .inc-eq-res,.inc-eq-res b{font-size:20px;}
  .jumpnav-n{width:17px; height:17px; font-size:9.5px;}
}

/* ---- THE VERDICT: the answer before the working ---- */
.vcard{border:2px solid var(--ink) !important; background:#FCFAF4 !important;}
.vcard-yes{border-color:#9FC4AF !important; background:#F4F8F6 !important;}
.vc-k{font-size:10px; font-weight:800; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted); margin-bottom:8px;}
.vcard h2{font-family:'Fraunces',serif; font-weight:700; font-size:clamp(24px,3vw,31px);
  letter-spacing:-.02em; line-height:1.12; margin:0 0 11px !important;}
.vc-p{font-size:15px; line-height:1.7; margin:0; max-width:720px;}
.vc-p b{color:var(--ink);}
.vc-aggr{margin:14px 0 0; background:#FBF1E2; border-left:4px solid #C98B4B; border-radius:0 10px 10px 0;
  padding:13px 16px; font-size:13.5px; line-height:1.65; max-width:760px;}
.vc-fine{font-size:11.5px; color:var(--muted); line-height:1.6; margin:12px 0 0;}

/* the receipt */
.vrec-b{border:1px solid var(--line); border-radius:12px; overflow:hidden; background:#fff;}
.vrec-r{display:flex; align-items:flex-start; justify-content:space-between; gap:16px;
  padding:13px 16px; border-bottom:1px dotted var(--line);}
.vrec-r span{flex:1;}
.vrec-r span b{display:block; font-size:13.5px; font-weight:600;}
.vrec-r span i{display:block; font-style:normal; font-size:11.5px; color:var(--muted);
  line-height:1.5; margin-top:2px;}
.vrec-r .v{font-family:'Fraunces',serif; font-weight:700; font-size:17px; white-space:nowrap;
  font-variant-numeric:tabular-nums;}
.vrec-r.neg .v{color:var(--neg);}
.vrec-r.neg span b{color:var(--ink);}
.vrec-r.neg span i{color:var(--muted);}
.vrec-r.tot{border-bottom:0; border-top:2px solid var(--ink); background:#FCFAF4; padding:15px 16px;}
.vrec-r.tot span b{font-size:14.5px;}
.vrec-r.tot .v{font-size:26px;}
.vrec-r.tot .v.pos{color:var(--pos);} .vrec-r.tot .v.neg{color:var(--neg);}
.vrec-say{margin-top:13px; background:#F7E7E5; border-radius:10px; padding:12px 15px;
  font-size:13px; line-height:1.6;}

/* the levers */
.vlev-r{display:flex; align-items:flex-start; gap:13px; padding:12px 0;
  border-bottom:1px dotted var(--line);}
.vlev-r:last-of-type{border-bottom:0;}
.vlev-r > i{width:25px; height:25px; border-radius:7px; background:#F1EDE3; color:var(--muted);
  font-style:normal; font-size:11px; font-weight:800; display:flex; align-items:center;
  justify-content:center; flex-shrink:0;}
.vlev-r.good > i{background:#E7F1EC; color:var(--pos);}
.vlev-r .t{flex:1;}
.vlev-r .t b{display:block; font-size:13.5px;}
.vlev-r .t span{display:block; font-size:11.5px; color:var(--muted); line-height:1.5; margin-top:2px;}
.vlev-r .v{font-family:'Fraunces',serif; font-weight:700; font-size:16px; white-space:nowrap;}
.vlev-r.good .v{color:var(--pos);} .vlev-r.bad .v{color:var(--neg);}
.vlev-note{margin:14px 0 0; padding-top:13px; border-top:1px solid var(--line);
  font-size:13px; line-height:1.65;}

/* the line between the answer and the working */
.vwork{margin:6px 0 22px; padding:13px 18px; background:#F6F2E8; border-radius:11px;
  font-size:12.5px; line-height:1.6; color:var(--muted); border:1px dashed var(--line);}

/* ---- mobileFold: heavy blocks get a summary line on phones, stay open on desktop ---- */
.mfold{padding:14px 16px !important;}
.mfold-s{display:flex; align-items:baseline; flex-wrap:wrap; gap:5px 11px; cursor:pointer;
  list-style:none;}
.mfold-s::-webkit-details-marker{display:none;}
.mfold-s b{font-family:'Fraunces',serif; font-size:19px; font-weight:700;}
.mfold-s span{font-size:12px; color:var(--muted);}
.mfold[open] > .mfold-s{margin-bottom:4px;}
/* the wrapped section keeps its own explanatory paragraph but not its heading,
   because the summary above is now that heading */
.mfold > .card{border:0 !important; box-shadow:none !important; background:transparent !important;
  padding:0 !important; margin:0 !important; border-radius:0 !important;}
.mfold > .card > .card-head > h2{display:none;}
.mfold > .card.decision-impact{border-left:0 !important;}
@media (max-width:780px){
  .mfold-s b{font-size:17px;}
  .mfold{padding:13px 15px !important;}
}

/* ---- the shared row: label, bar on a common scale, value. Used by the rate
   ladder, the profit waterfall and anywhere a small table used to sit. This is
   the same shape as .rlev-r in Tax strategy - one vocabulary across the tool. --- */
.uro-list{display:flex; flex-direction:column;}
.uro{display:flex; align-items:center; gap:13px; padding:11px 0;
  border-bottom:1px dotted var(--line);}
.uro:last-child{border-bottom:0;}
.uro[role="button"]{cursor:pointer; border-radius:9px; margin:0 -9px; padding-left:9px; padding-right:9px;}
.uro[role="button"]:hover{background:#FBF6E9;}
.uro[role="button"]:focus-visible{outline:2px solid var(--ink); outline-offset:2px;}
.uro.on{background:#FBF6E9; margin:0 -9px; padding-left:9px; padding-right:9px; border-radius:9px;}
.uro-l{width:104px; flex-shrink:0; font-size:13.5px; font-weight:600;
  display:flex; align-items:baseline; gap:7px;}
.uro-l em{font-style:normal; font-size:9.5px; font-weight:800; letter-spacing:.05em;
  text-transform:uppercase; color:#8A5B24; background:#F7EBDA; border-radius:99px; padding:2px 7px;}
.uro-b{flex:1; height:17px; background:#F1EDE3; border-radius:5px; overflow:hidden; min-width:30px;}
.uro-b i{display:block; height:100%; border-radius:5px;}
.uro-v{width:112px; text-align:right; flex-shrink:0;
  font-family:'Fraunces',serif; font-weight:700; font-size:16px;}
.uro-v em{display:block; font-family:'Inter',sans-serif; font-style:normal; font-weight:500;
  font-size:10.5px; color:var(--muted); margin-top:1px;}
.uro-d{width:86px; text-align:right; flex-shrink:0;
  font-family:'Fraunces',serif; font-weight:700; font-size:14px;}
.uro-d.muted{color:var(--muted);} .uro-d.pos{color:var(--pos);} .uro-d.neg{color:var(--neg);}
@media (max-width:760px){
  .uro{flex-wrap:wrap; align-items:baseline; gap:3px 10px; padding:12px 0;}
  .uro-l{width:auto; flex:1;}
  .uro-d{width:auto;}
  .uro-v{width:auto; text-align:left; order:3; flex-basis:100%; display:flex;
    align-items:baseline; gap:9px; margin-top:3px;}
  .uro-v em{display:inline; margin-top:0;}
  .uro-b{order:4; flex-basis:100%; margin-top:5px;}
}

/* ---- shared fold: one summary line, content behind it ---- */
.payfold, .ratefold{margin-top:14px; border-top:1px solid var(--line); padding-top:12px;}
.payfold > summary, .ratefold > summary{display:flex; align-items:baseline; gap:9px; cursor:pointer;
  list-style:none; padding:2px 0;}
.payfold > summary::-webkit-details-marker, .ratefold > summary::-webkit-details-marker{display:none;}
.payfold > summary b, .ratefold > summary b{font-family:'Fraunces',serif; font-size:14px;}
.payfold > summary span, .ratefold > summary span{font-size:11.5px; color:var(--muted);}
.payfold > summary i, .ratefold > summary i{margin-left:auto; font-style:normal; font-size:11px;
  font-weight:700; color:var(--muted); border:1px solid var(--line); border-radius:99px;
  padding:3px 11px; white-space:nowrap;}
.payfold[open] > summary i::after, .ratefold[open] > summary i::after{content:"n";
  font-size:0;}
.payfold[open] > summary i, .ratefold[open] > summary i{color:var(--ink);}
.payfold > summary + *, .ratefold > summary + *{margin-top:12px;}
.paylede{display:flex; align-items:baseline; flex-wrap:wrap; gap:5px 12px; margin:0 0 13px;}
.paylede b{font-family:'Fraunces',serif; font-size:31px; font-weight:700; line-height:1;}
.paylede span{font-size:12.5px; color:var(--muted);}
.pay-next{margin-bottom:0;}

/* ---- shared: a section-closing pointer to the decision that matters ---- */
.sec-point{background:#F1F7F4; border-left:4px solid #2F7A61; border-radius:0 11px 11px 0;
  padding:13px 16px; margin:14px 0 0; font-size:13px; line-height:1.65;}
.sec-point b{font-family:'Fraunces',serif; font-weight:700;}
.sec-point a{color:#2F7A61; font-weight:600;}

/* ---- the retirement verdict: the lever that comes first ---- */
.rvrec .vrec-say{background:#EEF4F1;}
.rvrec .vrec-r.tot .v{color:var(--pos);}
.rcard{border-color:#2F7A61 !important; background:#F4F8F6 !important;}
.rcomp{margin:16px 0 4px; background:#fff; border:1px solid #D9E5DE; border-radius:12px; padding:13px 15px 11px;}
.rcomp-r{display:flex; align-items:center; gap:12px; padding:5px 0;}
.rcomp-r .l{width:210px; flex-shrink:0; font-size:12.5px; color:#4A5A52;}
.rcomp-r .b{flex:1; height:15px; background:#F1EDE3; border-radius:4px; overflow:hidden; min-width:40px;}
.rcomp-r .b i{display:block; height:100%; border-radius:4px;}
.rcomp-r .v{width:86px; text-align:right; font-family:'Fraunces',serif; font-weight:700;
  font-size:15px; flex-shrink:0;}
.rcomp-n{display:block; margin-top:9px; padding-top:9px; border-top:1px dotted #D9E5DE;
  font-size:12px; line-height:1.6; color:#4A5A52;}
.rcard .vrec-say, .rlev + * {}
.rlev-r{display:flex; align-items:center; gap:13px; padding:12px 0;
  border-bottom:1px dotted var(--line);}
.rlev-r:last-of-type{border-bottom:0;}
.rlev-r > i{width:25px; height:25px; border-radius:7px; background:#F1EDE3; color:var(--muted);
  font-style:normal; font-size:11px; font-weight:800; display:flex; align-items:center;
  justify-content:center; flex-shrink:0;}
.rlev-r.best > i{background:#E7F1EC; color:var(--pos);}
.rlev-r .t{width:264px; flex-shrink:0;}
.rlev-r .t b{display:flex; align-items:baseline; gap:7px; font-size:13.5px;}
.rlev-r .t b em{font-style:normal; font-size:9.5px; font-weight:800; letter-spacing:.05em;
  text-transform:uppercase; color:var(--pos); background:#E7F1EC; border-radius:99px; padding:2px 7px;}
.rlev-r .t > span{display:block; font-size:11.5px; color:var(--muted); line-height:1.5; margin-top:2px;}
.rlev-r .bar{flex:1; height:15px; background:#F1EDE3; border-radius:4px; overflow:hidden; min-width:30px;}
.rlev-r .bar i{display:block; height:100%; border-radius:4px; background:#8AA98F;}
.rlev-r.best .bar i{background:#2F7A61;}
.rlev-r .v{width:104px; text-align:right; font-family:'Fraunces',serif; font-weight:700;
  font-size:16px; flex-shrink:0;}
.rlev-r .v em{display:block; font-family:'Inter',sans-serif; font-style:normal; font-weight:500;
  font-size:10.5px; color:var(--muted); margin-top:1px;}

/* ---- the structure question, folded to one line ---- */
.vfold{border:1.5px solid var(--line) !important;}
.vfold[open]{border-color:var(--ink) !important;}
.vfold-s{display:flex; align-items:baseline; flex-wrap:wrap; gap:6px 12px; cursor:pointer;
  list-style:none; padding:2px 0;}
.vfold-s::-webkit-details-marker{display:none;}
.vfold-k{font-size:10px; font-weight:800; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted); width:100%;}
.vfold-q{font-family:'Fraunces',serif; font-size:18px; font-weight:700;}
.vfold-a{font-family:'Fraunces',serif; font-size:18px; font-weight:700;}
.vfold-v{display:flex; align-items:baseline; gap:6px;}
.vfold-v b{font-family:'Fraunces',serif; font-size:18px;}
.vfold-v i{font-style:normal; font-size:11.5px; color:var(--muted);}
.vfold-o{margin-left:auto; font-size:11.5px; font-weight:700; color:var(--muted);
  border:1px solid var(--line); border-radius:99px; padding:4px 12px; white-space:nowrap;}
.vfold-o em{font-style:normal;}
.vfold-o .c{display:none;}
.vfold[open] .vfold-o .o{display:none;}
.vfold[open] .vfold-o .c{display:inline;}
.vfold[open] .vfold-s{margin-bottom:14px; padding-bottom:12px; border-bottom:1px solid var(--line);}
.vfold > .card{border:1px solid var(--line) !important; box-shadow:none !important; margin-bottom:14px;}
.vfold > .vcard{border:2px solid var(--ink) !important;}

@media (max-width:760px){
  .vrec-r{flex-wrap:wrap; gap:6px;}
  .vrec-r .v{font-size:16px;}
  .vrec-r.tot .v{font-size:22px;}
  .vc-p{font-size:14px;}
  .rcomp-r{flex-wrap:wrap; gap:4px 10px;}
  .rcomp-r .l{width:auto; flex:1;}
  .rcomp-r .b{order:3; flex-basis:100%; min-width:0;}
  .rlev-r{flex-wrap:wrap; align-items:flex-start; gap:3px 0;}
  .rlev-r > i{margin-right:13px;}
  .rlev-r .t{width:auto; flex:1 1 calc(100% - 38px);}
  .rlev-r .v{order:2; width:auto; flex-basis:100%; margin-left:38px; text-align:left;
    display:flex; align-items:baseline; gap:8px; margin-top:5px;}
  .rlev-r .v em{margin-top:0;}
  .rlev-r .bar{order:3; flex-basis:calc(100% - 38px); margin:6px 0 2px 38px;}
  .vfold-o{margin-left:0;}
}

/* ---- the opener: what this section is, before it asks anything ---- */
.opener{border:2px solid var(--line) !important;}
.opener-eyebrow{font-size:10.5px; font-weight:800; letter-spacing:.1em; text-transform:uppercase;
  color:#C98B4B; margin-bottom:9px;}
.opener h2{font-size:26px !important; margin:0 0 11px !important;}
.opener p{font-size:14.5px; line-height:1.7; margin:0 0 14px; max-width:690px; color:var(--ink);}
.opener-qs{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:20px 0 0;}
.opener-q{background:#FCFAF4; border:1px solid var(--line); border-radius:11px; padding:13px 15px;}
.opener-q b{display:block; font-family:'Fraunces',serif; font-size:14.5px; margin-bottom:4px;}
.opener-q span{font-size:12.5px; color:var(--muted); line-height:1.5;}
.opener-cant{margin-top:18px; background:#FBF1E2; border-left:4px solid #C98B4B; border-radius:0 10px 10px 0;
  padding:13px 16px; font-size:13px; line-height:1.6;}
.opener-cant b{display:block; margin-bottom:3px;}

/* ---- the stepper ---- */
.rail-wrap{margin:0 0 22px; border:1px solid var(--line); border-radius:14px; overflow:hidden; background:#fff;}
.rail{display:flex;}
.rail-step{flex:1; display:flex; flex-direction:column; gap:5px; padding:13px 15px;
  border-right:1px solid var(--line);}
.rail-step:last-child{border-right:0;}
.rail-top{display:flex; align-items:center; gap:8px;}
.rail-n{display:inline-flex; align-items:center; justify-content:center; width:21px; height:21px;
  border-radius:50%; font-size:11px; font-weight:800; font-style:normal; background:#EFEAE0;
  color:var(--muted); flex-shrink:0;}
.rail-top b{font-size:12.5px; letter-spacing:-.01em;}
.rail-s{font-size:10.5px; color:var(--muted); line-height:1.35;}
.rail-step.done{background:#F4F8F6;}
.rail-step.done .rail-n{background:var(--pos); color:#fff;}
.rail-step.opt .rail-n{background:#EFEAE0;}
.rail-step.out{background:#FCFAF4;}
.rail-step.out.done{background:#F4F8F6;}
.rail-bar{height:4px; background:#EFEAE0;}
.rail-bar i{display:block; height:100%; background:var(--pos); transition:width .3s;}
.rail-meta{display:flex; justify-content:space-between; align-items:baseline; padding:9px 15px;
  font-size:11px; color:var(--muted); background:#FCFAF4;}
.rail-meta b{color:var(--ink); font-size:11.5px;}

/* ---- money flow ---- */
.fkey{display:flex; gap:8px; flex-wrap:wrap; margin:4px 0 16px;}
.fkey span{display:inline-flex; align-items:center; gap:7px; border:1px solid var(--line);
  background:#FCFAF4; border-radius:9px; padding:7px 12px 7px 9px; font-size:12px; line-height:1.35;}
.fkey i{width:13px; height:13px; border-radius:4px; flex-shrink:0;}
.fkey em{font-style:normal; color:var(--muted);}
.scen{margin-bottom:6px;}
.scen-lab{display:flex; justify-content:space-between; align-items:baseline; gap:12px; margin-bottom:6px;}
.scen-lab b{font-size:12.5px;}
.scen-lab span{font-size:11.5px; color:var(--muted);}
.fbar{display:flex; height:54px; border-radius:9px; overflow:hidden;}
.fbar i{display:flex; flex-direction:column; align-items:center; justify-content:center; font-style:normal;
  color:#fff; text-align:center; padding:0 5px; min-width:0; transition:width .3s;}
.fbar i b{font-family:'Fraunces',serif; font-size:16px; line-height:1.1; order:2;}
.fbar i span{font-size:8.5px; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
  opacity:.92; order:1; margin-bottom:2px;}
.s-irs{background:#B5483F;} .s-bank{background:var(--ink);} .s-inv{background:var(--pos);}
.arrowrow{display:flex; align-items:center; gap:12px; margin:13px 0; padding:12px 15px;
  background:#F4F8F6; border:1px dashed #9FC4AF; border-radius:10px; font-size:13px; line-height:1.55;}
.arrowrow .big{font-family:'Fraunces',serif; font-weight:700; font-size:19px; color:var(--pos); white-space:nowrap;}
.mftotals{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:18px;}
.mftot{border:2px solid var(--line); border-radius:12px; padding:14px 16px; display:flex; flex-direction:column;}
.mftot.win{border-color:#9FC4AF; background:#F4F8F6;}
.mftot .l{font-size:10px; font-weight:800; letter-spacing:.07em; text-transform:uppercase; color:var(--muted);}
.mftot b{font-family:'Fraunces',serif; font-weight:700; font-size:27px; margin:5px 0 6px;}
.mftot.win b{color:var(--pos);}
.mftot .n{font-size:12px; color:var(--muted); line-height:1.55;}
.mfpunch{margin-top:16px; background:#F4F8F6; border:1px solid #9FC4AF; border-radius:12px;
  padding:15px 17px; font-size:14px; line-height:1.7;}
.mfpunch > b:first-child{font-family:'Fraunces',serif; font-size:17px; display:block; margin-bottom:5px;}
.mftrade{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:14px;}
.mft{border-radius:11px; padding:13px 15px; font-size:13px; line-height:1.6;}
.mft b{display:block; font-family:'Fraunces',serif; font-size:15px; margin-bottom:3px;}
.mft.cost{background:#FBF1E2; border-left:4px solid #C98B4B;}
.mft.gain{background:#F4F8F6; border-left:4px solid var(--pos);}
.mflater{margin-top:16px; border:1px solid var(--line); border-radius:12px; overflow:hidden;}
.mflater-h{padding:11px 15px; background:#F6F2E8; font-size:11px; font-weight:800; letter-spacing:.07em;
  text-transform:uppercase; color:var(--muted);}
.mflater-b{padding:15px; display:flex; align-items:center; gap:16px; flex-wrap:wrap;}
.mflater-b .n{font-family:'Fraunces',serif; font-weight:700; font-size:30px; color:var(--pos);}
.mflater-b .d{font-size:12.5px; color:var(--muted); line-height:1.55; flex:1; min-width:230px;}
.mfwarn{margin-top:13px; background:#FBF1E2; border-left:4px solid #C98B4B; border-radius:0 9px 9px 0;
  padding:12px 15px; font-size:12.5px; line-height:1.6;}

/* ---- contribute-nothing vs max: reuses the comparison-table pattern ---- */
.mfh{padding:0 !important;}
.mfh-in{display:flex; flex-direction:column; gap:3px; padding:11px 12px 12px;}
.mfh-in b{font-family:'Fraunces',serif; font-size:14.5px; line-height:1.15; letter-spacing:-.01em;}
.mfh-in small{font-size:10.5px; color:var(--muted);}
.mfmini{display:flex; height:9px; border-radius:5px; overflow:hidden; margin-top:5px;}
.mfmini i{display:block;}
.mftable .cmp-l{width:34%;}
@media (max-width:760px){
  .mftable .mfh-in{padding:9px 10px;}
  .mfc .cmp-cell::before{content:attr(data-lab);}
  .mf-none::before{color:#7C766A;}
  .mf-max::before{color:#2F7A61;}
}

/* ---- Social Security detail ---- */
.ssd-tbl{width:100%; border-collapse:separate; border-spacing:0; font-size:13px;}
.ssd-tbl th{font-size:10px; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted); padding:0 10px 8px; text-align:right;}
.ssd-tbl th:first-child{text-align:left;}
.ssd-tbl td{padding:12px 10px; border-top:1px solid var(--line); text-align:right;
  font-variant-numeric:tabular-nums; font-family:'Fraunces',serif; font-weight:700; font-size:18px;}
.ssd-tbl td:first-child{text-align:left; font-family:'Inter',sans-serif; font-weight:400; font-size:13px;}
.ssd-tbl td:first-child b{font-size:15px;}
.ssd-tbl td:first-child span{display:block; font-size:11.5px; color:var(--muted); margin-top:2px;}
.ssd-tbl tr.hi td{box-shadow:inset 0 0 0 99px rgba(251,246,233,.55);}
.ssd-tbl .gap{color:var(--neg); font-size:15px;}
.ssd-ass{margin-top:18px; border:1px dashed var(--line); border-radius:11px; padding:14px 16px;
  background:#FCFAF4;}
.ssd-ass > b{font-size:10.5px; font-weight:800; letter-spacing:.07em; text-transform:uppercase;
  color:var(--muted); display:block; margin-bottom:9px;}
.ssd-ass ul{margin:0; padding-left:17px; font-size:12.5px; line-height:1.8; color:var(--muted);}
.ssd-ass ul b{color:var(--ink);}
.ssd-port{margin-top:16px; border:1px solid var(--line); border-radius:12px; overflow:hidden;}
.ssd-port-h{padding:12px 16px; background:#F6F2E8;}
.ssd-port-h b{font-family:'Fraunces',serif; font-size:15px;}
.ssd-port-h span{display:block; font-size:11.5px; color:var(--muted); margin-top:2px;}
.ssd-row{display:flex; align-items:center; gap:12px; padding:10px 16px; border-top:1px solid var(--line);
  font-size:13px; flex-wrap:wrap;}
.ssd-row > b{min-width:118px; font-weight:600;}
.ssd-row > span{flex:1; min-width:200px; font-size:11.5px; color:var(--muted); line-height:1.5;}
.ssd-row > i{font-style:normal; font-size:10.5px; font-weight:800; letter-spacing:.05em;
  text-transform:uppercase; padding:3px 10px; border-radius:20px; white-space:nowrap;}
.ssd-row > i.yes{background:#E7F1EC; color:var(--pos);}
.ssd-row > i.no{background:#F7E7E5; color:var(--neg);}
.ssd-med{margin-top:14px; background:#F7E7E5; border-left:4px solid var(--neg); border-radius:0 9px 9px 0;
  padding:12px 15px; font-size:13px; line-height:1.6;}
.ssd-med b{display:block; margin-bottom:3px;}

@media (max-width:820px){
  .opener-qs,.mftotals,.mftrade{grid-template-columns:1fr;}
  .rail{flex-wrap:wrap;}
  .rail-step{flex:1 1 46%; border-bottom:1px solid var(--line);}
  .fbar{flex-direction:column; height:auto;}
  .fbar i{width:100% !important; flex-direction:row; align-items:center; justify-content:space-between;
    padding:11px 14px; min-height:44px; text-align:left;}
  .fbar i span{margin-bottom:0; order:1;} .fbar i b{order:2;}
  .scen-lab{flex-direction:column; align-items:flex-start; gap:2px;}
  .scen{margin-bottom:14px;}
  .arrowrow{flex-direction:column; align-items:flex-start; gap:6px;}
  .ssd-tbl td{font-size:15px; padding:10px 6px;}
  .ssd-tbl th{padding:0 6px 8px;}
}

/* ---- Step 1: numbered, self-counting, and blank when it is blank ---- */
.stepcard{border:2px solid var(--amber) !important;}
.stepcard-done{border-color:#9FC4AF !important;}
.stepcard-head{display:flex; align-items:flex-start; gap:14px; margin:-4px 0 16px;}
.stepcard-n{display:flex; align-items:center; justify-content:center; width:34px; height:34px;
  border-radius:50%; background:var(--ink); color:#fff; font-family:'Fraunces',serif; font-weight:700;
  font-size:16px; flex-shrink:0;}
.stepcard-done .stepcard-n{background:var(--pos);}
.stepcard-head h2{margin:0 0 3px !important;}
.stepcard-head p{margin:0 !important; max-width:600px;}
.stepcard-count{margin-left:auto; text-align:right; flex-shrink:0;}
.stepcard-count b{display:block; font-family:'Fraunces',serif; font-size:19px;}
.stepcard-count span{font-size:10px; font-weight:700; letter-spacing:.06em; text-transform:uppercase;
  color:var(--muted);}
.sfields{display:grid; grid-template-columns:repeat(3,1fr); gap:16px;}
.sfield label{display:flex; align-items:center; gap:6px; font-size:10.5px; font-weight:800;
  letter-spacing:.06em; text-transform:uppercase; color:var(--muted); margin-bottom:7px;}
.sfield-tick{display:inline-flex; align-items:center; justify-content:center; width:14px; height:14px;
  border-radius:50%; font-size:8px; font-weight:800; font-style:normal; background:#EFEAE0; color:#fff;}
.sfield-tick.on{background:var(--pos);}
.sfield input{width:100%; font-family:'Fraunces',serif; font-size:21px; font-weight:600; color:var(--ink);
  border:1.5px dashed #D8D2C4; background:#fff; border-radius:9px; padding:9px 12px;}
.sfield input::placeholder{color:#BDB6A6; font-style:italic; font-size:15px;}
.sfield input:focus{outline:none; border-color:#B5483F; border-style:solid;}
.sfield.ok input{border-style:solid; border-color:#9FC4AF; background:#F4F8F6;}
.sfield-hint{display:block; font-size:11px; color:var(--muted); margin-top:6px; line-height:1.4;}

/* ---- the smaller gate: a look at what is behind it, not a grey wall ---- */
.peek{position:relative; border:2px dashed var(--line); border-radius:14px; overflow:hidden;
  background:#fff; margin-top:16px;}
.peek-blur{filter:blur(3.5px); opacity:.45; pointer-events:none; padding:16px 18px; user-select:none;}
.peek-row{display:flex; align-items:center; gap:10px; padding:7px 0; font-size:13px;
  border-top:1px solid var(--line);}
.peek-row:first-child{border-top:0;}
.peek-row span{flex:1; font-weight:600;}
.peek-row i{font-style:normal; font-family:'Fraunces',serif; font-weight:700; font-size:14px;
  width:104px; text-align:right; padding:4px 8px; border-radius:5px;}
.peek-over{position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
  justify-content:center; gap:11px; text-align:center; padding:22px;
  background:linear-gradient(rgba(251,249,243,.80),rgba(251,249,243,.96));}
.peek-over h4{font-family:'Fraunces',serif; font-weight:700; font-size:19px; margin:0; letter-spacing:-.015em;}
.peek-over p{font-size:13px; color:var(--muted); margin:0; max-width:470px; line-height:1.6;}
.peek-need{display:flex; gap:7px; flex-wrap:wrap; justify-content:center;}
.peek-need span{display:inline-flex; align-items:center; background:#fff; border:1.5px solid var(--line);
  border-radius:20px; padding:5px 12px; font-size:12px; font-weight:600;}
.peek-need span.ok{border-color:#9FC4AF; background:#F4F8F6; color:var(--pos);}
.peek-go{background:var(--ink); color:#fff; border:0; border-radius:24px; padding:9px 19px; font:inherit;
  font-weight:700; font-size:13px; cursor:pointer;}
.peek-go:hover{background:#3D3931;}
@media (max-width:760px){
  .sfields{grid-template-columns:1fr;}
  .stepcard-count{margin-left:0; text-align:left; width:100%; display:flex; align-items:baseline; gap:7px;}
  .peek-row span{font-size:11.5px;}
  .peek-row i{width:78px; font-size:12px;}
}

/* the structure picker - same two colours as the table columns */
.entpick{display:flex; align-items:center; gap:9px; flex-wrap:wrap; margin-bottom:16px;}
.entpick-lab{font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:.07em;
  color:var(--muted);}
.entpick-btn{display:inline-flex; align-items:center; gap:8px; font:inherit; font-weight:700;
  font-size:14px; padding:9px 16px 9px 9px; cursor:pointer; border:2px solid; border-radius:24px;
  transition:all .14s ease;}
.entpick-btn:hover{filter:brightness(.97);}

/* the inline name tag, used in prose and on cards outside the table */
.enttag{display:inline-flex; align-items:center; gap:5px; border:1px solid; border-radius:20px;
  padding:2px 9px 2px 3px; font-size:11.5px; font-weight:700; line-height:1.5; white-space:nowrap;
  vertical-align:baseline;}
.enttag i{display:inline-flex; align-items:center; justify-content:center; width:15px; height:15px;
  border-radius:50%; color:#fff; font-size:9px; font-weight:800; font-style:normal;}
.enttag-solid{color:#fff;}
.enttag-solid i{background:rgba(255,255,255,.28) !important;}
.enttag-sm{font-size:10.5px; padding:1px 7px 1px 2px;}
.enttag-sm i{width:13px; height:13px; font-size:8px;}

/* ---- the two identity cards above the table ---- */
.cmp-legend{display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:4px 0 18px;}
.cmp-legcard{display:flex; flex-direction:column; gap:7px; text-align:left; font:inherit;
  cursor:pointer; border:2px solid; border-radius:14px; padding:15px 16px 14px;
  transition:border-color .15s, background .15s, transform .12s;}
.cmp-legcard:hover{transform:translateY(-1px);}
.cmp-legtop{display:flex; align-items:center; gap:8px;}
.cmp-legtop b{font-family:'Fraunces',serif; font-size:17px; letter-spacing:-.01em; line-height:1.15;}
.cmp-legsub{font-size:12px; line-height:1.5; color:var(--muted);}
.cmp-legnum{font-family:'Fraunces',serif; font-weight:700; font-size:23px; color:var(--ink);
  display:flex; flex-direction:column; margin-top:auto; padding-top:6px;}
.cmp-legnum small{font-family:'Inter',sans-serif; font-weight:600; font-size:10px; color:var(--muted);
  text-transform:uppercase; letter-spacing:.06em; margin-top:2px;}
.cmp-legpick{align-self:flex-start; font-size:10.5px; font-weight:700; text-transform:uppercase;
  letter-spacing:.05em; border:1.5px solid; border-radius:20px; padding:4px 11px; margin-top:4px;}
.cmp-chip{display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px;
  border-radius:50%; color:#fff; font-size:11px; font-weight:800; font-style:normal; flex-shrink:0;}

/* ---- the table ---- */
.cmp-wrap{overflow:visible;}
.cmp-table{width:100%; border-collapse:separate; border-spacing:0;}
.cmp-table th{padding:0; vertical-align:bottom;}
.cmp-h-l{width:36%;}
.cmp-col-a,.cmp-col-b{width:21%;}
.cmp-col-d{width:15%;}

/* sticky header - sits just under the sticky jump-nav, never over it */
.cmp-table thead th{position:sticky; top:70px; z-index:8;}
.cmp-h{border-top:4px solid; border-left:1px solid; border-right:1px solid transparent;
  border-radius:12px 12px 0 0; padding:0 !important; overflow:hidden;}
.cmp-h-l,.cmp-h-d{background:var(--bg);}
.cmp-hbtn{display:flex; flex-direction:column; gap:3px; width:100%; text-align:left; font:inherit;
  cursor:pointer; background:transparent; border:0; padding:11px 12px 12px;}
.cmp-hname{display:flex; align-items:center; gap:7px; font-family:'Fraunces',serif; font-weight:700;
  font-size:14.5px; line-height:1.15; letter-spacing:-.01em;}
.cmp-hsub{font-size:10.5px; color:var(--muted); line-height:1.3;}
.cmp-hpick{align-self:flex-start; margin-top:4px; font-size:9.5px; font-weight:800;
  text-transform:uppercase; letter-spacing:.05em; border:1.5px solid; border-radius:20px; padding:3px 9px;}
.cmp-h-d{text-align:right; padding:0 8px 11px !important; vertical-align:bottom;}
.cmp-h-d span{display:block; font-size:11.5px; font-weight:700; color:var(--muted);}
.cmp-h-d small{display:block; font-size:9.5px; color:var(--muted); opacity:.8; margin-top:1px;}

/* body */
.cmp-table tbody td{padding:10px 10px; border-top:1px solid var(--line); font-size:14px;
  vertical-align:top;}
.cmp-l{width:36%;}
.cmp-lbl{display:block; font-weight:600; font-size:13.5px; line-height:1.35;}
.cmp-hint{display:block; font-size:11px; color:var(--muted); margin-top:3px; line-height:1.4;}
.cmp-cell{text-align:right; font-variant-numeric:tabular-nums; border-left:1px solid; position:relative;
  white-space:nowrap;}
.cmp-v{font-weight:600;}
.cmp-wintick{font-style:normal; font-size:10px; color:var(--pos); margin-right:4px; vertical-align:1px;}
.cmp-win .cmp-v{color:var(--pos);}
.cmp-d{text-align:right; font-variant-numeric:tabular-nums; font-weight:600; color:var(--muted);
  padding-left:14px !important;}
.cmp-d.pos{color:var(--pos);}
.cmp-d.neg{color:var(--neg);}
.cmp-big td{padding-top:13px !important; padding-bottom:13px !important;}
.cmp-big .cmp-lbl{font-size:14.5px;}
.cmp-big .cmp-v{font-family:'Fraunces',serif; font-weight:700; font-size:19px;}
.cmp-big .cmp-d{font-size:15px;}
.cmp-big .cmp-wintick{font-size:12px;}

/* group bands - they repeat the column identity every few rows so you never
   have to scroll back up to remember which side you are reading */
.cmp-grp td{background:#F6F2E8; border-top:2px solid var(--line); padding:8px 10px !important;
  vertical-align:middle;}
.cmp-grp td:first-child b{display:block; font-size:11px; font-weight:800; text-transform:uppercase;
  letter-spacing:.07em; color:var(--ink);}
.cmp-grp td:first-child span{display:block; font-size:11px; color:var(--muted); margin-top:2px;
  text-transform:none; letter-spacing:0; font-weight:400; line-height:1.35;}
.cmp-grpcol{text-align:right; border-left:1px solid; font-size:9.5px; font-weight:800;
  text-transform:uppercase; letter-spacing:.05em; white-space:nowrap;}
.cmp-grpcol i{display:inline-flex; align-items:center; justify-content:center; width:13px; height:13px;
  border-radius:50%; color:#fff; font-size:8px; font-weight:800; font-style:normal; margin-right:4px;
  vertical-align:-2px;}
.cmp-grpdiff{text-align:right; font-size:9.5px; font-weight:800; text-transform:uppercase;
  letter-spacing:.05em; color:var(--muted);}

/* the invest-vs-Social-Security verdict under the table */
.cmp-verdict{margin:16px 0 4px; padding:13px 16px; background:#fff; border:1px solid var(--line);
  border-left:4px solid; border-radius:10px; font-size:13.5px; line-height:1.6;}
.cmp-verdict b{color:var(--ink);}

/* ---- phone: the table becomes one card per row, each side still colour-coded ---- */
@media (max-width:760px){
  .cmp-legend{grid-template-columns:1fr; gap:10px;}
  .cmp-legnum{font-size:21px;}
  .cmp-table thead{display:none;}
  .cmp-table,.cmp-table tbody,.cmp-table tr,.cmp-table td,.cmp-table colgroup,.cmp-table col{display:block;}
  .cmp-table colgroup{display:none;}
  .cmp-row{border:1px solid var(--line); border-radius:12px; background:#fff; overflow:hidden;
    margin-bottom:9px;}
  .cmp-table tbody td{border-top:none; width:auto !important;}
  .cmp-l{padding:11px 13px 9px !important; background:#FCFAF4; border-bottom:1px solid var(--line);}
  .cmp-cell{display:flex !important; align-items:baseline; justify-content:space-between;
    text-align:right; border-left:4px solid; padding:9px 13px !important; white-space:normal;}
  .cmp-cell::before{content:attr(data-lab); font-size:11px; font-weight:800; text-transform:uppercase;
    letter-spacing:.05em; opacity:.85;}
  .cmp-side-a::before{color:#3B5A7A;}
  .cmp-side-b::before{color:#6A4A78;}

  .cmp-d{display:flex !important; align-items:baseline; justify-content:space-between;
    padding:8px 13px !important; background:#FBF9F3; border-top:1px solid var(--line);}
  .cmp-d::before{content:attr(data-lab); font-size:11px; font-weight:800; text-transform:uppercase;
    letter-spacing:.05em; color:var(--muted);}
  .cmp-grp{margin:18px 0 9px;}
  .cmp-grp td{background:transparent !important; border-top:none !important; padding:0 2px !important;}
  .cmp-grpcol,.cmp-grpdiff{display:none !important;}
  .cmp-grp td:first-child b{font-size:12px;}
  .cmp-big .cmp-v{font-size:17px;}
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
.planner.guided-mode #sec-statement{order:65;}
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
.jumpnav-prog{display:block; height:3px; background:#EFEAE0; border-radius:2px; margin-top:4px; overflow:hidden;}
.jumpnav-prog i{display:block; height:100%; background:#C98B4B; transition:width .3s;}
.jumpnav-active .jumpnav-prog{background:rgba(255,255,255,.25);}
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
.stats > .stat{display:flex; flex-direction:column; justify-content:center;}
.stats > .stat > .stat-label{margin-bottom:8px;}
.stats > .stat-col > .stat{justify-content:flex-start;}
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
.strip{display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:14px; margin-bottom:28px;}
.strip-lede{margin-top:4px;}
.strip-lede .strip-year{background:#F4F8F6; border-color:#C9DED4;}
.strip-lede .strip-year .strip-v{font-size:30px; color:#2F7A61;}
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
.one-up{display:grid; grid-template-columns:1fr; gap:14px; margin-bottom:14px;}
.two-up .card{margin-bottom:24px;}

/* table */
.table-wrap{overflow-x:auto; max-width:100%; -webkit-overflow-scrolling:touch;}
.card,.job2,.stats,.residency-grid{min-width:0;}
.planner{overflow-x:hidden;}
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
.wf{display:flex; flex-direction:column;}
.wf-row{display:grid; grid-template-columns:180px 1fr 120px; gap:13px; align-items:center;
  padding:11px 0; border-bottom:1px dotted var(--line);}
.wf-row:last-child{border-bottom:0;}
.wf-k{font-size:13.5px; color:var(--muted); font-weight:500;}
.wf-track{height:17px; background:#F1EDE3; border-radius:5px; overflow:hidden;}
.wf-bar{height:100%; border-radius:5px; transition:width .2s;}
.wf-out{background:#D9A9A2;}
.wf-v{font-family:'Fraunces',serif; font-size:16px; font-weight:700; text-align:right;}
.wf-final{border-top:2px solid var(--ink); border-bottom:0; padding-top:13px; margin-top:4px;}
.wf-final .wf-k{color:var(--ink); font-weight:700; font-size:15px;}
.wf-final .wf-v{font-size:21px;}
@media (max-width:780px){
  .wf-row{grid-template-columns:1fr auto; gap:2px 10px; padding:12px 0;}
  .wf-k{grid-area:1 / 1 / 2 / 2; align-self:baseline;}
  .wf-v{grid-area:1 / 2 / 2 / 3; align-self:baseline;}
  .wf-track{grid-area:2 / 1 / 3 / 3; margin-top:5px;}
}

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
  .controls,.two-up,.goal-body,.job2-body,.residency-grid,.funnel-input-grid,.funnel-score-row,.funnel-target-grid{grid-template-columns:1fr;}
  /* two-up rather than one: eight full-width stat cards was most of the Income
     section's height on a phone, for numbers that read fine at half the width */
  .stats,.strip{grid-template-columns:1fr 1fr; gap:10px;}
  .stats > .stat-big, .stats > .statpend{grid-column:1 / -1;}
  .stats > .stat-col{grid-column:1 / -1; display:grid; grid-template-columns:1fr 1fr; gap:10px;}
  .stat-col{flex-direction:row;}
  .strip-cell{padding:12px 14px;}
  .strip-v{font-size:20px; margin-top:6px;}
  .tabs{grid-template-columns:1fr 1fr;}
  .tab{padding:12px 14px;}
  .city-picker{grid-template-columns:1fr;}
  .exp-row{grid-template-columns:1fr 110px 28px; gap:10px;}
  .exp-bar{display:none;}
  .exp-yr{display:none;}
  .wf-k{font-size:12.5px;}
  .card-head-row{flex-direction:column;}
  .pay-grid{grid-template-columns:repeat(2,1fr);}
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