def calculate_total(cart):
    return sum(item["total"] for item in cart)

def apply_peak_charge(slot, total):
    if "8:30 PM" in slot:
        return total + 20
    return total
