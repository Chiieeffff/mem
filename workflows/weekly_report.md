# Weekly Report — Workflow

## Objective

Collect weekly activity data across LinkedIn outreach, incoming leads, and optional exhibition coverage, then produce a formatted Google Doc report in the user's My Drive. Return the link in chat.

---

## Required inputs

- Week date range (e.g., "19–23 травня 2026")

If not provided, ask before proceeding. Everything else is collected interactively via the artifact.

---

## Step 1 — Open the report builder

Ask the user to open `weekly_report.html` in VSCode Preview:

> Відкрий `weekly_report.html` у VSCode: правий клік на файлі → **Open Preview** (або `Cmd+Shift+V` з відкритим файлом).

The artifact is self-contained — no install or server needed. The week range auto-fills to the current Mon–Fri; the user can adjust it.

---

## Step 2 — User fills in the artifact

The user fills in all relevant blocks:

- **LinkedIn** — requests sent, responses, meetings booked, key conversation notes
- **Вхідні ліди** — add lead cards (company, source, temperature, status, next step) and a general comment
- **Виставка** — toggle on only if there was an event; fill in name, dates, what was done, contacts, follow-up plan

When done, the user clicks **"Згенерувати звіт"**, then **"Копіювати"** and pastes the output into chat.

---

## Step 3 — Review and confirm

Read the pasted report. If any section looks incomplete or inconsistent (e.g., 0 leads but a comment referencing several), ask the user to clarify before creating the doc.

---

## Step 4 — Create the Google Doc

Create a new Google Doc in My Drive (parent: `0AP21eksGl4UGUk9PVA`) titled:
`Weekly Report — [week range]`

Upload as `text/plain` using the `mcp__claude_ai_Google_Drive__create_file` tool.

Use the following structure for the document body (plain text):

```
📋 WEEKLY REPORT — [дата початку] – [дата кінця]
════════════════════════════════════════════════

🔗 LINKEDIN
────────────────────────────────
Надіслано запитів:      [N]
Отримано відповідей:    [N] ([%])
Зустрічей заброньовано: [N]

Нотатки:
[key conversations text, or "—" if blank]


📥 ВХІДНІ ЛІДИ
────────────────────────────────
Всього: [N] | 🔴 Гарячих: [N] | 🟡 Теплих: [N] | 🔵 Холодних: [N]

[For each lead:]
[i]. [Компанія]
     Джерело: [source] · [temperature]
     Статус: [status]
     Наступний крок: [next step]

Коментар:
[leads comment, or "—" if blank]


🎪 ВИСТАВКА  ← include this section only if present
────────────────────────────────
Подія: [name]
Дати: [dates]

Що зроблено:
[done text]

Нових контактів: [N]
Ключові контакти:
[contacts list]

План follow-up:
[followup text]


════════════════════════════════════════════════
Згенеровано: [date and time]
```

After creating the file, return only the Google Doc link in chat.

---

## Output checklist (verify before delivering)

- [ ] Week date range is correct and matches what the user provided
- [ ] LinkedIn response rate matches sent/received numbers
- [ ] All lead cards are present and none are missing fields
- [ ] Виставка section is included only if the toggle was on
- [ ] Google Doc created and link returned

---

## Anti-patterns (do not do)

- Do not invent or estimate numbers — use exactly what the user provided
- Do not include the Виставка block if the toggle was off
- Do not add commentary, judgements, or recommendations to the report — it is a factual log
- Do not create the doc before the user has pasted the report text
