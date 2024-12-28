from sqlalchemy.orm import Session
from models import User
from uuid import uuid4
from fastapi import HTTPException, status
from schemas import UserCreate
from datetime import datetime


def create_superadmin(db: Session):
    superadmin = db.query(User).filter(User.mobile_number == "9708188605").first()
    if not superadmin:
        superadmin = User(
            user_id=str(uuid4()),
            mobile_number="9708188605",
            name="Superadmin",
            is_verified=True,
            is_superadmin=True,
            type="superadmin",
            otp=1234,
        )
        db.add(superadmin)
        db.commit()
        print("Superadmin created with mobile number 9708188604.")


# CRUD Functions
def register_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.mobile_number == user.mobile_number).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this mobile number already exists")

    new_user = User(
        name=user.name,
        mobile_number=user.mobile_number,
        date_of_birth=user.date_of_birth,
        occupation=user.occupation,
        type=user.type,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    users = db.query(User).filter(
    User.is_deleted == False
    ).all()
    return users

def update_user_role(user_id: str, role: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if role not in ["superadmin", "admin", "staff", "normal"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

    user.type = role
    db.commit()
    return {"message": f"User role updated to {role}"}

def delete_user(user_id: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_deleted = True
    user.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "User deleted successfully"}
