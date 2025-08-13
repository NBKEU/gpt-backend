from pydantic import BaseModel, Field
from typing import Optional, Literal

# Supported protocols (name -> auth length) enforced elsewhere
class ProcessRequest(BaseModel):
    card_number: str = Field(..., min_length=8, max_length=19)
    protocol: str
    auth_code: str
    amount: float = Field(..., gt=0)
    payout_type: Literal["BANK", "CRYPTO"]
    # For CRYPTO: ERC20 or TRC20; For BANK: a bank account number or identifier
    payout_network: Optional[str] = None
    payout_target: str  # wallet address or bank account number

class ProcessResponse(BaseModel):
    status: str
    reference: str
    mode: str
