# HubSpot Pipeline Design — GatewayCrypto LinkedIn Outreach

## Context

This is a 4-touch LinkedIn outreach cadence targeting iGaming decision-makers for GatewayCrypto. The sequence spans ~17 days:

- **Day 0** — Connection request sent with a 12–15 word personalised note (T1)
- **Day 2–3** — Post-acceptance follow-up, 50–70 words, A/B/C variants (T2)
- **Day 7–10** — Concrete proof point follow-up with a specific number (T3)
- **Day 14–17** — Pressure point / soft exit message (T4)

Leads are pre-screened before entering, qualification happens before this pipeline. When a lead shows genuine interest at any stage, they move to the **Deals pipeline** for further development.

---

## Stages (in order)

| # | Stage | What it means |
|---|-------|---------------|
| 1 | **Leadstack** | Lead entered + sequence built; intake and research in one stage |
| 2 | **Connect** | T1 connection request (12–15 word note) sent — Day 0 |
| 3 | **Accepted** | Connection accepted, T2 not yet sent — awaiting follow-up |
| 4 | **Touch 1** | T2 sent — post-acceptance follow-up (50–70 words, Day 2–3) |
| 5 | **Touch 2** | T3 sent — concrete proof point follow-up (Day 7–10) |
| 6 | **Touch 3** | T4 sent — pressure point / soft exit (Day 14–17) |
| 7 | **Touch 4** | Optional 5th message or manual override touch |
| 8 | **Responded** | Lead replied — switch communication to Telegram |
| 9 | **Reject** | Final disposition — no response, wrong fit, or hard no. Create a task to follow up in 1 month; check reject reason before reaching out again. |

---

## Final Pipeline Flow

```
Leadstack → Connect → Accepted → Touch 1 → Touch 2 → Touch 3 → Touch 4 → Responded → Reject
```

Interested leads exit into the Deals pipeline at any stage. Responded is the manual handoff point — conversation moves to Telegram from here.

---

## Notes

- **Reject** should be a closed-lost stage in HubSpot with a reason property (No response, Hard no, Wrong fit, Competitor customer). If the reason is No response, create a 1-month follow-up task to re-evaluate — skip the task for Wrong fit or Competitor customer.
- **Responded** stops the LinkedIn sequence — no further automated touches once a lead is here.
- No changes to workflow scripts needed — these are purely CRM tracking stages.
