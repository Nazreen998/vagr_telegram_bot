from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from products import get_products_by_category, get_categories


# 🔥 SHOW CATEGORY LIST (for Add More)
async def show_categories(update, context):
    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat_{cat}")]
        for cat in get_categories()
    ]

    await update.edit_message_text(
        "📦 Select category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔥 CATEGORY CLICK → SHOW PRODUCTS
async def category_click(update, context):
    q = update.callback_query
    await q.answer()

    selected_cat = q.data.replace("cat_", "")
    df = get_products_by_category(selected_cat)

    if df.empty:
        await q.edit_message_text("❌ No products found")
        return

    keyboard = [
        [InlineKeyboardButton(
            row["Product Name"],
            callback_data=f"prod_{row['Product Name']}"
        )]
        for _, row in df.iterrows()
    ]

    await q.edit_message_text(
        f"🛒 <b>{selected_cat} Products:</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
