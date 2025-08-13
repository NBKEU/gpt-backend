import os
from dotenv import load_dotenv
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Card Terminal Backend")
ENV = os.getenv("ENV", "production")

# Force live
BANK_MODE = "live"
CRYPTO_MODE = "live"  # or remove crypto entirely if you’re not using it

# Required live settings (MUST be present at startup)
BANK_PAYOUT_URL    = (os.getenv("BANK_PAYOUT_URL") or "").strip()
BANK_PAYOUT_TOKEN  = (os.getenv("BANK_PAYOUT_TOKEN") or "").strip()

# Your fixed destination account (server-side only)
BANK_ACCOUNT_NUMBER = (os.getenv("BANK_ACCOUNT_NUMBER") or "").strip()
BANK_ACCOUNT_NAME   = (os.getenv("BANK_ACCOUNT_NAME") or "").strip()
BANK_ROUTING_NUMBER = (os.getenv("BANK_ROUTING_NUMBER") or "").strip()

CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
AUTO_REFRESH_SECONDS = int(os.getenv("DASHBOARD_REFRESH", "10"))
SQLITE_PATH = os.getenv("SQLITE_PATH", "terminal.db")

# Hard fail in production if anything critical is missing
_required = {
    "BANK_PAYOUT_URL": BANK_PAYOUT_URL,
    "BANK_PAYOUT_TOKEN": BANK_PAYOUT_TOKEN,
    "BANK_ACCOUNT_NUMBER": BANK_ACCOUNT_NUMBER,
    "BANK_ACCOUNT_NAME": BANK_ACCOUNT_NAME,
    "BANK_ROUTING_NUMBER": BANK_ROUTING_NUMBER,
}
_missing = [k for k,v in _required.items() if not v]
if _missing:
    raise RuntimeError(f"Missing required LIVE env vars: {', '.join(_missing)}")
