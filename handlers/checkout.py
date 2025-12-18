from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta


async def add_more(update, context):
    q = update.callback_query
    await q.answer()

    context.user_data.pop("edit_idx", None)
    context.user_data.pop("awaiting_new_qty", None)

    from handlers.start import start
    await start(q, context)


async def checkout(update, context):
    q = update.callback_query

    cart = context.user_data.get("cart", [])
    if not cart:
        if q:
            await q.edit_message_text("🛒 Cart is empty")
        else:
            await update.message.reply_text("🛒 Cart is empty")
        return

    text = "🧾 <b>Order Summary</b>\n\n"
    total = 0

    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['product']} × {item['qty']} = ₹{item['total']}\n"
        total += item["total"]

    text += f"\n💰 <b>Total: ₹{total}</b>"

    keyboard = [
        [InlineKeyboardButton("✏️ Edit Order", callback_data="edit_order")],
        [InlineKeyboardButton("✅ Confirm Order", callback_data="confirm_order")],
        [InlineKeyboardButton("➕ Add More", callback_data="add_more")]
    ]

    if q:
        await q.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

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
        "✏️ <b>Select item to edit:</b>",
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
        f"Editing:\n<b>{item['product']} × {item['qty']}</b>",
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

async def confirm_order(update, context):
    q = update.callback_query
    await q.answer()

    # 🔁 Redirect to Agency selection (BUTTON UI)
    from handlers.booking import ask_name

    await ask_name(update, context)
    return

