from app.db.database import SessionLocal
from app.db.models import AuditLog

def log_action(username: str, role: str, action: str, resource: str = None):
    db = SessionLocal()
    try:
        log = AuditLog(
            username=username,
            role=role,
            action=action,
            resource=resource
        )
        db.add(log)
        db.commit()
    finally:
        db.close()
