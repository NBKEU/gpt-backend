from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models.transaction import ProcessRequest, ProcessResponse
from ..services.protocol_service import validate_protocol
from ..services.bank_service import bank_payout
from ..services.crypto_service import crypto_payout
from ..config import BANK_MODE, CRYPTO_MODE
from ..db import conn, cur

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
def process_card(payload: ProcessRequest):
    """
    Process a payment and trigger a payout.
    This saves the payout record immediately so it can be tracked via /status.
    """

    # Validate protocol & auth code length
    if not validate_protocol(payload.protocol, payload.auth_code):
        raise HTTPException(status_code=400, detail="Invalid protocol or auth code length")

    # Store only last 4 digits of card number for logs
    card_last4 = payload.card_number[-4:]

    reference = ""
    result_status = "failed"
    mode_used = ""

    try:
        if payload.payout_type.upper() == "BANK":
            result = bank_payout(amount=payload.amount, account_number=payload.payout_target)
            reference = result.get("transfer_id", "")
            result_status = result.get("status", "pending")
            mode_used = f"bank:{BANK_MODE}"

        elif payload.payout_type.upper() == "CRYPTO":
            result = crypto_payout(
                network=(payload.payout_network or "ERC20"),
                amount=payload.amount,
                to_wallet=payload.payout_target
            )
            reference = result.get("tx_id", "")
            result_status = result.get("status", "pending")
            mode_used = f"crypto:{CRYPTO_MODE}"

        else:
            raise HTTPException(status_code=400, detail="Invalid payout_type (BANK or CRYPTO)")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payout processing failed: {str(e)}")

    # Save transaction to DB
    cur.execute(
        """
        INSERT INTO transactions (
            card_last4, protocol, auth_code, amount, payout_type, payout_network,
            payout_target, result_status, reference, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            card_last4, payload.protocol, payload.auth_code, payload.amount,
            payload.payout_type, payload.payout_network, payload.payout_target,
            result_status, reference, datetime.utcnow().isoformat()
        )
    )
    conn.commit()

    return ProcessResponse(status=result_status, reference=reference, mode=mode_used)
