from fastapi import APIRouter, Depends, HTTPException, Form, Body
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from database import get_db
import services.topics
from services.auth import get_current_user 
from services.classes import create_response
router = APIRouter()

@router.post("/", response_model=None)
def create_topic(
    topic: schemas.TopicCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        db_topic = services.topics.create_topic(db=db, topic=topic, chapter_id=topic.chapter_id)

        response_data = {
            "id": db_topic.id,
            "name": db_topic.name,
            "chapter_id":db_topic.chapter_id,
            "details":db_topic.details,
            "tagline": db_topic.tagline,
            "image_link": db_topic.image_link
        }
        return create_response(success=True, message="Topic created successfully", data=response_data)
    except HTTPException as e:
        return create_response(success=False, message=e.detail)
    except Exception as e:
        return create_response(success=False, message="An unexpected error occurred")


@router.get("/", response_model=None)
def read_all_topics(
    request: schemas.ReadTopicRequest, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),   
):
    try:
        limit = request.limit
        name = request.name
        topics = services.topics.get_all_topics(db, limit=limit, name=name)

        response_data = [
            {
                "id": sub.id,
                "name": sub.name,
                "chapter_id":sub.chapter_id,
                "tagline": sub.tagline,
                "details": sub.details,
                "image_link": sub.image_link
            }
            for sub in topics
        ]

        return create_response(success=True, message="Topic retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message=f"An unexpected error occurred: {e}")


@router.get("/chapter/{chapter_id}", response_model=None)
def read_topic(
    chapter_id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user), 
):
    try:
        db_topic = services.topics.get_topics_by_chapter(db=db, chapter_id=chapter_id)
        if not db_topic:
            raise HTTPException(status_code=404, detail="No topics found for the chapter")
        response_data = [
            {
                "id": sub.id,
                "name": sub.name,
                "chapter_id":sub.chapter_id,
                "tagline": sub.tagline,
                "details": sub.details,
                "image_link": sub.image_link
            }
            for sub in db_topic
        ]

        return create_response(success=True, message="Topics retrieved successfully", data=response_data)
    except Exception as e:
        return create_response(success=False, message=f"An unexpected error occurred: {e}")




# @router.get("/all_data", response_model=List[schemas.TopicData])
# def read_topics(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
#     topics = services.topics.get_topics(db, skip=skip, limit=limit)
#     return topics