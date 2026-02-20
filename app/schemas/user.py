from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
  email: EmailStr
  password: str
  role_id: int

class UserRead(BaseModel):
  id: int
  email: EmailStr
  role: str  

  class config:
    from_attributes = True