# -*- coding: utf-8 -*-
"""The 24 Bay Area organization profiles - hand-written from the banked
research (claude/bay-org-profiles-research.md, three fetch passes, all
read 16 August 2026). Every fact below was read from a fetched page whose
URL is recorded beside it; nothing is inferred.

RULES THIS DATA OBEYS
  - No availability language, ever. "Its site describes a program" is a
    fact; "it is hiring" is a guess about today. The builder guards this.
  - No personal names or personal email addresses - the research recorded
    some; they are deliberately NOT carried here. Program pages are linked
    instead, which is where a contact belongs anyway.
  - `status` is what the org's OWN SITE publishes, on the read date:
      published   a clinical training / trainee / associate program page
      none        nothing published (which is a finding, not a blank)
      paused      a program page that itself announces a pause
      volunteer   a volunteer training that is not a licensure track
      collective  an organization built around associates rather than
                  running a placement program
      nonclinical no mental-health clinical content on the site at all
  - Meta fields (question/outcome/number/desc) are plain ASCII - entities
    in ts:meta double-escape downstream (registry_meta -> social_cards).
"""

READ = "16 August 2026"

ORGS = [
 dict(
  slug="momentum-for-health.html", name="Momentum for Health",
  irs="Momentum for Health", site="momentumforhealth.org",
  where="San Jose &middot; Santa Clara County", status="published",
  what=["Santa Clara County behavioral-health nonprofit serving 4,500+ "
        "people a year: adult outpatient, residential and crisis "
        "residential, a crisis stabilization unit, supported and "
        "transitional housing, employment services, the TRUST "
        "non-law-enforcement mobile crisis team, and the La Selva "
        "Community Clinic. CARF-accredited and DHCS-licensed, with a "
        "staff of about 550 working across 44 languages including ASL."],
  facts=[
   ("Its internships page states that Momentum offers &ldquo;both "
    "mentored practicum and field placement opportunities&rdquo; across "
    "outpatient, residential and partial-hospitalization settings, at "
    "about 16&ndash;24 hours per week, and describes the placements as "
    "paid.", "https://momentumforhealth.org/internships/"),
   ("Its careers page states: &ldquo;we offer hours toward licensure "
    "and clinical supervision in a community behavioral health "
    "nonprofit setting.&rdquo;",
    "https://momentumforhealth.org/work-with-us/"),
   ("Benefits its site publishes include a retirement match of "
    "4&ndash;9%.", "https://momentumforhealth.org/work-with-us/"),
  ],
  question="Does Momentum for Health publish a clinical training program?",
  outcome="Yes - a practicum and field placement page, described as paid,"
          " across outpatient, residential and PHP settings",
  number="4,500+ people served a year across 44 languages",
  desc="Profile of Momentum for Health, San Jose: what the organization "
       "is, and what its own site publishes about practicum and field "
       "placements, read on one dated day."),

 dict(
  slug="caminar.html", name="Caminar",
  irs="Caminar", site="caminar.org",
  where="San Mateo &amp; Santa Clara counties", status="published",
  what=["Mental health and substance-use treatment with wraparound "
        "services &mdash; housing, vocational and job training &mdash; "
        "plus counseling, psychiatry and medication management, "
        "outpatient SUD treatment and sober living, prevention and "
        "education programs including LGBTQIA+ services, and the Teen "
        "and Family Wellness Center in Palo Alto. Its own 2025 figures: "
        "12,721 people accessing services and 23,096 reached through "
        "housing support."],
  facts=[
   ("A school-based practicum description linked from its careers page "
    "offers &ldquo;group and individual supervision and extensive "
    "training&rdquo; for interns and trainees pursuing BBS licensure.",
    "https://caminar.org/careers"),
   ("The same description states &ldquo;20 to 40 hours of paid clinical "
    "work per week&rdquo; counting toward the 3,000, in San Jose-area "
    "school and community settings, through its Family &amp; Children "
    "Services affiliation.", "https://caminar.org/careers"),
  ],
  question="Does Caminar publish a clinical training program?",
  outcome="Yes - a school-based practicum description with 20 to 40 paid "
          "clinical hours a week, via its careers page",
  number="20 to 40 hours of paid clinical work per week",
  desc="Profile of Caminar: what the organization is, and the "
       "school-based practicum its own careers page describes, read on "
       "one dated day."),

 dict(
  slug="rams-san-francisco.html",
  name="RAMS (Richmond Area Multi-Services)",
  irs="Richmond Area Multi-services Inc", site="ramsinc.org",
  where="San Francisco &amp; Alameda counties", status="published",
  what=["San Francisco community behavioral-health nonprofit &mdash; "
        "&ldquo;30+ Programs | 130+ Sites&rdquo; by its own count "
        "&mdash; across the Richmond District, Lower Pacific Heights, "
        "Dogpatch and the Tenderloin, plus Alameda County, with care "
        "offered in more than 30 languages. Clinical and counseling "
        "services, the Hire-Ability vocational program, peer services "
        "and prevention."],
  facts=[
   ("Its Training Institute page describes Social Work, MFT and PCC "
    "practicums &mdash; &ldquo;systems oriented, Community Mental "
    "Health Practicums&rdquo; &mdash; and an Outpatient Clinical "
    "Practicum open to psychology, social work and MFT students.",
    "https://ramsinc.org/programs/rams-training-institute/"),
   ("The same Institute houses the National Asian American Psychology "
    "Training Center doctoral internship, established 1979, which its "
    "site calls the first program in the USA focused on training "
    "psychologists expert in Asian-American communities.",
    "https://ramsinc.org/programs/rams-training-institute/"),
  ],
  question="Does RAMS publish a clinical training program?",
  outcome="Yes - a named Training Institute with MFT, PCC and MSW "
          "practicums and a doctoral internship dating to 1979",
  number="30+ programs across 130+ sites, in 30+ languages",
  desc="Profile of RAMS in San Francisco: what the organization is, and "
       "the practicums its Training Institute page describes, read on "
       "one dated day."),

 dict(
  slug="aaci-san-jose.html",
  name="AACI (Asian Americans for Community Involvement)",
  irs="Asian Americans for Community Involvement of Santa Clara Co Inc",
  site="aaci.org",
  where="San Jose &middot; Santa Clara County", status="published",
  what=["Among the largest community-based organizations serving "
        "marginalized ethnic communities in Santa Clara County: primary "
        "care, dentistry and behavioral health &mdash; adult and older "
        "adult, family and children, and the Center for Survivors of "
        "Torture &mdash; plus a domestic-violence shelter and senior "
        "and youth programs, in more than 40 languages, from 2400 "
        "Moorpark Avenue in San Jose."],
  facts=[
   ("Its internship page describes an APA-accredited clinical "
    "psychology doctoral internship at &ldquo;$26.00 an hour for the "
    "entire internship year,&rdquo; across three tracks, with at least "
    "two hours of weekly didactics.", "https://aaci.org/internship-training/"),
   ("The published program is doctoral. Whether AACI places MFT-level "
    "trainees is not addressed on the pages read &mdash; its careers "
    "page is where that question goes.", "https://aaci.org/careers/"),
  ],
  question="Does AACI publish a clinical training program?",
  outcome="Yes at the doctoral level - an APA-accredited psychology "
          "internship at $26 an hour; MFT-level placement is not "
          "addressed on its site",
  number="$26.00 an hour for the entire internship year",
  desc="Profile of AACI in San Jose: what the organization is, and the "
       "doctoral internship its own site describes, read on one dated "
       "day."),

 dict(
  slug="lincoln-families.html", name="Lincoln Families",
  irs="Lincoln", site="lincolnfamilies.org",
  where="Oakland &middot; Alameda &amp; Contra Costa counties",
  status="published",
  what=["Founded 1883, working to &ldquo;disrupt cycles of poverty and "
        "trauma&rdquo; through thirteen programs of school- and "
        "community-based mental health across Alameda and Contra Costa "
        "counties."],
  facts=[
   ("Its clinicians training program page describes a practicum for "
    "clinical or counseling psychology, MFT and social work graduate "
    "students: individual, group and family therapy, with &ldquo;one "
    "hour per week of individual supervision,&rdquo; &ldquo;two hours "
    "per week of group supervision (case conference)&rdquo; and two "
    "hours of weekly didactics.",
    "https://lincolnfamilies.org/clinicians-training-program"),
   ("The same page lists educational reimbursements: &ldquo;$4000 for "
    "first year graduate students&rdquo; and &ldquo;$2000 for each "
    "additional graduate student year.&rdquo;",
    "https://lincolnfamilies.org/clinicians-training-program"),
   ("Its careers pages describe licensing-fee reimbursement, 90&ndash;"
    "95% subsidized benefits, and PSLF eligibility.",
    "https://lincolnfamilies.org/clinicians-training-program"),
  ],
  question="Does Lincoln Families publish a clinical training program?",
  outcome="Yes - a practicum page with the supervision hours itemized "
          "and a $4,000 first-year educational reimbursement",
  number="$4,000 first-year educational reimbursement",
  desc="Profile of Lincoln Families in Oakland: what the organization "
       "is, and the practicum structure its training page itemizes, "
       "read on one dated day."),

 dict(
  slug="east-bay-agency-for-children.html",
  name="East Bay Agency for Children (EBAC)",
  irs="East Bay Agency for Children", site="ebac.org",
  where="Oakland &middot; Alameda County", status="published",
  what=["Alameda County nonprofit headquartered at 2828 Ford Street, "
        "Oakland: family resource centers, school-based behavioral "
        "health, grief and loss services, afterschool and early "
        "childhood programs, and the Trauma Transformed initiative."],
  facts=[
   ("Its careers page states EBAC &ldquo;accepts applications for "
    "social work students in a Master&rsquo;s degree program,&rdquo; "
    "with a practicum that &ldquo;focuses on grief and loss support "
    "groups&hellip; grief education, and short term grief therapy "
    "services for children.&rdquo;", "https://ebac.org/careers/careers.asp"),
   ("The same page describes intern practicum placements for graduate "
    "and undergraduate students. The published track is MSW-shaped; "
    "MFT specifics are not addressed on the pages read.",
    "https://ebac.org/careers/careers.asp"),
  ],
  question="Does EBAC publish a clinical training program?",
  outcome="Yes - a grief-focused MSW practicum described on its careers "
          "page; MFT specifics not addressed",
  number="A grief-focused practicum for MSW students",
  desc="Profile of East Bay Agency for Children: what the organization "
       "is, and the grief-focused practicum its careers page describes, "
       "read on one dated day."),

 dict(
  slug="westcoast-childrens-clinic.html",
  name="WestCoast Children's Clinic",
  irs="Westcoast Childrens Clinic", site="westcoastcc.org",
  where="Oakland &middot; Alameda County", status="published",
  what=["Oakland children&rsquo;s psychology clinic whose mission "
        "statement explicitly includes training &ldquo;the next "
        "generation of mental health professionals&rdquo;: assessment, "
        "therapy, care coordination, a 24/7 crisis hotline for foster "
        "youth, intensive services for commercially sexually exploited "
        "children, and young-adult wraparound for ages 16&ndash;24."],
  facts=[
   ("Its internships page describes an eight-month compensated clinical "
    "training program for incoming second-year MSW or MFT students, "
    "running September to April with a week-long August "
    "pre-orientation; partner schools listed are CSU East Bay, Palo "
    "Alto University, SFSU, Smith, Saint Mary&rsquo;s and UC Berkeley.",
    "https://westcoastcc.org/internships"),
   ("An Advanced Assessment Practicum for fourth-year doctoral students "
    "runs 20 hours a week with &ldquo;2 hours of individual supervision "
    "each week, and&hellip; 1.5 hours of group supervision&rdquo; plus "
    "two didactic hours, at a stipend of &ldquo;$3,500 for the "
    "year.&rdquo;", "https://westcoastcc.org/internships"),
   ("It also runs an APA-accredited doctoral internship.",
    "https://westcoastcc.org/internships"),
  ],
  question="Does WestCoast Children's Clinic publish a clinical "
           "training program?",
  outcome="Yes - an 8-month compensated MSW/MFT program with named "
          "partner schools, plus doctoral tracks",
  number="An 8-month compensated program, September to April",
  desc="Profile of WestCoast Children's Clinic in Oakland: what the "
       "organization is, and the training programs its internships "
       "page describes, read on one dated day."),

 dict(
  slug="side-by-side-youth.html", name="Side by Side",
  irs="Side By Side", site="sidebysideyouth.org",
  where="Marin, Alameda, Sonoma &amp; Napa counties", status="published",
  what=["Youth services organization for ages 5&ndash;26 and their "
        "families: behavioral and mental health services, early "
        "intervention in schools, LGBTQIA+ programs, transitional "
        "housing for former foster youth, special education, and care "
        "coordination, across Marin, Alameda, Sonoma and Napa "
        "counties."],
  facts=[
   ("Its careers and internships page describes community counseling "
    "internships with &ldquo;1 hour of clinical supervision per week, "
    "2 hours of group supervision per week, training opportunities "
    "within the agency.&rdquo;",
    "https://sidebysideyouth.org/careers-and-internships/"),
  ],
  question="Does Side by Side publish a clinical training program?",
  outcome="Yes - community counseling internships with the supervision "
          "hours stated",
  number="1 hour individual plus 2 hours group supervision a week",
  desc="Profile of Side by Side: what the organization is, and the "
       "counseling internships its own site describes, read on one "
       "dated day."),

 dict(
  slug="crisis-support-services-alameda.html",
  name="Crisis Support Services of Alameda County",
  irs="Crisis Support Services of Alameda County",
  site="crisissupport.org",
  where="Oakland &middot; Alameda County", status="published",
  what=["Operating since 1966: 988 call, text and chat plus a local "
        "24-hour line (1-800-309-2131), therapy and counseling from "
        "youth through older adults, support groups across Alameda "
        "County, and community education, from its Oakland office."],
  facts=[
   ("Its join-our-team page states: &ldquo;Our interns are graduate and "
    "doctoral students who have progressed far enough through their "
    "degree programs to start obtaining hours for licensure,&rdquo; "
    "across child psychology, grief, crisis counseling and geriatric "
    "mental health.", "https://crisissupport.org/join-our-team"),
   ("The same page recruits licensed clinicians &ldquo;to supervise our "
    "trainees and associates&rdquo; &mdash; which is its own statement "
    "that both trainees and associates work there.",
    "https://crisissupport.org/join-our-team"),
  ],
  question="Does Crisis Support Services of Alameda County publish a "
           "clinical training program?",
  outcome="Yes - its site describes interns obtaining hours for "
          "licensure, and supervision of trainees and associates",
  number="A 24-hour crisis line running since 1966",
  desc="Profile of Crisis Support Services of Alameda County: what the "
       "organization is, and what its own site publishes about interns "
       "and supervision, read on one dated day."),

 dict(
  slug="one-life-counseling-center.html",
  name="One Life Counseling Center",
  irs="One Life Counseling Center",
  site="onelifecounselingcenter.org",
  where="San Carlos &middot; San Mateo County", status="published",
  what=["San Mateo County counseling nonprofit at 1303 San Carlos "
        "Avenue: individual and family counseling, Child-Parent "
        "Psychotherapy, school-based services, the Una Vida program, "
        "Music for the Mind, Monday Market food assistance, and youth "
        "development."],
  facts=[
   ("Its work-with-us page describes &ldquo;tailored trainee and "
    "associate positions&rdquo; for counseling psychology, MFT and "
    "LPCC graduate students, with &ldquo;comprehensive "
    "supervision&rdquo; and the ability to &ldquo;earn competitive pay "
    "while gaining the hours.&rdquo;",
    "https://onelifecounselingcenter.org/work-with-us"),
   ("The same page counts &ldquo;six active supervision groups&rdquo; "
    "and &ldquo;over 70 licensed therapists as community "
    "members,&rdquo; and states Spanish-language capacity explicitly.",
    "https://onelifecounselingcenter.org/work-with-us"),
  ],
  question="Does One Life Counseling Center publish a clinical training "
           "program?",
  outcome="Yes - paid trainee and associate roles described, with six "
          "supervision groups and explicit Spanish capacity",
  number="Six active supervision groups",
  desc="Profile of One Life Counseling Center in San Carlos: what the "
       "organization is, and the trainee and associate roles its own "
       "site describes, read on one dated day."),

 dict(
  slug="family-paths.html", name="Family Paths",
  irs="Family Paths Inc", site="familypaths.org",
  where="Oakland &middot; Alameda County", status="paused",
  what=["Established 1972 in Oakland: trauma-informed mental health "
        "treatment, a 24/7 parenting helpline (1-800-829-3777), "
        "parenting education, case management and employment support "
        "through CalWORKS/BOOST, and a foster-parent advice line."],
  facts=[
   ("Its volunteer page describes a clinical intern program for "
    "second-year graduate students and registered interns, with an "
    "annual stipend of &ldquo;$2,500 for trainees, $3,000 for "
    "registered interns&rdquo; and weekly individual and group "
    "supervision.", "https://familypaths.org/volunteer"),
   ("THE FLAG, in the site&rsquo;s own words: &ldquo;Due to some "
    "planned reorganization in 2026, the agency will be pausing our "
    "Clinical Intern Program at the end of August 2026.&rdquo; Read "
    "that date against your own timeline before spending an "
    "application here.", "https://familypaths.org/volunteer"),
   ("Its careers pages describe free CEUs, supervision offered in "
    "Spanish, a 5% bilingual differential, and a salary increase on "
    "licensure.", "https://familypaths.org/volunteer"),
  ],
  question="Does Family Paths publish a clinical training program?",
  outcome="Yes, with a published pause - its own site announces the "
          "intern program pauses at the end of August 2026",
  number="Program pause announced for the end of August 2026",
  desc="Profile of Family Paths in Oakland: the clinical intern program "
       "its site describes, and the pause the same page announces, read "
       "on one dated day."),

 # ---------------------------------------------------- nothing published
 dict(
  slug="progress-foundation.html", name="Progress Foundation",
  irs="Progress Foundation", site="progressfoundation.org",
  where="San Francisco, Napa &amp; Sonoma counties", status="none",
  what=["Runs &ldquo;alternatives to institutional placement&rdquo;: a "
        "psychiatric crisis clinic, crisis residential and transitional "
        "residential programs, case management and cooperative living, "
        "all voluntary-admission, across San Francisco, Napa, Sonoma "
        "and Marin."],
  none_note=["No practicum or trainee program page was found on its "
             "site. What it does publish is an employment culture: "
             "&ldquo;every open position is posted in-house, and every "
             "internal candidate is interviewed,&rdquo; with 100% "
             "employer-paid medical, dental, vision, EAP and life "
             "coverage, three to six weeks of vacation, and a 403(b) "
             "with a 4% contribution. For an associate that reads as an "
             "employer profile rather than a placement shelf."],
  careers="https://progressfoundation.org/employment/",
  question="Does Progress Foundation publish a clinical training "
           "program?",
  outcome="No program page found - what it publishes is a "
          "promotion-from-within employment culture and full-paid "
          "benefits",
  number="100% employer-paid medical, dental and vision",
  desc="Profile of Progress Foundation: what the organization is, and "
       "the finding that no training program page exists on its site, "
       "read on one dated day."),

 dict(
  slug="edgewood-center.html",
  name="Edgewood Center for Children and Families",
  irs="Edgewood Center for Children and Families", site="edgewood.org",
  where="San Francisco &amp; San Mateo counties", status="none",
  what=["Working with children, teens and young adults 18&ndash;26 "
        "since 1851: 24/7 crisis stabilization, residential treatment, "
        "intensive outpatient, outpatient, psychological testing, "
        "partial hospitalization, a non-public high school, "
        "transitional-age-youth housing and a family resource center, "
        "across more than 15 programs and six Bay Area locations, "
        "serving about 4,000 people a year with 300+ youth "
        "mental-health professionals."],
  none_note=["A site search for &ldquo;internship&rdquo; returns "
             "nothing, and the careers page describes culture rather "
             "than a training track. For a trainee that means the "
             "question goes to the organization directly, with your "
             "program&rsquo;s placement office in the loop."],
  careers="https://edgewood.org",
  question="Does Edgewood publish a clinical training program?",
  outcome="No - a site search for internship returns nothing; the "
          "question goes to the organization directly",
  number="More than 15 programs across 6 Bay Area locations",
  desc="Profile of Edgewood Center for Children and Families: what the "
       "organization is, and the finding that no training page exists "
       "on its site, read on one dated day."),

 dict(
  slug="fred-finch-youth-center.html", name="Fred Finch Youth Center",
  irs="Fred Finch Youth Center", site="fredfinch.org",
  where="Oakland &middot; Alameda County", status="none",
  what=["Serving youth and families since 1891: mental health services, "
        "residential programs, housing, Enhanced Care Management, "
        "young-adult services, school services and the Rising Harte "
        "Wellness Center. Joint Commission accredited."],
  none_note=["Its &ldquo;Training Institute&rdquo; is easy to misread "
             "from the name: the page describes a free, Title "
             "IV-E-funded continuing-education institute offering CE "
             "hours to already-licensed LMFTs, LCSWs, LPCCs and LEPs "
             "&mdash; not a practicum or associate track. No "
             "pre-licensed clinical training page was found.",],
  careers="https://fredfinch.org/careers",
  question="Does Fred Finch publish a clinical training program?",
  outcome="No - its Training Institute is licensed-clinician CE, not a "
          "licensure track",
  number="Serving youth and families since 1891",
  desc="Profile of Fred Finch Youth Center: what the organization is, "
       "and why its Training Institute is not a practicum track, read "
       "on one dated day."),

 dict(
  slug="prc-baker-places.html", name="PRC (with Baker Places)",
  irs="Baker Places Inc", site="prcsf.org",
  where="San Francisco", status="none",
  what=["PRC merged with the AIDS Emergency Fund and Baker Places in "
        "2016 and serves 5,000+ clients a year from 170 9th Street: "
        "residential treatment, acute services, supportive housing, "
        "legal advocacy and workforce development. Baker Places no "
        "longer has a standalone site."],
  none_note=["No training or practicum page was found; the careers "
             "surface is a bare applicant-tracking portal. The IRS "
             "file still lists Baker Places Inc separately, which is "
             "why directory rows and this profile carry both names."],
  careers="https://prcsf.org",
  question="Does PRC publish a clinical training program?",
  outcome="No page found - the careers surface is a bare portal, and "
          "Baker Places has no standalone site since the 2016 merger",
  number="5,000+ clients a year",
  desc="Profile of PRC and Baker Places in San Francisco: what the "
       "merged organization is, and the finding that no training page "
       "exists, read on one dated day."),

 dict(
  slug="buckelew-programs.html", name="Buckelew Programs",
  irs="Buckelew Programs", site="buckelew.org",
  where="Marin, Sonoma, Lake &amp; Mendocino counties", status="none",
  what=["By its own description the North Bay&rsquo;s largest nonprofit "
        "provider of mental health and substance-use treatment, since "
        "1970: counseling, detox, residential and sober-living SUD "
        "programs, suicide prevention including 988 work, and supported "
        "housing, from offices in Novato and Santa Rosa. "
        "&ldquo;Hablamos espa&ntilde;ol&rdquo;; the Mariposa program "
        "offers free clinical therapy for Spanish-speaking women; "
        "Medi-Cal, Carelon and private pay."],
  none_note=["Its counseling page mentions &ldquo;internships and "
             "volunteer opportunities&rdquo; in passing and lists an "
             "AMFT on staff, but no program page describes a track, "
             "supervision structure or application. Benefits its "
             "careers page does publish: 100% employer-paid medical, "
             "dental, vision and life, up to six weeks PTO, and a "
             "403(b) match."],
  careers="https://buckelew.org/about/careers/",
  question="Does Buckelew Programs publish a clinical training program?",
  outcome="No program page - one passing mention of internships, an "
          "AMFT on staff, and a benefits page",
  number="The North Bay's largest nonprofit MH provider, since 1970",
  desc="Profile of Buckelew Programs: what the organization is, and the "
       "gap between its internship mention and a published program, "
       "read on one dated day."),

 dict(
  slug="westside-community-mental-health.html",
  name="Westside Community Mental Health Center",
  irs="Westside Community Mental Health Center",
  site="westside-health.org",
  where="San Francisco", status="none",
  what=["A roughly 60-year-old San Francisco community mental-health "
        "organization at 1153 Oak Street: child, adolescent and adult "
        "outpatient and crisis clinics, methadone substance-use "
        "treatment, HIV case management, a Clubhouse psychosocial "
        "rehabilitation program, and violence-prevention work including "
        "the Ajani Program, Black to the Future, and the NO VIOLENCE "
        "ALLIANCE."],
  none_note=["Nothing about practicum, trainees or associates is "
             "published anywhere on the site that was read. That makes "
             "it a lead for a direct question, not a shelf."],
  careers="https://westside-health.org/employment-opportunities",
  question="Does Westside Community Mental Health Center publish a "
           "clinical training program?",
  outcome="No - nothing published; a direct-question lead rather than "
          "a shelf",
  number="Roughly 60 years serving San Francisco",
  desc="Profile of Westside Community Mental Health Center: what the "
       "organization is, and the finding that no training content is "
       "published, read on one dated day."),

 dict(
  slug="jfcs-east-bay.html", name="JFCS East Bay",
  irs="Jewish Family and Community Services East Bay",
  site="jfcs-eastbay.org",
  where="Berkeley &amp; Concord &middot; Alameda &amp; Contra Costa",
  status="none",
  what=["Jewish Family and Community Services East Bay, from Berkeley "
        "(2484 Shattuck) and Concord: refugee resettlement and mental "
        "health, immigration legal services, older-adult care "
        "management and counseling, children and family services "
        "including play therapy, Holocaust-survivor support, "
        "Russian-language programs and LGBTQ refugee support."],
  none_note=["No practicum or trainee content is published on the pages "
             "read. Its careers page does carry unusual benefit detail "
             "&mdash; a 401(k) with a 3% match and ten federal plus six "
             "Jewish paid holidays &mdash; which reads as an employer "
             "profile for licensed and associate-level applicants."],
  careers="https://jfcs-eastbay.org/who-we-are/careers/",
  question="Does JFCS East Bay publish a clinical training program?",
  outcome="No - nothing published about practicum or trainees; the "
          "careers page is an employer profile",
  number="Ten federal plus six Jewish paid holidays",
  desc="Profile of JFCS East Bay: what the organization is, and the "
       "finding that no training content is published, read on one "
       "dated day."),

 dict(
  slug="peninsula-healthcare-connection.html",
  name="Peninsula Healthcare Connection",
  irs="Peninsula Healthcare Connection Inc", site="peninsulahcc.org",
  where="Palo Alto &middot; Santa Clara &amp; San Mateo counties",
  status="none",
  what=["Healthcare for unhoused and vulnerable people for over 15 "
        "years, from 33 Encina Avenue in Palo Alto: primary care, "
        "behavioral health with a board-certified psychiatrist and "
        "licensed counselors offering medication management and "
        "therapy, and the New Directions community behavioral-health "
        "and case-management program."],
  none_note=["No training or practicum page was found on its site."],
  careers="https://peninsulahcc.org/careers",
  question="Does Peninsula Healthcare Connection publish a clinical "
           "training program?",
  outcome="No page found - the behavioral-health team it describes is "
          "licensed-level",
  number="15+ years of street-level healthcare in Palo Alto",
  desc="Profile of Peninsula Healthcare Connection: what the "
       "organization is, and the finding that no training page exists, "
       "read on one dated day."),

 dict(
  slug="john-muir-behavioral-health.html",
  name="John Muir Behavioral Health",
  irs="John Muir Behavioral Health", site="johnmuirhealth.com",
  where="Concord &middot; Contra Costa County", status="none",
  what=["The behavioral-health arm of the John Muir Health system: an "
        "inpatient psychiatric hospital at 2740 Grant Street, Concord "
        "(no walk-in or emergency entrance), with partial "
        "hospitalization and intensive outpatient programs for adults, "
        "serving children through older adults in crisis."],
  none_note=["The only training programs found anywhere on the health "
             "system&rsquo;s site are a Family Medicine residency and a "
             "pharmacy residency &mdash; physician and pharmacist "
             "tracks, not behavioral-health licensure. No pre-licensed "
             "clinical track is published."],
  careers="https://johnmuirhealth.com/get-involved/careers.html",
  question="Does John Muir Behavioral Health publish a clinical "
           "training program?",
  outcome="No - the only residencies published are physician and "
          "pharmacy tracks",
  number="Physician and pharmacy residencies only",
  desc="Profile of John Muir Behavioral Health: what the hospital "
       "system runs, and the finding that no behavioral-health "
       "licensure track is published, read on one dated day."),

 # ---------------------------------------------------------- the specials
 dict(
  slug="center-for-mindful-psychotherapy.html",
  name="Center for Mindful Psychotherapy",
  irs="Center for Mindful Psychotherapy Inc", site="mindfulcenter.org",
  where="San Francisco &middot; telehealth across California",
  status="collective",
  what=["By its own description &ldquo;a non-profit collective of "
        "~125 Associate Marriage and Family Therapists dedicated to "
        "providing holistic, mindful care&rdquo; &mdash; in-person in "
        "the San Francisco Bay Area and by telehealth throughout "
        "California, working in somatic, relational, mindfulness-based "
        "and trauma-informed modalities."],
  none_note=["This is the one organization on this shelf that is BUILT "
             "AROUND associates rather than running a placement "
             "program on the side: the collective is the associates. "
             "Its homepage does not detail the supervision structure, "
             "so the questions to bring are exactly the standard ones "
             "&mdash; who supervises, on what schedule, and under "
             "which employment terms. One caution from this "
             "site&rsquo;s own research: a similarly-named Santa "
             "Barbara solo practice at a different domain is a "
             "different organization entirely."],
  careers="https://mindfulcenter.org",
  question="What is the Center for Mindful Psychotherapy?",
  outcome="A nonprofit collective of roughly 125 associate MFTs - the "
          "collective is the associates, not a program beside them",
  number="A collective of ~125 associate MFTs",
  desc="Profile of the Center for Mindful Psychotherapy in San "
       "Francisco: a nonprofit collective built around associate MFTs, "
       "read on one dated day."),

 dict(
  slug="contra-costa-crisis-center.html",
  name="Contra Costa Crisis Center",
  irs="Contra Costa Crisis Center", site="crisis-center.org",
  where="Walnut Creek &middot; Contra Costa County", status="volunteer",
  what=["Running since 1963 from the Walnut Creek area: 24/7 crisis and "
        "suicide prevention (988, or text HOPE to 20121), grief "
        "support, the 211 information line for Contra Costa County, "
        "homeless services and on-site crisis response, with a staff "
        "of about 35 and roughly 40 volunteers."],
  none_note=["What it publishes is a VOLUNTEER track, not a clinical "
             "practicum: &ldquo;A 54-hour training program prepares "
             "new volunteers to answer our 24-hour crisis lines,&rdquo; "
             "followed by a weekly four-hour shift for a year; grief "
             "facilitators need twelve months of call-center experience "
             "or 200 hours of group facilitation. Whether any of those "
             "hours can count toward a practicum is not addressed on "
             "its site &mdash; that is a question for your program, "
             "answered against the trainee rules, before you commit a "
             "year of shifts."],
  careers="https://crisis-center.org",
  question="Does the Contra Costa Crisis Center offer clinical "
           "practicum hours?",
  outcome="What it publishes is a 54-hour volunteer track with a "
          "year-long shift commitment - not a clinical practicum",
  number="A 54-hour volunteer training, then a weekly shift for a year",
  desc="Profile of the Contra Costa Crisis Center: the volunteer track "
       "its site describes, and why it is not a practicum, read on one "
       "dated day."),

 dict(
  slug="translifeline.html", name="Trans Lifeline",
  irs="Translifeline", site="translifeline.org",
  where="Remote &middot; based in San Francisco", status="volunteer",
  what=["A national trans-led peer-support hotline (877-565-8860) that "
        "has answered 150,000+ calls, alongside roughly $1.5 million in "
        "microgrants, a resource library, and the #SafeHotlines "
        "advocacy campaign. Fully remote, based in San Francisco."],
  none_note=["Volunteers complete a 36-hour self-guided training. On "
             "clinical-hours credit its site commits to nothing: "
             "&ldquo;Depending on your program&rsquo;s specific "
             "requirements, it may be possible,&rdquo; case by case. "
             "Treat it as peer-support volunteering that MIGHT credit, "
             "confirmed in writing by both your program and the "
             "organization before you count a single hour."],
  careers="https://translifeline.org",
  question="Can Trans Lifeline volunteering count toward clinical "
           "hours?",
  outcome="Its site says only that credit may be possible case by case "
          "- get it in writing from your program first",
  number="150,000+ calls answered by a trans-led peer line",
  desc="Profile of Trans Lifeline: the peer-support volunteer track its "
       "site describes, and the case-by-case answer it gives on hours, "
       "read on one dated day."),

 dict(
  slug="eden-housing-resident-services.html",
  name="Eden Housing Resident Services",
  irs="Eden Housing Resident Services Inc", site="edenhousing.org",
  where="Hayward &middot; statewide", status="nonclinical",
  what=["An affordable-housing developer and manager with 160+ "
        "communities across California, whose resident-services arm "
        "provides education, technology access, economic empowerment, "
        "health and wellness programming, and a referral line "
        "(855-451-8111)."],
  none_note=["It appears in the Bay Area nonprofit table because its "
             "IRS activity code lands in the mental-health family, but "
             "no clinical or mental-health service content appears "
             "anywhere on its site. It is filed here so the next "
             "person does not spend an afternoon discovering the same "
             "thing: this is a housing organization, not a clinical "
             "placement."],
  careers="https://edenhousing.org",
  question="Is Eden Housing Resident Services a clinical placement "
           "lead?",
  outcome="No - a housing organization whose IRS code lands near "
          "mental health; no clinical content on its site",
  number="160+ housing communities, zero clinical pages",
  desc="Profile of Eden Housing Resident Services: why a housing "
       "organization appears in a mental-health table, and why it is "
       "not a placement lead, read on one dated day."),
]

# Every org above must be one of the directory's curated set, and the
# builder asserts the reverse too - a curated org without a profile is
# listed by name so the gap is loud rather than silent.
