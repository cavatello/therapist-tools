# -*- coding: utf-8 -*-
"""Terms of Use and Privacy for therapistsupport / cavatello.github.io.

Written from an audit of what the site ACTUALLY does, not from a template:

  Google Analytics 4  G-BHXXEN4P0X   every page
  Google AdSense      ca-pub-6079968999170000   practice-simulator.html only
  Formspree           /f/xzdnyabp    about, contact, newsletter, rates, tools
  Google Fonts        fonts.googleapis.com / fonts.gstatic.com   every page
  unpkg CDN           React, on practice-simulator.html
  GitHub Pages        hosting

A privacy policy that claims "we collect nothing" while running GA4 and AdSense
is worse than no policy at all - it is a false statement about data practices to
an audience of licensed professionals. So the policy says what is true: the
TOOLS store nothing, and the SITE carries analytics and, on one page, ads.

I am not a lawyer and this is not legal advice. It is a careful, honest draft
built on what the site does, and it is much cheaper for a lawyer to review than
to write from nothing. The user has been told this in as many words.
"""

SITE = "https://cavatello.github.io/therapist-tools"
BRAND = "Therapist Support"
OWNER = "Cavatello"
CONTACT_PAGE = "contact.html"
EFFECTIVE = "2 August 2026"

# ---------------------------------------------------------------- TERMS ----
TERMS_TITLE = "Terms of Use"
TERMS_DECK = (
    "The short version: everything here is arithmetic and reference material, not "
    "advice. It is free, it is provided as-is, and you are responsible for the "
    "decisions you make with it. The longer version, which is the one that governs, "
    "is below.")

TERMS = [
 ("1. Agreement",
  ["By using %s (the &ldquo;Site&rdquo;) you agree to these Terms of Use. If you do "
   "not agree, please do not use the Site." % BRAND,
   "These terms apply to every page, calculator, article and download on the Site."]),

 ("2. No professional advice, and no professional relationship",
  ["<b>Nothing on this Site is tax, legal, accounting, financial, investment, "
   "clinical or business advice.</b> It is general information and arithmetic, "
   "published for education.",
   "Using the Site does not create an accountant&ndash;client, attorney&ndash;client, "
   "adviser&ndash;client or any other professional relationship between you and %s, "
   "and no duty of care arises from your use of it." % OWNER,
   "The Site is not a substitute for advice from a qualified professional who knows "
   "your circumstances. Before acting on anything you read or calculate here, consult "
   "a licensed CPA, enrolled agent, attorney or financial adviser, and where a "
   "licensure question is involved, the California Board of Behavioral Sciences.",
   "%s is not a licensed attorney, certified public accountant, enrolled agent or "
   "registered investment adviser, and does not hold itself out as any of those." % OWNER]),

 ("3. Calculations are illustrations",
  ["The calculators on this Site apply published tax rates, contribution limits and "
   "regulatory thresholds to figures <b>you</b> enter. They make simplifying "
   "assumptions, which are stated on each page.",
   "The output is an illustration of a model, not a computation of your actual "
   "liability, entitlement, licensure date or income. Your real position depends on "
   "facts the Site never asks for &mdash; other household income, deductions, credits, "
   "prior-year positions, filing history, local taxes, and the particular facts of "
   "your practice.",
   "Do not file a return, structure an entity, accept a job, or make any financial "
   "commitment on the basis of a figure produced here."]),

 ("4. Accuracy and currency",
  ["Rates, limits, thresholds and regulations change, sometimes retroactively. "
   "Figures described as applying to a given tax year may be superseded, and some "
   "figures are the best available published estimate rather than a final schedule "
   "&mdash; where that is the case the page says so.",
   "Reasonable care is taken to cite primary sources and to keep them current, but "
   "<b>no representation or warranty is made that any figure, statement, citation or "
   "calculation is accurate, complete or current</b>. Where a citation is given, the "
   "cited source governs, not this Site&rsquo;s summary of it."]),

 ("5. Links to other sites",
  ["The Site links to government agencies, regulators, publishers and other third "
   "parties. Those links are provided for reference and convenience.",
   "%s does not control, endorse, or take responsibility for the content, accuracy, "
   "availability or privacy practices of any external site, and is not liable for "
   "anything you do in reliance on one." % OWNER]),

 ("6. Your responsibilities",
  ["You agree to use the Site lawfully, and not to: interfere with or disrupt it; "
   "attempt to gain unauthorised access to it or to any system connected to it; "
   "scrape, mirror or systematically extract it for commercial redistribution; or "
   "present its output as professional advice to a third party.",
   "You are responsible for verifying anything you rely on, and for the consequences "
   "of decisions you make."]),

 ("7. Intellectual property",
  ["The text, design, code, calculators and original research on the Site are owned "
   "by %s and protected by copyright. You may read, print and share pages for your "
   "own professional use, and you may link to them freely." % OWNER,
   "You may not republish substantial portions, sell access, or present the material "
   "as your own, without written permission. Statutes, regulations and government "
   "publications quoted here remain the property of their issuers."]),

 ("8. No warranty",
  ["<b>The Site is provided &ldquo;as is&rdquo; and &ldquo;as available&rdquo;, "
   "without warranty of any kind</b>, express or implied, including but not limited "
   "to implied warranties of merchantability, fitness for a particular purpose, "
   "accuracy, and non-infringement.",
   "No warranty is given that the Site will be uninterrupted, error-free, secure, or "
   "free of harmful components."]),

 ("9. Limitation of liability",
  ["<b>To the fullest extent permitted by law, %s and anyone associated with the Site "
   "will not be liable for any loss or damage arising out of or in connection with "
   "your use of, or inability to use, the Site</b> &mdash; including without "
   "limitation direct, indirect, incidental, consequential, special, exemplary or "
   "punitive damages, lost profits, lost revenue, lost data, tax penalties, interest, "
   "professional fees, or business interruption &mdash; whether based in contract, "
   "tort (including negligence), strict liability or otherwise, and whether or not "
   "the possibility of such damage was advised." % OWNER,
   "Where liability cannot be excluded as a matter of law, it is limited to the "
   "greater of (a) the amount you paid to use the Site, which is nothing, and "
   "(b) one hundred United States dollars (US$100).",
   "Some jurisdictions do not allow certain exclusions or limitations, so parts of "
   "this section may not apply to you. Nothing in these terms excludes liability "
   "that cannot lawfully be excluded."]),

 ("10. Indemnity",
  ["You agree to indemnify and hold harmless %s from any claim, demand, loss, "
   "liability or expense (including reasonable legal fees) arising out of your use of "
   "the Site, your breach of these terms, or your reliance on, or presentation to "
   "others of, anything produced here." % OWNER]),

 ("11. Changes",
  ["These terms may be updated at any time. The version in force is the one published "
   "on this page, and the effective date is shown at the top. Continuing to use the "
   "Site after a change means you accept the updated terms."]),

 ("12. Governing law",
  ["These terms are governed by the laws of the State of California, without regard "
   "to its conflict-of-laws rules. The exclusive venue for any dispute is the state "
   "or federal courts located in California, and you consent to their jurisdiction."]),

 ("13. Severability, and the whole agreement",
  ["If any provision is held unenforceable, the remainder stays in force and the "
   "unenforceable provision is applied to the maximum extent permitted. A failure to "
   "enforce a provision is not a waiver of it.",
   "These terms, together with the Privacy Policy, are the entire agreement between "
   "you and %s regarding the Site." % OWNER]),

 ("14. Contact",
  ["Questions about these terms, or a correction to something published here, can be "
   "sent through the <a href=\"%s\">contact page</a>. Corrections are genuinely "
   "welcome &mdash; a wrong figure on this Site is a problem worth hearing about."
   % CONTACT_PAGE]),
]

# -------------------------------------------------------------- PRIVACY ----
PRIVACY_TITLE = "Privacy Policy"
PRIVACY_DECK = (
    "The short version: the calculators store nothing &mdash; there is no account and "
    "no server, and what you type stays in your browser and in the address bar. The "
    "site itself does carry Google Analytics, and one page carries ads. All of that is "
    "set out below, including how to switch it off.")

PRIVACY = [
 ("What the tools do not do",
  ["<b>The calculators on this Site have no account, no login and no database.</b> "
   "Figures you enter are held in the page while it is open and written into the "
   "address bar so you can bookmark or share a link. Nothing you type is transmitted "
   "to a server operated by this Site, and nothing is stored after you close the tab.",
   "No browser storage API &mdash; no cookies set by this Site, no localStorage, no "
   "sessionStorage &mdash; is used to hold your figures.",
   "One consequence worth understanding: <b>because your setup lives in the URL, "
   "anyone you send that link to can see the numbers in it.</b> Treat a share link "
   "the way you would treat the figures themselves."]),

 ("What third parties do collect",
  ["The Site uses a small number of third-party services. Each collects data under "
   "its own privacy policy, not this one.",
   "<b>Google Analytics 4</b> (measurement ID G-BHXXEN4P0X) runs on every page and "
   "records pages viewed, approximate location derived from IP address, device and "
   "browser type, and referring site. It is used to understand which tools are "
   "actually useful. It sets cookies.",
   "<b>Google AdSense</b> (publisher ID ca-pub-6079968999170000) runs on the full "
   "simulator page only, and may use cookies or similar technologies to serve and "
   "measure advertising. You can control personalised advertising through Google&rsquo;s "
   "<a href=\"https://myadcenter.google.com/\" target=\"_blank\" rel=\"noopener "
   "noreferrer\">Ad Settings</a>.",
   "<b>Formspree</b> handles the contact and feedback forms. If you send a message, "
   "Formspree processes the content of that message and any email address you supply, "
   "and forwards it by email.",
   "<b>Google Fonts</b> serves the typefaces, which involves a request to Google "
   "carrying your IP address.",
   "<b>GitHub Pages</b> hosts the Site and, like any web host, processes request logs.",
   "<b>unpkg</b> serves a JavaScript library on the full simulator page."]),

 ("What you give voluntarily",
  ["If you subscribe to updates, the email address you supply is used to send those "
   "updates and nothing else. It is not sold, rented, or shared for anyone "
   "else&rsquo;s marketing.",
   "Marketing consent is a separate, unticked box &mdash; subscribing to the update "
   "email does not opt you into anything further, and either can be stopped at any "
   "time.",
   "If you use a contact or feedback form, whatever you put in it is sent by email. "
   "Please do not include client information, protected health information, or "
   "anything else confidential in a form on this Site."]),

 ("Cookies, and switching them off",
  ["This Site sets no cookies of its own. Cookies present are set by Google Analytics "
   "and, on the full simulator page, Google AdSense.",
   "You can block or delete them in your browser settings, use Google&rsquo;s "
   "<a href=\"https://tools.google.com/dlpage/gaoptout\" target=\"_blank\" "
   "rel=\"noopener noreferrer\">Analytics opt-out add-on</a>, or send a Global "
   "Privacy Control signal. Blocking them does not stop any calculator working."]),

 ("California privacy rights",
  ["Most readers of this Site are in California, so this is set out plainly.",
   "Under the California Consumer Privacy Act as amended by the CPRA, California "
   "residents have the right to know what personal information is collected and how "
   "it is used, to request deletion of it, to correct it, and to opt out of its "
   "&ldquo;sale&rdquo; or &ldquo;sharing&rdquo;.",
   "<b>This Site does not sell personal information</b> and does not knowingly share "
   "it for cross-context behavioural advertising other than through the third-party "
   "advertising described above, which you can switch off in Google&rsquo;s Ad "
   "Settings or by blocking cookies.",
   "To exercise any of these rights, use the <a href=\"%s\">contact page</a>. You "
   "will not be treated differently for asking." % CONTACT_PAGE]),

 ("Children",
  ["The Site is intended for practising and pre-licensed mental-health professionals "
   "and is not directed at children. No personal information is knowingly collected "
   "from anyone under 16."]),

 ("Changes",
  ["This policy may be updated. The version in force is the one on this page, and the "
   "effective date is shown at the top."]),

 ("Contact",
  ["Questions about privacy, or a request to exercise a right described above, can be "
   "sent through the <a href=\"%s\">contact page</a>." % CONTACT_PAGE]),
]
