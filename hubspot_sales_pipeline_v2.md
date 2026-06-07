# GatewayCrypto — HubSpot Sales Pipeline

## Context

Primary sales pipeline for GatewayCrypto. Tracks all leads from initial sourcing through to live client, regardless of how they entered. Leads come from any lead source.

---

## Stages (in order)

| # | Stage | What it means |
|---|-------|---------------|
| 1 | **Lead Stack** | Raw, unworked leads in the queue. No evaluation or outreach has happened yet. |
| 2 | **Qualification** | Actively being evaluated for ICP fit. |
| 3 | **MQL** | Passed qualification. Initial contact made or intent shown — waiting on real engagement. |
| 4 | **SQL** | Engaged and ready for a sales conversation. Real back-and-forth is live. |
| 5 | **Pushing** | Demo done. Active deal in motion — driving toward close. |
| 6 | **Compliance** | Closed, KYB in process. |
| 7 | **Client** | Merchant is live on GatewayCrypto. Terminal stage. |
| 8 | **Lost** | Disqualified or dropped at any stage. Loss reason must be logged. |

---

## Final Pipeline Flow

```
Lead Stack → Qualification → MQL → SQL → Pushing → Compliance → Client
```

Every stage can exit to Lost. Loss reason required before moving.

---

## Notes

**ICP**

C2B merchants and platforms with real transaction volume that need to accept crypto payments, convert crypto to fiat, or both.

Minimum bar:
- Operates a business that processes payments (not an individual)
- Meaningful transaction volume (low turnover is a disqualifier)
- Can pass KYB
- Genuine use case for crypto acceptance, off-ramp, or both

**Lead sources**
- LinkedIn — responded to outreach, showed genuine interest
- Own — sourced directly, outside LinkedIn
- Inbound — reached out to us first
- Referral — introduced by a partner or existing client

**Stage detail**

Lead Stack
- Entry: Added to HubSpot via any source
- Exit: Opened and reviewed
- Trigger: Pulled for evaluation → Qualification

Qualification — what you're checking: meaningful transaction volume? Clear use case for crypto or off-ramp? Likely to pass KYB? A real business, not an individual?
- Entry: Pulled from Lead Stack
- Exit: ICP decision made
- Trigger: Fits ICP → MQL | Off-target → Lost (Off Target or Low Turnover)

MQL
- Entry: ICP confirmed + one of: outreach sent / inbound received / LinkedIn reply
- Exit: Meaningful reply showing real interest (not a courtesy response)
- Trigger: Genuine engagement → SQL | No response after full sequence → Lost

SQL
- Entry: Meaningful two-way dialogue — questions, interest, or call agreed
- Exit: Demo done + strong fit confirmed + clear timeline (all three required)
- Trigger: All three met → Pushing | Goes cold → Lost

Pushing — activities: pricing and commercial terms, integration scoping (API or Backoffice), legal sign-off
- Entry: Demo done + fit confirmed + timeline real
- Exit: Agreement reached and KYB initiated, or deal collapses
- Trigger: Agreement reached → Compliance | Collapses → Lost (reason required)

Compliance
- Entry: Deal agreed, KYB process initiated
- Exit: KYB approved, or KYB refused/failed
- Trigger: KYB approved → Client | KYB refused/failed → Lost (Refused/Failed KYB)

Client
- Entry: KYB approved + onboarding complete (API integrated or Backoffice active)
- Exit: N/A — terminal stage

Lost — may be reactivated manually if circumstances change
- Entry: Deal inactive or disqualified, reason logged
- Exit: N/A

**Lost reasons**
- Price — rates or fees don't work
- In-house solution — building or already built their own processing
- External solution — chose a competitor
- Missing feature/functionality — GWC can't support their requirement
- Refused/Failed KYB — did not pass compliance
- Low turnover — volume too low to make sense commercially
- Off target — wrong profile, never should have been in the pipeline
