from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import TokenResponse
from app.db.database import SessionLocal
from app.db.models import User
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        db_user = (
            db.query(User)
            .filter(User.username == form_data.username)
            .first()
        )

        if not db_user or not verify_password(form_data.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "sub": db_user.username,
            "role": db_user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        db.close()
