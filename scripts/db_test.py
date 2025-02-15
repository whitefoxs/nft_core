# scripts/db_test.py

from app.database import SessionLocal
from app.models.user import User


def test_db():
    db = SessionLocal()
    new_user = User(
        email="test_db_script@example.com",  # changed email!
        password_hash="hashed_password",
        bip39_mnemonic="word1 word2 word3 ... word12"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("Inserted User:", new_user)
    db.close()
