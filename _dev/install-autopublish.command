#!/bin/bash
# Double-click me once. After that, auto-publish runs by itself.
#
# Installs a LaunchAgent so the watcher starts at login and restarts if it
# ever dies — no Terminal window to keep open, survives a reboot.
#
# To stop it later, double-click _dev/uninstall-autopublish.command.

set -u
cd "$(dirname "$0")/.." || exit 1
ROOT="$(pwd)"
LABEL="com.cavatello.therapist-tools.publish"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

say()  { printf "  %s\n" "$*"; }
fail() { printf "\n  %s\n\n" "$*" >&2; read -r -p "Press return to close." _; exit 1; }

echo
say "Installing auto-publish for:"
say "  $ROOT"
echo

command -v git >/dev/null 2>&1 || fail "git is not installed. Run: xcode-select --install"
[ -d "$ROOT/.git" ] || fail "This folder is not connected to Cloudflare yet. Run ./_dev/publish.sh setup first."
[ -f "$ROOT/_dev/$LABEL.plist" ] || fail "Missing _dev/$LABEL.plist — re-sync the _dev folder."

# Confirm a push actually works before handing the job to a background service.
# A LaunchAgent that cannot authenticate fails silently forever.
say "Testing that a push works before installing..."
if ! git ls-remote origin >/dev/null 2>&1; then
  echo
  say "Could not reach Cloudflare with your saved credentials."
  say "Fix that first, then run this again:"
  say "   brew install gh && gh auth login"
  fail "Not installed."
fi
say "Cloudflare reachable."
echo

mkdir -p "$HOME/Library/LaunchAgents" || fail "Could not create ~/Library/LaunchAgents"

# Unload any previous copy so re-running this is safe.
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null

sed "s|__REPO__|$ROOT|g" "$ROOT/_dev/$LABEL.plist" > "$PLIST" || fail "Could not write $PLIST"
say "Wrote $PLIST"

if launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null; then
  say "Loaded."
else
  # bootstrap fails if it is somehow still registered; kickstart covers that.
  launchctl kickstart -k "gui/$(id -u)/$LABEL" 2>/dev/null || fail "launchctl could not start it. See $ROOT/_dev/autopublish.log"
  say "Restarted an existing copy."
fi

echo
say "Waiting for the first heartbeat..."
ok=0
for _ in 1 2 3 4 5 6 7 8 9 10; do
  sleep 2
  if [ -f "$ROOT/_dev/.watch-heartbeat" ]; then
    now=$(date '+%s'); beat=$(cat "$ROOT/_dev/.watch-heartbeat" 2>/dev/null)
    [ $(( now - ${beat:-0} )) -le 30 ] && { ok=1; break; }
  fi
done

echo
if [ "$ok" = "1" ]; then
  say "Auto-publish is ON and will stay on."
  say "It starts at login and restarts itself if it stops."
  echo
  say "Save any file in this folder and it publishes about 15 seconds later."
  say "Check on it any time with:   ./_dev/publish.sh status"
  say "Log:                         _dev/autopublish.log"
else
  say "Installed, but no heartbeat yet. Check the log:"
  say "   $ROOT/_dev/autopublish.log"
fi
echo
read -r -p "Press return to close." _
