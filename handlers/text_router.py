# handlers/text_router.py

async def text_router(update, context):
    """
    Text input router.
    --------------------------------
    This project uses:
    ✅ BUTTONS for agency / date / slot
    ✅ TEXT only for quantity input
    --------------------------------
    """

    # All text messages are treated as quantity input
    from handlers.cart import quantity_input
    await quantity_input(update, context)
