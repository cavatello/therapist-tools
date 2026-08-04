#!/bin/bash
# Double-click me to keep publishing automatically whenever files change.
cd "$(dirname "$0")/.." || exit 1

rm -f .git/index.lock 2>/dev/null

if [ ! -d .git ] || ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  echo "First run - setting up the connection to GitHub..."
  echo
  ./_dev/publish.sh setup || { echo; echo "Setup did not finish. Fix the problem above, then try again."; exit 1; }
  echo
fi

echo "Auto-publish is ON. Leave this window open."
echo "Press Ctrl-C (or close the window) to stop."
echo
exec ./_dev/publish.sh watch
