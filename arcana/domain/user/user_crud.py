from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import and_

from domain.user import schema, database, models

from passlib.context import CryptContext
# argon2, bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_user(email: str,
                db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(new_user: schema.NewUserForm, db: Session):
    user = models.User(
        user_name = new_user.name,
        phone = new_user.phone,
        email = new_user.email,
        hashed_pw = pwd_context.hash(new_user.password)
    )
    db.add(user)
    db.commit()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)