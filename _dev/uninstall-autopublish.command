#!/bin/bash
# Double-click me to turn auto-publish back off.
# Your files and the repo are untouched — this only stops the background watcher.
set -u
cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"
LABEL="com.cavatello.therapist-tools.publish"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null && echo "  Stopped." || echo "  It was not running."
rm -f "$PLIST" && echo "  Removed $PLIST"
rm -f "$ROOT/_dev/.watch-heartbeat"
echo
echo "  Auto-publish is OFF. Publish by hand with ./_dev/publish.sh,"
echo "  or double-click _dev/publish-watch.command for the old window-based watcher."
echo
read -r -p "Press return to close." _
