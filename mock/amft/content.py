#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every researched fact the Associate MFT Job Advisor states, in one place.

Kept separate from the markup so a number can be corrected without going
anywhere near the layout, and so the citation that backs a number sits
physically next to it. Nothing on the page may state a rule that is not
represented here with a source.

Sources checked 2 August 2026:
  BBS Handbook for Future LMFTs   bbs.ca.gov/pdf/publications/lmft_handbook.pdf
  BBS MFT FAQ                     bbs.ca.gov/pdf/publications/mft_faq.pdf
  BBS fee schedule                bbs.ca.gov/pdf/bbs_fee_increase_2021.pdf
  B&P 4980.43.3                   employment status of associates
  Sentio, pre-licensure earnings  2025 setting-by-setting figures
"""

# --- the four gates -------------------------------------------------------
GATES = [
    dict(key="total",  need=3000, label="Total supervised hours",
         note="Everything that counts, clinical and non-clinical together."),
    dict(key="direct", need=1750, label="Direct clinical counseling",
         note="Face to face with clients. Notes, meetings and supervision are not this."),
    dict(key="rel",    need=500,  label="Couples, families and children",
         note="A subset of the 1,750, not on top of it. The one most associates finish last."),
    dict(key="weeks",  need=104,  label="Weeks of supervised experience",
         note="A calendar floor. You cannot finish in under two years however many hours you log."),
]

CAP_NONCLIN = 1250      # Category B ceiling
CAP_WEEK = 40           # hours credited in any one week
CAP_SUP_WEEK = 6        # supervision hours credited in any one week
SUP_RATIO_TRIGGER = 10  # >10 face-to-face hours in a week => 2 units of supervision
WEEKS_INDIV_SUP = 52    # of the 104 weeks, this many must include individual/triadic
LOOKBACK_YEARS = 6

# --- fees, effective 1 January 2021 --------------------------------------
# BBS temporary fee reduction, effective 1 July 2026 through 30 June 2030.
# Verified line by line against bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf
# on 5 August 2026. Every one of these halved. A separate $20 Mental Health
# Practitioner Education Fund fee is NOT reduced and is stated in the note
# rather than folded into the total, because the FAQ does not enumerate which
# renewal-related applications it attaches to.
# NOTE: bbs.ca.gov/licensees/manage.html still shows the pre-reduction table.
# The FAQ is the more specific and more recent document; cite the FAQ.
FEES = [("Associate registration", 75), ("Associate renewal, each year", 75),
        ("California Law and Ethics exam", 75), ("Application for licensure", 125),
        ("Clinical exam", 125), ("Licence renewal, every two years", 100)]

# --- what associates are actually paid, by setting (2025) ----------------
PAY = [("Community mental health", 58000, 62000, "supervision and benefits usually included"),
       ("Federally Qualified Health Center", 62000, 62000, "supervision included"),
       ("School based", 58000, 58000, "school calendar, so fewer paid weeks"),
       ("Group private practice", 40600, 46000, "gross before supervision; net after is the lower figure"),
       ("Telehealth platform", 36000, 36000, "often fee-for-service, so no-shows are your problem")]

# --- the rules that decide whether an offer is even legal ----------------
RULES = [
    ("You are an employee or a volunteer. Never a contractor.",
     "An associate cannot be paid on a 1099 for clinical work. The narrow exceptions are "
     "reimbursement of expenses and recruitment stipends, not your caseload. If an offer "
     "says independent contractor, the offer is the problem, not your understanding of it.",
     "B&P 4980.43.3"),
    ("No private practice until your registration is in your hand.",
     "You may work in a private practice or professional corporation only after the "
     "registration is issued, and only during your first six years of registration. A "
     "subsequent registration cannot be used in that setting at all.",
     "BBS MFT FAQ"),
    ("Apply within 90 days of your degree date.",
     "If the Board receives your associate application within 90 days of your degree being "
     "awarded, and it is then issued, every post-degree hour counts. Miss that window and "
     "the hours before the registration issues are gone.",
     "BBS MFT FAQ"),
    ("Live scan first, or the hours do not count.",
     "Graduates from 2020 onwards must show live scan fingerprinting completed by the "
     "employer before pre-registration hours are credited. There is no exception to this one.",
     "BBS MFT FAQ"),
    ("The supervision agreement is signed within 60 days.",
     "Your supervisor is required by law to complete and sign it within 60 days of "
     "supervision starting. If nobody has mentioned it by week eight, ask.",
     "BBS Handbook"),
    ("Six years, five renewals, then a new number.",
     "A registration expires annually and can be renewed five times. After six years you "
     "need a subsequent registration, which cannot be used in private practice. The law "
     "and ethics exam has to be taken during each renewal cycle.",
     "BBS MFT FAQ"),
]

# --- what associates report going wrong ----------------------------------
FLAGS = [
    ("Notes on your own time",
     "Documentation is work. If your paid hours cover only the sessions, you are being paid "
     "for perhaps two thirds of the job. Put the real number in the unpaid box above and "
     "watch the hourly figure move."),
    ("Pay that waits on the insurer",
     "Some group practices pay you when the claim is reimbursed, which can be sixty days "
     "or never. You are an employee; your wages are not contingent on their collections."),
    ("Supervision billed back to you",
     "Common in group practice and legal. It is also a real four to six thousand dollars a "
     "year, so it belongs in the comparison rather than in the footnotes."),
    ("Productivity targets set above the hours",
     "A target of 28 billable hours inside a 40 hour week leaves 12 for notes, meetings, "
     "no-shows and everything else. Check the arithmetic before you agree to the number."),
    ("Your hours used as leverage",
     "The single thing that makes this job market different: your licence depends on a "
     "signature from the person paying you. Get the hours signed off as you go, not at "
     "the end, and keep your own weekly log."),
    ("A caseload that is all adult individuals",
     "Perfectly pleasant, and it will strand you 500 hours short. Ask what proportion of "
     "the caseload is couples, families and minors before you accept, not after."),
]

CITES = [
    (1, "BBS, Handbook for Future Licensed Marriage and Family Therapists",
     "https://www.bbs.ca.gov/pdf/publications/lmft_handbook.pdf",
     "3,000 hours over at least 104 weeks; 1,750 minimum direct clinical counselling; 500 "
     "minimum with couples, families and children; 1,250 maximum non-clinical; 40 hours "
     "credited in any week; 6 hours of supervision credited in any week; 52 weeks must "
     "include individual or triadic supervision; two units required in any week with more "
     "than 10 hours of face-to-face psychotherapy."),
    (2, "BBS, Marriage and Family Therapist frequently asked questions",
     "https://www.bbs.ca.gov/pdf/publications/mft_faq.pdf",
     "The 90-day application window, the live scan requirement for 2020-and-later "
     "graduates, annual renewal with five renewals available, the law and ethics exam each "
     "renewal cycle, and the private-practice restriction on subsequent registrations."),
    # leginfo rather than a mirror: it is the state's own text, and the
    # sectionNum/lawCode pattern was checked against the live page, which
    # returns the "employee or a volunteer" language quoted here.
    (3, "California Business and Professions Code section 4980.43.3",
     "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
     "?sectionNum=4980.43.3.&amp;lawCode=BPC",
     "Associates and trainees work as W-2 employees or volunteers; narrow exceptions for "
     "expense reimbursement and recruitment stipends."),
    (4, "BBS temporary fee reduction, effective 1 July 2026",
     "https://www.bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf",
     "Registration $75, annual renewal $75, law and ethics exam $75, application for "
     "licensure $125, clinical exam $125, licence renewal $100. Halved from 1 July 2026 "
     "until 30 June 2030; a separate $20 Mental Health Practitioner Education Fund fee "
     "is not reduced."),
    (5, "IRS Revenue Procedure 2025-32",
     "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
     "2026 federal rate schedules and the $16,100 single standard deduction used here."),
    (6, "Social Security Administration, contribution and benefit base",
     "https://www.ssa.gov/oact/cola/cbb.html",
     "The 2026 Social Security wage base of $184,500. Medicare has no cap."),
    (7, "California EDD, state disability insurance rate",
     "https://edd.ca.gov/en/payroll_taxes/rates_and_withholding/",
     "SDI is withheld at 1.3% of all wages in 2026 with no wage ceiling."),
    (8, "Sentio, what therapists earn before licensure in California, 2025",
     "https://sentio.org/what-therapists-earn-before-licensure-in-california",
     "Setting-by-setting associate pay, and supervision at roughly $450 a month where you "
     "pay for it yourself."),
    (9, "BBS, important answers to frequently asked questions for supervisors",
     "https://www.bbs.ca.gov/pdf/publications/faqs_for_supervisors.pdf",
     "&#8220;One unit&#8221; is one hour of individual or triadic supervision, or two hours "
     "of group. At least one unit is required in any week experience is gained in a setting, "
     "and one additional unit in any week the associate provides more than 10 hours of "
     "direct clinical counselling in that setting."),
]
