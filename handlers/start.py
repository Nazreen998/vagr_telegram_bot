from telegram import InlineKeyboardButton
from products import get_categories
from utils.keyboard import make_keyboard


async def start(update, context):
    if "cart" not in context.user_data:
        context.user_data["cart"] = []

    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat_{cat}")]
        for cat in get_categories()
    ]

    if update.message:
        await update.message.reply_text(
            "🙏 Welcome to ABHINAV AGENCY\n📦 Select Category:",
            reply_markup=make_keyboard(keyboard)
        )
    else:
        await update.callback_query.edit_message_text(
            "📦 Select Category:",
            reply_markup=make_keyboard(keyboard)
        )
