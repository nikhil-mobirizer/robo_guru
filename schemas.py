from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class TopicBase(BaseModel):
    name: str
    tagline: str 
    image_link: str
    details: Optional[str] = None

class TopicCreate(TopicBase):
    name: str
    details: Optional[str] = None
    tagline: str 
    chapter_id: int
    image_link: str

class ReadTopicRequest(BaseModel):
    limit: Optional[int] = 10
    name: Optional[str] = None

class TopicData(TopicBase):
    id: int
    name: str
    details: Optional[str] = None
    tagline: str 
    chapter_id: int
    image_link: str


class Topic(TopicBase):
    id: int

    class Config:
        from_attributes = True  

class ChapterBase(BaseModel):
    name: str
    tagline: str 
    image_link: str

class ChapterCreate(ChapterBase):
    name: str
    tagline: str 
    image_link: str
    subject_id: int

class ReadChapterRequest(BaseModel):
    limit: Optional[int] = 10
    name: Optional[str] = None

class ChapterData(ChapterBase):
    id: int
    name: str
    tagline: str 
    subject_id: int 
    image_link: str


class Chapter(ChapterBase):
    id: int
    topics: list[Topic] = []

    class Config:
        from_attributes = True 

class SubjectBase(BaseModel):
    name: str
    tagline: str 
    image_link: str

class ReadSubjectRequest(BaseModel):
    limit: Optional[int] = 10
    name: Optional[str] = None

class SubjectCreate(SubjectBase):
    name: str
    tagline: str 
    class_id : int 
    image_link: str

class SubjectData(SubjectBase):
    id: int
    name: str
    tagline: str 
    class_id : int 
    image_link: str


class Subject(SubjectBase):
    id: int
    chapters: list[Chapter] = []

    class Config:
        from_attributes = True  

class ClassBase(BaseModel):
    name: str
    tagline: str 
    image_link: str

class ClassCreate(ClassBase):
    name: str
    tagline: str 
    level_id: int
    image_link: str

class ReadClassesRequest(BaseModel):
    limit: Optional[int] = 10
    name: Optional[str] = None
    
class ClassData(ClassBase):
    id: int
    tagline: str 
    image_link: str
    subjects: list[Subject] = []

class Class(ClassBase):
    id: int

    class Config:
        from_attributes = True  

class EducationLevelBase(BaseModel):
    name: str
    description: Optional[str] = None

class EducationLevelCreate(EducationLevelBase):
    pass

class ReadEducationLevelRequest(BaseModel):
    limit: Optional[int] = 10
    name: Optional[str] = None

class EducationLevel(EducationLevelBase):
    id: int

class EducationLevelResponse(EducationLevelBase):
    id: int
    classes: List[str] = []

    class Config:
        orm_mode = True
        
class ResponseModel(BaseModel):
    message: str
    data: Optional[Dict] = None

class ChatRequest(BaseModel):
    session_id: str
    request_message: str


class ChatBase(BaseModel):
    session_id: uuid.UUID
    request_message: str
    response_message: str


class ChatResponse(ChatBase):
    session_id: uuid.UUID
    request_message: str
    response_message: str
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    pass


class SessionResponse(SessionBase):
    id: uuid.UUID
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    chats: List[ChatResponse] = []

    class Config:
        from_attributes = True

