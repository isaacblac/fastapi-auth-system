from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError

def validation_exception_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(status_code=422, content={"error": "ValidationError", "details": exc.errors()})

def generic_exception_handler(request: Request, exc: Exception):
  return JSONResponse(status_code=500, content={"error": "InternalServerError", "message": "Something went wrong"})