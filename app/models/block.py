# app/models/block.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.models.user import User  # optional if we want direct references

class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # The hash of this block
    block_hash = Column(String, unique=True, nullable=False)
    # The hash of the previous block in the chain
    prev_hash = Column(String, nullable=True)
    # The block creation timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)
    # Optional data for storing additional info
    data = Column(Text, nullable=True)

    # Relationship back to user if you want it:
    user = relationship("User", backref="blocks")

    def __repr__(self):
        return f"<Block id={self.id}, user_id={self.user_id}, block_hash={self.block_hash}>"
