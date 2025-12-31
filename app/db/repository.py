from app.db.database import SessionLocal
from app.db.models import Transaction

def fetch_all_transactions():
    db = SessionLocal()
    try:
        records = db.query(Transaction).all()
        return [
            {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "vendor": t.vendor,
                "department": t.department,
                "transaction_date": t.transaction_date
            }
            for t in records
        ]
    finally:
        db.close()

def fetch_all_transaction_objects():
    db = SessionLocal()
    try:
        return db.query(Transaction).all()
    finally:
        db.close()