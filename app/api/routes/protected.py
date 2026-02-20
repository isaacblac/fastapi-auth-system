from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from fastapi import APIRouter, Depends
from app.core.dependencies import require_role

router = APIRouter(prefix="/auth", tags=["Protected"])

@router.get("/me")
def read_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.name,
    }

@router.get("/admin-only")
def admin_only(current_user: User = Depends(require_role("admin"))):
    return {
        "message": "Welcome admin",
        "user_id": current_user.id,
        "email": current_user.email,
    }
