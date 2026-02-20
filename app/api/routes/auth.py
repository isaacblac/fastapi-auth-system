from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db.session import get_db
from app.services.auth_service import register_user, authenticate_user
from app.core.dependencies import decode_token, get_current_user, require_role
from app.models.user import User
from app.core.security import create_access_token
from jose import jwt
from app.core.config import settings
from app.services.user_service import create_user
from fastapi import Depends
from app.core.security import oauth2_scheme
from app.core.token_blacklist import add_to_blacklist
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------
# Schemas (request bodies)
# ---------------------------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------------------
# Register
# ---------------------------

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(
        db=db,
        email=payload.email,
        password=payload.password,
        role_id=payload.role_id,
    )

    return {
        "message": "User created successfully",
        "user_id": user.id
    }


# ---------------------------
# Login
# ---------------------------

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token({
        "user_id": user.id,
        "role": user.role.name,
    })

    refresh_token = create_refresh_token({
        "user_id": user.id,
    })

    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = db.query(User).filter(User.id == payload["user_id"]).first()

    if not user or user.refresh_token != token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token mismatch",
        )

    new_access_token = create_access_token({
        "user_id": user.id,
        "role": user.role.name,
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }



# ---------------------------
# Get Current User
# ---------------------------

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role.name,
    }


# ---------------------------
# Admin Only Example
# ---------------------------

@router.get("/admin-only")
def admin_only(current_user: User = Depends(require_role("admin"))):
    return {
        "message": f"Welcome admin {current_user.email}"
    }

@router.post("/refresh")
def refresh_token(token: str):
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")

    new_access_token = create_access_token({"user_id": user_id, "role": payload["role"]})

    return {"access_token": new_access_token}

@router.post("/logout")
def logout(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user.refresh_token = None
    db.commit()
    return {"message": "Logged out"}



