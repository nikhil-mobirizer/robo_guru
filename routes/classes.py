from fastapi import Body, APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import schemas
from database import get_db
from services.classes import get_class_by_level ,create_class_in_db, get_all_classes, get_class, create_response
from services.auth import get_current_user  


router = APIRouter()

@router.post("/", response_model=None)
def create_class(
    classes: schemas.ClassCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        created_class = create_class_in_db(db=db, classes=classes)
        response_data = {
            "id": created_class.id,
            "name": created_class.name,
            "level_id": created_class.level_id,
            "tagline": created_class.tagline,
            "image_link": created_class.image_link
        }
        return create_response(success=True, message="Class created successfully", data=response_data)
    except HTTPException as e:
        return create_response(success=False, message=e.detail)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")
    

@router.get("/all_data", response_model=None)
def read_classes(
    limit: int = 1000,
    name: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        classes_list = get_all_classes(db, limit=limit, name=name)

        response_data = [
            {
                "id": cls.id,
                "name": cls.name,
                "level_id": cls.level_id,
                "tagline": cls.tagline,
                "image_link": cls.image_link,
                "subjects": [subject.name for subject in cls.subjects]  
            }
            for cls in classes_list
        ]

        return create_response(success=True, message="Classes retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")
    

@router.get("/", response_model=None)
def read_all_classes(
    request: schemas.ReadClassesRequest, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),   
):
    try:
        limit = request.limit
        name = request.name
        classes_list = get_all_classes(db, limit=limit, name=name)
        if not classes_list:
            return create_response(success=False, message="No classes found for this level")
        response_data = [
            {
                "id": cls.id,
                "name": cls.name,
                "level_id": cls.level_id,
                "tagline": cls.tagline,
                "image_link": cls.image_link
            }
            for cls in classes_list
        ]

        return create_response(success=True, message="Classes retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")


@router.get("/level/{level_id}", response_model=None)
def read_class(
    level_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        db_classes = get_class_by_level(db=db, level_id=level_id)
        if not db_classes:
            return create_response(success=False, message="No classes found for this level")

        response_data = [
            {
                "id": cls.id,
                "name": cls.name,
                "level_id": cls.level_id,
                "tagline": cls.tagline,
                "image_link": cls.image_link
            }
            for cls in db_classes
        ]

        return create_response(success=True, message="Classes retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message=f"An unexpected error occurred: {str(e)}")

