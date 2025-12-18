import os
from fastapi import FastAPI, Request
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from database import init_db

# -------- HANDLERS --------
from handlers.start import start
from handlers.category import category_click
from handlers.product import product_click
from handlers.cart import quantity_input, change_qty_prompt
from handlers.checkout import (
    add_more,
    checkout,
    confirm_order,
    edit_order,
    edit_item,
    remove_item,
)
from handlers.booking import (
    ask_name,
    agency_select,
    date_select,
    slot_select
)
from handlers.text_router import text_router

# -------- FASTAPI --------
app = FastAPI()
telegram_app = ApplicationBuilder().token(TOKEN).build()


@app.on_event("startup")
async def startup():
    init_db()

    # START
    telegram_app.add_handler(CommandHandler("start", start))

    # CATEGORY / PRODUCT
    telegram_app.add_handler(CallbackQueryHandler(category_click, "^cat_"))
    telegram_app.add_handler(CallbackQueryHandler(product_click, "^prod_"))

    # CART
    telegram_app.add_handler(CallbackQueryHandler(add_more, "^add_more$"))
    telegram_app.add_handler(CallbackQueryHandler(checkout, "^checkout$"))
    telegram_app.add_handler(CallbackQueryHandler(edit_order, "^edit_order$"))
    telegram_app.add_handler(CallbackQueryHandler(edit_item, "^edit_item_"))
    telegram_app.add_handler(CallbackQueryHandler(change_qty_prompt, "^change_qty$"))
    telegram_app.add_handler(CallbackQueryHandler(remove_item, "^remove_item$"))
    telegram_app.add_handler(CallbackQueryHandler(confirm_order, "^confirm_order$"))

    # BOOKING
    telegram_app.add_handler(CallbackQueryHandler(ask_name, "^confirm_order$"))
    telegram_app.add_handler(CallbackQueryHandler(agency_select, "^agency_"))
    telegram_app.add_handler(CallbackQueryHandler(date_select, "^date_"))
    telegram_app.add_handler(CallbackQueryHandler(slot_select, "^slot_"))

    # TEXT INPUT (SAFE)
    telegram_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_router)
    )

    await telegram_app.initialize()
    await telegram_app.start()
    print("🚀 Bot Ready (Webhook Mode)")


@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()
    await telegram_app.update_queue.put(update)
    return {"ok": True}


@app.get("/")
def health():
    return {"status": "running"}
