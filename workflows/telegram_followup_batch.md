# Telegram Follow-Up Batch — Workflow

## Objective

Given a batch of stalled Telegram (or LinkedIn DM) conversations, produce a ready-to-send follow-up message for each — in one pass. Output is a numbered list Roman can work through sequentially without drafting anything himself.

---

## Required inputs

For each conversation, provide:
- **Name**: who you're messaging
- **Relationship type**: lead / partner / team
- **Last message sent**: what you said (or what they said last)
- **Days since last contact**: approximate
- **Goal of follow-up**: move to call / get a reply / share an update / other

Minimum required: name + relationship type + days since last contact. The more context, the better the draft.

**Preferred input format** (paste one block per person):

```
Name: [First Last]
Type: [lead / partner / team]
Last contact: [X days ago]
Last message: [what was said — 1–2 sentences]
Goal: [what you want from this message]
```

---

## Step 1 — Process each entry

For each conversation, determine:

| Field | How to calibrate |
|---|---|
| Tone | Lead → professional but human. Partner → warm, peer-level. Team → direct, no formalities. |
| Urgency frame | < 7 days: light nudge. 7–14 days: casual check-in with a reason. > 14 days: re-open with value, not guilt. |
| Length | Leads: 2–4 sentences. Partners/team: 1–3 sentences. |
| Opening | Never "just checking in". Lead with something specific. |

---

## Step 2 — Draft all messages

Write all follow-ups in a single output block, numbered to match the input order.

### Tone guidelines by relationship type

**Lead (cold or warm)**
- Re-anchor to their context or something relevant that happened (news, market event, your product update)
- Do not re-pitch from scratch — they've already been introduced to GatewayCrypto
- Soft exit option: "No worries if the timing's off — happy to revisit when it makes sense."
- Never: "I wanted to follow up on my previous message"

**Partner (active or potential)**
- Peer-level — not sales-y
- Reference something shared: a past conversation point, a mutual goal, a recent industry event
- Forward-looking: "wanted to share something" / "had a thought on X" / "quick update your way"
- Never: "Hope you're well" as the opener

**Team**
- Ultra-direct — no opener formalities
- State what you need or what's happening in the first sentence
- One ask or update per message
- Never: sign-offs, pleasantries, or anything that reads like an email

---

## Step 3 — Output format

```
Follow-up batch — [date or session label]

1. [Name] ([type] — [X days])
[Message text]

2. [Name] ([type] — [X days])
[Message text]

[...]

---
Notes:
- [Any flags: e.g., "Lead #3 may be in a competing vendor situation — see if they confirm before pushing further"]
- [Any entries skipped and why]
```

---

## Anti-patterns

- "Just following up" — never, ever
- "I wanted to circle back" — cut
- "As per my last message" — never
- Re-pitching the full product to a lead who already engaged
- Using the same opener across multiple messages in the same batch
- Messages longer than 4 sentences for a follow-up
- Guilt-tripping: "I haven't heard back from you" — don't frame silence as their failure
