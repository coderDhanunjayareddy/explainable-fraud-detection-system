from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer
from datetime import datetime
from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    source_transaction_ref = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    department = Column(String, nullable=False)
    vendor = Column(String, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    fraud_score = Column(Float)
    is_suspicious = Column(Boolean)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN or AUDITOR

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    role = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)   