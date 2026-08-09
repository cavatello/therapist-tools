#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make "where you apply" a link you can actually click.

WHAT WAS WRONG

The panels page names the exact route onto each California payer's behavioural
health network - Anthem's join form, Blue Shield's application packet, Optum's
Provider Express, Kaiser Southern California's letter of intent - and then
makes the reader go and find every one of them in a search engine. The page
does the hard part (which panels are open, in what order, on what statutory
clock) and stops one inch short of the part that costs the reader an hour.

Same for the two universal steps. "You apply at NPPES" and "the provider login
is still at proview.caqh.org" are both plain text.

EVERY URL HERE WAS OPENED AND CHECKED ON 9 AUGUST 2026

That is the project rule for citations and it earned its keep here - two of the
obvious guesses are wrong:

  - Aetna's classic behavioural-health application deep link now REDIRECTS to
    an `extaz-oci.aetna.com` host that is a JS shell, robots-disallowed, and
    named like infrastructure. A copy of the old form still answers on
    myplanportal.com, but aetna.com no longer points at it. So this links the
    stable "Join the Aetna network" hub instead of either.

  - Availity's old login URL (`apps.availity.com/availity/web/public.elegant.
    login`) now redirects into `essentials.availity.com/static/public/onb/...`.
    Carelon's own page is linked rather than Availity's.

Two more findings worth carrying in the copy rather than the link:

  - Magellan has NO public self-service application. Its own page says only
    "contact your Network Contact", and that contact lookup sits behind a
    session-bound gateway with a jsessionid in the URL, so there is nothing
    stable to link. That is stated as a fact about Magellan, not hidden.

  - Kaiser Permanente NORTHERN California publishes no route for individual
    clinicians at all - checked across three levels of their provider site.
    Southern California publishes a letter-of-intent email. The asymmetry is
    real and is now on the page.

WHY A PASS AND NOT A FIX IN THE BUILDER

`mock/articles/build_articles.py` cannot run any more - its `_chrome.html`
input is gone, the same way `mock/psychedelics/build_psy.py` lost its `data/`
directory. Those article pages are frozen HTML, and a pass is the only way to
change them. Written so it re-applies cleanly over its own output.

Idempotent, guarded. Run in the STRUCTURE stage.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = "insurance-panels-california-therapist.html"
MARK = "<!-- _dev/payer_links.py -->"
CHECKED = "9 August 2026"

# (exact phrase already on the page, url, why this url and not another)
#
# Matched on the phrase rather than the table row, because the row markup is
# generated and the phrases are authored - the phrase is the thing that will
# still be there after the next restyle.
LINKS = [
    ("Anthem&rsquo;s join-our-network form",
     "https://providers.anthem.com/california-provider/our-network/join",
     "Anthem has no behavioural-health-specific application in California. An "
     "LMFT goes through the same CAQH-then-Availity funnel as any other "
     "practitioner, and this is where it starts."),

    ("Application packet, signed contract and rates",
     "https://www.blueshieldca.com/en/provider/guidelines-resources/"
     "prospective-providers/join-behavioral-health-providers",
     "The clearest page any California payer publishes for this audience. "
     "Carries the individual-provider application PDF, the email, the fax, and "
     "a stated 45-60 day turnaround."),

    ("Behavioral Health Provider Application Request form",
     "https://www.aetna.com/health-care-professionals/join-the-aetna-network.html",
     "NOT the old behavioral-health-application.html deep link, which now "
     "redirects to a robots-disallowed JS shell on an extaz-oci host."),

    ("Interest form only",
     "https://static.evernorth.com/assets/evernorth/provider/resourceLibrary/"
     "behavioralResources/doingBusinessWithUs/cbhCredentialing.html",
     "The interest form itself is a forms.office.com URL, which will rot. The "
     "credentialing page carries the pause notice and the form link."),

    ("Provider Express, Join Our Network",
     "https://public.providerexpress.com/content/ope-provexpr/us/en/"
     "our-network/jon.html",
     "The next page along is called jon-states.html and contains no state "
     "table, so it will be renamed. This one is stable."),

    ("Behavioral Health Network Participation Request form",
     "https://www.healthnet.com/content/healthnet/en_us/providers/"
     "work-with-hn-menu/join-network-menu.html",
     "The PDF sits on a content/dam path that changes at every form revision. "
     "The landing page names MFTs explicitly."),

    ("Carelon payer space in Availity",
     "https://www.carelonbehavioralhealth.com/providers/join-our-network",
     "Carelon's own page, not Availity's - Availity's login URL now redirects "
     "to a different host."),

    ("magellanprovider.com",
     "https://www.magellanprovider.com/MHS/MGL/provnet/join_network/",
     "There is no application here to link. The page's entire instruction is "
     "to contact a Network Contact, and that lookup is session-bound."),
]

# Inline links in the prose, outside the table.
PROSE = [
    ("You apply at NPPES", "NPPES", "https://nppes.cms.hhs.gov/",
     "The application portal. NOT npiregistry.cms.hhs.gov, which is the public "
     "lookup and a common mis-link."),
    ("proview.caqh.org", "proview.caqh.org", "https://proview.caqh.org/",
     "Still live after the DataSpring rebrand - caqh.org now redirects to "
     "dataspring.com, but the provider login did not move."),
]

# The two public payers the page does not mention at all, and the routes for
# them, which are the best-documented of the lot.
PUBLIC = """%(mark)s
<section class="pl-pub" id="the-public-payers">
<h2>The two public payers, which the table above leaves out</h2>
<p>Both publish a real route, and both are better documented than any
commercial payer on this page.</p>
<dl class="pl-dl">
<dt>Medi-Cal</dt>
<dd>The Department of Health Care Services keeps
<a href="https://www.dhcs.ca.gov/providers-partners/licensed-marriage-and-family-therapists-application-information/" target="_blank" rel="noopener">a
page specifically for marriage and family therapists</a>, which lists the
twelve document categories you will be asked to upload. Applications go through
<b>PAVE</b>, the Provider Application and Validation for Enrollment portal.
Worth knowing before you start Carelon: Carelon will ask for a Medi-Cal ID or
proof of a PAVE application before it will consider you for its Medi-Cal
network.</dd>
<dt>Medicare</dt>
<dd>MFTs became eligible to enrol in Medicare in 2024. CMS's
<a href="https://www.cms.gov/files/document/marriage-and-family-therapists-and-mental-health-counselors-faq.pdf" target="_blank" rel="noopener">FAQ
for marriage and family therapists and mental health counselors</a> (May 2024)
sets out the path: an NPI first, then an Identity &amp; Access account, then
either <a href="https://www.cms.gov/medicare/enrollment-renewal/providers-suppliers/chain-ownership-system-pecos" target="_blank" rel="noopener">PECOS</a>
or the paper CMS-855I.</dd>
</dl>
<p class="pl-note">Every link on this page was opened and checked on %(checked)s.
Two payers publish no route for an individual clinician at all: <b>Magellan</b>,
whose own page says only to contact a Network Contact, and <b>Kaiser Permanente
Northern California</b> &mdash; Southern California publishes a letter-of-intent
address, Northern California publishes nothing.</p>
</section>
<!-- /payer_links -->"""

CSS = """<style>/* _dev/payer_links.py */
.pl-pub{margin:34px 0}
.pl-pub h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.03em;font-size:24px;color:#16211B;margin:0 0 10px}
.pl-pub>p{font-size:15.4px;line-height:1.68;color:#635E53;margin:0 0 14px;max-width:70ch}
.pl-dl{border:2px solid #16211B;border-radius:12px;background:#FBF9F3;
  box-shadow:5px 5px 0 #16211B;padding:18px 20px;margin:0 0 14px}
.pl-dl dt{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.13em;text-transform:uppercase;color:#2C6350;margin:0 0 6px}
.pl-dl dd{margin:0 0 16px;font-size:15px;line-height:1.7;color:#3A3529;max-width:70ch}
.pl-dl dd:last-child{margin:0}
.pl-dl a{color:#2C6350}
.pl-note{font-size:13.6px;line-height:1.66;color:#635E53;max-width:74ch;margin:0}
.pl-note b{color:#16211B}
</style>"""


def main():
    p = os.path.join(SITE, PAGE)
    if not os.path.exists(p):
        sys.exit("payer_links: %s is missing" % PAGE)
    s = open(p, encoding="utf-8").read()

    # ------------------------------------------------------------ idempotent
    s = re.sub(re.escape(MARK) + r"[\s\S]*?<!-- /payer_links -->\n?", "", s)
    s = re.sub(r"\n?<style>/\* _dev/payer_links\.py \*/[\s\S]*?</style>\n?", "", s)
    # unwrap any link this pass added before
    s = re.sub(r'<a class="pl"[^>]*>([\s\S]*?)</a>', r"\1", s)

    print("verified %s. linking:" % CHECKED)
    missing = 0

    def anchor(text, url):
        return ('<a class="pl" href="%s" target="_blank" rel="noopener">%s</a>'
                % (url, text))

    # --------------------------------------------------------- table phrases
    for phrase, url, why in LINKS:
        n = s.count(phrase)
        if n == 0:
            print("  MISSING  %-46s" % phrase[:46])
            missing += 1
            continue
        # The FIRST occurrence is the table cell; later ones are the numbered
        # citation list at the foot of the page, which already carries its own
        # links and must not be wrapped in a second one.
        s = s.replace(phrase, anchor(phrase, url), 1)
        print("  ok       %-46s -> %s%s"
              % (phrase[:46], url[:52],
                 "  (also in citations, left alone)" if n > 1 else ""))

    # ---------------------------------------------------------- prose links
    for context, text, url, why in PROSE:
        if context not in s:
            print("  MISSING  %s" % context)
            missing += 1
            continue
        # link only the word inside its own sentence, not every occurrence
        i = s.index(context)
        j = s.index(text, i)
        s = s[:j] + anchor(text, url) + s[j + len(text):]
        print("  ok       %-46s -> %s" % (text[:46], url[:52]))

    # ------------------------------------------- a citation that went stale
    # Citation [36] points at myplanportal.com, which still serves Aetna's
    # classic behavioural-health form but which aetna.com no longer links to.
    # It was correct when it was written; it is now a link into a deprecated
    # surface. Repointed at the hub, which is the same page the table links.
    stale = ("https://www.myplanportal.com/health-care-professionals/forms/"
             "behavioral-health-application.html")
    fresh = "https://www.aetna.com/health-care-professionals/join-the-aetna-network.html"
    if stale in s:
        s = s.replace(stale, fresh)
        print("  ok       citation [36] repointed off the deprecated "
              "myplanportal copy")

    # ------------------------------------------------- the two public payers
    block = PUBLIC % {"mark": MARK, "checked": CHECKED}
    # after the table's section, before the page's closing furniture
    anchor_pat = re.search(r"</table>\s*</div>", s)
    if not anchor_pat:
        print("  MISSING  the panels table - nowhere to put the public payers")
        missing += 1
    else:
        k = anchor_pat.end()
        s = s[:k] + "\n" + block + "\n" + s[k:]
        print("  ok       Medi-Cal and Medicare block added after the table")

    e = s.lower().rfind("</body>")
    s = s[:e] + CSS + "\n" + s[e:]

    open(p, "w", encoding="utf-8").write(s)

    # ------------------------------------------------------------- guards
    s = open(p, encoding="utf-8").read()
    bad = missing
    for _phrase, url, _why in LINKS:
        if url not in s:
            print("GUARD: %s did not land" % url[:60]); bad += 1
    for _c, _t, url, _w in PROSE:
        if url not in s:
            print("GUARD: %s did not land" % url[:60]); bad += 1
    if s.count(MARK) != 1:
        print("GUARD: %d copies of the public-payer block" % s.count(MARK)); bad += 1

    # Every external link opens a tab, so every one needs noopener.
    for url, attrs in re.findall(r'<a class="pl" href="(https?://[^"]+)"([^>]*)>', s):
        if "noopener" not in attrs:
            print("GUARD: %s opens a tab without noopener" % url[:50]); bad += 1

    # The two URLs the research proved wrong must never appear.
    for wrong, why in (
        ("npiregistry.cms.hhs.gov", "the public NPI lookup, not the application"),
        ("extaz-oci.aetna.com", "a robots-disallowed JS shell"),
        ("apps.availity.com", "redirects to a different host now"),
        ("jsessionid", "a session-bound URL that cannot be linked"),
        ("myplanportal.com", "a deprecated copy aetna.com no longer points at"),
    ):
        if wrong in s:
            print("GUARD: the page links %s - %s" % (wrong, why)); bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    n = len(re.findall(r'<a class="pl"', s))
    print("\nguards clean - %d verified link(s) on %s" % (n, PAGE))


if __name__ == "__main__":
    main()
