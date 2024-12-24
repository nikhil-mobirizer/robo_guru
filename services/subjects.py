from sqlalchemy.orm import Session
from models import Subject
from schemas import SubjectCreate
from fastapi import HTTPException
from models import Class

# Get subjects by class_id from the database
def get_subjects_by_class(db: Session, class_id: int):
    
    return db.query(Subject).filter(Subject.class_id == class_id).all()

# Get all subjects from the database
def get_all_subjects(db: Session, limit: int = 10, name: str = None):
    query = db.query(Subject)

    if name:
        query = query.filter(Subject.name.ilike(f"%{name}%"))
    return query.limit(limit).all()

# Create a new subject in the database
def create_subject(db: Session, subject: SubjectCreate):
    existing_class = db.query(Class).filter(Class.id == subject.class_id).first()
    if not existing_class:
        raise HTTPException(status_code=400, detail="Class does not exists")  
    
    db_subject = Subject(name=subject.name, class_id=subject.class_id, tagline=subject.tagline, image_link=subject.image_link)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject
