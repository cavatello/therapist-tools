# -*- coding: utf-8 -*-
"""The question index — the first thing on the hub.

Indexed by what a therapist actually types, not by what we felt like writing.
Every destination is a page that EXISTS. Nothing here points at an article that
has not been written: the site's whole proposition is that its links are real,
and a hub full of dead promises would break that on the page whose job is to
route people.

(question, category, destination, label, kind)
kind: "tool" renders with a gold wash and means a calculator that runs on your
      own numbers; "read" is a document; "ref" is the reference index below.
"""
QUESTIONS = [
 ("How much will I actually take home?", "Practice",
  "practice-simulator.html", "Practice simulator", "tool"),
 ("Should I incorporate, or stay a sole proprietor?", "Money",
  "therapist-tax-strategy-california.html#structure", "Tax &amp; retirement", "tool"),
 ("What should I be charging?", "Rates",
  "rates.html", "The California rate gap", "read"),
 ("How much of my tax bill is optional?", "Money",
  "therapist-tax-strategy-california.html", "Tax &amp; retirement", "tool"),
 ("Which of my 3,000 hours is holding me up?", "Licensure",
  "amft-3000-hours-california.html", "3,000 hours", "tool"),
 ("Is this job offer any good?", "Licensure",
  "associate-mft-job-advisor.html", "Job advisor", "tool"),
 ("What is one client actually worth to me?", "Practice",
  "grow-your-therapy-practice.html#worth", "Grow your practice", "tool"),
 ("Where are my clients coming from, and which channel is leaking?", "Practice",
  "grow-your-therapy-practice.html#channels", "Grow your practice", "tool"),
 ("Can I see a client who has moved to another state?", "Telehealth",
  "therapist-working-remotely-california.html", "Working remotely", "read"),
 ("What does it cost to live here on this income?", "Practice",
  "therapist-cost-of-living-california.html", "Cost of living", "tool"),
 ("What do I need to renew my licence, and by when?", "Licensure",
  "#g-the-board", "The Board", "ref"),
 ("How do I get on an insurance panel?", "Getting paid",
  "#g-getting-paid", "Getting paid", "ref"),
 ("What insurance and paperwork protects the practice?", "Risk",
  "#g-protecting-the-practice", "Protecting the practice", "ref"),
 ("Where do I list my practice so people find me?", "Getting clients",
  "#g-getting-clients", "Getting clients", "ref"),
]

# The three career stages, and what genuinely exists for each today.
STAGES = [
 ("Pre-licensed", "Accruing hours, choosing a placement", [
   ("associate-mft-job-advisor.html", "Job advisor",
    "What a placement really pays once unpaid notes are counted, and the date all "
    "four BBS gates close.", "tool"),
   ("amft-3000-hours-california.html", "3,000 hours",
    "Four requirements closing at different speeds. It names the one you are "
    "actually waiting on.", "tool"),
   ("#g-the-board", "Licence, fees and exams",
    "Registration through licence is $875 in Board fees since July, down from "
    "$1,750 &mdash; and it reverts in 2030.", "ref"),
 ]),
 ("Newly licensed", "First year on your own licence", [
   ("rates.html", "What California therapists charge",
    "Insurance against private pay, by metro, with the sample sizes admitted "
    "rather than hidden.", "read"),
   ("#g-getting-paid", "Getting on panels",
    "One CAQH profile feeds every application. Anthem quotes 45 days; Evernorth "
    "is closed until September.", "ref"),
   ("practice-simulator.html", "Practice simulator",
    "Put in a rate and a caseload and see what a California practice actually "
    "leaves you.", "tool"),
 ]),
 ("Running a practice", "Structure, tax and growth", [
   ("therapist-tax-strategy-california.html", "Tax &amp; retirement",
    "How much of the bill is optional, and whether a professional corporation is "
    "worth it on your numbers.", "tool"),
   ("grow-your-therapy-practice.html", "Grow your practice",
    "What one client is worth over their whole time with you, and which channel "
    "is quietly losing you the most.", "tool"),
   ("therapist-working-remotely-california.html", "Working remotely",
    "What the Board allows, what it costs you in tax, and what changes if you "
    "leave California.", "read"),
 ]),
]
