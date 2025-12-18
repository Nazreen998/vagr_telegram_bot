import sqlite3
import json
import os
print("DB PATH =", os.path.abspath("slots.db"))

# ===================== DB CONNECTION =====================
conn = sqlite3.connect("slots.db", check_same_thread=False)
cur = conn.cursor()


# ===================== INIT DATABASE =====================
def init_db():
    # -------- BOOKINGS TABLE --------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        area TEXT,
        area_group TEXT,
        amount REAL,
        date TEXT,
        slot TEXT,
        vehicle TEXT,
        driver TEXT,
        items TEXT,
        status TEXT
    )
    """)

    # -------- WAITING QUEUE TABLE --------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS waiting_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        area TEXT,
        area_group TEXT,
        amount REAL,
        date TEXT,
        slot TEXT,
        items TEXT
    )
    """)

    conn.commit()


# ===================== ADD DIRECT BOOKING =====================
def add_booking(
    name,
    area,
    area_group,
    amount,
    date,
    slot,
    vehicle,
    driver,
    items,
    status="CONFIRMED"
):
    cur.execute("""
        INSERT INTO bookings
        (name, area, area_group, amount, date, slot, vehicle, driver, items, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        area,
        area_group,
        amount,
        date,
        slot,
        vehicle,
        driver,
        json.dumps(items),
        status
    ))
    conn.commit()


# ===================== GET BOOKED VEHICLES =====================
def get_booked_vehicles(date, slot):
    cur.execute(
        "SELECT vehicle FROM bookings WHERE date=? AND slot=?",
        (date, slot)
    )
    rows = cur.fetchall()
    return [r[0] for r in rows]


# ===================== ADD TO WAITING QUEUE =====================
def queue_order(
    name,
    area,
    area_group,
    amount,
    items,
    date,
    slot
):
    cur.execute("""
        INSERT INTO waiting_queue
        (name, area, area_group, amount, date, slot, items)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        area,
        area_group,
        amount,
        date,
        slot,
        json.dumps(items)
    ))
    conn.commit()


# ===================== GET WAITING ORDERS =====================
def get_waiting_orders(area_group):
    cur.execute("""
        SELECT name, area, amount, items, date, slot
        FROM waiting_queue
        WHERE area_group=?
    """, (area_group,))

    rows = cur.fetchall()

    total = sum(r[2] for r in rows)
    count = len(rows)

    orders = []
    for r in rows:
        orders.append({
            "name": r[0],
            "area": r[1],
            "amount": r[2],
            "items": json.loads(r[3]),
            "date": r[4],
            "slot": r[5]
        })

    return {
        "total": total,
        "count": count,
        "orders": orders
    }


# ===================== CLEAR WAITING GROUP =====================
def clear_waiting_group(area_group):
    cur.execute(
        "DELETE FROM waiting_queue WHERE area_group=?",
        (area_group,)
    )
    conn.commit()
