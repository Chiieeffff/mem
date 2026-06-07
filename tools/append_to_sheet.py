"""
Append rows to a Google Sheet.
Usage: python tools/append_to_sheet.py --rows '[{...}, {...}]' [--sheet-id SHEET_ID]

Rows are dicts with keys matching the header columns. Missing keys are written as empty.
On first run against an empty sheet, writes the header row automatically.

Auth: requires credentials.json in the repo root (downloaded from Google Cloud Console).
      Saves token.json after first OAuth flow — subsequent runs are non-interactive.

Output: JSON {appended: N, sheet_url: "..."}
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

REPO_ROOT = Path(__file__).parent.parent
CREDENTIALS_PATH = REPO_ROOT / "credentials.json"
TOKEN_PATH = REPO_ROOT / "token.json"

HEADERS = [
    "Date",
    "Category",
    "Company",
    "Headline",
    "Lead Potential",
    "Why It Matters",
    "Suggested Action",
    "Status",
    "Source URL",
]


def get_sheets_service():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print(
            "Error: Google API packages not installed. Run:\n"
            "  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib",
            file=sys.stderr,
        )
        sys.exit(1)

    if not CREDENTIALS_PATH.exists():
        print(
            f"Error: {CREDENTIALS_PATH} not found.\n"
            "Download it from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client IDs.\n"
            "Enable the Google Sheets API for the project first.",
            file=sys.stderr,
        )
        sys.exit(1)

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())

    return build("sheets", "v4", credentials=creds)


def append_rows(sheet_id: str, rows: list[dict]) -> dict:
    service = get_sheets_service()
    sheets = service.spreadsheets()

    # Check if sheet is empty (no header yet)
    result = sheets.values().get(spreadsheetId=sheet_id, range="A1:A1").execute()
    is_empty = "values" not in result

    values_to_write = []
    if is_empty:
        values_to_write.append(HEADERS)

    for row in rows:
        values_to_write.append([row.get(h, "") for h in HEADERS])

    sheets.values().append(
        spreadsheetId=sheet_id,
        range="A1",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": values_to_write},
    ).execute()

    appended_count = len(rows)
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    return {"appended": appended_count, "sheet_url": sheet_url}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", required=True, help="JSON array of row dicts")
    parser.add_argument(
        "--sheet-id",
        default=os.getenv("GOOGLE_SHEET_ID"),
        help="Google Sheet ID (defaults to GOOGLE_SHEET_ID in .env)",
    )
    args = parser.parse_args()

    if not args.sheet_id:
        print("Error: --sheet-id not provided and GOOGLE_SHEET_ID not set in .env", file=sys.stderr)
        sys.exit(1)

    try:
        rows = json.loads(args.rows)
    except json.JSONDecodeError as e:
        print(f"Error: --rows must be a valid JSON array: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(rows, list) or not rows:
        print("Error: --rows must be a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    result = append_rows(args.sheet_id, rows)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
