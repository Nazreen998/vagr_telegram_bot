import os
import pandas as pd
from datetime import datetime

EXCEL_FILE = "orders.xlsx"


def save_order_to_excel(
    name,
    area,
    area_group,
    items_text,
    total,
    date,
    slot,
    vehicle,
    driver
):
    row = {
        "Order Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Customer Name": name,
        "Area": area,
        "Area Group": area_group,
        "Items": items_text,
        "Total Amount": total,
        "Date": date,
        "Slot": slot,
        "Vehicle": vehicle,
        "Driver": driver,
    }

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_excel(EXCEL_FILE, index=False)
