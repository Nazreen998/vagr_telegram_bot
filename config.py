import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


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
    "CENTRAL": ["kalavasal", "south gate"],
    "SOUTH": ["avaniyapuram"],
    "MATTUTHAVANI": ["mattuthavani", "pudhur", "anna nagar", "annanagar", "kk nagar", "kknagar"],
}
AGENCY_LOCATION_MAP = {
    "ABHINAV AGENCY": "https://maps.app.goo.gl/DN2zbZo6ceDdmvJWA",
    "M.M AGENCY": "https://maps.app.goo.gl/mMXT9vY3rzL7yXXZ8",
    "KUMAR AGENCY": "https://maps.app.goo.gl/75DDYYNLbb4EGbQXA",
    "R.D AGENCY": "https://maps.app.goo.gl/uydt7cuEELPTZ1kR8",
    "AMD & CO AGENCY": "https://maps.app.goo.gl/DehSJxKZ14MGCk9JA",
    "CHELLAM TRADERS": "https://maps.app.goo.gl/Pm2tSqBtjkTT4vX38",
    "SRI HARI AGENCY": "https://maps.app.goo.gl/RNeZkbPpR7G9HuaD7",
    "ANANTHALAKSHMI AGENCY": "https://maps.app.goo.gl/X6D7LD2J4qVymm6q8",
    "SREE AGENCY": "https://maps.app.goo.gl/TC3N6v3Fkw1P2o157",
    "VPR MARKETING GODOWN": "https://maps.app.goo.gl/uatPoUdMSndotiuf6",
    "VPR MARKETING HOUSE": "https://maps.app.goo.gl/zqabp87cgu7JN89r9",
    "SRI ALAGARMALAIYAN AGENCY": "https://maps.app.goo.gl/WzyGhkC51G5sqL1o6",
    "JF FOODS": "https://maps.app.goo.gl/qh6DUq4CBrC7Xq5r5",
    "BISMI AGENCY": "https://maps.app.goo.gl/1HGkQ4RWZSvMt8qs8",
    "FELINA AGENCY": "https://maps.app.goo.gl/W1p81chXMCYqbF7M8",
    "RAJAN AGENCY (K.K)": "https://maps.app.goo.gl/z4TP58jwNcCBwFEv5",
    "SRI VERA VELAVAN AGENCY": "https://maps.app.goo.gl/ynwBzTN96XNiwcKw9",
    "SRI VEERU CHINNAMMAL AGENCY": "https://maps.app.goo.gl/L97ApVkhtx2V2a4h9",
    "RAJAN AGENCY (CHOKKI)": "https://maps.app.goo.gl/zxQLN1ZSYPScz94r5",
    "SRI KARUPPASAMY AGENCY": "https://maps.app.goo.gl/Jvh1jP3wxyRUHEVF6",
    "STAR LUCENTS": "https://maps.app.goo.gl/R6Gnh3snCEoBUxCx9",
    "SUNDARAMAHALINGAM AGENCY": "https://maps.app.goo.gl/2JpwKN3eBCSNXvof7",
    "VPS AGENCY": "https://maps.app.goo.gl/SBiV54A54MvSBb7z7",
    "K.B.AMUTHA AGENCY": "https://maps.app.goo.gl/xej5QeurxRyVDmRt7",
    "SAMRAH AGENCY": "https://maps.app.goo.gl/vcWJXrH3jeMKHfoFA",
    "LAKSHMI TRADERS": "https://maps.app.goo.gl/BeKUDn2j4me62vPu5",
    "UMAAS AGENCY": "https://maps.app.goo.gl/rwLFMnSiybrxKB8N6",
    "SSR AGENCY": "https://maps.app.goo.gl/CEDjRzP5Hv9Fwv6F9",
    "VEL AGENCY": "https://maps.app.goo.gl/tFjPS7f4GTnCAZWt7",
    "RAJVARNA AGENCY SURYANAGAR": "",
    "RAJVARNA AGENCY THIRIPPUVANAM": ""
}
