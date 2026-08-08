#!/bin/bash
# Whole-folder sync for the Practice Income Planner.
#
# The old habit was to re-sync only the file you planned to edit. That is how a
# stale file gets published: a deploy uploads the whole directory, so any file
# you did not pull first gets overwritten with whatever your working copy holds.
# This script works on the entire published set instead.
#
#   ./_dev/sync.sh pull            download every published file from live
#   ./_dev/sync.sh check           compare live vs this working copy
#   ./_dev/sync.sh check mac.txt   three-way: live vs working copy vs the Mac
#
# For the three-way, get the Mac column first (device_bash has no network, so it
# can only report its own hashes):
#
#   cd <mac folder> && md5sum app.js index.html rates.html tycoon.html \
#     concepts.html robots.txt README.md package.json package-lock.json
#
# ...then save that output to a file and pass it as the second argument.

set -u
cd "$(dirname "$0")/.." || exit 1
SITE="https://therapistsupport.org"

# Everything GitHub Pages actually serves. _dev/, _to_delete/ and node_modules/
# are gitignored or unpublished and are deliberately absent.
# Verified against the live host: every name below returns 200.
FILES="index.html practice-simulator.html therapist-working-remotely-california.html therapist-cost-of-living-california.html rates.html tools.html about.html newsletter.html contact.html privacy.html terms.html associate-mft-job-advisor.html amft-3000-hours-california.html therapist-tax-strategy-california.html grow-your-therapy-practice.html tycoon.html concepts.html robots.txt README.md package.json package-lock.json og-image.png tools-booking.png sitemap.xml"

hash_of() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

do_pull() {
  echo "Pulling the published set from $SITE"
  local n=0 changed=0
  for f in $FILES; do
    local before after
    before=$(hash_of "$f")
    if ! curl -sfS "$SITE/$f" -o "$f.tmp"; then
      printf "  %-20s FETCH FAILED — left your copy alone\n" "$f"
      rm -f "$f.tmp"; continue
    fi
    mv "$f.tmp" "$f"
    after=$(hash_of "$f")
    n=$((n+1))
    if [ "$before" != "$after" ]; then
      changed=$((changed+1))
      printf "  %-20s UPDATED  %s -> %s\n" "$f" "${before:0:8}" "${after:0:8}"
    else
      printf "  %-20s same\n" "$f"
    fi
  done
  echo "$n files pulled, $changed changed."
  [ "$changed" -gt 0 ] && echo "Re-read anything you were mid-edit on before touching it again."
}

do_check() {
  local macfile="${1:-}"
  local drift=0
  if [ -n "$macfile" ]; then
    printf "%-20s %-10s %-10s %-10s %s\n" FILE LIVE WORKING MAC STATUS
  else
    printf "%-20s %-10s %-10s %s\n" FILE LIVE WORKING STATUS
  fi
  for f in $FILES; do
    local live local_h mac_h status
    live=$(curl -sfS "$SITE/$f" 2>/dev/null | md5sum | cut -d' ' -f1)
    local_h=$(hash_of "$f")
    [ -z "$local_h" ] && local_h="(absent)"
    if [ -n "$macfile" ]; then
      mac_h=$(grep -E "[[:space:]]\*?$f\$" "$macfile" 2>/dev/null | awk '{print $1}' | head -1)
      [ -z "$mac_h" ] && mac_h="(absent)"
      if [ "$live" = "$local_h" ] && [ "$live" = "$mac_h" ]; then status="ok"
      else status="DRIFT"; drift=$((drift+1)); fi
      printf "%-20s %-10s %-10s %-10s %s\n" "$f" "${live:0:8}" "${local_h:0:8}" "${mac_h:0:8}" "$status"
    else
      if [ "$live" = "$local_h" ]; then status="ok"
      else status="DRIFT"; drift=$((drift+1)); fi
      printf "%-20s %-10s %-10s %s\n" "$f" "${live:0:8}" "${local_h:0:8}" "$status"
    fi
  done
  echo
  if [ "$drift" -eq 0 ]; then
    echo "All $(echo $FILES | wc -w) published files agree."
  else
    echo "$drift file(s) out of sync. Do not deploy until this reads clean —"
    echo "a deploy uploads the whole directory and will overwrite live with your copy."
  fi
  return $drift
}

case "${1:-check}" in
  pull)  do_pull ;;
  check) do_check "${2:-}" ;;
  *)     echo "usage: $0 [pull|check [mac-hashes.txt]]"; exit 1 ;;
esac
