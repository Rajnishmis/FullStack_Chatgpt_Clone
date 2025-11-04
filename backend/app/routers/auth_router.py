from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models
from ..auth import get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app import models, database
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import os
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

# Register new user


@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

# Login and get JWT token


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.email).first()
    # if not user or not verify_password(request.password, user.hashed_password):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    print("DEBUG:", request.password, user.hashed_password)  # temporary debug
    if not verify_password(request.password, user.hashed_password):
        print("Password verification failed!")  # debug
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    """
    Decodes the JWT token and returns the current authenticated user.
    """

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"

    # If the SECRET_KEY is missing, raise an error
    if not SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SECRET_KEY not set in environment."
        )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # 'sub' was set during token creation

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token - missing user info",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Fetch user from DB
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
