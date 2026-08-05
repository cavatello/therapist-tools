#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three directions for a Help Scout-style content hub, at fidelity.

Built to be judged side by side, so all three use the site's real design tokens
(Fraunces / Inter / IBM Plex Mono, pine, gold, cream) and the same nine real
articles. The differences between them are structural, not cosmetic.

A - THE DESK        closest to Help Scout. Purpose-statement hero, most recent,
                    then topic rails by career stage, newsletter mid-page.
B - FIELD NOTES     editorial. One lead story carrying a real figure, then a
                    dated reading list. Extends the rates.html dossier look.
C - THE ANSWER INDEX question-led. The hero is a filter; content is indexed by
                    what a therapist actually types, mixing articles and tools.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from articles import ARTICLES

STAGE = {"pre": "Pre-licensed", "new": "Newly licensed", "run": "Running a practice"}

CSS = """
:root{--pine:#2C6350;--deep:#17271F;--dark:#1E4436;--pop:#F6C560;--paper:#FBF6E9;
 --white:#FFFDF6;--ink:#17271F;--muted:#5D574C;--line:#E4DCC8;--green:#3F9577}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:Inter,system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
.pw{max-width:1120px;margin:0 auto;padding:0 26px}
h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:600;letter-spacing:-.02em;margin:0}
.mono{font-family:'IBM Plex Mono',ui-monospace,monospace}

/* ---- mock chrome */
.switch{position:sticky;top:0;z-index:50;background:var(--deep);color:#EFF5F2;
 padding:11px 0;border-bottom:2px solid var(--pop)}
.switch .pw{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.switch b{font-family:Fraunces,serif;font-size:14px;margin-right:6px}
.switch a{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;
 text-transform:uppercase;text-decoration:none;padding:7px 13px;border-radius:999px;
 border:1px solid rgba(255,255,255,.28);min-height:32px;display:inline-flex;align-items:center}
.switch a:hover{background:rgba(255,255,255,.1)}
.vlabel{background:var(--pop);color:#2A2010;padding:26px 0 22px}
.vlabel h2{font-size:clamp(20px,2.4vw,26px)}
.vlabel p{margin:6px 0 0;font-size:13.6px;line-height:1.6;max-width:74ch;color:#4A3A18}
.vlabel span{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;
 text-transform:uppercase;display:block;margin-bottom:7px;opacity:.72}

/* ---- shared bits */
.kick{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.14em;
 text-transform:uppercase;color:var(--pop);margin:0 0 12px}
.tag{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--pine);font-weight:600}
.rt{font-family:'IBM Plex Mono',monospace;font-size:10.5px;color:#8A8477}
.more{display:inline-flex;align-items:center;min-height:40px;font-size:13.4px;
 font-weight:700;color:var(--pine);text-decoration:none;border-bottom:2px solid var(--pop);
 padding-bottom:1px}

/* ================================================= A - THE DESK */
.a-hero{background:linear-gradient(135deg,#141712 0%,#1E241C 52%,#2C6350 100%);
 color:#EFF5F2;padding:52px 0 48px}
.a-hero h1{font-size:clamp(28px,4vw,46px);line-height:1.06;color:#fff;max-width:20ch}
.a-hero h1 em{font-style:normal;color:var(--pop)}
.a-hero p{font-size:16px;line-height:1.7;color:rgba(255,255,255,.86);max-width:60ch;
 margin:15px 0 0}
.a-sec{padding:40px 0 6px}
.a-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;
 flex-wrap:wrap;margin-bottom:16px;border-bottom:1px solid var(--line);padding-bottom:11px}
.a-head h2{font-size:clamp(19px,2.2vw,24px)}
.a-head .st{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.1em;
 text-transform:uppercase;color:#8A8477}
.a-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.a-card{background:var(--white);border:1px solid var(--line);border-radius:14px;
 padding:18px 19px;display:flex;flex-direction:column;gap:9px;text-decoration:none}
.a-card:hover{border-color:var(--pine)}
.a-card h3{font-size:16.5px;line-height:1.28}
.a-card p{margin:0;font-size:13.2px;line-height:1.62;color:var(--muted)}
.a-card .foot{margin-top:auto;padding-top:6px;display:flex;justify-content:space-between;
 align-items:center;gap:10px}
.a-lead{background:var(--white);border:1px solid var(--line);border-radius:16px;
 padding:26px 28px;display:grid;grid-template-columns:1.35fr .65fr;gap:26px;
 align-items:center;margin-bottom:22px;text-decoration:none}
.a-lead h3{font-size:clamp(21px,2.6vw,28px);line-height:1.16;margin-bottom:9px}
.a-lead p{margin:0;font-size:14.4px;line-height:1.68;color:var(--muted)}
.a-stat{background:var(--paper);border:1px solid var(--line);border-radius:12px;
 padding:18px;text-align:center}
.a-stat b{display:block;font-family:Fraunces,serif;font-size:clamp(28px,3.6vw,40px);
 color:var(--pine);line-height:1}
.a-stat span{display:block;font-size:11.6px;line-height:1.5;color:#8A8477;margin-top:7px}
.a-nl{background:var(--dark);color:#EFF5F2;border-radius:16px;padding:30px 32px;
 margin:34px 0 8px;display:grid;grid-template-columns:1.2fr .8fr;gap:26px;align-items:center}
.a-nl h2{font-size:clamp(19px,2.3vw,25px);color:#fff}
.a-nl p{margin:9px 0 0;font-size:13.6px;line-height:1.65;color:rgba(255,255,255,.82)}
.a-nl form{display:flex;gap:8px;flex-wrap:wrap}
.a-nl input{flex:1;min-width:170px;min-height:46px;border-radius:10px;border:0;
 padding:0 14px;font-size:14px;background:var(--white)}
.a-nl button{min-height:46px;border:0;border-radius:10px;background:var(--pop);
 color:#2A2010;font-weight:800;font-size:14px;padding:0 20px;cursor:pointer}
.a-tools{background:var(--white);border-top:1px solid var(--line);padding:36px 0 42px;
 margin-top:30px}
.a-tools .row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:14px}
.a-tool{border:1px solid var(--line);border-radius:12px;padding:15px 16px;
 text-decoration:none;background:var(--paper)}
.a-tool b{display:block;font-size:14px;margin-bottom:4px}
.a-tool span{font-size:12.2px;line-height:1.55;color:var(--muted)}

/* ================================================= B - FIELD NOTES */
.b-wrap{background:#F7F3E6}
.b-hero{padding:46px 0 30px;border-bottom:3px double var(--line)}
.b-hero .ey{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--pine);margin:0 0 14px}
.b-hero h1{font-size:clamp(30px,4.4vw,52px);line-height:1.02;max-width:16ch}
.b-hero h1 em{font-style:italic;color:var(--pine)}
.b-hero p{font-size:15.4px;line-height:1.75;color:var(--muted);max-width:56ch;margin:16px 0 0}
.b-lead{display:grid;grid-template-columns:1.5fr .9fr;gap:34px;padding:32px 0;
 border-bottom:1px solid var(--line);align-items:start}
.b-lead h2{font-size:clamp(24px,3.2vw,36px);line-height:1.1;margin-bottom:12px}
.b-lead .dek{font-size:15px;line-height:1.75;color:var(--muted);margin:0 0 14px}
.b-gap{border-left:3px solid var(--pop);padding:4px 0 4px 18px}
.b-gap b{display:block;font-family:Fraunces,serif;font-size:clamp(34px,4.6vw,52px);
 line-height:1;color:var(--pine)}
.b-gap span{display:block;font-size:12.4px;line-height:1.55;color:#8A8477;margin-top:8px;
 max-width:26ch}
.b-list{padding:8px 0 34px}
.b-item{display:grid;grid-template-columns:104px 1fr 108px;gap:22px;padding:20px 0;
 border-bottom:1px solid var(--line);text-decoration:none;align-items:baseline}
.b-item:hover h3{color:var(--pine)}
.b-item .when{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.08em;
 text-transform:uppercase;color:#8A8477;padding-top:3px}
.b-item h3{font-size:19px;line-height:1.26;margin-bottom:6px}
.b-item p{margin:0;font-size:13.4px;line-height:1.65;color:var(--muted);max-width:64ch}
.b-item .fig{text-align:right;font-family:Fraunces,serif;font-size:21px;color:var(--pine)}
.b-item .fig small{display:block;font-family:Inter,sans-serif;font-size:10.4px;
 color:#8A8477;margin-top:3px;line-height:1.4}
.b-side{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:20px}
.b-side h4{font-family:Fraunces,serif;font-size:15px;margin:0 0 4px}
.b-side p{font-size:12.6px;line-height:1.6;color:var(--muted);margin:0 0 14px}
.b-side a{display:block;font-size:13.2px;padding:9px 0;border-top:1px solid var(--line);
 text-decoration:none;font-weight:600}
.b-side a:hover{color:var(--pine)}

/* ================================================= C - ANSWER INDEX */
.c-hero{background:var(--deep);color:#EFF5F2;padding:44px 0 40px}
.c-hero h1{font-size:clamp(26px,3.6vw,42px);line-height:1.08;color:#fff;max-width:19ch}
.c-hero h1 em{font-style:normal;color:var(--pop)}
.c-hero p{font-size:15px;line-height:1.7;color:rgba(255,255,255,.84);max-width:56ch;
 margin:14px 0 20px}
.c-filters{display:flex;gap:8px;flex-wrap:wrap}
.c-filters button{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;
 text-transform:uppercase;min-height:40px;padding:0 15px;border-radius:999px;cursor:pointer;
 background:transparent;color:#EFF5F2;border:1px solid rgba(255,255,255,.34)}
.c-filters button.on{background:var(--pop);color:#2A2010;border-color:var(--pop);font-weight:700}
.c-body{padding:34px 0 44px}
.c-q{border-bottom:1px solid var(--line)}
.c-q>div{display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center;
 padding:17px 2px;text-decoration:none;cursor:pointer}
.c-q h3{font-size:17.5px;line-height:1.3;font-family:Inter,sans-serif;font-weight:600;
 letter-spacing:0}
.c-q .meta{display:flex;gap:11px;align-items:center;margin-top:5px}
.c-q .goes{font-family:'IBM Plex Mono',monospace;font-size:10.4px;letter-spacing:.06em;
 text-transform:uppercase;color:#8A8477;white-space:nowrap}
.c-q .arrow{font-size:19px;color:var(--pine)}
.c-q.tool>div{background:linear-gradient(90deg,rgba(246,197,96,.16),transparent 62%);
 margin:0 -10px;padding-left:12px;padding-right:12px;border-radius:8px}
.c-note{background:var(--white);border:1px solid var(--line);border-left:3px solid var(--pine);
 border-radius:0 12px 12px 0;padding:16px 18px;margin:26px 0 0;font-size:13.2px;
 line-height:1.65;color:var(--muted)}
.c-note b{color:var(--ink)}

@media(max-width:900px){
 .a-grid,.a-tools .row{grid-template-columns:1fr}
 .a-lead,.a-nl,.b-lead{grid-template-columns:1fr}
 .b-item{grid-template-columns:1fr;gap:7px}
 .b-item .fig{text-align:left}
 .b-item .when{padding-top:0}
}
"""


def card(a):
    k, t, d, s, sl, m, st = a
    return ('<a class="a-card" href="#"><span class="tag">' + k + "</span>"
            + "<h3>" + t + "</h3><p>" + d[:118] + "&hellip;</p>"
            + '<span class="foot"><span class="rt">' + str(m) + " min read</span>"
            + '<span class="rt">' + STAGE[st] + "</span></span></a>")


def variant_a():
    o = []
    o.append('<section class="a-hero"><div class="pw">'
             '<p class="kick">Therapist Support &middot; the practice desk</p>'
             "<h1>The business side of a therapy practice, <em>worked out</em>.</h1>"
             "<p>Written for California therapists, and every figure in it is either "
             "computed from your own numbers or cited to the page it came from. No "
             "course at the end of it.</p></div></section>")

    o.append('<div class="pw"><section class="a-sec">'
             '<div class="a-head"><h2>Start here</h2>'
             '<span class="st">Most read this month</span></div>')
    a = ARTICLES[0]
    o.append('<a class="a-lead" href="#"><div><span class="tag">' + a[0] + "</span>"
             "<h3>" + a[1] + "</h3><p>" + a[2] + "</p></div>"
             '<div class="a-stat"><b>' + a[3] + "</b><span>" + a[4] + "</span></div></a>")
    o.append('<div class="a-grid">' + "".join(card(x) for x in ARTICLES[1:4]) + "</div>")
    o.append("</section>")

    for stage in ("pre", "new", "run"):
        rows = [x for x in ARTICLES if x[6] == stage][:3]
        if not rows:
            continue
        o.append('<section class="a-sec"><div class="a-head"><h2>' + STAGE[stage] + "</h2>"
                 '<a class="more" href="#">View more posts &rarr;</a></div>'
                 '<div class="a-grid">' + "".join(card(x) for x in rows) + "</div></section>")

    o.append('<section class="a-nl"><div><h2>One email a month. What changed in the numbers.</h2>'
             "<p>When the Board moves a fee, when the IRS publishes next year&rsquo;s limits, "
             "when a panel closes to new applicants. Nothing else.</p></div>"
             '<form onsubmit="return false"><input placeholder="you@practice.com">'
             "<button>Count me in</button></form></section></div>")

    o.append('<section class="a-tools"><div class="pw">'
             '<div class="a-head"><h2>The tools underneath</h2>'
             '<span class="st">Free, no account</span></div><div class="row">'
             '<a class="a-tool" href="#"><b>Practice simulator</b><span>What a California '
             "practice actually leaves you</span></a>"
             '<a class="a-tool" href="#"><b>Tax &amp; retirement</b><span>How much of the '
             "bill is optional</span></a>"
             '<a class="a-tool" href="#"><b>Grow your practice</b><span>What a client is '
             "worth, and where they come from</span></a>"
             '<a class="a-tool" href="#"><b>Job advisor</b><span>What a placement pays, and '
             "when it closes</span></a>"
             "</div></div></section>")
    return "".join(o)


def variant_b():
    o = ['<div class="b-wrap"><div class="pw">']
    o.append('<section class="b-hero"><p class="ey">Field Notes &middot; California '
             "&middot; since 2025</p>"
             "<h1>Reporting on the <em>money side</em> of a therapy practice.</h1>"
             "<p>Research documents, not blog posts. Each one names its sources, admits its "
             "sample size, and shows the arithmetic that produced the headline number.</p>"
             "</section>")

    a = ARTICLES[6]
    o.append('<section class="b-lead"><div><span class="tag">' + a[0] + " &middot; the lead</span>"
             "<h2>" + a[1] + "</h2>"
             '<p class="dek">' + a[2] + "</p>"
             '<a class="more" href="#">Read the full document &rarr;</a></div>'
             '<div><div class="b-gap"><b>' + a[3] + "</b><span>" + a[4] + "</span></div>"
             '<div class="b-side" style="margin-top:20px"><h4>New here?</h4>'
             "<p>Three documents that explain how the rest of this is put together.</p>"
             '<a href="#">How we count a rate &rarr;</a>'
             '<a href="#">Where the tax figures come from &rarr;</a>'
             '<a href="#">What we will not publish &rarr;</a></div></div></section>')

    o.append('<section class="b-list">')
    when = ["5 Aug", "2 Aug", "28 Jul", "21 Jul", "14 Jul", "9 Jul", "1 Jul", "24 Jun"]
    for i, x in enumerate([y for y in ARTICLES if y is not a][:8]):
        o.append('<a class="b-item" href="#">'
                 '<span class="when">' + when[i] + "<br>" + x[0] + "</span>"
                 "<div><h3>" + x[1] + "</h3><p>" + x[2][:150] + "&hellip;</p></div>"
                 '<span class="fig">' + x[3] + "<small>" + x[4] + "</small></span></a>")
    o.append("</section></div></div>")
    return "".join(o)


def variant_c():
    QS = [
     ("Can I see a client who has moved to another state?", "Telehealth", "Article", False),
     ("Should I incorporate, or stay a sole proprietor?", "Money", "Tool &middot; Tax", True),
     ("What should I be charging?", "Rates", "Article", False),
     ("How much will I actually take home?", "Practice", "Tool &middot; Simulator", True),
     ("Which of my 3,000 hours is holding me up?", "Licensure", "Tool &middot; 3,000 hours", True),
     ("Is this job offer any good?", "Licensure", "Tool &middot; Job advisor", True),
     ("What does joining a panel involve?", "Getting paid", "Article", False),
     ("Do I have to give clients a written estimate?", "Getting paid", "Article", False),
     ("Can I afford to drop insurance?", "Rates", "Article", False),
     ("What does it cost to live here on this income?", "Practice", "Tool &middot; Cost of living", True),
    ]
    o = ['<section class="c-hero"><div class="pw">'
         '<p class="kick">Therapist Support</p>'
         "<h1>Start with the question you <em>actually</em> came with.</h1>"
         "<p>Everything here is indexed by what therapists type, not by what we felt like "
         "writing. Some answers are a document; some are a calculator that uses your own "
         "numbers.</p>"
         '<div class="c-filters">'
         '<button class="on">Everything</button><button>Pre-licensed</button>'
         "<button>Newly licensed</button><button>Running a practice</button>"
         "<button>Just the tools</button></div></div></section>"]
    o.append('<div class="c-body"><div class="pw">')
    for q, cat, goes, is_tool in QS:
        o.append('<div class="c-q' + (" tool" if is_tool else "") + '"><div>'
                 "<div><h3>" + q + "</h3>"
                 '<div class="meta"><span class="tag">' + cat + "</span>"
                 '<span class="goes">' + goes + "</span></div></div>"
                 '<span class="arrow">&rarr;</span></div></div>')
    o.append('<div class="c-note"><b>Why the gold rows look different.</b> A shaded row '
             "hands you a calculator that runs on your own numbers; a plain row is something "
             "to read. The distinction is the whole point &mdash; you should never have to "
             "guess whether a link is going to do the arithmetic for you.</div>")
    o.append("</div></div>")
    return "".join(o)


VARIANTS = [
 ("A", "The Desk", "Closest to Help Scout",
  "Purpose-statement hero with no image, a lead story, then rails by career stage each "
  "capped at three cards with a &ldquo;view more&rdquo;, newsletter mid-page, tools at the "
  "foot. Scales to hundreds of articles and is the most familiar shape to anyone who reads "
  "SaaS blogs. Weakest on what makes this site unusual, which is that it computes things.",
  variant_a),
 ("B", "Field Notes", "Editorial, extends rates.html",
  "One lead document carrying a real figure, then a dated reading list where every row shows "
  "its headline number. Leans on the &ldquo;research dossier&rdquo; look already built for "
  "rates.html. Strongest identity and the best fit for citation-heavy work; the reading list "
  "gets long before it needs sectioning, so it suits ~40 documents rather than 400.",
  variant_b),
 ("C", "The Answer Index", "Question-led, mixes tools and reading",
  "The hero is a filter and the index is organised by what a therapist actually types. Tools "
  "and articles sit in one list, visually distinguished, so a calculator is a legitimate "
  "answer to a question. This is what the project&rsquo;s own information-scent doctrine "
  "argues for (see claude/content-block-system.md), and the least like a blog.",
  variant_c),
]


def main():
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8">'
             '<meta name="viewport" content="width=device-width,initial-scale=1">'
             "<title>Content hub &mdash; three directions</title>"
             '<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,'
             '400;9..144,600&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700;800'
             '&display=swap" rel="stylesheet">'
             "<style>" + CSS + "</style></head><body>"]
    parts.append('<div class="switch"><div class="pw"><b>Three directions</b>'
                 + "".join('<a href="#v%s">%s &mdash; %s</a>' % (v[0], v[0], v[1])
                           for v in VARIANTS)
                 + "</div></div>")
    for code, name, tagline, blurb, fn in VARIANTS:
        parts.append('<section class="vlabel" id="v' + code + '"><div class="pw">'
                     "<span>Direction " + code + " &middot; " + tagline + "</span>"
                     "<h2>" + name + "</h2><p>" + blurb + "</p></div></section>")
        parts.append(fn())
    parts.append("</body></html>")
    out = "".join(parts)
    dest = os.path.join(HERE, "content-hub-directions.html")
    open(dest, "w", encoding="utf-8").write(out)
    print("content-hub-directions.html  %d bytes  %d variants"
          % (len(out.encode("utf-8")), len(VARIANTS)))


if __name__ == "__main__":
    main()
