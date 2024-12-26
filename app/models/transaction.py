from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tx_type = Column(String, nullable=False)
    tx_details = Column(Text, nullable=True)
    # Use a lambda so it's called at runtime
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    block = relationship("Block", backref="transactions")

    def __repr__(self):
        return f"<Transaction id={self.id}, block_id={self.block_id}, user_id={self.user_id}>"
