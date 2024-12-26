from typing import cast
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.models.user import User
from app.models.block import Block
from app.models.transaction import Transaction
from app.core.blockchain_utils import (
    get_last_block_for_user,
    create_block,
    validate_new_transaction
)

router = APIRouter(prefix="/transaction", tags=["Transaction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TransactionRequest(BaseModel):
    email: str
    tx_type: str
    tx_details: str | None = None


class TransactionResponse(BaseModel):
    message: str
    transaction_id: int


@router.post("/create", response_model=TransactionResponse)
def create_transaction(req: TransactionRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id_int = cast(int, user.id)
    last_block = get_last_block_for_user(db, user_id_int)

    # Validate
    if not validate_new_transaction(db, user_id_int, last_block.id if last_block else None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction validation failed"
        )

    prev_hash = last_block.block_hash if last_block else "GENESIS"
    block_data = f"Transaction Type: {req.tx_type}; Details: {req.tx_details or ''}"
    new_block = create_block(db, user_id_int, prev_hash, block_data)

    new_tx = Transaction(
        block_id=cast(int, new_block.id),
        user_id=user_id_int,
        tx_type=req.tx_type,
        tx_details=req.tx_details
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)

    return TransactionResponse(
        message="Transaction created successfully",
        transaction_id=new_tx.id
    )
