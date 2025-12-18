async def text_router(update, context):
    stage = context.user_data.get("stage")

    if stage == "ask_name":
        from handlers.booking import save_name
        await save_name(update, context)
        return

    if stage == "ask_area":
        from handlers.booking import save_area
        await save_area(update, context)
        return

    # default = quantity input
    from handlers.cart import quantity_input
    await quantity_input(update, context)
