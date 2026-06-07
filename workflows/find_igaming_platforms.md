# Workflow: Find New iGaming Platform Prospects

## Objective
Find new B2B iGaming platform/technology companies that match GatewayCrypto's ideal customer profile (ICP). These are companies that build white-label casino or sportsbook platforms and need crypto payment infrastructure.

## Required Inputs
- `blacklist.csv` — companies to exclude (already contacted or not relevant)
- `icp_examples.csv` — reference companies (rows 1–84 with numbered entries)
- `suggested_companies.csv` — auto-generated; companies already returned in previous searches (exclude these too)

## ICP Definition
Target companies are **B2B iGaming platform and technology providers** with these traits:

**What they do:**
- Build white-label casino or sportsbook platforms for operators
- Provide turnkey iGaming solutions, aggregators, or platform-as-a-service
- Sell B2B software/platform to online gambling operators (NOT direct-to-player)

**What they are NOT:**
- Operators/casinos themselves (B2C gambling brands)
- Game content studios (slots, live dealer)
- Pure payment processors or fintech
- Forex/CFD brokers

**Size:** Mid-range to early-stage — from funded startups up to ~300 employees. NOT enterprise giants (SBTech, Kambi, Sportradar-scale). Startups are welcome, especially recently founded ones (2019–present).

**Regions to cover:** EU, LATAM, CIS, Africa, SE Asia, India, North America

**Reference companies (use as examples of ideal fit):**
1. ProgressPlay (progressplay.com) — EU
2. Salsa Technology (salsatechnology.com) — LATAM
3. FSB SportsTech (fsbtechnology.com) — EU/UK/US
4. Acesystems (acesystem.io) — Global
5. WA.Technology (watechnology.com) — EU/LATAM/Africa
6. Gamingtec (gamingtec.com) — EU/Global
7. SkillOnNet (skillonnet.com) — EU/Global
8. Relum (relum.com) — EU/CIS
9. InPlaySoft (inplaysoft.com) — Global
10. Ultraplay (ultraplay.co) — LatAm/Europe/SE Asia

## System Prompt Template

---

You are a B2B prospect researcher for GatewayCrypto — a crypto payment infrastructure provider for the iGaming industry.

**Your goal:** Find iGaming platform companies that are a strong fit for GatewayCrypto's services.

**Target profile (ICP):**
GatewayCrypto's ideal customers are B2B iGaming platform/technology providers — companies that build white-label casino or sportsbook platforms, turnkey iGaming solutions, or aggregator platforms for online gambling operators. They need crypto deposit/withdrawal infrastructure to offer their operator clients.

Examples of ideal-fit companies:
- ProgressPlay (EU) — white-label casino platform
- Salsa Technology (LATAM) — turnkey iGaming platform
- FSB SportsTech (EU/UK/US) — sports betting platform provider
- Acesystems (acesystem.io) — iGaming platform provider
- WA.Technology (EU/LATAM/Africa) — white-label betting platform
- Gamingtec (EU/Global) — turnkey iGaming solutions
- SkillOnNet (EU/Global) — online casino platform
- Relum (EU/CIS) — iGaming aggregator/platform
- InPlaySoft (Global) — sports betting software
- Ultraplay (LatAm/Europe/SE Asia) — sportsbook platform

**Do NOT suggest:**
- Online casinos or operators (B2C gambling brands)
- Game studios (slot/live dealer content providers)
- Payment processors or fintech companies
- Forex/CFD brokers
- Enterprise-scale platforms with 500+ employees or publicly traded status
- Companies that publicly list a native crypto payment solution on their website or in their product docs
- Companies headquartered or primarily operating in: **USA, China, Russia, Iran, North Korea, Belarus, Syria, Cuba, Venezuela** (compliance/sanctions restrictions — GatewayCrypto cannot serve these jurisdictions)
- Any company from the blacklist below

**Exclude ALL companies from these three lists — do not suggest any of them:**

1. Blacklist:
[PASTE blacklist.csv content here]

2. ICP reference companies (these are examples only, not targets):
ProgressPlay, Salsa Technology, FSB SportsTech, Acesystems, WA.Technology, Gamingtec, SkillOnNet, Relum, InPlaySoft, Ultraplay, GiG, Finnplay, Uplatform, iGP, White Hat Gaming, Altenar, Betby, Pronet Gaming, Tecpinion, BetStarters, 2WinPower, PlaylogiQ, BETINSPIRE, Bede Gaming, Bragg Gaming, TG.Casino Platform, TRUEiGTECH, OpenBet, InstaSoft, GAMING1, Bejoynd, Cybetic, Sportingtech, Gamanza, Platin Gaming, We Are Casino, LionGaming, Groove, Blue Ocean Gaming, Relum, EventGaming, 7777Gaming, EPlay24, AdwaBet, InPlaySoft, Skilrock, BetFounders, Quantum Gaming, Cubea, Elantil, IgPixel, TC Gaming, Bethero, Dstgaming, Ultraplay, Denchsolutions, Gaming-Ent, Togethergaming, Strive Gaming, 4Play Gaming, PieGaming, BetAlly, Aardvark Technologies, Maticz Technologies, KodeDice, Gambitec, Czar Gaming, Root Codex, TheCFox, iGcore, UningPlay, Blokotech, Creatiosoft, Rebel Live, Aqbay, Source Code Lab, Cactusgaming, Mobinc, Vegangster, Innovaplay, Mondo Gaming, Bet B2B, Gamingsoft, Digitain, Spinree, Acesystems

3. Previously suggested (auto-updated after each run):
[PASTE suggested_companies.csv content here if it exists]

**Before suggesting a company, check:**
- Does their website mention built-in crypto payments, crypto wallet, or blockchain integration? If yes — skip it.
- Are they a well-known enterprise platform (500+ employees, VC-backed at scale, publicly traded)? If yes — skip it.

**Output format for each suggested company:**
1. Company name
2. Website
3. LinkedIn URL
4. Region/HQ
5. Why it fits the ICP (1 sentence)
6. Estimated size (employees)
7. Crypto solution status: "No public crypto offering found" or explain if unsure

**Task:** Find [X] new companies similar to the ICP examples above. Focus on [REGION] if specified. Prioritize: (1) recently founded companies (2024–present), (2) companies that are growing but not yet widely known, (3) startups that have launched a platform but haven't built crypto infrastructure yet.

---

## Post-Processing (after AI returns results)

Once you have the list of companies from the AI, run these steps:

**Step 1 — Format and export to XLSX:**
```bash
python3 tools/export_prospects.py --input '<JSON_ARRAY_OF_COMPANIES>'
```
JSON format per company:
```json
{"name":"Company","website":"site.com","linkedin":"linkedin.com/company/...","region":"EU","why_fits":"...","size":"100","crypto_status":"No public crypto offering found"}
```
This will:
- Create `.tmp/prospects_YYYYMMDD_HHMMSS.xlsx`
- **Auto-append** all company names to `suggested_companies.csv` (excluded from future runs)

**Step 2 — Upload to Google Drive:**
Read the XLSX file as base64 and upload via `mcp__claude_ai_Google_Drive__create_file` with:
- `title`: e.g. `iGaming Prospects 2024-05-21`
- `contentMimeType`: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- `base64Content`: base64-encoded XLSX bytes

## How to Update
- **Add to blacklist:** Append company name to `blacklist.csv` after outreach
- **Change region focus:** Edit the `[REGION]` placeholder in the prompt
- **Change batch size:** Edit `[X]` in the prompt
- **Improve ICP:** Replace or add to the reference company list based on which ones convert best

## Notes
- The blacklist contains ~400+ unique companies (with duplicates — treat as unique set)
- Many original ICP examples are already in the blacklist (contacted): GiG, Finnplay, Uplatform, Altenar, Bede Gaming, Sportingtech, Gamanza, etc.
- GatewayCrypto itself is in the blacklist — correct
