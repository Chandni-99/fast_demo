from typing import List, Optional

from pydantic import BaseModel, EmailStr


class RoleBase(BaseModel):
    name: str
    permissions: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    roles: List[Role] = []

    class Config:
        from_attributes = True


class UserPasswordReset(BaseModel):
    token: str
    new_password: str


class UserInDB(User):
    hashed_password: str
