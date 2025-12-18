import pandas as pd
import os


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
        "Name": name,
        "Area": area,
        "Area Group": area_group,
        "Items": items_text,
        "Total Amount": total,
        "Date": date,
        "Slot": slot,
        "Vehicle": vehicle,
        "Driver": driver
    }

    # If file exists → read
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        # Create new DataFrame
        df = pd.DataFrame(columns=row.keys())

    # ✅ Pandas 2.x SAFE WAY (NO append)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # Save back
    df.to_excel(EXCEL_FILE, index=False)
