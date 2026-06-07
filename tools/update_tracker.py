"""
Outreach tracker tool — generates a CSV for the master outreach tracker sheet.
The agent uploads the resulting CSV to Google Drive using the MCP tool.

Usage:
  python tools/update_tracker.py --leads '[
    {
      "name": "John Doe",
      "company": "SoftSwiss",
      "linkedin": "https://linkedin.com/in/johndoe",
      "touch": "T2",
      "status": "sent",
      "last_contact": "2026-05-15",
      "next_action": "Follow up T3 on 2026-05-22",
      "notes": "Replied with interest, asked about fees"
    }
  ]'

Output: CSV string to stdout, ready to upload as a Google Sheet.

Valid touch values: T1, T2, T3, T4, replied, call-booked, converted, dead
Valid status values: sent, replied, no-reply, interested, not-interested, dead, converted
"""

import argparse
import csv
import io
import json
import sys


VALID_TOUCHES = {"T1", "T2", "T3", "T4", "replied", "call-booked", "converted", "dead"}
VALID_STATUSES = {"sent", "replied", "no-reply", "interested", "not-interested", "dead", "converted"}

COLUMNS = ["Name", "Company", "LinkedIn", "Touch Stage", "Status", "Last Contact", "Next Action", "Notes"]


def build_csv(leads: list[dict]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    writer.writerow(["GatewayCrypto — Outreach Tracker"])
    writer.writerow([f"Last updated: {_today()}. {len(leads)} active lead(s)."])
    writer.writerow([])
    writer.writerow(COLUMNS)

    for lead in leads:
        writer.writerow([
            lead.get("name", ""),
            lead.get("company", ""),
            lead.get("linkedin", ""),
            lead.get("touch", ""),
            lead.get("status", ""),
            lead.get("last_contact", ""),
            lead.get("next_action", ""),
            lead.get("notes", ""),
        ])

    return output.getvalue()


def _today() -> str:
    from datetime import date
    return date.today().isoformat()


def validate_leads(leads: list[dict]) -> list[str]:
    errors = []
    for i, lead in enumerate(leads):
        if not lead.get("name"):
            errors.append(f"Lead {i}: missing 'name'")
        if not lead.get("company"):
            errors.append(f"Lead {i}: missing 'company'")
        touch = lead.get("touch", "")
        if touch and touch not in VALID_TOUCHES:
            errors.append(f"Lead {i} ({lead.get('name', '?')}): invalid touch '{touch}'. Valid: {sorted(VALID_TOUCHES)}")
        status = lead.get("status", "")
        if status and status not in VALID_STATUSES:
            errors.append(f"Lead {i} ({lead.get('name', '?')}): invalid status '{status}'. Valid: {sorted(VALID_STATUSES)}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--leads",
        required=True,
        help="JSON array of lead objects",
    )
    args = parser.parse_args()

    try:
        leads = json.loads(args.leads)
    except json.JSONDecodeError as e:
        print(f"Error: --leads must be a valid JSON array: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(leads, list) or not leads:
        print("Error: --leads must be a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    errors = validate_leads(leads)
    if errors:
        for err in errors:
            print(f"Validation error: {err}", file=sys.stderr)
        sys.exit(1)

    csv_output = build_csv(leads)
    print(csv_output, end="")


if __name__ == "__main__":
    main()
