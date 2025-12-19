def is_valid_quantity(text):
    try:
        qty = int(text)
        return qty > 0
    except:
        return False
