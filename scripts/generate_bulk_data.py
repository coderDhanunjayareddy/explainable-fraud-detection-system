import random
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db.models import Transaction

vendors = [
    "ABC Infra", "XYZ Constructions", "RoadWorks Ltd",
    "UrbanBuild Corp", "MegaBuild Pvt Ltd"
]

departments = [
    "Public Works", "Municipal Corporation",
    "Urban Development", "Transport Department"
]

def generate_transactions(n=200):
    db = SessionLocal()
    try:
        for i in range(n):
            amount = random.choice([
                random.uniform(5000, 50000),          # normal
                random.uniform(200000, 500000),       # medium
                random.uniform(800000, 2000000)       # suspicious
            ])

            txn = Transaction(
                transaction_id=f"TXN{i+1000}",
                amount=round(amount, 2),
                vendor=random.choice(vendors),
                department=random.choice(departments),
                transaction_date=datetime.now() - timedelta(days=random.randint(1, 180)),
                description="Automated generated transaction",
                fraud_score=None,
                is_suspicious=None
            )

            db.add(txn)

        db.commit()
        print(f"{n} transactions inserted successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    generate_transactions(200)
