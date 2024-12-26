from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.bip39_utils import generate_bip39_mnemonic

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

    # Generate BIP39 mnemonic & hash the password
    mnemonic = generate_bip39_mnemonic()
    hashed_pw = hash_password(req.password)

    new_user = User(
        email=req.email,
        password_hash=hashed_pw,
        bip39_mnemonic=mnemonic
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Cast to str to satisfy type checker
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
