from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from services.users import (
    get_all_users,
    update_user_role,
    delete_user,
    register_user,
)
from services.dependencies import superadmin_only  
from schemas import UserCreate
from services.auth import get_current_user  
from services.classes import create_response


router = APIRouter()

@router.post("/register", response_model=None)
def create_user(
    user: UserCreate= Body(...),
    db: Session = Depends(get_db),
):
    try:
        registered_user = register_user(user, db)
        response_data = {
            "name": registered_user.name,
            "mobile_number": registered_user.mobile_number,
            "date_of_birth": registered_user.date_of_birth,
            "occupation": registered_user.occupation,
        }   
        return create_response(success=True, message="Registration successfully", data=response_data)
    except HTTPException as e:
        return create_response(success=False, message=e.detail)
    except Exception as e:
        return create_response(success=False, message= f"An unexpected error occurred: {str(e)}")
             

@router.get("/users", response_model=None)
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    superadmin_only(current_user) 
    try:
        user_list = get_all_users(db)
        if not user_list:
            return create_response(success=False, message="User not found")
        response_data = [
            {
                "id": user.user_id,
                "name": user.name,
                "mobile_number": user.mobile_number,
                "email": user.email,
                "date_of_birth": user.date_of_birth,
                "occupation": user.occupation,
            }  
            for user in user_list
        ]
        return create_response(success=True, message="User list retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")


@router.delete("/users/{user_id}")
def remove_user(user_id: str, db: Session = Depends(get_db), _: User = Depends(superadmin_only)):
    return delete_user(user_id, db)
