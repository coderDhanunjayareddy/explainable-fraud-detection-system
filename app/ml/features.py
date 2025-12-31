import pandas as pd

def build_features(transactions: list[dict]) -> pd.DataFrame:
    """
    Converts raw transaction records into ML-ready features
    """

    df = pd.DataFrame(transactions)

    # --- Basic Features ---
    df["amount"] = df["amount"].astype(float)

    # Time-based features
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["day"] = df["transaction_date"].dt.day
    df["month"] = df["transaction_date"].dt.month
    df["weekday"] = df["transaction_date"].dt.weekday

    # Frequency-based features
    df["vendor_txn_count"] = df.groupby("vendor")["transaction_id"].transform("count")
    df["department_txn_count"] = df.groupby("department")["transaction_id"].transform("count")

    # Normalized amount (important for ML)
    df["amount_zscore"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()

    # Select only numeric features for ML
    feature_columns = [
        "amount",
        "vendor_txn_count",
        "department_txn_count",
        "day",
        "month",
        "weekday",
        "amount_zscore"
    ]
    df_features = df[feature_columns].fillna(0)
    return df_features
