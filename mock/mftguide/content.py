# -*- coding: utf-8 -*-
"""Every figure on the licensure page, with the section that produces it.

Sourced 6 August 2026 from the Board of Behavioral Sciences' own January 2026
compilation of B&P Division 2 Chapter 13 and 16 CCR Division 18, plus the
Board's published exam statistics, fee regulations and processing times.

A note on leginfo. The canonical URL for a Business and Professions Code
section is leginfo.legislature.ca.gov, and that is what every citation here
links to, because it is the version of record. The TEXT was read out of the
Board's own compilation PDF, since leginfo blocks automated retrieval. Those
two should agree - the compilation is the regulator reproducing the code it
enforces - but the link goes to the source of record rather than to the copy.
"""

BBS_LAWREGS = "https://www.bbs.ca.gov/pdf/publications/lawsregs.pdf"
LEGINFO = ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml"
           "?sectionNum=%s&lawCode=BPC")

# ---------------------------------------------------------------- the gates
GATES = [
    ("01", "A qualifying master's",
     "60 semester or 90 quarter units, from a program the Board will accept.",
     "&sect;4980.36(d)"),
    ("02", "Practicum, while you are still a student",
     "6 semester units, 150 face-to-face hours, plus 75 more.",
     "&sect;4980.36(d)(1)(B)"),
    ("03", "Register as an associate",
     "The Board must <em>receive</em> your application within 90 days of the degree.",
     "&sect;4980.43(b)(1)(A)"),
    ("04", "3,000 hours over at least 104 weeks",
     "With a floor on relational hours and a ceiling on everything that is not counselling.",
     "&sect;4980.43(c)"),
    ("05", "Two exams",
     "Law and Ethics in your first year of registration; Clinical once the hours are done.",
     "&sect;4980.397"),
]

# ---------------------------------------------------------------- the hours
HOURS_TOTAL = 3000
HOURS = [
    # label, value, kind, note, cite
    ("Direct clinical counselling", 1750, "min",
     "Individuals, groups, couples or families. A minimum, not a target.",
     "&sect;4980.43(c)(8)"),
    ("Everything that is not counselling", 1250, "max",
     "Supervision, testing, report writing, progress notes, client-centred "
     "advocacy, approved training. A ceiling.",
     "&sect;4980.43(c)(10)"),
]
HOURS_INSIDE = [
    ("Couples, families and children", 500,
     "Carved out of the 1,750, not added to it. The category associates most often "
     "finish short on, because agencies serving mostly individual adults do not "
     "generate it.", "&sect;4980.43(c)(8)"),
]
HOURS_SPLIT = [
    ("Before the degree", 1300, "ceiling",
     "Of which no more than 750 may be counselling and supervisor contact combined, "
     "so at most 550 is non-clinical.", "&sect;4980.43(c)(4)&ndash;(5)"),
    ("After the degree", 1700, "floor",
     "A minimum. Nothing counts at all until you have finished 12 semester units.",
     "&sect;4980.43(c)(3), (c)(6)"),
]

WEEKLY = [
    ("104", "weeks minimum", "Each one needs at least an hour of supervisor contact "
     "in every setting you claim.", "&sect;4980.43(c)(1)"),
    ("52", "of those weeks individual or triadic",
     "A placement that only offers group supervision cannot get you past half.",
     "&sect;4980.43.2(a)(4)"),
    ("40", "hours a week, maximum", "In any seven consecutive days.",
     "&sect;4980.43(c)(2)"),
    ("6", "hours of supervision credited a week",
     "Individual, triadic or group. More than six is unpaid overhead.",
     "&sect;4980.43.2(a)(2)&ndash;(3)"),
    ("8", "supervisees in a group, maximum",
     "And two hours of group counts as one hour of supervision.",
     "&sect;4980.43.2(b)(1)(C)"),
    ("6", "years before hours go stale",
     "Measured to the day the Board receives your licensure application. Up to 500 "
     "practicum hours are exempt.", "&sect;4980.43(c)(7)"),
]

# ---------------------------------------------------------------- the exams
EXAMS = [
    ("California Law and Ethics", 4608, 3715, 6009, 4499, 90,
     "Taken within the first year of registration, and re-taken every year until "
     "you pass &mdash; participation is a renewal condition.",
     "&sect;4980.397(b), &sect;4984.01(b)(3)"),
    ("LMFT Clinical", 3216, 2667, 4374, 3071, 240,
     "Only after every hour is logged, every education requirement is met, and the "
     "Law and Ethics exam is passed.", "&sect;4980.397(c)"),
]
EXAM_SRC = "https://www.bbs.ca.gov/pdf/exam_stats/exam_stats_2025.pdf"

# ---------------------------------------------------------------- the money
FEES = [
    ("Associate registration application", 150, 75, "16 CCR &sect;1816.1(f)"),
    ("Associate annual renewal", 150, 75, "16 CCR &sect;1816(a)"),
    ("Law and Ethics exam", 150, 75, "16 CCR &sect;1816.2(b)"),
    ("Clinical exam", 250, 125, "16 CCR &sect;1816.2(c)"),
    ("Application for licensure", 250, 125, "16 CCR &sect;1816.4(a)"),
    ("Initial licence issuance", 200, 100, "16 CCR &sect;1816.1(a)"),
]
FEES_OTHER = [
    ("Fingerprinting &mdash; state", "$32", "Paid to the DOJ through the Live Scan operator."),
    ("Fingerprinting &mdash; federal", "$17", "Paid to the FBI the same way."),
    ("Live Scan rolling fee", "varies",
     "Set by whichever site takes your prints. The Board publishes no figure."),
    ("Exam vendor", "$0",
     "Pearson VUE administers both exams and charges you nothing; the fee is "
     "already in what you paid the Board."),
]
FEE_NOTE = ("Halved on 1 July 2026 and due to revert on 1 July 2030. An application "
            "the Board received before 1 July 2026 paid the old fee and no refund "
            "was issued.")
FEE_SRC = "https://www.bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf"

# ---------------------------------------------------------------- timeline
PROCESSING = [
    ("Associate registration", 27, 72, "days"),
    ("Application for licensure", 69, 123, "days"),
]
PROC_SRC = "https://bbs.ca.gov/pdf/agen_notice/2026/20260219_20_item_14.pdf"

# ---------------------------------------------------------------- traps
TRAPS = [
    ("The 90-day rule is a receipt deadline",
     "The Board must <b>receive</b> the associate application within 90 days of the "
     "degree being granted &mdash; not postmark it, receive it. Miss it and every "
     "post-degree hour worked before the registration issues is gone.",
     "&sect;4980.43(b)(1)(A)"),
    ("The 90-day rule has a second condition almost nobody knows about",
     "If you finished graduate study on or after 1 January 2020, your workplace must "
     "have <b>required completed Live Scan fingerprinting before you began accruing "
     "hours</b> &mdash; and you have to produce that form years later, with the "
     "licensure application. Keep the copy.",
     "&sect;4980.43(b)(1)(B)"),
    ("You cannot be a 1099 contractor. Ever.",
     "Trainee, associate or applicant for licensure &mdash; employee or volunteer only. "
     "W-2s go in with the licensure application.",
     "&sect;4980.43.3(a)"),
    ("Private practice is closed until the number is issued",
     "Not applied for. Issued. And a trainee may never work in a private practice or "
     "professional corporation at all.",
     "&sect;4980.43(b)(2), &sect;4980.43.3(b)(1)(A)"),
    ("Supervision has to happen in the same week as the hours",
     "You cannot make up a missed week later. Each week you claim needs its own hour, "
     "in each setting.", "&sect;4980.43.2(e)"),
    ("Your supervisor's qualifications are your problem",
     "Two of the last five years licensed, supervision training done, licence active "
     "and not on probation, never your own therapist, not a relative or domestic "
     "partner. If any of it fails, <b>your hours do not count</b> &mdash; not theirs.",
     "&sect;4980.03(g), &sect;4980.43.3(d)"),
    ("The supervision agreement has a 60-day clock",
     "Signed under penalty of perjury within 60 days of starting any supervision. You "
     "keep the original and file it years later.",
     "16 CCR &sect;1833(c)(1)"),
    ("The registration itself expires at six years",
     "Renewable five times, then it is over &mdash; and a second registration number "
     "bars you from private practice on it.",
     "&sect;4984.01(d)"),
    ("The 500 relational hours are carved out, not added",
     "They sit inside the 1,750, and they are the ones people reach 3,000 without.",
     "&sect;4980.43(c)(8)"),
    ("Three separate one-year clocks can abandon your application",
     "Cure deficiencies within a year. Sit a required exam at least once every 365 "
     "days. Pay the licence fee within a year of passing. Abandonment means starting "
     "over at current requirements and full fees.",
     "16 CCR &sect;1806(a)&ndash;(c)"),
    ("No money from clients, no stake in the practice",
     "No payment from patients, no leasing space, no buying the furniture. This is the "
     "one that catches associates asked to chip in for rent.",
     "&sect;4980.43.3(e)&ndash;(f)"),
    ("Nothing counts before 12 semester units",
     "Volunteering early banks nothing at all.", "&sect;4980.43(c)(6)"),
]

# ---------------------------------------------------------------- degree
DEGREE_TITLES = [
    "Marriage and family therapy", "Couple and family therapy",
    "Marriage, family and child counseling", "Psychology", "Clinical psychology",
    "Counseling psychology",
    "Counseling or clinical mental health counseling, with an MFT emphasis",
]
CONTENT_AREAS = [
    ("12 semester units", "Psychotherapeutic theory and marital and family systems, "
     "applied across individuals, couples, families, adults including elders, "
     "children, adolescents and groups", "&sect;4980.36(d)(1)(A)"),
    ("10 hours", "Human sexuality, including gender identity and psychosexual "
     "dysfunction", "16 CCR &sect;1807"),
    ("7 contact hours", "Child abuse assessment and reporting", "B&amp;P &sect;28"),
    ("6 hours", "Suicide risk assessment and intervention &mdash; certified separately "
     "at application, not assumed from the degree", "&sect;4980.396"),
    ("3 hours", "Telehealth, including its law and ethics",
     "&sect;4980.395"),
]

SOURCES = [
    ("BBS, Statutes and Regulations Relating to the Practice of Marriage and Family "
     "Therapy, January 2026", BBS_LAWREGS,
     "The Board's own compilation of the code it enforces. Every statutory figure on "
     "this page was read here and linked to leginfo."),
    ("BBS, Handbook for Future LMFTs",
     "https://www.bbs.ca.gov/pdf/publications/lmft_handbook.pdf",
     "The Board's plain-language guide, including the 550-hour pre-degree "
     "non-clinical figure that is arithmetic rather than statute."),
    ("BBS, Exam Results by School, 1 January &ndash; 31 December 2025", EXAM_SRC,
     "Statewide totals for both exams, first-time and all takers."),
    ("BBS, Temporary Fee Reduction FAQ", FEE_SRC,
     "The 1 July 2026 reduction, the 30 June 2030 reversion, and the no-refund rule."),
    ("BBS, Notice of Approval of Regulatory Action &mdash; fee reductions",
     "https://www.bbs.ca.gov/pdf/regulation/pending/fee_reduc_noa.pdf",
     "Filed with the Secretary of State 4 February 2026."),
    ("BBS, Licensing Update, February 2026 board meeting", PROC_SRC,
     "Current processing times for clean and deficient applications."),
    ("BBS, 2025 Sunset Review Report",
     "https://www.bbs.ca.gov/pdf/publications/bbs_2025_sunset_report.pdf",
     "Five-year average processing figures and the Board's own account of its backlog."),
    ("Pearson VUE, California BBS Candidate Handbook, July 2026",
     "https://www.pearsonvue.com/content/dam/VUE/vue/en/documents/publications/580500.pdf",
     "Exam length, question counts, the 90-day retake wait, and confirmation that the "
     "vendor charges nothing at the test centre."),
    ("California Business and Professions Code, Division 2, Chapter 13",
     LEGINFO % "4980.36",
     "The version of record. Substitute any section number in the address."),
]

NOT_VERIFIED = [
    "How long a master's takes. The Board sets a unit floor and no duration at all, "
     "so this varies by programme and by whether you go full-time.",
    "Average or median time from starting a master's to holding a licence. Checked "
     "the 2025 sunset review and the Board's licensing updates &mdash; BBS does not "
     "publish it.",
    "The passing score on either exam. Results are pass/fail for those who pass; the "
     "cut score is not published.",
    "What a Live Scan site charges to roll your prints. It varies and the Board says so.",
]
