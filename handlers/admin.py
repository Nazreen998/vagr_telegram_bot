from telegram.ext import CommandHandler
from database import get_all_bookings

async def today_orders(update, context):
    bookings = get_all_bookings()
    if not bookings:
        await update.message.reply_text("No bookings yet")
        return

    text = "📋 All Bookings\n\n"
    for b in bookings:
        text += f"📅 {b[0]} | 🕒 {b[1]}\n"

    await update.message.reply_text(text)

def register_admin(app):
    app.add_handler(CommandHandler("orders", today_orders))
