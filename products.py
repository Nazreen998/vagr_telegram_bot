import pandas as pd

try:
    products = pd.read_excel("products.xlsx")
except Exception as e:
    raise RuntimeError(f"Failed to load products.xlsx: {e}")

products.columns = [col.strip() for col in products.columns]
products["Category"] = products["Category"].ffill()

# ===================== GET CATEGORIES =====================
def get_categories():
    return sorted(products["Category"].dropna().unique())

# ===================== GET PRODUCTS IN A CATEGORY =====================
def get_products_by_category(category):
    return products[products["Category"] == category]

# ===================== GET PRICE FOR PRODUCT =====================
def get_price(product_name):
    row = products[products["Product Name"] == product_name]
    if row.empty:
        return None
    return float(row.iloc[0]["Price"])
