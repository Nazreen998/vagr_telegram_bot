from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from db.mongo import get_orders_collection

async def add_more(update, context):
    q = update.callback_query
    await q.answer()

    from products import get_categories

    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat_{cat}")]
        for cat in get_categories()
    ]

    await q.edit_message_text(
        "📦 Select category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def checkout(update, context):
    force_edit = context.user_data.pop("_force_edit", False)

    if update.callback_query:
        q = update.callback_query
        await q.answer()
        edit_fn = q.edit_message_text

    elif force_edit and context.user_data.get("last_summary_msg"):
        edit_fn = context.user_data["last_summary_msg"].edit_text

    else:
        msg = await update.message.reply_text("⏳ Updating order...")
        edit_fn = msg.edit_text

    cart = context.user_data.get("cart", [])

    if not cart:
        await edit_fn("🛒 Cart is empty")
        return

    text = "🧾 <b>Order Summary</b>\n\n"
    total = 0

    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['product']} × {item['qty']} = ₹{item['total']}\n"
        total += item["total"]

    text += f"\n💰 <b>Total: ₹{total}</b>"

    keyboard = [
        [InlineKeyboardButton("✏️ Edit Order", callback_data="edit_order")],
        [InlineKeyboardButton("➕ Add More", callback_data="add_more")],
        [InlineKeyboardButton("✅ Finish Order", callback_data="finish_order")]
    ]

    msg = await edit_fn(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # 🔥 STORE MESSAGE REF
    context.user_data["last_summary_msg"] = msg

async def edit_order(update, context):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton(
            f"{item['product']} × {item['qty']}",
            callback_data=f"edit_item_{i}"
        )]
        for i, item in enumerate(context.user_data["cart"])
    ]

    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="checkout")])

    await q.edit_message_text(
        "✏️ Select item to edit:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def edit_item(update, context):
    q = update.callback_query
    await q.answer()

    idx = int(q.data.replace("edit_item_", ""))
    context.user_data["edit_idx"] = idx

    keyboard = [
        [InlineKeyboardButton("✏️ Change Qty", callback_data="change_qty")],
        [InlineKeyboardButton("🗑 Remove", callback_data="remove_item")],
        [InlineKeyboardButton("🔙 Back", callback_data="edit_order")]
    ]

    item = context.user_data["cart"][idx]

    await q.edit_message_text(
        f"Editing: <b>{item['product']} × {item['qty']}</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def remove_item(update, context):
    q = update.callback_query
    await q.answer()

    idx = context.user_data.pop("edit_idx")
    context.user_data["cart"].pop(idx)

    if not context.user_data["cart"]:
        await q.edit_message_text("🛒 Cart is empty")
        return

    await checkout(update, context)

async def finish_order(update, context):
    q = update.callback_query
    await q.answer()

    cart = context.user_data.get("cart")
    agency = context.user_data.get("agency")

    if not cart or not agency:
        await q.edit_message_text("❌ Order data missing")
        return

    total = sum(item["total"] for item in cart)

    order_doc = {
        "agency": agency,
        "items": cart,
        "total": total,
        "created_at": datetime.utcnow()
    }

    orders_collection = get_orders_collection()
    orders_collection.insert_one(order_doc)

    text = "✅ <b>Order Confirmed</b>\n\n"
    text += f"🏪 <b>Agency:</b> {agency}\n\n"

    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['product']} × {item['qty']} = ₹{item['total']}\n"

    text += f"\n💰 <b>Total: ₹{total}</b>"

    context.user_data.clear()

    await q.edit_message_text(text, parse_mode="HTML")
