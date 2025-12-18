def is_valid_quantity(text):
    try:
        qty = int(text)
        return qty > 0
    except:
        return False

def can_book_slot(booked_slots, slot):
    return slot not in booked_slots
