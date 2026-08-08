#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""therapist-working-remotely-california.html

The residency comparison, given the page it has wanted since the migration plan
was written. The tax page keeps a THREE-ROW teaser that links here; two pages
carrying the same eight-row table would be near-duplicate content and would
split whatever ranking either earns.

The lead is not the tax. It is the Board's own answer:

    "Can a California licensee while out-of-state provide telehealth services
     to a client located in California?"  -- Yes.

That is the most linkable fact this site holds, it is the thing people actually
search for, and it is buried three sections down on the tax page. Here it is the
h1's job.

Engine: _engine_core.js + _residency_core.js, both lifted from mock/tax. Parity
with the retired app.js was asserted to the cent across 42 comparisons before
that file was removed.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
TAXDIR = os.path.join(HERE, "..", "tax")
CH = os.path.join(HERE, "..", "amft")

SITE = "https://therapistsupport.org"
SLUG = "therapist-working-remotely-california.html"
TITLE = ("Can a California Therapist Work Remotely? The Board says yes — "
         "the tax is the catch")
DESC = ("A California-licensed therapist may provide telehealth to California clients "
        "from outside the state — the BBS has answered this directly. What it costs "
        "is the other question: the same practice priced against eight places, on your "
        "own profit, with the US tax that follows your passport.")

chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
chrome_ftr = open(os.path.join(CH, "_chrome_ftr.txt")).read()

# no nav entry of its own yet, so nothing is marked current
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r"\1", chrome_hdr)

CORE = open(os.path.join(TAXDIR, "_engine_core.js")).read()
RESID = open(os.path.join(TAXDIR, "_residency_core.js")).read()

# ------------------------------------------------------------------ CSS ----
CSS = """
.rw{--paper:#FBF9F3;--white:#fff;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
  --field:#FBF6E9;--fieldline:#E4D9BE;--pine:#2C6350;--gold:#B08430;--pop:#F6C560;
  --pos:#3F9577;--neg:#B5483F;--indigo:#4B3B93;
  background:var(--white);color:var(--ink);font-family:Inter,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased}
.rw *,.rw *::before,.rw *::after{box-sizing:border-box}
.rwwrap{max-width:1020px;margin:0 auto;padding:0 24px}
.rwnarrow{max-width:740px}
@media (max-width:520px){.rwwrap{padding:0 18px}}
.rw h1,.rw h2,.rw h3{font-family:Fraunces,Georgia,serif;font-weight:700;
  letter-spacing:-.015em;line-height:1.1;margin:0 0 .45em}
.rweyebrow{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;margin:0 0 14px}

/* hero. Dark, because the answer in it is the reason to be here. */
/* BAND, not slab. Measured before this change: the hero was 716px — 80% of a
   900px viewport — and the first input a reader could touch sat at y=1748, more
   than twice as far down as any other page on the site. Seven stacked text
   blocks, nothing operable, and the right half of the band empty. This is the
   same treatment mock/cola already carries as "Option 3", for the same reason:
   orientation still does its whole job, in about a third of the height, with
   the proof figures beside the copy instead of below it. */
.rwband{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(300px,.9fr);
  gap:clamp(22px,3.4vw,52px);align-items:center}
.rwhero{background:linear-gradient(160deg,#2C6350 0%,#1F4C3C 70%,#1A4234 100%);
  color:#F4F1E8;padding:clamp(20px,2.4vw,30px) 0 clamp(20px,2.4vw,30px)}
.rwhero .rweyebrow{color:#9FC4B4}
.rwhero h1{font-size:clamp(24px,2.6vw,34px);color:#FFFDF6;max-width:22ch;
  margin-bottom:.28em}
.rwhero h1 em{font-style:normal;color:var(--pop)}
.rwdeck{font-size:clamp(14.6px,1.05vw,16px);line-height:1.55;color:#C9DED5;
  max-width:56ch;margin:0 0 14px}
/* NOT .rwcite — that name is already used further down this same stylesheet by
   the footnote rows, which are `display:grid;grid-template-columns:34px
   minmax(0,1fr)`. Reusing it dropped the quote into a 34px footnote-number
   column and wrapped it one character per line, 285px tall. Declared later, it
   won. The chrome-collision check below did not catch it because the clash was
   with this page's OWN css, not the chrome.
   Demoted. It was a 21px italic pull-quote occupying the middle of the hero,
   and it RESTATED the headline — "The Board says yes", then a quote whose whole
   point is that the Board says yes. It is a citation, so it now looks like one. */
.rwsrc{border-left:3px solid var(--pop);padding:2px 0 2px 12px;margin:12px 0 0;
  max-width:60ch;font-size:12.4px;line-height:1.55;color:#9FC4B4}
.rwsrc b{font-weight:400;font-style:italic;color:#C9DED5}
.rwquote{border-left:4px solid var(--pop);padding:4px 0 4px 18px;margin:0 0 26px;
  max-width:56ch}
.rwquote b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(17px,1.6vw,21px);
  font-weight:400;font-style:italic;line-height:1.35;color:#FFFDF6;margin-bottom:8px}
.rwquote span{display:block;font-size:13px;color:#9FC4B4}
.rwcta{display:inline-flex;align-items:center;min-height:50px;padding:0 24px;
  border-radius:999px;background:var(--pop);color:#1B4536;font-weight:700;font-size:16px;
  text-decoration:none}
.rwcta:hover{background:#FFD37A}

/* Figure styles are scoped to the ROWS (.rwbig > div > b), never a bare
   `.rwbig b`. A bare descendant selector is exactly what broke the
   cost-of-living hero: it also matched the <b> inside the worked-example
   paragraph, which then inherited white-space:nowrap at 22px and rendered
   406px wide in a 390px viewport. See claude/cola-hero-overflow.md. */
.rwbig{display:grid;gap:2px 0;margin:0;padding:16px 20px;min-width:0;
  background:rgba(0,0,0,.20);border:1px solid rgba(255,255,255,.14);border-radius:14px}
.rwbig > div{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
  min-width:0;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.12)}
.rwbig > div:last-of-type{border-bottom:0}
.rwbig > div > b{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2vw,27px);
  line-height:1;color:var(--pop);white-space:nowrap;order:2}
.rwbig > div > em{font-style:normal;font-size:12.4px;color:#C9DED5;line-height:1.4;
  max-width:24ch;order:1}
.rweg{grid-column:1/-1;margin:11px 0 0;font-size:12px;line-height:1.5;color:#9FC4B4}
.rweg b{color:#DCEAE3;font-weight:600}

@media (max-width:900px){
  .rwband{grid-template-columns:minmax(0,1fr);gap:18px}
}
@media (max-width:560px){
  .rwhero h1{font-size:23px;line-height:1.14}
  .rwdeck{font-size:14.4px;margin-bottom:12px}
  .rwbig{padding:12px 14px}
  .rwbig > div{display:block}
  .rwbig > div > b{white-space:normal;display:block;margin-bottom:2px}
  .rwbig > div > em{max-width:none;display:block}
  /* One figure above the fold on a short phone; the other two are a scroll
     away. Same call cola's Option 3 makes, for the same reason — the band only
     helps if it is actually shorter than what it replaced. */
  .rwbig > div:nth-of-type(n+2){display:none}
  .rweg{display:none}
  .rwsrc{font-size:11.8px;margin-top:10px}
}

.rwsec{padding:clamp(38px,5vw,68px) 0}
.rwsec.rwpaper{background:var(--paper);border-top:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.rwsec h2{font-size:clamp(24px,2.6vw,34px)}
.rwlede{font-size:16.5px;line-height:1.66;color:var(--muted);max-width:64ch;margin:0 0 26px}
.rw p{margin:0 0 1em}
.rw a{color:var(--pine)}

/* the inputs */
.rwform{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;
  margin:0 0 18px}
.rwf{display:block;background:var(--field);border:1.5px solid var(--fieldline);
  border-radius:12px;padding:9px 13px 11px;min-height:60px}
.rwf:focus-within{border-color:var(--gold);box-shadow:0 0 0 3px rgba(176,132,48,.16)}
.rwf em{display:block;font-style:normal;font-size:9px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:#7C766A;margin-bottom:3px}
.rwf span{display:flex;align-items:baseline;gap:3px;font-family:Fraunces,Georgia,serif;
  font-weight:600;font-size:19px}
.rwf input,.rwf select{width:100%;min-width:0;background:none;border:0;padding:0;
  font:inherit;color:inherit;outline:none;-moz-appearance:textfield}
.rwf input::-webkit-outer-spin-button,.rwf input::-webkit-inner-spin-button{
  -webkit-appearance:none;margin:0}
.rwf input::placeholder{font-style:italic;font-weight:400;color:#BDB6A6;opacity:1}
.rwf select{font-size:15px;cursor:pointer;font-family:Inter,sans-serif}

/* the ranked rows - same component as the tax teaser, own prefix */
.rwrow{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(90px,1.4fr) minmax(0,124px);
  gap:14px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}
.rwrow:first-child{border-top:1px solid var(--line)}
.rwrow.rwhome{background:#F4F1E7;border-radius:8px;padding-left:10px;padding-right:10px}
.rwname b{display:block;font-size:15.5px;font-weight:700;line-height:1.25}
.rwname b i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:10px;
  font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--pine);
  border:1px solid var(--pine);border-radius:999px;padding:2px 7px;margin-left:6px;
  vertical-align:2px}
.rwname em{display:block;font-style:normal;font-size:12.4px;line-height:1.45;
  color:var(--muted);margin-top:3px}
.rwbar{height:26px;background:#EDEAE0;border-radius:6px;overflow:hidden}
.rwbar span{display:block;height:100%;background:var(--pine);border-radius:6px}
.rwhome .rwbar span{background:var(--gold)}
.rwfig{text-align:right}
.rwfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:19px;line-height:1}
/* NOT .rwtaxline or anything already used — checked against the stylesheet
   first, after .rwcite taught me that lesson the hard way. */
.rwfig .rwtax{display:block;font-family:'IBM Plex Mono',monospace;font-size:11.2px;
  color:var(--muted);margin-top:3px;white-space:nowrap}
.rwfig em{display:block;font-style:normal;font-size:11.6px;margin-top:4px}
.rwfig .rwup{color:var(--pos);font-weight:600}
.rwfig .rwdn{color:var(--neg)}
.rwfig .rwz{color:var(--muted)}
@media (max-width:700px){
  .rwrow{grid-template-columns:minmax(0,1fr) auto;gap:6px 12px}
  .rwbar{grid-column:1/-1;height:18px}
}
.rwsum{font-size:13px;line-height:1.6;color:var(--muted);margin:14px 0 0}

.rwcard{background:var(--white);border:1px solid var(--line);border-top:3px solid var(--pine);
  border-radius:14px;padding:clamp(20px,2.4vw,28px);margin:0 0 18px}
.rwcard[data-a="gold"]{border-top-color:var(--gold)}
.rwcard[data-a="brick"]{border-top-color:#8E4B45}
.rwcard h3{font-size:clamp(19px,1.9vw,24px)}
.rwcard p{font-size:15.6px;line-height:1.65;color:#3A362E}
.rwcard p:last-child{margin-bottom:0}
.rwpull{background:#F1F7F4;border-left:4px solid var(--pos);border-radius:0 10px 10px 0;
  padding:14px 16px;margin:0 0 1em;font-size:15px;line-height:1.6}
.rwwarn{background:#FBF1F0;border-left:4px solid var(--neg);border-radius:0 10px 10px 0;
  padding:14px 16px;margin:0 0 1em;font-size:15px;line-height:1.6}
.rwfine{font-size:13.4px;line-height:1.6;color:var(--muted)}
.rwcites{border-top:1px solid var(--line);padding-top:22px;margin-top:32px}
.rwcites h3{font-size:17px}
.rwcite{display:grid;grid-template-columns:34px minmax(0,1fr);gap:6px;padding:9px 0;
  border-bottom:1px solid var(--line);font-size:13.6px;line-height:1.55}
.rwcite b{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--gold)}
.rw :focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:6px}
"""

_bare = set(re.findall(r"^\.([A-Za-z][\w-]*)\s*\{", CSS, re.M))
_chrome = set(re.findall(r"\.([A-Za-z][\w-]*)", chrome_css))
assert not (_bare & _chrome), "collides with the chrome: %s" % sorted(_bare & _chrome)

# The check above only looks OUTWARD, at the chrome. `.rwcite` was invented for
# the hero while this same stylesheet already used it for footnote rows — no
# error, no warning, just a quote rendered one character per line in a 34px
# column. Ordinary re-declaration is fine and common (overrides), so flag only
# the case that actually hurts: the same bare class declared twice with
# DIFFERENT `display` values, which means two incompatible layouts share a name.
_disp = {}
for _sel, _body in re.findall(r"^\.([A-Za-z][\w-]*)\s*\{([^}]*)\}", CSS, re.M):
    _d = re.search(r"(?:^|;)\s*display\s*:\s*([\w-]+)", _body)
    if _d:
        _disp.setdefault(_sel, set()).add(_d.group(1))
_twoways = sorted(k for k, v in _disp.items() if len(v) > 1)
assert not _twoways, (
    "these classes are declared with conflicting display values, so two "
    "different layouts are sharing one name: %s" % _twoways)

# ------------------------------------------------------------------- JS ----
JS = r"""
var S = blank();
S.weeksOff = 2; S.filing = "single"; S.billingPct = 0;
S.expMonth = "";
var KEYS = ["rate","sessions","weeksOff","expMonth","filing"];

function $(id){ return document.getElementById(id); }
function money(v){ if (!isFinite(v)) return "—";
  var n = Math.round(v);
  return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US"); }
function esc(s){ return String(s == null ? "" : s)
  .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

/* One monthly figure rather than twelve categories: this page is not the
   simulator and does not pretend to be. It maps into misc so compute() sees a
   real cost base, and health cover stays out of it because compute() treats
   that as a Schedule 1 adjustment rather than a Schedule C expense. */
function sync(){
  EXPENSES.forEach(function(e){ S.exp[e[0]] = ""; });
  S.exp.misc = num(S.expMonth);
}

var PLACES = [
  {k:"uae",        name:"Dubai, UAE",          note:"9% corporate tax above AED 375,000, no personal income tax — and the US bill it does not shelter"},
  {k:"pittsburgh", name:"Pittsburgh, PA",      note:"PA flat 3.07%, city and school EIT 3%, $52 local services tax"},
  {k:"california", name:"California",          note:"where you are now"},
  {k:"brisbane",   name:"Brisbane, Australia", note:"resident rates plus the 2% Medicare levy"},
  {k:"nyc",        name:"New York City",       note:"state and city income tax, the unincorporated business tax, and the MCTMT"},
  {k:"berlin",     name:"Berlin, Germany",     note:"§32a EStG income tax, statutory health cover, solidarity surcharge"},
  {k:"portugal",   name:"Lisbon, Portugal",    note:"Categoria B simplified regime — taxed on 75% of GROSS, expenses not separately deducted"},
  {k:"france",     name:"Bordeaux, France",    note:"cotisations sociales plus the income tax scale"}
];

function draw(){
  sync();
  var live = num(S.rate) > 0 && num(S.sessions) > 0;
  var out = $("rows"), sum = $("sum"), head = $("headline");
  if (!live){
    out.innerHTML = "";
    sum.innerHTML = "Put a rate and a caseload in above and the eight places price "
      + "themselves against your own practice.";
    head.textContent = "—";
    writeHash();
    return;
  }
  var c = compute(S, 0);
  var expC = Math.max(0, c.expenses - c.sehi);
  var r = RESID.computeResidency(c.gross, expC);
  /* Keep the whole result, not just netUSD. Every place already returns taxUSD
     and it was being thrown away — so the table showed what each place LEAVES
     you without showing what it TAKES, which is the only thing that differs.
     Profit is identical everywhere by the page's own premise: same practice,
     same clients, same profit. Tax is the entire story. */
  var res = {
    california: {netUSD: c.net, taxUSD: c.totalTax},
    nyc:        RESID.computeNYC(c.gross, expC, 0, S.filing, c.sehi),
    pittsburgh: RESID.computePittsburgh(c.gross, expC, 0, S.filing, c.sehi),
    france:     RESID.computeFrance(c.gross, expC),
    uae:        RESID.computeUAE(c.gross, expC, S.filing),
    brisbane:   RESID.computeBrisbane(c.gross, expC),
    berlin:     r.berlin,
    portugal:   r.portugal
  };
  var net = {};
  PLACES.forEach(function(p){ net[p.k] = res[p.k].netUSD; });
  var profit = c.profit;
  var rows = PLACES.map(function(p){
    return {k:p.k, name:p.name, note:p.note, net:res[p.k].netUSD,
            tax:res[p.k].taxUSD,
            rate:profit > 0 ? res[p.k].taxUSD / profit : NaN,
            delta:res[p.k].netUSD - res.california.netUSD};
  }).sort(function(a,b){ return b.net - a.net; });
  var top = Math.max.apply(null, rows.map(function(x){ return x.net; }));
  var better = rows.filter(function(x){ return x.delta > 0; }).length;
  var best = rows[0];

  head.textContent = best.k === "california" ? money(net.california)
    : "+" + money(best.delta);

  /* Mirror the verdict into the hero from the SAME computation, so the two can
     never disagree. The worked example hides the moment the figures are real. */
  var hb = $("hbest"), hc = $("hcount"), hn = $("hname"), he = $("hbeg");
  if (hb) hb.textContent = best.k === "california" ? money(net.california)
                                                   : "+" + money(best.delta);
  if (hc) hc.textContent = better + " of " + rows.length;
  if (hn) hn.textContent = best.name;
  if (he) he.hidden = true;
  $("headsub").textContent = best.k === "california"
    ? "California already keeps you the most of the eight"
    : "the most any of the eight beats California by, before anything but tax";

  out.innerHTML = rows.map(function(x){
    var home = x.k === "california";
    /* The bar is the SPLIT, not a ranking. Every place starts from the same
       profit — that is the page's premise — so a bar scaled to the biggest net
       only re-stated the number printed beside it. Scaled to profit instead,
       the filled part is what you keep and the empty part is what that place
       takes, and the eight become directly comparable at a glance. */
    var w = profit > 0 ? Math.max(2, x.net / profit * 100) : 2;
    return '<div class="rwrow' + (home ? " rwhome" : "") + '">'
      + '<div class="rwname"><b>' + esc(x.name) + (home ? ' <i>you are here</i>' : "")
      + '</b><em>' + esc(x.note) + '</em></div>'
      + '<div class="rwbar" title="' + esc(money(x.net) + " kept, " + money(x.tax)
          + " taken, from " + money(profit) + " of profit")
      + '"><span style="width:' + w.toFixed(1) + '%"></span></div>'
      + '<div class="rwfig"><b>' + money(x.net) + '</b>'
      + '<em class="rwtax">&minus;' + money(x.tax)
      + (isFinite(x.rate) ? " tax &middot; " + Math.round(x.rate * 100) + "%" : " tax")
      + '</em>'
      + '<em class="' + (home ? "rwz" : x.delta > 0 ? "rwup" : "rwdn") + '">'
      + (home ? "your baseline"
             : (x.delta > 0 ? "+" : "−") + money(Math.abs(x.delta)) + " a year")
      + "</em></div></div>";
  }).join("");

  sum.innerHTML = "Same practice, same clients, same <b>" + money(c.profit)
    + "</b> of profit before tax. " + (better === 0
        ? "<b>Not one of the seven leaves you better off.</b>"
        : better === 1 ? "<b>One of the seven leaves you better off.</b>"
        : "<b>" + better + " of the seven leave you better off.</b>")
    + " This year's rates on your own numbers, converted at today's rough exchange "
    + "rates. None of it prices the cost of living once you get there.";
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
  raw.split("&").forEach(function(pair){
    var i = pair.indexOf("="); if (i < 0) return;
    var k = pair.slice(0, i), v = decodeURIComponent(pair.slice(i + 1));
    if (KEYS.indexOf(k) >= 0) S[k] = v;
    /* the simulator and the tax page both send twelve categories; collapse
       them into the single monthly box this page asks for */
    else if (k.indexOf("exp_") === 0) S.exp[k.slice(4)] = v;
  });
  var t = 0, any = false;
  EXPENSES.forEach(function(e){
    if (S.exp[e[0]] !== "" && S.exp[e[0]] != null){ t += num(S.exp[e[0]]); any = true; }
  });
  if (any && !S.expMonth) S.expMonth = Math.round(t);
}

function bind(id, key){
  var el = $(id); if (!el) return;
  el.value = S[key];
  el.addEventListener("input", function(){ S[key] = el.value; draw(); });
  el.addEventListener("change", function(){ S[key] = el.value; draw(); });
}
readHash();
KEYS.forEach(function(k){ bind("i-" + k, k); });
draw();
"""

# ---------------------------------------------------------------- content --
CITES = [
 (1, "California Board of Behavioral Sciences, telehealth FAQ",
  "https://www.bbs.ca.gov/pdf/publications/telehealth_faq.pdf",
  "&#8220;Can a California licensee while out-of-state provide telehealth services to a "
  "client located in California?&#8221; &mdash; the Board&#8217;s answer is yes, subject "
  "to a current and active licence and 16 CCR &#167;1815.5."),
 (2, "California Code of Regulations, title 16, section 1815.5",
  "https://www.law.cornell.edu/regulations/california/16-CCR-1815.5",
  "Standards of practice for telehealth. Requires the client&#8217;s full name and present "
  "location to be obtained verbally and documented at the start of each session; imposes "
  "no requirement about the licensee&#8217;s own location."),
 (3, "IRS, self-employment tax for businesses abroad",
  "https://www.irs.gov/individuals/international-taxpayers/self-employment-tax-for-businesses-abroad",
  "&#8220;You must take all your self-employment income into account in figuring your net "
  "earnings from self-employment, even if all, or a portion of, gross income was excluded "
  "because of the foreign earned income exclusion.&#8221;"),
 (4, "IRS, foreign tax credit",
  "https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit",
  "The mechanism that absorbs most of the US bill in a high-tax country, and has nothing "
  "to absorb in a low-tax one."),
 (5, "IRS Revenue Procedure 2025-32", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
  "2026 federal rate schedules and the standard deduction used throughout."),
 (6, "California Franchise Tax Board, 2025 540 tax rate schedules",
  "https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf",
  "The California schedules. The FTB has not published 2026 rates, and its own 2026 Form "
  "540-ES instructs filers to use the 2025 tables."),
]

FIELDS = [
    ("rate", "Your session rate", "$", 'type="number" min="0" step="5" placeholder="200"'),
    ("sessions", "Sessions a week", "", 'type="number" min="0" step="1" placeholder="25"'),
    ("weeksOff", "Weeks off a year", "wks", 'type="number" min="0" max="30" step="1"'),
    ("expMonth", "Monthly running costs", "$/mo", 'type="number" min="0" step="50" placeholder="3548"'),
]

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s" />
<link rel="canonical" href="%(site)s/%(slug)s" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:type" content="article" />
<meta property="og:url" content="%(site)s/%(slug)s" />
%(head)s
<style>%(chrome_css)s</style>
<style>%(css)s</style>
<script type="application/ld+json">%(ld)s</script>
</head><body>
%(hdr)s
<main class="rw">
%(body)s
</main>
%(ftr)s
<script>%(navjs)s</script>
<script>
%(engine)s
%(resid)s
%(js)s
</script>
</body></html>
"""


def build():
    B = []
    A = B.append

    A('<section class="rwhero"><div class="rwwrap"><div class="rwband">')
    A('<div>')
    A('<p class="rweyebrow">California &middot; telehealth &middot; 2026 rates</p>')
    A('<h1>Can a California therapist work remotely? <em>The Board says yes.</em></h1>')
    A('<p class="rwdeck">The interesting question is not whether you may &mdash; it is what '
      'it costs. The same practice, same clients, same profit, priced against eight places '
      'on your own numbers.</p>')
    A('<a class="rwcta" href="#compare">See what each place leaves you &darr;</a>')
    A('<p class="rwsrc"><b>&ldquo;Can a California licensee while out-of-state provide '
      'telehealth services to a client located in California?&rdquo;</b> Board of '
      'Behavioral Sciences telehealth FAQ &mdash; and the answer it gives is '
      'yes.<sup>[1]</sup></p>')
    A('</div>')
    A('<div class="rwbig">'
      '<div><b id="hbest">+$18,700</b><em>the most any of the eight beats California by</em></div>'
      '<div><b id="hcount">5 of 8</b><em>places that leave you more than California</em></div>'
      '<div><b id="hname">Dubai</b><em>the best of them, on your numbers</em></div>'
      '<p class="rweg" id="hbeg"><b>Worked example</b> &mdash; a $200 hour, 25 sessions a '
      'week, filing single. Put your own numbers in below and all three become yours.</p>'
      '</div>')
    A('</div></div></section>')

    # --- the licensure answer, in full
    A('<section class="rwsec"><div class="rwwrap rwnarrow">')
    A('<h2>Your licence is not the obstacle</h2>')
    A('<div class="rwcard"><h3>What the Board actually says</h3>')
    A('<p>The Board of Behavioral Sciences was asked this directly, and answered: '
      '<b>yes</b> &mdash; if the licence is current and active, the case is appropriate '
      'for telehealth, and the licensee follows 16 CCR &#167;1815.5.<sup>[1]</sup></p>')
    A('<p>That regulation sets standards for the session itself, including verbally '
      'obtaining and documenting <b>the client&rsquo;s</b> full name and present location '
      'at the start of every one. It sets no requirement at all about where the '
      '<em>licensee</em> is.<sup>[2]</sup></p>')
    A('<p class="rwpull"><b>Which puts the constraint somewhere other than where most '
      'people assume.</b> Your licence covers clients in California, so your clients stay '
      'in California. You are the one who moves.</p>')
    A('<p>What then binds is not California. It is the country you move to: its own rules '
      'about practising a regulated profession on its soil, and whether your visa permits '
      'you to work at all. Neither is a Board question, and neither is priced below.</p>')
    A('</div></div></section>')

    # --- the comparison
    A('<section class="rwsec rwpaper" id="compare"><div class="rwwrap">')
    A('<h2>What eight places would leave you</h2>')
    A('<p class="rwlede">Four numbers. Everything below is computed from them &mdash; '
      'nothing is saved, and your setup lives in the address bar.</p>')
    A('<div class="rwform">')
    for fid, lab, unit, attrs in FIELDS:
        A('<label class="rwf"><em>%s</em><span>%s<input id="i-%s" %s></span></label>'
          % (lab, ("<i style='font-style:normal'>%s</i>" % unit) if unit == "$" else "",
             fid, attrs))
    A('<label class="rwf"><em>Filing status</em><span><select id="i-filing">'
      '<option value="single">Single</option><option value="hoh">Head of household</option>'
      '<option value="mfj">Married, filing jointly</option></select></span></label>')
    A('</div>')
    A('<div class="rwcard" data-a="gold" style="margin-bottom:22px">'
      '<p class="rweyebrow" style="color:#6E695E">The biggest gap</p>'
      '<p style="font-family:Fraunces,Georgia,serif;font-size:38px;line-height:1;margin:0">'
      '<span id="headline">&mdash;</span></p>'
      '<p class="rwfine" id="headsub" style="margin:8px 0 0">Put a rate and caseload in '
      'above.</p></div>')
    A('<div id="rows"></div>')
    A('<p class="rwsum" id="sum"></p>')
    A('</div></section>')

    # --- the tax half
    A('<section class="rwsec"><div class="rwwrap rwnarrow">')
    A('<h2>The tax follows the passport, not the address</h2>')
    A('<div class="rwcard" data-a="brick">')
    A('<p>The United States taxes citizens on worldwide income wherever they live. In a '
      'high-tax country the foreign tax credit absorbs most of the US bill, which is why '
      'Berlin and Bordeaux above land close to their local tax and not much above it. In a '
      'low-tax country there is nothing to credit, so the US bill arrives in '
      'full.<sup>[4]</sup></p>')
    A('<p class="rwwarn"><b>And the foreign earned income exclusion &mdash; the thing '
      'everyone reaches for first &mdash; does not touch self-employment tax.</b> The IRS '
      'is explicit: you must count all your self-employment income even if the exclusion '
      'removed it from your gross income.<sup>[3]</sup> A self-employed therapist in Dubai '
      'still owes the full 15.3% on the way through, on top of whatever the UAE '
      'charges.</p>')
    A('<p>Which is why the top of that list is a smaller win than &ldquo;no income '
      'tax&rdquo; would suggest.</p>')
    A('</div>')
    A('<p class="rwfine"><b>This is a comparison, not a plan.</b> It prices tax and nothing '
      'else: not visas, not the right to work, not health cover, not what a flat costs in '
      'Lisbon against Fresno, not currency risk, not the time-zone question, and not '
      'whether a treaty changes your position. Treat it as a reason to ask a cross-border '
      'accountant a better question.</p>')
    A('</div></section>')

    # --- where next
    A('<section class="rwsec rwpaper"><div class="rwwrap rwnarrow">')
    A('<h2>Before any of this matters</h2>')
    A('<p class="rwlede">Every figure here is downstream of one number: what the practice '
      'clears before tax. If that is a guess, this page is a guess about a guess.</p>')
    A('<a class="rwcta" href="practice-simulator.html" '
      'style="background:#2C6350;color:#fff">Build the profit properly &rarr;</a>')
    A('</div></section>')

    # --- sources
    A('<section class="rwsec"><div class="rwwrap rwnarrow"><div class="rwcites">')
    A("<h3>Sources</h3>")
    for n, cite, url, note in CITES:
        A('<div class="rwcite"><b>[%d]</b><div><a href="%s" target="_blank" '
          'rel="noopener noreferrer">%s</a> &mdash; %s</div></div>' % (n, url, cite, note))
    A('<p class="rwfine" style="margin-top:16px"><b>Estimates, not advice.</b> This models '
      'a California-resident sole proprietor with no other household income and no '
      'itemised deductions, and prices each location on its headline resident rules. It '
      'ignores treaty positions, transition years, exit taxes, state residency-severance '
      'rules and anything specific to you. Talk to a cross-border accountant before acting '
      'on it.</p>')
    A('</div></div></section>')
    return "\n".join(B)


LD = [
 {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{
   "@type": "Question",
   "name": "Can a California-licensed therapist provide telehealth from outside California?",
   "acceptedAnswer": {"@type": "Answer", "text":
     "Yes. The California Board of Behavioral Sciences states that a California licensee "
     "who is out of state may provide telehealth services to a client located in "
     "California, provided the licence is current and active, the case is appropriate for "
     "telehealth, and the licensee follows 16 CCR section 1815.5."}}]},
 {"@context": "https://schema.org", "@type": "WebPage", "name": TITLE,
  "url": SITE + "/" + SLUG, "description": DESC,
  "isPartOf": {"@type": "WebSite", "name": "Therapist Support", "url": SITE + "/"},
  "dateModified": "2026-08-02"},
]


def main():
    html = SHELL % dict(title=TITLE, desc=DESC, site=SITE, slug=SLUG,
                        head=chrome_head, chrome_css=chrome_css, css=CSS,
                        ld=json.dumps(LD, separators=(",", ":")),
                        hdr=chrome_hdr, body=build(), ftr=chrome_ftr,
                        navjs=chrome_js, engine=CORE, resid=RESID, js=JS)
    assert html.count("<h1") == 1
    assert html.count("<footer") == 1
    assert 'href="terms.html"' in html and 'href="privacy.html"' in html
    assert "</script>" not in JS and "</script>" not in RESID
    for n, _, _, _ in CITES:
        assert "[%d]</b>" % n in html
    open(os.path.join(HERE, SLUG), "w", encoding="utf-8").write(html)
    print("wrote %s  %d kB" % (SLUG, len(html) // 1024))


if __name__ == "__main__":
    main()
