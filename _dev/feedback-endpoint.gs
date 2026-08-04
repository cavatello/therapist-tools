/**
 * Feedback endpoint for the Therapy Practice Simulator.
 * Appends every submission to a Google Sheet AND emails you a copy.
 *
 * ═══════════════════════════════════════════════════════════════════════════
 *  IF YOU HIT "Error 401: invalid_client — The OAuth client was not found"
 * ═══════════════════════════════════════════════════════════════════════════
 *
 *  That error is a Google session problem, not a problem with this code. It
 *  almost always means the browser is signed into more than one Google
 *  account and the deploy flow resolved the wrong one. In order of likelihood:
 *
 *   1. MULTI-ACCOUNT. Open an Incognito/Private window, sign in with ONLY the
 *      account that owns the script, and do the deploy there. This fixes it
 *      the large majority of the time. (Same cause if your URL bar shows
 *      /u/1/ or /u/2/ — that is account #2 or #3, not your default.)
 *
 *   2. STALE PROJECT. In the Apps Script editor: Project Settings (gear) →
 *      Google Cloud Platform (GCP) Project. If it looks detached or errors,
 *      the quickest cure is to make a NEW Apps Script project and paste this
 *      file in again — a fresh project gets a fresh default GCP project.
 *
 *   3. WORKSPACE POLICY. If shawn@shawnwalters.com is a Google Workspace
 *      account, an admin policy can block third-party/unverified app
 *      authorisation. Try it from a personal @gmail.com account instead —
 *      the Sheet can still be shared with you.
 *
 *  If none of that clears it in five minutes, do not fight it. Use the
 *  Formspree route instead — see FORMSPREE.md. It takes about ninety seconds,
 *  needs no Google OAuth at all, and still emails you every submission.
 *
 * ═══════════════════════════════════════════════════════════════════════════
 *  SETUP
 * ═══════════════════════════════════════════════════════════════════════════
 *
 *  1. Create the Sheet first: go to sheets.new, name it something like
 *     "Practice Simulator — feedback", and leave it empty.
 *
 *  2. Copy its ID out of the URL and paste it into SHEET_ID below. The ID is
 *     the long string between /d/ and /edit:
 *        docs.google.com/spreadsheets/d/【THIS PART】/edit
 *
 *     Setting SHEET_ID explicitly is deliberate — it means this works whether
 *     you create the script from inside the Sheet (Extensions → Apps Script)
 *     or as a standalone project at script.new. The earlier version relied on
 *     getActiveSpreadsheet(), which returns null in a standalone project and
 *     would have failed at runtime even after a successful deploy.
 *
 *  3. Paste this whole file into the Apps Script editor, replacing what is
 *     there. Name the project something recognisable.
 *
 *  4. Run once manually to authorise: pick `setup` from the function dropdown
 *     and press Run. Approve the permissions. You will see an "unverified
 *     app" warning because it is your own private script — click Advanced →
 *     Go to (project) → Allow. Doing this BEFORE deploying often avoids the
 *     401 entirely.
 *
 *  5. Deploy → New deployment → gear icon → Web app.
 *        Execute as:      Me
 *        Who has access:  Anyone      ← must be "Anyone", NOT "Anyone with a
 *                                       Google account", or visitors fail.
 *
 *  6. Copy the Web app URL (it ends in /exec) and paste it into app.js:
 *        const FEEDBACK_ENDPOINT = "https://script.google.com/macros/s/…/exec";
 *
 *  7. Test it: open that /exec URL in a browser. You should see
 *     {"ok":true,...}. Then submit the real form once and check the Sheet.
 *
 *  Redeploying later: Deploy → Manage deployments → pencil → Version: New
 *  version. Creating a *new* deployment gives a different URL and leaves the
 *  old one running the old code.
 */

var SHEET_ID     = '';                          // ← paste your Sheet ID here
var NOTIFY_EMAIL = 'shawn@shawnwalters.com';
var SHEET_NAME   = 'Feedback';

/** Run this once from the editor to trigger the authorisation prompt. */
function setup() {
  var sheet = getSheet_();
  Logger.log(sheet ? 'Sheet OK: ' + sheet.getParent().getName() : 'No sheet — set SHEET_ID');
  MailApp.sendEmail(NOTIFY_EMAIL, 'Practice Simulator — feedback endpoint is live',
    'Authorisation worked. You can deploy the web app now.');
  Logger.log('Test email sent to ' + NOTIFY_EMAIL);
}

function getSheet_() {
  var ss = null;
  if (SHEET_ID) {
    ss = SpreadsheetApp.openById(SHEET_ID);
  } else {
    // Fall back to the container if the script is bound to a Sheet.
    ss = SpreadsheetApp.getActiveSpreadsheet();
  }
  if (!ss) return null;
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Received', 'Type', 'Name', 'Message', 'Their setup', 'Share link', 'Page', 'Browser']);
    sheet.getRange(1, 1, 1, 8).setFontWeight('bold');
    sheet.setFrozenRows(1);
    sheet.setColumnWidth(4, 420);
  }
  return sheet;
}

function doPost(e) {
  var data = {};
  try { data = JSON.parse(e.postData.contents); } catch (err) { data = (e && e.parameter) || {}; }
  var when = new Date();
  var sheetError = '';

  // Write to the Sheet, but never let a Sheet problem swallow the message —
  // the email below is the thing that must always get through.
  try {
    var sheet = getSheet_();
    if (sheet) {
      sheet.appendRow([when, data.type || '', data.name || '(anonymous)', data.message || '',
        data.setup || '', data.share || '', data.page || '', data.agent || '']);
    } else {
      sheetError = 'SHEET_ID is not set, so nothing was logged to a spreadsheet.';
    }
  } catch (err) {
    sheetError = String(err);
  }

  try {
    if (NOTIFY_EMAIL) {
      MailApp.sendEmail({
        to: NOTIFY_EMAIL,
        subject: '[' + (data.type || 'feedback') + '] Practice Simulator — ' + (data.name || 'anonymous'),
        replyTo: NOTIFY_EMAIL,
        htmlBody:
          '<div style="font-family:-apple-system,Segoe UI,sans-serif;font-size:14px;line-height:1.6;color:#26241E">' +
            '<p style="margin:0 0 14px"><strong>' + esc(data.type || 'feedback') + '</strong> from <strong>' +
              esc(data.name || 'anonymous') + '</strong></p>' +
            '<div style="background:#FBF9F3;border-left:4px solid #C98B4B;padding:12px 16px;margin:0 0 16px;white-space:pre-wrap">' +
              esc(data.message || '') + '</div>' +
            '<p style="margin:0 0 6px;color:#7C766A">Their setup: <strong style="color:#26241E">' +
              esc(data.setup || 'not given') + '</strong></p>' +
            (data.share ? '<p style="margin:0 0 6px"><a href="' + esc(data.share) +
              '">Open their exact setup &rarr;</a></p>' : '') +
            (sheetError ? '<p style="margin:14px 0 0;color:#B5483F;font-size:12px">Sheet write failed: ' +
              esc(sheetError) + '</p>' : '') +
            '<p style="margin:18px 0 0;font-size:11px;color:#9C948A">' +
              esc(String(when)) + '<br>' + esc(data.agent || '') + '</p>' +
          '</div>'
      });
    }
  } catch (err) {
    return json({ ok: false, error: 'email failed: ' + String(err), sheetError: sheetError });
  }

  return json({ ok: true, sheetError: sheetError });
}

/** Opening the /exec URL in a browser should show this — a quick liveness check. */
function doGet() {
  var sheet = null, note = '';
  try { sheet = getSheet_(); } catch (err) { note = String(err); }
  return json({
    ok: true,
    endpoint: 'Practice Simulator feedback',
    sheetConnected: !!sheet,
    sheetName: sheet ? sheet.getParent().getName() : null,
    notifyEmail: NOTIFY_EMAIL,
    note: note || (sheet ? 'Ready. POST JSON here.' : 'Deployed, but SHEET_ID is not set — emails will still send.')
  });
}

function esc(v) {
  return String(v == null ? '' : v)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
