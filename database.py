import os
import json
import psycopg2
import psycopg2.extras

# ===================== DB CONNECTION =====================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

print("DB CONNECTING TO POSTGRES")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True


# ===================== INIT DATABASE =====================
def init_db():
    with conn.cursor() as cur:
        # -------- BOOKINGS TABLE --------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            name TEXT,
            area TEXT,
            area_group TEXT,
            amount DOUBLE PRECISION,
            date TEXT,
            slot TEXT,
            vehicle TEXT,
            driver TEXT,
            items JSONB,
            status TEXT
        )
        """)

        # -------- WAITING QUEUE TABLE --------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS waiting_queue (
            id SERIAL PRIMARY KEY,
            name TEXT,
            area TEXT,
            area_group TEXT,
            amount DOUBLE PRECISION,
            date TEXT,
            slot TEXT,
            items JSONB
        )
        """)


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
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bookings
            (name, area, area_group, amount, date, slot, vehicle, driver, items, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s)
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


# ===================== GET BOOKED VEHICLES =====================
def get_booked_vehicles(date, slot):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT vehicle FROM bookings WHERE date=%s AND slot=%s",
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
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO waiting_queue
            (name, area, area_group, amount, date, slot, items)
            VALUES (%s,%s,%s,%s,%s,%s,%s::jsonb)
        """, (
            name,
            area,
            area_group,
            amount,
            date,
            slot,
            json.dumps(items)
        ))


# ===================== GET WAITING ORDERS =====================
def get_waiting_orders(area_group):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("""
            SELECT name, area, amount, items, date, slot
            FROM waiting_queue
            WHERE area_group=%s
        """, (area_group,))
        rows = cur.fetchall()

    total = sum(float(r["amount"]) for r in rows)
    count = len(rows)

    orders = []
    for r in rows:
        orders.append({
            "name": r["name"],
            "area": r["area"],
            "amount": float(r["amount"]),
            "items": r["items"],
            "date": r["date"],
            "slot": r["slot"]
        })

    return {
        "total": total,
        "count": count,
        "orders": orders
    }


# ===================== CLEAR WAITING GROUP =====================
def clear_waiting_group(area_group):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM waiting_queue WHERE area_group=%s",
            (area_group,)
        )
