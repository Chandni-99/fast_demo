from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

user_role = Table('user_role', Base.metadata,
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('role_id', Integer, ForeignKey('roles.id'))
                  )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary=user_role, back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = Column(String)
    users = relationship("User", secondary=user_role, back_populates="roles")
