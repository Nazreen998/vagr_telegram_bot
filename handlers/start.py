from telegram import InlineKeyboardButton, InlineKeyboardMarkup

AGENCIES = [
    "VAGR AGENCY",
    "M.M AGENCY",
    "KUMAR AGENCY",
    "R.D AGENCY",
    "ABHINAV AGENCY"
]

async def start(update, context):
    context.user_data.clear()
    context.user_data["cart"] = []

    keyboard = [
        [InlineKeyboardButton(a, callback_data=f"agency_{a}")]
        for a in AGENCIES
    ]

    text = "🏪 Please select agency:"

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
