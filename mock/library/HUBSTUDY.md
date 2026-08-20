# Resource-library architecture: what the best operators actually do, and what we should do

Research date: 6 August 2026. Every claim below was checked by fetching the page on that date, not from memory. Where a widely-repeated claim about one of these sites is no longer true, it is flagged **[CHANGED]**.

Subject site: `https://therapistsupport.org/` — hub at `/resources.html`, ~80 pages today, several hundred planned across financial calculators, CA licensure, 65 MFT graduate programmes, 16 psychedelic-assisted therapy trainings, insurance/payers, practice growth, and a long tail of SEO articles.

---

## 1. What Help Scout actually does

### 1.1 The browse taxonomy is three items. That is the whole thing.

Every content page on Help Scout carries the same horizontal sub-nav (`<nav class="SubNav PostsNav">`), directly under the site header:

```
Customer Service   |   Growth & Culture   |   Product
```

Verified in the markup of `https://www.helpscout.com/resources/`, `https://articles.helpscout.com/growth/`, and `https://articles.helpscout.com/blog/remote-culture/`. Three links, no more. "Customer Service" points at `/blog/`, i.e. the default category is the blog root itself.

There are **no tags anywhere**. Grep for `href=".../tag/"` or `/tags/` across the resources page, a category page, an article page and a comparison page: zero matches on all four. Help Scout runs categories only, and only three of them.

The top nav "Resources" dropdown (verified on `https://www.helpscout.com/blog/`) exposes the library as five destinations, each with a one-line description of *what kind of thing you get*:

| Label | Description shown |
|---|---|
| Help Scout Blog | "Tips and actionable content" |
| Guides & Tools | "Resources to help you grow" |
| Live Classes | "Free training and demos" |
| Help Center | "Searchable product tutorials" |
| The Supportive | (brand property — newsletter/podcast) |

Note the split: the dropdown is organised by **content type**, and the sub-nav under it is organised by **topic**. Two axes, deliberately not merged.

### 1.2 The card, field by field

Help Scout has exactly two card variants on `https://www.helpscout.com/resources/` (`variant--DEFAULT` ×22, `variant--FEATURED_HORIZONTAL` ×1). Verbatim markup for a default card:

```html
<a class="Card flex-item--1 flex-item--2-M variant--DEFAULT"
   href="/help-desk-staffing-calculator/">
  <figure class="Card--figure"><img alt="Customer Support Hiring Calculator" loading="lazy" …></figure>
  <article>
    <header>
      <span class="overline type--mono-XS color--text-light">Support Toolkit</span>
      <h5>Foundations of Great Service</h5>
    </header>
  </article>
</a>
```

Reading it top to bottom, at descending visual weight:

1. **Image** (16:9, brand illustration, lazy-loaded, responsive `srcSet` up to 1194w). Largest element.
2. **Eyebrow**: category name, monospace, XS, `color--text-light`. Smallest and lightest text on the card.
3. **Title**: `<h5>`. The dominant text element.
4. **Description**: optional. 11 of the 23 cards have `Card--description type--text-L`; the other 12 carry an explicit `Card no-description` class modifier. So description is an editorial choice per card, not a template constant.

The featured card adds, in order: a real `Badge` (mono, size M, `background-color--charcoal-200`) instead of the light eyebrow, `<h4>` instead of `<h5>`, a description, and a "Read more →" `TextLink` with an inline chevron SVG.

**What is NOT on a Help Scout card, anywhere:**
- No reading time. Grep `"min read"` across the resources page, the `/growth/` category page and a full article page: **0, 0, 0**. **[CHANGED]** — "Help Scout shows reading time on its blog cards" is a commonly repeated claim and it is false as of Aug 2026. Ahrefs also shows 0. Only Zapier in this sample shows reading time.
- No publish date on cards.
- No author on cards.
- No content-type label separate from the category. The eyebrow does double duty: "Support Toolkit" is simultaneously the category and the signal that this is a downloadable/tool asset rather than an article.
- No tags, no share counts, no "new" badges.

### 1.3 The eyebrow conflates category and content type, on purpose

On `https://www.helpscout.com/resources/`, cards carry only two eyebrow values: `Support Toolkit` and `Customer Service`. "Support Toolkit" is not one of the three blog categories — it is the *format* bucket. So a single one-word chip resolves "is this an article or a thing I can use?" without a second field.

The calculator on that page — "Customer Support Hiring Calculator" — is carried in the same feed as ebooks and templates, under `Support Toolkit`, but it links to `/help-desk-staffing-calculator/`: **a root-level URL, not under `/resources/` and not under `/blog/`**. Tools get top-level URLs; the resources shelf is a merchandising surface pointing at them.

### 1.4 A category page is not an index — it is a magazine front

`https://articles.helpscout.com/growth/` in order:

1. `<h1>` Growth & Culture
2. One-sentence category definition: "Articles and insights for company founders and leaders on growing a thriving business and building an exceptional company culture."
3. "Most Recent Posts" — **three** posts. One featured (with description), two title-only. Then "View All Posts →".
4. Newsletter capture ("Help Scout Weekly").
5. "Discover the latest in…" — three posts from **each of the other two categories**, each with its own "View More Posts".
6. Support Toolkit cross-sell block.
7. Product CTA, footer.

Three posts. That is the entire category listing. The real archive is one click away at `https://articles.helpscout.com/growth/all-posts/`, which is a **single un-paginated reverse-chronological list of 62 posts** (counted from the markup), cards reduced to *title + author + date*, no images, no descriptions, no categories. Grep that page for `Load more`, `pagination`, `?page`, `rel="next"`: **0 for all**.

This is the most transferable idea on the whole site: **the category page's job is orientation, the archive page's job is completeness, and they are two different pages.**

### 1.5 The bottom of an article: there is no related-posts grid

`https://articles.helpscout.com/blog/remote-culture/`, in order after the body:

1. "Like what you see? Share with a friend." + social icons
2. Author bio cards (photo, name, bio paragraph, links to `/authors/<slug>/`)
3. Product CTA ("Start for Free / Book a Demo")
4. Newsletter block (two newsletters, one form)
5. Footer

**No related articles. No "read next". No tag list. No breadcrumb.** **[CHANGED]** — the standard write-up of Help Scout's blog describes a related-posts module; there isn't one now.

Their entire cluster→cluster internal linking is **contextual, in-body**. Extracting every `<a>` from the article body of that post gives 12 links: 2 author links, 4 social share links, 3 external citations (Lattice, Culture Amp, McKinsey) and **3 internal editorial links** — anchored on natural phrases: "we're still committed to DEI", "retreats", "performance review". That's it. Three in-body internal links in a ~3,500-word post.

Article header carries: title (`h1`), then `Written By <author> & <author> • August 15, 2025`. Date yes, reading time no.

### 1.6 Comparison pages are articles at a special URL

`https://www.helpscout.com/compare/hubspot/` uses the **identical article template**: `<h1>` "Help Scout vs. HubSpot Service Hub: Deep-Dive Comparison", then `Written By Jessica Greene • January 14, 2026`. Same byline component, same footer, same author bio, same absence of breadcrumbs.

Structure of the body, which is the reusable part:

1. One-paragraph framing of who's reading.
2. An **AI-era trust note**, verbatim: *"At Help Scout, we only publish deeply researched, human-written content. If you find our content to be as helpful as we strive to make it be, you can set us as a preferred source in Google so you'll see our content surfaced more often when you're searching."*
3. **"Quick look: Who is Help Scout best for vs. who is HubSpot Service Hub best for?"** — the verdict, stated in the second screen, before any evidence.
4. Repeating pattern for the rest of the page: prose claim → comparison table → prose caveat. Tables are two-column feature grids with prices written out in full ("Included in the Standard plan at $25/user per month") rather than ticks, so a screenshot of one row is self-contained.
5. Explicit fairness notes ("Note: at the time of writing… we opted to use the undiscounted price"), and one concession per section where the competitor wins ("Service Hub does offer one feature you won't find in Help Scout: skill-based routing").

The six comparison pages (`/compare/{zendesk,intercom,freshdesk,hubspot,gorgias,frontapp}/`) appear **only in the footer**, in a column headed "Compare". They are not in the top nav.

### 1.7 SEO plumbing: less than you'd expect

- `https://www.helpscout.com/resources/` — `<meta name="robots" content="index,follow">`, self-canonical, **zero `application/ld+json` blocks**.
- `https://articles.helpscout.com/growth/` — `index,follow`, self-canonical.
- `https://articles.helpscout.com/growth/all-posts/` — `index,follow`, self-canonical.
- `https://www.helpscout.com/compare/hubspot/` — **0 occurrences of `BreadcrumbList`, 0 `application/ld+json` scripts on the entire page.**

So: every listing page is indexable, and there is no structured data and no breadcrumb markup at all. **[CHANGED]** — do not repeat the common claim that Help Scout's content is a showcase of Article/BreadcrumbList schema. It isn't.

### 1.8 **[CHANGED]** The blog now lives on a different hostname

Articles have moved to `articles.helpscout.com`. Verified:

| URL | Result |
|---|---|
| `https://www.helpscout.com/blog/ai-adoption/` | **404** |
| `https://articles.helpscout.com/blog/ai-adoption/` | 200 |
| `https://www.helpscout.com/customer-service-skills/` | **404** |
| `https://articles.helpscout.com/growth/` | 200 |

`https://www.helpscout.com/blog/` still resolves and is the blog front page, but every article card on it links to `articles.helpscout.com`. The in-body editorial links inside articles are still written as `www.helpscout.com/blog/…` and **do 302 across to the subdomain** (checked three: `/blog/committed-to-dei/`, `/performance-management-at-help-scout/`, `/blog/rome-retreat/` — all end at `articles.helpscout.com` with a 200). It works, but it means every internal link in their back catalogue now takes a cross-host hop.

The lesson for us is a negative one: **splitting a content library across hostnames costs you a redirect on every legacy internal link forever.** We are on Cloudflare Pages with no server-side redirects; we cannot afford this move even if we wanted it.

---

## 2. The other exemplars, and why these four

I picked for the specific problems we have — a topic library that also carries calculators and directories — rather than for general fame.

### 2.1 Ahrefs — because it solves "start here" vs. "latest" with two parallel axes

`https://ahrefs.com/blog/` nav exposes **two separate trees**:

- **Topics** (chronological blog): Marketing → General Marketing, Content Marketing, Affiliate Marketing, Paid Marketing, Video Marketing, AI Search. SEO → General SEO, Keyword Research, On-Page SEO, Link Building, Technical SEO, Local SEO, Enterprise SEO. Plus Data & Studies, Product.
- **Guides**: SEO, Keyword Research, On-Page SEO, Link Building, Technical SEO, Local SEO — *the same nouns*, but pointing to `https://ahrefs.com/seo/keyword-research`, not `/blog/category/…`.

`https://ahrefs.com/seo` is `<h1>` "Beginner's Guide to SEO" and is a **numbered ten-chapter curriculum**, not a card grid:

```
01 How Search Engines Work      06 Link Building
02 SEO Basics                   07 Technical SEO
03 Keyword Research             08 Local SEO
04 SEO Content                  09 What AI Means for SEO
05 On-Page SEO                  10 How AI Search Engines Work
```

and each chapter block lists its own sub-lessons inline, e.g. under `/01 How Search Engines Work`: "Search engine basics / How search engines build their indexes / How search engines rank pages / How search engines personalize results". The pillar page links **directly to every leaf**, not to an intermediate index.

Blog card markup (`https://ahrefs.com/blog/`) is text-only — no image at all:

```html
<div class="post-category"><a href="https://ahrefs.com/blog/category/marketing/" rel="tag">General Marketing</a></div>
<h2><a href="…">Vibe Coding for Marketers: A Beginner's Guide</a></h2>
<div class="post-meta"><span>{description}</span><span class="post-author">…</span> {date}</div>
```

Category, title, description, author, date. Cards can carry multiple categories, comma-separated ("Content Marketing, Data & Studies, General SEO"). No reading time, no image, no tags — `rel="tag"` there is WordPress boilerplate on a *category* link.

Two things worth stealing and one worth avoiding:
- **Steal:** free tools ship inside the editorial feed. "Free LLMs.txt Generator" appears in the blog index dated July 24, filed under category `AI Search`, with a description written like an article's. A tool announced as an article gets the editorial distribution; the tool itself lives at its own URL.
- **Steal:** `https://ahrefs.com/free-seo-tools` groups tools by **the same topic vocabulary as the blog categories** — AI Visibility / Keyword Research / Link Building / SERP & Ranking / Other Tools — with a one-line "what it does" under each. Same nouns, different root.
- **Avoid:** `https://ahrefs.com/blog/page/2/` returns 200 but its canonical is `https://ahrefs.com/blog/`. They canonicalise every paginated page back to page 1, which tells Google not to index pages 2–20 while still linking through them. It's a defensible-but-dated choice; Google's own guidance is self-canonical on each page. Don't copy it.

### 2.2 Zapier — because it is the only one carrying a directory of ~9,000 items *and* an editorial blog

`https://zapier.com/blog/` runs a **two-level category tree**, and every parent has an "All articles" child:

```
App picks              → All articles · Best apps · App of the day · App comparisons
Automation with Zapier → All articles · Automation inspiration · Zapier tutorials
                         · Zapier feature guides · Customer stories
Productivity           → All articles · Productivity tips · App tips · App tutorials
Business growth        → All articles · Marketing tips · Business tips
Product & platform     → All articles · Partner case studies · Product news · Platform tips
Company updates        → All articles · Company news · Zapier initiatives
Remote work            → All articles · Remote work tips · How we work at Zapier
Zapier guides          (separate axis, no children)
```

Six or seven parents, 2–5 children each, and a *separate* "Zapier guides" axis — the same pillar/feed split as Ahrefs.

Cards carry **subcategory eyebrow → title → description → `By {author} • {N} min read`**, and in the compact variant **subcategory → title → `{date} | {N} min read`**. Zapier is the only site in this sample using reading time, and it uses it consistently, including on a 28-minute listicle.

The directory is entirely separate: `https://zapier.com/apps`, with its own faceted UI —

- **Sort Apps By**: Most Popular / Premium / Beta / Recently Launched
- **Categories** as a two-level tree, each with an "All X" entry: App Families (Amazon, Facebook, Google, Microsoft, WordPress, Zapier, Zoho), Artificial Intelligence (All AI, AI Agents, AI Assistants, AI Chatbots, …), Business Intelligence, Commerce, Communication, Content & Files, Human Resources, IT Operations, …

And the reconciliation, which is the point: a directory item page like `https://zapier.com/apps/slack/integrations` carries a **category eyebrow** ("Team Chat"), a **tab bar** ("Integrations | Help"), a "Or pick an app to pair with" grid of sibling directory items (each card = *name + its own category*), and — checked in the markup — **outbound links into the editorial blog**: `/blog/what-you-should-automate/`, `/blog/what-are-webhooks/`, `/blog/get-started-with-zapier/`, `/blog/zapier-mcp-guide/` and others.

So the two content shapes meet in exactly two places: an editorial category *about* the directory ("App picks → Best apps / App comparisons"), and contextual editorial links *from* directory pages. The directory never appears in the blog's card feed.

### 2.3 NerdWallet — because it is the closest structural analogue we have: money topics + calculators + product directory + long tail

`https://www.nerdwallet.com/mortgages` — `<h1>` "Mortgages". Its `<h2>` sequence, in page order:

```
1. Mortgage tools              ← calculators and rate tools, FIRST block on the page
2. Explore By:                 ← First-time homebuyers / Homeownership / Buying a home / Selling your home
3. The latest news in mortgages
4. Getting started with a mortgage lender
5. Our Mortgage Partners
6. Do the math
7. Pre-qualification & pre-approval
8. How do mortgage rates work?
9. Leverage your equity
10. Mortgage FAQs
```

Tools first. Then an audience/intent facet. Then a dated feed. Then task clusters, each of which is a mini-hub of 2–4 articles with `by {author}` and a one-line description. Then FAQ.

The mega-nav is the real prize. Every topic in it decomposes into the **same five labelled groups**:

| Group | Example (Auto insurance) |
|---|---|
| Action | "Compare car insurance quotes" |
| Best-of / picks | "Best car insurance companies", "Cheapest car insurance companies" |
| Reviews (directory) | "Car insurance reviews" |
| Calculator | "Auto insurance calculator" |
| Geographic long tail | "Cheapest car insurance by state" → California, Texas, New York, Georgia, Michigan, Washington |
| Escape hatch | "Explore more auto insurance resources" → the topic hub |

And crucially, **calculators are their own named group inside each topic, not a site-wide section**: "Credit card calculators" (Balance transfer savings calculator, Credit card interest calculator), "Banking calculators" (Compound interest, Emergency fund), "Home calculators" (Mortgage, Down payment, How much house can I afford, Closing costs, Cost of living, Amortization, Refinance, Rent vs buy), "Auto loan calculators", "Investing and retirement calculators". Nine to twelve calculators sit under one topic, grouped, with no separate "/calculators" hub in the nav at all.

That is the single most directly applicable finding in this study, and it is what I'd base our recommendation on.

`https://www.nerdwallet.com/mortgages` is self-canonical and carries **no `BreadcrumbList`** either.

### 2.4 Numbeo — because it is the cleanest example of "topic × view-type" for data-shaped content

`https://www.numbeo.com/cost-of-living/`. The nav is a matrix. Each data domain repeats the same set of *views*:

```
Cost of Living   → Comparison · Calculator · Index (Current) · Index · Index by Country · Prices by City · Prices by Country
Property Prices  → Comparison · Index (Current) · Index · Index by Country
Quality of Life  → Comparisons · Index · Index by Country
Crime            → Index · Index by Country
Health Care      → Index · Index by Country
Pollution        → Index · Index by Country
Traffic          → Index · Index by Country
Compensation     → Cost of Living Estimator · Market Basket Comparison by City / by Country ·
                   Global Salary Equivalent Calculator · Relocation Salary Calculator ·
                   Net-To-Gross Salary Converter · Per Diem Allowance Calculator
```

Calculators are a **view type**, not a category. "Cost of Living Calculator", "Taxi Fare Calculator", "Salary Calculator" sit inside the topic they compute, adjacent to the reference tables that feed them.

Numbeo also does the one thing our site already does well and should keep doing loudly: it puts the provenance stat in the nav flow — "9,872,502 prices in 12,824 cities entered by 884,857 contributors."

### 2.5 Ones I checked and am not recommending

- **Stripe Docs** (`https://docs.stripe.com/`) — top nav is task-shaped (Get started, Payments, Revenue, Platforms and marketplaces, Money management, Developer resources, APIs & SDKs, Help). The useful idea is that **reference (`APIs & SDKs`) is a separate top-level peer of guides**, never interleaved. But docs solve a versioned-API problem we don't have, and the sidebar-tree pattern is wrong for a site people arrive at from search rather than from a product.
- **Intercom** — `https://www.intercom.com/resources` **now 302s to `https://www.intercom.com/why-choose-intercom`**. **[CHANGED]** — Intercom's resources hub is gone; they kept only `/blog/`. Advice citing Intercom's resource library as an exemplar is out of date. Worth noting as evidence that a "resources" catch-all shelf is the first thing companies delete when they rationalise.
- **Investopedia** returned HTTP 402 to a plain fetch and **Niche.com** returned 403, so I could not verify anything about them first-hand and have deliberately made no claims about either.

---

## 3. Directory-shaped content: how sites carry both without the directory swamping the articles

Our case: 65 schools + 16 trainings = 81 pages, and today's whole site is ~80 pages. The directory is about to be half the library while answering roughly two reader questions. Three mechanisms, all observed:

**1. Separate root, never in the editorial feed.** Zapier: articles at `/blog/…`, directory at `/apps/…`. The 9,000 app pages appear zero times in the blog's card feed. The blog's card feed is bounded by editorial output; the directory's size is irrelevant to it. Help Scout does the same thing more quietly — `/help-desk-staffing-calculator/` is a root-level tool that is *merchandised* on `/resources/` as one card among 23 but is not part of the blog taxonomy.

**2. The directory gets a facet UI; articles get a card feed.** These are different interaction models and merging them is the mistake. `https://zapier.com/apps` has sort controls (Most Popular / Premium / Beta / Recently Launched) and a two-level category tree — because with 9,000 items you *filter*. `https://zapier.com/blog/` has none of that — because with a few thousand articles you *browse recency and topic*. Numbeo goes further and gives the data its own view vocabulary entirely (Comparison / Calculator / Index / Index by Country).

**3. The bridge is exactly two links, in both directions.**
- *Editorial → directory*: one editorial category that is **about** the directory. Zapier's "App picks → Best apps / App of the day / App comparisons" is a blog category whose entire job is to write about directory items. NerdWallet's equivalent is the "NerdWallet's Picks" group ("Best personal loans", "Best private student loans", "Best Medigap companies") sitting beside "Explore more resources" in the same nav column.
- *Directory → editorial*: contextual links out of directory item pages. Verified on `https://zapier.com/apps/slack/integrations` — it links to `/blog/what-are-webhooks/`, `/blog/what-you-should-automate/`, `/blog/get-started-with-zapier/` and more.

**The rule that falls out:** a directory contributes exactly **one card** to any editorial surface — the card for the directory itself, carrying its count. Individual entries are reachable only through the directory's own facets, its own sitemap, and contextual links. This is what stops 81 pages from drowning 24 questions.

One anti-pattern worth naming: NerdWallet's geographic long tail ("California car insurance", "Texas car insurance", "Best home insurance in New York" …) is directory-shaped content that they *did* promote into the nav, and it is the ugliest part of their nav — six arbitrary states listed, the other 44 invisible. If we ever generate per-county or per-city pages, they go behind a facet, never into a nav list.

---

## 4. The taxonomy question

### 4.1 Verdict: two axes, no tags

Every site studied runs **topic** and **content type** as separate axes and neither runs a general tag vocabulary. Help Scout: 3 topics × {article, Support Toolkit}. Ahrefs: ~15 topics × {blog post, guide chapter, free tool}. Zapier: 7 parents/~25 children × {article, guide, app}. NerdWallet: ~8 verticals × {best-of, review, calculator, how-to, news}. Numbeo: 7 data domains × {comparison, calculator, index, index-by-country}.

**Do not add tags.** They fail in a specific, predictable way on a library this size: a tag vocabulary with no cardinality limit grows one term per article, tag pages have 1–3 items each, and you end up with 200 thin indexable pages that dilute the topics. None of the five reference sites has them. If you need cross-cutting retrieval later, that is what search is for.

### 4.2 The smallest taxonomy that holds our seven content areas

**Five topics.** Not seven — two of the seven stated areas are formats, not topics, and one is a long tail that has to distribute across the others rather than getting a bucket of its own.

| # | Topic | Slug | Absorbs |
|---|---|---|---|
| 1 | **Money** | `/money/` | practice take-home, entity choice (sole prop vs professional corp), S-corp/SDI, estimated taxes, retirement, backdoor Roth, cost of incorporating, cost of living |
| 2 | **Licensure** | `/licensure/` | becoming an MFT, BBS fees, exams, 3,000 hours, supervision, associates/AMFT, **+ the graduate programmes directory** |
| 3 | **Getting paid** | `/getting-paid/` | insurance panels, credentialing, CAQH/NPI, Medicare/Medi-Cal, Headway/Alma/Grow, rates and the rate gap, superbills, Good Faith Estimates |
| 4 | **Running a practice** | `/practice/` | growth, client value, funnel, client directories, telehealth and working remotely, malpractice/HIPAA/risk, business admin |
| 5 | **Training** | `/training/` | CE requirements, specialisation, **+ the psychedelic-assisted therapy trainings directory** |

The "long tail of SEO articles" is **not** a sixth bucket. Every article gets exactly one of these five as its primary topic, or it doesn't get published. If a piece genuinely doesn't fit any of the five, that is the signal that either the piece is off-strategy or the taxonomy needs a sixth item — and adding a sixth should be a considered decision, not a default.

Five is deliberately near the low end. Help Scout runs three. The cost of too few is that a topic hub gets crowded, and the fix is cheap (add an `<h2>` cluster inside it). The cost of too many is that hubs go thin and the reader has to make an unforced choice, and the fix is expensive (a taxonomy migration with redirects, on a host that can't issue a 301).

The current hub already carries a proto-taxonomy of **ten** topic pills — Practice, Money, Rates, Licensure, Telehealth, Getting paid, Risk, Getting clients, Training, About. That is too many and it overlaps: *Rates* is *Getting paid*; *Getting clients* and *Risk* are both *Running a practice*; *Telehealth* splits (scope-of-practice → Licensure, run-from-anywhere → Running a practice); *About* is not a topic at all. Collapse ten to five.

### 4.3 Content type: a separate axis, five values, used as a chip not a tree

| Format | What it promises | Where it lives |
|---|---|---|
| **Calculator** | runs on numbers you type | its own root-level URL, listed on its topic hub |
| **Guide** | the long, complete, evergreen answer — the pillar | topic hub, position 1 in its cluster |
| **Answer** | one question, short, dated, sourced — the long tail | topic hub, in a cluster list |
| **Directory** | a set you filter (65 schools, 16 trainings) | its own root, one card on its topic hub |
| **Reference** | checked outbound links to the Board, payers, statutes | a section on each topic hub |

Five formats, and **format is a chip on a card, never a browse tree**, with exactly one exception: calculators. See below.

### 4.4 Where calculators sit

Two live models, and they disagree:

- **NerdWallet**: calculators are a *named group inside each topic* ("Home calculators", "Banking calculators", "Auto loan calculators"), and there is no site-wide calculators section in the nav.
- **Ahrefs**: tools get a single dedicated root (`https://ahrefs.com/free-seo-tools`) grouped by *the same topic nouns as the blog*.

Both are right for their businesses, and the tiebreaker is what the site *is*. For Ahrefs, free tools are lead-gen for a paid product — one shopfront makes sense. For NerdWallet, the calculator is a step inside a money task, so it belongs beside the task.

**We are neither, and we should do both, in this precedence:**

1. **Calculators live on their topic hub, in a group at the top of it** — NerdWallet's placement, and its "Mortgage tools" is literally the first `<h2>` on `https://www.nerdwallet.com/mortgages`. A therapist asking "should I incorporate?" wants the tax calculator adjacent to the two statutes, not on a different page.
2. **Plus one flat `/calculators/` index** as a format shortcut, because six calculators is a *product*, it is the site's strongest differentiator, and it is what someone returns for. This is the single exception to "format is not a browse tree" and it earns the exception because the format itself is the reason to come back.
3. **Calculators are never a topic.** There is no "Calculators" bucket in the five-topic list. Every calculator has a topic: take-home → Money, job advisor → Licensure, client value → Running a practice.

So the answer to "same taxonomy or separate axis" is: **same topic vocabulary, separate axis, and one privileged index page.**

Directories get the same treatment with one difference: they earn a root (`/programmes/`, `/trainings/`) because they have internal facets, but they get **no** cross-directory index page — two directories is not a shelf.

---

## 5. Browse paths: how many, and what to cut

Ten candidate entry paths. Verdict on each.

### Keep — four

**1. Topic (5 hubs).** The spine. Every page belongs to exactly one, every page links up to it, both nav and breadcrumb express it. Non-negotiable; it is the only path that scales linearly with page count.

**2. The question index.** Our best asset. Keep it — see §9 for the role change.

**3. Calculators.** One flat index. Earned by being the product.

**4. "What changed, and when."** A dated feed of *number* changes, not of posts. The current hub's "Why the dates matter" block is the seed of this and it is the most distinctive thing on the page: *"BBS fees halved on 1 July 2026 and revert in 2030. One large insurance panel is closed to new applicants until September."* Nobody else in the sample has an equivalent — the closest is Help Scout's `updates.helpscout.com`, which is product changelog, not domain changelog. On a site whose promise is "checked", a visible change log **is** the proof of the promise, and it doubles as the newsletter's content. This is a differentiator worth building rather than a nav item worth adding.

### Demote — two

**5. Audience stage** (Pre-licensed / Newly licensed / Established). Currently a full block, "Where you are right now", three cards each. The reasoning behind it is right — an associate and an eight-year practitioner need different pages. But as a *taxonomy* it is a trap: every page would need an audience assignment, most pages serve two of the three, and you'd end up maintaining a third axis for a benefit you can get from three hand-written cards. **Keep as exactly one hand-curated block of three cards, on the home page, and delete it from the hub.** Do not let it become a facet, do not build `/for-associates/` unless and until it is a real pillar page with its own body copy.

**6. Search.** Earns its place at 300 pages, not at 80. Header only, never a body element on the hub — a search box in the middle of a hub page is a confession that the browse structure failed. Ship it when the question index can no longer be exhaustive (see §6), index page titles **plus the question phrasings**, and nothing else.

### Cut — four

**7. Tags.** No. §4.1.

**8. A chronological "latest posts" feed.** This is the one thing every exemplar has that we should not copy. Help Scout, Ahrefs, Zapier and NerdWallet all run recency feeds because they are publishers with a subscription relationship and a reason to signal "we're alive". We are a *reference*. A therapist looking up the CE hour count does not care what was published on Tuesday. Recency for us is expressed by the **"checked" date on the thing they're reading**, which is more useful and cheaper to maintain. Replace the recency feed with the change log (path 4).

**9. Alphabetical / A–Z index.** Only ever useful for a glossary. We don't have one. If we build one, it gets its own page and stays there.

**10. Editor's picks / "featured".** Help Scout has one ("Editor's Picks" on `https://www.helpscout.com/blog/`, three items). It exists because their catalogue is so large that curation is the only remaining signal. At 300 pages our curation surface is the question index itself, which is already hand-picked. A second curated block competes with it and confuses the reader about which list is authoritative. Cut.

**Net: four site-wide browse paths.** Topic, questions, calculators, changes. Plus in-directory facets, which are local to `/programmes/` and `/trainings/` and never appear elsewhere.

---

## 6. The card

### 6.1 Fields, in render order

```
┌────────────────────────────────────────────────────────┐
│ CALCULATOR                                  Aug 2026   │   ← 1. format chip   5. checked stamp
│ How much will I actually take home?                    │   ← 2. title (question form)
│ Rate and caseload in, a real net figure out.           │   ← 3. one-line outcome
│ $875 in Board fees                                     │   ← 4. the number (optional)
└────────────────────────────────────────────────────────┘
```

**1. Format chip** — `Calculator` / `Guide` / `Answer` / `Directory` / `Reference`. First and visually distinct (the shaded-row device already on the hub is the right instinct, generalised). *Rationale:* on this site the format gap is enormous — one card leads to something that computes your tax, the next to a paragraph. That expectation gap is worth more than the topic, because the card is nearly always already sitting under a topic heading. Help Scout's single eyebrow proves one chip is enough; NerdWallet proves that separating "calculator" from "guide" is what readers actually navigate by.

**2. Title, in question form where a question exists.** The current hub already does this and it is the best thing about it. It also happens to be exactly what retrieval — Google and AI assistants alike — matches against.

**3. One line of *outcome*, not summary.** 8–14 words. "Rate and caseload in, a real net figure out" beats "A calculator that models therapist income." Help Scout makes this optional (11 of 23 cards have it, the rest carry an explicit `Card no-description` class). **Make it mandatory.** Optional descriptions produce ragged grids and let weak entries hide.

**4. One hard number, where a real one exists.** `$875 in Board fees` · `65 schools` · `16 programmes` · `72 checked links` · `1.3% SDI, no cap`. *Rationale:* this site's whole voice is numeric, and a number is the highest information per pixel available. Numbeo does this in its nav ("9,872,502 prices in 12,824 cities"); the current hub already does it in prose ("The $1,248 the S-corp pitch forgets"). Optional — do not invent one to fill the slot.

**5. "Checked {Mon YYYY}"** — small, right-aligned, muted. Only on cards whose content can go stale (anything citing a fee, a limit, a rate, a panel status). *Rationale:* this is the site's entire competitive claim, and none of the five exemplars does it. Help Scout, Ahrefs, Zapier and NerdWallet all show *publish* dates, which on evergreen reference content actively hurt — a correct page dated 2024 looks worse than a wrong page dated last week. A "checked" stamp inverts that.

### 6.2 What NOT to include, and why

- **Reading time.** Verified absent from Help Scout (0 occurrences across resources, category, and article pages) and Ahrefs (0). Only Zapier uses it. It is a scroll-commitment signal for feed browsing; a reference reader wants the fee, not a time budget. Adding it would also require maintaining it on 300 pages.
- **Publish date.** See above. Ship "checked", not "published".
- **Author.** One author. Help Scout runs bylines because they have a newsroom; it costs them a component on every card and buys us nothing.
- **Thumbnail image.** The strongest single recommendation in this section. `https://www.helpscout.com/resources/` carries 23 `Card--figure` images, each with a responsive `srcSet` up to 1194w, and every one of them is abstract brand art carrying zero information about the page behind it — the card is 60% image and 40% content. `https://ahrefs.com/blog/` has **no images on its index at all** and is denser, faster, and more scannable. For a reference library, an image is pure cost: bytes, layout, and an editorial task per page.
- **A topic pill *and* a format chip.** Redundant when the card already sits under a topic `<h2>`. One chip. Only the standalone question index — which is deliberately cross-topic — gets both, and there the topic is the secondary, muted one.
- **Auto-generated excerpt.** If the one-liner isn't hand-written it isn't worth the row.
- **Tags, share counts, view counts, "New" badges.** New badges in particular: nobody ever removes them.

### 6.3 One list variant, not five

Help Scout's `/resources/` page has 2 card variants; its `/growth/` category page has 10 (`DEFAULT`, `FEATURED_HORIZONTAL`, `HORIZONTAL`, `L`, `LARGE`, `LARGE_WITH_DESCRIPTION`, `FEATURED`, `WITH_FEATURED`, `OUTLINE`, `COMPACT`). That's a design-system smell — a component that grew a variant per layout accident. Ship **two**: the card above, and a compact one-line row (format chip + title + checked stamp) for archives and long lists, which is exactly what `https://articles.helpscout.com/growth/all-posts/` degrades to for its 62 items.

---

## 7. What breaks at 300 pages

Eight failure modes of the flat question index, each with the exemplar's counter-move.

**1. The exhaustiveness promise silently becomes a lie.** This is the worst one and it is specific to *this* hub. At 24 rows, "Everything in one place… indexed by the question you arrived with" is verifiably true, and the reader can see that it's true. At 300 pages you can only show a subset, and the reader cannot distinguish "we don't cover that" from "it's not on this screen". A hub whose selling point is completeness cannot become a sampler without saying so. **Counter-move:** Help Scout separates the two claims onto two pages — `https://articles.helpscout.com/growth/` shows 3 posts and makes no completeness claim; `https://articles.helpscout.com/growth/all-posts/` shows all 62 and makes nothing but a completeness claim.

**2. Linear scan collapses.** 24 rows is ~1.5 screens. 300 rows is ~15 desktop screens and far worse on a phone, where the row layout degrades hardest. There is no scan strategy for 300 undifferentiated rows. **Counter-move:** everyone caps the top-level listing hard — Help Scout at 3 per category, Ahrefs at ~6 before pagination, NerdWallet at 2–4 per task cluster.

**3. Question collision.** "What should I be charging?" / "What do therapists charge in Los Angeles?" / "How do I raise my rates?" / "What does insurance pay per session?" are four rows that look like near-duplicates in a flat list, and disambiguating each one editorially is unbounded work. **Counter-move:** Zapier's two-level tree gives near-duplicates different *parents* ("App comparisons" vs "Best apps"), so proximity does the disambiguating.

**4. Directory swamp.** 81 directory pages against ~24 questions. Include them and they drown everything; exclude them and 81 pages are unreachable from the hub, which starves them of internal links. **Counter-move:** §3 — separate root, one card, facets inside.

**5. Nowhere to put a page.** Under a question index, a page only exists if someone writes a question row for it. Long-tail SEO articles by definition arrive faster than curated rows, so they become orphans reachable only from the sitemap. **Counter-move:** Zapier's "All articles" child under every parent category, and Help Scout's `/all-posts/` — a guaranteed home for anything not featured.

**6. Maintenance is O(n) and lands on one person.** Every new page requires a hand edit to the hub. At 300 pages that stops happening, and the hub drifts — which for a site whose pitch is "every link checked" is fatal in a way it wouldn't be for a blog. **Counter-move:** all four sites generate their listings from content metadata and hand-curate only the top slot. The question index must become *generated from a `question:` field on each page*, with a hand-picked top 20, not a hand-maintained list of 300.

**7. Link equity flattens.** One hub linking to 300 pages passes each ~1/300 of its authority and communicates no topical grouping. **Counter-move:** hub → 5 topic hubs → clusters concentrates it, and gives Google a topical structure to read. Ahrefs' `https://ahrefs.com/seo` is the purest form: the pillar links to all ten chapters *and* every sub-lesson under each.

**8. There is no orientation for the reader who doesn't have a question.** A question index only works if you arrive with the question. Roughly half of a reference site's readers arrive with a *situation* ("I just passed my exam"). **Counter-move:** Ahrefs' `https://ahrefs.com/seo` numbered curriculum, and the existing "Where you are right now" block — which is already the right answer and just needs to move to the home page.

---

## 8. SEO structure, as actually implemented

### 8.1 Hub → cluster

Two live patterns:

- **Exhaustive**: `https://ahrefs.com/seo` links to all 10 chapters *and* names each chapter's 3–4 sub-lessons on the pillar page itself. Maximum link equity distribution, and the pillar reads as a table of contents.
- **Curated + escape hatch**: `https://articles.helpscout.com/growth/` links to 3 posts and to `/growth/all-posts/`, which then links to all 62. Two hops to the tail.

**Take Ahrefs' pattern for our five topic hubs** (we have hundreds, not thousands, of pages — a topic hub can afford to name 40–60 leaves), and **Help Scout's pattern for the directories** (65 schools should not be enumerated on the Licensure hub).

### 8.2 Cluster → hub

This is where the exemplars will surprise you. `https://articles.helpscout.com/blog/remote-culture/` has:
- no breadcrumb,
- no related-posts module,
- no tag list,
- **3 in-body internal editorial links in a ~3,500-word article**, anchored on natural phrases.

Its only structural link back up is the 3-item `SubNav` in the header, present on every page. That's it. `https://www.helpscout.com/compare/hubspot/` is the same. So the widely-repeated "pillar-cluster requires every cluster page to link back to the pillar with an exact-match anchor" is **not** what Help Scout does.

They can get away with it because they have three categories, a persistent 3-item sub-nav that *is* the up-link on every page, and enormous domain authority. **We have none of those.** So: implement the up-link properly — a breadcrumb on every page, a "More on {Topic} →" link at the foot of every article, and in-body contextual links, which the site already writes well (the existing hub prose links naturally to `therapist-tax-strategy-california.html#structure` and `grow-your-therapy-practice.html#channels`).

### 8.3 Breadcrumbs

Checked for `BreadcrumbList` JSON-LD:

| Page | Result |
|---|---|
| `https://www.helpscout.com/compare/hubspot/` | 0 — and 0 `application/ld+json` blocks of any kind |
| `https://www.nerdwallet.com/mortgages` | 0 |
| `https://ahrefs.com/blog/` | 0 |

**[CHANGED]** — the claim that these content operations are structured-data showcases is false. They ship none of it on the pages checked.

Ship breadcrumbs anyway, both visible and as `BreadcrumbList`. Our reasons are the ones they don't have: we will have three-level paths (`Home › Licensure › Programmes › Pepperdine`), we are a small domain that needs every structural signal, and directory item pages are worthless in a SERP without a visible parent.

### 8.4 URL shape

| Site | Articles | Pillar/guide | Tool | Directory |
|---|---|---|---|---|
| Help Scout | `articles.helpscout.com/blog/<slug>/` | — | `www.helpscout.com/<tool-slug>/` | — |
| Ahrefs | `/blog/<slug>/`, categories at `/blog/category/<cat>/` | `/seo/<chapter>` | `/free-seo-tools` | — |
| Zapier | `/blog/<slug>/` | `/blog/<cat>/<subcat>/` | — | `/apps/<app>/integrations` |
| NerdWallet | `/article/<topic>/<slug>` | `/<topic>` | `/<topic>/…-calculator` | `/reviews/…`, `/best/…` |

Every one of them uses **directories, not a flat namespace**. We currently do not: `become-an-mft-california.html`, `mft-programs-california.html`, `s-corp-sdi-california-therapist.html` all sit at the root, and the 65 school pages are queued to land at the root too (`alliant-international-university-mft.html`, `azusa-pacific-university-mft.html`, … — from `school_slugs.json`). **Fix this before generating them**, not after. Once 65 school pages are indexed at the root, moving them costs 65 redirect stubs on a host that cannot issue a 301.

Proposed shape (Cloudflare Pages serves subfolders fine — verified, `/css/…` resolves 200):

```
/                                  home
/resources.html                    hub          (keep the URL — it has history)
/questions.html                    full question index
/calculators/                      format index
/money/  /licensure/  /getting-paid/  /practice/  /training/     topic hubs
/money/s-corp-sdi/                 article
/programmes/                       directory     (65 schools)
/programmes/pepperdine-university/ directory item
/trainings/                        directory     (16 programmes)
/changes/                          the change log
```

For anything already indexed, use the existing `build_redirect.py` recipe — `rel=canonical` + 0s meta refresh + `location.replace()` + a real visible link, no `noindex`. That file already documents why each of the four parts is needed; reuse it rather than reinventing it.

### 8.5 Pagination

Nobody infinite-scrolls. Verified:

- **Help Scout** does not paginate at all: `https://articles.helpscout.com/growth/all-posts/` puts all 62 posts on one page, and greps for `Load more`, `pagination`, `?page`, `rel="next"` return 0.
- **Ahrefs** paginates with real numbered URLs (`/blog/page/2/`, links out to page 20) but sets the canonical of `/blog/page/2/` to `https://ahrefs.com/blog/`. Don't copy the canonical part.
- **Zapier** uses a "See all articles" link out of the curated front.

**Recommendation: don't paginate.** A single long archive page per topic, compact one-line rows, is what Help Scout does at 62 items and it is simpler, better for crawling, and better for Ctrl-F — which is how a reference audience actually uses an archive. Revisit only if a single topic exceeds ~150 items. Directory pages are the exception: they get filters, and filters replace pagination.

### 8.6 Avoiding thin category pages

The mechanism in all four cases is that **the category page has hand-written content of its own**, so it is never an auto-generated list:

- Help Scout: an `<h1>`, a one-sentence category definition ("Articles and insights for company founders and leaders on growing a thriving business…"), 3 curated posts, a newsletter block, and 3+3 cross-links into the other two categories. The page would still be worth reading with the listing removed.
- Ahrefs: every guide on `https://ahrefs.com/seo` carries a hand-written one-line promise ("Improve clickthrough rates with enticing title tags"), so the pillar is 40 unique sentences, not 40 titles.
- NerdWallet: `https://www.nerdwallet.com/mortgages` opens with tools and an intent facet, and each cluster (`Do the math`, `Pre-qualification & pre-approval`) has its own prose.

**For us:** every topic hub gets an opening paragraph in the site's existing voice, its calculators, its reference links, and its clusters. If a topic hub can't sustain ~300 words of hand-written orientation, that topic shouldn't exist.

### 8.7 Should category pages be indexable?

Yes, with one exception. Verified: all three Help Scout listing pages are `index,follow` with self-canonicals — `/resources/`, `/growth/`, and even the 62-item `/growth/all-posts/`.

- **Topic hubs (`/money/` etc.): index, and treat as landing pages.** They target the head term ("california therapist taxes") and should be written to win it.
- **`/calculators/`, `/programmes/`, `/trainings/`, `/questions.html`: index.** Each targets a real query with real intent.
- **Directory facet permutations (`/programmes/?online=1&region=bay-area`): noindex, or don't generate URLs for them at all.** This is where a directory generates infinite thin pages, and it is the failure mode Zapier avoids by keeping facets client-side on `/apps`.

---

## 9. Recommendation for our hub

### 9.1 The principle

`/resources.html` stops being *the library* and becomes *the front door*. Its job is to get a reader into one of five topic hubs, one of six calculators, or one of two directories within one screen and one click. Everything exhaustive moves down a level.

### 9.2 What the page contains, in order

1. **Promise + change strip.** One sentence, then the dated "what moved" line. Keep the existing copy — *"BBS fees halved on 1 July 2026 and revert in 2030. One large insurance panel is closed to new applicants until September."* — and link it to `/changes/`. This block is the site's differentiator and belongs above everything.
2. **Calculators.** Six cards. First, because they are the product, and because NerdWallet puts "Mortgage tools" as the literal first `<h2>` on its topic hub.
3. **The question index — top 20, explicitly framed as a selection.** "The twenty questions people arrive with" + "All 140 questions →". Framing it as a selection is what keeps the completeness promise honest (§7.1).
4. **Five topic cards.** Each with a page count and three sample titles. This is the block that does the actual architectural work and it is currently missing.
5. **Two directory cards.** "65 California MFT programmes" / "16 psychedelic-assisted therapy trainings", each with its top facets as entry links (region, online/in-person, cost band).
6. **Reference: one card, not 72 rows.** "72 checked links to the Board, the payers, the statutes →" pointing at a reference index, with the 72 links themselves redistributed onto the five topic hubs (the Board group → `/licensure/`, panels → `/getting-paid/`, HIPAA/malpractice → `/practice/`, entity/tax → `/money/`).
7. **Newsletter.** Keep, keep it last-but-one. Every exemplar does this.

### 9.3 What moves off the hub

| Currently on `/resources.html` | Moves to |
|---|---|
| All 72 reference links, in 8 groups | The five topic hubs, split by topic; one index page |
| "Notes" (3 short pieces) | `/money/` and `/licensure/` clusters |
| "Field Notes" (2 long reads) | Promoted to Guides on `/getting-paid/` and `/practice/` |
| "Where you are right now" (3 audience columns) | Home page, as three cards |
| "Where numbers come from" (7 data sources) | A `/methodology` page, linked from every calculator |
| Questions 21–140 | `/questions.html` |

Estimated hub length after: roughly one third of today's, and it stays that length at 300 pages.

### 9.4 Wireframe

```
┌───────────────────────────────────────────────────────────────────────┐
│  Therapist Support        Tools ▾   Learn ▾   About ▾        [search] │
└───────────────────────────────────────────────────────────────────────┘
   Home › Resources                                        ← breadcrumb

   ╔═══════════════════════════════════════════════════════════════════╗
   ║ Free tools for California therapists, and the rules behind them.  ║
   ║ Every figure computed or cited. Nothing saved, nothing sent.      ║
   ║                                                                   ║
   ║ ▸ WHAT MOVED  BBS fees halved 1 Jul 2026, revert 2030 · Evernorth ║
   ║   closed to new applicants until Sep 2026     What changed →      ║
   ╚═══════════════════════════════════════════════════════════════════╝

   RUN YOUR OWN NUMBERS                                6 calculators
   ┌────────────────┐┌────────────────┐┌────────────────┐
   │ CALCULATOR     ││ CALCULATOR     ││ CALCULATOR     │
   │ What will I    ││ Should I incor-││ What is one    │
   │ take home?     ││ porate?        ││ client worth?  │
   │ Rate + caseload││ Sole prop vs   ││ Rate × lifetime│
   │ in, net out.   ││ prof. corp, on ││ sessions, with │
   │                ││ your numbers.  ││ channel leaks. │
   │      Aug 2026  ││      Aug 2026  ││      Aug 2026  │
   └────────────────┘└────────────────┘└────────────────┘
   ┌────────────────┐┌────────────────┐┌────────────────┐
   │ Job advisor    ││ 3,000 hours    ││ Cost of living │
   └────────────────┘└────────────────┘└────────────────┘

   START WITH THE QUESTION YOU CAME WITH        20 of 140 · all →
   ┌───────────────────────────────────────────────────────────────┐
   │ ▨ CALCULATOR  How much will I actually take home?          →  │  ← shaded
   │ □ GUIDE       What should I be charging?                   →  │
   │ □ ANSWER      Can I set my practice up as an LLC?          →  │
   │ ▨ CALCULATOR  Is this job offer any good?                  →  │
   │ □ DIRECTORY   Which graduate programme should I go to?     →  │
   │   …                                                           │
   └───────────────────────────────────────────────────────────────┘
                            [ All 140 questions → ]

   BROWSE BY TOPIC
   ┌─────────────────────────┐┌─────────────────────────┐
   │ MONEY               41  ││ LICENSURE           68  │
   │ Tax, entity, retirement ││ The Board, hours, exams │
   │ · The $1,248 SDI gap    ││ · Becoming an MFT       │
   │ · You cannot use an LLC ││ · BBS fees, 2026        │
   │ · Estimated taxes       ││ · 65 CA programmes      │
   └─────────────────────────┘└─────────────────────────┘
   ┌─────────────────────────┐┌─────────────────────────┐
   │ GETTING PAID        33  ││ RUNNING A PRACTICE  29  │
   └─────────────────────────┘└─────────────────────────┘
   ┌─────────────────────────┐
   │ TRAINING            22  │
   └─────────────────────────┘

   DIRECTORIES
   ┌──────────────────────────────┐┌──────────────────────────────┐
   │ DIRECTORY                    ││ DIRECTORY                    │
   │ 65 California MFT programmes ││ 16 psychedelic trainings     │
   │ Cost, format, COAMFTE, and   ││ What each certificate does   │
   │ what students say.           ││ and does not let you do.     │
   │ Bay Area · SoCal · Online    ││ In person · Online · Under $10k│
   │                    Aug 2026  ││                    Aug 2026  │
   └──────────────────────────────┘└──────────────────────────────┘

   ┌───────────────────────────────────────────────────────────────┐
   │ REFERENCE   72 checked links — the Board, the payers,      →  │
   │ the statutes, the directories, with what each costs.          │
   └───────────────────────────────────────────────────────────────┘

   ┌ One email a month. What changed in the numbers. ─── [Sign up] ┐
   └───────────────────────────────────────────────────────────────┘
```

And the topic hub one level down, which is where the volume actually goes:

```
   Home › Money

   MONEY                                                41 pages
   [ two or three paragraphs of hand-written orientation — what a
     California therapist actually has to decide about money, in order ]

   TOOLS          [take-home] [tax & retirement] [cost of living]
   START HERE     GUIDE  Sole proprietor or professional corporation →
   ── Entity and structure ──────────────────────  8 pages
      ANSWER  Can I use an LLC?                    Aug 2026 →
      ANSWER  What does incorporating cost?        Aug 2026 →
      …
   ── Tax ───────────────────────────────────────  14 pages
   ── Retirement ────────────────────────────────  9 pages
   ── Reference: entity, tax, retirement ────────  17 checked links
```

---

## 10. What to keep: the question index

**It should survive, and it is the best idea on the current site. It should stop being the index.**

The reasoning, honestly:

**Why it works.** Plain questions match how the audience actually searches, they match how AI assistants retrieve, and they are self-evidently written by someone who knows the domain — "Which of my 3,000 hours is holding me up?" is a question only a person who has done this asks. That is trust signalling that no card grid achieves. None of the five sites studied has anything as good; the nearest is NerdWallet's "Mortgage FAQs" block, buried tenth on the page.

**Why it can't stay the index.** §7.1. Its power comes entirely from being *complete and short at the same time*, and at 300 pages those two properties become mutually exclusive. The moment it is a subset presented as a whole, it converts the site's central promise into a small lie — and this hub's copy makes that promise explicitly ("Everything in one place… indexed by the question you arrived with").

**The three roles it should take instead:**

1. **The spine of the hub**, capped at ~20, framed as a selection with a visible count ("20 of 140") and a link to the full set. Framing is the whole fix — a curated selection that says it is one is honest; the same list unlabelled is not.
2. **A page of its own** at `/questions.html`, exhaustive, generated from a `question:` field on every page, grouped by topic, one compact row each. This is the Help Scout `/all-posts/` move: completeness gets its own page and its own contract with the reader.
3. **A block inside every topic hub** — "Questions people ask about money" — which is where it does the most SEO work, because a hub full of literal questions is what both Google's FAQ surfaces and AI assistants match on.

**The operational change that makes all three work:** the question stops being a row in a hand-maintained hub file and becomes **a field on the page itself**. Every page declares its primary question, its topic (one of five), its format (one of five), and its checked date. Every list on the site — the hub's top 20, `/questions.html`, the topic hub's question block, the calculators index — is then generated from that. It is the only version of this that still exists at 300 pages.

One extension worth taking from Help Scout: their comparison pages open with the verdict ("Quick look: who is X best for vs. who is Y best for") before any evidence. Our question rows are questions; the pages behind them should open with the **one-sentence answer**, then the working. On a reference site, that pairing — question in the index, answer in the first line, arithmetic below — is worth more than any amount of taxonomy.

---

## Appendix: every URL fetched, 6 Aug 2026

| URL | Status | What it evidenced |
|---|---|---|
| `https://www.helpscout.com/blog/` | 200 | 3-category taxonomy; nav "Resources" dropdown; Editor's Picks |
| `https://www.helpscout.com/resources/` | 200 | Card variants and fields; calculator in the editorial feed; no pagination; `index,follow`; 0 JSON-LD |
| `https://www.helpscout.com/compare/hubspot/` | 200 | Comparison = article template; verdict-first; 0 `BreadcrumbList`; compare links footer-only |
| `https://articles.helpscout.com/growth/` | 200 | Category page = magazine front, 3 posts; `index,follow`; self-canonical |
| `https://articles.helpscout.com/growth/all-posts/` | 200 | 62 posts, one page, no pagination; title+author+date rows |
| `https://articles.helpscout.com/blog/remote-culture/` | 200 | No breadcrumb, no related posts, no tags, no reading time; 3 in-body internal links |
| `https://www.helpscout.com/blog/ai-adoption/` | **404** | Blog has moved to `articles.` subdomain |
| `https://www.helpscout.com/blog/committed-to-dei/` | 302→200 | Legacy in-body links redirect cross-host |
| `https://www.helpscout.com/help-desk-staffing-calculator/` | 200 | Tools live at root, not under `/resources/` |
| `https://ahrefs.com/blog/` | 200 | Two-axis nav; text-only cards; multi-category cards |
| `https://ahrefs.com/blog/page/2/` | 200 | Numbered pagination, canonical back to `/blog/` |
| `https://ahrefs.com/seo` | 200 | 10-chapter numbered pillar, sub-lessons named inline |
| `https://ahrefs.com/free-seo-tools` | 200 | Tools grouped by the blog's topic vocabulary |
| `https://zapier.com/blog/` | 200 | Two-level category tree, "All articles" per parent; reading time |
| `https://zapier.com/apps` | 200 | Faceted directory: sort + two-level categories |
| `https://zapier.com/apps/slack/integrations` | 200 | Directory item → blog contextual links; category eyebrow |
| `https://www.nerdwallet.com/mortgages` | 200 | Tools first; Explore By facet; task clusters; calculators as a per-topic group; 0 `BreadcrumbList` |
| `https://www.numbeo.com/cost-of-living/` | 200 | Topic × view-type matrix; calculators as a view type |
| `https://docs.stripe.com/` | 200 | Reference as a top-level peer of guides |
| `https://www.intercom.com/resources` | **302 → `/why-choose-intercom`** | Resources hub retired |
| `https://www.investopedia.com/` | **402** | Blocked — no claims made |
| `https://www.niche.com/graduate-schools/…` | **403** | Blocked — no claims made |
| `https://therapistsupport.org/resources.html` | 200 | Current hub: 24 question rows, 72 reference links, 10 topic pills, 37 internal links, flat root URLs |
