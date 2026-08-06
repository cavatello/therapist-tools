# -*- coding: utf-8 -*-
"""Where people talk candidly about these programmes.

Every URL below was live-verified on 6 August 2026 against the host's own
endpoint - not constructed from a thread ID, which is how link rot gets shipped
at scale. Descriptions are mine. Nothing is quoted beyond a phrase, because the
point is to send a reader to the discussion rather than to reproduce it here.

Two subreddits that used to be the richest source for this topic are gone:
r/psychotherapy is private and r/mft is banned. Nine otherwise-good threads
were dropped for that reason. Where a school has no entry below, it is because
nothing credible was found - which is itself worth knowing, and the page says
so rather than leaving a silent gap.

sentiment: one of "positive", "mixed", "negative", "info"
"""

# institution key -> [(url, forum, title, year, sentiment, note)]
THREADS = {
 "Alliant International University (CSPP)": [
  ("https://www.reddit.com/r/ClinicalPsychology/comments/1bw1b13/hearing_a_ton_of_alliant_criticism/",
   "r/ClinicalPsychology", "Hearing a ton of Alliant criticism…", 2024, "negative",
   "63 comments. Long argument between people calling it a degree mill and people defending it."),
  ("https://www.reddit.com/r/psychologystudents/comments/13kptax/mft_program_at_alliant_international_university/",
   "r/psychologystudents", "MFT Program at Alliant International University (Online)", 2023, "mixed",
   "Specifically the online MFT: COAMFTE status and whether online training is adequate."),
  ("https://www.reddit.com/r/psychologystudents/comments/1peb1fp/alliant_mft_program_everyones_thoughts/",
   "r/psychologystudents", "Alliant MFT Program. Everyones thoughts?", 2025, "mixed",
   "Recent. LA applicant weighing Alliant against Pepperdine and USC; replies focus on practicum placement support."),
  ("https://www.reddit.com/r/ClinicalPsychology/comments/1izpvky/alliant_or_pepperdine_for_online_ma_mft/",
   "r/ClinicalPsychology", "Alliant or Pepperdine for online MA MFT", 2025, "negative",
   "Frames it as roughly $60k against $120k. Most replies say do neither and get an MSW."),
 ],
 "Antioch University Santa Barbara": [
  ("https://www.reddit.com/r/psychologystudents/comments/1j5h5bt/i_highly_recommend_not_going_to_antioch_lmft/",
   "r/psychologystudents", "I highly recommend NOT going to Antioch LMFT program (any of them!)", 2025,
   "negative", "A student's detailed complaint about tuition increases and administration; several classmates corroborate."),
  ("https://www.reddit.com/r/askatherapist/comments/16ixaaj/ma_clinical_psychology_antioch_la_vs_pacifica/",
   "r/askatherapist", "MA Clinical Psychology - Antioch LA vs. Pacifica?", 2023, "mixed",
   "Applicant wants IFS and somatic training; replies favour Antioch over Pacifica."),
 ],
 "Antioch University Los Angeles": [
  ("https://www.reddit.com/r/ClinicalPsychology/comments/103q704/my_end_goal_is_to_be_a_therapist_i_am_looking_at/",
   "r/ClinicalPsychology", "…Antioch LA, but it is expensive. $70–80,000 total. Is it worth it?", 2023,
   "negative", "Cost against licence portability. Consensus leans towards MSW."),
 ],
 "Pepperdine University (GSEP)": [
  ("https://www.reddit.com/r/psychologystudents/comments/1cap5vb/pepperdine_or_loma_linda/",
   "r/psychologystudents", "Pepperdine or Loma Linda", 2024, "mixed",
   "Direct MFT comparison: COAMFTE status, medical-centre placements, course load, campus culture."),
  ("https://www.reddit.com/r/ClinicalPsychology/comments/1etasyz/thoughts_on_pepperdine/",
   "r/ClinicalPsychology", "Thoughts on Pepperdine", 2024, "mixed",
   "Career-changer asks about online options. Includes a disputed exchange about religious affiliation, with current students rebutting."),
  ("https://www.reddit.com/r/psychologystudents/comments/1tiwq3k/usa_mft_masters_pepperdine_vs_antioch_vs_pacific/",
   "r/psychologystudents", "MFT Masters: Pepperdine vs Antioch vs Pacific Oaks vs Alliant", 2026, "info",
   "Very recent and specific: a parent who needs online or low-residency and cannot use the Cal States."),
 ],
 "Chapman University": [
  ("https://www.reddit.com/r/gradadmissions/comments/11ldt2v/has_anyone_heard_back_from_chapman_for_their_mft/",
   "r/gradadmissions", "Has anyone heard back from Chapman for their mft program?", 2023, "info",
   "Admissions-cycle chatter: interviews, timing, outcomes."),
  ("https://www.reddit.com/r/gradadmissions/comments/sy2h6z/chapman_mft_interview/",
   "r/gradadmissions", "chapman mft interview", 2022, "positive",
   "What the ninety-minute group interview is actually like."),
 ],
 "The Chicago School": [
  ("https://www.reddit.com/r/AcademicPsychology/comments/1fn6nx3/does_anyone_know_the_reputation_of_the_counseling/",
   "r/AcademicPsychology", "Does anyone know the reputation of the Counseling program at The Chicago School?",
   2024, "negative", "OP notes the doctoral discourse is negative and asks whether the master's differs."),
 ],
 "Touro University Worldwide": [
  ("https://www.reddit.com/r/therapists/comments/9qhxkk/touro_university_worldwide_legit_school/",
   "r/therapists", "Touro University Worldwide - Legit School?", 2018, "negative",
   "A Californian accepted to the online MFT, worried about self-sourcing internships and accreditation."),
  ("https://www.reddit.com/r/psychologystudents/comments/1mivzmt/antioch_vs_touro_mft_which_program_better/",
   "r/psychologystudents", "Antioch vs. Touro MFT — which supports licensure and working parents?", 2025,
   "info", "Concrete detail on Touro's unusual relational-hours practicum requirement."),
 ],
 "University of Southern California (Rossier)": [
  ("https://www.reddit.com/r/gradadmissions/comments/17jmmtt/usc_rossier_mft_program/",
   "r/gradadmissions", "USC Rossier – MFT Program", 2023, "info",
   "Applicants comparing assessments, acceptance rates and scholarship offers."),
  ("https://forums.studentdoctor.net/threads/usc-mft-vs-pepperdine-mft.1121395/",
   "Student Doctor Network", "USC MFT vs Pepperdine MFT", 2015, "info",
   "Roughly $100k against $60k, plus a Palo Alto University offer."),
 ],
 "University of San Francisco": [
  ("https://www.reddit.com/r/gradadmissions/comments/11kkmqt/university_of_san_francisco_counseling_psychology/",
   "r/gradadmissions", "University of San Francisco - Counseling Psychology, MFT 3yr Program", 2023,
   "positive", "Admitted students comparing the two-year and three-year tracks, and USF against CIIS."),
  ("https://www.reddit.com/r/gradadmissions/comments/1s6q40g/accepted_to_my_top_choice_but_terrified_of_debt/",
   "r/gradadmissions", "Accepted to my top choice but terrified of debt", 2026, "negative",
   "USF two-year MFT at $81k. Replies do explicit return-on-investment arithmetic."),
 ],
 "California Institute of Integral Studies": [
  ("https://www.reddit.com/r/ClinicalPsychology/comments/11b4phi/thoughts_on_ciis/",
   "r/ClinicalPsychology", "Thoughts on CIIS", 2023, "mixed",
   "Centres on accreditation and institutional history."),
  ("https://www.reddit.com/r/ClinicalPsychology/comments/1j4rujy/is_ciis_basically_a_scamwaste_of_money/",
   "r/ClinicalPsychology", "Is CIIS basically a scam/waste of money?", 2025, "mixed",
   "Includes an alum, nearly licensed, who says it prepared them well."),
 ],
 "Palo Alto University": [
  ("https://www.reddit.com/r/therapists/comments/11es4pl/is_palo_alto_university_ok_for_a_masters_to_get_a/",
   "r/therapists", "Is Palo Alto University OK for a Masters to get a MFT license?", 2023, "positive",
   "Directly master's and MFT focused, unlike most PAU threads."),
 ],
 "The Wright Institute": [
  ("https://www.reddit.com/r/ClinicalPsychology/comments/1j6zhp9/thoughts_on_the_wright_institute_psyd_program/",
   "r/ClinicalPsychology", "Thoughts on the Wright Institute — reputable, decent, or degree mill?", 2025,
   "mixed", "Includes alumni offering to answer questions directly."),
  ("https://forums.studentdoctor.net/threads/wright-institute.1428911/",
   "Student Doctor Network", "Wright Institute", 2020, "negative",
   "Long thread, mostly discouraging, from Bay Area applicants."),
 ],
 "Pacifica Graduate Institute": [
  ("https://www.reddit.com/r/psychologystudents/comments/1dq6360/is_pacifica_graduate_institute_worth_the_price/",
   "r/psychologystudents", "Is Pacifica Graduate Institute worth the price tag — MA in Counseling Psychology",
   2024, "mixed", "Applicant facing roughly $170k. Alumni disagree sharply about culture and value."),
  ("https://www.reddit.com/r/psychologystudents/comments/12scqyh/pacifica_graduate_institute_alums_or_students/",
   "r/psychologystudents", "Pacifica Graduate Institute alums or students?", 2023, "mixed",
   "Attendance requirements, and students weighing whether to leave after a quarter."),
 ],
 "California State University, Northridge": [
  ("https://www.reddit.com/r/csun/comments/1j8f2cu/rejected_in_2024_ive_been_accepted_to_csuns_mft/",
   "r/csun", "Rejected in 2024; I've been accepted to CSUN's MFT 2025 program!", 2025, "positive",
   "38 comments. A reapplicant explains what they changed; others share outcomes."),
  ("https://www.reddit.com/r/csun/comments/1api3q2/got_rejected_what_did_i_do_wrong/",
   "r/csun", "Got rejected. What did I do wrong?", 2024, "info",
   "44 comments on selectivity and application quality, from a 3.45 GPA applicant with clinical experience."),
 ],
 "San Diego State University": [
  ("https://www.reddit.com/r/gradadmissions/comments/10wbgrs/sdsu_mft_interview_invitation_2023/",
   "r/gradadmissions", "SDSU MFT interview invitation 2023", 2023, "info",
   "59 comments — the largest SDSU MFT admissions thread."),
  ("https://www.reddit.com/r/SDSU/comments/s5hyi4/sdsu_mft_program/",
   "r/SDSU", "SDSU MFT program", 2022, "mixed",
   "Application and interview structure, plus candid remarks about the profession."),
 ],
 "California State University, East Bay": [
  ("https://www.reddit.com/r/CSUEB/comments/1qqswo8/mft_program_info_sessions_experience/",
   "r/CSUEB", "MFT program info sessions experience", 2026, "negative",
   "Applicants report department staff not appearing at their own advertised info sessions two years running. Also real numbers: about 400 applications for cohorts of 20–25."),
  ("https://www.reddit.com/r/CSUEB/comments/1s2j8ff/2026_mft_grad_program/",
   "r/CSUEB", "2026 MFT grad program", 2026, "info", "Current admissions cycle."),
 ],
 "San Francisco State University": [
  ("https://www.reddit.com/r/SFSU/comments/16jzth2/applying_for_a_masters_in_counselingcmhc_or_mft/",
   "r/SFSU", "Applying for a masters in counseling — CMHC or MFT", 2023, "positive",
   "A graduate of the programme answers questions on the two tracks and on stipends. One of the better first-hand CSU accounts."),
 ],
 "California State University, Long Beach": [
  ("https://www.reddit.com/r/gradadmissions/comments/s05miy/anyone_from_csulb_counseling_psych_program_lmft/",
   "r/gradadmissions", "Anyone from CSULB counseling psych program (LMFT)?", 2022, "info",
   "45 comments on the statement of purpose and the application."),
  ("https://www.reddit.com/r/CSULB/comments/1b2lelm/denied_an_interview_for_csulb_ms_in_counseling/",
   "r/CSULB", "Denied an interview for CSULB MS in Counseling", 2024, "info",
   "A 3.9 GPA applicant denied an interview. Useful on selectivity."),
 ],
 "San Jose State University": [
  ("https://www.reddit.com/r/SJSU/comments/12f4ifu/sjsu_ma_counseling_and_guidance/",
   "r/SJSU", "SJSU MA Counseling and Guidance", 2023, "info",
   "Includes a detailed description of the group interview."),
 ],
 "Santa Clara University": [
  ("https://www.reddit.com/r/psychologystudents/comments/1rntbex/ucla_msw_vs_scu_counseling_psychology_if_i_want/",
   "r/psychologystudents", "UCLA MSW vs SCU Counseling Psychology, if I want to be a therapist", 2026,
   "mixed", "20 comments weighing the two routes."),
  ("https://forum.thegradcafe.com/topic/50830-accepted-but-now-what-msw-vs-mft",
   "The GradCafe", "Accepted, but now what? MSW vs MFT", 2014, "mixed",
   "Accepted to Santa Clara, USF and Alliant. A USF alum recommends USF; OP notes USF gave no institutional aid to MFT students that year."),
 ],
 "Loma Linda University": [
  ("https://www.reddit.com/r/therapists/comments/1ghatcl/how_is_the_play_therapy_certificate_from_loma/",
   "r/therapists", "How is the play therapy certificate from Loma Linda?", 2024, "info",
   "On the play-therapy certificate against the RPT credential."),
 ],
 "Pacific Oaks College": [
  ("https://www.reddit.com/r/psychologystudents/comments/1qw3g5g/need_advice_on_masters_programs_lmft/",
   "r/psychologystudents", "Need advice on masters programs (LMFT)", 2026, "info",
   "Pacific Oaks for someone working full time. Replies steer towards MSW."),
 ],
 "Hope International University": [
  ("https://www.reddit.com/r/AcademicPsychology/comments/bwurnc/got_accepted_into_two_mft_programs_cant_decide/",
   "r/AcademicPsychology", "Got accepted into two MFT programs, can't decide", 2019, "info",
   "Hope International against USF Sacramento. Thin, and the only credible Hope thread found."),
 ],
 "Azusa Pacific University": [
  ("https://www.reddit.com/r/psychologystudents/comments/fd9sg0/usa_ca_masters_program_for_mft/",
   "r/psychologystudents", "Masters program for MFT", 2020, "positive",
   "Azusa Pacific against University of La Verne, with second-hand alumni accounts."),
 ],
 "Saybrook University": [
  ("https://www.reddit.com/r/therapists/comments/yg9n2y/do_major_telehealth_providers_better_help_wonder/",
   "r/therapists", "Do major telehealth providers hire grads from Saybrook?", 2022, "negative",
   "Employability of an online, non-APA master's. Several people redirect to cheaper state programmes."),
 ],
 "Daybreak University": [
  ("https://forums.studentdoctor.net/threads/daybreak-university-mft-program.1502583/",
   "Student Doctor Network", "Daybreak University MFT program", 2024, "info",
   "A small COAMFTE-accredited Anaheim programme. Posters suggest verifying faculty and preferring a public university."),
 ],
}

# threads that are about the decision rather than about one school
GENERAL = [
 ("https://www.reddit.com/r/psychologystudents/comments/1uvpwko/usa_mft_msw_lpc_masters_programs_with_wscuc/",
  "r/psychologystudents", "MFT / MSW / LPC programs with WSCUC accreditation vs COAMFTE or CACREP", 2026,
  "info", "The clearest explanation found of why a WSCUC-accredited, BBS-approved degree is fine inside California and painful outside it."),
 ("https://www.reddit.com/r/therapists/comments/15zqp94/mft_moving_from_ca_to_ny_noncoamfte_school/",
  "r/therapists", "MFT moving from CA to NY (non-COAMFTE school), seeking board licensing advice", 2023,
  "negative", "What a non-COAMFTE California degree actually costs you if you leave the state."),
 ("https://www.reddit.com/r/therapists/comments/1iiik10/if_a_school_loses_accreditation_do_you_still_get/",
  "r/therapists", "If a school loses accreditation, do you still get to keep your license?", 2025, "info",
  "A prospective California student choosing among COAMFTE-listed schools that people call degree mills."),
 ("https://forums.studentdoctor.net/threads/research-shows-most-coamfte-mft-students-dont-feel-prepared-for-clinical-practice.1517656/",
  "Student Doctor Network", "Research shows most COAMFTE MFT students don't feel prepared for clinical practice",
  2026, "negative", "Cites a 2025 survey of COAMFTE practicum students. Directly relevant to whether accreditation is a quality signal."),
 ("https://forums.studentdoctor.net/threads/questions-about-mft-programs-and-practicums-in-california.1493104/",
  "Student Doctor Network", "Questions about MFT programs and practicums in California", 2024, "info",
  "A recent California graduate, now an associate, explains at length why practicum quality matters more than coursework."),
 ("https://forums.studentdoctor.net/threads/mft-program-need-advice.1306819/",
  "Student Doctor Network", "MFT program, need advice", 2018, "info",
  "A faculty member replies that at master's level there is little reputational difference, and recommends the public CSUs."),
 ("https://www.reddit.com/r/psychologystudents/comments/15lxnry/los_angeles_lmftlpcc_training_hours_always_unpaid/",
  "r/psychologystudents", "Los Angeles LMFT/LPCC training hours — always unpaid?", 2023, "negative",
  "Whether practicum and traineeship hours are paid in Los Angeles."),
 ("https://www.reddit.com/r/therapists/comments/trxr7o/no_practicum_sites_in_my_area/",
  "r/therapists", "No practicum sites in my area", 2022, "negative",
  "A rural California student in an online programme unable to find a placement. The practicum risk, made concrete."),
 ("https://www.reddit.com/r/therapists/comments/1sv18zj/the_road_to_licensure_is_destroying_my_mental/",
  "r/therapists", "The road to licensure is destroying my mental health", 2026, "negative",
  "72 comments. A California associate at about 25 clients a week. Read this before you commit."),
 ("https://www.reddit.com/r/CounselingPsychology/comments/1sc3kh9/is_taking_out_130k_ish_loan_in_loan_for_mft/",
  "r/CounselingPsychology", "Is taking out a $130k loan for an MFT program worth it in California?", 2026,
  "negative", "Every reply says no."),
 ("https://forum.thegradcafe.com/topic/53812-cacrep-and-coamfte-accredited-mft-in-california",
  "The GradCafe", "CACREP and COAMFTE accredited MFT in California", 2014, "info",
  "An applicant realising after acceptance that none of their California programmes hold either accreditation."),
 ("https://forum.thegradcafe.com/topic/121887-csun-and-csulb-mft-masters-in-counseling",
  "The GradCafe", "CSUN and CSULB MFT / masters in counseling", 2020, "info",
  "The busiest CSUN and CSULB admissions thread."),
]

# institutions searched for and not found, so the page can say so rather than
# leaving a silent gap
NONE_FOUND = [
 "Phillips Graduate Institute", "Sofia University", "Mount Saint Mary's University",
 "Notre Dame de Namur University", "Loyola Marymount University",
 "John F. Kennedy University", "National University",
 "California State University, Bakersfield", "California State University, Stanislaus",
 "California State University, San Bernardino",
 "California State University, Fresno (Fresno State)",
 "California State University, Sacramento", "California State University, Chico",
 "Sonoma State University", "Cal Poly Humboldt",
 "California State University, Fullerton (University Extension)",
 "California State University, Los Angeles",
 "California State University, Dominguez Hills",
]

DEAD_SUBS = ("r/psychotherapy is now private and r/mft has been banned. Both carried "
             "good California threads; nine of them had to be dropped because they "
             "no longer resolve.")
