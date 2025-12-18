# ===================== BOT TOKEN =====================
TOKEN = "8091821443:AAFdHoqYHsbegXG1sAWtCg_2KtT2W6_UEkY"
ADMIN_ID = 8091821443


# ===================== DELIVERY SLOTS =====================
SLOTS = {
    "S1": "8:30 AM – 10:30 AM",
    "S2": "12:30 PM – 2:30 PM",
    "S3": "4:30 PM – 6:30 PM",
    "S4": "8:30 PM – 10:30 PM",
}


# ===================== VEHICLES =====================
# SAME NAMES will be stored in DB
VEHICLES = [
    "TN 64 AD 4420",
    "TN 64 AD 4438",
    "TN 64 AD 4428",
    "TN 64 AD 4430",
]


# ===================== DRIVER MAPPING =====================
# Auto-assigned based on VEHICLE name
DRIVERS = {
    "TN 64 AD 4420": "ARUN",
    "TN 64 AD 4438": "KATHAVARAYAN",
    "TN 64 AD 4428": "VENKADESH",
    "TN 64 AD 4430": "SITHIK",
}


# ===================== AREA GROUPING =====================
# Your original list mapped into clusters
AREA_GROUPS = {
    "MELUR_SIDE": ["melur", "otthakadai", "pandikovil"],
    "CENTRAL": ["kalavasal", "southgate", "south gate"],
    "SOUTH": ["avaniyapuram"],
    "MATTUTHAVANI": ["mattuthavani", "pudhur", "puthur", "anna nagar", "annanagar", "kk nagar", "kknagar"],
}
