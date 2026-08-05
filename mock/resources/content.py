# -*- coding: utf-8 -*-
"""Verified external resources for California therapists in private practice.

EVERY entry here was fetched and read on 5 August 2026. Nothing is included on
the strength of a search-result snippet, and no price or figure appears unless
it was read off the page itself. Where a page would not yield a figure to an
automated fetch, the entry says so rather than repeating a number from a
third-party review site.

Format: (title, url, description). The description may contain <b> and inline
markup; it must NOT contain a bare <a> - the builder wraps the whole card.
"""

# ---------------------------------------------------------------------------
GROUPS = [
 ("The Board", "Licence, renewal, exams",
  "The BBS is where every deadline you have originates. Bookmark the lookup and "
  "the fee page; the rest you will need once or twice a year.",
  [
   ("Board of Behavioral Sciences",
    "https://www.bbs.ca.gov/",
    "The agency that issues, renews and disciplines your licence."),
   ("Licence and registration lookup",
    "https://search.dca.ca.gov/",
    "Confirm a licence number, status and expiry — yours, a supervisor's, or a "
    "referral partner's."),
   ("Renew your licence",
    "https://www.bbs.ca.gov/licensees/manage.html",
    "The renewal hub. <b>A licence cannot be renewed more than 90 days before "
    "it expires, and there is no grace period</b> — late means a delinquency fee."),
   ("Fees: the temporary reduction",
    "https://www.bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf",
    "BBS fees roughly halved on <b>1 July 2026</b> and stay reduced until "
    "<b>30 June 2030</b>. Associate registration and annual renewal are $75, "
    "the law and ethics exam $75, licensure application $125, LMFT clinical "
    "exam $125, and biennial licence renewal $100. A separate $20 Mental Health "
    "Practitioner Education Fund fee is not reduced. Note the Board's own "
    "renewal page still shows the old table."),
   ("Statutes and regulations",
    "https://www.bbs.ca.gov/pdf/publications/lawsregs.pdf",
    "Every statute and regulation governing your practice in one PDF, "
    "January 2026 edition."),
   ("What changed, and when",
    "https://www.bbs.ca.gov/about/law_reg.html",
    "Three regulations took effect in 2026 — fee reductions and disciplinary "
    "guidelines on 1 July, and <b>advertising on 1 April</b>, which affects how "
    "you may describe yourself."),
   ("California Law and Ethics exam",
    "https://www.bbs.ca.gov/exams/calaw_ethics.html",
    "Administered by Pearson VUE, and there is a separate exam for each licence "
    "type. <b>Associates must take it annually until they pass</b> in order to "
    "renew."),
   ("Book an exam (Pearson VUE)",
    "https://www.pearsonvue.com/us/en/cabbs.html",
    "Where the Law and Ethics and LMFT clinical exams are actually scheduled. "
    "The LCSW clinical exam is run by ASWB and the LPCC's by NBCC instead."),
  ]),

 ("CE and supervision", "What you must do every cycle",
  "The hour counts are exact and the Board publishes them. These are the two "
  "pages people misremember most.",
  [
   ("Continuing education requirements",
    "https://www.bbs.ca.gov/licensees/cont_ed.html",
    "<b>36 hours every two-year renewal period</b>, including <b>6 hours of law "
    "and ethics</b>. Associates need 3 hours of California law and ethics each "
    "one-year period. One-time requirements: <b>6 hours of suicide risk "
    "assessment</b> and <b>3 hours of telehealth</b>."),
   ("CE summary chart",
    "https://www.bbs.ca.gov/pdf/forms/cechart.pdf",
    "The whole picture on one page — the fastest thing to hand a colleague who "
    "is confused about renewal."),
   ("Supervisor qualifications",
    "https://www.bbs.ca.gov/pdf/supervisor_qualifications.pdf",
    "Before you promise an associate hours you can sign for: you need <b>two of "
    "the last five years licensed</b>, then <b>15 hours of supervision training "
    "within 60 days</b> of starting, and <b>6 hours of supervision CPD each "
    "renewal cycle</b> after that. (It is 15 up front and 6 per cycle, not the "
    "other way round.)"),
   ("Supervision agreement",
    "https://www.bbs.ca.gov/pdf/forms/supervision_agreement.pdf",
    "Must be signed <b>within 60 days</b> of starting with a new supervisee. "
    "Without it the supervised experience does not count."),
   ("Supervisor resources",
    "https://www.bbs.ca.gov/licensees/supervisor.html",
    "Every form and rule governing the supervisory relationship."),
  ]),

 ("Your association", "Legal cover, mostly",
  "The concrete reason a solo practitioner joins is rarely the newsletter. It "
  "is having somebody to call about a subpoena.",
  [
   ("CAMFT", "https://www.camft.org/Membership/Join-CAMFT",
    "The California MFT association. Clinical membership is <b>$227 plus a $50 "
    "application fee</b>; pre-licensed is <b>$95</b>."),
   ("CAMFT legal consultations",
    "https://www.camft.org/Membership/Legal-Team-Consultations",
    "<b>Free, unlimited</b> calls to staff attorneys about subpoenas, mandated "
    "reporting and confidentiality. This is the benefit most members actually "
    "use."),
   ("NASW", "https://www.socialworkers.org/Membership/Membership-Types",
    "For LCSWs. <b>$236 a year</b> at MSW/DSW/PhD level, and you are placed in "
    "the California chapter automatically. Includes free ethics and legal "
    "consultations."),
   ("NASW California chapter", "https://www.naswca.org/",
    "The state chapter that lobbies on scope of practice and reimbursement."),
   ("CALPCC", "https://calpcc.org/pages/benefits-of-membership",
    "For LPCCs. <b>$255 a year</b> professional, <b>$155</b> associate, "
    "<b>$80</b> student. The professional tier includes attorney consultations "
    "twice a year and 2 free CEUs."),
  ]),

 ("Getting paid", "Panels, credentialing and self-pay",
  "Credentialing is mostly one profile that every payer reads, plus waiting. "
  "Check a panel is open before you spend a week on its paperwork.",
  [
   ("CAQH Provider Data Portal",
    "https://proview.caqh.org/login?Type=EPM",
    "Nearly every commercial panel pulls your licence, work history and "
    "malpractice details from this one profile, so a stale profile stalls every "
    "application at once. <b>CAQH rebranded to DataSpring in June 2026</b> but "
    "the provider login is still here, still branded CAQH."),
   ("Get an NPI (NPPES)",
    "https://nppes.cms.hhs.gov/",
    "The free, official place to get the Type 1 individual NPI that goes on "
    "every claim and superbill. Paid lookalike sites rank well in search; this "
    "is the real one."),
   ("Medicare: what therapists need to know",
    "https://www.cms.gov/files/document/marriage-and-family-therapists-and-mental-health-counselors-faq.pdf",
    "CMS confirms LMFTs and mental health counselors can bill Medicare — "
    "<b>payment began 1 January 2024</b>. Enrol through PECOS or the paper "
    "CMS-855I; clean web applications are processed within 15 days."),
   ("Medicare enrolment (PECOS)",
    "https://pecos.cms.hhs.gov/pecos/login.do",
    "Where the CMS-855I is filed. It will reject you until you have I&amp;A "
    "credentials, which is the step most people miss."),
   ("Medi-Cal enrolment (PAVE)",
    "https://pave.dhcs.ca.gov/",
    "The only route into fee-for-service Medi-Cal. Help desk (866) 252-1949."),
   ("Medi-Cal: who can enrol",
    "https://www.dhcs.ca.gov/provgovpart/Pages/Provider-Enrollment-Options.aspx",
    "Confirms in writing that LMFT, LCSW, LPCC and psychologist are eligible "
    "applicant types, which saves guessing at the category."),
   ("Anthem Blue Cross California",
    "https://providers.anthem.com/california-provider/our-network/join",
    "The clearest California-specific statement of what a complete file needs. "
    "<b>Credentialing typically takes 45 days</b> from a completed CAQH "
    "application; recredentialing every three years."),
   ("Blue Shield of California — behavioral health",
    "https://www.blueshieldca.com/en/provider/guidelines-resources/prospective-providers/join-behavioral-health-providers",
    "Names LMFT, LCSW and LPCC explicitly. Applications must be dated no more "
    "than 30 days from submission; <b>45 to 60 days</b> to process."),
   ("Optum / United Behavioral Health",
    "https://public.providerexpress.com/content/ope-provexpr/us/en/our-network/individually-contracted-clinicians.html",
    "The solo-practitioner track at the largest behavioral health network. "
    "Applications stall most often on a CAQH profile that does not match the "
    "Optum form."),
   ("Aetna behavioral health",
    "https://www.aetna.com/health-care-professionals/join-the-aetna-network.html",
    "Behavioral health has its own request form, and <b>contracting comes "
    "before credentialing</b> — the reverse of what most people assume."),
   ("Evernorth (Cigna) behavioral health",
    "https://static.evernorth.com/assets/evernorth/provider/resourceLibrary/behavioralResources/doingBusinessWithUs/cbhCredentialing.html",
    "<b>Currently closed to new individual applicants.</b> Evernorth paused new "
    "applications on 1 June 2026 and points providers back to this page after "
    "1 September 2026. Check before you start."),
   ("Availity Essentials",
    "https://www.availity.com/essentials/",
    "Several large payers route eligibility checks and remittances only through "
    "Availity, so you end up with an account whether or not you wanted a "
    "clearinghouse."),
   ("Good Faith Estimates (self-pay clients)",
    "https://www.cms.gov/medical-bill-rights/help/guides/good-faith-estimate",
    "The federal rule that applies to essentially every private-pay client. "
    "Booked 3–9 business days ahead, the estimate is due <b>within 1 business "
    "day</b>; 10 or more days ahead, <b>within 3</b>."),
   ("Good Faith Estimate — the notice",
    "https://www.cms.gov/files/document/nsa-gfe-required-notice.pdf",
    "A ready-made compliant notice. A client can dispute a bill that exceeds "
    "the estimate by <b>$400 or more</b>."),
  ]),

 ("Telehealth", "And clients who travel",
  "One statute and one FAQ answer almost every question here, and the answer to "
  "the out-of-state one surprises people.",
  [
   ("B&amp;P Code §2290.5 — the telehealth statute",
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=2290.5.&lawCode=BPC",
    "You must inform the client and <b>obtain and document consent</b> before "
    "delivering care by telehealth. Failure to comply <b>is unprofessional "
    "conduct</b>. Associates and trainees are covered too. Amended by SB 402, "
    "effective 1 January 2026."),
   ("BBS telehealth FAQ",
    "https://www.bbs.ca.gov/pdf/publications/telehealth_faq.pdf",
    "The Board's own answer to the question that quietly creates the most "
    "liability in a remote practice: you may treat a client in another state "
    "<b>only if you meet that state's requirements to practise there</b>. "
    "Licensure follows the client's physical location, not yours."),
   ("Counseling Compact",
    "https://counselingcompact.gov/",
    "<b>California is not a member state</b>, so it grants a California "
    "licensee nothing — and the compact covers LPCs and LPCCs only, never "
    "LMFTs. Worth knowing precisely because it is widely misunderstood."),
  ]),

 ("Protecting the practice", "Insurance, HIPAA, confidentiality",
  "Malpractice cover and a risk assessment are the two things a solo practice "
  "is most likely to be missing.",
  [
   ("CPH &amp; Associates",
    "https://cphins.com/counselor/",
    "Professional liability for therapists. Includes <b>$35,000 of licensing "
    "board defence</b>, $10,000 per deposition. There is a CAMFT-specific "
    "programme for California LMFTs."),
   ("HPSO",
    "https://www.hpso.com/Insurance-for-you/Individual-Practitioners/Counselors",
    "The main alternative. Up to $1m per claim, but <b>licence defence is "
    "$25,000</b> against CPH's $35,000 — a real difference worth comparing "
    "rather than assuming carriers are interchangeable."),
   ("The Trust",
    "https://www.trustinsurance.com/mental-health-other-allied-professionals/",
    "Best known for psychologists; this page confirms LMFT, LCSW and LPCC are "
    "eligible. Up to $2m per incident."),
   ("HIPAA Privacy Rule",
    "https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html",
    "What you may do with client information and what rights clients have to "
    "their own records."),
   ("HIPAA Security Rule",
    "https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html",
    "Electronic records only — which is the entire footprint of a practice "
    "running an EHR and telehealth. A significant tightening has been proposed "
    "but <b>the current rule still stands</b>."),
   ("Security Risk Assessment tool",
    "https://healthit.gov/privacy-security/security-risk-assessment-tool/",
    "The Security Rule requires a risk assessment and this free tool is built "
    "for small providers with no IT department. <b>Nothing you enter leaves "
    "your computer.</b>"),
   ("Breach notification",
    "https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html",
    "A stolen laptop starts a clock: notify affected individuals <b>within 60 "
    "days</b>. Breaches under 500 people are reported annually, 500 or more "
    "within 60 days."),
   ("Psychotherapy notes are different",
    "https://www.hhs.gov/hipaa/for-professionals/faq/2088/does-hipaa-provide-extra-protections-mental-health-information-compared-other-health.html",
    "The most misunderstood point in the whole set: psychotherapy notes need "
    "the client's authorisation before disclosure <b>for any reason, including "
    "treatment</b> — with exceptions for mandated reporting and duty to warn."),
   ("Confidentiality of Medical Information Act",
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=56.10.&lawCode=CIV",
    "California's own confidentiality law sits on top of HIPAA and is stricter "
    "in places, so HIPAA compliance alone is not enough here. §56.10 is the "
    "section you reach for when a subpoena arrives."),
   ("Mandated reporting — who and when",
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=11166.&lawCode=PEN",
    "Phone the agency <b>immediately</b>, then send a written report "
    "<b>within 36 hours</b>. The two-step clock is the detail people get wrong "
    "under pressure."),
   ("Suspected Child Abuse Report form",
    "https://oag.ca.gov/childabuse/forms",
    "The form that 36-hour written report has to be made on. Download it before "
    "you ever need it."),
  ]),

 ("Money and structure", "Entity, tax, retirement",
  "The entity question has a wrong answer that gets repeated constantly. Start "
  "with the two code sections.",
  [
   ("You cannot use an LLC — Corp. Code §17701.04",
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17701.04.&lawCode=CORP",
    "<b>A California LLC may not render professional services.</b> For a "
    "licensed therapist the real choice is sole proprietorship or a "
    "professional corporation — never an LLC, whatever a generic small-business "
    "guide says."),
   ("Professional corporations — Corp. Code §13401.5",
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=13401.5.&lawCode=CORP",
    "Sets who may co-own one. Other licensed professionals may hold <b>no more "
    "than 49%</b> — which is where the familiar “51% therapist-owned” "
    "figure comes from; the statute states the 49% cap, not the 51%."),
   ("Naming the corporation — B&amp;P §4987.7",
    "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=4987.7.&lawCode=BPC",
    "You cannot name it whatever you like. The name must contain one of "
    "“marriage”, “family” or “child” together with "
    "“counseling”, “counselor”, “therapy” or "
    "“therapist”. This is where filings get rejected."),
   ("Secretary of State — forms and fees",
    "https://www.sos.ca.gov/business-programs/business-entities/forms",
    "Where the Articles of Incorporation for a professional corporation live."),
   ("The $800 that decides it",
    "https://www.ftb.ca.gov/file/business/types/corporations/index.html",
    "<b>Every corporation owes California $800 a year whether or not it made a "
    "profit</b> (waived in the first year). This is the single biggest reason a "
    "low-revenue practice should stay a sole proprietorship."),
   ("California and the S election",
    "https://www.ftb.ca.gov/file/business/types/corporations/s-corporations.html",
    "California does not honour the S election the way the IRS does — the "
    "entity still pays <b>1.5% on California source income</b>, which erases "
    "part of the federal saving."),
   ("Schedule C",
    "https://www.irs.gov/forms-pubs/about-schedule-c-form-1040",
    "Where a sole proprietor's whole practice income and expenses land."),
   ("Estimated taxes",
    "https://www.irs.gov/businesses/small-businesses-self-employed/estimated-taxes",
    "Nobody withholds tax from private-pay income. You generally must pay "
    "quarterly if you will owe <b>$1,000 or more</b>; the safe harbour is 90% "
    "of this year or <b>100% of last year's tax</b>, whichever is smaller."),
   ("Solo 401(k)",
    "https://www.irs.gov/retirement-plans/one-participant-401k-plans",
    "The highest-capacity plan available with no employees. Once it holds "
    "<b>$250,000 or more</b> you must file Form 5500-EZ annually — the step "
    "that surprises people."),
   ("2026 contribution limits",
    "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-401k-and-profit-sharing-plan-contribution-limits",
    "<b>$24,500</b> employee deferral, <b>$8,000</b> catch-up at 50, and an "
    "overall cap of <b>$72,000</b>. SIMPLE deferral is $17,000 with a $4,000 "
    "catch-up."),
   ("Social Security wage base",
    "https://www.ssa.gov/oact/cola/cbb.html",
    "<b>$184,500 for 2026</b>, up from $176,100. This is the cap where the "
    "12.4% Social Security half of self-employment tax stops — the biggest kink "
    "in a solo practice's tax curve."),
  ]),

 ("Getting clients", "Directories and networks",
  "Two different commitments here. A directory lists you and you keep your own "
  "billing; a managed network credentials you and sets what you are paid.",
  [
   ("Psychology Today",
    "https://join.psychologytoday.com/us/signup",
    "The largest referral source most California therapists use, at "
    "<b>$29.95 a month</b> — and the line item that recurs whether or not it "
    "produced a client."),
   ("TherapyDen",
    "https://www.therapyden.com/benefits",
    "<b>Free</b>, with no card required, so there is no financial reason not to "
    "have a second listing. An optional premium tier is $30 a month."),
   ("Inclusive Therapists",
    "https://www.inclusivetherapists.com/join",
    "Free tier available; paid tiers from <b>$22 a month</b> billed annually. "
    "Sliding-scale discounts of 15–35% for BIPOC therapists."),
   ("Open Path Collective",
    "https://openpathcollective.org/open-path-therapists/",
    "<b>Costs the therapist nothing</b>, but caps what you may charge those "
    "clients at <b>$40–70</b> a session. It trades rate for referral flow. "
    "Pre-licensed and associate therapists are eligible."),
   ("GoodTherapy",
    "https://www.goodtherapy.org/join-therapist-directory-membership.html",
    "The priciest mainstream directory — <b>$30.95 to $49.95 a month</b>. Worth "
    "putting on a trial-and-cancel timer."),
   ("Alma",
    "https://helloalma.com/for-providers/",
    "Not a directory: <b>$95 a month</b> for credentialing, billing and "
    "negotiated insurance rates. A fixed cost that only pays back at volume."),
   ("Headway",
    "https://headway.co/for-providers",
    "No membership fee, but Headway sets the insurance rate you are paid — the "
    "cost is inside the reimbursement rather than a subscription. Credentialing "
    "in as little as 30 days."),
   ("Grow Therapy",
    "https://growtherapy.com/providers",
    "Same model. Credentialing in <b>5–7 days</b> on average. Compare the "
    "effective hourly against your private-pay rate before switching."),
  ]),

 ("Where numbers come from", "The sources behind the tools here",
  "Every figure in the calculators on this site traces to one of these. They "
  "are listed so you can check the work, or build your own.",
  [
   ("MIT Living Wage Calculator",
    "https://livingwage.mit.edu/states/06",
    "A county-specific floor for what you actually need to earn, rather than a "
    "national average. California's living wage for one adult with no children "
    "is <b>$30.48 an hour</b>; data last updated 15 February 2026."),
   ("BLS wage data by occupation",
    "https://www.bls.gov/oes/2025/may/oes_stru.htm",
    "The authoritative wage survey. Note BLS retired its static per-occupation "
    "pages after May 2023, so current figures have to be read from the "
    "interactive tool."),
   ("Median pay — marriage and family therapists",
    "https://www.bls.gov/ooh/community-and-social-service/marriage-and-family-therapists.htm",
    "<b>$63,780</b> median, May 2024, with employment projected to grow 13% "
    "from 2024 to 2034."),
   ("Median pay — counselors",
    "https://www.bls.gov/ooh/community-and-social-service/substance-abuse-behavioral-disorder-and-mental-health-counselors.htm",
    "<b>$59,190</b> a year, or $28.46 an hour, May 2024."),
   ("Median pay — social workers",
    "https://www.bls.gov/ooh/community-and-social-service/social-workers.htm",
    "<b>$61,330</b> median overall; healthcare social workers $68,090 and "
    "mental health and substance abuse social workers $60,060, May 2024."),
   ("California payroll tax rates",
    "https://edd.ca.gov/en/payroll_taxes/rates_and_withholding/",
    "If you elect S-corp treatment and put yourself on payroll, these come out "
    "of your own cheque. <b>SDI is 1.3% for 2026 with no wage cap</b> — the cap "
    "was removed in 2024, so any older model that caps it is wrong."),
   ("California tax rate schedules",
    "https://www.ftb.ca.gov/file/personal/tax-calculator-tables-rates.asp",
    "The bracket tables the state calculation should be built from, straight "
    "from FTB. Re-check each January."),
  ]),
]
