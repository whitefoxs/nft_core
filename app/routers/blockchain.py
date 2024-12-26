# app/routers/blockchain.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.user import User
from app.models.block import Block
from app.core.blockchain_utils import validate_user_chain
from pydantic import BaseModel

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/validate-chain/{email}")
def validate_chain(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_valid = validate_user_chain(db, user.id)
    return {"user": email, "chain_valid": is_valid}


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
