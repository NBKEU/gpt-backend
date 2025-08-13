from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models.transaction import ProcessRequest, ProcessResponse
from ..services.protocol_service import validate_protocol
from ..services.bank_service import bank_payout
from ..config import BANK_MODE
from ..db import conn, cur

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
def process_card(payload: ProcessRequest):
    # Validate protocol & auth code length
    if not validate_protocol(payload.protocol, payload.auth_code):
        raise HTTPException(status_code=400, detail="Invalid protocol or auth code length")

    # Only store last4 (never full PAN)
    card_last4 = payload.card_number[-4:]

    # Always send to YOUR default bank account
    result = bank_payout(amount=payload.amount)
    reference = result.get("transfer_id", "")
    result_status = result.get("status", "pending")
    mode_used = f"bank:{BANK_MODE}"

    # Store "(default account)" so UI doesn't leak your real account
    cur.execute(
        """INSERT INTO transactions (card_last4, protocol, auth_code, amount, payout_type, payout_network,
           payout_target, result_status, reference, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            card_last4, payload.protocol, payload.auth_code, payload.amount,
            "BANK", None, "(default account)",
            result_status, reference, datetime.utcnow().isoformat()
        )
    )
    conn.commit()

    if result_status != "succeeded":
        raise HTTPException(status_code=502, detail=f"Payout failed: {result.get('error','unknown')}")

    return ProcessResponse(status=result_status, reference=reference, mode=mode_used)
