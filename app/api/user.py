from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.user import create_user, get_users, delete_user, get_user_by_email, get_user
from app.db.base import get_db
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=User)
async def update_user(
        user_id: int,
        user_update: UserUpdate,  # Expect the UserUpdate schema in the request body
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Fetch the user from the database
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields based on the UserUpdate model
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.password = user_update.password
    # Add other fields similarly

    # Save the changes to the database
    db.commit()
    db.refresh(db_user)

    return db_user  # Make sure to return the actual user object


@router.delete("/{user_id}", response_model=User)
def delete_user_account(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    return delete_user(db=db, user_id=user_id)
