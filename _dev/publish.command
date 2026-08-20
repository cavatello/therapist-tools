#!/bin/bash
# Double-click me in Finder to publish the site to Cloudflare Pages.
cd "$(dirname "$0")/.." || exit 1

# git leaves a stale lock behind if a previous run was interrupted
rm -f .git/index.lock 2>/dev/null

if [ ! -d .git ] || ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  echo "First run - setting up the connection to Cloudflare..."
  echo
  ./_dev/publish.sh setup
else
  ./_dev/publish.sh
fi

echo
echo "----------------------------------------------------"
echo "Live site:  https://therapistsupport.org/"
echo "Give it about a minute, then hard-refresh (Cmd+Shift+R)."
echo
echo "You can close this window."
