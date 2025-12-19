from telegram.ext import ContextTypes
from telegram import Update
from handlers.start import start as start_categories

async def agency_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    agency = q.data.replace("agency_", "")
    context.user_data["agency"] = agency

    # 👉 Now move to category selection
    from products import get_categories
    from utils.keyboard import make_keyboard
    from telegram import InlineKeyboardButton

    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat_{cat}")]
        for cat in get_categories()
    ]

    await q.edit_message_text(
        f"🏪 <b>{agency}</b> selected\n\n📦 Select category:",
        parse_mode="HTML",
        reply_markup=make_keyboard(keyboard)
    )
