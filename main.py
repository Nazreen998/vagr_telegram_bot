# main.py
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN

# HANDLERS
from handlers.start import start
from handlers.category import category_click
from handlers.product import product_click
from handlers.cart import change_qty_prompt
from handlers.checkout import (
    add_more,
    checkout,
    edit_order,
    edit_item,
    remove_item,
    finish_order,
)
from handlers.agency import agency_select
from handlers.text_router import text_router

app = FastAPI()

telegram_app = ApplicationBuilder().token(TOKEN).build()

@app.on_event("startup")
async def startup():
    telegram_app.add_handler(CommandHandler("start", start))

    telegram_app.add_handler(CallbackQueryHandler(category_click, "^cat_"))
    telegram_app.add_handler(CallbackQueryHandler(product_click, "^prod_"))

    telegram_app.add_handler(CallbackQueryHandler(add_more, "^add_more$"))
    telegram_app.add_handler(CallbackQueryHandler(checkout, "^checkout$"))
    telegram_app.add_handler(CallbackQueryHandler(edit_order, "^edit_order$"))
    telegram_app.add_handler(CallbackQueryHandler(edit_item, "^edit_item_"))
    telegram_app.add_handler(CallbackQueryHandler(change_qty_prompt, "^change_qty$"))
    telegram_app.add_handler(CallbackQueryHandler(remove_item, "^remove_item$"))

    telegram_app.add_handler(CallbackQueryHandler(agency_select, "^agency_"))
    telegram_app.add_handler(CallbackQueryHandler(finish_order, "^finish_order$"))

    telegram_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_router)
    )

    await telegram_app.initialize()
    print("🤖 Telegram Bot Initialized (Webhook mode)")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    await telegram_app.process_update(update)
    return {"ok": True}

@app.get("/")
def health():
    return {"status": "running"}
