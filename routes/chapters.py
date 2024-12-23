from fastapi import APIRouter, Depends, HTTPException, Form, Body
from typing import List, Optional
import schemas
from database import get_db
import services.chapters
from sqlalchemy.orm import Session
from services.auth import get_current_user
from services.classes import create_response

router = APIRouter()


@router.post("/", response_model=None)
def create_chapter(
    chapter: schemas.ChapterCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  
):
    try:
        created_chapter = services.chapters.create_chapter_in_db(db=db, chapter=chapter, subject_id=chapter.subject_id)

        response_data = {
            "id": created_chapter.id,
            "name": created_chapter.name,
            "subject_id":created_chapter.subject_id,
            "tagline": created_chapter.tagline,
            "image_link": created_chapter.image_link
        }
        return create_response(success=True, message="Chapter created successfully", data=response_data)
    except HTTPException as e:
        return create_response(success=False, message=e.detail)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")

@router.get("/", response_model=None)
def read_all_chapters(
    request: schemas.ReadChapterRequest, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        limit = request.limit
        name = request.name
        chapters_list = services.chapters.get_all_chapters(db, limit=limit, name=name)

        response_data = [
            {
                "id": sub.id,
                "name": sub.name,
                "subject_id":sub.subject_id,
                "tagline": sub.tagline,
                "image_link": sub.image_link
            }
            for sub in chapters_list
        ]

        return create_response(success=True, message="Chapters retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message=f"An unexpected error occurred: {e}")

@router.get("/subject/{subject_id}", response_model=None)
async def get_chapters_by_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        chapters = services.chapters.get_chapters_by_subject(db, subject_id)
        if not chapters:
            raise HTTPException(status_code=404, detail="No chapters found for the subject")
        response_data = [
            {
                "id": sub.id,
                "name": sub.name,
                "subject_id":sub.subject_id,
                "tagline": sub.tagline,
                "image_link": sub.image_link
            }
            for sub in chapters
        ]

        return create_response(success=True, message="Subjects retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")







# @router.get("/{chapter_id}", response_model=schemas.Chapter)
# def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
#     db_chapter = services.chapters.get_chapter(db=db, chapter_id=chapter_id)
#     if db_chapter is None:
#         raise HTTPException(status_code=404, detail="Chapter not found")
#     return db_chapter