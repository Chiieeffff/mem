# Outreach Tracker — Workflow

## Objective

Maintain a single master Google Sheet that shows the full state of all active GatewayCrypto outreach leads — touch stage, status, next action, and notes. This replaces the split between HubSpot and Google Sheets with one source of truth that can be updated in one command.

---

## Required inputs

For each lead to add or update:
- **name**: Full name
- **company**: Company name
- **linkedin**: LinkedIn profile URL (optional but recommended)
- **touch**: Which touch was last sent — one of: `T1`, `T2`, `T3`, `T4`, `replied`, `call-booked`, `converted`, `dead`
- **status**: Current state — one of: `sent`, `replied`, `no-reply`, `interested`, `not-interested`, `dead`, `converted`
- **last_contact**: Date of last message sent (YYYY-MM-DD)
- **next_action**: What to do next and when (plain text)
- **notes**: Anything relevant — replied content, objections, key details (optional)

**Shorthand input Roman can use:**
```
Name: John Doe
Company: SoftSwiss
Touch: T2
Status: replied
Last contact: 2026-05-15
Next action: Follow up T3 on May 22
Notes: Asked about integration time
```

---

## Step 1 — Build the lead list

Convert Roman's input into a JSON array for the tool. If updating existing leads, merge with any previously tracked data (ask Roman or read the current sheet if needed).

---

## Step 2 — Generate the CSV

```
python tools/update_tracker.py --leads '[
  {
    "name": "John Doe",
    "company": "SoftSwiss",
    "linkedin": "https://linkedin.com/in/johndoe",
    "touch": "T2",
    "status": "replied",
    "last_contact": "2026-05-15",
    "next_action": "Follow up T3 on 2026-05-22",
    "notes": "Asked about integration time"
  }
]'
```

Output is a CSV string.

---

## Step 3 — Upload or update the Google Sheet

**First time (no tracker sheet exists yet):**
Create a new Google Sheet in Roman's My Drive (parent: `0AP21eksGl4UGUk9PVA`) titled:
`GatewayCrypto — Outreach Tracker`

Use `mcp__claude_ai_Google_Drive__create_file` with `mimeType: text/csv`.

**Subsequent updates (sheet already exists):**
Read the current sheet ID from the previous session or ask Roman.
Use `mcp__claude_ai_Google_Drive__create_file` to create a new version (Google Drive auto-versions), or overwrite by re-creating with the same name.

After upload, return only the Google Sheet link.

---

## Status reference

| Status | Meaning |
|---|---|
| `sent` | Touch sent, no reply yet |
| `replied` | They replied — check touch stage for context |
| `no-reply` | Touch sent, no reply after expected window |
| `interested` | Expressed interest, conversation active |
| `not-interested` | Declined or disengaged |
| `dead` | No reply after T4, consider closed |
| `converted` | Deal done or meeting booked |

---

## Touch stage reference

| Touch | Meaning |
|---|---|
| `T1` | Connection request sent |
| `T2` | First DM after accept |
| `T3` | Follow-up |
| `T4` | Final pressure-point message |
| `replied` | They replied (any stage) |
| `call-booked` | Call or meeting scheduled |
| `converted` | Partnership confirmed |
| `dead` | Sequence complete, no response |

---

## Output checklist

- [ ] All leads have name, company, touch, and status filled
- [ ] Next action includes a specific date or trigger condition (not just "follow up")
- [ ] Google Sheet link returned after upload
- [ ] No lead left with status `sent` and a next_action older than 7 days (flag these to Roman)
