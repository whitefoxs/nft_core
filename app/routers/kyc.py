from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import cast

from app.database import SessionLocal
from app.models.user import User
from app.models.user_kyc import UserKyc

router = APIRouter(prefix="/kyc", tags=["KYC"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class KycRequest(BaseModel):
    email: str
    phone: str | None = None
    nik: str | None = None
    npwp: str | None = None
    sex: str | None = None
    marital_status: str | None = None
    birth_info: str | None = None
    mother_maiden_name: str | None = None
    favorite_pet_name: str | None = None
    city_of_growth: str | None = None

class KycResponse(BaseModel):
    message: str
    user_id: int
    phone: str | None
    nik: str | None
    npwp: str | None
    sex: str | None
    marital_status: str | None
    birth_info: str | None
    mother_maiden_name: str | None
    favorite_pet_name: str | None
    city_of_growth: str | None

@router.post("/update", response_model=KycResponse)
def update_kyc(req: KycRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_kyc = db.query(UserKyc).filter(UserKyc.user_id == user.id).first()

    if not existing_kyc:
        # Create new
        new_kyc = UserKyc(
            # Use cast(int, ...) to hush the linter about InstrumentedAttribute
            user_id=cast(int, user.id),
            phone=req.phone,
            nik=req.nik,
            npwp=req.npwp,
            sex=req.sex,
            marital_status=req.marital_status,
            birth_info=req.birth_info,
            mother_maiden_name=req.mother_maiden_name,
            favorite_pet_name=req.favorite_pet_name,
            city_of_growth=req.city_of_growth
        )
        db.add(new_kyc)
        db.commit()
        db.refresh(new_kyc)

        return KycResponse(
            message="KYC created successfully",
            user_id=cast(int, new_kyc.user_id),
            phone=str(new_kyc.phone) if new_kyc.phone else None,
            nik=str(new_kyc.nik) if new_kyc.nik else None,
            npwp=str(new_kyc.npwp) if new_kyc.npwp else None,
            sex=str(new_kyc.sex) if new_kyc.sex else None,
            marital_status=str(new_kyc.marital_status) if new_kyc.marital_status else None,
            birth_info=str(new_kyc.birth_info) if new_kyc.birth_info else None,
            mother_maiden_name=str(new_kyc.mother_maiden_name) if new_kyc.mother_maiden_name else None,
            favorite_pet_name=str(new_kyc.favorite_pet_name) if new_kyc.favorite_pet_name else None,
            city_of_growth=str(new_kyc.city_of_growth) if new_kyc.city_of_growth else None
        )
    else:
        # Update existing
        existing_kyc.phone = req.phone
        existing_kyc.nik = req.nik
        existing_kyc.npwp = req.npwp
        existing_kyc.sex = req.sex
        existing_kyc.marital_status = req.marital_status
        existing_kyc.birth_info = req.birth_info
        existing_kyc.mother_maiden_name = req.mother_maiden_name
        existing_kyc.favorite_pet_name = req.favorite_pet_name
        existing_kyc.city_of_growth = req.city_of_growth
        db.commit()
        db.refresh(existing_kyc)

        return KycResponse(
            message="KYC updated successfully",
            user_id=cast(int, existing_kyc.user_id),
            phone=str(existing_kyc.phone) if existing_kyc.phone else None,
            nik=str(existing_kyc.nik) if existing_kyc.nik else None,
            npwp=str(existing_kyc.npwp) if existing_kyc.npwp else None,
            sex=str(existing_kyc.sex) if existing_kyc.sex else None,
            marital_status=str(existing_kyc.marital_status) if existing_kyc.marital_status else None,
            birth_info=str(existing_kyc.birth_info) if existing_kyc.birth_info else None,
            mother_maiden_name=str(existing_kyc.mother_maiden_name) if existing_kyc.mother_maiden_name else None,
            favorite_pet_name=str(existing_kyc.favorite_pet_name) if existing_kyc.favorite_pet_name else None,
            city_of_growth=str(existing_kyc.city_of_growth) if existing_kyc.city_of_growth else None
        )
