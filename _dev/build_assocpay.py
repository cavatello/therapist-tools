#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What associate jobs actually pay in Los Angeles and the Bay Area.

THE QUESTION THIS ANSWERS

Posted to a California AMFT/APCC/ASW registration support group by somebody
weighing offers:

  "Private practice: 20-25 clients a week, higher per-session rate, admin
   hours at $18-20/hr, doesn't add up to a 40 hour week. Nonprofit: $70k-$75k
   for a 40-hour week regardless of caseload, 10-25 clients a week. I'm
   struggling to see why I'd choose a private practice offer over a set,
   predictable salary?"

WHY THIS IS A SEPARATE PAGE AND NOT A SECTION SOMEWHERE

The site already has two calculators that do the arithmetic:
`associate-mft-job-advisor.html` computes take-home and the real hourly, and
`amft-3000-hours-california.html` projects a licensure date. Neither carries
what the question actually needs, which is **evidence** - named California
employers, published pay scales, the local wage floors the offer has to clear,
and the loan-repayment programs that are worth more than the entire salary
gap. That is a research page, not a calculator, and it links to both rather
than rebuilding either.

THE FOUR FINDINGS THAT REFRAME THE QUESTION

1. **$70,000 is $304 under the line.** California's 2026 exempt-salary floor is
   two times the state minimum wage for full-time work: $16.90 x 2 x 2,080 =
   $70,304. A "$70k salary for a 40-hour week regardless of caseload" cannot
   lawfully be an exempt salary in 2026. Either the employer owes overtime on
   every hour past 40, or the classification is wrong. The threshold moves with
   the STATE minimum wage, not the local one, so it is the same figure in
   Fresno and in San Francisco.

2. **$18/hr admin pay is below minimum wage in the City of Los Angeles.** From
   1 July 2026 the city floor is $18.42, unincorporated LA County $18.47, San
   Francisco and Berkeley $19.61, Emeryville $20.34. And per-session pay is
   piece rate, so under Labor Code 226.2 the non-session hours - notes,
   no-shows, meetings, required supervision - have to be paid separately at no
   less than the applicable minimum wage. The employer may not average the
   session rate across them.

3. **Above about 17 direct clinical hours a week, working harder does not
   license you sooner.** 1,750 direct clinical hours over the statutory
   104-week minimum is 16.83 hours a week. Past that the calendar binds, not
   the caseload. Below it, every hour is a week: at 10 clients a week an AMFT
   needs 175 weeks of clinical work, at 20 the 104-week floor takes over. So
   "10-25 clients a week" is not a detail in the nonprofit offer. It is the
   difference between two years and three and a half.

4. **The loan-repayment gap is bigger than the salary gap.** NHSC is closed to
   associates - it wants a full, unrestricted license. But California's
   BH-CONNECT MBH-SLRP names AMFT, ASW and APCC in Tier 2 at up to $180,000
   against a four-year obligation, HCAI's LMHSPEP names them too at $15,000 up
   to three times, and PSLF turns on the employer being a 501(c)(3) or
   government body rather than on the job title. All three are unavailable in a
   private practice. That is not a rounding error on a $5,000 salary
   difference.

WHAT IS DELIBERATELY NOT ON THE PAGE

A recommendation. Both offers are defensible and the page says which facts
decide it, not which offer to take. And no invented figures: every number in
the pay tables is a published pay scale or a posted range, labelled with its
source, and the derived numbers are marked as derived.

METHOD NOTE FOR WHOEVER MAINTAINS THIS

County salary schedules and civil-service class specifications will still
resolve in a year. Nonprofit applicant-tracking links will not. The pay tables
therefore lead with the public-agency figures and treat the nonprofit postings
as dated observations, with the date stated.

Idempotent - rewrites its page from scratch every run. Guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PAGE = "associate-therapist-pay-los-angeles-bay-area.html"
CHROME_FROM = os.path.join(SITE, "hiring-first-associate-california-therapist.html")
CHECKED = "August 2026"

ADVISOR = "associate-mft-job-advisor.html"
HOURS = "amft-3000-hours-california.html"
COL = "therapist-cost-of-living-california.html"

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"
MUTED = "#635E53"
RED = "#B5483F"

# --------------------------------------------------------------- the floors
# California's exempt-salary test is two times the STATE minimum wage for
# full-time work, so it is one number statewide and does not move with the
# local ordinance. 2,080 hours is 40 x 52.
CA_MIN = 16.90
EXEMPT = CA_MIN * 2 * 2080          # 70304.0

# Local general minimum wages effective 1 July 2026, and the state floor for
# comparison. Sorted high to low, because the reader is checking whether an
# offered admin rate clears the one where they work.
#
# ON THE FOURTH COLUMN, WHICH IS A URL OR None AND NOT A URL FOR EVERY ROW.
#
# The first version of this table linked all eleven city names to the city's
# own minimum-wage page. Six of those URLs were CONSTRUCTED from a plausible
# pattern rather than found, and a link check afterwards showed what that is
# worth: emeryville.org/191/Minimum-Wage-Ordinance and the two others tried
# returned 404, and several city sites block a checker outright so a bad link
# would not even have announced itself.
#
# So a name is a link only where the official page has been opened and seen to
# resolve, and is plain text otherwise. The figures for the unlinked rows all
# come from one source that HAS been read - the CalChamber summary cited under
# the table - and saying so once is more honest than eleven links of which six
# are guesses. A wrong citation is worse than a shared one.
WAGE_FLOORS = [
    ("Emeryville", "20.34", "Alameda County", None),
    ("San Francisco", "19.61", "City and county",
     "https://www.sf.gov/information--minimum-wage-ordinance"),
    ("Berkeley", "19.61", "Alameda County",
     "https://berkeleyca.gov/doing-business/operating-berkeley/"
     "workforce-standards-and-enforcement"),
    ("Pasadena", "18.57", "LA County", None),
    ("Milpitas", "18.50", "Santa Clara County", None),
    ("LA County &mdash; unincorporated", "18.47", "Not the City of LA",
     "https://dcba.lacounty.gov/minimum-wage/"),
    ("Santa Monica", "18.47", "LA County", None),
    ("City of Los Angeles", "18.42", "Two hours a week in the city is enough",
     "https://wagesla.lacity.gov/"),
    ("Fremont", "18.05", "Alameda County", None),
    ("Alameda (city)", "17.76", "Not Alameda County", None),
    ("California &mdash; state floor", "16.90", "Anywhere with no local ordinance",
     "https://www.dir.ca.gov/dlse/faq_minimumwage.htm"),
]

# ------------------------------------------------------ public agency scales
# name, class, published scale, pre-licensed?, source label, url
PUBLIC = [
    ("City and County of San Francisco", "2930 Behavioral Health Clinician",
     "$118,820 &ndash; $144,352",
     "Yes &mdash; the class specification accepts ASW, AMFT and APCC "
     "registration alongside full licensure",
     "careers.sf.gov class 2930, rates effective 1 July 2026",
     "https://careers.sf.gov/classifications/?classCode=2930"),
    ("County of Santa Clara", "Marriage &amp; Family Therapist I (P97)",
     "$101,130 &ndash; $122,425",
     "Level I of the series",
     "County pay schedule, run date 3 August 2026",
     "https://files.sccgov.org/bc-entesa/basic_salary_plan.pdf"),
    ("County of Alameda", "Behavioral Health Clinician I (6505)",
     "$97,227 &ndash; $111,599",
     "Yes &mdash; the spec calls it the trainee-level class and requires ASW, "
     "AMFT, APCC or psychological associate registration within six months",
     "Alameda County class specification 6505",
     "https://www.jobapscloud.com/Alameda/specs/classspecdisplay.asp?ClassNumber=6505"),
    ("County of Los Angeles", "Mental Health Clinician I / Psychiatric Social "
     "Worker I",
     "$76,804 &ndash; $98,035",
     "Entry step of a flexibly-staffed series",
     "LA County class and salary listing, 1 August 2026",
     "https://file.lacounty.gov/SDSInter/lac/1043266_alpha.pdf"),
]

# ------------------------------------------------------- nonprofit postings
# employer, role, city, range, note
LA_NONPROFIT = [
    ("Wellnest", "Clinical Therapist I", "Los Angeles",
     "$70,716 &ndash; $94,475",
     "Two Clinical Therapist I postings at this band; the intensive-services "
     "post tops out at $79,344.",
     "https://www.wellnestla.org/careers/"),
    ("The Help Group", "Therapist &mdash; CAPIT", "Lynwood",
     "$73,560 &ndash; $84,760",
     "Names AMFT, APCC, ACSW. States supervision toward licensure; $2,500 "
     "sign-on for a BBS-registered full-time therapist.",
     "https://www.thehelpgroup.org/careers/"),
    ("The Help Group", "In-home therapist", "Inglewood",
     "$68,560 &ndash; $83,960",
     "Supervision toward licensure stated.",
     "https://www.thehelpgroup.org/careers/"),
    ("Pacific Clinics", "Clinician I", "Los Angeles",
     "$66,560 &ndash; $81,860",
     "BBS or Board of Psychology registration required. Posting states the "
     "role &ldquo;meets revenue and productivity standards&rdquo; without "
     "giving a number. Up to 7.5% bilingual differential.",
     "https://careers.pacificclinics.org/"),
    ("The Help Group", "School-based therapist", "Sherman Oaks",
     "$58,207 &ndash; $77,672",
     "The lowest floor found in LA. School-year roles are often ten months.",
     "https://www.thehelpgroup.org/careers/"),
]

BAY_NONPROFIT = [
    ("Seneca Family of Agencies", "Wraparound therapist", "San Jose",
     "$90,041 &ndash; $104,041",
     "ASW, AMFT, APCC or licensed. <b>+$4,000 on licensure</b>, $2,000 "
     "sign-on. States individual and group supervision, case conferences and "
     "licensure courses provided.",
     "https://www.senecafoa.org/careers"),
    ("Seneca Family of Agencies", "Bilingual school therapist", "El Sobrante",
     "$82,156 &ndash; $96,156",
     "+$4,000 on licensure.",
     "https://www.senecafoa.org/careers"),
    ("RAMS, Inc.", "Bilingual behavioral health clinician", "San Francisco",
     "$80,307 &ndash; $95,891",
     "Registration <i>or</i> licensure accepted. RAMS pays its licensed "
     "Mental Health Counselor role the same band, which is unusual and worth "
     "asking about.",
     "https://www.ramsinc.org/careers/"),
    ("Seneca Family of Agencies", "School therapist &mdash; floater",
     "San Francisco", "$78,666 &ndash; $92,666",
     "+$4,000 on licensure.",
     "https://www.senecafoa.org/careers"),
    ("Seneca Family of Agencies", "Crisis therapist", "Concord",
     "$75,409 &ndash; $89,409",
     "+$4,000 on licensure.",
     "https://www.senecafoa.org/careers"),
    ("Pacific Clinics", "Clinician I", "San Jose / Los Gatos",
     "$71,760 &ndash; $90,358",
     "Associate registration; must license within five years. 8% differential "
     "once licensed.",
     "https://careers.pacificclinics.org/"),
]

# ------------------------------------------------- private practice postings
# employer, city, session rate, non-session pay, caseload asked, note
PRIVATE = [
    ("A Los Angeles solo practice", "Los Angeles",
     "$50 per insurance session; 50/50 on cash pay",
     "1 hour paid admin, supervision paid at $17/hr",
     "22&ndash;26 a week",
     "W-2. The $17 supervision rate was lawful when posted and is now "
     "$1.42 under the City of Los Angeles floor."),
    ("A Long Beach practice", "Long Beach",
     "$35 &ndash; $75 per session",
     "$18 &ndash; $25/hr for supervision, meetings and charting",
     "25 a week",
     "W-2, 15 guaranteed hours in the first 30 days. The bottom of that "
     "admin band is now under the LA County unincorporated floor."),
    ("A Walnut Creek institute", "Walnut Creek",
     "$35 &ndash; $45 per session hour",
     "Group supervision included; no separate admin rate stated",
     "10&ndash;15 a week minimum",
     "W-2. No stated pay for notes or no-shows, which is the gap "
     "Labor Code &sect;226.2 is about."),
    ("A California telehealth practice", "Statewide, remote",
     "$30 &ndash; $35 per session",
     "5&ndash;6 paid admin hours a week at a full caseload, plus paid "
     "clinical supervision",
     "Not stated",
     "W-2. The compliant shape: piece rate for sessions, hourly for "
     "everything else."),
]

# ------------------------------------------------------------ hours to license
# clinical hrs/week, weeks to 1,750 clinical, what binds
def hours_rows():
    rows = []
    for c in (6, 8, 10, 12, 15, 17, 20, 25, 30):
        wk = -(-1750 // c)          # ceil
        binds = "the 104-week floor" if wk <= 104 else "your caseload"
        eff = max(wk, 104)
        rows.append((c, wk, eff, round(eff / 52.0, 1), binds))
    return rows


# ------------------------------------------------------------ loan repayment
LOANS = [
    ("BH-CONNECT MBH-SLRP &mdash; Tier 2", "Up to <b>$180,000</b>",
     "AMFT, ASW and APCC are named in Tier 2",
     "Four years full-time (32 hrs/week of direct client care) at a Medi-Cal "
     "safety-net site &mdash; FQHC, community mental health center, rural "
     "health clinic, or a Medi-Cal-enrolled behavioral health facility. "
     "Cycle 2 closed 29 May 2026; the next is expected May 2027.",
     "https://hcai.ca.gov/workforce/initiatives/behavioral-health-bh-connect/mbhslrp/"),
    ("HCAI LMHSPEP", "Up to <b>$15,000</b>, receivable three times",
     "ACSW, AMFT and APCC named alongside licensed clinicians",
     "Twelve months minimum at 32 hrs/week of direct client care, at a "
     "mental-health HPSA, a publicly funded or county-contracted nonprofit "
     "facility, a children's hospital, a correctional facility, a public "
     "school, an SUD facility or a veterans' facility.",
     "https://hcai.ca.gov/workforce/financial-assistance/loan-repayment/lmhspep"),
    ("PSLF", "The remaining balance, after 120 payments",
     "Any job, as long as the <i>employer</i> qualifies",
     "The employer must be a government body, a 501(c)(3), or a qualifying "
     "non-501(c)(3) nonprofit. Full-time is an average of 30 hours a week, "
     "and hours at two part-time qualifying employers can be combined. "
     "1099 work does not count, which for an associate is moot.",
     "https://studentaid.gov/manage-loans/forgiveness-cancellation/public-service"),
    ("NHSC Loan Repayment", "Up to $50,000 &mdash; but not yet",
     "<b>Closed to associates.</b> Requires a full, permanent, unencumbered, "
     "unrestricted license",
     "MFTs, LCSWs and LPCCs are all eligible disciplines once licensed. Worth "
     "knowing now because it changes what a post-licensure job is worth: the "
     "SUD variant pays up to $75,000 and the rural variant up to $100,000.",
     "https://nhsc.hrsa.gov/loan-repayment/nhsc-loan-repayment-program"),
    ("California SLRP", "$50,000 full-time",
     "<b>Closed to associates.</b> Requires a valid unrestricted California "
     "license",
     "Two-year obligation at a HPSA site. The 2026 cycle runs 15 July to "
     "15 September 2026.",
     "https://hcai.ca.gov/workforce/financial-assistance/loan-repayment/slrp/"),
]

# ------------------------------------------------------------------- sources
SOURCES = [
    ("Minimum wage and the exempt-salary floor", [
        ("DIR minimum wage FAQ &mdash; $16.90 statewide from 1 January 2026",
         "https://www.dir.ca.gov/dlse/faq_minimumwage.htm"),
        ("City of Los Angeles Office of Wage Standards &mdash; $18.42 from "
         "1 July 2026", "https://wagesla.lacity.gov/"),
        ("LA County Consumer &amp; Business Affairs &mdash; $18.47 in "
         "unincorporated areas from 1 July 2026",
         "https://dcba.lacounty.gov/minimum-wage/"),
        ("CalChamber summary of the 1 July 2026 local increases",
         "https://hrwatchdog.calchamber.com/2026/06/"
         "california-local-minimum-wage-increases-for-july-1-2026/"),
        ("Labor Code &sect;515 &mdash; the exempt-salary test",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=515.&lawCode=LAB"),
    ]),
    ("How an associate may be paid", [
        ("Bus. &amp; Prof. Code &sect;4980.43.3 &mdash; employee or volunteer, "
         "not an independent contractor (AMFT)",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4980.43.3.&lawCode=BPC"),
        ("Bus. &amp; Prof. Code &sect;4996.23.2 &mdash; the same rule for ASWs",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4996.23.2.&lawCode=BPC"),
        ("Bus. &amp; Prof. Code &sect;4999.46.3 &mdash; the same rule for APCCs",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4999.46.3.&lawCode=BPC"),
        ("Labor Code &sect;226.2 &mdash; piece rate, and paying separately for "
         "non-productive time",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=226.2.&lawCode=LAB"),
        ("DIR &mdash; what piece-rate compensation is",
         "https://dir.ca.gov/pieceratebackpayelection/piecerate.html"),
        ("Labor Code &sect;2802 &mdash; the employer reimburses necessary "
         "business expenses",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=2802.&lawCode=LAB"),
        ("Labor Code &sect;1194 &mdash; unpaid wages, plus interest and "
         "attorney's fees, notwithstanding any agreement to work for less",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=1194.&lawCode=LAB"),
        ("Labor Code &sect;2783 &mdash; the exemption list that includes "
         "psychologists and not MFTs, LCSWs or LPCCs",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=2783.&lawCode=LAB"),
        ("CAMFT Pre-licensed Corner &mdash; labor laws that affect MFTs",
         "https://www.camft.org/Resources/Pre-licensed-Corner/"
         "Labor-Laws-that-Affect-MFTs"),
    ]),
    ("The hours", [
        ("Bus. &amp; Prof. Code &sect;4980.43 &mdash; 3,000 hours, 104 weeks, "
         "1,750 direct clinical, 500 relational, 40 a week",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4980.43.&lawCode=BPC"),
        ("Bus. &amp; Prof. Code &sect;4980.43.2 &mdash; supervision, and the "
         "extra unit past ten clinical hours",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4980.43.2.&lawCode=BPC"),
        ("Bus. &amp; Prof. Code &sect;4996.23 &mdash; the ASW requirements, "
         "including 2,000 clinical and 750 psychotherapy",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4996.23.&lawCode=BPC"),
        ("Bus. &amp; Prof. Code &sect;4999.46 &mdash; the APCC requirements",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4999.46.&lawCode=BPC"),
        ("Bus. &amp; Prof. Code &sect;4984.01 &mdash; five renewals, six years",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=4984.01.&lawCode=BPC"),
        ("BBS statutes and regulations, January 2026 edition",
         "https://www.bbs.ca.gov/pdf/publications/lawsregs.pdf"),
    ]),
    ("Pay scales", [
        ("City and County of San Francisco &mdash; class 2930",
         "https://careers.sf.gov/classifications/?classCode=2930"),
        ("County of Alameda &mdash; class specification 6505",
         "https://www.jobapscloud.com/Alameda/specs/classspecdisplay.asp"
         "?ClassNumber=6505"),
        ("County of Los Angeles &mdash; class and salary listing",
         "https://file.lacounty.gov/SDSInter/lac/1043266_alpha.pdf"),
        ("County of Santa Clara &mdash; basic salary plan",
         "https://files.sccgov.org/bc-entesa/basic_salary_plan.pdf"),
        ("Labor Code &sect;432.3 &mdash; why a posting has to carry a pay "
         "scale at all",
         "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
         "?sectionNum=432.3.&lawCode=LAB"),
    ]),
    ("Loan repayment and benefits", [
        ("HCAI &mdash; BH-CONNECT Medi-Cal behavioral health student loan "
         "repayment",
         "https://hcai.ca.gov/workforce/initiatives/behavioral-health-bh-connect/mbhslrp/"),
        ("HCAI &mdash; LMHSPEP",
         "https://hcai.ca.gov/workforce/financial-assistance/loan-repayment/lmhspep"),
        ("HCAI &mdash; California SLRP",
         "https://hcai.ca.gov/workforce/financial-assistance/loan-repayment/slrp/"),
        ("NHSC Loan Repayment Program",
         "https://nhsc.hrsa.gov/loan-repayment/nhsc-loan-repayment-program"),
        ("34 CFR 685.219 &mdash; the PSLF employer and full-time definitions",
         "https://www.ecfr.gov/current/title-34/subtitle-B/chapter-VI/part-685/"
         "subpart-B/section-685.219"),
        ("BLS Employer Costs for Employee Compensation, March 2026",
         "https://www.bls.gov/news.release/ecec.nr0.htm"),
        ("KFF 2025 Employer Health Benefits Survey",
         "https://www.kff.org/health-costs/"
         "annual-family-premiums-for-employer-coverage-rise-6-in-2025-nearing-"
         "27000-with-workers-paying-6850-toward-premiums-out-of-their-paychecks/"),
    ]),
]


# ------------------------------------------------------------------ the CSS
CSS = """<style>/* _dev/build_assocpay.py */
.ap-wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.ap-sec{margin:36px 0}
.ap-k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:%(pine)s;margin:0 0 6px}
.ap-h{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.032em;font-size:27px;line-height:1.12;color:%(ink)s;margin:0 0 10px}
.ap-h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:20px;line-height:1.18;color:%(ink)s;
  margin:30px 0 8px}
.ap-d{font-size:15.4px;line-height:1.68;color:%(muted)s;margin:0 0 16px;max-width:68ch}
.ap-d b{color:%(ink)s}
.ap-d i{color:%(ink)s;font-style:italic}
.ap-d a{color:%(pine)s}

/* -------------------------------------------------------------- the hero */
.ap-hero{border:2px solid %(ink)s;border-radius:16px;box-shadow:8px 8px 0 %(ink)s;
  background:%(pine)s;color:#fff;padding:30px 30px 26px;margin:0 0 26px}
.ap-hero .hk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:#FFD37A;margin:0 0 12px}
.ap-hero h1{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.034em;font-size:41px;line-height:1.03;color:#fff;margin:0 0 14px;
  max-width:20ch}
.ap-hero .hl{font-size:17px;line-height:1.6;color:rgba(255,255,255,.92);
  margin:0 0 18px;max-width:64ch}
/* Not the site gold. #F6C560 on pine measures 4.35:1 at this size, which is
   under the 4.5 floor every other pass on this site enforces - close enough
   to look fine and still fail an audit. #FFD37A is the lighter gold the hero
   kicker directly above already uses on the same background, so this borrows
   a colour that is in the palette rather than inventing one. On the ink
   panels further down, plain %(gold)s clears the floor comfortably and is
   left alone. */
.ap-hero .hl b{color:#FFD37A}
.ap-figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:0;border:2px solid %(ink)s;border-radius:12px;overflow:hidden;margin:0 0 18px;
  background:%(ink)s}
.ap-figs>div{background:%(cream)s;padding:14px 15px}
.ap-figs .n{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:29px;
  line-height:1;color:%(ink)s;display:block;letter-spacing:-.02em}
.ap-figs .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;display:block;
  margin:8px 0 0;line-height:1.5}
.ap-hero .hj{display:flex;flex-wrap:wrap;gap:9px;margin:0}
.ap-hero .hj a{display:inline-block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;
  border:2px solid %(ink)s;border-radius:999px;padding:8px 14px;background:%(gold)s;
  color:%(ink)s;box-shadow:3px 3px 0 %(ink)s}
.ap-hero .hj a:hover{transform:translate(1px,1px);box-shadow:2px 2px 0 %(ink)s}

/* ------------------------------------------------------------ the question */
.ap-q{border:2px solid %(ink)s;border-left-width:9px;border-radius:12px;
  background:%(cream)s;padding:19px 21px;margin:0 0 26px;box-shadow:4px 4px 0 %(gold)s}
.ap-q .ql{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.13em;text-transform:uppercase;color:%(pine)s;margin:0 0 10px}
.ap-q p{font-size:15.6px;line-height:1.7;color:#3A3529;margin:0 0 11px;max-width:68ch}
.ap-q p:last-child{margin:0}
.ap-q p b{color:%(ink)s}

/* ---------------------------------------------------------------- verdicts */
.ap-v{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  box-shadow:5px 5px 0 %(ink)s;overflow:hidden;margin:0 0 24px}
.ap-v>div{padding:16px 19px;border-bottom:1.5px solid #E6E0D2}
.ap-v>div:last-child{border-bottom:0}
.ap-v .vn{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:26px;
  line-height:1;color:%(pine)s;display:block;margin:0 0 7px;letter-spacing:-.02em}
.ap-v .vt{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.024em;font-size:17.5px;line-height:1.25;color:%(ink)s;
  display:block;margin:0 0 7px}
.ap-v p{font-size:15px;line-height:1.66;color:%(muted)s;margin:0;max-width:70ch}
.ap-v p b{color:%(ink)s}

/* ------------------------------------------------------------- the tables */
.ap-tw{overflow-x:auto;border:2px solid %(ink)s;border-radius:12px;
  box-shadow:5px 5px 0 %(ink)s;background:#fff;margin:0 0 14px}
.ap-t{border-collapse:collapse;width:100%%;min-width:560px}
.ap-t th,.ap-t td{text-align:left;padding:11px 14px;border-bottom:1.5px solid #E6E0D2;
  font-size:14px;line-height:1.55;color:#3A3529;vertical-align:top;
  overflow-wrap:break-word}
.ap-t th{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;background:%(cream)s;
  white-space:nowrap}
.ap-t tr:last-child td{border-bottom:0}
.ap-t td.f{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:17px;
  color:%(ink)s;white-space:nowrap}
.ap-t td.m{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12.5px;
  color:%(ink)s;white-space:nowrap}
.ap-t tr.under td{background:#FCF1EF}
.ap-t tr.under td.f{color:%(red)s}
.ap-t tr.floorrow td{background:%(paper)s}
.ap-cap{font-size:13.2px;line-height:1.65;color:%(muted)s;margin:0 0 26px;max-width:74ch}
.ap-cap b{color:%(ink)s}
.ap-cap a{color:%(pine)s}

/* ------------------------------------------------------------ the callout */
.ap-call{border:2px solid %(ink)s;border-radius:14px;background:%(ink)s;color:#fff;
  padding:22px 25px;margin:0 0 26px}
.ap-call h3{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:%(gold)s;margin:0 0 10px;
  font-weight:400}
.ap-call p{font-size:16.2px;line-height:1.62;color:#fff;margin:0 0 12px;max-width:66ch}
.ap-call p:last-child{margin:0}
.ap-call p b{color:%(gold)s}
.ap-call .big{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:34px;
  color:%(gold)s;display:block;line-height:1.1;margin:2px 0 4px}

/* ------------------------------------------------------------ the checklist */
.ap-ask{border:2px solid %(ink)s;border-radius:12px;background:%(paper)s;
  box-shadow:5px 5px 0 %(pine)s;padding:20px 22px;margin:0 0 20px}
.ap-ask h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.026em;font-size:19px;color:%(ink)s;margin:0 0 10px}
.ap-ask ul{margin:0;padding:0 0 0 19px}
.ap-ask li{font-size:15.2px;line-height:1.68;color:%(muted)s;margin:0 0 10px;
  max-width:68ch}
.ap-ask li:last-child{margin:0}
.ap-ask li b{color:%(ink)s}

/* --------------------------------------------------------- the calculator */
.ap-calc{border:2px solid %(ink)s;border-radius:14px;background:%(cream)s;
  box-shadow:6px 6px 0 %(gold)s;padding:22px 24px;margin:0 0 20px}
.ap-cg{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:0 0 20px}
.ap-cc h3{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.026em;font-size:18px;color:%(ink)s;margin:0 0 12px}
.ap-fl{display:block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;
  margin:0 0 5px}
.ap-calc input{width:100%%;box-sizing:border-box;font-family:'IBM Plex Mono',
  ui-monospace,monospace;font-size:15px;color:%(ink)s;background:#fff;
  border:2px solid %(ink)s;border-radius:8px;padding:9px 11px;margin:0 0 13px}
.ap-calc input:focus{outline:3px solid %(gold)s;outline-offset:1px}
.ap-out{border:2px solid %(ink)s;border-radius:12px;background:#fff;overflow:hidden}
.ap-out .r{display:grid;grid-template-columns:1fr auto auto;gap:12px;
  padding:12px 16px;border-bottom:1.5px solid #E6E0D2;align-items:baseline}
.ap-out .r:last-child{border-bottom:0}
.ap-out .r.hd{background:%(cream)s}
.ap-out .r.hd span{font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:%(pine)s}
.ap-out .lbl{font-size:14.4px;line-height:1.5;color:#3A3529}
.ap-out .va,.ap-out .vb{font-family:Fraunces,Georgia,serif;font-weight:600;
  font-size:18px;color:%(ink)s;text-align:right;min-width:104px}
.ap-note{font-size:13.2px;line-height:1.65;color:%(muted)s;margin:14px 0 0;
  max-width:72ch}
.ap-note b{color:%(ink)s}

/* ------------------------------------------------------------- the sources */
.ap-src{border:2px solid %(ink)s;border-radius:12px;background:#fff;padding:20px 22px;
  margin:0 0 18px;box-shadow:5px 5px 0 %(ink)s}
.ap-src h3{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.13em;text-transform:uppercase;color:%(pine)s;margin:0 0 11px;
  font-weight:400}
.ap-src ol{margin:0;padding:0 0 0 20px}
.ap-src li{font-size:14.2px;line-height:1.62;color:%(muted)s;margin:0 0 8px}
.ap-src li:last-child{margin:0}
.ap-src a{color:%(pine)s}

.ap-fine{font-size:13.4px;line-height:1.68;color:%(muted)s;margin:26px 0 0;
  max-width:74ch}
.ap-fine b{color:%(ink)s}
.ap-fine a{color:%(pine)s}

@media (max-width:900px){
  .ap-figs{grid-template-columns:1fr 1fr}
  .ap-hero h1{font-size:32px}
  .ap-cg{grid-template-columns:1fr;gap:8px}
}
@media (max-width:640px){
  .ap-hero{padding:22px 20px 20px}
  .ap-hero h1{font-size:27px;max-width:none}
  .ap-h{font-size:23px}
  .ap-calc{padding:18px 17px}
  .ap-t th,.ap-t td{padding:10px 11px;font-size:13.4px;overflow-wrap:break-word}
  .ap-out .r{grid-template-columns:1fr;gap:3px}
  .ap-out .va,.ap-out .vb{text-align:left;min-width:0}
  .ap-out .r.hd{display:none}
  .ap-out .va::before{content:'Salaried: ';font-family:'IBM Plex Mono',
    ui-monospace,monospace;font-size:10.5px;letter-spacing:.1em;
    text-transform:uppercase;color:%(pine)s}
  .ap-out .vb::before{content:'Per session: ';font-family:'IBM Plex Mono',
    ui-monospace,monospace;font-size:10.5px;letter-spacing:.1em;
    text-transform:uppercase;color:%(pine)s}
}
</style>"""


# ------------------------------------------------------------ the calculator
# No URL state, no analytics, nothing typed leaves the page. The site's printed
# promise is that nothing a reader types is sent anywhere, and a calculator
# that reported its inputs would be the one place that broke it.
CALC_JS = """<script>
(function(){
  var root = document.getElementById('ap-calc');
  if(!root) return;
  var f = function(id){ var e = document.getElementById(id);
    return e ? (parseFloat(e.value) || 0) : 0; };
  var money = function(n){ return '$' + Math.round(n).toLocaleString('en-US'); };
  function calc(){
    var sal = f('ap-sal'), salH = f('ap-salh'), salC = f('ap-salc');
    var rate = f('ap-rate'), sess = f('ap-sess'),
        adm = f('ap-adm'), admH = f('ap-admh');
    var floor = f('ap-floor'), lic = f('ap-lic'), clin = 1750;

    // Salaried: the week is the week, whatever the caseload does.
    var salWk = sal / 52, salHr = salH > 0 ? salWk / salH : 0;
    // Per session: sessions at piece rate, everything else hourly.
    var ppWk = (rate * sess) + (adm * admH);
    var ppH = sess + admH, ppHr = ppH > 0 ? ppWk / ppH : 0;
    var ppYr = ppWk * 52;

    // Weeks to the direct-clinical minimum, floored at the statutory 104.
    var wA = salC > 0 ? Math.max(104, Math.ceil(clin / salC)) : 0;
    var wB = sess > 0 ? Math.max(104, Math.ceil(clin / sess)) : 0;

    var set = function(id, v){ var e = document.getElementById(id);
      if(e) e.textContent = v; };
    set('o-yr-a', money(sal));            set('o-yr-b', money(ppYr));
    set('o-wk-a', money(salWk));          set('o-wk-b', money(ppWk));
    set('o-hr-a', salHr ? '$' + salHr.toFixed(2) : '\\u2014');
    set('o-hr-b', ppHr ? '$' + ppHr.toFixed(2) : '\\u2014');
    set('o-wks-a', wA ? wA + ' weeks' : '\\u2014');
    set('o-wks-b', wB ? wB + ' weeks' : '\\u2014');
    set('o-yrs-a', wA ? (wA/52).toFixed(1) + ' years' : '\\u2014');
    set('o-yrs-b', wB ? (wB/52).toFixed(1) + ' years' : '\\u2014');

    // Who gets there first, and by how much.
    // A tie is the common case, not an edge case: any caseload at or above
    // 17 direct clinical hours a week lands on the 104-week floor, so two
    // busy offers licence you on the same day. Saying "0 weeks sooner"
    // twice reads as a bug; saying "the same date" is the finding.
    var gap = Math.abs(wA - wB);
    var lbl = function(mine, other){
      if(!wA || !wB) return '\\u2014';
      if(mine === other) return 'the same date';
      return mine < other ? gap + ' weeks sooner' : '\\u2014';
    };
    set('o-gap-a', lbl(wA, wB));
    set('o-gap-b', lbl(wB, wA));

    // THE ROW THAT MATTERS, AND THE ONE THIS CALCULATOR GOT WRONG FIRST TIME.
    //
    // It originally showed each offer's earnings over ITS OWN road to
    // licensure - which compares a 117-week total against a 104-week total
    // and hands the win to whichever job takes longer. That is not a
    // comparison, it is a units error dressed as a finding.
    //
    // Both offers are now carried to the SAME date: the later of the two
    // licensure weeks. Whoever licenses first spends the remaining weeks
    // earning licensed pay, which is the entire argument for a heavier
    // caseload and the thing an offer letter never shows you.
    var horizon = Math.max(wA, wB), licWk = lic / 52;
    set('o-hz', horizon ? 'week ' + horizon : '\\u2014');
    set('o-tot-a', wA ? money(salWk * wA + licWk * (horizon - wA)) : '\\u2014');
    set('o-tot-b', wB ? money(ppWk * wB + licWk * (horizon - wB)) : '\\u2014');

    // The floor check. Non-session hours are the ones at risk, because the
    // session rate may not be averaged across them.
    var warn = document.getElementById('ap-warn'), msgs = [];
    if(floor > 0 && adm > 0 && adm < floor){
      msgs.push('The non-session rate of $' + adm.toFixed(2) +
        ' is below the $' + floor.toFixed(2) + ' floor you entered. ' +
        'Under Labor Code \\u00a7226.2 the session rate may not be averaged ' +
        'across those hours to make up the difference.');
    }
    if(sal > 0 && sal < 70304){
      msgs.push('A salary of ' + money(sal) + ' is under California\\u2019s ' +
        '2026 exempt-salary floor of $70,304, so the post cannot lawfully be ' +
        'salaried-exempt. Ask whether it is non-exempt \\u2014 in which case ' +
        'every hour past 40 in a week is overtime.');
    }
    if(warn){
      warn.innerHTML = msgs.length
        ? msgs.map(function(m){ return '<p>' + m + '</p>'; }).join('')
        : '';
      warn.style.display = msgs.length ? 'block' : 'none';
    }
  }
  root.addEventListener('input', calc);
  calc();
})();
</script>"""


def esc(x):
    return x


def money(n):
    return "$%s" % format(int(round(n)), ",d")


def _nums(rng):
    """The two dollar figures out of a "$66,560 &ndash; $81,860" cell."""
    got = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", rng)]
    if len(got) != 2:
        sys.exit("build_assocpay: %r is not a two-figure range. Every band in "
                 "the pay tables is read for the summary sentences under them, "
                 "so a cell that cannot be parsed is a sentence that would "
                 "have been wrong." % rng)
    return got


def band_floor(rng):
    return _nums(rng)[0]


def band_ceiling(rng):
    return _nums(rng)[1]


# ------------------------------------------------------------------ the body
def body():
    o = ['<article class="ap-wrap">']

    # ---------------------------------------------------------------- hero
    o.append('<section class="ap-hero">')
    o.append('<p class="hk">Associate pay &middot; Los Angeles and the Bay '
             'Area &middot; checked %s</p>' % CHECKED)
    o.append("<h1>A nonprofit salary or a per-session private practice?</h1>")
    o.append('<p class="hl">Published pay scales from named California '
             'employers, the wage floors an offer has to clear, and <b>the '
             'four numbers that decide it</b> &mdash; none of which is the '
             'salary.</p>')
    o.append('<div class="ap-figs">')
    for n, l in (("$70,304", "the 2026 salaried-exempt floor"),
                 ("$18.42", "LA city minimum wage, 1 July 2026"),
                 ("17 hrs", "the caseload past which the calendar decides"),
                 ("$180,000", "loan repayment associates can claim")):
        o.append('<div><span class="n">%s</span><span class="l">%s</span></div>'
                 % (n, l))
    o.append("</div>")
    o.append('<p class="hj">')
    o.append('<a href="#legal">Is the offer legal?</a>')
    o.append('<a href="#paid">What they pay</a>')
    o.append('<a href="#hours">The hours</a>')
    o.append('<a href="#compare">Compare two offers</a>')
    o.append('<a href="#loans">Loan repayment</a>')
    o.append("</p>")
    o.append("</section>")

    # ------------------------------------------------------------ the question
    o.append('<section class="ap-sec">')
    o.append('<div class="ap-q">')
    o.append('<p class="ql">The question, as associates keep asking it</p>')
    o.append('<p>The private practice offers 20 to 25 clients a week at a '
             'higher per-session rate, pays admin hours at $18&ndash;20, and '
             '<b>doesn&rsquo;t add up to a 40-hour week</b>. The nonprofit '
             'offers $70,000&ndash;$75,000 for a 40-hour week regardless of '
             'caseload, with 10 to 25 clients a week. Why would anyone take '
             'the private practice offer?</p>')
    o.append("</div>")

    o.append('<p class="ap-k">The reframe</p>')
    o.append('<h2 class="ap-h">It is not one question. It is four, and only '
             'one of them is about salary.</h2>')
    o.append('<p class="ap-d">Compared year by year the two offers are close '
             'enough that the choice looks like temperament &mdash; security '
             'against upside. Compared across the road to licensure they are '
             'not close at all, and the thing that separates them is not the '
             'money. Here is what actually decides it.</p>')

    o.append('<div class="ap-v">')
    for n, t, p in (
        ("1", "Is the offer lawful on its face?",
         "Two of the numbers in that post are already under a California "
         "floor. <b>$70,000 is $304 below the 2026 salaried-exempt "
         "threshold</b>, and <b>$18 an hour is below the City of Los "
         "Angeles minimum wage</b> from 1 July 2026. Neither is a "
         "dealbreaker; both are questions you are entitled to ask before "
         "you sign."),
        ("2", "How many direct clinical hours, really?",
         "Not clients seen &mdash; hours the Board will credit as direct "
         "clinical counseling. <b>Above about 17 a week, the statutory "
         "104-week minimum takes over and working harder does not license "
         "you sooner.</b> Below it, every hour is a week. &ldquo;10 to 25 "
         "clients&rdquo; is the widest possible answer to the most "
         "important question."),
        ("3", "What does the non-session time pay?",
         "An associate cannot be a 1099 contractor in California, so both "
         "offers are W-2 and the self-employment-tax argument does not "
         "apply. What differs is whether notes, no-shows, meetings and "
         "<b>the supervision the Board requires</b> are paid at all. "
         "Per-session pay is piece rate; the law says those hours are "
         "paid separately."),
        ("4", "Which one is a qualifying employer?",
         "A 501(c)(3) or county employer opens <b>PSLF, HCAI&rsquo;s "
         "LMHSPEP, and BH-CONNECT loan repayment of up to $180,000 that "
         "names associates by registration type</b>. A private practice "
         "opens none of them. For an associate carrying graduate debt "
         "this is worth more than the whole salary difference, several "
         "times over."),
    ):
        o.append('<div><span class="vn">%s</span><span class="vt">%s</span>'
                 "<p>%s</p></div>" % (n, t, p))
    o.append("</div>")
    o.append("</section>")

    # -------------------------------------------------------------- is it legal
    o.append('<section class="ap-sec" id="legal">')
    o.append('<p class="ap-k">Check one</p>')
    o.append('<h2 class="ap-h">Three floors an offer has to clear.</h2>')
    o.append('<p class="ap-d">None of these is advice about which job to take. '
             'They are the checks that turn &ldquo;does this feel fair?&rdquo; '
             'into a question with an answer.</p>')

    o.append('<h3 class="ap-h3">The salaried-exempt floor: $70,304</h3>')
    o.append('<p class="ap-d">California requires an exempt salaried employee '
             'to be paid at least <b>two times the state minimum wage for '
             'full-time work</b>. In 2026 that is $16.90 &times; 2 &times; '
             '2,080 hours = <b>$70,304 a year</b>, or $5,858.67 a month. It is '
             'the same figure everywhere in California, because it tracks the '
             '<i>state</i> minimum wage and not the local one.</p>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Offer</th><th>Against the $70,304 floor</th>"
             "<th>What it means</th></tr>")
    for amt, verdict, what, cls in (
        ("$70,000", "$304 under", "Cannot lawfully be salaried-exempt in 2026. "
         "Either it is a non-exempt post &mdash; in which case every hour past "
         "8 in a day or 40 in a week is overtime, and &ldquo;regardless of "
         "caseload&rdquo; cuts in your favour &mdash; or the classification is "
         "wrong.", "under"),
        ("$70,304", "exactly at it", "The minimum lawful exempt salary. Ask "
         "what happens on 1 January 2027, when the state minimum wage moves "
         "and this floor moves with it.", ""),
        ("$75,000", "$4,696 over", "Clears the salary test. Exemption still "
         "also requires the duties test &mdash; primarily professional work, "
         "customarily exercising discretion and independent judgment &mdash; "
         "which is a real question for a registrant practising under mandated "
         "supervision.", ""),
    ):
        o.append('<tr class="%s"><td class="f">%s</td><td>%s</td><td>%s</td></tr>'
                 % (cls, amt, verdict, what))
    o.append("</table></div>")
    o.append('<p class="ap-cap">Derived from the state minimum wage under '
             '<a href="https://leginfo.legislature.ca.gov/faces/'
             'codes_displaySection.xhtml?sectionNum=515.&amp;lawCode=LAB" '
             'target="_blank" rel="noopener">Labor Code &sect;515</a> and the '
             '<a href="https://www.dir.ca.gov/dlse/faq_minimumwage.htm" '
             'target="_blank" rel="noopener">DIR minimum wage FAQ</a>. '
             '<b>The arithmetic is ours; the $16.90 is published.</b></p>')

    o.append('<h3 class="ap-h3">The hourly floor where you actually work</h3>')
    o.append('<p class="ap-d">Admin, charting and supervision hours paid at '
             '$18&ndash;$20 sound like a courtesy. In most of the places an '
             'associate works, they are the legal minimum &mdash; and '
             'sometimes below it. These are the general minimum wages in '
             'effect from <b>1 July 2026</b>.</p>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Where</th><th>Per hour</th><th>Note</th>"
             "<th>$18/hr clears it?</th></tr>")
    for name, rate, note, url in WAGE_FLOORS:
        ok = float(rate) <= 18.00
        cls = "" if ok else "under"
        cell = ('<a href="%s" target="_blank" rel="noopener">%s</a>'
                % (url, name)) if url else "<b>%s</b>" % name
        o.append('<tr class="%s"><td>%s</td><td class="f">$%s</td>'
                 '<td>%s</td><td class="m">%s</td></tr>'
                 % (cls, cell, rate, note, "yes" if ok else "NO"))
    o.append("</table></div>")
    o.append('<p class="ap-cap">Coverage generally turns on where the work is '
             'performed, not where the employer is registered &mdash; the City '
             'of Los Angeles ordinance reaches anyone working two hours a week '
             'inside city limits. A telehealth associate sitting in Berkeley '
             'for a Los Angeles practice is a real question, not a trick one. '
             '<b>Where a city name above is a link, that page was opened and '
             'checked. Where it is not, the figure comes from the '
             '<a href="https://hrwatchdog.calchamber.com/2026/06/'
             'california-local-minimum-wage-increases-for-july-1-2026/" '
             'target="_blank" rel="noopener">CalChamber summary of the '
             '1 July 2026 increases</a></b> &mdash; several city sites block '
             'an automated check, and a link that has not been opened is not '
             'a citation. Rates move again on 1 January and 1 July; check the '
             'date before you rely on one.</p>')

    o.append('<h3 class="ap-h3">Per-session pay is piece rate, and piece rate '
             'has rules</h3>')
    o.append('<p class="ap-d">First, the rule that surprises people: '
             '<b>a California associate may not be an independent '
             'contractor.</b> Not a preference &mdash; the Business and '
             'Professions Code says it outright for all three registrations, '
             'and requires you to hand the Board a W-2 for every year of '
             'experience you claim. So the usual 1099-versus-W-2 arithmetic, '
             'where the contractor eats both halves of FICA, is not part of '
             'this comparison at all.</p>')
    o.append('<p class="ap-d">The same sections bar an associate from taking '
             'payment directly from clients, from holding any proprietary '
             'interest in the employer&rsquo;s business, and from renting '
             'space or paying for furnishings, equipment or supplies. If an '
             'offer asks you to cover any of that, it is not a hard bargain; '
             'it is outside the statute.</p>')
    o.append('<p class="ap-d">Second: a flat sum per completed session is '
             '<b>piece-rate compensation</b>. Under Labor Code &sect;226.2 '
             'the employer must pay separately, at no less than the applicable '
             'minimum wage, for <b>all other non-productive time</b> &mdash; '
             'progress notes, treatment planning, no-shows and late '
             'cancellations, staff meetings, training, intake calls, and the '
             'weekly supervision the Board requires. Rest breaks are paid '
             'separately again. <b>The session rate may not be averaged across '
             'those hours to reach the minimum.</b></p>')
    o.append('<div class="ap-call">')
    o.append("<h3>The arithmetic that follows</h3>")
    o.append('<p>A practice paying $35 a session and nothing for the twenty '
             'minutes of notes after it is very likely underpaying, and '
             '<a href="https://leginfo.legislature.ca.gov/faces/'
             'codes_displaySection.xhtml?sectionNum=1194.&amp;lawCode=LAB" '
             'target="_blank" rel="noopener" style="color:%s">Labor Code '
             '&sect;1194</a> makes the unpaid balance recoverable with '
             'interest and attorney&rsquo;s fees &mdash; <b>notwithstanding '
             'any agreement to work for less</b>.</p>' % GOLD)
    o.append('<p>Which is why the good offers already look like this: '
             '<b>piece rate for sessions, a separate hourly rate for '
             'everything else.</b> An offer that pays $18&ndash;20 for admin '
             'is not being generous. It is being lawful &mdash; and in the '
             'City of Los Angeles, $18 no longer is.</p>')
    o.append("</div>")
    o.append("</section>")

    # ------------------------------------------------------------- what they pay
    o.append('<section class="ap-sec" id="paid">')
    o.append('<p class="ap-k">Check two</p>')
    o.append('<h2 class="ap-h">What these jobs actually pay, by name.</h2>')
    o.append('<p class="ap-d">California requires employers with fifteen or '
             'more staff to publish a pay scale in a job posting, so most of '
             'this is on the record rather than crowdsourced. Public agencies '
             'publish salary schedules that will still resolve in a year; the '
             'nonprofit figures are postings read in <b>%s</b> and should be '
             'treated as dated observations.</p>' % CHECKED)

    o.append('<h3 class="ap-h3">Public agencies, and the finding nobody '
             'expects</h3>')
    o.append('<p class="ap-d">County and city behavioral health pays '
             'associates more than nonprofits do, and in San Francisco it is '
             'not close. <b>SF&rsquo;s class 2930 starts at $118,820 for a '
             'post whose own specification accepts an ASW, AMFT or APCC '
             'registration</b> &mdash; roughly $38,000 above what a San '
             'Francisco nonprofit pays the same registrant. If the whole '
             'question is salary security, this is the column to read '
             'first.</p>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Employer</th><th>Class</th><th>Published scale</th>"
             "<th>Open to associates?</th></tr>")
    for emp, cls, scale, pre, srclab, url in PUBLIC:
        o.append('<tr><td><b>%s</b><br><span style="font-size:12.4px;'
                 'color:%s">%s</span></td><td>%s</td><td class="f">%s</td>'
                 "<td>%s</td></tr>"
                 % (emp, MUTED, srclab, cls, scale, pre))
    o.append("</table></div>")
    o.append('<p class="ap-cap">Annual equivalents where the source publishes '
             'hourly or biweekly rates; the conversion is ours, the rates are '
             'theirs. LA County is the exception to the pattern &mdash; its '
             'entry band sits <i>inside</i> the LA nonprofit range rather than '
             'above it, unless a 20% Correctional Health assignment bonus '
             'applies, which takes an entry Psychiatric Social Worker I to '
             'about $89,300. <b>For LA County and Santa Clara we could not '
             'verify from the class specification itself whether Level I is '
             'open to a registrant</b>, so treat that as likely rather than '
             'established; Alameda and San Francisco say so in writing.</p>')

    o.append('<h3 class="ap-h3">Los Angeles County nonprofits</h3>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Employer</th><th>Role</th><th>City</th>"
             "<th>Posted range</th><th>Note</th></tr>")
    for emp, role, city, rng, note, url in LA_NONPROFIT:
        o.append('<tr><td><a href="%s" target="_blank" rel="noopener">%s</a>'
                 "</td><td>%s</td><td>%s</td><td class='f'>%s</td>"
                 "<td>%s</td></tr>" % (url, emp, role, city, rng, note))
    o.append("</table></div>")
    # Counted, not asserted. The first draft of this sentence said "four of
    # the five" from memory; it is three, and a wrong count sitting under a
    # table the reader can count themselves is the fastest way to lose them.
    WORD = ("none", "one", "two", "three", "four", "five", "six", "seven")
    under = [r for r in LA_NONPROFIT if band_floor(r[3]) <= EXEMPT]
    o.append('<p class="ap-cap">The LA associate band runs roughly '
             '<b>$%s to $%s</b>. Note that %s of the %s postings start at or '
             'below the $70,304 exempt floor, so the bottom of those bands '
             'cannot lawfully be a salaried-exempt post.</p>'
             % (format(min(band_floor(r[3]) for r in LA_NONPROFIT), ",d"),
                format(max(band_ceiling(r[3]) for r in LA_NONPROFIT), ",d"),
                WORD[len(under)], WORD[len(LA_NONPROFIT)]))

    o.append('<h3 class="ap-h3">Bay Area nonprofits</h3>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Employer</th><th>Role</th><th>City</th>"
             "<th>Posted range</th><th>Note</th></tr>")
    for emp, role, city, rng, note, url in BAY_NONPROFIT:
        o.append('<tr><td><a href="%s" target="_blank" rel="noopener">%s</a>'
                 "</td><td>%s</td><td>%s</td><td class='f'>%s</td>"
                 "<td>%s</td></tr>" % (url, emp, role, city, rng, note))
    o.append("</table></div>")
    # Median of the band floors either side, computed from the rows above, so
    # the sentence moves when the tables do.
    def med(rows):
        v = sorted(band_floor(r[3]) for r in rows)
        n = len(v)
        return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0
    o.append('<p class="ap-cap">On the rows above, the median Bay Area band '
             'starts at %s against %s in LA &mdash; <b>about %s more</b> for '
             'the same work, against a cost of living that is higher by a '
             'good deal more than that. The site&rsquo;s '
             '<a href="%s">cost-of-living comparison</a> has the offsetting '
             'numbers. Seneca&rsquo;s <b>+$4,000 on licensure</b> is worth '
             'noticing: it prices the thing this whole decision is about.</p>'
             % (money(med(BAY_NONPROFIT)), money(med(LA_NONPROFIT)),
                money(med(BAY_NONPROFIT) - med(LA_NONPROFIT)), COL))

    o.append('<h3 class="ap-h3">Private practice, per session</h3>')
    o.append('<p class="ap-d">Almost nothing is published here. Consultants '
             'quote 50/50, 60/40 and 70/30 splits, but every one of those '
             'guides is written for <i>licensed</i> clinicians &mdash; '
             '<b>we found no published California split figure specific to '
             'associates</b>, so anyone quoting one is extrapolating. What is '
             'on the record are the postings themselves.</p>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Practice</th><th>Per session</th>"
             "<th>Non-session pay</th><th>Caseload asked</th><th>Note</th></tr>")
    for emp, city, rate, adm, load, note in PRIVATE:
        o.append('<tr><td><b>%s</b><br><span style="font-size:12.4px;'
                 'color:%s">%s</span></td><td class="f">%s</td><td>%s</td>'
                 "<td>%s</td><td>%s</td></tr>"
                 % (emp, MUTED, city, rate, adm, load, note))
    o.append("</table></div>")
    o.append('<p class="ap-cap">Practices are unnamed here for the same '
             'reason the discipline library de-identifies its cases: the point '
             'is the shape of the market, not any one employer. All four '
             'postings were public in 2025&ndash;26 and all four are W-2, as '
             'the statute requires. <b>The observed range is $30&ndash;$75 a '
             'session, clustering at $35&ndash;$50.</b> Against a Los Angeles '
             'associate&rsquo;s typical client fee, $50 a session on insurance '
             'is an effective split somewhere around a third.</p>')
    o.append("</section>")

    # -------------------------------------------------------------- the hours
    o.append('<section class="ap-sec" id="hours">')
    o.append('<p class="ap-k">Check three</p>')
    o.append('<h2 class="ap-h">Seventeen hours a week is where the argument '
             'ends.</h2>')
    o.append('<p class="ap-d">An AMFT or APCC needs 3,000 supervised hours, of '
             'which <b>at least 1,750 must be direct clinical counseling</b>, '
             'gained over <b>not less than 104 weeks</b>, at no more than 40 '
             'credited hours in any seven days. Two years is the floor no '
             'matter what you do.</p>')
    o.append('<p class="ap-d">1,750 divided by 104 weeks is <b>16.83 direct '
             'clinical hours a week</b>. Which produces the one piece of '
             'arithmetic that settles most of this decision:</p>')
    o.append('<div class="ap-call">')
    o.append("<h3>The crossover</h3>")
    o.append('<span class="big">17 hours a week</span>')
    o.append('<p>At or above it, the <b>calendar</b> decides your licensure '
             'date and a heavier caseload buys you nothing. Below it, your '
             '<b>caseload</b> decides it, and every client you are not seeing '
             'costs you weeks. For an ASW the same sum on 2,000 clinical hours '
             'puts the crossover at <b>20 hours a week</b>.</p>')
    o.append('<p>Which means the nonprofit&rsquo;s &ldquo;10 to 25 clients a '
             'week&rdquo; is the single most important sentence in the offer, '
             'and it is the one part of it that has not been quantified.</p>')
    o.append("</div>")

    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Direct clinical hrs/week</th><th>Weeks to 1,750</th>"
             "<th>Actual weeks</th><th>Years</th><th>What binds</th></tr>")
    for c, wk, eff, yrs, binds in hours_rows():
        cls = "floorrow" if wk <= 104 else ""
        if c <= 8:
            cls = "under"
        o.append('<tr class="%s"><td class="f">%d</td><td class="m">%d</td>'
                 '<td class="m">%d</td><td class="m">%s</td><td>%s</td></tr>'
                 % (cls, c, wk, eff, yrs, binds))
    o.append("</table></div>")
    o.append('<p class="ap-cap">AMFT and APCC figures. <b>Derived</b> from the '
             '1,750-hour direct clinical minimum and the 104-week floor in '
             '<a href="https://leginfo.legislature.ca.gov/faces/'
             'codes_displaySection.xhtml?sectionNum=4980.43.&amp;lawCode=BPC" '
             'target="_blank" rel="noopener">&sect;4980.43</a>; the statute is '
             'published, the division is ours. Assumes no weeks lost. '
             '<b>The two rows in red at the top</b> are where the six-year '
             'registration limit becomes a live risk &mdash; a registration '
             'may be renewed five times and no further, and at six clinical '
             'hours a week you would need 292 weeks with nothing at all going '
             'wrong. <b>The four shaded rows at the foot</b> are where the '
             'calendar has taken over: the caseload has stopped mattering and '
             'every one of them licenses you on the same day.</p>')

    o.append('<h3 class="ap-h3">Four things that quietly change the '
             'answer</h3>')
    o.append('<div class="ap-ask">')
    o.append("<h3>Read these before you compare two caseloads</h3>")
    o.append("<ul>")
    o.append('<li><b>Clients seen is not hours credited.</b> A no-show is not '
             'a direct clinical hour. Ask what the practice does when a client '
             'cancels &mdash; both for your pay and for your hours.</li>')
    o.append('<li><b>The 40-hour weekly cap is across all settings, not per '
             'setting.</b> That is the Board&rsquo;s reading in its own FAQs '
             'rather than the statute&rsquo;s words, but it is the reading '
             'that governs in practice. Two part-time jobs do not get you '
             'there faster.</li>')
    o.append('<li><b>Past ten direct clinical hours in a week at one setting, '
             'you owe a second unit of supervision that week.</b> A bigger '
             'caseload costs supervision time as well as clinical time, and '
             'supervision counts against the 1,250-hour non-clinical cap.</li>')
    o.append('<li><b>500 of the AMFT&rsquo;s 1,750 must be with couples, '
             'families and children.</b> A setting that never sends you a '
             'family is a setting you cannot finish in. <i>APCCs: this '
             'requirement was repealed effective 1 January 2022 and a good '
             'many websites still list it.</i></li>')
    o.append("</ul>")
    o.append("</div>")
    o.append('<p class="ap-d">The site&rsquo;s '
             '<a href="%s">3,000-hours calculator</a> projects a real '
             'licensure date against all four gates from your own weekly '
             'numbers.</p>' % HOURS)
    o.append("</section>")

    # ----------------------------------------------------------- the calculator
    o.append('<section class="ap-sec" id="compare">')
    o.append('<p class="ap-k">Put your two offers in</p>')
    o.append('<h2 class="ap-h">Side by side, including the road to '
             'licensure.</h2>')
    o.append('<p class="ap-d">The annual figures are what a job advert compares. '
             'The bottom row is what actually differs: <b>everything you earn '
             'between now and the license</b>. Nothing you type here leaves '
             'the page.</p>')
    o.append('<div class="ap-calc" id="ap-calc">')
    o.append('<div class="ap-cg">')

    o.append('<div class="ap-cc"><h3>The salaried offer</h3>')
    o.append('<label class="ap-fl" for="ap-sal">Annual salary</label>')
    o.append('<input id="ap-sal" type="number" inputmode="decimal" value="73000" '
             'min="0" step="500">')
    o.append('<label class="ap-fl" for="ap-salh">Hours a week you are '
             'expected on site</label>')
    o.append('<input id="ap-salh" type="number" inputmode="decimal" value="40" '
             'min="0" step="1">')
    o.append('<label class="ap-fl" for="ap-salc">Direct clinical hours a '
             'week</label>')
    o.append('<input id="ap-salc" type="number" inputmode="decimal" value="15" '
             'min="0" step="1">')
    o.append("</div>")

    o.append('<div class="ap-cc"><h3>The per-session offer</h3>')
    o.append('<label class="ap-fl" for="ap-rate">Pay per session</label>')
    o.append('<input id="ap-rate" type="number" inputmode="decimal" value="50" '
             'min="0" step="1">')
    o.append('<label class="ap-fl" for="ap-sess">Sessions a week you actually '
             'hold</label>')
    o.append('<input id="ap-sess" type="number" inputmode="decimal" value="22" '
             'min="0" step="1">')
    o.append('<label class="ap-fl" for="ap-adm">Non-session hourly rate</label>')
    o.append('<input id="ap-adm" type="number" inputmode="decimal" value="19" '
             'min="0" step="0.25">')
    o.append('<label class="ap-fl" for="ap-admh">Non-session hours a week they '
             'pay for</label>')
    o.append('<input id="ap-admh" type="number" inputmode="decimal" value="10" '
             'min="0" step="1">')
    o.append("</div>")
    o.append("</div>")

    o.append('<div class="ap-cg">')
    o.append('<div class="ap-cc">')
    o.append('<label class="ap-fl" for="ap-floor">Minimum wage where you '
             'work</label>')
    o.append('<input id="ap-floor" type="number" inputmode="decimal" '
             'value="18.42" min="0" step="0.01">')
    o.append("</div>")
    o.append('<div class="ap-cc">')
    o.append('<label class="ap-fl" for="ap-lic">What a year pays once you are '
             'licensed</label>')
    o.append('<input id="ap-lic" type="number" inputmode="decimal" '
             'value="95000" min="0" step="1000">')
    o.append("</div>")
    o.append("</div>")

    o.append('<div class="ap-out">')
    o.append('<div class="r hd"><span>&nbsp;</span><span>Salaried</span>'
             "<span>Per session</span></div>")
    for lbl, a, b in (("A year", "o-yr-a", "o-yr-b"),
                      ("A week", "o-wk-a", "o-wk-b"),
                      ("Per paid hour", "o-hr-a", "o-hr-b"),
                      ("Weeks to 1,750 clinical hours", "o-wks-a", "o-wks-b"),
                      ("Which is", "o-yrs-a", "o-yrs-b"),
                      ("Licensed", "o-gap-a", "o-gap-b"),
                      ('Earned by <span id="o-hz">the later date</span>, '
                       "counting licensed pay after each license date",
                       "o-tot-a", "o-tot-b")):
        o.append('<div class="r"><span class="lbl">%s</span>'
                 '<span class="va" id="%s">&mdash;</span>'
                 '<span class="vb" id="%s">&mdash;</span></div>' % (lbl, a, b))
    o.append("</div>")

    o.append('<div id="ap-warn" class="ap-cap" style="display:none;'
             'margin:15px 0 0;color:%s"></div>' % RED)

    o.append('<p class="ap-note"><b>Why the last row is the only fair '
             'comparison.</b> Two offers that license you on different dates '
             'cannot be compared over different lengths of road &mdash; the '
             'slower one wins simply by taking longer. So both are carried to '
             'the later of the two license dates, and whoever gets there first '
             'spends the remaining weeks on licensed pay. That is the entire '
             'case for the heavier caseload, and no offer letter shows it. '
             'The licensed figure is <b>yours to set</b>; for a sense of '
             'scale, San Francisco pays a licensed class 2932 clinician '
             '$124,748 and Pacific Clinics pays a Clinician II '
             '$85,050&ndash;$107,275, while Seneca simply adds $4,000 to '
             'whatever you were on.</p>')
    o.append('<p class="ap-note"><b>What this deliberately leaves out.</b> '
             'Benefits, which are not small: employer-paid health cover '
             'averaged <b>$7,885</b> a year for single coverage and '
             '<b>$20,143</b> for family in 2025, and free supervision is worth '
             '$2,000&ndash;$3,300 a year bought as group or '
             '$5,200&ndash;$10,400 bought individually. Also excluded: paid '
             'leave, retirement match, and the loan repayment below. '
             '<b>Add those to whichever offer provides them before you '
             'decide.</b> For take-home after federal, state, FICA and SDI, '
             'use the <a href="%s">job advisor</a>.</p>' % ADVISOR)
    o.append("</div>")
    o.append("</section>")

    # ------------------------------------------------------------- loan repayment
    o.append('<section class="ap-sec" id="loans">')
    o.append('<p class="ap-k">Check four</p>')
    o.append('<h2 class="ap-h">The number that is larger than the salary '
             'difference.</h2>')
    o.append('<p class="ap-d">Two offers $5,000 apart is a real difference. It '
             'is not the same order of magnitude as this. <b>California names '
             'AMFTs, ASWs and APCCs &mdash; by registration, not by license '
             '&mdash; in a loan repayment program worth up to $180,000</b>, '
             'and it is only available if your employer is a Medi-Cal '
             'safety-net site. A private practice is not one.</p>')
    o.append('<div class="ap-tw"><table class="ap-t">')
    o.append("<tr><th>Program</th><th>Worth</th><th>Open to associates?</th>"
             "<th>What it asks</th></tr>")
    for name, worth, who, asks, url in LOANS:
        o.append('<tr><td><a href="%s" target="_blank" rel="noopener"><b>%s</b>'
                 "</a></td><td class='f'>%s</td><td>%s</td><td>%s</td></tr>"
                 % (url, name, worth, who, asks))
    o.append("</table></div>")
    o.append('<p class="ap-cap">Award amounts and windows as published in '
             '%s. Cycles close and reopen &mdash; check the program page '
             'before you plan around one. <b>PSLF note:</b> a rule excluding '
             'employers said to be engaged in illegal activity was published '
             'in October 2025 to take effect 1 July 2026, and was vacated by '
             'two federal district courts on 30 June and 1 July 2026. It never '
             'took effect; PSLF is operating under the pre-existing employer '
             'rules, and an appeal is possible.</p>' % CHECKED)
    o.append('<p class="ap-d">The shape of it: <b>NHSC and the California '
             'SLRP both want a full license and are therefore closed to you '
             'today</b>, but they are two more reasons the licensure date in '
             'the section above is worth money. LMHSPEP and BH-CONNECT are '
             'open now. PSLF starts counting from your first qualifying '
             'payment at a qualifying employer, so the clock on it begins the '
             'day you take the nonprofit job and not the day you are '
             'licensed.</p>')
    o.append("</section>")

    # ---------------------------------------------------------------- what to ask
    o.append('<section class="ap-sec" id="ask">')
    o.append('<p class="ap-k">Before you sign</p>')
    o.append('<h2 class="ap-h">Nine questions, and what a good answer sounds '
             'like.</h2>')

    o.append('<div class="ap-ask">')
    o.append("<h3>Ask the private practice</h3>")
    o.append("<ul>")
    o.append('<li><b>What is paid for a no-show or a late cancellation?</b> '
             '&ldquo;Nothing&rdquo; is an answer worth having in writing '
             'before you count on 25 sessions a week.</li>')
    o.append('<li><b>Which hours are paid at the non-session rate?</b> Notes, '
             'treatment planning, staff meetings, training, intake calls and '
             'supervision should all be on that list.</li>')
    o.append('<li><b>Is supervision paid time?</b> The Board requires at least '
             'one unit a week in every setting where you gain hours. It is not '
             'optional, so it is not your own time.</li>')
    o.append('<li><b>How many sessions has a full-time associate here actually '
             'held, on average, over the last three months?</b> The number in '
             'the offer is a ceiling. This one is the floor.</li>')
    o.append('<li><b>Who pays for the EHR, the liability policy, and the '
             'phone?</b> Labor Code &sect;2802 says the employer reimburses '
             'necessary business expenses, and &sect;4980.43.3(f) separately '
             'bars an associate from paying for the employer&rsquo;s '
             'obligations.</li>')
    o.append("</ul></div>")

    o.append('<div class="ap-ask">')
    o.append("<h3>Ask the nonprofit</h3>")
    o.append("<ul>")
    o.append('<li><b>How many direct clinical hours a week does someone in '
             'this post actually bill?</b> Not the target &mdash; the '
             'realized number. This decides your licensure date more than '
             'anything else in the offer.</li>')
    o.append('<li><b>Is the post exempt or non-exempt?</b> If it is under '
             '$70,304 it cannot be exempt in 2026, which means overtime past '
             '40 hours. Get the answer in the offer letter.</li>')
    o.append('<li><b>Are you a 501(c)(3), and will you certify PSLF '
             'employment?</b> The employer&rsquo;s tax status is the whole '
             'test. Ask who signs the form.</li>')
    o.append('<li><b>Do you participate in BH-CONNECT or LMHSPEP, and is this '
             'site eligible?</b> Site eligibility, not your registration, is '
             'usually the binding constraint.</li>')
    o.append("</ul></div>")
    o.append("</section>")

    # ------------------------------------------------------------------ sources
    o.append('<section class="ap-sec" id="sources">')
    o.append('<p class="ap-k">Sources</p>')
    o.append('<h2 class="ap-h">Every figure on this page, and where it came '
             'from.</h2>')
    o.append('<p class="ap-d">Published figures are linked to the body that '
             'published them. Derived figures &mdash; the $70,304, the 16.83 '
             'hours, the weeks-to-licensure table, the annual equivalents of '
             'hourly pay scales &mdash; are marked as derived where they '
             'appear, and the arithmetic is stated so you can check it.</p>')
    n = 0
    for head, items in SOURCES:
        o.append('<div class="ap-src"><h3>%s</h3><ol start="%d">' % (head, n + 1))
        for label, url in items:
            n += 1
            o.append('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>'
                     % (url, label))
        o.append("</ol></div>")
    o.append('<p class="ap-fine"><b>This is not legal advice, and it is not '
             'employment advice.</b> It is a reading of published California '
             'law and published pay scales, assembled so that a registrant can '
             'ask better questions of an employer. Wage floors move every '
             'January and July, award cycles close, and a posted range is not '
             'an offer. Where a figure matters to a decision, open the source '
             'and check the date on it. If something here is wrong, '
             '<a href="contact.html">tell us</a> and it gets '
             'fixed.</p>')
    o.append("</section>")

    o.append("</article>")
    return "".join(o)


# ------------------------------------------------------------------- chrome
def chrome_parts():
    if not os.path.exists(CHROME_FROM):
        sys.exit("build_assocpay: the chrome donor page is missing")
    chrome = open(CHROME_FROM, encoding="utf-8").read()

    head = chrome[:chrome.index("</head>")]
    head = re.sub(r"<title>[\s\S]*?</title>", "", head)
    head = re.sub(r'<meta name="description"[^>]*>', "", head)
    head = re.sub(r'<meta property="og:[^>]*>', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', "", head)
    head = re.sub(r'<meta name="ts:[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', "", head)
    head = re.sub(r"<!-- _dev/[\s\S]*?-->", "", head)

    body_open_end = chrome.index(">", chrome.index("<body")) + 1
    header_end = chrome.index("</header>") + len("</header>")
    header = chrome[body_open_end:header_end]
    foot_start = chrome.rindex("<footer")
    footer = chrome[foot_start:chrome.index("</footer>", foot_start)
                    + len("</footer>")]
    links = re.findall(r'<link rel="stylesheet" href="css/[0-9a-f]{12}\.css">',
                       chrome)
    tail = chrome[chrome.index("</footer>", foot_start) + len("</footer>"):]
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>", tail)
    return head, header, footer, links, scripts


META = (
    "<title>Associate pay in LA and the Bay Area: salary or per session</title>\n"
    '<meta name="description" content="Published pay scales from named '
    "California employers, the 2026 wage floors an offer has to clear, and the "
    'four numbers that decide a nonprofit salary against a per-session offer." />\n'
    '<link rel="canonical" href="https://therapistsupport.org/%s">\n'
    # licensure, not money. The page is about which job to take, and it sits
    # in the same cluster as the job advisor and the hours calculator - the
    # two pages a reader will bounce to from here. Weight 5 is the site's top
    # band; anything above it is out of scale, because the sort is by -weight
    # and there is no sixth tier.
    '<meta name="ts:topic" content="licensure">\n'
    '<meta name="ts:format" content="guide">\n'
    '<meta name="ts:question" content="Nonprofit salary or private practice '
    'per session &mdash; which associate job is actually worth more?">\n'
    '<meta name="ts:outcome" content="Published pay scales for LA and the Bay '
    'Area, the wage floors an offer must clear, and the four numbers that '
    'decide it">\n'
    '<meta name="ts:number" content="$70,304 salaried-exempt floor">\n'
    '<meta name="ts:weight" content="5">\n'
    # `ts:stale` is misnamed and it matters. It does not mean "this page has
    # gone stale" - mock/library/build_library.py reads it as the flag that
    # PRINTS the "Checked Aug 2026" badge on the page's hub card. Setting it
    # false on a page built this month is the opposite of what it looks like:
    # it makes freshly-checked research the only card on the hub with no
    # checked date, next to neighbours that have one.
    '<meta name="ts:stale" content="true">\n' % PAGE
)


def main():
    print("associate pay, Los Angeles and the Bay Area")

    # ------------------------------------------------------- sanity, up front
    bad = 0
    if abs(EXEMPT - 70304.0) > 0.5:
        print("GUARD: the exempt floor computes to %.2f, not 70304. The state "
              "minimum wage constant is wrong or the year has turned." % EXEMPT)
        bad += 1
    cross = 1750 / 104.0
    if not (16.5 < cross < 17.0):
        print("GUARD: the crossover computes to %.2f, and the page says "
              "16.83" % cross)
        bad += 1
    print("  the exempt floor: $16.90 x 2 x 2080 = %s" % money(EXEMPT))
    print("  the crossover:    1750 / 104 weeks  = %.2f clinical hrs/week"
          % cross)

    parts = chrome_parts()
    head, header, footer, links, scripts = parts
    css = CSS % {"ink": INK, "pine": PINE, "gold": GOLD, "paper": PAPER,
                 "cream": CREAM, "muted": MUTED, "red": RED}
    html = ('<!DOCTYPE html>\n<html lang="en">\n' + head + META + "</head>\n"
            "<body>" + header + "<main>" + body() + "</main>" + footer
            + "\n" + "\n".join(links) + "\n" + css
            + "\n" + CALC_JS
            + "\n" + "\n".join(scripts) + "\n</body>\n</html>\n")

    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("\nwrote %s, %s bytes" % (PAGE, format(len(html), ",d")))

    # --------------------------------------------------------------- guards
    s = open(p, encoding="utf-8").read()

    # The chrome has to have arrived whole. A page assembled from someone
    # else's header without the script that binds it ships a dead masthead.
    for what, needle in (("the masthead", "sitenav"),
                         ("the footer", "<footer"),
                         ("a stylesheet link", 'href="css/'),
                         ("the calculator", 'id="ap-calc"'),
                         ("the calculator's script", "ap-warn"),
                         ("the licensed-pay input", 'id="ap-lic"'),
                         ("the common-horizon row", 'id="o-hz"')):
        if needle not in s:
            print("GUARD: %s is missing from the written page" % what)
            bad += 1
    if not scripts:
        print("GUARD: the donor page yielded no inline scripts, so the nav "
              "panel will not open")
        bad += 1

    # Every section the hero links to must exist, or the jump nav is a set of
    # dead buttons. This is the check the project keeps learning the hard way:
    # syntax passing is not the same as the element being there.
    for anchor in re.findall(r'class="hj"[\s\S]*?</p>', s)[:1]:
        for href in re.findall(r'href="#([a-z-]+)"', anchor):
            if 'id="%s"' % href not in s:
                print("GUARD: the hero links to #%s and no element has that "
                      "id" % href)
                bad += 1

    # No naked http, and no link to a page that is not on the site.
    for href in set(re.findall(r'href="(?!https?:|#|mailto:)([^"#]+)"', s)):
        if href.endswith(".html") and not os.path.exists(
                os.path.join(SITE, href)):
            print("GUARD: links to %s, which is not on the site" % href)
            bad += 1

    # British spellings are a recurring import from research notes: the words
    # are all spelled correctly, just not for this site.
    #
    # The patterns are DERIVED from the correct spellings rather than written
    # out, and that is not cleverness for its own sake. The first version of
    # this guard listed the British spellings as literals, a blanket
    # search-and-replace over this file to fix the prose rewrote the guard's
    # own patterns into the American spellings too, and the guard then fired on
    # every correct word and caught nothing. There is now no British spelling
    # literal anywhere in this file for a future sweep to find.
    # Reader-visible prose only. Scripts and stylesheets are stripped whole,
    # not just tag-stripped: the donor chrome carries a JavaScript comment with
    # a British spelling in it, and failing this build over a code comment
    # nobody reads would be the guard crying wolf on its first outing.
    text = re.sub(r"<(script|style)\b[\s\S]*?</\1>", " ", s, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text).lower()
    for right, cut, paste in (("license", "se", "ce"), ("labor", "or", "our"),
                              ("behavior", "or", "our"), ("defense", "se", "ce"),
                              ("counseling", "el", "ell"), ("organiz", "z", "s"),
                              ("realized", "z", "s"), ("recognize", "z", "s"),
                              ("center", "er", "re"), ("program", "", "me")):
        wrong = right.replace(cut, paste) if cut else right + paste
        if wrong in text:
            print("GUARD: %r appears; this site is written in American English "
                  "(%r)" % (wrong, right))
            bad += 1

    # The privacy promise. Nothing the reader types may be read by anything
    # that reports. The calculator reads .value; no analytics may.
    for m in re.finditer(r"<script[^>]*>([\s\S]*?)</script>", s):
        code = m.group(1)
        if "ap-calc" in code:
            for leak in ("gtag(", "dataLayer", "clarity(", "fetch(",
                         "XMLHttpRequest", "sendBeacon"):
                if leak in code:
                    print("GUARD: the calculator's script contains %r. Nothing "
                          "a reader types on this site is sent anywhere."
                          % leak)
                    bad += 1

    # The legal correction that this whole page rests on.
    if "may not be an independent" not in s and "not be an independent" not in s:
        print("GUARD: the page no longer states that an associate cannot be "
              "an independent contractor, which is the finding the pay "
              "section depends on")
        bad += 1

    # Both figures in the hero must appear again in the body with their
    # working shown, or the hero is asserting numbers the page never
    # justifies.
    for fig in ("$70,304", "16.83", "$18.42", "$180,000"):
        if s.count(fig) < 2:
            print("GUARD: %s appears in the hero but is never worked through "
                  "in the body" % fig)
            bad += 1

    print("  %d source link(s) in %d group(s)"
          % (sum(len(i) for _h, i in SOURCES), len(SOURCES)))
    print("  %d employer pay scale(s): %d public, %d LA nonprofit, "
          "%d Bay nonprofit, %d private practice"
          % (len(PUBLIC) + len(LA_NONPROFIT) + len(BAY_NONPROFIT) + len(PRIVATE),
             len(PUBLIC), len(LA_NONPROFIT), len(BAY_NONPROFIT), len(PRIVATE)))

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - chrome whole, every jump target present, every "
          "internal link real, and nothing typed leaves the page")


if __name__ == "__main__":
    main()
