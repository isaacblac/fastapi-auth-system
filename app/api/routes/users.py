from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    delete_user,
)
from app.models.user import User
from app.core.dependencies import require_role

router = APIRouter(prefix="/users", tags=["Users"])


# USER REGISTRATION (keep this)
@router.post("/", response_model=UserRead)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = create_user(
        db=db,
        email=payload.email,
        password=payload.password,
        role_id=payload.role_id,
    )

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.name,
    }


# ADMIN: GET ALL USERS
@router.get("/", dependencies=[Depends(require_role("admin"))])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)


# GET USER BY ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ADMIN: DELETE USER
@router.delete("/{user_id}", dependencies=[Depends(require_role("admin"))])
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
