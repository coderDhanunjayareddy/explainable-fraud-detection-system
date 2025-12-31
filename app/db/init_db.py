from app.db.database import engine, Base
from app.db.models import Transaction, User, AuditLog

def init_db():
    Base.metadata.create_all(bind=engine)
