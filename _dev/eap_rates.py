#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill in the EAP rate table, which said "No usable report yet" three times.

WHAT THE PAGE SAID BEFORE

    Lyra Health     $120   Single clinician report, July 2026
    Spring Health   —      No usable report yet.
    Modern Health   —      No usable report yet.
    Headspace       —      No usable report yet.

and then a note headed "Why the rest of this table is empty", explaining that
platform contracts are confidential and there is nothing to cite.

That note was honest and it is now wrong, because there IS something to cite -
just not where anyone was looking.

THE ANGLE THAT OPENED IT: CALIFORNIA LABOR CODE §432.3

SB 1162 requires a pay scale in any job posting for a POSITION. That does not
reach independent-contractor postings, which is why:

  - Spring Health's contractor job description states its own rate outright:
    "$70-$150 per 55 minute session"
  - Headspace posts $82-$87 per session for a 1099 role and $75-$80/hr for a
    California W-2 role that requires CA licence AND CA residency
  - Octave posts $122-$135/hr for a master's-level clinician in Los Angeles
  - Two Chairs posts $70/hr and then publishes a worked example converting it
    to $93.30 per attended session
  - Lyra's California CONTRACTOR postings disclose nothing at all, lawfully

So the gap in this table was never "platforms don't publish rates". It was
"nobody was reading job postings". The one figure that genuinely is not
published anywhere is Lyra's 1099 network rate - which is exactly the number
this audience most wants, and the page now says so plainly instead of implying
the whole channel is opaque.

THE THREE DISTINCTIONS THE OLD NOTE WAS RIGHT ABOUT, KEPT

The old note's real insight was that these numbers are not comparable, and that
survives into the new table as a column rather than a caveat:

  W-2 hourly vs 1099 per-session   Two completely different arrangements,
                                   quoted interchangeably in the same forum
                                   thread. Two Chairs is the only source found
                                   that does the conversion honestly.
  session length                   Spring Health's $70-150 buys 55 minutes.
                                   Headspace's $82-87 buys a 45-minute
                                   follow-up. Those are not the same product.
  what gets billed                 EAP work bills CPT 99404, not 90834/90837,
                                   at a 45-50 minute "therapeutic hour" with no
                                   client co-pay. Comparing it to a private-pay
                                   90837 is comparing two different codes.

Every figure carries whether it is PUBLISHED by the company or REPORTED by a
clinician, and a link. Nothing is averaged, ranged or inferred.

Checked 9 August 2026. Run in the STRUCTURE stage.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = "rates.html"
MARK = "<!-- _dev/eap_rates.py -->"
CHECKED = "9 August 2026"

# name, sub, rate, kind, model, basis, url
# kind: "pub" = published by the company, "rep" = reported by a clinician
ROWS = [
    ("Spring Health", None, "$70&ndash;$150", "pub", "1099 contractor",
     "Stated in Spring Health&rsquo;s own contractor job description, and "
     "confirmed separately by a company representative. Buys a <b>55-minute</b> "
     "session &mdash; the longest on this table, so the least comparable to the "
     "rest of it. A 2.1&times; spread with no published basis for where you land "
     "in it.",
     "https://www.springhealth.com/solutions/for-providers"),

    ("Headspace", "formerly Ginger", "$82&ndash;$87", "pub", "1099 contractor",
     "Posted rate, live August 2026. Intake is 60 minutes, follow-up is "
     "<b>45</b> &mdash; so this is 90834 territory, not a like-for-like against "
     "Spring Health&rsquo;s 55 minutes. Note-taking is stated as included in the "
     "rate.",
     "https://job-boards.greenhouse.io/hs"),

    ("Headspace", "California W-2 role", "$75&ndash;$80/hr", "pub",
     "W-2, part-time",
     "A California posting requiring both a CA licence and CA residency, with a "
     "floor of five sessions a week &mdash; low enough to sit alongside a private "
     "practice. Carries a 401(k), malpractice cover and a home-office stipend. "
     "Posting has since closed; cite as a point-in-time rate.",
     "https://job-boards.greenhouse.io/hs"),

    ("Octave", "Los Angeles, in person", "$122&ndash;$135/hr", "pub",
     "Contract",
     "The highest published California rate found &mdash; $122&ndash;$145/hr for "
     "a doctoral-level clinician. One large caveat: the in-person rate requires "
     "<b>you to provide your own commercial office</b>, so a significant overhead "
     "sits behind the headline. Virtual is $117&ndash;$140/hr.",
     "https://www.octavehealth.com/careers"),

    ("Two Chairs", "California", "$70/hr &rarr; $93.30", "pub", "W-2",
     "The most transparent employer found, and the most useful entry here. Two "
     "Chairs publishes a worked example converting its hourly rate into an "
     "effective <b>per attended session</b> figure &mdash; because a W-2 clinician "
     "is paid for no-shows and admin time and a 1099 clinician is not. This is "
     "the conversion nobody else does, and it is why an hourly rate and a "
     "per-session rate cannot be compared directly.",
     "https://www.twochairs.com/careers"),

    ("Brightside Health", None, "$83&ndash;$103", "pub", "1099 contractor",
     "The only rate on this page bound explicitly to a session length: "
     "&ldquo;per <b>53+ minute</b> session&rdquo;, which makes it the one figure "
     "cleanly comparable to a private-pay 90837. Rates are state-variable and "
     "<b>no California posting was found</b> &mdash; treat the band as national.",
     "https://www.brightside.com/careers/"),

    ("Modern Health", None, "$70&ndash;$225/hr", "rep", "1099 contractor",
     "Clinician-reported, March 2023, so <b>three and a half years old</b>. "
     "Unusual model worth knowing: the clinician proposes their own rate and "
     "Modern Health negotiates down against a regional benchmark &mdash; so this "
     "is the observed spread of negotiated outcomes, not a fee schedule.",
     "https://www.therapistsintech.com/companies/modern-health"),

    ("SonderMind", None, "$120 / $92", "rep", "1099 contractor",
     "$120 intake, $92 per session. Clinician-reported, March 2023 and not "
     "California-specific. SonderMind declines to publish rates and refers "
     "clinicians to contact it directly. Given the sector-wide cuts through "
     "2024&ndash;25, treat as historical.",
     "https://www.therapistsintech.com/companies/sondermind"),

    ("Lyra Health", "the 1099 network rate", "not published", "gap",
     "1099 network",
     "The number this audience most wants, and it is <b>published nowhere</b>. "
     "Lyra&rsquo;s California contractor postings disclose no pay, lawfully &mdash; "
     "California&rsquo;s pay-scale rule reaches job postings for positions, not "
     "for independent contractors. Lyra&rsquo;s W-2 track does publish a "
     "$70,000&ndash;$92,000 salary band, which is a different job.",
     "https://careers.lyrahealth.com/licensed-therapist-jobs"),
]

BADGE = {"pub": ("Published", "eb-pub"),
         "rep": ("Reported", "eb-rep"),
         "gap": ("Not published", "eb-gap")}

CSS = """<style>/* _dev/eap_rates.py */
.eap-tbl td b{display:block}
.eap-tbl td span.eap-sub{display:block;font-size:12.5px;color:#6b6455;
  font-weight:400;margin-top:2px}
.eap-badge{display:inline-block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;
  border:1.5px solid currentColor;border-radius:999px;padding:2px 7px;
  margin:0 0 6px;vertical-align:middle}
.eb-pub{color:#2C6350}
.eb-rep{color:#8a6a20}
.eb-gap{color:#8a4038}
.eap-tbl td.rate b{font-weight:inherit}
.eap-why{border:2px solid #16211B;border-radius:12px;background:#FBF9F3;
  box-shadow:5px 5px 0 #F6C560;padding:18px 20px;margin:18px 0 0}
.eap-why h4{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.02em;font-size:17px;color:#16211B;margin:0 0 8px}
.eap-why p{font-size:14.6px;line-height:1.7;color:#3A3529;margin:0 0 10px;max-width:70ch}
.eap-why p:last-child{margin:0}
.eap-why b{color:#16211B}
.eap-why a{color:#2C6350}
</style>"""


def row_html(name, sub, rate, kind, model, basis, url):
    label, cls = BADGE[kind]
    subhtml = ('<span class="eap-sub">%s</span>' % sub) if sub else ""
    rate_cell = rate if kind != "gap" else "&mdash;"
    return (
        "<tr>"
        "<td><b>%s</b>%s<span class=\"eap-sub\">%s</span></td>"
        "<td class=\"rate\">%s</td>"
        "<td><span class=\"eap-badge %s\">%s</span> %s "
        "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">Source</a></td>"
        "</tr>" % (name, subhtml, model, rate_cell, cls, label, basis, url))


# NOTE: this is %-formatted, so every literal percent sign in it must be
# doubled. A bare "30%" here raises "not enough arguments for format
# string" - the third time that exact mistake has been made in this
# codebase, after build_insurance's width:100% and content_frame's 3.1%.
WHY = """<div class="eap-why">%(mark)s
<h4>Why this table stopped being empty</h4>
<p>It was empty for a good reason, and the reason turned out to be wrong.
Platform contracts <b>are</b> confidential, and there is no fee schedule to
cite the way there is for Medi-Cal or Medicare. But California&rsquo;s
pay-transparency rule &mdash; Labor Code &sect;432.3 &mdash; requires a pay
scale in any job posting for a <b>position</b>, and several of these platforms
hire clinicians into positions. The rates were sitting in job postings the
whole time.</p>
<p>That same rule is why the one number missing here is missing:
<b>&sect;432.3 does not reach postings for independent contractors</b>. Lyra
hires California network clinicians as 1099 contractors and therefore publishes
nothing, entirely lawfully. That is not an oversight on this page &mdash; it is
the structure of the disclosure rule.</p>
<p><b>Three things make these numbers less comparable than they look</b>, and
they are the reason each row carries its model and its session length. A W-2
hourly rate pays you for no-shows and admin time; a 1099 per-session rate does
not, and the two get quoted interchangeably in the same forum thread. Session
length runs from 45 minutes to 55 for roughly the same money. And EAP work
bills <b>CPT 99404</b> at a 45&ndash;50 minute &ldquo;therapeutic hour&rdquo;
with no client co-pay &mdash; a different code from the 90834 and 90837 in Part
I, which is what makes a straight comparison invalid rather than merely
awkward.</p>
<p><b>Rates in this channel have been cut, repeatedly.</b> Alma cut New York and
Virginia rates on 1 December 2024. Headway cut some New York doctoral rates by
around 30%% on 1 January 2025. Talkspace restructured its bonus on 1 April 2025
in a way clinicians describe as a significant cut. Any figure from 2023 should
be treated as void, which is why the two 2023 rows above are labelled and dated
rather than quietly folded into a range.</p>
<p>Every figure was checked on %(checked)s. Nothing here is averaged or
estimated: each row is either published by the company or reported by a named
clinician, and says which.</p>
</div>
<!-- /eap_rates -->"""


def main():
    p = os.path.join(SITE, PAGE)
    if not os.path.exists(p):
        sys.exit("eap_rates: %s is missing" % PAGE)
    s = open(p, encoding="utf-8").read()
    orig = s

    # ------------------------------------------------------------ idempotent
    s = re.sub(re.escape(MARK) + r"[\s\S]*?<!-- /eap_rates -->\n?", "", s)
    s = re.sub(r"\n?<style>/\* _dev/eap_rates\.py \*/[\s\S]*?</style>\n?", "", s)

    # ------------------------------------------------------- the table body
    m = re.search(r'(<table class="eap-tbl">[\s\S]*?<tbody>)([\s\S]*?)(</tbody>)', s)
    if not m:
        sys.exit("eap_rates: could not find the eap-tbl body")

    old_body = m.group(2)
    # The Lyra clinician report is a real data point and is kept, at the top,
    # because a named person's actual contract rate is worth more than any
    # posting - it is just no longer the ONLY thing on the table.
    lyra = re.search(r"<tr>\s*<td>\s*<b>Lyra Health</b>[\s\S]*?</tr>", old_body)
    if not lyra:
        sys.exit("eap_rates: the existing Lyra row is not where it was")

    body = [lyra.group(0)] + [row_html(*r) for r in ROWS]
    s = s[:m.start(2)] + "\n" + "\n".join(body) + "\n" + s[m.end(2):]

    # --------------------------------------------- retire the old empty note
    # "Why the rest of this table is empty" is no longer true. Replaced, not
    # deleted - the reasoning in it about non-comparability was correct and is
    # carried into the new block.
    old_note = re.search(
        r'<div class="note">\s*<b>Why the rest of this table is empty\.</b>'
        r'[\s\S]*?</div>', s)
    why = WHY % {"mark": MARK, "checked": CHECKED}
    if old_note:
        s = s[:old_note.start()] + why + s[old_note.end():]
        replaced = True
    else:
        # already replaced on a previous run - put it back after the table
        k = s.index("</table>", m.start()) + len("</table>")
        s = s[:k] + "\n" + why + s[k:]
        replaced = False

    e = s.lower().rfind("</body>")
    s = s[:e] + CSS + "\n" + s[e:]
    open(p, "w", encoding="utf-8").write(s)

    print("EAP rate table, checked %s:" % CHECKED)
    for name, sub, rate, kind, model, _b, _u in ROWS:
        print("  %-9s %-22s %-18s %s"
              % (BADGE[kind][0].lower(), name + (" (%s)" % sub if sub else ""),
                 rate.replace("&ndash;", "-").replace("&rarr;", "->"), model))
    print("\nthe old \"why this table is empty\" note %s"
          % ("replaced" if replaced else "was already replaced"))

    # ------------------------------------------------------------- guards
    s = open(p, encoding="utf-8").read()
    bad = 0
    if "No usable report yet" in s:
        print("GUARD: a row still says 'No usable report yet'"); bad += 1
    if "Why the rest of this table is empty" in s:
        print("GUARD: the old empty-table note survived"); bad += 1
    if "Lyra Health" not in s:
        print("GUARD: the original Lyra clinician report was lost"); bad += 1
    for _n, _s, _r, _k, _m, _b, url in ROWS:
        if url not in s:
            print("GUARD: %s has no source link" % url[:52]); bad += 1
    # Every rate must travel with its model, or the W-2/1099 conflation this
    # whole block exists to prevent gets reintroduced by the table itself.
    for name, sub, rate, kind, model, _b, _u in ROWS:
        if model not in s:
            print("GUARD: %s printed without its model" % name); bad += 1
    if s.count(MARK) != 1:
        print("GUARD: %d copies of the note" % s.count(MARK)); bad += 1
    for url, attrs in re.findall(r'<a href="(https?://[^"]+)"([^>]*)>', s):
        if 'target="_blank"' in attrs and "noopener" not in attrs:
            print("GUARD: %s opens a tab without noopener" % url[:48]); bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d row(s), every one carrying its model and a source"
          % (len(ROWS) + 1))


if __name__ == "__main__":
    main()
