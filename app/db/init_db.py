from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.role import Role


def seed_roles() -> None:
    db: Session = SessionLocal()

    try:
        existing = db.query(Role).first()

        if not existing:
            db.add_all([
                Role(name="admin"),
                Role(name="user"),
            ])
            db.commit()

    finally:
        db.close()
