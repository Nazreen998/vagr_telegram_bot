import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -------- ENV VARIABLES --------
SERVICE_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

if not SERVICE_JSON:
    raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON not set")

if not SHEET_ID:
    raise RuntimeError("GOOGLE_SHEET_ID not set")

# -------- AUTH --------
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
sheet = gc.open_by_key(SHEET_ID).sheet1


# -------- SAVE ORDER --------
def save_order_to_sheet(order):
    """
    order = {
        name, area, area_group,
        items(list[str]), total,
        date, slot, vehicle, driver
    }
    """

    order_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    items_text = "\n".join(order["items"])

    row = [
        order_time,                 # Order Time
        order["name"],              # Customer Name
        order["area"],              # Area
        order["area_group"],        # Area Group
        items_text,                 # Items
        order["total"],             # Total
        order["date"],              # Date
        order["slot"],              # Slot
        order["vehicle"],           # Vehicle
        order["driver"]             # Driver
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")
