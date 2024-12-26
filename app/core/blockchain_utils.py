from sqlalchemy.orm import Session
from hashlib import sha256
from datetime import datetime, timezone

from app.models.block import Block


def get_last_block_for_user(db: Session, user_id: int) -> Block | None:
    return (
        db.query(Block)
        .filter(Block.user_id == user_id)
        .order_by(Block.id.desc())
        .first()
    )


def compute_block_hash(raw_string: str) -> str:
    return sha256(raw_string.encode("utf-8")).hexdigest()


def create_block(db: Session, user_id: int, prev_hash: str, data: str) -> Block:
    timestamp_str = datetime.now(timezone.utc).isoformat()
    new_block_hash = compute_block_hash(f"{user_id}{timestamp_str}{prev_hash}{data}")

    new_block = Block(
        user_id=user_id,
        block_hash=new_block_hash,
        prev_hash=prev_hash,
        data=data
    )
    db.add(new_block)
    db.commit()
    db.refresh(new_block)
    return new_block


def validate_user_chain(db: Session, user_id: int) -> bool:
    blocks = (
        db.query(Block)
        .filter(Block.user_id == user_id)
        .order_by(Block.id.asc())
        .all()
    )
    if not blocks:
        return True

    for i in range(1, len(blocks)):
        prev_block = blocks[i - 1]
        current_block = blocks[i]
        if current_block.prev_hash != prev_block.block_hash:
            return False
        # Re-check hash
        raw_str = f"{current_block.user_id}{current_block.timestamp.isoformat()}{current_block.prev_hash}{current_block.data}"
        if compute_block_hash(raw_str) != current_block.block_hash:
            return False

    return True


def validate_new_transaction(db: Session, user_id: int, block_id: int | None = None) -> bool:
    """
    A placeholder for transaction validation logic:
    1. Confirm user exists.
    2. Confirm block_id (if provided) is the last block for this user.
    3. Additional checks can be inserted (balances, signatures, etc.).
    """
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False

    last_block = get_last_block_for_user(db, user_id)
    if block_id and last_block and (last_block.id != block_id):
        return False

    return True
