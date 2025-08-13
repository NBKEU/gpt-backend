import os
from dotenv import load_dotenv

load_dotenv()

# Service
APP_NAME = os.getenv("APP_NAME", "Card Terminal Backend")
ENV = os.getenv("ENV", "production")

# CORS
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")

# Modes
# BANK_MODE: simulation | live
BANK_MODE = os.getenv("BANK_MODE", "simulation").lower()
# CRYPTO_MODE: simulation | live
CRYPTO_MODE = os.getenv("CRYPTO_MODE", "simulation").lower()

# Bank live settings
BANK_PAYOUT_URL = os.getenv("BANK_PAYOUT_URL", "").strip()
BANK_PAYOUT_TOKEN = os.getenv("BANK_PAYOUT_TOKEN", "").strip()

# Crypto live settings - point these to YOUR wallet services (HTTP)
ERC20_PAYOUT_URL = os.getenv("ERC20_PAYOUT_URL", "").strip()
ERC20_PAYOUT_TOKEN = os.getenv("ERC20_PAYOUT_TOKEN", "").strip()
TRC20_PAYOUT_URL = os.getenv("TRC20_PAYOUT_URL", "").strip()
TRC20_PAYOUT_TOKEN = os.getenv("TRC20_PAYOUT_TOKEN", "").strip()

# Dashboard
AUTO_REFRESH_SECONDS = int(os.getenv("DASHBOARD_REFRESH", "10"))

# SQLite path
SQLITE_PATH = os.getenv("SQLITE_PATH", "terminal.db")
