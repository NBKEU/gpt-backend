import os
import sys
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Card Terminal Backend")
ENV = os.getenv("ENV", "production").lower()

# Modes
BANK_MODE = "live"   # Force live payouts
CRYPTO_MODE = "live"  # Or disable if unused

# Bank payout settings
BANK_PAYOUT_URL = (os.getenv("BANK_PAYOUT_URL") or "").strip()
BANK_PAYOUT_TOKEN = (os.getenv("BANK_PAYOUT_TOKEN") or "").strip()

# Your fixed destination account (server-side only)
BANK_ACCOUNT_NUMBER = (os.getenv("BANK_ACCOUNT_NUMBER") or "").strip()
BANK_ACCOUNT_NAME = (os.getenv("BANK_ACCOUNT_NAME") or "").strip()
BANK_ROUTING_NUMBER = (os.getenv("BANK_ROUTING_NUMBER") or "").strip()

# Frontend/other settings
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
AUTO_REFRESH_SECONDS = int(os.getenv("DASHBOARD_REFRESH", "10"))
SQLITE_PATH = os.getenv("SQLITE_PATH", "terminal.db")

# Required variables for live mode
_required = {
    "BANK_PAYOUT_URL": BANK_PAYOUT_URL,
    "BANK_PAYOUT_TOKEN": BANK_PAYOUT_TOKEN,
    "BANK_ACCOUNT_NUMBER": BANK_ACCOUNT_NUMBER,
    "BANK_ACCOUNT_NAME": BANK_ACCOUNT_NAME,
    "BANK_ROUTING_NUMBER": BANK_ROUTING_NUMBER,
}

_missing = [k for k, v in _required.items() if not v]

if ENV == "production":
    # Fail hard in production if any are missing
    if _missing:
        raise RuntimeError(f"Missing required LIVE env vars: {', '.join(_missing)}")
else:
    # In non-production, warn but allow startup
    if _missing:
        print(f"[WARNING] Missing env vars: {', '.join(_missing)} — using dummy values for development.", file=sys.stderr)
        # Fill in dummy placeholders so code can run
        if not BANK_ACCOUNT_NUMBER:
            BANK_ACCOUNT_NUMBER = "0000000000"
        if not BANK_ACCOUNT_NAME:
            BANK_ACCOUNT_NAME = "DEV_ACCOUNT"
        if not BANK_ROUTING_NUMBER:
            BANK_ROUTING_NUMBER = "000000000"
