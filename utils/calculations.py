def calculate_total(cart):
    return sum(item["total"] for item in cart)
