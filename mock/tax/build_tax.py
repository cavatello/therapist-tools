#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""therapist-tax-strategy-california.html

Step 2 of the migration in claude/site-architecture-and-seo.md. The tax chapter
leaves the home page and becomes a real file with a keyword-bearing slug, its
own title, and enough depth to be worth ranking.

Treatment: THE SORTING BAR, of the five tree designs. It is the one that suits
this chapter's actual job - there are four accounts, they are alternatives
rather than a sequence, and the reader's situation rules some of them out. A
bar that re-sorts and greys what does not apply keeps every option on the page
(which the other four designs do not, and which search engines need) while
still answering the question. Swapping it later means replacing drawSorting()
in render.py; nothing else depends on it.
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
from css import CSS
from render import JS as RENDER_JS
import engine

SITE = "https://cavatello.github.io/therapist-tools"
SLUG = "therapist-tax-strategy-california.html"
TITLE = ("Therapist Tax Strategy California — what a therapist can legally defer in 2026")
DESC = ("Work out how much of a California therapy practice's tax bill is optional: "
        "Solo 401(k), SEP, SIMPLE and IRA priced against your own profit, then sole "
        "proprietor versus professional corporation with the Social Security cost included. "
        "2026 federal and California rates.")

BLOCKS = json.load(open(os.path.join(HERE, "_blocks.json")))

# ---------------------------------------------------------------- chrome ---
CH = os.path.join(HERE, "..", "amft")
chrome_css = open(os.path.join(CH, "_chrome_css.txt")).read()
chrome_hdr = open(os.path.join(CH, "_chrome_hdr.txt")).read()
chrome_head = open(os.path.join(CH, "_chrome_head.txt")).read()
chrome_js = open(os.path.join(CH, "_chrome_js.txt")).read().split("\n/*---*/\n")[0]
# The footer was never lifted, which is why this page used to just stop.
chrome_ftr = open(os.path.join(CH, "_chrome_ftr.txt")).read()

# This page REPLACES the old "Tax & Retirement" entry, which pointed at an
# anchor inside the simulator. Adding a second entry with the same name would
# leave the reader choosing between two things called the same thing.
_tax_anchor = re.search(r'<a href="(?:index\.html)?#tax">(.*?)</a>', chrome_hdr, re.S)
if _tax_anchor and SLUG not in chrome_hdr:
    chrome_hdr = chrome_hdr.replace(_tax_anchor.group(0),
        '<a href="' + SLUG + '" class="on">'
        + _tax_anchor.group(1).replace(
            "sole prop vs professional corp, priced",
            "how much of your tax bill is optional")
        + '</a>', 1)
SELF = SLUG
# The chrome is lifted from tools.html, where "All free tools" legitimately
# carries class="on". Lifted onto another page that marker is a lie: every page
# was telling the reader they were on the tools page. Strip every marker first,
# then set the one that belongs to THIS page.
chrome_hdr = re.sub(r'(<a href="[^"]*") class="on"', r'\1', chrome_hdr)
_self = re.search(r'<a href="' + re.escape(SELF) + r'"', chrome_hdr)
assert _self, "this page has no entry of its own in the lifted nav: " + SELF
chrome_hdr = (chrome_hdr[:_self.end() - 1] + '" class="on"'
              + chrome_hdr[_self.end():])
assert chrome_hdr.count('class="on"') == 1

# ------------------------------------------------------------ structured ---
LD = [
 {"@context":"https://schema.org","@type":"WebApplication",
  "name":"California Therapist Tax & Retirement Strategy",
  "url":SITE + "/" + SLUG, "applicationCategory":"FinanceApplication",
  "operatingSystem":"Any web browser","browserRequirements":"Requires JavaScript",
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}, "description":DESC,
  "audience":{"@type":"Audience",
    "audienceType":"California-licensed marriage and family therapists, clinical social "
                   "workers, professional clinical counselors and psychologists"},
  "featureList":["Solo 401(k), SEP, SIMPLE and traditional IRA priced on your own profit",
                 "Tax saving measured by running the full engine twice, not estimated",
                 "Sole proprietor versus California professional corporation, itemised",
                 "The Social Security cost of a below-profit S-corp salary",
                 "2026 federal and California rates"]},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
   {"@type":"ListItem","position":1,"name":"Therapist Support","item":SITE + "/"},
   {"@type":"ListItem","position":2,"name":"Free tools","item":SITE + "/tools.html"},
   {"@type":"ListItem","position":3,"name":"Tax & retirement strategy",
    "item":SITE + "/" + SLUG}]},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
   {"@type":"Question","name":"How much can a therapist in private practice contribute to a Solo 401(k)?",
    "acceptedAnswer":{"@type":"Answer","text":
      "In 2026, up to $24,500 as the employee deferral ($32,500 from age 50) plus 20% of net "
      "self-employment earnings as the employer contribution, capped at $72,000 in total. On "
      "$165,000 of practice profit that is roughly $55,000 of room, of which about 27% is "
      "funded by tax you would otherwise have paid."}},
   {"@type":"Question","name":"Can a California therapist form an LLC?",
    "acceptedAnswer":{"@type":"Answer","text":
      "No. California Corporations Code section 17701.04(e) bars an LLC from rendering "
      "professional services requiring a licence. The real choice for a licensed therapist is "
      "between a sole proprietorship and a California professional corporation — for an MFT, "
      "a Marriage and Family Therapy Corporation — which can then elect S-corp tax treatment."}},
   {"@type":"Question","name":"Is an S-corp worth it for a therapy practice?",
    "acceptedAnswer":{"@type":"Answer","text":
      "Less often than the pitch suggests. The payroll-tax saving on the distribution has to "
      "cover California's franchise tax (the greater of $800 and 1.5% of net income), payroll "
      "and 1120-S filing costs, and the QBI deduction you give up because a wage is not "
      "qualified business income. On a solo practice it is frequently within a few thousand "
      "dollars either way, and it also reduces the earnings credited to your Social Security "
      "record every year."}},
   {"@type":"Question","name":"What is a defensible S-corp salary for a therapist?",
    "acceptedAnswer":{"@type":"Answer","text":
      "There is no safe-harbour percentage in the Internal Revenue Code. The test is "
      "reasonable compensation for the services actually performed. The 50%-of-profit figure "
      "commonly quoted is a practitioner convention, not a rule; the defensible number is "
      "what you would have to pay a licensed therapist to carry your clinical hours, plus "
      "something for running the business."}},
   {"@type":"Question","name":"Does deferring tax into a retirement account just postpone the problem?",
    "acceptedAnswer":{"@type":"Answer","text":
      "It postpones the tax, which is the point. You pay it on withdrawal, usually decades "
      "later and usually at a lower rate, on money that has compounded in the meantime. The "
      "real cost is liquidity: reaching the money before age 59 and a half generally means a "
      "10% penalty on top of the tax."}}]}]


def field(fid, label, unit="", kind="number", opts=None, mn=None, mx=None, step=None, ph=""):
    if kind == "select":
        val = ('<span class="fv"><select id="i-' + fid + '">'
               + "".join('<option value="%s">%s</option>' % (v, t) for v, t in opts)
               + "</select></span>")
    else:
        a = 'id="i-%s" type="%s"' % (fid, kind)
        if mn is not None: a += ' min="%s"' % mn
        if mx is not None: a += ' max="%s"' % mx
        if step is not None: a += ' step="%s"' % step
        if ph: a += ' placeholder="%s"' % ph
        pre = '<span class="unit">$</span>' if unit == "$" else ""
        post = ('<span class="unit">' + unit + "</span>") if unit and unit != "$" else ""
        val = '<span class="fv">' + pre + "<input " + a + ">" + post + "</span>"
    return '<label class="f"><em>' + label + "</em>" + val + "</label>"


FILING = [("single", "Single"), ("mfj", "Married filing jointly"),
          ("hoh", "Head of household")]

# ------------------------------------------------------------------ body ---
B = []
A = B.append
A('<div class="tax">')

# ---- hero
A('<section class="thero"><div class="in"><div>')
A('<p class="tkick">Chapter 04 &middot; California &middot; 2026 rates</p>')
A('<h1>Therapist tax strategy in <em>California</em>.</h1>')
A('<p class="ttag">Some of your tax bill is optional. Here is how much.</p>')
A('<p class="tlede">Not a loophole and not aggressive — ordinary accounts the tax code '
  'created on purpose. The only real question is whether that money goes to the IRS this '
  'April or into an account with your name on it. <b>Everything below is worked out from '
  'your own profit</b>, and the saving from each account is measured by running the whole '
  'tax engine twice rather than estimated from a bracket table.</p>')
A('<div class="therocta"><a href="#plan">Make the plan</a>'
  '<a class="ghost" href="#which">Which account</a>'
  '<a class="ghost" href="#structure">Sole prop or corporation</a></div>')
A('</div><div class="tpanel">'
  '<div class="pr"><em>Your practice profit</em><b id="heroprofit">$217,350</b></div>'
  '<div class="pr"><em>Of the tax on it, optional</em>'
  '<b class="gold" id="herooptional">$18,244</b></div>'
  '<p class="pn" id="heroeg" style="margin-top:2px"><b>Worked example</b> &mdash; a $250,000 '
  'practice with $41,650 of running costs. Put your own numbers in below, or arrive from '
  'the simulator and they come with you.</p>'
  '<p class="pn">Arrived from the simulator? Your rate, caseload and costs came with you. '
  'Nothing is saved and there is no account — your setup lives in the address bar.</p>'
  '</div></div></section>')

# ---- 01 recap
A('<section class="slab pine" id="profit"><div class="chh"><span class="chn">01</span>'
  '<h2>Start from the profit</h2></div>')
A('<p class="dek">Planning does not stop at profit — it starts there. This is what the '
  'practice actually cleared before a dollar of tax, and every figure on this page is built '
  'from it. Change anything here and the whole page moves.</p>')
A('<div class="fgrid">')
A(field("rate", "Your session rate", "$", mn=0, mx=1000, step=5, ph="150"))
A(field("sessions", "Sessions a week", "", mn=0, mx=60, step=1, ph="25"))
A(field("weeksOff", "Weeks off a year", "wks", mn=0, mx=26, step=1, ph="2"))
A(field("expMonth", "Monthly running costs, all in", "$/mo", mn=0, mx=100000,
        step=50, ph="2400"))
A(field("filing", "Filing status", kind="select", opts=FILING))
A(field("age", "Your age", "", mn=18, mx=90, step=1, ph="40"))
A('</div>')
A('<div id="recap" style="margin-top:18px"></div>')
A('</section>')

# ---- 02 the sell
A('<section class="slab carbon" id="why"><div class="chh"><span class="chn">02</span>'
  '<h2>What deferral actually is, and why it is worth this much</h2></div>')
A('<p class="dek">A dollar you move into a retirement account is <b>not taxed this year</b>. '
  'You still own it. The tax is postponed rather than cancelled, and in the meantime the '
  'whole dollar compounds instead of the seventy-odd cents that would have survived the '
  'April bill. That is the entire mechanism, and on a therapy practice it is worth more than '
  'every other lever on this page combined.</p>')
A('<div id="sell"></div>')
A('</section>')

# ---- 03 the planner
A('<section class="slab pine" id="plan"><div class="chh"><span class="chn">03</span>'
  '<h2>The most you can put away this year</h2></div>')
A('<p class="dek">Before choosing between accounts, it is worth seeing the ceiling — because '
  'the number surprises people, and because the share of it funded by tax is the argument. '
  'Set what you would actually contribute, what return you want to assume, and how long you '
  'have.</p>')
A('<div class="fgrid">')
A(field("contrib", "Contribute this year", "$", mn=0, mx=80000, step=500, ph="0"))
A(field("retRet", "Assumed return", "%", mn=0, mx=20, step=.5, ph="7"))
A(field("retYrs", "Years invested", "yrs", mn=1, mx=45, step=1, ph="20"))
A('</div>')
A('<button class="maxbtn" id="b-max" type="button">Max it out</button>')
A('<div id="planout" style="margin-top:16px"></div>')
A('<p class="fine">A return is an assumption, not a promise, and the figure is before '
  'inflation and before the tax you will pay on the way out. The default of 7% is roughly '
  'the long-run real-ish average people plan with; 11% is the sort of number a good two '
  'decades produced and a bad one did not.</p>')
A('</section>')

# ---- 04 the sorting bar
A('<section class="slab brick" id="which"><div class="chh"><span class="chn">04</span>'
  '<h2>Which account, and what each is worth to you</h2></div>')
A('<p class="dek">No wizard and no pages. Four answers at the top, and everything below '
  're-orders around them. <b>Nothing is ever removed</b> — an account that does not apply '
  'drops to a dashed line that says which answer ruled it out, because the reason is the '
  'useful part.</p>')
A('<div class="sbar" id="sbar"></div>')
# The backdoor Roth card cannot answer honestly without this. It sits with the
# sorting bar rather than up in the profit section because it is a question
# about ONE account, and asking everyone for it up front would be noise.
A('<div class="slider" style="margin-top:14px">'
  '<label for="i-pretaxIra">Money already sitting in Traditional, SEP or SIMPLE '
  'IRAs &mdash; needed only for the backdoor Roth below. A Solo 401(k) balance '
  'does not count.</label>'
  '<div class="fgrid" style="max-width:280px;margin-top:8px">'
  + field("pretaxIra", "Pre-tax IRA balance", "$", mn=0, mx=5000000, step=1000,
          ph="0") + "</div></div>")
A('<div id="blocks"></div>')
A('<p class="fine">The headline figure is the <b>best single route</b>, not a total. These '
  'are alternatives drawing on the same profit — a SIMPLE and a Solo 401(k) cannot share a '
  'year at all, and adding two of these together would overstate what is available by '
  'thousands.</p>')
A('</section>')

# ---- 05 structure
A('<section class="slab indigo" id="structure"><div class="chh"><span class="chn">05</span>'
  '<h2>The last decision: sole proprietor, or a professional corporation?</h2></div>')
A('<p class="dek">This one comes last on purpose. It is the smaller lever, it depends on '
  'what you decided above, and it is the only choice here that costs you something other '
  'than money. <b>A California-licensed therapist cannot use an LLC</b> — the real choice is '
  'between a sole proprietorship and a professional corporation that elects S-corp tax '
  'treatment.</p>')
A('<div class="slider"><label for="i-salPct">Salary you would pay yourself, as a share of '
  'profit</label><input id="i-salPct" type="range" min="20" max="100" step="5" value="50">'
  '<div class="out" id="salout">&mdash;</div></div>')
A('<div id="corpout" style="margin-top:16px"></div>')
A('</section>')

# ---- 06 working remotely
A('<section class="slab gold" id="remote"><div class="chh"><span class="chn">06</span>'
  '<h2>Curious about working remotely?</h2></div>')
A('<p class="dek">Everything above this line moves money between accounts. This moves '
  '<em>you</em>. Same clients, same profit, eight different places to be sitting when you '
  'see them. How many of them beat California depends on your own profit, so the count '
  'below is computed rather than quoted &mdash; and the rule that decides whether you '
  'can do it at all is <b>not</b> the one you expect.</p>')
A('<div id="remoteout"></div>')
A('<a class="tcta" href="therapist-working-remotely-california.html" '
  'style="margin-top:16px"><strong>Can a California therapist work remotely? &rarr;</strong>'
  '<span>the Board&rsquo;s own answer, all eight places, and the US tax that follows your '
  'passport</span></a>')
A('<details class="txref"><summary><span><b>Your licence is not the obstacle</b>'
  '<i>the Board has answered this directly &mdash; and it is a yes</i></span></summary>'
  '<div class="txb"><p>The Board of Behavioral Sciences was asked whether a California '
  'licensee can provide telehealth from outside the state, and answered: <b>yes</b> &mdash; '
  'if the licence is current and active, the case is appropriate for telehealth, and the '
  'licensee follows 16 CCR &#167;1815.5. That regulation sets standards for the session, '
  'including verbally obtaining and documenting <b>the client\u2019s</b> full name and '
  'present location at the start of every one. It sets no requirement about where the '
  '<em>licensee</em> is.<sup>[10][11]</sup></p>'
  '<p>Which puts the constraint where it actually sits: your licence covers clients '
  'in California, so your clients stay in California. You are the one who moves. And the '
  'country you move to has its own view about practising a regulated profession from its '
  'soil, and about whether your visa lets you work at all &mdash; neither of which is a '
  'California question, and neither of which is priced above.</p></div></details>')
A('<details class="txref"><summary><span><b>The tax follows the passport, not the address'
  '</b><i>why Dubai is not the windfall the bar makes it look</i></span></summary>'
  '<div class="txb"><p>The United States taxes citizens on worldwide income wherever they '
  'live. In a high-tax country the foreign tax credit absorbs most of the US bill, which is '
  'why Berlin and Bordeaux above are close to their local tax and not much more. In a '
  'low-tax one there is nothing to credit, so the US bill lands in full.</p>'
  '<p>And the foreign earned income exclusion, the thing everyone reaches for first, '
  '<b>does not touch self-employment tax</b> &mdash; the IRS is explicit about it. A '
  'self-employed therapist in Dubai still owes the full 15.3% on the way through, on top of '
  'whatever the UAE charges.<sup>[12][13]</sup></p></div></details>')
A('<p class="pay-note">This is a comparison, not a plan. It prices tax and nothing else: '
  'not visas, not the right to work, not health cover, not what a flat costs in Lisbon '
  'versus Fresno, not currency risk, and not whether a client in Sacramento wants a '
  'therapist nine time zones away. Treat it as a reason to ask a cross-border accountant a '
  'better question.</p>')
A('</section>')

# ---- 07 reference
A('<section class="slab carbon" id="reference"><div class="chh"><span class="chn">07</span>'
  '<h2>The parts worth reading once</h2></div>')
A('<p class="dek">Everything above is arithmetic on your numbers. This is the material '
  'underneath it — the mechanic the whole chapter turns on, what other California therapists '
  'actually do, what the people who do this for a living disagree about, and what actually '
  'gets challenged.</p>')
REF_ORDER = ["setax", "prevalence", "experts", "wage", "setup", "audit", "llc", "assoc"]
for bid in REF_ORDER:
    b = BLOCKS[bid]
    A('<details class="txref"><summary><span><b>' + b["title"] + '</b><i>' + b["sub"]
      + '</i></span></summary><div class="txb">' + b["body"] + '</div></details>')
A('</section>')

# ---- 08 CTA
A('<section class="slab pine" id="next"><div class="chh"><span class="chn">08</span>'
  '<h2>Back to the practice</h2></div>')
A('<p class="dek">Everything here is downstream of one number: the profit at the top. If '
  'that is a guess, this whole page is a guess about a guess — the simulator builds it '
  'properly, category by category.</p>')
A('<a class="tcta" href="index.html"><strong>Model the whole practice &rarr;</strong>'
  '<span>rate, caseload, twelve expense categories, residency and growth &middot; free '
  '&middot; nothing is saved</span></a>')
A('</section>')
A('</div>')

# ---- citations
CITES = [
 (1, "IRS Revenue Procedure 2025-32", "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
  "2026 federal rate schedules, the $16,100 single standard deduction, and the widened "
  "&#167;199A phase-out used throughout."),
 (2, "IRS, retirement topics &mdash; 401(k) and profit-sharing plan contribution limits",
  "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-401k-and-profit-sharing-plan-contribution-limits",
  "The employee deferral, the age-50 catch-up, and the overall &#167;415(c) limit that caps "
  "the two halves of a Solo 401(k) together."),
 (3, "IRS, self-employed individuals &mdash; calculating your own retirement plan contribution",
  "https://www.irs.gov/retirement-plans/self-employed-individuals-calculating-your-own-retirement-plan-contribution-and-deduction",
  "Why the employer half is 20% of net self-employment earnings rather than 25% of a salary, "
  "and why half of self-employment tax comes off first."),
 (4, "IRS, S corporation compensation and medical insurance issues",
  "https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-compensation-and-medical-insurance-issues",
  "Reasonable compensation. There is no safe-harbour percentage; the test is what the "
  "services are worth."),
 (5, "California Corporations Code section 17701.04",
  "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
  "?sectionNum=17701.04.&amp;lawCode=CORP",
  "Subdivision (e): an LLC may not render professional services requiring a licence. This is "
  "why the choice here is sole proprietorship or professional corporation."),
 (6, "California Business and Professions Code section 13401.5",
  "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
  "?sectionNum=13401.5.&amp;lawCode=CORP",
  "Who may own shares in a Marriage and Family Therapy Corporation."),
 (7, "California Franchise Tax Board, S corporation tax",
  "https://www.ftb.ca.gov/file/business/types/corporations/s-corporations.html",
  "California taxes an S corporation at 1.5% of net income, subject to the $800 minimum "
  "franchise tax."),
 (8, "Social Security Administration, contribution and benefit base",
  "https://www.ssa.gov/oact/cola/cbb.html",
  "The 2026 Social Security wage base of $184,500, which is where the payroll-tax saving "
  "stops growing. Medicare has no cap."),
 (9, "Social Security Administration, primary insurance amount",
  "https://www.ssa.gov/oact/cola/piaformula.html",
  "The bend points used to price what a below-profit salary costs your benefit."),
 (10, "California Board of Behavioral Sciences, telehealth FAQ",
  "https://www.bbs.ca.gov/pdf/publications/telehealth_faq.pdf",
  "&#8220;Can a California licensee while out-of-state provide telehealth services to a "
  "client located in California?&#8221; &#8212; the Board&#8217;s answer is yes, subject to "
  "a current and active licence and 16 CCR &#167;1815.5."),
 (11, "California Code of Regulations, title 16, section 1815.5",
  "https://www.law.cornell.edu/regulations/california/16-CCR-1815.5",
  "Standards of practice for telehealth. Requires the client&#8217;s full name and present "
  "location to be obtained verbally and documented at the start of each session; imposes no "
  "requirement about the licensee&#8217;s own location."),
 (12, "IRS, self-employment tax for businesses abroad",
  "https://www.irs.gov/individuals/international-taxpayers/self-employment-tax-for-businesses-abroad",
  "&#8220;You must take all your self-employment income into account in figuring your net "
  "earnings from self-employment, even if all, or a portion of, gross income was excluded "
  "because of the foreign earned income exclusion.&#8221;"),
 (13, "IRS, foreign tax credit",
  "https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit",
  "The mechanism that absorbs most of the US bill in a high-tax country, and has nothing to "
  "absorb in a low-tax one."),
]
A('<div class="tax"><div class="cites"><h3>Sources</h3>')
for n, cite, url, note in CITES:
    A('<div class="cite"><span class="n">[' + str(n) + ']</span><span>'
      + '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + cite + '</a>'
      + ' &mdash; ' + note + '</span></div>')
A('</div>')
A('<p class="disc"><b>Estimates, not advice.</b> This models a California resident whose '
  'practice income is self-employment income, with no other household income and no itemised '
  'deductions. Federal figures are the final 2026 amounts; California has not published 2026 '
  'rate schedules, and the FTB&rsquo;s own 2026 Form 540-ES instructs filers to use the 2025 '
  'tables, so that is what this uses. The professional-corporation comparison prices payroll, '
  'the 1120-S and the Statement of Information at typical figures, not quotes you have been '
  'given. The salary convention is a practitioner rule of thumb and carries real audit risk; '
  'the Social Security comparison answers &ldquo;what if this year were typical of a 35-year '
  'record&rdquo;, which is not the same question as &ldquo;what will I get&rdquo;. Talk to a '
  'CPA before acting on any of it.</p>')
A('</div>')

BODY = "\n".join(B)

# ------------------------------------------------------------------ head ---
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
{chrome_head}
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="google-adsense-account" content="ca-pub-6079968999170000" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{site}/{slug}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Therapist Support" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{site}/{slug}" />
<meta property="og:image" content="{site}/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{ld}</script>
<style>
{chrome_css}
</style>
<style>
{css}
</style>
</head>
<body>
{hdr}
<main>
{body}
</main>
<script>
{navjs}
</script>
<script>
{engine}
{render}
</script>
{ftr}
</body>
</html>
"""

html = HTML.format(chrome_head=chrome_head, title=TITLE, desc=DESC, site=SITE, slug=SLUG,
                   ld=json.dumps(LD, separators=(",", ":")), chrome_css=chrome_css, css=CSS,
                   hdr=chrome_hdr, body=BODY, navjs=chrome_js,
                   engine=engine.js(), render=RENDER_JS, ftr=chrome_ftr)

# --- build-time guards, every one of which has been a real bug on this site ---
# THREE separate blank-section bugs on this page came from the same cause: a
# class this page invented (.tl, .ref, .sr) already existed in the shared site
# chrome, which is lifted verbatim and cannot be edited from here. A bare
# single-class selector is the dangerous shape - it has no qualifier to lose to.
# So: no bare .foo{} rule in this page's CSS may use a name the chrome also
# styles. Scoped selectors (.txb table.cmp tr.band td) are fine and are allowed.
def _classes(css, bare_only=False):
    body = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = set()
    for sel_group in re.findall(r"([^{}]+)\{", body):
        if sel_group.strip().startswith("@"):
            continue
        for sel in sel_group.split(","):
            sel = sel.strip()
            if bare_only:
                m = re.fullmatch(r"\.([a-zA-Z][\w-]*)(:[\w-]+(\([^)]*\))?)?", sel)
                if m:
                    out.add(m.group(1))
            else:
                out.update(re.findall(r"\.([a-zA-Z][\w-]*)", sel))
    return out
_bare = _classes(CSS, bare_only=True)
_chrome = _classes(chrome_css)
_clash = sorted(_bare & _chrome)
assert not _clash, ("these page classes are declared bare and also exist in the site "
                    "chrome, which will silently win or lose somewhere: " + ", ".join(_clash))

assert "</script>" not in engine.js() and "</script>" not in RENDER_JS
assert html.count("<style>") == 2 and html.count("</style>") == 2
assert html.count("<body>") == 1 and html.count("</body>") == 1
# Three pages shipped with no footer at all because the lift never took it.
assert html.count("<footer") == 1, "exactly one footer, please"
assert 'href="terms.html"' in html and 'href="privacy.html"' in html, \
    "the footer must carry the legal links"
for need in ['id="recap"', 'id="sell"', 'id="planout"', 'id="sbar"', 'id="blocks"',
             'id="corpout"', 'id="b-max"', 'id="i-salPct"', 'id="salout"', 'id="i-pretaxIra"',
             'id="heroprofit"', 'id="herooptional"']:
    assert html.count(need) == 1, "expected exactly one " + need
# every field the renderer binds must exist, and vice versa
bound = re.search(r'\["rate","sessions",.*?\]', RENDER_JS).group(0)
for k in re.findall(r'"(\w+)"', bound):
    assert 'id="i-%s"' % k in html, "bound key %s has no input" % k
for k in set(re.findall(r'id="i-(\w+)"', html)):
    assert k in bound or k == "salPct", "input i-%s is bound to nothing" % k
# The reference prose must have arrived, tables and all. Section 06 adds two
# more collapsibles of its own, so the count is the reference blocks plus those
# two rather than a bare len() - if either disappears, this fails.
REMOTE_DETAILS = 2
assert html.count('class="txref"') == len(REF_ORDER) + REMOTE_DETAILS, \
    html.count('class="txref"')
assert "Curious about working remotely" in html
# The intro must not assert how many places win: that depends on the reader's
# profit, and the line under the bars computes it. A number typed into the prose
# is true for exactly one visitor.
_intro = re.search(r'Curious about working remotely.*?<div id="remoteout">', html, re.S).group(0)
assert not re.search(r"\b(one|two|three|four|five|six|seven|eight)\s+of\s+the\s+(eight|seven)\b",
                     _intro, re.I), "the section intro hard-codes a count"
assert "RESID" in html and "computeResidency" in html
assert '"1815.5"' not in html and "1815.5" in html
assert "17701.04" in html and "LLC" in html
# and no block may quietly reference a figure it no longer has
assert "undefined" not in BODY

out = os.path.join(HERE, SLUG)
open(out, "w").write(html)
print("wrote", SLUG, len(html) // 1024, "kB;",
      len(re.findall(r'id="i-', html)), "inputs;", len(REF_ORDER), "reference blocks")
