# Therapy Practice Simulator — local working copy

**This folder is the source of truth.**

**Live site: https://therapistsupport.org/** (Cloudflare Pages, free)

`practice-income-planner.cloudflare.app` is **no longer a website** — as of 25 July 2026
it holds nothing but a `_redirects` file that 301s every path to Cloudflare Pages. Do not
deploy the site there again unless you mean to undo that.


---

## Previewing locally (free — no deploy needed)

Every deploy costs Cloudflare build credit, so develop against the local server and
deploy once when you're happy with a batch of changes.

```bash
cd ~/Downloads/therapy-practice-site
python3 _dev/serve.py
```

Then open **http://localhost:8080** — it opens automatically. Ctrl-C to stop.
Port busy? `python3 _dev/serve.py 8081`.

Or double-click **`_dev/serve.command`** in Finder. (First time, macOS may block it:
right-click → Open, or run `chmod +x _dev/serve.command` once.)

| Page | URL |
|---|---|
| Simulator | http://localhost:8080/#sim |
| Grow Your Practice | http://localhost:8080/#grow |
| Field Notes | http://localhost:8080/rates.html |
| Tycoon | http://localhost:8080/tycoon.html |
| Layout concepts | http://localhost:8080/concepts.html |

Layout variants: `?v=01` … `?v=04` — same engine, different first screen.

### What the dev server does that `python3 -m http.server` does not

- **Live reload.** Edit `app.js` and the open page refreshes itself. No Cmd-R.
- **Waits for the write to finish.** It only reloads once the file has stopped
  changing, so you never catch a half-saved `app.js` and see a spurious blank page.
- **Never caches `app.js`.** Plain `http.server` will happily serve you a stale
  285KB bundle and make you think your edit did nothing.
- **Leaves your files alone.** The reload snippet is injected into the HTTP
  response, never written to disk, so nothing dev-only can leak into a deploy.
- Serves `.js` as `charset=utf-8`, so non-ASCII in the bundle can't mis-decode.

`file://` will not work for these pages — they load React from a CDN and use
`localStorage`. You need a real HTTP server.

### `_dev/` must not be deployed

Keep `_dev/` and `_to_delete/` out of any folder you deploy from. A Cloudflare deploy
uploads everything it is given.

---

## Deploying (only when a batch is ready)

Deploys replace the **entire** file set, so every page must be present or it is
deleted from the live site.

```bash
# 1. always re-download tycoon.html first — see below
curl -s https://therapistsupport.org/tycoon.html -o tycoon.html

# 2. deploy (fetch a fresh token immediately before; they expire fast)
npx -y @cloudflare/mcp@latest \
  --site-id a98d0381-c701-48a2-af30-404118b3c8a6 \
  --proxy-path "<fresh token>"
```

**Gotcha:** the token URL comes back containing a doubled slash
(`cloudflare-mcp.cloudflare.app//proxy/…`). Passed as-is it fails with a bare
`404 Not Found` that looks like an auth or billing problem. Collapse it to a single
slash and it works.

Afterwards, re-download the live files and grep for something that should now be
there. Don't trust the success message.

### tycoon.html — do not edit

`tycoon.html` belongs to a different work session. The copy here is byte-identical
to live (`abb342744a732277b04044cbdbc71552`) and has never been opened. It is here
**only** so navigation resolves locally and so a deploy does not delete it from the
live site. It changes often — it grew from 13,670 to 178,877 bytes over 25 July —
so always re-download it immediately before deploying.

---

## Notes for editing app.js

- Compiled JSX — `React.createElement(...)` throughout. No build step, no JSX.
- `node --check app.js` proves the file parses and **nothing more**. Three separate
  changes on 25 July passed it while rendering a blank page, all temporal dead zone
  errors — a `const` referenced above its declaration. The tell is a green syntax
  check plus an empty `#root`. Always look at the page.
- Declaration order matters: `funnelSessions` must sit below `sessions`, and the
  structure-comparison panel below `soleFullYear` / `sCorpFullYear`.
- Wrapping an element in a new parent is the other classic break — one unclosed
  `(`, and `node --check` reports the error at the *last line of the file*, nowhere
  near the mistake.
- Regression check: rate `200`, sessions/week `20` → Gross/year **$208,000**,
  Gross/week **$4,000**.
- **Never "LLC".** CA-licensed MFTs cannot form one (Cal. Corp. Code §17701.04(e)).
  The choice is Sole Proprietorship or Professional Corp with an S-corp election.
  `grep -n "LLC" app.js` should return 10 hits, all explaining why it isn't an option.

---

## Housekeeping

`_to_delete/` holds files I could not remove from this side (the bridge is
read-write but not delete-capable). Safe to drag to the Trash.

---

## Publishing to Cloudflare Pages (free, for phone review)

Public preview: **https://therapistsupport.org/**
Repo: https://dash.cloudflare.com/

This is separate from Cloudflare and costs nothing. Use it to look at the site on a
phone or send it to someone.

```bash
# one time only
./_dev/publish.sh setup

# afterwards, push whatever changed
./_dev/publish.sh

# or leave this running and it pushes by itself
./_dev/publish.sh watch
```

`watch` polls every 5s and pushes once edits have stopped for 15 seconds, so a burst
of changes becomes one commit rather than twenty. Cloudflare Pages rebuilds about a
minute after each push.

`_dev/` and `_to_delete/` are gitignored, so the dev server and scratch files never
reach the repo.

**Authentication.** `git push` over HTTPS will not accept your Cloudflare account
password. The simplest fix, once:

```bash
brew install gh && gh auth login
```

Alternatively create a fine-grained Personal Access Token with Contents: Read and
write, and paste it when git asks for a password.

**The repo is public** — required for free Pages — so `app.js` is readable, including
the mailto address in the feedback form. Same exposure as the Cloudflare site.

### Which one to use

| | Local server | Cloudflare Pages | Cloudflare |
|---|---|---|---|
| Cost | free | free | build credit |
| Live reload | yes | no | no |
| Works on a phone | same Wi-Fi only | anywhere | anywhere |
| Purpose | building | reviewing, sharing | the real site |

---

## The Cloudflare redirect (25 July 2026)

The Cloudflare site now contains exactly one file, `_redirects`:

```
/index.html     .../index.html     301!
/rates.html     .../rates.html     301!
/tycoon.html    .../tycoon.html    301!
/app.js         .../app.js         301!
/*              .../index.html     301!
```

Known pages keep their deep links; anything else lands on the simulator. Query
strings (`?v=01`) and hash fragments (`#sim`, and `#s=` share links) survive a 301,
so old links still work.

**Why `301!` and not `301`.** Cloudflare serves an existing file in preference to a
redirect rule. The `!` forces the redirect regardless. It does not matter while
`_redirects` is the only file, but it will the moment anything else is added.

**Caution.** A Cloudflare deploy replaces the *entire* file set. On 25 July a deploy
containing only a hand-written redirect `index.html` deleted `app.js`, `rates.html`,
`concepts.html` and `tycoon.html` from the live site. Nothing was lost — every file
existed on Cloudflare Pages and in this folder, and `tycoon.html` was verified
byte-identical (`abb342744a732277b04044cbdbc71552`) — but that is the failure mode to
watch for. That page also pointed at `https://therapistsupport.org`, which is not a site.
