from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import SessionLocal
from app.models.user import User
from app.models.block import Block
from app.models.transaction import Transaction
from app.core.blockchain_utils import (
    get_last_block_for_user,
    create_block,
    validate_user_chain,
)

router = APIRouter(prefix="/transaction", tags=["Transaction"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Transaction creation ---

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

    last_block = get_last_block_for_user(db, user.id)
    prev_hash = last_block.block_hash if last_block else "GENESIS"
    block_data = f"Transaction Type: {req.tx_type}; Details: {req.tx_details or ''}"
    new_block = create_block(db, user.id, prev_hash, block_data)

    new_tx = Transaction(
        block_id=new_block.id,
        user_id=user.id,
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


# --- Chain Validation ---

@router.get("/validate-chain/{email}")
def validate_chain(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_valid = validate_user_chain(db, user.id)
    return {"user": email, "chain_valid": is_valid}


# --- Get Chain ---

class BlockSchema(BaseModel):
    id: int
    block_hash: str
    prev_hash: str | None
    data: str | None
    timestamp: str


@router.get("/user-chain/{email}", response_model=List[BlockSchema])
def get_user_chain(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    blocks = (
        db.query(Block)
        .filter(Block.user_id == user.id)
        .order_by(Block.id.asc())
        .all()
    )

    result = []
    for b in blocks:
        result.append(BlockSchema(
            id=b.id,
            block_hash=str(b.block_hash),
            prev_hash=str(b.prev_hash) if b.prev_hash else None,
            data=str(b.data) if b.data else None,
            timestamp=b.timestamp.isoformat()
        ))
    return result
