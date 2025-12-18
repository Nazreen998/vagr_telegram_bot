from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import products


async def product_click(update, context):
    q = update.callback_query
    await q.answer()

    product = q.data.replace("prod_", "")
    context.user_data["product"] = product
    context.user_data["stage"] = "quantity"   # 🔥 IMPORTANT

    price = products.get_price(product)

    context.user_data.pop("awaiting_new_qty", None)
    context.user_data.pop("edit_idx", None)

    await q.edit_message_text(
        f"🛒 *{product}*\n"
        f"💰 Price: ₹{price}\n\n"
        f"✏️ Enter quantity:",
        parse_mode="Markdown"
    )
