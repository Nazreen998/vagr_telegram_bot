from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# SIMPLE AGENCY LIST
AGENCIES = [
    "ABHINAV AGENCY",
    "M.M AGENCY",
    "KUMAR AGENCY",
    "R.D AGENCY",
    "CHELLAM TRADERS"
]

async def ask_agency(update, context):
    q = update.callback_query
    await q.answer()

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"agency_{name}")]
        for name in AGENCIES
    ]

    await q.edit_message_text(
        "🏪 Select Agency:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def agency_select(update, context):
    q = update.callback_query
    await q.answer()

    agency = q.data.replace("agency_", "")
    context.user_data["agency"] = agency

    from handlers.checkout import finish_order
    await finish_order(update, context, agency)
