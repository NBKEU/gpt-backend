import requests, time, uuid
from ..config import (
    BANK_PAYOUT_URL, BANK_PAYOUT_TOKEN, BANK_ACCOUNT_NUMBER,
    BANK_ACCOUNT_NAME, BANK_ROUTING_NUMBER
)

def bank_payout(*, amount: float) -> dict:
    """
    Sends a real payout to YOUR fixed bank account.
    """
    payload = {
        "amount": round(float(amount), 2),
        "currency": "USD",
        "destination": {
            "type": "ach",
            "account_name": BANK_ACCOUNT_NAME,
            "account_number": BANK_ACCOUNT_NUMBER,
            "routing_number": BANK_ROUTING_NUMBER,
        }
    }
    headers = {
        "Authorization": f"Bearer {BANK_PAYOUT_TOKEN}",
        "Content-Type": "application/json",
        # Idempotency protects against duplicate payouts if the client retries
        "Idempotency-Key": str(uuid.uuid4()),
    }

    # simple exponential backoff on transient errors
    for attempt in range(4):
        try:
            r = requests.post(
                f"{BANK_PAYOUT_URL}/transfers",
                json=payload, headers=headers,
                timeout=20
            )
            if 200 <= r.status_code < 300:
                data = r.json() if r.content else {}
                return {"status": "succeeded", "transfer_id": data.get("id", "")}
            # 429/5xx -> retry; 4xx -> fail
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(0.5 * (2 ** attempt))
                continue
            return {"status": "failed", "error": f"{r.status_code}:{r.text}"}
        except requests.RequestException as e:
            # retry network errors
            if attempt < 3:
                time.sleep(0.5 * (2 ** attempt))
                continue
            return {"status": "failed", "error": str(e)}

    return {"status": "failed", "error": "max_retries_exceeded"}
