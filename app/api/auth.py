import os
from datetime import timedelta
from jinja2 import Environment,FileSystemLoader
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, create_password_reset_token, \
    verify_password_reset_token, send_email
from app.crud.user import authenticate_user, get_user_by_email, create_user, update_user_password
from app.db.base import get_db
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserPasswordReset, User

router = APIRouter()
env = Environment(loader=FileSystemLoader("app/templates"))  # Adjust if needed

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = create_user(db=db, user=user)  # Use a different variable name
    return created_user  # Return the created user object directly


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ensure you're using the correct identifier
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    username=email.split("@")[0]

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_reset_token = create_password_reset_token(email)
    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password?token={password_reset_token}"
    # Prepare email content
    subject = "Password Reset Instructions"
    template = env.get_template("email_template.html")  # Point to your actual template file
    html_body = template.render(
        username=username,
        password_reset_token=password_reset_token,
        reset_url=reset_url

    )
    plain_body = f"""
        Hello {username},
    
        You have requested to reset your password. Please use the following token to reset your password:

        {reset_url}

        If you did not request a password reset, please ignore this email.

        Best regards,
        Wappnet systems pvt ltd.
        """
    if send_email(email, subject, plain_body, html_body):
        return {"message": "Password reset instructions sent to your email", "reset_token": password_reset_token}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")


@router.post("/reset-password")
def reset_password(reset_data: UserPasswordReset, db: Session = Depends(get_db)):
    # Verify the reset token
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Get the user by email
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's password
    hashed_password = get_password_hash(reset_data.new_password)
    update_user_password(db, user.id, hashed_password)

    return {"message": "Password has been reset successfully"}
