# LinkedIn Outreach — Workflow

## Objective

Produce a personalized 4-step LinkedIn outreach sequence for a GatewayCrypto iGaming partner lead.
Output is a Google Sheet in the user's My Drive, following the Maticz example format (Lead context + 4-step sequence table + Sources). Return the link in chat.

---

## Required inputs

- LinkedIn profile URL (or full name + company)
- Company website URL

If either is missing, ask once before proceeding.

---

## Step 1 — Research the lead

Run `tools/search_web.py` with the following queries (replace with actual name and company):

```
python tools/search_web.py --queries '[
  "\"Firstname Lastname\" LinkedIn post 2025 2026",
  "\"Firstname Lastname\" interview podcast iGaming SBC SiGMA iGB ICE 2025 2026",
  "\"CompanyName\" iGaming platform launch partnership 2025 2026",
  "\"CompanyName\" Crunchbase funding employees",
  "\"CompanyName\" CoinsPaid OR NowPayments OR BitPay OR Coinify OR Paycos"
]'
```

Run `tools/scrape_website.py` on the company website:

```
python tools/scrape_website.py --url https://companywebsite.com
```

Run both tools in parallel — they are independent.

---

## Step 2 — Extract lead context

From the research output, identify:

| Field | What to look for |
|---|---|
| Name | Full name (confirm spelling from LinkedIn URL slug) |
| Role | Current title and company |
| Company type | Map to ICP table (turnkey platform, white-label, build studio, crypto-native, etc.) |
| Hook | Best recent personal opinion: LinkedIn post → press quote → company launch. Last ~60 days preferred. |
| Existing payments vendor | If CoinsPaid / NowPayments / BitPay / Coinify / Paycos found → deprioritize lead, flag to user |
| Touch 4 feature | Select from selection guide below based on company type |

**ICP priority check** — skip if:
- Company is US-based or primarily serves a US client base
- Company is sweepstakes-only
- Company operates in China or any sanctioned country: Iran, Russia, North Korea, Eritrea, Syria, Cuba, Belarus
- Lead role is: Sales, Marketing, HR, Ops, Account Manager, Customer Success

---

## Step 3 — Write the sequence

Follow the rules below exactly. The worked examples in `GatewayCrypto_LinkedIn_SOP_v2.md` are the quality benchmark.

### Touch 1 — Connection request (Day 0)
- **Length**: ~12–15 words
- **Pattern**: `Hey [First], your "[specific recent post / opinion / launch]" was [sharp / spot on / interesting]. Let's connect.`
- Pull hook from their actual recent LinkedIn post, podcast, press quote, or company milestone
- **No pitch. No product mention.**

### Touch 2 — After accept (Day 2–3)
- **Length**: ~50–70 words
- **Pattern**: Acknowledge connect → tie back to their hook → describe partnership shape (their clients get crypto by default, they get a cut) → feature-specific proof point → soft ask
- **Each variant uses a different killer feature:**

| Variant | Killer feature | Pain addressed |
|---|---|---|
| A (recommended) | Reference partners — SoftGamings, TrueLabel, LYNON, GammaStack | Vendor risk |
| B | MultiChain unified balance | Fee bleed |
| C | Fast API — live within 24 hours | Integration speed |

- **Reference partners appear ONLY in Touch 2. They must not appear in Touch 3 or Touch 4.**

### Touch 3 — Follow-up (Day 7–10)
- **Length**: ~50–60 words
- **Pattern**: Lead with the concrete savings or time-to-value tied to the variant's feature. Tie to their context. Soft ask.
- **Reference partners must NOT appear in this touch.**
- **Each variant uses a different killer feature:**

| Variant | Killer feature | Pain addressed |
|---|---|---|
| A (recommended) | MultiChain unified balance | Fee bleed (~$20k/month, $240k/year, TRC20 → BEP20) |
| B | Fast API — live within 24 hours | Integration speed / dev cost |
| C | Company-type primary feature (Variant A from Touch 4 table) | Company-type pain |

### Touch 4 — Pressure point (Day 14–17)
- **Length**: ~50–60 words
- **Pattern**: Open with industry pressure framing → drop the relevant stat → soft exit ("won't keep nudging")
- **Reference partners must NOT appear in this touch.**
- **Each variant uses a different killer feature.** Select from the row matching the company type:

| Company type | Variant A (recommended) | Variant B | Variant C |
|---|---|---|---|
| Custom dev / build studio | Fast API — live within 24h (#6) | MultiChain unified balance (#2) | Zero chargebacks (#3) |
| Tier-1 regulated EU | AML / KYC / KYT (#9) | Near-perfect acceptance (#4) | Zero chargebacks (#3) |
| High-volume sportsbook | Instant payouts (#5) | Zero chargebacks (#3) | Near-perfect acceptance (#4) |
| Crypto-native / multi-coin | 700+ coins (#8) | MultiChain unified balance (#2) | Instant payouts (#5) |
| Card-payments dependent | Zero chargebacks (#3) | Near-perfect acceptance (#4) | MultiChain unified balance (#2) |

---

## Step 4 — Create the Google Sheet

Create a new Google Sheet in the user's My Drive (parent: `0AP21eksGl4UGUk9PVA`) titled:
`Sequence — [FirstName] [LastName] — [CompanyName]`

Upload as `text/csv` (auto-converts to Google Sheet) using the `mcp__claude_ai_Google_Drive__create_file` tool.

Use the following CSV structure — this matches the Maticz example format:

```
Recommended Sequence — [CompanyName]
4-step LinkedIn sequence for a GatewayCrypto iGaming partner lead. Each touch leans on a different killer feature; no repetition.

Lead context
Name,[value]
Role,[value]
Company,[value]
LinkedIn,[URL]
Personalization hook,[value]
Why he/she fits,[value]

The 4-step sequence
Step,Variant,Timing,Message,Killer feature,Pain addressed,Why it works
Touch 1 — Connection request,—,Day 0,[message],— (no pitch),Attention,[explanation ~1 sentence]
Touch 2 — After accept,A ★,Day 2–3,[message A],Reference partners,Vendor risk,[explanation ~1 sentence]
Touch 2 — After accept,B,Day 2–3,[message B],MultiChain unified balance,Fee bleed,[explanation ~1 sentence]
Touch 2 — After accept,C,Day 2–3,[message C],Fast API — live within 24h,Integration speed,[explanation ~1 sentence]
Touch 3 — Follow-up,A ★,Day 7–10,[message A],MultiChain unified balance,Fee bleed,[explanation ~1 sentence]
Touch 3 — Follow-up,B,Day 7–10,[message B],Fast API — live within 24h,Integration speed / dev cost,[explanation ~1 sentence]
Touch 3 — Follow-up,C,Day 7–10,[message C],[company-type primary feature],[company-type pain],[explanation ~1 sentence]
Touch 4 — Pressure point,A ★,Day 14–17,[message A],[feature A],[pain A],[explanation ~1 sentence]
Touch 4 — Pressure point,B,Day 14–17,[message B],[feature B],[pain B],[explanation ~1 sentence]
Touch 4 — Pressure point,C,Day 14–17,[message C],[feature C],[pain C],[explanation ~1 sentence]

Sources
Source,URL
[source name],[URL]
```

After creating the file, output only the Google Sheet link in chat.

---

## Output checklist (verify before delivering)

- [ ] Touch 1 references the lead's *own* recent published opinion or move — not a generic company fact
- [ ] Each variant (A/B/C) within a touch uses a *different* killer feature — no two variants of the same touch share the same feature
- [ ] Each touch is under ~80 words
- [ ] No corporate hedging ("are you the right person…", "wondering if it'd be useful…")
- [ ] Touch 3 has a concrete number ($20k/month, $240k/year, or another verified figure)
- [ ] Touch 4 is fresh-angle + soft exit ("won't keep nudging")
- [ ] Reference partners appear *only in Touch 2*
- [ ] Google Sheet created and link returned (not plain text in chat)

If any box is unchecked, revise before delivering.

---

## Anti-patterns (do not do)

- Pitching in the connection request
- Generic comp-shoutouts as "personalization"
- Repeating reference partners in Touch 3 or 4
- "Are you the right person to discuss this?" — cut
- Stacking 3–4 features into one message
- Multi-paragraph product summaries
- Pitching the lead as if they're the operator — they're a partner; operators are their clients
- Do not work with US-based companies or companies whose primary client base is US-facing
- Do not work with sweepstakes operators
- Do not target companies in China or sanctioned countries (Iran, Russia, North Korea, Eritrea, Syria, Cuba, Belarus)
