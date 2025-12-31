from app.db.database import SessionLocal
from app.db.models import Transaction
from app.ml.features import build_features
from app.ml.anomaly_model import FraudAnomalyModel
from app.ml.explainability import FraudExplainer
from app.ml.nlg_explainer import generate_audit_explanation
from app.core.audit import log_action

def explain_frauds():
    db = SessionLocal()
    try:
        # Fetch only suspicious transactions
        suspicious_txns = (
            db.query(Transaction)
            .filter(Transaction.is_suspicious == True)
            .all()
        )

        if not suspicious_txns:
            print("No suspicious transactions found.")
            return
        
        log_action(
            username="system",
            role="AUDITOR",
            action="VIEW_FRAUD_EXPLANATIONS",
            resource="multiple_transactions"
        )
        
        # Convert ORM objects to dicts for feature engineering
        txn_dicts = [
            {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "vendor": t.vendor,
                "department": t.department,
                "transaction_date": t.transaction_date
            }
            for t in suspicious_txns
        ]

        # Build ML features
        X = build_features(txn_dicts)

        # Train anomaly model (same logic as scoring phase)
        model = FraudAnomalyModel()
        model.train(X)

        # Initialize SHAP explainer
        explainer = FraudExplainer(model, X.columns)
        shap_values = explainer.explain(X)

        # Convert SHAP values to natural language explanations
        for i, txn in enumerate(suspicious_txns):
            explanation = generate_audit_explanation(
                transaction_id=txn.transaction_id,
                shap_values=shap_values[i],
                feature_names=X.columns
            )

            print(f"\nTransaction ID: {explanation['transaction_id']}")
            for line in explanation["audit_explanation"]:
                print(f"- {line}")

    finally:
        db.close()


if __name__ == "__main__":
    explain_frauds()
