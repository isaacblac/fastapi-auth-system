from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

def create_user(
    db: Session,
    email: str,
    password: str,
    role_id: int,
) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role_id=role_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
