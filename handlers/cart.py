from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import products

async def quantity_input(update, context):
    text = update.message.text.strip()

    # ===== EDIT QTY MODE =====
    if context.user_data.get("awaiting_new_qty"):
        try:
            qty = int(text)
            if qty <= 0:
                raise ValueError
        except:
            await update.message.reply_text("❌ Enter valid quantity")
            return

        idx = context.user_data["edit_idx"]
        item = context.user_data["cart"][idx]

        price = item.get("price", products.get_price(item["product"]))
        item["qty"] = qty
        item["price"] = price
        item["total"] = qty * price

        context.user_data.pop("awaiting_new_qty", None)
        context.user_data.pop("edit_idx", None)

        # 🔥 IMPORTANT FLAG
        context.user_data["_force_edit"] = True

        from handlers.checkout import checkout
        await checkout(update, context)
        return

    # ===== ADD MODE =====
    if "product" not in context.user_data:
        return

    try:
        qty = int(text)
        if qty <= 0:
            raise ValueError
    except:
        await update.message.reply_text("❌ Enter valid quantity")
        return

    product = context.user_data["product"]
    price = products.get_price(product)
    total = qty * price

    context.user_data.setdefault("cart", []).append({
        "product": product,
        "qty": qty,
        "price": price,
        "total": total
    })

    context.user_data.pop("product", None)

    await update.message.reply_text(
        f"✅ <b>Added to cart</b>\n\n"
        f"{product} × {qty} = ₹{total}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add More", callback_data="add_more")],
            [InlineKeyboardButton("🧾 Checkout", callback_data="checkout")]
        ])
    )

async def change_qty_prompt(update, context):
    q = update.callback_query
    await q.answer()

    context.user_data["awaiting_new_qty"] = True
    context.user_data.pop("product", None)

    await q.edit_message_text("✏️ Enter new quantity:")
