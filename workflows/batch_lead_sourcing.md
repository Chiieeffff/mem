# Batch Lead Sourcing — Workflow

## Objective

Given a list of company names (or a company type to discover), research and score 5–10 iGaming leads in one pass. Output is a prioritized Google Sheet with fit scores, rationale, and recommended hook for each lead — ready for Roman to pick from and kick off outreach sequences.

---

## Required inputs

**Option A — Named companies** (Roman provides a list):
- Company names (required)
- Website URLs (optional — improves research quality)
- Contact name (optional — used to find LinkedIn profile)

**Option B — Discovery** (Roman provides a type):
- Company type: e.g., "white-label iGaming platforms", "crypto-native online casinos", "turnkey sportsbook providers"
- Target count: how many leads to find (default: 5–10)

If neither is provided, ask once.

---

## Step 1 — Compile the lead list

**If Option A:** Use the provided list directly. Go to Step 2.

**If Option B:** Run `tools/search_web.py` with discovery queries:
```
python tools/search_web.py --queries '[
  "[company type] iGaming SBC SiGMA iGB ICE 2025 platform provider",
  "[company type] iGaming company list Europe Malta Gibraltar",
  "top [company type] iGaming 2024 2025"
]'
```
Extract 8–12 company names from results, then proceed as Option A.

---

## Step 2 — Run batch research

Run `tools/batch_lead_sourcing.py` with the full lead list:

```
python tools/batch_lead_sourcing.py --leads '[
  {"company": "CompanyName", "website": "https://...", "contact": "First Last"},
  {"company": "CompanyName2", "website": "https://..."}
]' --workers 4
```

This runs web searches and site scrapes in parallel for all leads. Output is a JSON array with search results and scraped text per company.

---

## Step 3 — Score each lead

For each company in the output, evaluate against the ICP checklist:

### Automatic SKIP criteria (flag and exclude)
- US-based company or primary client base is US-facing
- Sweepstakes-only operator
- Operates in or primarily serves China, Iran, Russia, North Korea, Eritrea, Syria, Cuba, or Belarus
- Existing crypto payment vendor detected (CoinsPaid, NowPayments, BitPay, Coinify, Paycos) → downgrade to MEDIUM, flag as "existing vendor"
- Company is a content studio / game supplier only (not a platform) → wrong ICP type, mark as SKIP unless referral play makes sense

### Fit scoring
| Score | Criteria |
|---|---|
| HIGH | iGaming platform or white-label, no US focus, no competing vendor, clear crypto volume potential |
| MEDIUM | Partial fit — one concern (e.g., existing vendor, unclear jurisdiction, small scale) |
| LOW | Multiple concerns but not automatic skip |
| SKIP | Meets any automatic skip criterion |

### Hook identification
Identify the best personalization hook for each HIGH/MEDIUM lead:
- Recent LinkedIn post or press quote (preferred)
- Company milestone (launch, expansion, partnership)
- Industry event appearance (SBC, SiGMA, iGB, ICE)
- No hook found → note it; do not fabricate

---

## Step 4 — Create the Google Sheet

Create a new Google Sheet in Roman's My Drive (parent: `0AP21eksGl4UGUk9PVA`) titled:
`Lead Batch — [company type or date]`

Upload as `text/csv` using `mcp__claude_ai_Google_Drive__create_file`.

### CSV structure

```
Lead Batch — [company type or date]
Researched and scored [N] iGaming leads for GatewayCrypto outreach.

Leads
Rank,Company,Website,Contact,Fit Score,ICP Type,Competing Vendor,Hook,Why it fits,Flags,Recommended next step
1,[name],[url],[name or —],[HIGH/MEDIUM/LOW/SKIP],[type],[vendor or none],[hook text or none],[rationale],[flags or none],[sequence / skip / flag for review]
...

Skipped
Company,Reason
[name],[reason]

Sources
Source,URL
[source name],[URL]
```

After creating the file, return only the Google Sheet link.

---

## Output checklist (verify before delivering)

- [ ] All HIGH leads have a specific hook (not "N/A" or "none found" without a note)
- [ ] All SKIP leads have a clear reason
- [ ] No US-facing company marked as HIGH or MEDIUM
- [ ] Competing vendor flag applied where evidence exists
- [ ] Google Sheet created and link returned

---

## Rate limit note

Tavily API has rate limits on the free tier. If running more than 10 leads, space out tool calls or use `--workers 2` instead of 4. Do not run again without checking with Roman if the first run consumed significant API credits.
