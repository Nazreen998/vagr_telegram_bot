import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SERVICE_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

if not SERVICE_JSON:
    raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON not set")

if not SHEET_ID:
    raise RuntimeError("GOOGLE_SHEET_ID not set")

creds_dict = json.loads(SERVICE_JSON)

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    creds_dict,
    scopes=scopes
)

gc = gspread.authorize(credentials)


def save_order_to_sheet(order):
    # ✅ OPEN SHEET INSIDE FUNCTION (SAFE)
    sheet = gc.open_by_key(SHEET_ID).sheet1

    order_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    items_text = "\n".join(order["items"])

    row = [
        order_time,
        order["name"],
        order["area"],
        order["area_group"],
        items_text,
        order["total"],
        order["date"],
        order["slot"],
        order["vehicle"],
        order["driver"]
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")
