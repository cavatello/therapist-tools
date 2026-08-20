#!/bin/bash
# Build a clean public bundle and deploy it directly to Cloudflare Pages.
set -eu
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
OUT="$ROOT/_publish"
PROJECT="therapist-tools"

say() { printf '  %s\n' "$*"; }
fail() { printf '\n  %s\n\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null 2>&1 || fail "Python 3 is required."
command -v npx >/dev/null 2>&1 || fail "Node.js/npx is required."

say "Regenerating sitemap and structured data..."
python3 _dev/discovery.py
say "Running strict SEO checks..."
python3 _dev/seo_rules.py --all --strict

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
for file in *.html *.txt *.png *.webmanifest robots.txt sitemap.xml _headers _redirects; do
  [ -f "$file" ] && cp "$file" "$STAGE/"
done
for dir in css for getting-paid hours licensure money ops practice seo training; do
  [ -d "$dir" ] && cp -R "$dir" "$STAGE/"
done

mkdir -p "$OUT"
rsync -a --delete "$STAGE/" "$OUT/"
say "Deploying $(find "$OUT" -type f | wc -l | tr -d ' ') public files to Cloudflare Pages..."
npx --yes wrangler pages deploy "$OUT" --project-name "$PROJECT" --branch main
say "Published: https://therapistsupport.org/"
