# main.py
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from handlers.booking import agency_select
from config import TOKEN
from database import init_db

# -------- SHOP FLOW HANDLERS --------
from handlers.start import start
from handlers.category import category_click
from handlers.product import product_click
# -------- CART & CHECKOUT --------
from handlers.cart import quantity_input, change_qty_prompt
from handlers.checkout import (
    add_more,
    checkout,
    confirm_order,
    edit_order,
    edit_item,
    remove_item,
)

# -------- BOOKING / AREA / CUSTOMER INFO --------
from handlers.booking import (
    ask_name,
    save_name,
    save_area,
    date_select,
    slot_select
)
from handlers.text_router import text_router

def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

   # ========== START ==========
    app.add_handler(CommandHandler("start", start))

# ========== CATEGORY / PRODUCT ========= =
    app.add_handler(CallbackQueryHandler(category_click, "^cat_"))
    app.add_handler(CallbackQueryHandler(product_click, "^prod_"))

# ========== CART ==========
    app.add_handler(CallbackQueryHandler(add_more, "^add_more$"))
    app.add_handler(CallbackQueryHandler(checkout, "^checkout$"))
    app.add_handler(CallbackQueryHandler(edit_order, "^edit_order$"))
    app.add_handler(CallbackQueryHandler(edit_item, "^edit_item_"))
    app.add_handler(CallbackQueryHandler(change_qty_prompt, "^change_qty$"))
    app.add_handler(CallbackQueryHandler(remove_item, "^remove_item$"))
    app.add_handler(CallbackQueryHandler(confirm_order, "^confirm_order$"))
    app.add_handler(CallbackQueryHandler(agency_select, "^agency_"))

# ========== BOOKING ==========
    app.add_handler(CallbackQueryHandler(date_select, "^date_"))
    app.add_handler(CallbackQueryHandler(slot_select, "^slot_"))

# ========== TEXT INPUT HANDLER (ONE ONLY) ==========
 # 🔥 ONLY ONE TEXT HANDLER
    app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    print("🚀 Bot Running Successfully…")
    app.run_polling()


if __name__ == "__main__":
    main()
