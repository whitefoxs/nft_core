# app/models/user.py

from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    bip39_mnemonic = Column(String, nullable=False)

    # Add these columns:
    private_key_hex = Column(String, nullable=True)
    public_key_hex = Column(String, nullable=True)
    wallet_address = Column(String, nullable=True)

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}>"
