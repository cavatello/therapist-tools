#!/bin/bash
# Publish the site folder to Cloudflare, which republishes the Cloudflare Pages site.
#
#   ./_dev/publish.sh setup     one time - wire this folder up to the repo
#   ./_dev/publish.sh           commit and push whatever has changed
#   ./_dev/publish.sh watch     keep running; push automatically when files change
#   ./_dev/publish.sh status    is the watcher alive? did the last push work?
#
# Pages usually rebuilds within a minute of a push - though it has taken eight.
#
# The watcher writes two files while it runs. _dev/ as a whole is NO LONGER
# gitignored (the build tooling lives there and must be tracked), so these two
# are named individually in .gitignore. They must stay there: .watch-heartbeat
# is touched every 5 seconds, so tracking it would make the watcher commit and
# push in an endless loop.
#
#   _dev/.watch-heartbeat   touched every few seconds while watching
#   _dev/.publish-error     written when a push fails, deleted when one works
#
# They exist so a dead watcher or a broken token is *visible*. Before these,
# the only symptom was edits quietly never appearing on the site.

set -u
cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"
REMOTE="https://dash.cloudflare.com/"
SITE="https://therapistsupport.org/"
WATCH_EXT="js html css txt md"
BEAT="$ROOT/_dev/.watch-heartbeat"
ERRF="$ROOT/_dev/.publish-error"

say()  { printf "  %s\n" "$*"; }
fail() { printf "\n  %s\n\n" "$*" >&2; exit 1; }

need_git() { command -v git >/dev/null 2>&1 || fail "git is not installed. Run: xcode-select --install"; }

fingerprint() {
  # size+mtime of every tracked-ish file at the top level; ignores _dev and _to_delete
  for e in $WATCH_EXT; do
    for f in "$ROOT"/*."$e"; do
      [ -e "$f" ] || continue
      stat -f "%N:%z:%m" "$f" 2>/dev/null || stat -c "%n:%s:%Y" "$f"
    done
  done | sort
}

do_setup() {
  need_git
  if [ -d "$ROOT/.git" ]; then
    say "Already a git repo - checking the remote."
  else
    say "Creating the git repo..."
    git init -q || fail "git init failed"
    git branch -M main
  fi

  if git remote get-url origin >/dev/null 2>&1; then
    cur="$(git remote get-url origin)"
    [ "$cur" = "$REMOTE" ] || { say "Repointing origin ($cur -> $REMOTE)"; git remote set-url origin "$REMOTE"; }
  else
    git remote add origin "$REMOTE"
  fi

  say "Fetching what is already on Cloudflare..."
  if ! git fetch -q origin main 2>/dev/null; then
    fail "Could not reach the repo. If it asked for a password, see AUTH below."
  fi

  # Adopt the existing remote history without touching any local file,
  # so the next commit lands cleanly on top of the web upload.
  git reset -q --soft origin/main 2>/dev/null || true
  git branch -M main
  git branch --set-upstream-to=origin/main main >/dev/null 2>&1 || true

  say "Setup done."
  echo
  do_publish "Set up publishing from the local folder"
}

# Runs immediately before every commit, so it cannot be skipped.
#
#   discovery.py   regenerates sitemap.xml from the pages that exist right now.
#                  This is the whole reason the sitemap can never go stale: the
#                  only path to the live site goes through it.
#   seo_rules.py   read-only. Fails ONLY on findings that are new since
#                  _dev/_snap/seo_rules.json, so a pre-existing problem never
#                  blocks a push and a regression always does.
#
# Set TS_SKIP_CHECKS=1 to push anyway. That is deliberately awkward to type.
prepublish() {
  command -v python3 >/dev/null 2>&1 || { say "python3 not found - skipping checks"; return 0; }
  [ -f "$ROOT/_dev/discovery.py" ] || return 0

  say "Regenerating the sitemap..."
  python3 "$ROOT/_dev/discovery.py" >/tmp/ts-discovery.log 2>&1 || {
    say "discovery.py failed:"; tail -12 /tmp/ts-discovery.log; }

  [ -f "$ROOT/_dev/seo_rules.py" ] || return 0
  say "Checking the SEO rules..."
  if python3 "$ROOT/_dev/seo_rules.py" >/tmp/ts-seo.log 2>&1; then
    tail -1 /tmp/ts-seo.log | sed 's/^/  /'
    return 0
  fi
  echo
  cat /tmp/ts-seo.log
  echo
  if [ "${TS_SKIP_CHECKS:-0}" = "1" ]; then
    say "TS_SKIP_CHECKS=1 - pushing anyway."
    return 0
  fi
  fail "Not pushing. Fix the findings above, or:  TS_SKIP_CHECKS=1 ./_dev/publish.sh"
}

do_publish() {
  need_git
  [ -d "$ROOT/.git" ] || fail "Not set up yet. Run:  ./_dev/publish.sh setup"
  msg="${1:-Update $(date '+%Y-%m-%d %H:%M')}"

  prepublish

  git add -A
  if git diff --cached --quiet; then
    say "Nothing changed - nothing to push."
    return 0
  fi

  say "Committing: $msg"
  git commit -q -m "$msg" || fail "commit failed"

  say "Pushing..."
  if git push -q origin main; then
    rm -f "$ERRF"
    say "Pushed. Pages rebuilds in about a minute:"
    say "$SITE"
  else
    printf '%s  push failed\n' "$(date '+%Y-%m-%d %H:%M:%S')" > "$ERRF"
    echo
    say "Push failed - almost always authentication."
    say "AUTH: easiest fix is the Cloudflare CLI -"
    say "   brew install gh && gh auth login"
    say "Then run this script again. (Your account password will not work;"
    say "git needs a token, which gh sets up for you.)"
    return 1
  fi
}

do_watch() {
  need_git
  [ -d "$ROOT/.git" ] || fail "Not set up yet. Run:  ./_dev/publish.sh setup"
  say "Watching $ROOT"
  say "Pushes automatically once edits stop for 15s. Ctrl-C to stop."
  date '+%s' > "$BEAT"
  echo
  last="$(fingerprint)"
  settle=0
  trap 'rm -f "$BEAT"; exit 0' INT TERM
  while true; do
    sleep 5
    date '+%s' > "$BEAT"
    now="$(fingerprint)"
    if [ "$now" != "$last" ]; then
      last="$now"; settle=0
      say "change detected..."
    elif [ -n "${PENDING:-}" ] || ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git status --porcelain)" ]; then
      settle=$((settle+5))
      if [ "$settle" -ge 15 ]; then
        echo
        do_publish "Auto-publish $(date '+%Y-%m-%d %H:%M')"
        echo
        settle=0
      fi
    fi
  done
}

do_status() {
  local now beat age
  now=$(date '+%s')
  if [ -f "$BEAT" ]; then
    beat=$(cat "$BEAT" 2>/dev/null)
    age=$(( now - ${beat:-0} ))
    if [ "$age" -le 30 ]; then
      say "Watcher: RUNNING (last beat ${age}s ago)"
    else
      say "Watcher: NOT RUNNING - last beat ${age}s ago ($(( age / 60 )) min)."
      say "         Your edits are not being published. Start it with:"
      say "         launchctl kickstart -k gui/\$(id -u)/com.cavatello.therapist-tools.publish"
      say "         ...or double-click _dev/publish-watch.command"
    fi
  else
    say "Watcher: never started (no heartbeat file)."
  fi

  if [ -f "$ERRF" ]; then
    say "Last push: FAILED - $(cat "$ERRF")"
    say "         Almost always the token. Fix with:  gh auth login"
  else
    say "Last push: ok"
  fi

  if [ -d "$ROOT/.git" ]; then
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
      say "Working copy: uncommitted changes present"
      git status --porcelain | sed 's/^/           /'
    else
      say "Working copy: clean"
    fi
  fi
}

case "${1:-publish}" in
  setup)   do_setup ;;
  watch)   do_watch ;;
  status)  do_status ;;
  publish) do_publish "${2:-}" ;;
  *)       do_publish "$*" ;;
esac
