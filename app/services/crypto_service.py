import uuid
import requests
from ..config import (
    CRYPTO_MODE,
    ERC20_PAYOUT_URL, ERC20_PAYOUT_TOKEN,
    TRC20_PAYOUT_URL, TRC20_PAYOUT_TOKEN
)

def crypto_payout(network: str, amount: float, to_wallet: str) -> dict:
    """
    Simulation -> returns fake tx_id.
    Live -> POST to your wallet services (ERC20/TRC20) with bearer token.
    """
    network = (network or "").upper()
    if CRYPTO_MODE == "simulation":
        return {
            "status": "success",
            "mode": "simulation",
            "tx_id": str(uuid.uuid4()),
            "network": network
        }

    if network == "ERC20":
        if not ERC20_PAYOUT_URL or not ERC20_PAYOUT_TOKEN:
            raise RuntimeError("ERC20 live mode requires ERC20_PAYOUT_URL and ERC20_PAYOUT_TOKEN")
        headers = {"Authorization": f"Bearer {ERC20_PAYOUT_TOKEN}", "Content-Type": "application/json"}
        payload = {"to": to_wallet, "amount": amount}
        r = requests.post(ERC20_PAYOUT_URL, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        jr = r.json()
        return {
            "status": jr.get("status", "pending"),
            "mode": "live",
            "tx_id": jr.get("tx_id", str(uuid.uuid4())),
            "network": "ERC20"
        }

    if network == "TRC20":
        if not TRC20_PAYOUT_URL or not TRC20_PAYOUT_TOKEN:
            raise RuntimeError("TRC20 live mode requires TRC20_PAYOUT_URL and TRC20_PAYOUT_TOKEN")
        headers = {"Authorization": f"Bearer {TRC20_PAYOUT_TOKEN}", "Content-Type": "application/json"}
        payload = {"to": to_wallet, "amount": amount}
        r = requests.post(TRC20_PAYOUT_URL, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        jr = r.json()
        return {
            "status": jr.get("status", "pending"),
            "mode": "live",
            "tx_id": jr.get("tx_id", str(uuid.uuid4())),
            "network": "TRC20"
        }

    raise ValueError("Unsupported CRYPTO network (use ERC20 or TRC20)")
