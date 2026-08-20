# The 90-second alternative to Apps Script

Use this if the Google deploy keeps throwing `Error 401: invalid_client`. It needs no
Google OAuth at all, and unlike the Apps Script route it answers CORS properly — which
means the form can tell the visitor honestly whether the message actually sent, rather
than assuming it did.

## Setup

1. Go to **formspree.io** and sign up with shawn@shawnwalters.com.
2. **+ New Form**. Name it "Practice Simulator feedback".
3. Copy the endpoint it gives you — it looks like `https://formspree.io/f/xayzabcd`.
4. Paste it into `app.js`:

   ```js
   const FEEDBACK_ENDPOINT = "https://formspree.io/f/xayzabcd";
   ```

5. Publish. Submit the form once yourself — Formspree emails you a confirmation link the
   first time, and submissions only start flowing after you click it.

The app detects a Formspree URL automatically and switches to a proper CORS request, so
"✓ Sent" means it genuinely arrived and "Didn't send" means it genuinely didn't.

## What you get

- **Email on every submission**, with all the fields including the share link back to the
  sender's exact setup.
- **A dashboard** at formspree.io listing every submission — that is your database, and
  it exports to CSV whenever you want the data elsewhere.
- Spam filtering, which the Apps Script route does not have.

## The catch

The free tier is **50 submissions a month**. For a niche tool that is almost certainly
plenty; if it is ever not, that is a good problem and the paid tier is inexpensive.

## If you want the Google Sheet as well

Nothing stops you having both later: Formspree can forward submissions on, or you can
export CSV into a Sheet periodically. Start with email working reliably — a database
nobody can write to is worth less than an inbox that fills up.

## Other options, for completeness

| | Free tier | Database | Email | Google account needed |
|---|---|---|---|---|
| **Formspree** | 50/mo | dashboard + CSV | yes | no |
| **Apps Script** | effectively unlimited | Google Sheet | yes | yes — and it is the one that just failed |
| **Web3Forms** | 250/mo | dashboard | yes | no |
| **Cloudflare Issues** via a form-to-issue action | unlimited | the repo's issues | Cloudflare notifies you | no |

The Cloudflare Issues route is worth a thought given everything already lives in a Cloudflare
repo — each piece of feedback becomes an issue you can label and close. It is a little
more setup than Formspree and makes the feedback public unless the repo is private.
