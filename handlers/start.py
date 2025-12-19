from telegram import InlineKeyboardButton, InlineKeyboardMarkup

AGENCIES = [
    "ABHINAV AGENCY",
    "M.M AGENCY",
    "KUMAR AGENCY",
    "R.D AGENCY",
]

async def start(update, context):
    context.user_data.clear()
    context.user_data["cart"] = []

    keyboard = [
        [InlineKeyboardButton(a, callback_data=f"agency_{a}")]
        for a in AGENCIES
    ]

    await update.message.reply_text(
        "🏪 Please select agency:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
