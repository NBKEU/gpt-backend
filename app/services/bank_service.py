import uuid
import requests
from . import protocol_service
from ..config import BANK_MODE, BANK_PAYOUT_URL, BANK_PAYOUT_TOKEN

def bank_payout(amount: float, account_number: str) -> dict:
    """
    Simulation -> returns fake transfer_id.
    Live -> POST to BANK_PAYOUT_URL with bearer token.
    """
    if BANK_MODE == "simulation":
        return {
            "status": "success",
            "mode": "simulation",
            "transfer_id": str(uuid.uuid4())
        }

    # live
    if not BANK_PAYOUT_URL or not BANK_PAYOUT_TOKEN:
        raise RuntimeError("BANK live mode requires BANK_PAYOUT_URL and BANK_PAYOUT_TOKEN")

    headers = {
        "Authorization": f"Bearer {BANK_PAYOUT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "account_number": account_number,
        "amount": amount,
    }
    r = requests.post(BANK_PAYOUT_URL, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    jr = r.json()
    return {
        "status": jr.get("status", "pending"),
        "mode": "live",
        "transfer_id": jr.get("transfer_id", str(uuid.uuid4()))
    }
