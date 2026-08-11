#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Five doors, three ways each - the expanded stage-hub mockup set.

WHY THIS EXISTS

`ops/stage-architecture.html` argued the case for stage-based entry points and
sketched three visual directions, one per stage. The response to it was the
right question: *show me the alternatives for each door, not one option per
door, and tell me what else changes.*

So this page does three things the first one did not:

  1. TWO OR THREE RENDERED VARIANTS FOR EVERY DOOR, not one. Each variant is a
     real HTML mockup at the real proportions, not a description of one.
  2. A RECOMMENDATION PER DOOR with the trade-off written down, because a
     mockup without a recommendation just moves the decision.
  3. THE IMPACT LIST - every pass, file and guard that changes if this ships.
     That is the part that actually decides whether it is a week or a month.

WHAT CHANGED SINCE THE FIRST PROPOSAL

`/for/students/` was recorded as **Hold - 0 pages**. That is now stale: the
practicum page and the career-change page shipped on 11 August, so the student
door has content of its own plus 78 program pages behind it. Four of the five
doors can open. Only `/for/practice-owners/` still fails the test.

CSS PROVENANCE

The stylesheet is read out of `ops/stage-architecture.html` at build time
rather than copied, so the two pages cannot drift apart. Only the classes this
page adds are defined here. If that file is ever rewritten without a <style>
block this pass fails loudly rather than shipping an unstyled page.

NOT IN THE REGISTRY

This lives under `ops/`, which is outside SUBDIRS and therefore invisible to
every pass in `_dev/` - no chrome, no nav, no CSS extraction. That is
deliberate: it is a working document, it carries `noindex`, and `robots.txt`
disallows the directory.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "stage-doors.html")
UPDATED = "11 August 2026"

# --------------------------------------------------------------- extra CSS
EXTRA = """
/* ---------- stage-doors additions ---------- */
.doors{display:grid;gap:14px;margin:6px 0 4px}
@media(min-width:820px){.doors{grid-template-columns:repeat(5,1fr)}}
.door{border:2px solid var(--ink);background:var(--cream);box-shadow:4px 4px 0 var(--ink);
  padding:13px 14px}
.door .n{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--muted)}
.door h4{font-size:15px;margin:4px 0 5px}
.door .u{font-family:var(--mono);font-size:10.5px;color:var(--pine);word-break:break-all}
.door .st{display:inline-block;margin-top:8px;font-family:var(--mono);font-size:9px;
  letter-spacing:.11em;text-transform:uppercase;border:1.5px solid var(--ink);padding:3px 6px}
.door .st.go{background:var(--pine);color:#fff;border-color:var(--pine)}
.door .st.hold{background:var(--gold)}
.door .st.new{background:var(--red);color:#fff;border-color:var(--red)}

.vh{display:flex;align-items:baseline;gap:10px;margin:30px 0 6px;
  border-top:2px solid var(--ink);padding-top:14px}
.vh .tag{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.1em;
  background:var(--ink);color:var(--gold);padding:4px 8px;white-space:nowrap}
.vh h4{font-size:20px;margin:0}
.vh .rec{margin-left:auto;font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;
  text-transform:uppercase;background:var(--pine);color:#fff;padding:4px 9px;white-space:nowrap}

.tradeoff{display:grid;gap:10px;margin:10px 0 6px}
@media(min-width:760px){.tradeoff{grid-template-columns:1fr 1fr}}
.tradeoff div{border:1.5px solid var(--line);background:#fff;padding:11px 13px}
.tradeoff .lab{display:block;margin-bottom:5px}
.tradeoff p{font-size:14px;margin:0}
.tradeoff .up{border-left:4px solid var(--green)}
.tradeoff .dn{border-left:4px solid var(--red)}

.pickbox{background:var(--pine);color:#fff;border:2px solid var(--ink);
  box-shadow:5px 5px 0 var(--ink);padding:15px 18px;margin:12px 0 6px}
.pickbox .lab{color:var(--gold-on-pine)}
.pickbox h4{color:#fff;font-size:18px;margin:5px 0 6px}
.pickbox p{color:#E2EDE7;font-size:14.5px;margin:0}

/* variant-specific mockup parts */
.twoq{display:grid;gap:11px;margin:12px 0 4px}
@media(min-width:560px){.twoq{grid-template-columns:1fr 1fr}}
.qcard{border:2px solid var(--ink);background:var(--cream);box-shadow:3px 3px 0 var(--ink);
  padding:13px 14px}
.qcard h3{font-size:16px;margin:5px 0 5px}
.qcard .mini{font-size:11px;color:var(--muted);line-height:1.4}
.qcard .go{display:inline-block;margin-top:9px;font-family:var(--mono);font-size:9px;
  letter-spacing:.11em;text-transform:uppercase;background:var(--gold);
  border:1.5px solid var(--ink);padding:4px 8px}

.pricerail{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:12px 0}
.pricerail div{border:2px solid var(--ink);background:#fff;padding:10px 11px;
  box-shadow:3px 3px 0 var(--ink)}
.pricerail .v{font-family:var(--fig);font-weight:800;font-size:21px;color:var(--deep);
  line-height:1.05;margin:3px 0 2px}
.pricerail .s{font-size:10.5px;color:var(--muted);line-height:1.3}

.lookup{border:2px solid var(--ink);background:var(--gold);padding:13px 14px;
  box-shadow:3px 3px 0 var(--ink);margin-bottom:12px}
.lookup .fake{background:#fff;border:2px solid var(--ink);padding:8px 11px;
  font-size:13px;display:flex;justify-content:space-between;align-items:center;margin-top:7px}
.lookup .fake span:last-child{font-family:var(--mono);font-size:10px;color:var(--muted)}
.answer{border:2px solid var(--ink);background:#fff;padding:12px 14px;margin-top:9px;
  box-shadow:3px 3px 0 var(--ink)}
.answer .verdict{font-family:var(--sans);font-weight:800;font-size:17px;color:var(--red);
  margin:3px 0 5px}
.answer .quote{font-size:12px;font-style:italic;color:#33423A;border-left:3px solid var(--line);
  padding-left:10px;margin-top:7px}

.rulecard{border:2px solid var(--ink);background:var(--cream);padding:13px 15px;
  box-shadow:3px 3px 0 var(--ink)}
.rulecard ol{margin:7px 0 0;padding-left:19px;font-size:12px;line-height:1.5}
.rulecard li{margin-bottom:5px}
.rulecard li b{font-family:var(--sans);font-weight:700}
.rulecard .cite{font-family:var(--mono);font-size:9.5px;color:var(--muted)}

.ledger{border:2px solid var(--ink);background:#fff;padding:14px 15px;
  box-shadow:3px 3px 0 var(--ink);margin-bottom:11px}
.bar{height:26px;border:2px solid var(--ink);background:var(--cream);position:relative;
  margin:9px 0 5px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--pine)}
.bar em{position:absolute;top:0;bottom:0;width:2px;background:var(--ink)}
.bar em::after{content:attr(data-l);position:absolute;top:100%;left:-2px;
  font-family:var(--mono);font-size:8.5px;color:var(--muted);white-space:nowrap;padding-top:3px}
.gates{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:24px}
.gates div{border:1.5px solid var(--line);padding:8px 9px;font-size:10.5px;line-height:1.35}
.gates .g{font-family:var(--fig);font-weight:800;font-size:16px;color:var(--deep);display:block}
.gates .warn{border-color:var(--red);border-left-width:4px}

.thread{border:2px solid var(--ink);background:#fff;padding:11px 13px;margin-bottom:9px;
  box-shadow:3px 3px 0 var(--ink)}
.thread .q{font-family:var(--fig);font-size:16px;font-weight:700;line-height:1.25;
  color:var(--deep)}
.thread .meta{font-family:var(--mono);font-size:9.5px;letter-spacing:.09em;color:var(--muted);
  text-transform:uppercase;margin-top:4px}
.thread .a{font-size:12px;margin-top:7px;border-top:1px solid var(--line);padding-top:7px}

.clog{border-left:3px solid var(--ink);padding-left:16px;margin:10px 0 4px}
.clog .row{position:relative;padding-bottom:13px}
.clog .row::before{content:"";position:absolute;left:-22px;top:5px;width:11px;height:11px;
  background:var(--gold);border:2px solid var(--ink)}
.clog .row.old::before{background:var(--cream)}
.clog .d{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;color:var(--muted)}
.clog h4{font-size:14.5px;margin:2px 0 3px}
.clog p{font-size:12px;margin:0;color:#39473F}
.clog .app{display:inline-block;margin-top:5px;font-family:var(--mono);font-size:9px;
  letter-spacing:.1em;text-transform:uppercase;border:1.5px solid var(--ink);padding:3px 7px;
  background:var(--cream)}

.panelgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.panelgrid div{border:2px solid var(--ink);background:var(--cream);padding:11px 12px;
  box-shadow:3px 3px 0 var(--ink)}
.panelgrid .q{font-family:var(--sans);font-weight:700;font-size:13.5px;margin-bottom:3px}
.panelgrid .n2{font-family:var(--fig);font-weight:800;font-size:19px;color:var(--pine)}
.panelgrid .s{font-size:10.5px;color:var(--muted)}

.tree{font-size:12.5px}
.tree .q{border:2px solid var(--ink);background:var(--gold);padding:9px 12px;
  font-family:var(--sans);font-weight:700;margin-bottom:9px}
.tree .branch{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.tree .branch div{border:2px solid var(--ink);background:#fff;padding:9px 11px}
.tree .branch .lab{display:block;margin-bottom:3px}

.band{border:2px solid var(--ink);background:var(--cream);padding:9px 13px;
  display:flex;gap:12px;align-items:center;flex-wrap:wrap;font-size:12px}
.band .you{font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;
  background:var(--ink);color:var(--gold);padding:3px 7px;white-space:nowrap}
.band .nx{margin-left:auto;font-family:var(--mono);font-size:10px;color:var(--pine)}
.bandfoot{border:2px solid var(--ink);background:var(--pine);color:#fff;padding:13px 15px}
.bandfoot .lab{color:var(--gold-on-pine)}
.bandfoot h4{color:#fff;font-size:16px;margin:5px 0 4px}
.bandfoot p{color:#DCEAE3;font-size:12px;margin:0}
.railmock{display:grid;grid-template-columns:1fr 150px;gap:14px}
.railmock .rail{border-left:2px solid var(--line);padding-left:12px;font-size:11px}
.railmock .rail .cur{background:var(--gold);border:1.5px solid var(--ink);padding:3px 6px;
  display:block;margin:3px 0}
.railmock .rail span{display:block;color:var(--muted);padding:3px 6px}

.impact li{margin-bottom:9px}
.impact code{font-family:var(--mono);font-size:12.5px;background:#fff;
  border:1px solid var(--line);padding:1px 5px}
.risk{border:2px solid var(--red);background:#FFF6F5;padding:13px 15px;margin:12px 0}
.risk h4{color:var(--red);font-size:16px}
.risk p{font-size:14px;margin:0 0 8px}
.risk p:last-child{margin-bottom:0}
@media(max-width:700px){
  .pricerail,.gates,.panelgrid,.tree .branch{grid-template-columns:1fr 1fr}
  .railmock{grid-template-columns:1fr}
  .vh{flex-wrap:wrap}.vh .rec{margin-left:0}
}
"""

NAV = [("read", "How to read this"), ("glance", "Five doors"),
       ("deciding", "1 · Deciding"), ("students", "2 · Students"),
       ("associates", "3 · Associates"), ("licensed", "4 · Licensed"),
       ("owners", "5 · Owners"), ("shell", "The shared shell"),
       ("impact", "What else changes"), ("order", "Build order")]


# ------------------------------------------------------------------ helpers
def frame(url, inner):
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="mk"><div class="mkhead"><span class="brand">Therapist '
            'Support</span><span class="nv"><span>Calculators</span>'
            '<span>Money</span><span>Licensure</span><span>Getting paid</span>'
            '<span>Practice</span></span></div><div class="mkbody">%s</div>'
            "</div></div>" % (url, inner))


def variant(tag, title, blurb, url, inner, up, down, rec=False):
    o = ['<div class="vh"><span class="tag">%s</span><h4>%s</h4>%s</div>'
         % (tag, title, '<span class="rec">Recommended</span>' if rec else "")]
    o.append("<p>%s</p>" % blurb)
    o.append(frame(url, inner))
    o.append('<div class="tradeoff"><div class="up"><span class="lab">What it '
             "buys</span><p>%s</p></div><div class=\"dn\"><span class=\"lab\">"
             "What it costs</span><p>%s</p></div></div>" % (up, down))
    return "".join(o)


def pick(title, why):
    return ('<div class="pickbox"><span class="lab">The call</span><h4>%s</h4>'
            "<p>%s</p></div>" % (title, why))


# ============================================================ door mockups
# ---------------------------------------------------------------- deciding
D1A = """
<div class="deskhero"><span class="lab">Thinking about it</span>
<h2>Eight years, five gates, and one decision you make before you apply.</h2>
<p>The whole route, with the gates that actually stop people marked.</p></div>
<span class="lab">The route</span>
<div class="ladder">
  <div class="rung now"><h4>Choose a license<span class="pill">You are here</span></h4>
    <div class="rs">LMFT, LCSW or LPCC. Only one banks your practicum hours.</div>
    <div class="gate"><span class="lab">The gate</span>
      <div class="gv">1,300 hours</div>
      <div class="rs">bankable pre-degree on the MFT route. Zero on the other two.</div></div></div>
  <div class="rung"><h4>Get in</h4><div class="rs">78 programs &middot; $37,800&ndash;$152,340</div></div>
  <div class="rung"><h4>The degree, and the practicum inside it</h4>
    <div class="rs">2&ndash;3 years &middot; 225 client hours minimum</div></div>
  <div class="rung"><h4>Degree &rarr; registration</h4>
    <div class="rs">90 days, and Live Scan before the first hour</div></div>
  <div class="rung"><h4>3,000 hours over 104 weeks</h4><div class="rs">Two exams</div></div>
  <div class="rung"><h4>Licensed</h4><div class="rs">59,706 people are already here</div></div>
</div>
<div class="qrow"><span class="qn">&rarr;</span><span><span class="qt">Coming from
another state, or already have a license?</span><span class="qs">Different route
entirely &mdash; Path A and Path B</span></span><span class="qb">Exit here</span></div>
"""

D1B = """
<div class="deskhero"><span class="lab">Thinking about it</span>
<h2>Two decisions. Everything else follows from them.</h2>
<p>Which license you aim at, and which program you go through. The site has
real data on both.</p></div>
<div class="twoq">
  <div class="qcard"><span class="lab">Decision one</span>
    <h3>Which license?</h3>
    <p class="mini">LMFT, LCSW or LPCC. They differ on statute, not temperament
    &mdash; and only one lets your practicum count toward the 3,000.</p>
    <div class="pricerail" style="grid-template-columns:1fr 1fr 1fr;margin:9px 0 0">
      <div style="box-shadow:none;padding:7px 8px"><div class="v">1,300</div>
        <div class="s">LMFT pre-degree</div></div>
      <div style="box-shadow:none;padding:7px 8px"><div class="v">0</div>
        <div class="s">LCSW</div></div>
      <div style="box-shadow:none;padding:7px 8px"><div class="v">0</div>
        <div class="s">LPCC</div></div>
    </div>
    <span class="go">Compare the three &rarr;</span></div>
  <div class="qcard"><span class="lab">Decision two</span>
    <h3>Which program?</h3>
    <p class="mini">All 78 the Board recognizes, compared on cost, format,
    accreditation &mdash; and on who finds your practicum site, which nothing
    else publishes.</p>
    <div class="pricerail" style="grid-template-columns:1fr 1fr 1fr;margin:9px 0 0">
      <div style="box-shadow:none;padding:7px 8px"><div class="v">78</div>
        <div class="s">programs</div></div>
      <div style="box-shadow:none;padding:7px 8px"><div class="v">29</div>
        <div class="s">publish nothing</div></div>
      <div style="box-shadow:none;padding:7px 8px"><div class="v">33</div>
        <div class="s">own a clinic</div></div>
    </div>
    <span class="go">Compare all 78 &rarr;</span></div>
</div>
<span class="lab" style="display:block;margin-top:14px">Then, in order</span>
<div class="qrow"><span class="qn">01</span><span><span class="qt">What it costs,
end to end</span><span class="qs">Tuition, fees, and the years you are not
earning</span></span></div>
<div class="qrow"><span class="qn">02</span><span><span class="qt">How many people
are doing this</span><span class="qs">The pipeline grew 66% in eight
years</span></span></div>
<div class="qrow"><span class="qn">03</span><span><span class="qt">Coming from
another state?</span><span class="qs">Path A, Path B, and what does not
transfer</span></span></div>
"""

D1C = """
<div class="deskhero"><span class="lab">Thinking about it &middot; the honest total</span>
<h2>Here is the bill, before anybody sells you the vocation.</h2>
<p>Every figure below links to the source it came from. None of it is an
estimate of what <em>you</em> will pay.</p></div>
<div class="pricerail">
  <div><span class="lab">Tuition</span><div class="v">$37,800</div>
    <div class="s">to $152,340 &mdash; of the 35 that publish</div></div>
  <div><span class="lab">Years, realistically</span><div class="v">5&ndash;6</div>
    <div class="s">statutory floor is about 4</div></div>
  <div><span class="lab">Practicum year pays</span><div class="v">$0</div>
    <div class="s">and takes 12&ndash;20 hrs/week</div></div>
  <div><span class="lab">County job, top of range</span><div class="v">$106,605</div>
    <div class="s">median across 55 counties</div></div>
</div>
<div class="qrow"><span class="qn">!</span><span><span class="qt">And the part
that offsets it</span><span class="qs">PSLF ignores your license entirely, so a
county associate can be accruing qualifying payments from month
one</span></span><span class="qb">Read</span></div>
<span class="lab" style="display:block;margin-top:13px">Before you commit</span>
<div class="qrow"><span class="qn">01</span><span><span class="qt">Which license,
and why it is a statute question</span></span></div>
<div class="qrow"><span class="qn">02</span><span><span class="qt">All 78 programs,
priced</span></span></div>
<div class="qrow"><span class="qn">03</span><span><span class="qt">Eight questions
to ask an admissions office</span></span></div>
"""

# ---------------------------------------------------------------- students
D2A = """
<div class="deskhero"><span class="lab">In a program</span>
<h2>Who finds your practicum site?</h2>
<p>29 of the 78 California programs publish no answer to that anywhere. Find
yours, in their own words.</p></div>
<div class="lookup"><span class="lab">Your program</span>
  <div class="fake"><span>Alliant International University (CSPP)</span>
    <span>change &rsaquo;</span></div></div>
<div class="answer"><span class="lab">What Alliant publishes</span>
  <div class="verdict">You find it.</div>
  <p style="font-size:12px;margin:0">No approved-site list is published. The
  school still has to approve the site and hold a written agreement with it
  &mdash; that duty is theirs by statute, not yours.</p>
  <div class="quote">&ldquo;As a student of the CFT program, you are fully
  responsible in securing your practicum site.&rdquo;</div></div>
<div class="gates" style="margin-top:14px">
  <div><span class="g">3</span>guaranteed</div>
  <div><span class="g">6</span>program places you</div>
  <div><span class="g">27</span>approved-site list</div>
  <div class="warn"><span class="g">29</span>publish nothing</div>
</div>
"""

D2B = """
<div class="deskhero"><span class="lab">In a program</span>
<h2>The four deadlines between here and a registration number.</h2>
<p>This stage is defined by dates, and one of them is unforgiving.</p></div>
<div class="ladder">
  <div class="rung done"><h4>12 semester units</h4>
    <div class="rs">No hour counts before this. &sect;&thinsp;4980.43(c)(6)</div></div>
  <div class="rung now"><h4>Practicum<span class="pill">You are here</span></h4>
    <div class="rs">Enrolled in the course while you see clients &mdash; a gap of
    fewer than 90 days is allowed, once</div>
    <div class="gate"><span class="lab">Your ceiling</span><div class="gv">1,300 / 750</div>
      <div class="rs">total pre-degree hours, of which counseling plus supervision</div></div></div>
  <div class="rung"><h4>Degree awarded</h4><div class="rs">The clock starts on the
  award date, not graduation day</div></div>
  <div class="rung"><h4>90 days to be <em>received</em></h4>
    <div class="rs">Miss it and every hour between degree and registration is gone.
    Live Scan must already have been required by the workplace.</div></div>
  <div class="rung"><h4>Registration issued</h4>
    <div class="rs">Private practice becomes legal for the first time</div></div>
</div>
"""

D2C = """
<div class="deskhero"><span class="lab">In a program</span>
<h2>Seven rules. Print this before you take a placement meeting.</h2>
<p>They live in four different sections of the code, which is most of the
reason hardly anyone has read all of them.</p></div>
<div class="rulecard"><span class="lab">What a California trainee may do</span>
<ol>
<li><b>Not in a private practice or a professional corporation.</b> Not as an
employee, not as a volunteer. <span class="cite">&sect;&thinsp;4980.43.3(b)(1)</span></li>
<li><b>Employee or volunteer. Never an independent contractor.</b>
<span class="cite">&sect;&thinsp;4980.43.3(a)</span></li>
<li><b>No money from a client, and no renting space from your site.</b>
<span class="cite">&sect;&thinsp;4980.43.3(e),(f)</span></li>
<li><b>Not before 12 semester or 18 quarter units.</b>
<span class="cite">&sect;&thinsp;4980.43(c)(6)</span></li>
<li><b>Enrolled in a practicum course while counseling</b>, with one gap of
fewer than 90 days. <span class="cite">&sect;&thinsp;4980.42(c)</span></li>
<li><b>Your school must approve the site and hold a written agreement with
it.</b> <span class="cite">&sect;&thinsp;4980.42(e)</span></li>
<li><b>Not supervised by a spouse, relative or domestic partner.</b>
<span class="cite">&sect;&thinsp;4980.43.3(d)</span></li>
</ol></div>
<div class="qrow" style="margin-top:11px"><span class="qn">&rarr;</span>
<span><span class="qt">Now: who finds your site?</span>
<span class="qs">All 78 programs, in their own words</span></span>
<span class="qb">Look up</span></div>
"""

# -------------------------------------------------------------- associates
D3A = """
<div class="deskhero"><span class="lab">You are counting toward 3,000</span>
<h2>Everything a California associate needs, in one place.</h2>
<p>Nothing you type here is sent anywhere. No account, no database.</p></div>
<span class="lab">Your desk &middot; figures stay in this browser</span>
<div class="tiles" style="margin-top:8px">
  <div class="tile"><span class="lab">Hours logged</span><div class="num">1,284</div>
    <div class="sub">of 3,000 &middot; 43%</div></div>
  <div class="tile act"><span class="lab">Relational hours</span><div class="num">228</div>
    <div class="sub">of 500 &mdash; <b>this is your gate</b></div></div>
  <div class="tile"><span class="lab">Weeks elapsed</span><div class="num">61</div>
    <div class="sub">of 104 minimum</div></div>
  <div class="tile"><span class="lab">Projected license</span><div class="num">Mar 2028</div>
    <div class="sub">at 18 hrs/week</div></div>
  <div class="tile"><span class="lab">Registration expires</span><div class="num">Jul 2027</div>
    <div class="sub">renewal now $75</div></div>
  <div class="tile"><span class="lab">Law &amp; ethics</span><div class="num">Not yet</div>
    <div class="sub">due in this renewal period</div></div>
</div>
"""

D3B = """
<div class="deskhero"><span class="lab">You are counting toward 3,000</span>
<h2>The three things this room is actually asking.</h2>
<p>Taken from what gets posted, not from what a taxonomy suggests.</p></div>
<div class="thread"><div class="q">&ldquo;547 hours and nobody will hire
me.&rdquo;</div><div class="meta">114 comments &middot; the loudest thread found</div>
<div class="a"><b>It is a billing rule, not an hour count.</b> Medi-Cal names
registered associates as billable staff. Commercial payers do not, which is why
the jobs are where they are. &rarr;</div></div>
<div class="thread"><div class="q">&ldquo;Am I supposed to be doing this
unpaid?&rdquo;</div><div class="meta">87 comments</div>
<div class="a"><b>The wage claim is a real one, and the Board is not where you
file it.</b> Step by step, with the form. &rarr;</div></div>
<div class="thread"><div class="q">&ldquo;Will my hours from out of state
count?&rdquo;</div><div class="meta">recurring &middot; the Board has answered
five times</div>
<div class="a"><b>Yes, with conditions.</b> Nobody reads the answer because it is
in a PDF nobody links. &rarr;</div></div>
<span class="lab" style="display:block;margin-top:13px">Then the shelf &mdash; 12 pages</span>
"""

D3C = """
<div class="deskhero"><span class="lab">You are counting toward 3,000</span>
<h2>One bar. Four gates. Nothing leaves this browser.</h2>
<p>Written for AMFTs; where an ASW or APCC differs it says so.</p></div>
<div class="ledger"><span class="lab">1,284 of 3,000 hours</span>
  <div class="bar"><i style="width:43%"></i>
    <em style="left:58%" data-l="1,750 direct"></em>
    <em style="left:100%" data-l="3,000"></em></div>
  <div class="gates">
    <div class="warn"><span class="g">228 / 500</span>relational &mdash; the gate
    people miss</div>
    <div><span class="g">61 / 104</span>weeks elapsed</div>
    <div><span class="g">Mar 2028</span>projected, at 18 hrs/wk</div>
    <div><span class="g">Jul 2027</span>registration expires</div>
  </div></div>
<div class="thread"><div class="q">&ldquo;547 hours and nobody will hire
me.&rdquo;</div><div class="a"><b>It is a billing rule, not an hour count.</b> &rarr;</div></div>
<div class="thread"><div class="q">&ldquo;Am I supposed to be doing this
unpaid?&rdquo;</div><div class="a"><b>The wage claim is real, and the Board is not
where you file it.</b> &rarr;</div></div>
"""

# ---------------------------------------------------------------- licensed
D4A = """
<div class="fp-mast"><div class="k"><span>The Licensed Desk</span>
  <span>Tuesday 11 August 2026</span></div>
  <h2>Therapist Support</h2>
  <div class="dek">What changed, what it costs you, and what the room is arguing about</div></div>
<div class="fp-cols">
  <div class="fp-lead">
    <div class="byl">Lead &middot; effective 1 April 2026</div>
    <h3>Your Psychology Today profile is probably now non-compliant.</h3>
    <p>The advertising rule changed what a licensee must display, and the
    default profile layout does not display it. What has to appear, where, and
    what the Board has said about enforcement.</p>
    <div class="byl">Second &middot; effective 1 January 2026</div>
    <h3>A per-session duty most therapists do not know exists.</h3>
    <p>Telehealth documentation, per session, not per client.</p>
  </div>
  <div class="fp-side"><span class="lab">In committee</span>
    <ol><li><b>AB &mdash;</b>supervision hours</li>
      <li><b>SB &mdash;</b>interstate compact</li>
      <li><b>AB &mdash;</b>fee schedule after 2030</li></ol></div>
</div>
<div class="fp-strip">
  <div><span class="lab">Rates</span>What insurers actually pay</div>
  <div><span class="lab">Panels</span>CAQH, PECOS, PAVE</div>
  <div><span class="lab">Tax</span>Sole prop or professional corp</div>
  <div><span class="lab">Records</span>Retention and subpoenas</div>
</div>
"""

D4B = """
<div class="deskhero"><span class="lab">Licensed</span>
<h2>What changed, and whether it applies to you.</h2>
<p>Reverse chronological. Every entry carries the date it took effect and the
date this page last checked it.</p></div>
<div class="clog">
  <div class="row"><div class="d">Effective 1 April 2026 &middot; checked August 2026</div>
    <h4>The advertising rule</h4>
    <p>What a licensee must display, and why the default directory profile does
    not display it.</p>
    <span class="app">Applies to every licensee</span></div>
  <div class="row"><div class="d">Effective 1 January 2026 &middot; checked August 2026</div>
    <h4>Telehealth documentation, per session</h4>
    <p>A duty that attaches to each session rather than to the client file.</p>
    <span class="app">Applies if you see anyone remotely</span></div>
  <div class="row old"><div class="d">Effective 1 July 2026 &middot; checked August 2026</div>
    <h4>Board fees halved</h4>
    <p>And reverting in 2030. What renewal costs now.</p>
    <span class="app">Applies at your next renewal</span></div>
  <div class="row old"><div class="d">Ongoing</div>
    <h4>36 hours of continuing education</h4>
    <p>Which six are mandatory, and what does not count.</p>
    <span class="app">Applies every two years</span></div>
</div>
<span class="lab" style="display:block;margin-top:11px">The reference shelf &mdash; 19 pages</span>
"""

# ------------------------------------------------------------------ owners
D5A = """
<div class="deskhero"><span class="lab">Running a practice</span>
<h2>Four decisions, each with the arithmetic attached.</h2>
<p>Not articles &mdash; calculators with your numbers in them.</p></div>
<div class="panelgrid">
  <div><div class="q">Incorporate, or stay a sole proprietor?</div>
    <div class="n2">$1,248</div><div class="s">the SDI line the pitch forgets</div></div>
  <div><div class="q">Hire an associate?</div>
    <div class="n2">Break-even</div><div class="s">at what caseload, in your county</div></div>
  <div><div class="q">Panels, or private pay?</div>
    <div class="n2">$38&ndash;$250</div><div class="s">per session, same code</div></div>
  <div><div class="q">Which EHR?</div>
    <div class="n2">15</div><div class="s">systems priced</div></div>
</div>
<span class="lab" style="display:block;margin-top:13px">The shelf &mdash; 8 pages, and
that is the problem</span>
"""

D5B = """
<div class="deskhero"><span class="lab">Running a practice</span>
<h2>Answer three questions, get the page.</h2></div>
<div class="tree">
  <div class="q">Are you taking insurance?</div>
  <div class="branch">
    <div><span class="lab">Yes</span>Panels, CAQH, and what each payer actually
    pays per session</div>
    <div><span class="lab">No</span>Good faith estimates, superbills, and what
    private pay charges</div>
  </div>
  <div class="q" style="margin-top:11px">Is anyone working under you?</div>
  <div class="branch">
    <div><span class="lab">Yes</span>Supervision, the wage rules, and the
    break-even caseload</div>
    <div><span class="lab">Not yet</span>What it costs to add the first one</div>
  </div>
</div>
"""

# ------------------------------------------------------------- shell mocks
S1 = """
<div class="band"><span class="you">You are at &middot; counting hours</span>
<span>This page tells you <b>what the wage claim is worth, and the 30-day
clock</b>.</span>
<span class="nx">All 12 for this stage &rarr;</span></div>
<div style="border:2px solid var(--ink);background:#fff;padding:14px 16px;margin-top:9px">
<h3 style="font-size:19px">Unpaid hours as a California associate</h3>
<p style="font-size:12px;color:var(--muted);margin:0">The wage claim, step by
step &mdash; and why the Board is not where you file it.</p></div>
"""

S2 = """
<div class="railmock">
  <div><h3 style="font-size:19px">Unpaid hours as a California associate</h3>
  <p style="font-size:12px;color:var(--muted)">The wage claim, step by step
  &mdash; and why the Board is not where you file it.</p>
  <p style="font-size:12px">An associate who is not paid for non-clinical time
  has a wage claim. It is filed with the Labor Commissioner&hellip;</p></div>
  <div class="rail"><span class="lab">The route</span>
    <span>Deciding</span><span>In a program</span>
    <span class="cur">Counting hours</span>
    <span>Licensed</span><span>Practice owner</span></div>
</div>
"""

S3 = """
<div style="border:2px solid var(--ink);background:#fff;padding:14px 16px">
<h3 style="font-size:19px">Unpaid hours as a California associate</h3>
<p style="font-size:12px;color:var(--muted);margin:0">The wage claim, step by
step&hellip;</p></div>
<div class="bandfoot" style="margin-top:11px"><span class="lab">You are counting
toward 3,000</span>
<h4>Eleven other pages are written for this stage.</h4>
<p>Next, most people read: what a job has to be able to bill before it can hire
you &middot; whether out-of-state hours count &middot; the 3,000-hour
calculator.</p></div>
"""


def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block to inherit "
                 "from. This page borrows its stylesheet from that file on "
                 "purpose, so the two cannot drift apart - fix the donor "
                 "rather than pasting a copy in here.")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>Five doors, three ways each &mdash; stage-hub mockups</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
         'opsz,wght@12..96,800&family=Fraunces:opsz,wght@9..144,600;9..144,800&'
         'family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&'
         'display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    # ------------------------------------------------------------- masthead
    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s &middot; '
             "not indexed</span>"
             "<h1>Five doors, three ways each.</h1>"
             "<p>The first proposal argued <em>whether</em> to build stage "
             "entry points and sketched one visual direction per stage. This "
             "one shows the alternatives for every door, says which one to "
             "pick and why, and lists everything else that changes if it "
             "ships.</p>"
             '<div class="meta"><span class="chip">16 mockups</span>'
             '<span class="chip">5 doors</span>'
             '<span class="chip">4 can open now</span>'
             '<span class="chip">Companion to stage-architecture</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, l in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, l))
    o.append("</ul></div></nav>")

    o.append('<div class="wrap">')

    # ----------------------------------------------------------------- read
    o.append('<section id="read"><div class="kicker"><span class="n">01</span>'
             "<h2>How to read this</h2></div>")
    o.append('<p class="lede">Every mockup below is real HTML at real '
             "proportions in the shipping design system, not a picture of an "
             "idea. Where a figure appears it is a figure the site already "
             "publishes, so you are looking at what the door would actually "
             "say on the day it opened.</p>")
    o.append('<div class="grid g3">')
    for t, b in [
        ("Two or three per door",
         "Variants differ in <b>what the door leads with</b> &mdash; a tool, a "
         "question, or a price &mdash; not in color. If two variants would "
         "produce the same page with different padding, only one is here."),
        ("A recommendation, with the cost of it",
         "Every variant carries what it buys and what it costs, and one is "
         "marked. A mockup set without a recommendation just moves the "
         "decision back to you, which is not help."),
        ("Then the part that decides the timeline",
         "Section 09 is the impact list: the registry field, the six passes "
         "that change, the one configuration line that would make all five "
         "hubs invisible, and the two ways this ships broken."),
    ]:
        o.append('<div class="card"><h3>%s</h3><p style="margin:0">%s</p></div>'
                 % (t, b))
    o.append("</div>")

    o.append('<div class="card gold"><h3>One thing in the first proposal is now '
             "out of date</h3><p style=\"margin:0\">The coverage audit recorded "
             "<b>&ldquo;Stage 2, in a program &mdash; 0 pages, hold&rdquo;</b>. "
             "That was true on 10 August. The practicum page and the "
             "career-change page shipped on the 11th, so the student door now "
             "has two pages of its own plus the 78 program pages and the "
             "placement dataset behind it. <b>Four of the five doors can open; "
             "only the practice-owner door still fails the test.</b></p></div>")
    o.append("</section><hr class=\"rule\">")

    # --------------------------------------------------------------- glance
    o.append('<section id="glance"><div class="kicker"><span class="n">02</span>'
             "<h2>The five doors</h2></div>")
    o.append('<div class="doors">')
    for num, name, url, state, cls, note in [
        ("01", "Deciding", "/for/deciding/", "Open now", "go", "73 pages"),
        ("02", "In a program", "/for/students/", "Newly open", "new",
         "2 + 78 behind"),
        ("03", "Counting hours", "/for/associates/", "Flagship", "go",
         "12 pages"),
        ("04", "Licensed", "/for/licensed/", "Open now", "go", "19 pages"),
        ("05", "Practice owner", "/for/practice-owners/", "Hold", "hold",
         "8 pages &mdash; too thin"),
    ]:
        o.append('<div class="door"><span class="n">%s</span><h4>%s</h4>'
                 '<div class="u">%s</div>'
                 '<p style="font-size:12px;color:var(--muted);margin:7px 0 0">%s</p>'
                 '<span class="st %s">%s</span></div>'
                 % (num, name, url, note, cls, state))
    o.append("</div>")
    o.append('<p class="src">Namespace, data model and build mechanics are '
             'unchanged from <a href="stage-architecture.html">the first '
             "proposal</a> &mdash; <code>/for/</code>, a <code>stages</code> "
             "array on each registry entry, and a generated hub rather than a "
             "standalone site. What follows is only the design and the "
             "consequences.</p>")
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- door 01
    o.append('<section id="deciding"><div class="kicker"><span class="n">03</span>'
             "<h2>Door 1 &mdash; Deciding</h2></div>")
    o.append('<p class="lede">Has not applied, or is choosing between programs. '
             "Biggest shelf on the site (73 pages) and the quietest audience by "
             "engagement. The door&rsquo;s job here is <b>routing</b>, not "
             "persuasion &mdash; this reader arrives from a search with a "
             "specific question already formed.</p>")
    o.append(variant(
        "1A", "The Ladder",
        "The whole route as one vertical, gates marked, current rung lit, with "
        "a visible exit for anyone arriving from another state.",
        "/for/deciding", D1A,
        "Orients somebody who has no map at all, and the gates are the honest "
        "part &mdash; it shows where people stop, not just the steps.",
        "Implies one linear path, which is wrong for the career-changer and the "
        "out-of-state applicant. The exit hatch helps but is doing a lot of "
        "work. And it duplicates door 2&rsquo;s timeline."))
    o.append(variant(
        "1B", "The Two Questions",
        "The page is literally the two decisions this reader has to make, each "
        "opening onto the comparison the site already publishes.",
        "/for/deciding", D1B,
        "Matches what people actually type into a search box, and it puts the "
        "site&rsquo;s two strongest assets &mdash; 78 programs and the "
        "three-license statutory table &mdash; in the doorway rather than three "
        "clicks down.",
        "Does not hand anything back on arrival, so it is less likely to be "
        "reposted than a tool. Reads as a menu if the two cards are not carrying "
        "real numbers.", rec=True))
    o.append(variant(
        "1C", "The Price Tag",
        "Leads with the honest bill: tuition range, years, the unpaid year, and "
        "what a job pays afterward.",
        "/for/deciding", D1C,
        "The single most-searched thing about this decision and nobody leads "
        "with it. Highly linkable, and it is the page a friend sends to a friend.",
        "Reads as discouragement whether or not it is meant that way, and the "
        "career-change page already carries a guard against exactly that. Also "
        "the tuition range is 35 of 78 programs, which needs a caveat too heavy "
        "for a hero."))
    o.append(pick(
        "1B, with 1C&rsquo;s four figures as the hero strip and 1A demoted to a "
        "compact rail lower down.",
        "The door&rsquo;s job is to route, and this reader has already formed a "
        "question. The ladder is a good <em>illustration</em> and a poor "
        "<em>navigation</em> &mdash; it makes you read six rungs to find the one "
        "you came for. Taking 1C&rsquo;s numbers as a strip keeps the honesty "
        "without making the whole door read as a warning."))
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- door 02
    o.append('<section id="students"><div class="kicker"><span class="n">04</span>'
             "<h2>Door 2 &mdash; In a program</h2></div>")
    o.append('<p class="lede">Enrolled, practicum approaching or underway. This '
             "is the door that just became possible. It is also the only stage "
             "where the site holds a dataset <b>nobody else has</b>, which "
             "should decide the design.</p>")
    o.append(variant(
        "2A", "The Placement Desk",
        "Opens as a lookup: pick your program, get its published answer to the "
        "one question that decides your year, in its own words.",
        "/for/students", D2A,
        "Turns the new dataset into a tool. Extremely shareable inside a cohort "
        "&mdash; this is the link one student sends to twenty. And it answers a "
        "question with a verdict, which almost nothing else on this topic does.",
        "One trick. Once you have looked up your own program there is little "
        "reason to come back, so the rest of the door has to carry the return "
        "visit.", rec=True))
    o.append(variant(
        "2B", "The Countdown",
        "A timeline of the four deadlines between 12 units and a registration "
        "number, with what must be true at each.",
        "/for/students", D2B,
        "This stage genuinely is defined by dates, and the 90-day rule is the "
        "sharpest deadline anywhere on the path &mdash; miss it and the hours "
        "are simply gone.",
        "Substantially the same shape as door 1&rsquo;s ladder, so building both "
        "means two vertical timelines two clicks apart. Better as a module than "
        "as a frame."))
    o.append(variant(
        "2C", "The Rules Card",
        "The seven trainee rules as a single printable card, with the dataset "
        "beneath it.",
        "/for/students", D2C,
        "The highest-utility artifact on the whole site for this reader: it can "
        "be screenshotted and taken into a placement meeting. The "
        "no-private-practice rule in particular saves people a wasted month.",
        "Entirely static, nothing personalized, and it will be read once. It is "
        "a great <em>module</em> and a weak <em>hero</em>."))
    o.append(pick(
        "2A as the hero, 2C immediately beneath it, 2B reduced to one module "
        "inside the page.",
        "The lookup is what gets the link shared; the rules card is what gets it "
        "saved. Putting them in that order means the door earns its traffic and "
        "then earns the bookmark. 2B&rsquo;s 90-day countdown is important "
        "enough to appear but not distinctive enough to lead &mdash; and "
        "building it as a frame would duplicate door 1."))
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- door 03
    o.append('<section id="associates"><div class="kicker"><span class="n">05</span>'
             "<h2>Door 3 &mdash; Counting hours</h2></div>")
    o.append('<p class="lede">The flagship. Loudest room in the community '
             "analysis, twelve pages ready, and the stage where the site is "
             "already strongest. One thing constrains every design here: a large "
             "share of this traffic arrives from a phone, from a link posted in "
             "a group.</p>")
    o.append(variant(
        "3A", "The Desk",
        "Six tiles of the things an associate is tracking at once, computed in "
        "the browser from figures they enter.",
        "/for/associates", D3A,
        "Hands something back on arrival, which is what gets a link reposted "
        "rather than just read. Densest information per screen of any variant "
        "here.",
        "Six tiles is six things to read before you know what the page is. The "
        "empty state &mdash; what it looks like before anything is typed &mdash; "
        "is the real design problem and this mockup quietly skips it. On a 390px "
        "phone the grid drops to two columns and the fold lands mid-tile."))
    o.append(variant(
        "3B", "The Three Questions",
        "Opens with the loudest threads verbatim, each answered by a page.",
        "/for/associates", D3B,
        "Highest recognition of any variant: somebody arriving from a group post "
        "sees their own sentence at the top. Directly addresses the first "
        "proposal&rsquo;s sixth objection &mdash; a tidy taxonomy is not a "
        "destination.",
        "Heavier in tone, and quoted community posts need care &mdash; the "
        "standing rule on this site is that nothing identifies the person. It "
        "also dates: a thread that was loud in August is not necessarily loud in "
        "March, and there is no machinery keeping it current."))
    o.append(variant(
        "3C", "The Ledger",
        "One horizontal bar for the 3,000 hours with the sub-gates marked, then "
        "the three questions beneath it.",
        "/for/associates", D3C,
        "Reads in one glance on a phone, which is where this traffic lands. It "
        "also puts the <b>relational-hours gate</b> &mdash; the one people miss "
        "and the one that costs the most &mdash; in the highest-contrast place "
        "on the page.",
        "Less information than the Desk. Somebody who wants all six numbers has "
        "to expand, so it trades depth for a faster first read.", rec=True))
    o.append(pick(
        "3C, with 3A&rsquo;s six tiles as the expanded state after input, and "
        "3B&rsquo;s questions as the section directly below the bar.",
        "All three are worth building and they are not really alternatives "
        "&mdash; they are the same door at three levels of engagement. The "
        "question is only which one is on top, and the answer is decided by the "
        "phone: one bar with a marked gate survives a 390px first screen and six "
        "tiles do not. The privacy line has to sit in the hero in every version, "
        "not the footer."))
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- door 04
    o.append('<section id="licensed"><div class="kicker"><span class="n">06</span>'
             "<h2>Door 4 &mdash; Licensed</h2></div>")
    o.append('<p class="lede">Nineteen pages, and the only stage whose defining '
             "content is <b>what changed recently</b>. That makes staleness the "
             "central design risk rather than an afterthought.</p>")
    o.append(variant(
        "4A", "The Front Page",
        "An editorial masthead with a dateline, a lead story and a bills-in-"
        "committee rail.",
        "/for/licensed", D4A,
        "The most repostable thing in the whole set, and the natural home for "
        "the newsletter signup. It reads as a publication rather than a "
        "reference site.",
        "A masthead with yesterday&rsquo;s date on it is worse than no masthead. "
        "It only works wired to the existing checked-date machinery, and the "
        "&ldquo;in committee&rdquo; rail needs a legislation tracker that does "
        "not exist yet."))
    o.append(variant(
        "4B", "The Change Log",
        "Reverse chronological, each entry carrying its effective date, its "
        "last-checked date, and who it applies to.",
        "/for/licensed", D4B,
        "<b>Cannot go stale, because staleness is its content.</b> An entry with "
        "an old checked-date is still doing its job. It also reuses the "
        "checked-date machinery and <code>changes.html</code> that already "
        "exist, so it is a fraction of the work.",
        "Less striking than a masthead, and it will not get reposted the way a "
        "lead story would. The &ldquo;applies to&rdquo; tags need to be honest "
        "and specific or they become noise."))
    o.append(pick(
        "4B, and revisit 4A only once a legislation tracker exists.",
        "The first proposal already said a stale masthead is worse than none. "
        "That is the whole argument, and the change log is the version of this "
        "door where the failure mode is impossible by construction. It is also "
        "roughly a fifth of the build."))
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- door 05
    o.append('<section id="owners"><div class="kicker"><span class="n">07</span>'
             "<h2>Door 5 &mdash; Practice owner</h2></div>")
    o.append('<p class="lede">Eight pages. This door fails the only test that '
             "matters &mdash; enough content specifically for this reader to "
             "justify its own section &mdash; and both variants below are here "
             "so the decision is made on a picture rather than a paragraph.</p>")
    o.append(variant(
        "5A", "The Control Panel",
        "Four decisions an owner is actually facing, each showing the number the "
        "site can already compute.",
        "/for/owners", D5A,
        "Every module is a calculator that exists. It is the closest thing to a "
        "product on the site, and owners are the segment with money.",
        "Four modules over eight pages is a thin shelf, and three of those pages "
        "are also on the licensed door. Built today it would be the "
        "duplicate-content risk in section 09, in its purest form.", rec=True))
    o.append(variant(
        "5B", "The Decision Tree",
        "Three branching questions that land the reader on one page.",
        "/for/owners", D5B,
        "Handles the thin shelf gracefully &mdash; a tree with eight leaves "
        "looks deliberate where a grid with eight tiles looks empty.",
        "Self-identification is exactly the cognitive tax the audience-navigation "
        "research warns about, and here it is asked twice before anything is "
        "shown. It also hides the shelf, which is the opposite of what a hub is "
        "for."))
    o.append(pick(
        "Neither, yet. 5A when the queue lands.",
        "Opening this door on eight pages, three of which belong to another "
        "door, is how a hub becomes a thin duplicate of a topic page. The "
        "advertising rule, the telehealth duty, paying associates and the records "
        "pages are all in the editorial queue; four of those and this opens "
        "honestly."))
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------------- shell
    o.append('<section id="shell"><div class="kicker"><span class="n">08</span>'
             "<h2>The shared shell</h2></div>")
    o.append('<p class="lede">The doors are five pages. The <b>&ldquo;you are '
             "here&rdquo; band is 200 pages</b>, and it is where the sense of a "
             "destination actually comes from &mdash; a reader who lands on a "
             "leaf page from a search never sees a hub at all unless something "
             "on that page tells them the hub exists. Three ways to do it.</p>")
    o.append(variant(
        "S1", "Above the article &mdash; the annotated breadcrumb",
        "One line above the headline: which stage this page belongs to, and the "
        "<code>stage_note</code> saying what it tells you <em>at your stage</em>.",
        "/associate-unpaid-hours-california.html", S1,
        "Seen by everybody, including the search visitor who bounces in four "
        "seconds. Cheap: one pass, one line, no duplication. The "
        "<code>stage_note</code> earns its place immediately.",
        "Competes with the existing breadcrumb trail for the same strip of "
        "screen. Two navigational lines above a headline is one too many, so the "
        "existing breadcrumb has to move or merge.", rec=True))
    o.append(variant(
        "S2", "A sticky rail beside the article",
        "A right-hand rail showing the five stages with the current one lit.",
        "/associate-unpaid-hours-california.html", S2,
        "Always visible while reading, and it teaches the whole model rather "
        "than just the current position.",
        "Dies on mobile, which is most of the traffic, and on desktop it "
        "competes with the jump nav the long pages already carry. It also "
        "narrows the measure on exactly the pages with the widest tables."))
    o.append(variant(
        "S3", "After the article &mdash; the next-step band",
        "A full-width band at the end: your stage, how many other pages are "
        "written for it, and the three people usually read next.",
        "/associate-unpaid-hours-california.html", S3,
        "Catches the reader at the moment they have finished and are deciding "
        "whether to leave, which is the highest-intent moment on the page. "
        "Fits the existing footer-band pass.",
        "Only reaches people who finish, and on a 28,000px page like the "
        "practicum comparison that is a small minority.", rec=True))
    o.append(pick(
        "S1 and S3 together. Not S2.",
        "They catch opposite ends of the same visit and neither costs a "
        "redesign: S1 is one line in the existing breadcrumb pass, S3 is one "
        "block in the existing footer-band pass. S2 is the most designed of the "
        "three and the least useful, because it is invisible exactly where the "
        "traffic is. Shipping S1 means merging it with the current breadcrumb "
        "rather than stacking a second line above it."))
    o.append("</section><hr class=\"rule\">")

    # --------------------------------------------------------------- impact
    o.append('<section id="impact"><div class="kicker"><span class="n">09</span>'
             "<h2>What else changes</h2></div>")
    o.append('<p class="lede">Five hub pages is the small part. This is the '
             "rest of it, in the order things would break.</p>")

    o.append('<div class="risk"><h4>The one that would waste a day</h4>'
             "<p>Every pass in <code>_dev/</code> walks the site root plus "
             "<code>SUBDIRS</code>, which is "
             "<code>(\"money\", \"licensure\", \"getting-paid\", \"practice\", "
             "\"training\")</code>. <b>A new top-level <code>/for/</code> "
             "directory is invisible to all of them</b> &mdash; no chrome, no "
             "nav, no analytics, no CSS extraction &mdash; and invisible to "
             "<code>discovery.py</code>, so the hubs would also be missing from "
             "the sitemap.</p>"
             "<p>The five hubs would build, look completely unstyled, and every "
             "guard would still report clean, because each guard checks its own "
             "pass and nothing checks the set of directories. <b>Add "
             "<code>&quot;for&quot;</code> to <code>SUBDIRS</code> in the same "
             "commit that creates the directory.</b></p></div>")

    o.append('<div class="card"><h3>The data model &mdash; one field, and one '
             "guard that has to be strict</h3>"
             "<p>Two keys per registry entry, alongside the existing "
             "<code>topic</code>:</p>"
             '<pre style="font-family:var(--mono);font-size:12px;overflow-x:auto;'
             'background:#fff;border:1.5px solid var(--line);padding:11px">'
             '"stages": ["associate", "student"],\n'
             '"stage_note": {\n'
             '  "associate": "What the claim is worth, and the 30-day clock.",\n'
             '  "student": "Why a placement cannot ask you to work unpaid."\n'
             "}</pre>"
             "<p style=\"margin:0\"><b><code>stage_note</code> must be mandatory "
             "wherever <code>stages</code> has an entry.</b> It is the only thing "
             "standing between a stage hub and a re-listed topic hub, and an "
             "optional field will be skipped on the pages where writing it is "
             "hardest &mdash; which are the pages that need it most.</p></div>")

    rows = [
        ("<code>mock/library/registry.json</code>",
         "Two new keys on ~200 entries",
         "The tagging pass itself. Roughly a day of judgment, not typing "
         "&mdash; deciding whether the county pay page belongs to Deciding, "
         "Associates or both is the actual work."),
        ("<code>_dev/registry_meta.py</code>, <code>registry_sync.py</code>",
         "Must learn the two keys",
         "They rewrite entries. Anything they do not know about is silently "
         "dropped on the next run, which would delete the tagging without "
         "failing a build."),
        ("<code>_dev/taxonomy_leaves.py</code>",
         "Five new clusters, or five catch-alls",
         "This pass fails the build on a catch-all cluster, which is correct "
         "&mdash; and it fired twice on 11 August for exactly this reason. "
         "Budget for it rather than being surprised."),
        ("<code>_dev/discovery.py</code>",
         "Sitemap, after <code>SUBDIRS</code> is fixed",
         "Runs last and derives the sitemap from what exists. Correct by "
         "construction once the directory is in scope."),
        ("<code>_dev/restyle.py</code>",
         "The masthead gains a doorway",
         "The nav is already at seven items on two rows at 1440px. Five more "
         "top-level entries will not fit; the doors need one entry that opens, "
         "not five that wrap."),
        ("<code>_dev/breadcrumbs.py</code>",
         "A page now has two parents",
         "Topic and stage. Recommendation: the breadcrumb stays the topic trail, "
         "and the stage becomes the S1 band merged into the same strip. Two "
         "trails is worse than either."),
        ("<code>_dev/uplinks.py</code>, <code>cluster_links.py</code>, "
         "<code>link_sinks.py</code>",
         "Sibling and sink maths change",
         "Five hubs at ~40 outbound links each is ~200 new internal links. Run "
         "the sink analysis before and after; the current shape of the link "
         "graph is the site&rsquo;s whole position."),
        ("<code>_dev/home_doorway.py</code>, <code>stage_router.py</code>",
         "Repoint the home band",
         "The &ldquo;Who this is for&rdquo; band already carries four situations "
         "pointing at <code>resources.html#where=&hellip;</code>. Those become "
         "the doors. This is the change that makes the whole thing visible."),
        ("<code>_dev/seo_head.py</code>, <code>seo_meta.py</code>, "
         "<code>social_cards.py</code>, <code>seo_rules.py</code>",
         "Five titles and descriptions",
         "Inside the existing limits &mdash; title 15&ndash;68, description "
         "70&ndash;168. Each hub needs a distinct primary query or it competes "
         "with the topic hub it overlaps."),
        ("<code>_dev/dark_band_labels.py</code>, <code>contrast_pass.py</code>",
         "Any new pine band",
         "Four of the five mockups above open on a pine gradient. The eyebrow "
         "label inherits <code>#4E4940</code> and lands at <b>1.20:1</b> unless "
         "the band is registered in the label pass &mdash; the exact bug fixed "
         "on 11 August."),
        ("<code>_dev/analytics_events.py</code>, <code>tool_analytics.py</code>",
         "One new event, behavior only",
         "Door &rarr; page is worth measuring. The guard fails the build if "
         "tracking can read <code>.value</code>, <code>.checked</code>, "
         "<code>FormData</code>, <code>location.hash</code> or "
         "<code>.search</code> &mdash; and the 3C ledger takes typed numbers, so "
         "this needs care rather than a copy-paste."),
        ("<code>_dev/extract_css.py</code>",
         "One shared style block",
         "Write the hub CSS once and identically across all five, so it hoists "
         "to a single stylesheet and <code>css_dedupe</code> collapses it. Five "
         "near-identical blocks ship as five files."),
        ("<code>_dev/ops_state.py</code>",
         "The board",
         "Doors move from proposal to in-flight to shipped as they land."),
    ]
    o.append('<div class="tw"><table><tr><th>What</th><th>Changes how</th>'
             "<th>Why it matters</th></tr>")
    for a, b, c in rows:
        o.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a, b, c))
    o.append("</table></div>")

    o.append('<div class="risk"><h4>The two ways this ships broken</h4>'
             "<p><b>1. Thin duplicates.</b> A stage hub that is 90% the same "
             "list as a topic hub is a thin page, and five of them pointed at "
             "overlapping content is the classic way a site loses ground it "
             "already held. <code>stage_note</code> is the entire mitigation: "
             "every listing has to say something the topic hub does not. Guard "
             "it, do not trust it.</p>"
             "<p><b>2. Stale duplicates.</b> This repo has shipped a "
             "stale-duplicate bug three times &mdash; double-escaping twice and "
             "the CIIS tuition card. Any figure appearing on both a hub and a "
             "leaf must be read from the same data module at build time, never "
             "written into the hub. If a number is typed into a hub, it is "
             "already wrong.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- order
    o.append('<section id="order"><div class="kicker"><span class="n">10</span>'
             "<h2>Build order</h2></div>")
    o.append('<p class="lede">Revised from the first proposal, because the '
             "student door opened. Each step is shippable on its own and the "
             "site is never half-migrated.</p>")
    o.append('<ol class="plan">')
    for h, why, out in [
        ("Add <code>&quot;for&quot;</code> to SUBDIRS, and tag the library",
         "The configuration line first, so nothing built afterward is invisible. "
         "Then <code>stages</code> and <code>stage_note</code> across ~200 "
         "entries, with the mandatory-note guard written before the tagging "
         "rather than after.",
         "No new pages. Registry is ready and nothing is live yet."),
        ("<code>/for/associates/</code> &mdash; variant 3C",
         "Loudest room, twelve pages ready, and the ledger is the cheapest of "
         "the three to build because the arithmetic already exists in the "
         "3,000-hour calculator.",
         "One hub. Measure it for a fortnight before building the next."),
        ("Ship S1 and S3, and repoint the home band",
         "This is the step that makes the doors exist for anyone who did not "
         "arrive at one. Doing it after a single hub means the band has "
         "somewhere real to point.",
         "200 pages gain a stage line and a next-step band."),
        ("<code>/for/students/</code> &mdash; variant 2A over 2C",
         "The lookup is the most shareable single thing in this document and it "
         "runs entirely off <code>practicum_data.py</code>, which shipped on "
         "11 August.",
         "One hub, one new interaction, no new research."),
        ("<code>/for/deciding/</code> &mdash; variant 1B",
         "Largest shelf, lowest urgency. It benefits most from the two hubs "
         "above already existing, because half of what it routes to is them.",
         "One hub. The doors are now a set rather than an experiment."),
        ("<code>/for/licensed/</code> &mdash; variant 4B",
         "Blocked only on the advertising-rule and telehealth-documentation "
         "pages, both already in the approved editorial list.",
         "One hub, plus the two pages it needs."),
        ("<code>/for/practice-owners/</code> &mdash; variant 5A",
         "Last, and only when four more owner pages have landed. Eight is not "
         "enough and opening it early is how the thin-duplicate risk becomes "
         "real.",
         "The set closes."),
    ]:
        o.append('<li><h4>%s</h4><p class="why">%s</p>'
                 '<span class="out">%s</span></li>' % (h, why, out))
    o.append("</ol>")
    o.append('<p class="src">Net new pages: <b>5 hubs</b>, plus the two licensed '
             "pages already on the editorial list. Everything else is a view "
             "over content that exists, one configuration line, and two passes "
             "that already run on every build.</p>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "%s. Companion to "
             '<a href="stage-architecture.html">the stage-architecture '
             "proposal</a>, whose evidence, coverage audit and namespace "
             "argument are not repeated here. Mockups are real HTML in the "
             "shipping design system; every figure in them is one the site "
             "already publishes. Nothing here is live.</p></div></footer>"
             % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("stage doors - the expanded mockup set")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes" % (os.path.basename(OUT),
                                        format(len(html), ",d")))

    bad = 0
    # Every jump target has to exist, because a nav of dead buttons is the
    # thing that ships silently.
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, which is not on the page" % h)
            bad += 1
    # Every door needs at least two rendered variants, or this document has
    # not done the thing it exists to do.
    for door in ("deciding", "students", "associates", "licensed", "owners"):
        i = html.find('id="%s"' % door)
        j = html.find('class="rule"', i)
        n = html.count('class="frame"', i, j if j > i else len(html))
        if n < 2:
            print("GUARD: door %s has %d mockup(s), expected at least 2"
                  % (door, n))
            bad += 1
    n_frames = html.count('class="frame"')
    if n_frames < 12:
        print("GUARD: %d mockups on the page, expected at least 12" % n_frames)
        bad += 1
    if "16 mockups" in html and n_frames != 16:
        print("GUARD: the masthead claims 16 mockups and the page has %d"
              % n_frames)
        bad += 1
    # The SUBDIRS trap is the single most expensive thing in the document.
    if "SUBDIRS" not in html:
        print("GUARD: the SUBDIRS warning is missing")
        bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: this is a working document and must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d mockups, %d jump targets" % (n_frames, len(NAV)))


if __name__ == "__main__":
    main()
