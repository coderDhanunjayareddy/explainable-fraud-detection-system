from app.db.database import SessionLocal
from app.db.models import Transaction
from app.ml.features import build_features
from app.ml.anomaly_model import FraudAnomalyModel

def score_transactions():
    db = SessionLocal()
    try:
        transactions = db.query(Transaction).all()

        if len(transactions) < 5:
            print("Not enough data for scoring.")
            return

        # Convert ORM → dict (for ML)
        txn_dicts = [
            {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "vendor": t.vendor,
                "department": t.department,
                "transaction_date": t.transaction_date
            }
            for t in transactions
        ]

        # Feature engineering
        X = build_features(txn_dicts)

        # Train model
        model = FraudAnomalyModel()
        model.train(X)

        # Predict
        scores, flags = model.predict(X)

        # Persist results (SAME SESSION ✅)
        for txn, score, flag in zip(transactions, scores, flags):
            txn.fraud_score = float(score)
            txn.is_suspicious = bool(flag)

        db.commit()
        print("Fraud scores updated successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    score_transactions()
