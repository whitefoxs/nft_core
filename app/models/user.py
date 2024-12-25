# app/models/user.py

from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    bip39_mnemonic = Column(String, nullable=False)

    # Optional fields for demonstration or expansion
    # e.g., handle creation of wallet address, private key, etc.

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}>"
