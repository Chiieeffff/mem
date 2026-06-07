# Daily Sales Intelligence Brief

## Objective
Surface lead signals and partnership opportunities for GatewayCrypto across iGaming, Forex, and crypto payments. Append findings to the master Google Sheet so Roman reviews them each morning.

## Inputs
- None required — all queries are predefined below
- Current date (use system date)

## Output
- Rows appended to `GatewayCrypto — Daily Sales Intel` Google Sheet (GOOGLE_SHEET_ID in .env)
- Sheet URL printed at the end

---

## Execution Steps

### Step 1 — Run news searches

Run `tools/search_web.py` with the following query array. Use `--max-results 5` per query.

```
python tools/search_web.py --max-results 5 --queries '[
  "iGaming B2B platform launch OR new operator 2026",
  "iGaming platform funding round OR acquisition 2026",
  "Forex CRM OR trading platform launch OR new broker 2026",
  "iGaming crypto payments integration announcement 2026",
  "iGaming licensing news LATAM OR Africa OR Southeast Asia 2026",
  "B2C online casino OR sportsbook expansion new market 2026",
  "crypto payment processor iGaming partnership 2026",
  "iGaming platform payment problems OR chargeback issues 2026",
  "fintech stablecoin B2B payments partnership iGaming 2026"
]'
```

### Step 2 — Synthesize and score

Review all results. For each distinct news item, evaluate:

**Category** (pick one):
- `Lead Signal` — a company that matches GatewayCrypto's ICP has a trigger event
- `Partnership Intel` — a platform, aggregator, or network that could integrate or co-sell with GatewayCrypto
- `Competitor Move` — a competing crypto payment processor wins a deal, launches a feature, or enters a new market
- `Market Trend` — regulatory, macro, or industry shift relevant to the sales narrative

**ICP reminder:**
- Sales targets: B2C operators (online casino, sportsbook), iGaming platforms (B2B software providers), Forex brokers
- Partnership targets: iGaming B2B platforms (provide software to operators), Forex CRM/platform providers

**Lead Potential:**
- `HIGH` — company fits ICP AND has a clear trigger: new launch, funding round, geo expansion, licensing, or explicit payment pain signal
- `MEDIUM` — fits ICP but trigger is weak or indirect
- `LOW` — loosely related; monitor only

**Filter rules:**
- Skip duplicate news items (same company, same event)
- Skip generic market trend articles with no named company
- Skip GatewayCrypto itself

### Step 3 — Deep research on HIGH leads

For each HIGH-potential company (cap at 3 per run to stay within Tavily limits):
1. Run `tools/scrape_website.py --url [company homepage]`
2. Look for: existing payment processor mentioned, crypto support, scale signals (client count, markets), tech stack hints
3. Add any relevant findings to the "Why It Matters" field for that row

```
python tools/scrape_website.py --url https://example.com
```

### Step 4 — Build row data

Construct a JSON array of rows. Each row must have these exact keys:

```json
[
  {
    "Date": "2026-06-07",
    "Category": "Lead Signal",
    "Company": "Company Name",
    "Headline": "One sentence describing the news event",
    "Lead Potential": "HIGH",
    "Why It Matters": "Why this is relevant to GatewayCrypto in 1-2 sentences. Be specific — mention the trigger, their likely payment gap, and how GWC fits.",
    "Suggested Action": "Specific next step. Examples: 'Run linkedin_outreach workflow for [Name, Title]', 'Monitor — revisit in 2 weeks', 'Research decision-maker on LinkedIn'",
    "Status": "",
    "Source URL": "https://..."
  }
]
```

**Suggested Action guidance:**
- HIGH leads: `Run linkedin_outreach workflow` or `Run batch_lead_sourcing for [Company]`
- MEDIUM leads: `Monitor — check again next week` or `Research decision-maker`
- Competitor Move: `Note competitive context — update pitch if needed`
- Market Trend: `Consider referencing in outreach for [geo/topic]`

### Step 5 — Append to Google Sheet

```
python tools/append_to_sheet.py --rows '[... your JSON array ...]'
```

The tool reads GOOGLE_SHEET_ID from .env. If the sheet is empty, it creates the header row automatically.

On success, it prints: `{"appended": N, "sheet_url": "https://docs.google.com/spreadsheets/d/..."}`

### Step 6 — Report

Print a brief summary:
- Total items found
- HIGH / MEDIUM / LOW counts
- Link to the sheet

---

## Edge Cases

**No results for a query:** Skip it, continue with remaining queries. Note in summary if more than 3 queries returned empty.

**Tavily rate limit error:** Stop remaining queries, process what was collected, append partial results. Note in summary that results are partial.

**append_to_sheet.py auth error (first run):** Browser will open for OAuth consent. Complete it once — subsequent runs are non-interactive. If running headlessly, set up credentials.json first (see Setup below).

**Duplicate detection:** Before appending, check the Headline and Company against today's existing rows if any were already written today (rare — but if workflow runs twice in one day, avoid duplicates by checking the source URL).

---

## Setup (one-time)

1. **Create the Google Sheet:**
   - Go to Google Sheets and create a new blank sheet
   - Name it `GatewayCrypto — Daily Sales Intel`
   - Copy the sheet ID from the URL: `docs.google.com/spreadsheets/d/[THIS_PART]/edit`
   - Add it to `.env`: `GOOGLE_SHEET_ID=your_sheet_id_here`

2. **Enable Google Sheets API:**
   - Go to Google Cloud Console → APIs & Services → Enable APIs
   - Enable "Google Sheets API"
   - Create OAuth 2.0 credentials (Desktop App type)
   - Download as `credentials.json` and place in repo root

3. **First auth run:**
   - Run: `python tools/append_to_sheet.py --rows '[{"Date":"test"}]' --sheet-id YOUR_ID`
   - Browser opens → sign in → grant access → `token.json` is saved
   - Delete the test row from the sheet

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

---

## Scheduling

**Automatic daily run (via /schedule):**
Prompt: `Read workflows/daily_sales_brief.md and execute it fully.`
Time: 7:00 AM local

**Manual trigger:**
From Claude.ai or Claude Code: `"Run the daily sales brief"` or `"Read workflows/daily_sales_brief.md and execute it."`
