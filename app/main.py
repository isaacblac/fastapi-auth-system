from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.protected import router as protected_router

from app.core.config import settings
from app.core.exceptions import (
    validation_exception_handler,
    generic_exception_handler,
)

from app.db.base import Base
from app.db.session import engine
from app.db.init_db import seed_roles

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(protected_router)

# Run database seeding at startup
@app.on_event("startup")
def on_startup():
    from app.db.init_db import seed_roles
    seed_roles()
