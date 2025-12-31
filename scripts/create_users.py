from app.db.database import SessionLocal
from app.db.models import User
from app.core.security import hash_password

def create_users():
    db = SessionLocal()
    try:
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="ADMIN"
        )

        auditor = User(
            username="auditor",
            password_hash=hash_password("audit123"),
            role="AUDITOR"
        )

        db.add_all([admin, auditor])
        db.commit()
        print("Users created successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    create_users()
