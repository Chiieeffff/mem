# Workflow: iGaming B2B Platform Market Intelligence Map

## Objective

Build and maintain a master spreadsheet of the top 100 B2B iGaming platforms — white-label casino/sportsbook providers, turnkey platforms, aggregators — with payment processor intelligence and CRM tracking. This is a market map, not a prospect filter: it includes companies regardless of whether they've been contacted.

---

## Column Structure

| Column | Source | Who fills it |
|---|---|---|
| Company | Compiled list | Auto |
| Website | Compiled list | Auto |
| HQ / Region | Research | Auto |
| Est. Size | Research | Auto |
| Payment Processor(s) | Research | Auto |
| Contact Known | Internal | **Manual** |
| Talked To | Internal | **Manual** |
| Status | Internal | **Manual** |
| Notes | Internal | **Manual** |

**Status values:** `—` / `Active` / `Contacted` / `Interested` / `Partner` / `Dead`

---

## Step 1 — Compile the 100-company list

Start with known sources and expand via search:

**Seed from existing data:**
- ICP reference companies in `workflows/find_igaming_platforms.md` (10 examples)
- B2B platform names in `blacklist.csv` (filter out operators and non-platforms)

**Expand via Tavily discovery queries:**
```bash
python tools/search_web.py --queries '[
  "top white-label casino platform providers iGaming B2B 2024 2025",
  "turnkey sportsbook platform providers iGaming Europe Malta 2025",
  "iGaming B2B platform providers LATAM Africa CIS SBC SiGMA 2025",
  "iGaming software platform providers India Southeast Asia 2024 2025",
  "casino platform aggregator B2B iGaming EGR awards 2024 2025"
]'
```

Extract company names. Remove:
- Pure operators/casinos (B2C brands)
- Game studios (slots/live dealer content)
- Pure payment processors
- US-primary companies
- Companies with 500+ employees (enterprise out of ICP)

Target: ~110 unique companies → trim to 100.

Compile as JSON array:
```json
[
  {"company": "EveryMatrix", "website": "https://everymatrix.com", "region": "EU"},
  {"company": "SOFTSWISS", "website": "https://softswiss.com", "region": "EU/CIS"},
  ...
]
```

---

## Step 2 — Run research in batches

Split the 100-company list into batches of 20–25. Run one batch at a time to avoid Tavily rate limits.

```bash
python tools/generate_market_map.py --leads '[
  {"company": "EveryMatrix", "website": "https://everymatrix.com", "region": "EU"},
  ... (20–25 companies)
]' --workers 2 --research-only > .tmp/batch_1_research.json
```

Repeat for each batch. Save to `.tmp/batch_2_research.json`, etc.

**Rate limit note:** If Tavily returns errors, drop to `--workers 1` or wait 60 seconds between batches.

---

## Step 3 — Synthesize processor + size from research JSON

After each batch, Claude reads the research JSON and extracts:

**For each company:**
- **Payment Processor(s):** Named processors found in search results or scraped pages. Examples: Nuvei, Paysafe, Worldpay, SafeCharge, CoinsPaid, NowPayments, Paycos, Stripe, Adyen, Skrill, Trustly. Write "Not found" if none detected.
- **HQ / Region:** Country or region (e.g. "Malta, EU", "LATAM", "Israel")
- **Est. Size:** Employee range or funding tier (e.g. "50–200", "Series A", "200+")

Build synthesized rows as JSON:
```json
[
  {
    "company": "EveryMatrix",
    "website": "https://everymatrix.com",
    "region": "Malta, EU",
    "size": "500+",
    "processors": "Nuvei, Paysafe, Worldpay"
  },
  ...
]
```

---

## Step 4 — Export to XLSX

Once all batches are synthesized into a single rows array, export:

```bash
python tools/generate_market_map.py --rows-json '[...full array...]' --output .tmp/market_map_v1.xlsx
```

Output: `.tmp/market_map_YYYYMMDD_HHMMSS.xlsx`

---

## Step 5 — Fill manual columns

Open the XLSX. Amber columns are for manual entry:
- **Contact Known:** Name(s) in Roman's network at that company (from LinkedIn, events, intros)
- **Talked To:** Name and date of any conversation that happened
- **Status:** Current pipeline status
- **Notes:** Any freeform context (hot lead, wrong ICP, intro pending, etc.)

---

## Refreshing the Map

Refresh quarterly or after major industry events (SBC, SiGMA, ICE):
1. Run new Tavily searches to find companies founded since last refresh
2. For existing entries where processor info is stale, re-run just those companies
3. Re-export XLSX, manually merge updates from the previous version's manual columns

---

## Files Used

| File | Purpose |
|---|---|
| `tools/generate_market_map.py` | Research + XLSX export |
| `tools/search_web.py` | Discovery queries to compile company list |
| `workflows/find_igaming_platforms.md` | ICP definition and seed companies |
| `blacklist.csv` | Existing contacts (useful as input, not for exclusion here) |
