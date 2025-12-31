from app.db.repository import fetch_all_transactions
from app.ml.features import build_features
from app.ml.anomaly_model import FraudAnomalyModel

# Fetch data
transactions = fetch_all_transactions()

if len(transactions) < 5:
    print("Not enough data to train ML model.")
    exit()

# Feature engineering
X = build_features(transactions)

# Train model
model = FraudAnomalyModel()
model.train(X)

# Predict on training data (demo purpose)
scores, flags = model.predict(X)

print("Anomaly Scores:", scores)
print("Suspicious Flags:", flags)
