from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from products import get_products_by_category

# ================= CATEGORY CLICK =================
async def category_click(update, context):
    q = update.callback_query
    await q.answer()

    selected_cat = q.data.replace("cat_", "")

    df = get_products_by_category(selected_cat)

    if df.empty:
        await q.edit_message_text("❌ No products found")
        return

    keyboard = []

    for _, row in df.iterrows():
        keyboard.append([
            InlineKeyboardButton(
                row["Product Name"],
                callback_data=f"prod_{row['Product Name']}"
            )
        ])

    await q.edit_message_text(
        f"🛒 *{selected_cat} Products:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
