# booking.py
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import AGENCY_LOCATION_MAP
from google_sheets import save_order_to_sheet
from config import SLOTS, VEHICLES, DRIVERS, AREA_GROUPS
from database import (
    add_booking,
    get_booked_vehicles,
    queue_order,
    get_waiting_orders,
    clear_waiting_group
)

# ===================== ASK AGENCY =====================
async def ask_name(update, context):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"agency_{name}")]
        for name in AGENCY_LOCATION_MAP.keys()
    ]

    context.user_data["stage"] = "select_agency"

    await q.edit_message_text(
        "🏪 *Select your Agency:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===================== AGENCY SELECT =====================
async def agency_select(update, context):
    q = update.callback_query
    await q.answer()

    agency = q.data.replace("agency_", "")
    location = AGENCY_LOCATION_MAP.get(agency, "")

    context.user_data["name"] = agency
    context.user_data["area"] = agency
    context.user_data["location"] = location

    # FIND AREA GROUP
    selected_group = None
    for grp, arr in AREA_GROUPS.items():
        if agency.lower() in arr:
            selected_group = grp
            break

    context.user_data["area_group"] = selected_group or "UNKNOWN"

    # SHOW DATE BUTTONS
    keyboard = [
        [InlineKeyboardButton(
            (datetime.now().date() + timedelta(days=i)).strftime("%d %b %Y"),
            callback_data=f"date_{i}"
        )]
        for i in range(7)
    ]

    await q.edit_message_text(
        f"📍 *Location auto filled*\n\n"
        f"🏪 Agency: *{agency}*\n"
        f"🗺 [Open Map]({location})\n\n"
        "📅 *Select delivery date:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===================== DATE SELECT =====================
async def date_select(update, context):
    q = update.callback_query
    await q.answer()

    idx = int(q.data.replace("date_", ""))
    date_str = (datetime.now().date() + timedelta(days=idx)).strftime("%d %b %Y")

    context.user_data["date"] = date_str

    keyboard = [
        [InlineKeyboardButton(slot, callback_data=f"slot_{key}")]
        for key, slot in SLOTS.items()
    ]

    await q.edit_message_text(
        f"📅 *Date:* {date_str}\n\n🕒 *Select delivery slot:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===================== SLOT SELECT =====================
async def slot_select(update, context):
    q = update.callback_query
    await q.answer()

    if "name" not in context.user_data or "area" not in context.user_data:
        await q.edit_message_text("❗ Please select agency first.")
        return

    cart = context.user_data.get("cart", [])
    if not cart:
        await q.edit_message_text("🛒 Cart is empty")
        return

    slot_key = q.data.replace("slot_", "")
    slot_value = SLOTS.get(slot_key)
    context.user_data["slot"] = slot_value

    total = sum(item["total"] for item in cart)

    # ================= DIRECT CONFIRM =================
    if total >= 80000:
        await assign_trip(update, context)
        return

    # ================= WAITING QUEUE =================
    queue_order(
        context.user_data["name"],
        context.user_data["area"],
        context.user_data["area_group"],
        total,
        cart,
        context.user_data["date"],
        slot_value
    )

    waiting = get_waiting_orders(context.user_data["area_group"])

    if waiting["total"] >= 80000 or waiting["count"] >= 3:
        await auto_assign_group(update, context, context.user_data["area_group"])
        return

    await q.edit_message_text(
        f"⏳ *Order added to waiting queue*\n\n"
        f"🏘 Group: *{context.user_data['area_group']}*\n"
        f"💰 Group Total: ₹{waiting['total']}\n"
        f"🛒 Orders: {waiting['count']}\n\n"
        "🚚 Vehicle will be assigned soon.",
        parse_mode="Markdown"
    )

    context.user_data.clear()


# ===================== DIRECT TRIP ASSIGN =====================
async def assign_trip(update, context):
    date = context.user_data["date"]
    slot = context.user_data["slot"]
    cart = context.user_data["cart"]

    booked = get_booked_vehicles(date, slot)
    vehicle = next((v for v in VEHICLES if v not in booked), None)
    driver = DRIVERS.get(vehicle, "Driver")

    total = sum(item["total"] for item in cart)

    # SAVE TO DATABASE
    add_booking(
        context.user_data["name"],
        context.user_data["area"],
        context.user_data["area_group"],
        total,
        date,
        slot,
        vehicle,
        driver,
        cart
    )

    items_text = "\n".join(
        f"{i+1}. {item['product']} × {item['qty']} = ₹{item['total']}"
        for i, item in enumerate(cart)
    )

    # SAVE TO GOOGLE SHEET
    save_order_to_sheet({
        "name": context.user_data["name"],
        "area": context.user_data["area"],
        "area_group": context.user_data["area_group"],
        "items": [
            f"{item['product']} × {item['qty']} = ₹{item['total']}"
            for item in cart
        ],
        "total": total,
        "date": date,
        "slot": slot,
        "vehicle": vehicle,
        "driver": driver
    })

    msg = (
        "✅ *ORDER CONFIRMED* 🎉\n\n"
        f"🏪 Agency: *{context.user_data['name']}*\n"
        f"📍 Area: *{context.user_data['area']}*\n"
        f"🏘 Group: *{context.user_data['area_group']}*\n"
        "----------------------\n"
        "🧺 *Items:*\n"
        f"{items_text}\n"
        "----------------------\n"
        f"💰 *Total:* ₹{total}\n"
        f"📅 *Date:* {date}\n"
        f"🕒 *Slot:* {slot}\n"
        f"🚐 *Vehicle:* {vehicle}\n"
        f"👨‍✈️ *Driver:* {driver}"
    )

    await update.callback_query.edit_message_text(msg, parse_mode="Markdown")
    context.user_data.clear()


# ===================== AUTO ASSIGN GROUP =====================
async def auto_assign_group(update, context, group):
    data = get_waiting_orders(group)
    orders = data["orders"]

    vehicle = VEHICLES[0]
    driver = DRIVERS.get(vehicle, "Driver")

    for o in orders:
        save_order_to_sheet({
            "name": o["name"],
            "area": o["area"],
            "area_group": group,
            "items": [
                f"{item['product']} × {item['qty']} = ₹{item['total']}"
                for item in o["items"]
            ],
            "total": o["amount"],
            "date": o["date"],
            "slot": o["slot"],
            "vehicle": vehicle,
            "driver": driver
        })

    clear_waiting_group(group)

    await update.callback_query.edit_message_text(
        f"🚚 *Trip Created for Group {group}*\n"
        f"🚐 Vehicle: *{vehicle}*\n"
        f"👨‍✈️ Driver: *{driver}*",
        parse_mode="Markdown"
    )
