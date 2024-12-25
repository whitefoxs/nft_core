# app/models/user_kyc.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class UserKyc(Base):
    __tablename__ = "users_kyc"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone = Column(String, nullable=True)
    nik = Column(String, nullable=True)      # NIK number
    npwp = Column(String, nullable=True)     # NPWP number
    sex = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)
    birth_info = Column(String, nullable=True)  # Could store 'place, date' in one or two columns
    mother_maiden_name = Column(String, nullable=True)
    favorite_pet_name = Column(String, nullable=True)
    city_of_growth = Column(String, nullable=True)

    def __repr__(self):
        return f"<UserKyc id={self.id}, user_id={self.user_id}>"
