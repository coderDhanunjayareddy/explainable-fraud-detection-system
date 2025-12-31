from app.db.repository import fetch_all_transactions
from app.ml.features import build_features

transactions = fetch_all_transactions()
df_features = build_features(transactions)

print(df_features.head())
print("\nShape:", df_features.shape)
