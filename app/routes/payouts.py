from fastapi import APIRouter, HTTPException
from ..db import cur, con
from .. import config
import requests
import uuid
import datetime

router = APIRouter()

# ---- Get payout history ----
@router.get("/history")
def payout_history():
    cur.execute("""
        SELECT id, card_last4, protocol, amount, payout_type, payout_network,
               payout_target, result_status, reference, created_at
        FROM transactions
        ORDER BY id DESC LIMIT 200
    """)
    rows = cur.fetchall()
    return {
        "items": [
            {
                "id": r[0],
                "card_last4": r[1],
                "protocol": r[2],
                "amount": r[3],
                "payout_type": r[4],
                "payout_network": r[5],
                "payout_target": r[6],
                "result_status": r[7],
                "reference": r[8],
                "created_at": r[9],
            }
            for r in rows
        ]
    }


# ---- Trigger a new payout ----
@router.post("/trigger")
def trigger_payout(amount: float, target_account: str):
    # Generate unique reference for tracking
    reference = str(uuid.uuid4())

    # Insert as pending in DB
    cur.execute("""
        INSERT INTO transactions (
            card_last4, protocol, amount, payout_type,
            payout_network, payout_target, result_status, reference, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "----",           # last4 (unknown for direct payout)
        "bank",           # protocol
        amount,
        "withdrawal",
        "bank_transfer",  # payout network
        target_account,
        "PENDING",        # initial status
        reference,
        datetime.datetime.utcnow()
    ))
    con.commit()

    # Call Airwallex payout API
    try:
        headers = {
            "Authorization": f"Bearer {config.BANK_PAYOUT_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "beneficiary": {
                "bank_details": {
                    "account_number": target_account
                }
            },
            "amount": amount,
            "currency": "USD",
            "reference": reference
        }
        resp = requests.post(config.BANK_PAYOUT_URL, json=payload, headers=headers)

        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Airwallex error: {resp.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "success": True,
        "payoutId": reference
    }
