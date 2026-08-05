# -*- coding: utf-8 -*-
"""Sample content for the hub mock-ups.

Every article below is one this site could actually write, because the research
behind it is already done and cited somewhere in the project. Nothing here is
filler — if a mock-up is going to be judged on whether the content model works,
the content has to be real enough to judge.

(kicker, title, dek, stat, statlab, minutes, stage)
stage: "pre" = pre-licensed · "new" = newly licensed · "run" = running a practice
"""
ARTICLES = [
 ("Money", "You cannot form an LLC in California. Here is what to do instead.",
  "Every generic small-business guide tells you to form an LLC. Corporations Code "
  "&sect;17701.04 says a California LLC may not render professional services, which "
  "means it is not on the menu for a licensed therapist. The real choice is two things.",
  "&sect;17701.04", "the section that closes the door", 7, "run"),

 ("Money", "SDI, and the $1,248 the S-corp pitch forgets.",
  "The moment your corporation pays you a wage it becomes an employer. State "
  "Disability is 1.3% of the whole salary with no cap since 2024, and a sole "
  "proprietor pays none of it. On a $96,000 salary that is most of the saving.",
  "$1,248", "a year, at a $96,000 salary", 6, "run"),

 ("Licensure", "BBS fees halved in July. What it actually saves you.",
  "Registration through licence used to cost $1,750 in Board fees. Since 1 July 2026 "
  "it is $875, and it goes back up in 2030. The Board&rsquo;s own renewal page still "
  "shows the old table, which is worth knowing before you budget.",
  "$875", "registration through licence, down from $1,750", 4, "pre"),

 ("Licensure", "The 3,000 hours: which gate closes last.",
  "There are four requirements and they close at different speeds. A caseload of "
  "adult individuals finishes the 3,000 and still will not qualify you, because 500 "
  "of your direct hours have to be couples, families or children.",
  "500", "relational hours, of the 3,000", 9, "pre"),

 ("Getting paid", "What credentialing actually takes, panel by panel.",
  "Anthem says 45 days from a complete CAQH file. Blue Shield says 45 to 60. "
  "Evernorth is closed to new applicants until September. The variable nobody "
  "mentions is that every one of them reads the same profile.",
  "45–60", "days, on the panels that publish a number", 11, "new"),

 ("Getting paid", "The Good Faith Estimate rule nobody told you about.",
  "If a client is paying you directly, federal law says they can ask for a written "
  "estimate — and the clock is short. Booked ten days out, you have three business "
  "days. A bill that exceeds it by $400 can be disputed.",
  "$400", "the dispute threshold", 5, "new"),

 ("Rates", "What California therapists actually charge in 2026.",
  "Insurance reimbursement against private pay, by metro, with the sample sizes "
  "admitted rather than hidden. The gap is wider than the averages suggest and it "
  "is widest exactly where the rent is highest.",
  "2.1&times;", "private pay against the panel rate", 14, "run"),

 ("Practice", "What one client is actually worth.",
  "Two numbers multiplied, and almost nobody in private practice knows the answer. "
  "It is the figure that turns every other decision on this page from anxiety into "
  "arithmetic.",
  "$4,800", "a $200 hour over 24 sessions", 6, "run"),

 ("Telehealth", "Your client went to Oregon for a month. Now what?",
  "Licensure follows the client&rsquo;s physical location, not yours. The Board says "
  "so in writing, and California is not in the Counseling Compact — which would not "
  "help an LMFT even if it were.",
  "&sect;2290.5", "consent, and it must be documented", 8, "run"),
]
