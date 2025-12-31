from fastapi import APIRouter, Depends, HTTPException
from app.schemas.transaction import TransactionBase, TransactionResponse
from app.db.database import SessionLocal
from app.db.models import Transaction
from app.core.dependencies import get_current_user
from app.core.audit import log_action
from typing import List
from app.schemas.fraud_result import FraudResultResponse
from app.schemas.fraud_explanation import FraudExplanationResponse
from app.ml.features import build_features
from app.ml.anomaly_model import FraudAnomalyModel
from app.ml.explainability import FraudExplainer
from app.ml.nlg_explainer import generate_audit_explanation


router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])


@router.post("/analyze", response_model=TransactionResponse)
def analyze_transaction(
    txn: TransactionBase,
    user=Depends(get_current_user)   # 👈 AUTHENTICATED USER
):
    db = SessionLocal()

    try:
        # 🔐 OPTIONAL ROLE CHECK (GOOD PRACTICE)
        if user["role"] not in ["ADMIN"]:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to analyze transactions"
            )

        # 🧾 AUDIT LOG (LOG INTENT FIRST)
        log_action(
            username=user["username"],
            role=user["role"],
            action="ANALYZE_TRANSACTION",
            resource=txn.transaction_id
        )

        # 🔍 FRAUD LOGIC (UNCHANGED)
        if txn.amount > 100000:
            fraud_score = 0.9
            is_suspicious = True
        else:
            fraud_score = 0.2
            is_suspicious = False

        db_txn = Transaction(
            transaction_id=txn.transaction_id,
            amount=txn.amount,
            department=txn.department,
            vendor=txn.vendor,
            transaction_date=txn.transaction_date,
            description=txn.description,
            fraud_score=fraud_score,
            is_suspicious=is_suspicious
        )

        db.add(db_txn)
        db.commit()

        return TransactionResponse(
            **txn.dict(),
            fraud_score=fraud_score,
            is_suspicious=is_suspicious
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

@router.get("/results", response_model=List[FraudResultResponse])
def get_fraud_results(
    user=Depends(get_current_user)
):
    # 🔐 ROLE CHECK
    if user["role"] not in ["ADMIN", "AUDITOR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view fraud results"
        )

    db = SessionLocal()
    try:
        # 🧾 AUDIT LOG
        log_action(
            username=user["username"],
            role=user["role"],
            action="VIEW_FRAUD_RESULTS",
            resource="fraud_results"
        )

        results = (
            db.query(Transaction)
            .filter(Transaction.is_suspicious == True)
            .order_by(Transaction.fraud_score.desc())
            .all()
        )

        return results

    finally:
        db.close()

@router.get("/explanations", response_model=List[FraudExplanationResponse])
def get_fraud_explanations(
    user=Depends(get_current_user)
):
    # 🔐 ROLE CHECK
    if user["role"] not in ["ADMIN", "AUDITOR"]:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view explanations"
        )

    db = SessionLocal()
    try:
        suspicious_txns = (
            db.query(Transaction)
            .filter(Transaction.is_suspicious == True)
            .all()
        )

        if not suspicious_txns:
            return []

        # 🧾 AUDIT LOG
        log_action(
            username=user["username"],
            role=user["role"],
            action="VIEW_FRAUD_EXPLANATIONS",
            resource="fraud_explanations"
        )

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

        X = build_features(txn_dicts)

        model = FraudAnomalyModel()
        model.train(X)

        explainer = FraudExplainer(model, X.columns)
        shap_values = explainer.explain(X)

        responses = []
        for i, txn in enumerate(suspicious_txns):
            explanation = generate_audit_explanation(
                transaction_id=txn.transaction_id,
                shap_values=shap_values[i],
                feature_names=X.columns
            )

            responses.append({
                "transaction_id": txn.transaction_id,
                "explanations": explanation["audit_explanation"]
            })

        return responses

    finally:
        db.close()
