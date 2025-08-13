from fastapi import APIRouter
from ..db import cur

router = APIRouter()

@router.get("/history")
def payout_history():
    cur.execute("""SELECT id, card_last4, protocol, amount, payout_type, payout_network,
                          payout_target, result_status, reference, created_at
                   FROM transactions
                   ORDER BY id DESC LIMIT 200""")
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
            } for r in rows
        ]
    }
