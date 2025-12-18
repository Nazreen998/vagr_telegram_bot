from datetime import datetime, timedelta

async def delivery_reminder(context):
    await context.bot.send_message(
        context.job.chat_id,
        "🔔 Reminder: Your delivery will start soon 🚚"
    )

def get_reminder_datetime(date_str, slot_str):
    """
    date_str example: '15 Jun 2025'
    slot_str example: '8:30 AM – 10:30 AM'
    """
    start_time = slot_str.split("–")[0].strip()
    delivery_dt = datetime.strptime(
        f"{date_str} {start_time}",
        "%d %b %Y %I:%M %p"
    )
    return delivery_dt - timedelta(hours=1)

def schedule_advanced_reminder(app, chat_id, date_str, slot_str):
    reminder_dt = get_reminder_datetime(date_str, slot_str)

    # Don't schedule past reminders
    if reminder_dt <= datetime.now():
        return

    app.job_queue.run_once(
        delivery_reminder,
        when=reminder_dt,
        chat_id=chat_id,
        name=f"reminder_{chat_id}"
    )
