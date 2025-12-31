import argparse
import pandas as pd
import uuid
from datetime import datetime

from app.db.database import SessionLocal
from app.db.models import Transaction


def load_dataframe(file_path=None, url=None):
    if file_path:
        try:
            return pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="ISO-8859-1")
    if url:
        try:
            return pd.read_csv(url, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(url, encoding="ISO-8859-1")
    raise ValueError("Either file path or URL must be provided")


def import_transactions(df):
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            amount = pd.to_numeric(
                str(row["Amount £"]).replace(",", ""),
                errors="coerce"
            )

            if pd.isna(amount):
                continue

            txn = Transaction(
                transaction_id=str(uuid.uuid4()),
                source_transaction_ref=str(row["Transaction Number"]),
                amount=float(amount),
                vendor=str(row["Supplier"]),
                department=str(row["Entity"]),
                transaction_date=pd.to_datetime(row["Date"]),
                description=str(row.get("Description", ""))
            )

            db.add(txn)

        db.commit()
        print(f"Imported {len(df)} transactions successfully.")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()



def main():
    parser = argparse.ArgumentParser(description="Import government spending data")
    parser.add_argument("--file", help="Path to local CSV file")
    parser.add_argument("--url", help="CSV URL")

    args = parser.parse_args()

    df = load_dataframe(file_path=args.file, url=args.url)

    # Limit rows for demo safety
    df = df.head(100)

    import_transactions(df)


if __name__ == "__main__":
    main()
