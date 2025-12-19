async def text_router(update, context):
    from handlers.cart import quantity_input
    await quantity_input(update, context)
