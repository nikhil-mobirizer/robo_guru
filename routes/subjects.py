from fastapi import APIRouter, Depends, HTTPException, Form, Body
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import get_db
import services.subjects
from services.auth import get_current_user 
from typing import List, Optional
from services.classes import create_response

router = APIRouter()

@router.post("/", response_model=None)
def create_subject(
    subject: schemas.SubjectCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:   
        created_subject = services.subjects.create_subject(db=db, subject=subject)

        response_data = {
            "id": created_subject.id,
            "name": created_subject.name,
            "class_id":created_subject.class_id,
            "tagline": created_subject.tagline,
            "image_link": created_subject.image_link
        }
        return create_response(success=True, message="Subject created successfully", data=response_data)
    except HTTPException as e:
        return create_response(success=False, message=e.detail)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")
    

@router.get("/", response_model=None)
def read_all_subjects(
    request: schemas.ReadSubjectRequest, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        limit = request.limit
        name = request.name
        subjects_list = services.subjects.get_all_subjects(db, limit=limit, name=name)
        if not subjects_list:
            return create_response(success=False, message="No subjects found for the class")
        response_data = [
            {
                "id": sub.id,
                "name": sub.name,
                "class_id":sub.class_id,
                "tagline": sub.tagline,
                "image_link": sub.image_link
            }
            for sub in subjects_list
        ]

        return create_response(success=True, message="Subjects retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")
    
@router.get("/class/{class_id}", response_model=None)
async def get_subjects_by_class(
    class_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  
):
    try:
        subjects = services.subjects.get_subjects_by_class(db, class_id)
        if not subjects:
            return create_response(success=False, message="No subjects found for the class")
        response_data = [
            {
                "id": sub.id,
                "name": sub.name,
                "class_id":sub.class_id,
                "tagline": sub.tagline,
                "image_link": sub.image_link
            }
            for sub in subjects
        ]

        return create_response(success=True, message="Subjects retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message= f"An unexpected error occurred: {str(e)}")
















# @router.get("/all_data", response_model=List[schemas.SubjectData])
# def read_subjects(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
#     subjects = services.subjects.get_subjects(db, skip=skip, limit=limit)
#     return subjects

# @router.get("/{subject_id}", response_model=schemas.Subject)
# def read_subject(subject_id: int, db: Session = Depends(get_db)):
#     db_subject = services.subjects.get_subject(db=db, subject_id=subject_id)
#     if db_subject is None:
#         raise HTTPException(status_code=404, detail="Subject not found")
#     return db_subject