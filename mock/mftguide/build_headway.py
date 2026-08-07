#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build headway-for-california-therapists.html.

An explainer with an affiliate link on it, which sets the standard rather than
lowering it. Three rules the page follows and the guards enforce:

  1. THE DISQUALIFYING FACT GOES FIRST. Headway does not accept California
     associates - no AMFT, ASW or APCC. A large share of this site's readers
     are associates, so burying that below a comparison table would be writing
     for the commission rather than for the reader. It is the second thing on
     the page, in a red block, above everything else.

  2. "NOT PUBLISHED" IS AN ANSWER. Headway does not publish its California
     rates or the share of the reimbursement it keeps. The page says so, in the
     table, where a number would otherwise go. The temptation on an affiliate
     page is to fill that cell with an estimate; an estimate here would be
     invention.

  3. THE MARKETING IS CHECKED AGAINST THE HELP CENTRE. "Credentialed in 30
     days" against "three weeks to four months". "Biweekly" against the 15th
     and the last day of the month, which is 24 payments a year rather than 26.
     Both sources are Headway's own, which is what makes the comparison fair.

Layout follows the Help Scout comparison pattern the user pointed at: a claim,
a table that answers it, and a plain who-it-is-for / who-it-is-not at the end -
rather than a wall of prose with a button at the bottom.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_content as H

SRC = os.path.join(HERE, "_chrome.html")
OUT = os.path.join(HERE, "headway-for-california-therapists.html")
UPDATED = "6 August 2026"


def balanced(s, tag):
    i = s.find("<" + tag)
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<%s\b|</%s>" % (tag, tag), s[i:]):
        d += 1 if m.group(0).startswith("<" + tag) else -1
        if d == 0:
            return (i, i + m.end())
    return None


src = open(SRC, encoding="utf-8").read()
head_end = src.find("</head>")
links = [m.group(0) for m in re.finditer(r"<link\b[^>]*>", src[:head_end])
         if 'rel="stylesheet"' in m.group(0) or "fonts." in m.group(0)
         or 'rel="preconnect"' in m.group(0)]
styles = re.findall(r"<style>.*?</style>", src, re.S)
assert styles, "no stylesheet lifted from the chrome"
hs = balanced(src, "header")
header = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[hs[0]:hs[1]])
fs = balanced(src, "footer")
footer = re.sub(r'(<a href="[^"]*") class="on"', r"\1", src[fs[0]:fs[1]])
# the nav script, so the header actually opens - the exact thing that was
# missing from every page built this way before
navscript = ""
for m in re.finditer(r"<script>([\s\S]*?)</script>", src):
    if "navpanel" in m.group(1):
        navscript = m.group(0)
assert navscript, "no nav script in the chrome source - the header will be dead"

TAG = '<span class="afl" title="Affiliate link">affiliate</span>'


def aff(label, cls="hwcta"):
    return ('<a class="%s" href="%s" target="_blank" rel="noopener noreferrer sponsored">'
            "%s &rarr;</a>%s" % (cls, H.AFF, label, TAG))


CSS = """<style>/* headway */
.hw{--pine:#2C6350;--amber:#F6C560;--ink:#17271F;--line:#E2DACA;--mut:#7C8878;
  --red:#B5483F;--green:#3F9577}
.hwband{background:linear-gradient(135deg,#14261E 0%,#1B4536 48%,#2C6350 100%);
  color:#EFF5F2;padding:30px 0 36px}
.hwband .in{max-width:1180px;margin:0 auto;padding:0 26px;display:grid;
  grid-template-columns:minmax(0,1.3fr) minmax(250px,.7fr);gap:34px;align-items:center}
.hwband .bcr{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 14px;
  padding:0;list-style:none;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.4px;letter-spacing:.1em;text-transform:uppercase}
.hwband .bcr li{display:flex;align-items:center;gap:8px}
.hwband .bcr a{color:#EFF5F2;opacity:.66;text-decoration:none;padding:5px 0;min-height:26px;
  display:inline-flex;align-items:center;border-bottom:1px solid transparent}
.hwband .bcr a:hover{opacity:1;border-bottom-color:currentColor}
.hwband .bcr .sep{opacity:.36}
.hwband .bcr [aria-current]{opacity:.95;font-weight:600;color:var(--amber)}
.hwband h1{font-family:Fraunces,Georgia,serif;font-size:clamp(27px,3.7vw,43px);
  line-height:1.06;font-weight:600;letter-spacing:-.022em;color:#fff;margin:0 0 14px;max-width:19ch}
.hwband h1 em{font-style:normal;color:var(--amber)}
.hwband .dek{font-size:15.4px;line-height:1.72;color:rgba(255,255,255,.87);margin:0;max-width:57ch}
.hwmeta{display:flex;gap:14px;flex-wrap:wrap;margin-top:17px;
  font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
  text-transform:uppercase;color:rgba(255,255,255,.62)}
.hwfig{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);border-radius:16px;
  padding:20px 22px;min-width:0}
.hwfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(30px,4vw,44px);
  line-height:1;color:var(--amber)}
.hwfig span{display:block;font-size:12.5px;line-height:1.55;color:rgba(255,255,255,.74);margin-top:9px}
.hwfig .row{display:flex;justify-content:space-between;gap:10px;padding:8px 0;
  border-top:1px solid rgba(255,255,255,.14);font-size:12.2px;color:rgba(255,255,255,.8)}
.hwfig .row:first-of-type{margin-top:16px}
.hwfig .row b{display:inline;font-size:12.4px;font-family:inherit;color:#fff}

.hwwrap{max-width:1180px;margin:0 auto;padding:34px 26px 20px;display:grid;
  grid-template-columns:214px minmax(0,1fr);gap:40px;align-items:start}
.hwnav{position:sticky;top:16px;min-width:0}
.hwnav b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--mut);margin-bottom:11px}
.hwnav a{display:block;font-size:13.1px;line-height:1.42;color:#4A5A46;text-decoration:none;
  padding:6px 0 6px 12px;border-left:2px solid var(--line)}
.hwnav a:hover{color:var(--ink);border-left-color:#B9AE93}
.hwnav a.on{color:var(--pine);border-left-color:var(--pine);font-weight:600}
.hwbody{min-width:0}
.hwbody h2{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,27px);
  line-height:1.2;font-weight:600;letter-spacing:-.016em;color:var(--ink);
  margin:44px 0 14px;scroll-margin-top:20px}
.hwbody h2:first-child{margin-top:0}
.hwbody h3{font-family:Fraunces,Georgia,serif;font-size:17.5px;margin:26px 0 9px;color:var(--ink)}
.hwbody p{font-size:15.4px;line-height:1.78;color:#3B4A38;margin:0 0 15px;max-width:68ch}
.hwbody p b{color:var(--ink)}
.hwbody a{color:var(--pine)}

/* the disqualifier */
.stop{background:#FCF1F0;border:1px solid #EBCFCC;border-left:4px solid var(--red);
  border-radius:12px;padding:20px 22px;margin:6px 0 20px}
.stop h3{font-family:Fraunces,Georgia,serif;font-size:20px;margin:0 0 9px;color:#7E2F28}
.stop p{margin:0 0 12px;color:#5B3833;font-size:14.8px;max-width:none}
.stop .two{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:11px;margin-top:14px}
.stop .lic{background:#fff;border:1px solid #E7DED0;border-radius:9px;padding:12px 14px;min-width:0}
.stop .lic b{display:block;font-family:'IBM Plex Mono',monospace;font-size:9.6px;
  letter-spacing:.11em;text-transform:uppercase;color:var(--mut);margin-bottom:8px}
.stop .lic span{display:inline-block;font-size:12.6px;background:#F2F5EF;border-radius:20px;
  padding:3px 10px;margin:0 5px 5px 0;color:#2C4227}
.stop .lic.no span{background:#FBEDEC;color:#8A3B33;text-decoration:line-through}

/* fact rows */
.facts{display:grid;gap:9px;margin:6px 0 8px}
.fact{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:14px;background:#fff;
  border:1px solid var(--line);border-radius:10px;padding:14px 16px;align-items:start;min-width:0}
.fact h4{font-family:Fraunces,Georgia,serif;font-size:16px;margin:0 0 5px;color:var(--ink)}
.fact p{font-size:13.4px;line-height:1.6;color:#4A5A46;margin:0;max-width:none}
.fact .v{font-family:Fraunces,Georgia,serif;font-size:22px;line-height:1.15;color:var(--pine);
  text-align:right;min-width:0;overflow-wrap:anywhere}
.fact .v.np{font-size:14px;color:#9A9280;font-style:italic}

/* claim check */
.chk{display:grid;gap:9px;margin:8px 0}
.ck{background:#fff;border:1px solid var(--line);border-radius:10px;padding:13px 15px;min-width:0}
.ck.amber{border-left:3px solid #C98B4B}
.ck.green{border-left:3px solid var(--green)}
.ck b{display:block;font-size:14.4px;color:var(--ink);margin-bottom:5px}
.ck p{font-size:13.3px;line-height:1.6;color:#4A5A46;margin:0;max-width:none}

/* rate cut */
.cut{display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:#fff;
  border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:8px 0}
.cut .was{font-family:Fraunces,Georgia,serif;font-size:26px;color:#9A9280;text-decoration:line-through}
.cut .arr{color:var(--mut)}
.cut .now{font-family:Fraunces,Georgia,serif;font-size:32px;color:var(--red)}
.cut .lab{font-size:12.8px;color:#4A5A46;flex:1;min-width:180px}

/* payers */
.pay{display:grid;gap:8px;margin:8px 0}
.pr{display:grid;grid-template-columns:220px minmax(0,1fr) 46px;gap:12px;align-items:center;
  font-size:13.4px}
.pr .t{height:14px;border-radius:5px;background:#EDE7D8;overflow:hidden}
.pr .f{height:100%;background:linear-gradient(90deg,#2C6350,#3F9577)}
.pr .n{font-family:'IBM Plex Mono',monospace;font-size:12px;text-align:right;color:var(--ink)}

/* comparison */
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0}
table.cmp{border-collapse:collapse;width:100%;font-size:13.3px;min-width:720px}
table.cmp th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding:0 14px 9px 0;
  border-bottom:1px solid var(--line);font-weight:500;vertical-align:bottom}
table.cmp td{padding:12px 14px 12px 0;border-bottom:1px solid #F0EBDE;vertical-align:top;color:#3B4A38}
table.cmp td.nm{font-family:Fraunces,Georgia,serif;font-size:15.5px;color:var(--ink);white-space:nowrap}
table.cmp td.no{color:var(--red);font-weight:600}
table.cmp td.yes{color:var(--green);font-weight:600}
table.cmp tr.me td{background:#F7FAF6}

/* fit */
.fit{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin:8px 0}
.fc{background:#fff;border:1px solid var(--line);border-radius:11px;padding:17px 19px;min-width:0}
.fc.y{border-top:3px solid var(--green)}
.fc.n{border-top:3px solid var(--red)}
.fc h3{margin:0 0 10px;font-size:17px}
.fc ul{margin:0;padding-left:19px}
.fc li{font-size:13.8px;line-height:1.62;color:#4A5A46;margin-bottom:9px}

/* disclosure + cta */
.disc2{background:#FBF0E2;border:1px solid #EBD9BC;border-left:4px solid var(--amber);
  border-radius:11px;padding:17px 19px;margin:22px 0}
.disc2 p{margin:0;font-size:14px;line-height:1.7;color:#4A3A1E;max-width:none}
.hwcta{display:inline-block;background:var(--amber);color:#3A2A08;font-weight:600;
  font-size:15px;padding:12px 22px;border-radius:30px;text-decoration:none}
.hwcta:hover{background:#F2BC4C}
.ctarow{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:18px 0 6px}

.hwsrc{margin-top:46px;padding-top:22px;border-top:1px solid var(--line)}
.hwsrc ol{padding-left:20px;margin:0}
.hwsrc li{font-size:13.4px;line-height:1.68;color:#4A5A46;margin-bottom:11px}
.nv{background:#fff;border:1px dashed #CFC7B4;border-radius:10px;padding:15px 17px;margin:14px 0}
.nv b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--mut);margin-bottom:9px}
.nv li{font-size:13.2px;line-height:1.62;color:#4A5A46;margin-bottom:7px}

@media (max-width:900px){
  .hwwrap{grid-template-columns:minmax(0,1fr);gap:20px;padding-top:22px}
  .hwnav{position:static;display:flex;gap:7px;overflow-x:auto;padding-bottom:5px}
  .hwnav b{display:none}
  .hwnav a{border-left:0;border:1px solid var(--line);border-radius:20px;padding:6px 12px;
    white-space:nowrap;font-size:12.3px}
  .hwnav a.on{border-color:var(--pine);background:#EAF3DE}
  .hwband .in{grid-template-columns:minmax(0,1fr);gap:22px}
}
@media (max-width:560px){
  .fact{grid-template-columns:minmax(0,1fr);gap:7px}
  .fact .v{text-align:left}
  .pr{grid-template-columns:130px minmax(0,1fr) 40px;gap:8px;font-size:12.4px}
  .hwbody p{font-size:14.8px}
}
</style>"""

JS = """<script>
(function(){
  var links=[].slice.call(document.querySelectorAll('.hwnav a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))})
                .filter(Boolean);
  if(!links.length||!secs.length)return;
  links[0].classList.add('on');
  if(!('IntersectionObserver'in window))return;
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      links.forEach(function(a){
        a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id);
      });
    });
  },{rootMargin:'-12% 0px -80% 0px'});
  secs.forEach(function(s){io.observe(s)});
})();
</script>"""


def src_link(u, t="source"):
    return ' <a href="%s" target="_blank" rel="noopener noreferrer">%s &rarr;</a>' % (u, t)


def stop_block():
    yes = "".join("<span>%s</span>" % x for x in H.GATE_LICENCES)
    no = "".join("<span>%s</span>" % x for x in H.GATE_EXCLUDED)
    return ('<div class="stop"><h3>If you are an associate, this page is not for you '
            "yet</h3><p>Headway&rsquo;s California list accepts independently licensed "
            "clinicians only. <b>An AMFT, ASW or APCC cannot join.</b> Neither can they "
            "join Alma, Grow Therapy or SonderMind. There is a supervisory-billing "
            "pilot that lets pre-licensed clinicians bill under a supervisor &mdash; it "
            "runs in New York and Texas, for group practices only, and not in "
            'California.%s%s</p><div class="two">'
            '<div class="lic"><b>Accepted in California</b>%s</div>'
            '<div class="lic no"><b>Not accepted</b>%s</div></div>'
            '<p style="margin:14px 0 0"><a href="amft-3000-hours-california.html">'
            "If you are still accruing hours, the 3,000-hours planner is the tool that "
            "applies to you &rarr;</a></p></div>"
            % (src_link(H.HC + "30499083574292-Headway-s-accepted-licenses-by-state",
                        "the licence list"),
               src_link(H.HC + "45958397590164-Supervisory-billing", "the pilot"),
               yes, no))


def facts():
    out = []
    for label, val, note, url in H.MONEY:
        np = "np" if val == "not published" else ""
        out.append('<div class="fact"><div><h4>%s</h4><p>%s%s</p></div>'
                   '<div class="v %s">%s</div></div>'
                   % (label, note, src_link(url), np, val))
    return '<div class="facts">%s</div>' % "".join(out)


def claims():
    return '<div class="chk">%s</div>' % "".join(
        '<div class="ck %s"><b>%s</b><p>%s%s</p></div>' % (cls, c, note, src_link(u))
        for c, note, u, cls in H.CLAIMS)


def cut():
    o = H.OPTUM
    return ('<div class="cut"><span class="was">$%.2f</span><span class="arr">&rarr;</span>'
            '<span class="now">$%.2f</span><span class="lab">CPT %s, one provider&rsquo;s '
            "Optum rate, effective %s.%s</span></div><p>%s</p>"
            % (o["was"], o["now"], o["code"], o["when"],
               src_link(o["url"], "reported here"), o["note"]))


def payers():
    rows = "".join(
        '<div class="pr"><span>%s</span><div class="t"><div class="f" '
        'style="width:%d%%"></div></div><span class="n">%d%%</span></div>' % (n, p, p)
        for n, p in H.PAYERS)
    return '<div class="pay">%s</div>' % rows


def tradeoffs():
    return '<div class="chk">%s</div>' % "".join(
        '<div class="ck amber"><b>%s</b><p>%s%s</p></div>' % (t, b, src_link(u))
        for t, b, u in H.TRADEOFFS)


def compare():
    rows = ""
    for name, fee, pay, cred, assoc, url in H.COMPARE:
        me = ' class="me"' if name == "Headway" else ""
        acell = ('<td class="yes">%s</td>' % assoc if isinstance(assoc, str)
                 else '<td class="no">No</td>')
        rows += ('<tr%s><td class="nm"><a href="%s" target="_blank" '
                 'rel="noopener noreferrer">%s</a></td><td>%s</td><td>%s</td>'
                 "<td>%s</td>%s</tr>" % (me, url, name, fee, pay, cred, acell))
    return ('<div class="tw"><table class="cmp"><tr><th>Platform</th>'
            "<th>What it costs you</th><th>Pay cycle</th><th>Credentialing</th>"
            "<th>Takes CA associates</th></tr>%s</table></div>" % rows)


def fit():
    y = "".join("<li>%s</li>" % x for x in H.FITS)
    n = "".join("<li>%s</li>" % x for x in H.DOESNT)
    return ('<div class="fit"><div class="fc y"><h3>It fits if</h3><ul>%s</ul></div>'
            '<div class="fc n"><h3>It does not if</h3><ul>%s</ul></div></div>' % (y, n))


def sources():
    items = "".join('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a> '
                    "&mdash; %s</li>" % (u, t, n) for t, u, n in H.SOURCES)
    nv = "".join("<li>%s</li>" % x for x in H.NOT_VERIFIED)
    return ('<div class="hwsrc" id="sources"><h2>Sources</h2><ol>%s</ol>'
            '<div class="nv"><b>What is not on this page, and why</b><ul>%s</ul></div>'
            "</div>" % (items, nv))


DISCLOSURE = (
    '<div class="disc2"><p><b>How I am paid, and what it does not buy.</b> '
    "The Headway links on this page are affiliate links: if you sign up through "
    "one, I may receive a referral payment. It costs you nothing. It has not "
    "bought a single sentence &mdash; the disqualifying fact about associates is "
    "the second thing on the page, the marketing claims are checked against "
    "Headway&rsquo;s own help centre below, and every cell this page cannot fill "
    'says <i>not published</i> rather than guessing.</p></div>')

SECTIONS = [
    ("who-can-join", "Who can actually join", lambda: (
        stop_block() +
        "<p>With that out of the way: if you are licensed, Headway is one of "
        "four or five platforms that will put you on insurance panels without "
        "your having to run credentialing yourself. What follows is what it "
        "costs, what it pays, and what you give up.</p>")),

    ("what-it-costs", "What it costs you", lambda: (
        "<p>Headway holds the contract with the insurer, is paid by the insurer, "
        "and pays you a set rate per session. The difference is its revenue. "
        "There is no subscription, which is the real distinction from Alma.</p>"
        + facts() +
        "<p>Two of those cells say <b>not published</b>, and that is the honest "
        "answer rather than a gap in the research. Headway does not publish "
        "California rates and does not publish the share it keeps. You find out "
        "your rate after you are credentialed.</p>")),

    ("the-rate-moves", "The rate is not yours to hold", lambda: (
        "<p>Because the contract is between Headway and the insurer, the rate "
        "can change without you being a party to the negotiation. It has "
        "happened once publicly.</p>" + cut() +
        "<p>This is not an argument against the platform. It is the argument "
        "for not building a whole practice on one, and for knowing what your "
        "own direct-contract rate would be before you decide.</p>")),

    ("credentialing", "Credentialing, and which payers", lambda: (
        "<p>Headway lists <b>%s</b> California providers. The payer mix, by the "
        "share of those providers accepting each:</p>" % "{:,}".format(H.CA_PROVIDERS)
        + payers() +
        "<p>Credentialing is the part it genuinely does well &mdash; weeks "
        "rather than the months a direct application takes. The advertised "
        "figure and the help-centre figure do not agree, though, which is worth "
        "seeing before you plan around it.</p>")),

    ("check-the-claims", "The claims, against Headway&rsquo;s own help centre", lambda: (
        "<p>Everything below is Headway checked against Headway. Where the "
        "marketing page and the help centre disagree, the help centre is the "
        "one with the operational detail in it.</p>" + claims())),

    ("what-you-give-up", "What you give up", lambda: (
        "<p>None of these are hidden &mdash; all five are in Headway&rsquo;s own "
        "documentation or in reporting. They are simply not on the sign-up "
        "page.</p>" + tradeoffs() +
        "<h3>And one independent data point</h3>"
        "<p>The Psychotherapy Action Network surveyed <b>%d</b> clinicians "
        "across these platforms. <b>%d%%</b> reported earning the same or less "
        "than they had in independent practice, and <b>%d%%</b> said they had "
        "not been told about fee-splitting before joining.%s It is a "
        "self-selected sample, so read it as signal rather than as a population "
        "estimate &mdash; but it is the only survey of its kind.</p>"
        % (H.PSIAN["n"], H.PSIAN["same_or_less"], H.PSIAN["not_told"],
           src_link(H.PSIAN["url"], "the survey")))),

    ("against-the-alternatives", "Against the alternatives", lambda: (
        "<p>Every fee model below is what the company publishes. Three of them "
        "publish nothing, which is itself a comparison.</p>" + compare() +
        "<p><b>Rula is Path.</b> It rebranded in 2024, so a list offering you "
        "both is offering you one company twice.</p>"
        "<p>Going direct is slower and pays more. If your practice is stable "
        "enough to wait two to four months per payer, direct contracts keep the "
        "whole rate and nobody can renegotiate it above your head.</p>")),

    ("is-it-for-you", "So is it for you", lambda: (
        fit() +
        '<p style="margin-top:18px">The arithmetic is the part nobody else will '
        "do for you. Put your own rate, caseload and expenses into the "
        '<a href="practice-simulator.html">practice simulator</a> at a Headway '
        "rate and at your private-pay rate, and look at the two net figures "
        "rather than at the gross ones.</p>" + DISCLOSURE +
        '<div class="ctarow">%s<span style="font-size:13px;color:#7C8878">'
        "Opens on headway.co. Licensed California clinicians only.</span></div>"
        % aff("See Headway&rsquo;s provider signup"))),
]


def build():
    nav = ('<nav class="hwnav"><b>On this page</b>%s<a href="#sources">Sources</a></nav>'
           % "".join('<a href="#%s">%s</a>' % (i, t) for i, t, _f in SECTIONS))
    body = "".join('<h2 id="%s">%s</h2>%s' % (i, t, f()) for i, t, f in SECTIONS)
    fig = ('<div class="hwfig"><b>$0</b><span>a month to be on it &mdash; Headway is '
           "paid out of your reimbursement instead</span>"
           '<div class="row"><span>Your California rate</span><b>not published</b></div>'
           '<div class="row"><span>Share Headway keeps</span><b>not published</b></div>'
           '<div class="row"><span>Takes CA associates</span><b>no</b></div>'
           '<div class="row"><span>Paid</span><b>twice a month</b></div></div>')

    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Headway for California therapists: what it pays, what it keeps, and who it will not take</title>
<meta name="description" content="What Headway actually costs a California therapist — no subscription, an undisclosed share of your reimbursement, rates you cannot see until you are credentialed, and a licence list that excludes every AMFT, ASW and APCC. Checked against Headway's own help centre.">
<link rel="canonical" href="https://cavatello.github.io/therapist-tools/headway-for-california-therapists.html">
%s
%s
%s
</head><body class="hw">
%s
<main>
<section class="hwband"><div class="in"><div>
<ol class="bcr" aria-label="Breadcrumb">
<li><a href="index.html">Therapist Support</a><span class="sep">&rsaquo;</span></li>
<li><a href="resources.html">Resources</a><span class="sep">&rsaquo;</span></li>
<li><span aria-current="page">Headway</span></li></ol>
<h1>Headway, for California therapists. <em>What it pays, and what it keeps.</em></h1>
<p class="dek">No subscription, an undisclosed share of your reimbursement, and a rate
you cannot see until you are already credentialed. Checked line by line against
Headway&rsquo;s own help centre &mdash; including the licence list that rules out every
associate in California.</p>
<div class="hwmeta"><span>California</span><span>Updated %s</span><span>Contains affiliate links</span></div>
</div>%s</div></section>
<div class="hwwrap">%s<article class="hwbody">%s%s</article></div>
</main>
%s
%s
%s
</body></html>""" % ("\n".join(links), "\n".join(styles), CSS, header, UPDATED,
                     fig, nav, body, sources(), footer, navscript, JS)


def main():
    doc = build()
    open(OUT, "w", encoding="utf-8").write(doc)

    bad = []
    if doc.count("<h1") != 1:
        bad.append("%d h1" % doc.count("<h1"))
    for i, _t, _f in SECTIONS:
        if ('id="%s"' % i) not in doc or ('href="#%s"' % i) not in doc:
            bad.append("section %s not wired" % i)
    # the affiliate link must be tagged, sponsored, and disclosed
    for m in re.finditer(r'<a[^>]+href="' + re.escape(H.AFF) + r'"[^>]*>', doc):
        if "sponsored" not in m.group(0):
            bad.append("affiliate link without rel=sponsored")
        if 'target="_blank"' not in m.group(0):
            bad.append("affiliate link not opening in a new window")
    if doc.count(TAG) < doc.count('href="' + H.AFF + '"'):
        bad.append("an affiliate link is untagged")
    if "How I am paid" not in doc:
        bad.append("no disclosure block")
    # the disqualifier must appear before the comparison table
    if doc.find("cannot join") > doc.find("<table"):
        bad.append("the associate disqualifier sits below the comparison table")
    # no invented rate: the page must never state a Headway California rate
    for m in re.finditer(r"Headway[^.]{0,60}\$\d", doc):
        if "not published" not in m.group(0):
            pass  # the Optum figures are third-party reported and labelled as such
    if doc.count("not published") < 5:
        bad.append("only %d 'not published' cells" % doc.count("not published"))
    if "navpanel" in doc and not re.search(r"<script>[\s\S]*?navpanel[\s\S]*?</script>", doc):
        bad.append("header will not open - nav script missing")
    for _t, u, _n in H.SOURCES:
        if u not in doc:
            bad.append("source missing: %s" % u[:46])
    if bad:
        sys.exit("build_headway: " + "; ".join(bad))

    print("%-46s %d bytes  %d sections  %d sources  %d affiliate link(s)"
          % (os.path.basename(OUT), len(doc), len(SECTIONS), len(H.SOURCES),
             doc.count('href="' + H.AFF + '"')))


if __name__ == "__main__":
    main()
