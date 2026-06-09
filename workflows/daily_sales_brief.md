# Daily Sales Intelligence Brief

## Objective
Surface NEW lead signals and partnership opportunities for GatewayCrypto across iGaming, Forex, and crypto payments. Append only genuinely new findings to the master Google Sheet — never repeat a company or story already in the sheet.

## Inputs
- None required — all queries are predefined below
- Current date (use system date)

## Output
- New rows appended to the master `GatewayCrypto — Daily Sales Intel` Google Sheet
- Sheet URL printed at the end

---

## Execution Steps

### Step 1 — Load seen history (CRITICAL — do this before searching)

**Remote environment (Google Drive MCP):**
Use the Google Drive MCP to search for the file named `GatewayCrypto — Daily Sales Intel` and read its full contents. Extract two lists:
- `seen_urls`: all values in the "Source URL" column
- `seen_companies`: all values in the "Company" column (lowercased)

You will use these to filter out duplicates in Step 3. If the sheet doesn't exist yet, both lists are empty.

**Local environment:**
```
python tools/append_to_sheet.py --read-existing
```
(or read the sheet directly via the Sheets API to extract Source URL and Company columns)

---

### Step 2 — Run news searches with cascading time window

Use a cascading window approach:
1. **First pass — last 7 days:** Run all 9 queries restricted to the past 7 days
2. **Check:** After Step 3 deduplication, if fewer than 5 new items survive, do a **second pass — last 30 days** (same queries, wider window, skip URLs already collected in first pass)
3. **If still fewer than 5 new items:** Do a **third pass — last 6 months** (same queries, skip all URLs already collected)
4. Stop expanding once you have 5+ new items, or once all three windows are exhausted

The goal is always to have a meaningful brief. Prefer fresh news, but don't leave the sheet empty just because the last 7 days were quiet.

**Local:**
```
python tools/search_web.py --max-results 5 --days 7 --queries '[...]'
# then retry with --days 30, then --days 180 if needed
```

**Remote (WebSearch tool):**
- First pass: prefix queries with `news last 7 days:`
- Second pass (if needed): prefix queries with `news last 30 days:`
- Third pass (if needed): prefix queries with `news last 6 months:`

Queries (same for all passes):
1. `iGaming B2B platform new launch site:igamingbusiness.com OR site:casinobeats.com`
2. `iGaming platform funding round OR acquisition deal`
3. `Forex broker OR CRM platform launch OR new product`
4. `online casino OR sportsbook crypto payment integration`
5. `iGaming operator license LATAM OR Africa OR Southeast Asia OR Brazil OR Nigeria OR Philippines`
6. `online casino OR sportsbook new market launch expansion`
7. `crypto payment processor gambling partnership deal`
8. `online casino payment chargeback problem OR payment provider switch`
9. `stablecoin USDT B2B iGaming OR Forex payments`

Collect every result with its URL, title, snippet, and publish date where visible.

---

### Step 3 — Deduplicate

For each result collected in Step 2:
- **Skip** if its URL is in `seen_urls`
- **Skip** if the company name (lowercased) is in `seen_companies` AND the event/trigger is the same story (same funding round, same launch, same announcement)
- **Skip** generic articles with no named company
- **Skip** GatewayCrypto itself

Only what survives this filter moves forward.

---

### Step 4 — Synthesize and score surviving items

For each surviving item, assign:

**Category** (pick one):
- `Lead Signal` — a company matching GatewayCrypto's ICP has a trigger event
- `Partnership Intel` — a platform/aggregator that could integrate or co-sell with GatewayCrypto
- `Competitor Move` — a competing crypto payment processor wins a deal, launches a feature, or enters a new market
- `Market Trend` — regulatory, macro, or industry shift relevant to the sales narrative

**GatewayCrypto ICP:**
- Sales targets: B2C operators (online casino, sportsbook), iGaming platforms (B2B software providers), Forex brokers
- Partnership targets: iGaming B2B platforms, Forex CRM/platform providers
- Product: crypto payment processing (USDT/USDC multichain, 300+ assets), fiat off-ramp (EUR via SEPA/SWIFT), zero chargebacks, API + Backoffice

**Lead Potential:**
- `HIGH` — company fits ICP AND has a clear trigger: new launch, funding round, geo expansion, licensing, or explicit payment pain signal
- `MEDIUM` — fits ICP but trigger is weak or indirect
- `LOW` — loosely related; monitor only

If zero new items survive after deduplication, report "No new items today — all results already in sheet" and stop. Do not write anything to the sheet.

---

### Step 5 — Deep research on HIGH leads (cap at 3)

For each HIGH-potential company:

**Local:** `python tools/scrape_website.py --url [company homepage]`

**Remote:** Use WebFetch on their homepage.

Look for: existing payment processor mentioned, crypto support, scale signals (client count, markets), tech stack hints. Add findings to "Why It Matters".

---

### Step 6 — Build row data

Construct a JSON array of rows. Each row:

```json
{
  "Date": "2026-06-08",
  "Category": "Lead Signal",
  "Company": "Company Name",
  "Headline": "One sentence describing the news event",
  "Lead Potential": "HIGH",
  "Why It Matters": "1-2 sentences — mention the trigger, their likely payment gap, and how GWC fits. Be specific.",
  "Suggested Action": "Run linkedin_outreach workflow for [Company]",
  "Status": "",
  "Source URL": "https://..."
}
```

**Suggested Action guidance:**
- HIGH: `Run linkedin_outreach workflow for [Company]` or `Run batch_lead_sourcing for [Company]`
- MEDIUM: `Monitor — check again next week` or `Research decision-maker`
- Competitor Move: `Note competitive context — update pitch if needed`
- Market Trend: `Consider referencing in outreach for [geo/topic]`

---

### Step 7 — Write to master sheet

**Remote (Google Drive MCP):**
Find the existing `GatewayCrypto — Daily Sales Intel` sheet and append the new rows to it. Do NOT create a new sheet each day — always append to the same master sheet. If the sheet doesn't exist, create it once with the header row:
`Date | Category | Company | Headline | Lead Potential | Why It Matters | Suggested Action | Status | Source URL`

**Local:**
```
python tools/append_to_sheet.py --rows '[... your JSON array ...]'
```

---

### Step 8 — Report

Print:
- Total new items added today
- HIGH / MEDIUM / LOW counts
- Items skipped as duplicates
- Link to the master sheet

---

## Edge Cases

**No new results after dedup:** Report "0 new items — all results already seen" and return the sheet URL. Do not write anything.

**Search returns only old articles:** Note in summary. Try adding the current month/year to one retry search per category.

**Sheet read fails:** Proceed without history (treat seen lists as empty), but note in summary that dedup was skipped.

**Tavily rate limit (local):** Stop, process what was collected, append partial results, note partial run in summary.

---

## Setup (one-time, local only)

1. Create a blank Google Sheet named `GatewayCrypto — Daily Sales Intel`
2. Copy the sheet ID from the URL and add to `.env`: `GOOGLE_SHEET_ID=your_id`
3. Enable Google Sheets API in Google Cloud Console, download `credentials.json`
4. Run first auth: `python tools/append_to_sheet.py --rows '[{"Date":"test"}]'` → browser opens → approve → delete test row
5. `pip install -r requirements.txt`

---

## Scheduling

**Automatic daily run:** 7:00 AM Nicosia time (4:00 AM UTC) via routine `trig_0152PZyF8TyZLjAYgJGPTtWh`

**Manual trigger:** `"Run the daily sales brief"` or `"Read workflows/daily_sales_brief.md and execute it."`
