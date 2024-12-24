from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import EducationLevelCreate, ReadEducationLevelRequest
from models import EducationLevel
from services.level import get_all_education_levels, create_education_level, get_all_education_levels, get_education_level
from services.auth import get_current_user  
from services.classes import create_response

router = APIRouter()

@router.post("/", response_model=None)
def create_level(
    level: EducationLevelCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        created_level = create_education_level(db=db, level=level)
        response_data = {
            "id": created_level.id,
            "name": created_level.name,
            "description": created_level.description
        }
        return create_response(success=True, message="Education Level created successfully", data=response_data)
    except HTTPException as e:
        return create_response(success=False, message=e.detail)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")
            


@router.get("/", response_model=None)
def read_all_levels(
    request: ReadEducationLevelRequest, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),   
):
    try:
        limit = request.limit
        name = request.name
        level_list = get_all_education_levels(db, limit=limit, name=name)
        if level_list is None:
            return create_response(success=False, message="Education Level not found")
        response_data = [
            {
                "id": l.id,
                "name": l.name,
                "description": l.description
            }
            for l in level_list
        ]

        return create_response(success=True, message="Education Level retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")

@router.get("/{level_id}", response_model=None)
def read_level(
    level_id: int = 1000,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  
):
    try:
        db_level = get_education_level(db=db, level_id=level_id)
        if db_level is None:
            return create_response(success=False, message="Education Level not found")

        response_data = {
            "id": db_level.id,
            "name": db_level.name,
            "description": db_level.description
        }

        return create_response(success=True, message="Education levels retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")

@router.get("/all_data", response_model=None)
def read_levels(
    limit: int = 1000,
    name: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        levels_list = get_all_education_levels(db, limit=limit, name=name)
        if levels_list is None:
            return create_response(success=False, message="Education Level not found")
        response_data = [
            {
                "id": l.id,
                "name": l.name,
                "description": l.description,
                "classes": [c.name for c in l.classes]
            }
            for l in levels_list
        ]

        return create_response(success=True, message="Education levels retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message=f"An unexpected error occurred: {str(e)}")