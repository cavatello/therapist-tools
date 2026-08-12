#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The information architecture, and a mockup of every door - revised.

WHY THIS SUPERSEDES HALF OF P2

`ops/stage-doors.html` drew sixteen mockups and picked one per door. Then the
first door shipped and two things came back from review that invalidate the
design half of that document:

  1. The hero was written for the wrong arrival. It opened with the tool -
     "One bar. Four gates." - which is what somebody already oriented wants.
     Most arrivals are cold, from a search for one specific question, and a
     cold arrival needs to know it is in the right place, that this is the
     whole thing, and where to start. None of which that hero said.

  2. "Gate" was jargon, and it pointed the wrong way. Four gates framed the
     3,000 as the thing you are working toward. The 3,000 is almost never
     what decides anybody's date.

Both are the same error: designing from the inside out. So this document
rebuilds every door around one pattern that answers the cold arrival first,
and the pattern - not the individual mockups - is the actual proposal.

WHAT IS ALREADY TRUE, AND WHAT IS STILL A PROPOSAL

`/for/associates` is live and is the reference implementation. Its shape is
the pattern below, and everything else here is a claim that the same shape
works for the other four. The tagging, the SUBDIRS fix and the sitewide plain
words are shipped. The band, the nav change and the other four doors are not.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "information-architecture.html")
UPDATED = "12 August 2026"

NAV = [("pattern", "The pattern"), ("map", "The map"),
       ("doors", "Five doors"), ("journey", "How somebody arrives"),
       ("furniture", "On every page"), ("model", "URLs and data"),
       ("order", "Build order")]

EXTRA = """
.pat{display:grid;gap:0;margin:14px 0;border:2px solid var(--ink);
  box-shadow:5px 5px 0 var(--ink);background:var(--cream);overflow:hidden}
.pat .row{display:grid;grid-template-columns:44px 1fr;border-top:1px solid var(--line)}
.pat .row:first-child{border-top:0}
.pat .n{background:var(--deep);color:var(--gold);font-family:var(--mono);
  font-size:12px;display:grid;place-items:center;font-weight:600}
.pat .b{padding:11px 14px}
.pat h4{font-size:15.5px;margin:0 0 3px}
.pat p{font-size:14px;margin:0;color:#39473F}
.pat .ex{font-family:var(--mono);font-size:11.5px;color:var(--pine);
  background:#fff;border:1px solid var(--line);padding:5px 8px;margin-top:6px;
  display:inline-block}
.vs{display:grid;gap:12px;margin:12px 0}
@media(min-width:820px){.vs{grid-template-columns:1fr 1fr}}
.vs>div{border:2px solid var(--ink);padding:13px 15px}
.vs .bad{background:#FFF6F5;border-left:6px solid var(--red)}
.vs .good{background:#F2F8F4;border-left:6px solid var(--green)}
.vs .lab{display:block;margin-bottom:7px}
.vs .hl{font-family:var(--sans);font-weight:800;font-size:19px;line-height:1.2;
  margin:0 0 6px}
.vs p{font-size:13.5px;margin:0}
.doorbar{display:grid;gap:10px;margin:12px 0 6px}
@media(min-width:900px){.doorbar{grid-template-columns:repeat(5,1fr)}}
.doorbar div{border:2px solid var(--ink);background:var(--cream);padding:11px 12px;
  box-shadow:3px 3px 0 var(--ink)}
.doorbar .u{font-family:var(--mono);font-size:10.5px;color:var(--pine);
  word-break:break-all;display:block;margin-bottom:4px}
.doorbar h4{font-size:14.5px;margin:0 0 4px}
.doorbar p{font-size:12px;margin:0;color:var(--muted)}
.doorbar .st{display:inline-block;margin-top:7px;font-family:var(--mono);font-size:9px;
  letter-spacing:.11em;text-transform:uppercase;border:1.5px solid var(--ink);padding:2px 6px}
.doorbar .st.live{background:var(--pine);color:#fff;border-color:var(--pine)}
.doorbar .st.next{background:var(--gold)}
.doorbar .st.hold{background:#fff}
.mkhero{background:var(--pine);color:#fff;margin:-18px -16px 14px;padding:18px 16px 16px;
  border-bottom:2px solid var(--ink)}
.mkhero .lab{color:var(--gold-on-pine)}
.mkhero h2{font-size:25px;color:#fff;margin:6px 0 7px;letter-spacing:-.02em;line-height:1.1}
.mkhero p{font-size:12.5px;color:#DAE8E1;margin:0;max-width:56ch}
.mkfig{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;background:var(--cream);
  border:2px solid var(--ink);padding:10px 12px;margin-top:12px}
.mkfig div .v{font-family:var(--fig);font-weight:800;font-size:19px;color:var(--deep);
  display:block;line-height:1.05}
.mkfig div .l{font-family:var(--mono);font-size:8.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);display:block;margin-top:2px}
.mkstart{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 12px}
.mkstart a{display:block;border:2px solid var(--ink);background:var(--pine);color:#fff;
  padding:9px 11px;text-decoration:none}
.mkstart .q{display:block;font-family:var(--sans);font-weight:800;font-size:13.5px;
  line-height:1.2}
.mkstart .s{display:block;font-size:11px;color:#CFE2D9;margin-top:3px;line-height:1.3}
.mkgrp{font-family:var(--sans);font-weight:800;font-size:13.5px;margin:12px 0 6px;
  padding-bottom:4px;border-bottom:2px solid var(--ink)}
.mkcards{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.mkcards div{border:2px solid var(--ink);background:var(--cream);padding:8px 10px}
.mkcards .t{font-family:var(--sans);font-weight:700;font-size:12.5px;line-height:1.2;
  display:block}
.mkcards .n{font-size:10.5px;color:var(--muted);line-height:1.35;display:block;margin-top:3px}
.trip{display:grid;gap:10px;margin:12px 0}
@media(min-width:900px){.trip{grid-template-columns:repeat(4,1fr)}}
.trip>div{border:2px solid var(--ink);background:#fff;padding:12px 13px;position:relative;
  box-shadow:4px 4px 0 var(--ink)}
.trip .s{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);display:block;margin-bottom:5px}
.trip h4{font-size:14.5px;margin:0 0 4px}
.trip p{font-size:12.5px;margin:0;color:#39473F}
.trip .hit{background:var(--gold)}
.axes{border:2px solid var(--ink);background:var(--cream);box-shadow:5px 5px 0 var(--ink);
  padding:0;overflow-x:auto;margin:12px 0}
.axes table{min-width:720px;margin:0}
.axes th:first-child,.axes td:first-child{position:sticky;left:0;background:var(--cream)}
.axes th{background:var(--deep)}
.axes td.x{text-align:center;font-family:var(--fig);font-weight:800;color:var(--pine);
  font-size:17px}
.axes td.o{text-align:center;color:var(--line)}
code{font-family:var(--mono);font-size:12.5px;background:#fff;border:1px solid var(--line);
  padding:1px 5px}
.note{border-left:5px solid var(--gold);padding:2px 0 2px 16px;margin:14px 0}
.note p{font-size:14.5px;margin:0 0 6px}
@media(max-width:700px){
  .mkfig,.mkstart,.mkcards{grid-template-columns:1fr 1fr}
  .mkhero h2{font-size:21px}
}
"""


def frame(url, inner):
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="mk"><div class="mkhead"><span class="brand">Therapist '
            'Support</span><span class="nv"><span>Calculators</span>'
            '<span>Money</span><span>Licensure</span><span>Getting paid</span>'
            '<span>Practice</span><span>For you</span></span></div>'
            '<div class="mkbody">%s</div></div></div>' % (url, inner))


def door(kicker, h1, lede, figs, starts, groups):
    o = ['<div class="mkhero"><span class="lab">%s</span><h2>%s</h2>'
         "<p>%s</p></div>" % (kicker, h1, lede)]
    o.append('<div class="mkfig">')
    for v, l in figs:
        o.append('<div><span class="v">%s</span><span class="l">%s</span></div>'
                 % (v, l))
    o.append("</div>")
    o.append('<span class="lab" style="display:block;margin-top:13px">'
             "Start here</span>")
    o.append('<div class="mkstart">')
    for q, s in starts:
        o.append('<a href="#"><span class="q">%s</span>'
                 '<span class="s">%s</span></a>' % (q, s))
    o.append("</div>")
    for name, cards in groups:
        o.append('<div class="mkgrp">%s</div><div class="mkcards">' % name)
        for t, n in cards:
            o.append('<div><span class="t">%s</span><span class="n">%s</span></div>'
                     % (t, n))
        o.append("</div>")
    return "".join(o)


DOORS = [
    ("/for/deciding", "next", "Deciding", "73 pages",
     "Thinking about it, or choosing between programs",
     door("For people thinking about becoming a therapist in California",
          "Everything you need before you apply, in one place.",
          "78 programs compared on cost, format and who finds your practicum "
          "site. Which of the three licenses to aim at, and why it is a "
          "statute question rather than a personality one. What it costs end "
          "to end, and what the work pays afterward.",
          [("78", "programs compared"), ("$37,800", "cheapest published"),
           ("5&ndash;6 yr", "realistic, not the floor"),
           ("$0", "and no account, ever")],
          [("Which license should I aim at?",
            "Only one of the three banks your practicum hours"),
           ("Which program, and what does it cost?",
            "All 78, priced, with the practicum question answered"),
           ("How long does this really take?",
            "Counted honestly, including the joins nobody advertises"),
           ("Can I afford the years I am not earning?",
            "The bill, before anybody sells you the vocation")],
          [("Choosing a license and a program",
            [("California MFT graduate programs",
              "All 78 the Board recognizes, compared"),
             ("Becoming a therapist as a career change",
              "The pipeline, the three licenses, the honest clock")]),
           ("What it costs, and what it pays",
            [("What county jobs pay therapists",
              "From payroll, not from job adverts"),
             ("Cost of living for California therapists",
              "What a month costs where you would work")])])),

    ("/for/students", "next", "In a program", "2 pages + 78 behind",
     "Enrolled, practicum approaching or underway",
     door("For California students in an MFT or counseling program",
          "Everything for the practicum year, in one place.",
          "Who finds your practicum site at each of the 78 programs, in their "
          "own words. The seven rules that decide whether a placement counts "
          "at all. And which of the hours you are logging now the Board will "
          "still be counting three years from now.",
          [("29 of 78", "publish nothing about placement"),
           ("7", "rules that decide if it counts"),
           ("1,300", "hours you can bank early"),
           ("$0", "and no account, ever")],
          [("Who finds my practicum site?",
            "Look up your program and read its own words"),
           ("Can I do my practicum in a private practice?",
            "No &mdash; not as an employee, not as a volunteer"),
           ("Do these hours count toward the 3,000?",
            "On the MFT route, up to 1,300 of them"),
           ("What happens between my degree and my number?",
            "90 days, and the clock starts at the award date")],
          [("Your practicum",
            [("The practicum year in California",
              "The seven rules, and all 78 programs compared"),
             ("California MFT graduate programs",
              "Your own program's page, with its sources")]),
           ("What comes next",
            [("Getting hired as a California associate",
              "Start reading this before you graduate, not after"),
             ("How long to 3,000 hours?",
              "What your practicum hours are worth once you register")])])),

    ("/for/associates", "live", "Counting hours", "20 pages &middot; LIVE",
     "Registered, working toward the 3,000",
     door("For California associates &middot; AMFT, ASW and APCC",
          "Everything a California associate needs, in one place.",
          "20 guides for the years between registration and your license "
          "&mdash; the hours and what counts toward them, why employers can "
          "or cannot hire you, what the work pays county by county, the loan "
          "repayment nobody mentions, and the Board&rsquo;s own numbers.",
          [("20", "guides for this stage"),
           ("58", "county job portals, checked"),
           ("165,000", "licensees in the register"),
           ("$0", "and no account, ever")],
          [("When do I actually finish?",
            "Your date, from the hours you are really logging"),
           ("Why is nobody hiring me?",
            "It is a billing rule, and it is not about your hour count"),
           ("What should this job pay?",
            "Salary against per-session, and what counties actually pay"),
           ("Do I have to work unpaid?",
            "No, and there is a wage claim with a deadline")],
          [("Your hours, and what counts toward them",
            [("How long to 3,000 hours?",
              "Which requirement is holding you up"),
             ("The practicum year in California",
              "What of your pre-degree hours the Board still counts")]),
           ("Getting hired, and what it pays",
            [("Getting hired as a California associate",
              "Why half your applications get no reply"),
             ("Where to apply, all 58 counties",
              "Including the seven whose obvious URL is somebody else")])])),

    ("/for/licensed", "hold", "Licensed", "19 pages",
     "Licensed, and running or joining a practice",
     door("For licensed California therapists &middot; LMFT, LCSW and LPCC",
          "What changed, and whether it applies to you.",
          "The rules that moved, newest first, each with the date it took "
          "effect and the date this page last checked it. Then the reference "
          "shelf: rates, panels, tax, records and the paperwork a private "
          "practice has to get right.",
          [("19", "guides for this stage"),
           ("Aug 2026", "last checked"),
           ("4", "rules changed this year"),
           ("$0", "and no account, ever")],
          [("Is my directory profile still compliant?",
            "The advertising rule changed on 1 April 2026"),
           ("What do I have to document per telehealth session?",
            "A duty that attaches to the session, not the file"),
           ("What does insurance actually pay?",
            "Per session, by payer, in California"),
           ("Sole proprietor or professional corporation?",
            "With the arithmetic attached, not the pitch")],
          [("What changed",
            [("What changed: fees, limits and rates",
              "Reverse chronological, each with its effective date"),
             ("California LMFT continuing education",
              "The 36 hours, and which six are mandatory")]),
           ("The reference shelf",
            [("What insurance actually pays per session",
              "By payer, in California"),
             ("Getting on insurance panels",
              "CAQH, PECOS, PAVE and the timelines")])])),

    ("/for/practice-owners", "hold", "Practice owner", "8 pages &mdash; too thin",
     "Employing other people, or about to",
     door("For California therapists running a practice",
          "The four decisions, each with the arithmetic attached.",
          "Not articles &mdash; calculators with your own numbers in them. "
          "Whether to incorporate, whether to hire, panels against private "
          "pay, and which software. Held until the queue lands: eight pages "
          "is not enough to open on, and three of them belong to the licensed "
          "door.",
          [("8", "pages &mdash; the reason it is held"),
           ("$1,248", "the SDI line the pitch forgets"),
           ("15", "EHR systems priced"),
           ("$0", "and no account, ever")],
          [("Incorporate, or stay a sole proprietor?",
            "The SDI line most comparisons leave out"),
           ("Can I afford to hire an associate?",
            "Break-even caseload, in your county"),
           ("Panels, or private pay?",
            "$38 to $250 for the same code"),
           ("Which EHR?", "15 systems, 14 with a published price")],
          [("The four decisions",
            [("Can a California therapist form an LLC?",
              "No &mdash; and what the actual choice is"),
             ("Hiring your first associate",
              "The real arithmetic, including supervision")])])),
]


def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block to inherit.")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>Information architecture, and every door &mdash; revised</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
         'opsz,wght@12..96,800&family=Fraunces:opsz,wght@9..144,600;9..144,800&'
         'family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&'
         'display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s &middot; revised '
             "after the first door shipped</span>"
             "<h1>One pattern, five doors.</h1>"
             "<p>Every landing page in the site, and the architecture "
             "underneath them. Rebuilt around the two corrections that came "
             "back from the live page: <b>lead with what the reader gets, not "
             "with the tool</b>, and <b>say it in words a stranger already "
             "knows</b>.</p>"
             '<div class="meta"><span class="chip">5 doors</span>'
             '<span class="chip">1 live</span>'
             '<span class="chip">No page moves</span>'
             '<span class="chip">Supersedes the design half of P2</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, l in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, l))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    # --------------------------------------------------------------- pattern
    o.append('<section id="pattern"><div class="kicker"><span class="n">01</span>'
             "<h2>The pattern every door follows</h2></div>")
    o.append('<p class="lede">This is the actual proposal. The five mockups '
             "further down are the same six blocks with different content, and "
             "if the pattern is right they will all work.</p>")

    o.append('<div class="vs">'
             '<div class="bad"><span class="lab">What shipped first, and was '
             "wrong</span>"
             '<p class="hl">&ldquo;One bar. Four gates. Nothing you type here '
             "leaves this browser.&rdquo;</p>"
             "<p>A headline describing a widget, two of four blocks about "
             "privacy, and four figures that were the statute &mdash; numbers "
             "the reader already knows. Written for somebody arriving from a "
             "link in a group, already oriented. A hub over twenty pages read "
             "as one calculator.</p></div>"
             '<div class="good"><span class="lab">What it says now</span>'
             '<p class="hl">&ldquo;Everything a California associate needs, in '
             "one place.&rdquo;</p>"
             "<p>The offer in the headline, the audience in the line above it, "
             "the scope in the line below, and figures about the "
             "<em>resource</em>: 20 guides, 58 portals checked, 165,000 "
             "licensees, $0. Then the four questions that actually bring "
             "people here.</p></div></div>")

    o.append('<div class="pat">')
    for n, h, p, ex in [
        ("01", "Who it is for, in the line above the headline",
         "A stranger decides in about a second whether a page is for them. "
         "Name them in their own words, including the licence letters they "
         "would search for.",
         "For California associates &middot; AMFT, ASW and APCC"),
        ("02", "The offer, as the headline",
         "Not what the page contains, not what it does. What the reader "
         "walks away with. The same sentence for every door, with one word "
         "changed, is a feature rather than a shortcut - it makes the set "
         "legible.",
         "Everything a California associate needs, in one place."),
        ("03", "The scope, in one paragraph",
         "How much of it there is, in concrete nouns, so nobody has to scroll "
         "to find out whether it is thin. Ends with the two things that "
         "separate this site from the rest of the results: every figure has a "
         "named source, and it is free.",
         "20 guides for the years between registration and your license &mdash;"),
        ("04", "Four figures about the resource, not the statute",
         "The old hero printed 3,000 / 1,750 / 500 / 104. A registered "
         "associate knows those. Print what they do not know: how much is "
         "here, how well checked it is, what it costs.",
         "20 guides &middot; 58 portals checked &middot; 165,000 licensees &middot; $0"),
        ("05", "Start here - the four questions that bring people",
         "Taken from what people actually search and post, phrased as they "
         "phrase it. This is the block that turns a hub into a route, and it "
         "is where a cold arrival self-selects without being asked to.",
         "Why is nobody hiring me?"),
        ("06", "The shelf, grouped and annotated",
         "Twenty flat cards is a wall; five headed groups is a table of "
         "contents. Each card carries what that page says AT THIS STAGE, from "
         "the registry, not the page's own summary - which is the whole "
         "difference between a stage hub and a re-listed topic hub.",
         "Which county to apply to first, from what each one actually paid"),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 '<h4>%s</h4><p>%s</p><span class="ex">%s</span></div></div>'
                 % (n, h, p, ex))
    o.append("</div>")

    o.append('<div class="note"><p><b>Where the tool goes.</b> If a door has an '
             "interactive piece &mdash; the associates ledger, the students "
             "lookup &mdash; it sits <em>after</em> block 05, not before it. "
             "The tool is what makes somebody stay; the first five blocks are "
             "what stops them leaving.</p>"
             "<p><b>And the words.</b> Requirement, not gate. Checkpoint, not "
             "gate. If a sentence needs the reader to learn a metaphor before "
             "it means anything, it is the wrong sentence for a page somebody "
             "found while worried.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ------------------------------------------------------------------- map
    o.append('<section id="map"><div class="kicker"><span class="n">02</span>'
             "<h2>The map</h2></div>")
    o.append('<p class="lede">Five doors, one per stage of the path. Stage is '
             "the <b>entry layer</b>; topic stays the organization; "
             "<b>no page moves</b>.</p>")
    o.append('<div class="doorbar">')
    for url, state, name, count, who, _ in DOORS:
        lab = {"live": "Live", "next": "Next", "hold": "Held"}[state]
        o.append('<div><span class="u">%s</span><h4>%s</h4><p>%s</p>'
                 '<span class="st %s">%s &middot; %s</span></div>'
                 % (url, name, who, state, lab, count))
    o.append("</div>")

    o.append('<p class="lab" style="display:block;margin-top:20px">Why stage '
             "and topic are different axes</p>")
    o.append('<div class="axes"><table>'
             "<tr><th>Page</th><th>Topic &mdash; where it is filed</th>"
             "<th>Deciding</th><th>Student</th><th>Associate</th>"
             "<th>Licensed</th><th>Owner</th></tr>")
    for page, topic, marks in [
        ("The practicum year", "Licensure", "01110"),
        ("What county jobs pay", "Getting paid", "10110"),
        ("Getting hired as an associate", "Licensure", "01100"),
        ("All 58 county job portals", "Licensure", "00110"),
        ("California MFT programs", "Licensure", "11000"),
        ("What insurance actually pays", "Getting paid", "10011"),
        ("Hiring your first associate", "Practice", "00001"),
    ]:
        cells = "".join('<td class="%s">%s</td>'
                        % (("x", "&bull;") if c == "1" else ("o", "&middot;"))
                        for c in marks)
        o.append("<tr><td>%s</td><td>%s</td>%s</tr>" % (page, topic, cells))
    o.append("</table></div>")
    o.append('<p class="src">One page belongs to exactly one topic and to as '
             "many stages as have something to say about it. That is why the "
             "annotation is mandatory: the county pay page tells a "
             "career-changer what the job pays at the end, and tells an "
             "associate which employer to apply to first. Same page, two "
             "sentences, and without them the second hub is just the first "
             "one again.</p>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- doors
    o.append('<section id="doors"><div class="kicker"><span class="n">03</span>'
             "<h2>Five doors</h2></div>")
    o.append('<p class="lede">Same six blocks every time. The associates door '
             "is live and rendered here from its real content; the other four "
             "are mockups using pages that already exist.</p>")
    for url, state, name, count, who, inner in DOORS:
        lab = {"live": "Live now", "next": "Proposed", "hold": "Held"}[state]
        o.append('<div class="vh"><span class="tag">%s</span><h4>%s</h4>'
                 '<span class="rec">%s</span></div>' % (url, name, lab))
        o.append("<p>%s. %s</p>" % (who, count))
        o.append(frame(url, inner))
    o.append("</section><hr class=\"rule\">")

    # --------------------------------------------------------------- journey
    o.append('<section id="journey"><div class="kicker"><span class="n">04</span>'
             "<h2>How somebody actually arrives</h2></div>")
    o.append('<p class="lede">The doors are five pages. Almost nobody lands on '
             "one. This is the journey the architecture has to serve, and the "
             "third step is the part that does not exist yet.</p>")
    o.append('<div class="trip">')
    for s, h, p, hit in [
        ("01", "A search, with a specific worry",
         "&ldquo;can amft hours be unpaid california&rdquo;. Not a browse. One "
         "question, asked at the worst moment.", False),
        ("02", "A leaf page, deep in the site",
         "They land on the wage-claim page. It answers the question well. "
         "They have no idea nineteen other pages were written for them.", False),
        ("03", "The band tells them where they are",
         "One line above the headline naming the stage, one block below it "
         "naming what people read next. <b>This is the piece that does not "
         "exist yet, and it is on 200 pages rather than five.</b>", True),
        ("04", "The door, and the shelf",
         "Now the hub is a destination rather than a page nobody found. They "
         "arrive already knowing why they are there.", False),
    ]:
        o.append('<div%s><span class="s">Step %s</span><h4>%s</h4><p>%s</p></div>'
                 % (' class="hit"' if hit else "", s, h, p))
    o.append("</div>")
    o.append('<p class="src">Which is the argument for building the band '
             "<em>before</em> the remaining four doors: a door nobody can find "
             "is worth less than a signpost on two hundred pages.</p>")
    o.append("</section><hr class=\"rule\">")

    # ------------------------------------------------------------- furniture
    o.append('<section id="furniture"><div class="kicker"><span class="n">05</span>'
             "<h2>What changes on every page</h2></div>")
    o.append('<p class="lede">Two small blocks and one nav entry. Nothing '
             "moves, nothing is renamed, no URL changes.</p>")

    o.append('<h3 style="margin:20px 0 6px">Above the article &mdash; the '
             "annotated breadcrumb</h3>")
    o.append("<p>Merged into the existing breadcrumb rather than stacked above "
             "it. Two navigational lines over a headline is one too many.</p>")
    o.append(frame("/associate-unpaid-hours-california.html",
                   '<div class="band"><span class="you">You are at &middot; '
                   "counting hours</span><span>This page tells you <b>what the "
                   "claim is worth, and the 30-day clock</b>.</span>"
                   '<span class="nx">All 20 for this stage &rarr;</span></div>'
                   '<div style="border:2px solid var(--ink);background:#fff;'
                   'padding:14px 16px;margin-top:9px">'
                   '<h3 style="font-size:19px">Unpaid hours as a California '
                   "associate</h3>"
                   '<p style="font-size:12px;color:var(--muted);margin:0">The '
                   "wage claim, step by step &mdash; and why the Board is not "
                   "where you file it.</p></div>"))

    o.append('<h3 style="margin:24px 0 6px">After the article &mdash; the '
             "next-step band</h3>")
    o.append("<p>Catches the reader at the highest-intent moment on the page: "
             "the one where they have finished and are deciding whether to "
             "leave.</p>")
    o.append(frame("/associate-unpaid-hours-california.html",
                   '<div style="border:2px solid var(--ink);background:#fff;'
                   'padding:12px 14px"><h3 style="font-size:17px">&hellip; and '
                   "that is the whole claim.</h3>"
                   '<p style="font-size:12px;color:var(--muted);margin:0">'
                   "Sources and the form are below.</p></div>"
                   '<div class="bandfoot" style="margin-top:10px">'
                   '<span class="lab">You are counting toward 3,000</span>'
                   "<h4>Nineteen other pages are written for this stage.</h4>"
                   "<p>Next, most people read: what a job has to be able to "
                   "bill before it can hire you &middot; where to apply in all "
                   "58 counties &middot; the 3,000-hour calculator.</p></div>"))

    o.append('<h3 style="margin:24px 0 6px">The nav gains one entry, not '
             "five</h3>")
    o.append("<p>The masthead is already on two rows at 1440px. Five more "
             "top-level items will not fit, and five persona labels in a nav "
             "is the pattern the research warns about. One entry that opens.</p>")
    o.append(frame("/",
                   '<div style="padding:6px 0 2px"><span class="lab">The '
                   "masthead, with the doors behind one entry</span>"
                   '<div style="display:flex;gap:14px;flex-wrap:wrap;'
                   'font-family:var(--mono);font-size:11px;letter-spacing:.08em;'
                   'text-transform:uppercase;margin:9px 0 12px;color:var(--muted)">'
                   "<span>Calculators</span><span>Money</span>"
                   "<span>Licensure</span><span>Getting paid</span>"
                   "<span>Practice</span><span>Training</span>"
                   '<span style="background:var(--gold);border:1.5px solid '
                   'var(--ink);padding:2px 8px;color:var(--ink)">For you '
                   "&or;</span></div>"
                   '<div style="border:2px solid var(--ink);background:var(--cream);'
                   'padding:11px 13px;box-shadow:4px 4px 0 var(--ink);max-width:430px">'
                   '<span class="lab">Where are you on the path?</span>'
                   '<div style="display:grid;gap:5px;margin-top:7px;font-size:13px">'
                   "<span><b>Thinking about it</b> &mdash; 73 guides</span>"
                   "<span><b>In a program</b> &mdash; the practicum year</span>"
                   "<span><b>Counting hours</b> &mdash; 20 guides</span>"
                   "<span><b>Licensed</b> &mdash; what changed, and the shelf</span>"
                   "<span><b>Running a practice</b> &mdash; four decisions</span>"
                   "</div></div></div>"))
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- model
    o.append('<section id="model"><div class="kicker"><span class="n">06</span>'
             "<h2>URLs and data</h2></div>")
    o.append('<div class="grid g2">')
    o.append('<div class="card"><h3>The namespace</h3>'
             "<p><code>/for/associates.html</code> &mdash; live. Then "
             "<code>/for/deciding.html</code>, <code>/for/students.html</code>, "
             "<code>/for/licensed.html</code>, "
             "<code>/for/practice-owners.html</code>.</p>"
             "<p style=\"margin:0\"><b>One level, not two.</b> The passes list "
             "the site root plus each directory one level down and do not "
             "recurse, so <code>/for/associates/index.html</code> would be "
             "invisible to every one of them. This was found the hard "
             "way.</p></div>")
    o.append('<div class="card"><h3>Two keys per page</h3>'
             '<pre style="font-family:var(--mono);font-size:11.5px;'
             'overflow-x:auto;background:#fff;border:1.5px solid var(--line);'
             'padding:10px">"stages": ["associate", "student"],\n'
             '"stage_note": {\n'
             '  "associate": "What the claim is worth, and the 30-day clock.",\n'
             '  "student": "Why a placement cannot ask you to work unpaid."\n'
             "}</pre>"
             "<p style=\"margin:0\"><b>The note is mandatory</b>, and that has "
             "a consequence worth stating: it makes bulk tagging impossible. "
             "Two hundred honest one-line annotations cannot be written in one "
             "pass, and generated ones would be exactly the thin duplicate the "
             "field exists to prevent. So a page is tagged when a door that "
             "lists it is built. 20 are done.</p></div>")
    o.append("</div>")

    o.append('<div class="note"><p><b>Three things already shipped that this '
             "depends on.</b> <code>&quot;for&quot;</code> is in "
             "<code>SUBDIRS</code> in all forty passes, and "
             "<code>_dev/subdirs_check.py</code> now fails the build if they "
             "ever disagree. <code>registry_sync.py</code> preserves keys it "
             "does not own &mdash; it was deleting the tagging on the first "
             "run, silently. And <code>_dev/plain_gates.py</code> made 309 "
             "replacements across 199 pages.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- order
    o.append('<section id="order"><div class="kicker"><span class="n">07</span>'
             "<h2>Build order</h2></div>")
    o.append('<p class="lede">Changed from P2 in one place, and the journey '
             "above is the reason: the band comes before the remaining "
             "doors.</p>")
    o.append('<ol class="plan">')
    for h, why, out, done in [
        ("SUBDIRS, the tagging, and the plain words",
         "The configuration line first, so nothing built afterward is "
         "invisible. Then the two registry keys, and the sitewide sweep that "
         "replaced a metaphor with two plain nouns.",
         "Shipped 12 August. 202 pages, 0 failures.", True),
        ("/for/associates &mdash; the reference implementation",
         "Loudest room, twenty pages ready. Built, reviewed, and corrected "
         "twice - which is what makes it worth copying rather than the first "
         "draft of it.",
         "Live. The pattern in section 01 is this page.", True),
        ("The band, on 200 pages, and the home page repointed",
         "Step 3 of the journey. A door nobody can find is worth less than a "
         "signpost on two hundred pages, and this is one line in the "
         "breadcrumb pass plus one block in the footer pass.",
         "200 pages gain a stage line and a next-step block.", False),
        ("/for/students &mdash; the practicum door",
         "Runs entirely off data that shipped on 11 August. The most "
         "shareable single thing in the set: look up your program, read its "
         "own words about who finds your site.",
         "One door, one new lookup, no new research.", False),
        ("/for/deciding &mdash; the largest shelf",
         "73 pages, lowest urgency. It benefits from the two doors above "
         "already existing, because half of what it routes to is them.",
         "One door. The set reads as a set.", False),
        ("/for/licensed &mdash; what changed",
         "Blocked only on the advertising-rule and telehealth pages, both "
         "already on the approved editorial list. Built as a change log, not "
         "a masthead: a change log cannot go stale, because staleness is its "
         "content.",
         "One door, plus the two pages it needs.", False),
        ("/for/practice-owners &mdash; last",
         "Eight pages, three of which belong to the licensed door. Opening it "
         "now is how a hub becomes a thin duplicate. Four more owner pages "
         "and it opens honestly.",
         "The set closes.", False),
    ]:
        o.append('<li><h4>%s%s</h4><p class="why">%s</p>'
                 '<span class="out">%s</span></li>'
                 % (h, ' <span class="badge">done</span>' if done else "",
                    why, out))
    o.append("</ol>")
    o.append('<p class="src">Net new: <b>4 doors</b> and two page-furniture '
             "blocks. Everything else is a view over content that already "
             "exists.</p>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "%s. Supersedes the design half of "
             '<a href="stage-doors.html">P2</a>, which was drawn before the '
             "first door shipped and leads with the tool. The evidence, the "
             "coverage audit and the namespace argument are in "
             '<a href="stage-architecture.html">P1</a> and are not repeated. '
             "Mockups are real HTML in the shipping design system; the "
             "associates door is rendered from its live content. Nothing else "
             "here is live.</p></div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("information architecture, revised")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes"
          % (os.path.basename(OUT), format(len(html), ",d")))

    bad = 0
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, absent" % h)
            bad += 1
    n = html.count('class="frame"')
    if n != len(DOORS) + 3:
        print("GUARD: %d mockups, expected %d" % (n, len(DOORS) + 3))
        bad += 1
    for needle, what in [
        ("Everything a California associate needs", "the live headline"),
        ("lead with what the reader gets", "the correction this is built on"),
        ("This is the piece that does not exist yet",
         "the band as the missing step"),
        ("makes bulk tagging impossible", "the consequence of the note rule"),
    ]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1
    # The word this document exists partly to remove must not be in its own
    # prose - but it may quote the headline it is correcting, and it has to be
    # able to say "requirement, not gate" out loud. Style blocks carry an
    # inherited CSS class name and are not prose at all.
    import re as _re
    t = _re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=_re.I)
    t = _re.sub(r"<[^>]+>", " ", t)
    QUOTING = ("golden gate", "not gate", "one bar. four gates",
               "and was wrong", "argues against")
    for m in _re.finditer(r"\bgates?\b", t, _re.I):
        ctx = t[max(0, m.start() - 60):m.start() + 60].lower()
        if any(q in ctx for q in QUOTING):
            continue
        print("GUARD: %r - this document argues against that word"
              % t[max(0, m.start() - 40):m.start() + 40].strip())
        bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d mockups, %d jump targets" % (n, len(NAV)))


if __name__ == "__main__":
    main()
