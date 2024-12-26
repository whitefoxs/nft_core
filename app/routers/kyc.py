# app/routers/kyc.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

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
    # Check user existence
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if KYC row exists
    existing_kyc = db.query(UserKyc).filter(UserKyc.user_id == user.id).first()

    if not existing_kyc:
        # Create new KYC row
        new_kyc = UserKyc(
            user_id=user.id,
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
            user_id=new_kyc.user_id,
            phone=new_kyc.phone,
            nik=new_kyc.nik,
            npwp=new_kyc.npwp,
            sex=new_kyc.sex,
            marital_status=new_kyc.marital_status,
            birth_info=new_kyc.birth_info,
            mother_maiden_name=new_kyc.mother_maiden_name,
            favorite_pet_name=new_kyc.favorite_pet_name,
            city_of_growth=new_kyc.city_of_growth
        )
    else:
        # Update existing KYC row
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
            user_id=existing_kyc.user_id,
            phone=existing_kyc.phone,
            nik=existing_kyc.nik,
            npwp=existing_kyc.npwp,
            sex=existing_kyc.sex,
            marital_status=existing_kyc.marital_status,
            birth_info=existing_kyc.birth_info,
            mother_maiden_name=existing_kyc.mother_maiden_name,
            favorite_pet_name=existing_kyc.favorite_pet_name,
            city_of_growth=existing_kyc.city_of_growth
        )
