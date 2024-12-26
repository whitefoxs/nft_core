from datetime import datetime
from hashlib import sha256

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.bip39_utils import generate_bip39_mnemonic
from app.core.crypto_utils import generate_key_pair, derive_wallet_address
from app.core.security import hash_password, verify_password
from app.database import SessionLocal
from app.models.block import Block
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic schemas
class SignUpRequest(BaseModel):
    email: str
    password: str


class SignUpResponse(BaseModel):
    email: str
    bip39_mnemonic: str


class SignInRequest(BaseModel):
    email: str
    password: str


class SignInResponse(BaseModel):
    message: str
    email: str


@router.post("/signup", response_model=SignUpResponse)
def sign_up(req: SignUpRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == req.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    # BIP39 + password hashing
    mnemonic = generate_bip39_mnemonic()
    hashed_pw = hash_password(req.password)

    # Generate ECDSA key pair + wallet
    priv_key, pub_key = generate_key_pair()
    wallet_addr = derive_wallet_address(pub_key)

    # Create user
    new_user = User(
        email=req.email,
        password_hash=hashed_pw,
        bip39_mnemonic=mnemonic,
        private_key_hex=priv_key,
        public_key_hex=pub_key,
        wallet_address=wallet_addr
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create genesis block
    timestamp_str = datetime.utcnow().isoformat()
    raw_string = f"{new_user.id}{timestamp_str}GENESIS"
    raw_hash = sha256(raw_string.encode("utf-8")).hexdigest()

    genesis_block = Block(
        user_id=new_user.id,
        block_hash=raw_hash,
        prev_hash="GENESIS",
        data="User genesis block"
    )
    db.add(genesis_block)
    db.commit()
    db.refresh(genesis_block)

    return SignUpResponse(
        email=str(new_user.email),
        bip39_mnemonic=str(new_user.bip39_mnemonic)
    )


@router.post("/signin", response_model=SignInResponse)
def sign_in(req: SignInRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Cast user.password_hash to str to avoid type checker warning
    if not verify_password(req.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password."
        )

    # Cast to str to satisfy type checker
    return SignInResponse(message="Sign-in successful", email=str(user.email))


@router.post("/recover-password")
def recover_password(email: str, mnemonic_words: list[str], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_words = user.bip39_mnemonic.split()
    matches = all(word in stored_words for word in mnemonic_words)

    if not matches:
        raise HTTPException(status_code=401, detail="Mnemonic words mismatch")

    return {"message": "Mnemonic validated. Proceed with password reset."}
