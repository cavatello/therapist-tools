# Spec for a Therapist Support article

You are writing one article for a reference site read by solo California-licensed
therapists (LMFT, LCSW, LPCC) and associates. Output is JSON to the path in your
assignment. It is compiled into HTML by an existing builder, so the shape matters
as much as the prose.

## THE STANDARD

**Every figure traces to a source.** No illustrative numbers, no "roughly",
no "typically around". If the IRS publishes a limit, cite the publication and
the year. If a rate is a computation from published inputs, show the arithmetic
so a reader can check it. If something is not published, say so in the article
rather than estimating it — that sentence is worth more than a made-up number.

**Do the arithmetic nobody else does.** The site's whole headroom is that almost
nobody writing for therapists actually runs the numbers. A worked example on a
concrete, stated income, carried all the way through, beats three paragraphs of
"it depends".

**California specifics are the point.** Federal guidance is everywhere. What is
scarce is what it means for someone whose state adds 9.3%, whose Board is the
BBS, who cannot form an LLC (Cal. Corp. Code §17701.04(e) — never say "LLC" as
an option for a licensed therapist), and who may be an associate rather than
licensed.

**Never overstate.** Where the honest answer is "this saves you less than people
claim", say that. Where a strategy only works above a certain income, name the
income. Where it needs an accountant, say so plainly.

## TONE

Plain, concrete, unhurried, second person. Short sentences carrying real
information. No hype, no "unlock", no "game-changer", no rhetorical questions
stacked for rhythm. Assume an intelligent reader who has not done a tax course.
Translate every term of art the first time it appears, in one clause.

Contractions are fine. British-flavoured spellings are used elsewhere on the
site for ordinary words (*practise* as a verb, *licence* as a noun where it is
not a US legal term) but American forms stay for US legal and tax terms
(*license* in a statute name, *S-corporation*, *Social Security*).

## OUTPUT SCHEMA

```json
{
  "slug": "kebab-case-file-name-without-html",
  "category": "Money | Licensure | Practice",
  "stage": "pre | new | run",
  "minutes": 9,
  "updated": "2026-08-07",
  "title": "The <title> tag. 55–70 chars, the question or the claim.",
  "h1": "The visible headline. May contain ONE <em>...</em> around the sharpest clause.",
  "h1_plain": "Same, with the em tags stripped.",
  "kicker": "California &middot; two or three words",
  "dek": "Two or three sentences under the headline. May contain &mdash; and &rsquo;.",
  "dek_plain": "Same, with entities as plain characters.",
  "figure": ["$4,207", "what it actually saves at $180k of profit"],
  "tool": ["therapist-tax-strategy-california.html",
           "A short imperative line",
           "Two sentences on what the tool does with the reader's own numbers."],
  "sections": [
    ["A section heading in sentence case", [
      ["p", "A paragraph. HTML entities allowed: &mdash; &rsquo; &ldquo; &rdquo; &sect; &times;. Inline <b> and <em> allowed. Footnote references as <sup><a href=\"#s1\">[1]</a></sup>."],
      ["ul", ["A list item.", "Another. <b>Lead with the bold claim</b> then explain."]],
      ["table", ["Header", "Header"], [["cell", "cell"], ["cell", "cell"]]],
      ["quote", "A quotation, in &ldquo;curly quotes&rdquo;.", "Attribution &mdash; see source [2]"],
      ["pull", "$1,248", "The one number the reader should leave with."]
    ]]
  ],
  "sources": [
    {"n": 1, "cite": "IRS Publication 560 (2026), Retirement Plans for Small Business", "url": "https://www.irs.gov/..."}
  ]
}
```

Rules on the blocks:

- **5 to 8 sections.** First section opens on the reader's actual situation, not
  on a definition. Last section is what to do on Monday.
- **At least one `table`** with real figures, and **at least one `pull`** — the
  single number the article exists to deliver.
- Footnote markers `<sup><a href="#s1">[1]</a></sup>` must match a `sources`
  entry with the same `n`. **Every source you cite in the body must be in
  `sources`, and every source in `sources` must be cited in the body.** The
  builder's guard refuses to ship an article that fails either direction — this
  has blocked three articles before, so check it yourself before finishing.
- `figure` is the hero stat: a short value and a caption under 46 characters.
  It renders large, so it must never be an em-dash or a placeholder.
- `tool` points at one of: `practice-simulator.html`,
  `therapist-tax-strategy-california.html`, `amft-3000-hours-california.html`,
  `grow-your-therapy-practice.html`, `therapist-cost-of-living-california.html`,
  `associate-mft-job-advisor.html`.

## LINK TO SIBLINGS

Where it is natural, link in-body to the site's existing pages using plain
relative hrefs. Available and relevant:

`therapist-llc-california.html` (sole prop vs professional corporation) ·
`s-corp-sdi-california-therapist.html` (the SDI cost of an S-corp salary) ·
`cost-of-incorporating-california-therapist.html` ·
`quarterly-estimated-taxes-california-therapist.html` ·
`backdoor-roth-pro-rata-therapist.html` ·
`bbs-fees-california-2026.html` · `become-an-mft-california.html` ·
`amft-3000-hours-california.html` · `therapist-tax-strategy-california.html` ·
`mft-programs-california.html` · `simplepractice-california-therapists.html`

Two or three contextual in-body links is right. Do not add a "related posts"
list — the builder handles that.

## RESEARCH FIRST

Fetch the primary sources before writing a word: IRS publications and the
relevant Internal Revenue Code sections via `law.cornell.edu/uscode/text/26/...`,
the FTB for California treatment, the SSA for anything Social Security, the EDD
for payroll, and the BBS for anything licensure. Verify every 2026 limit — do
not carry a 2025 figure forward. Where the IRS has not yet published a 2026
number, say the year you are quoting.
