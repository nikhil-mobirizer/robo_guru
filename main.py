from fastapi import FastAPI, Request, Depends
from database import engine, get_db
import models
from routes import classes, subjects, chapters, topics, login, chat, level
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
import services 
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(login.router, tags=["login"])
app.include_router(level.router, prefix="/level", tags=["level"])
app.include_router(classes.router, prefix="/classes", tags=["classes"])
app.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
app.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
app.include_router(topics.router, prefix="/topics", tags=["topics"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request, db: Session = Depends(get_db)):
#     classes = services.classes.get_classes(db=db)
#     return templates.TemplateResponse("index2.html", {"request": request, "classes": classes})



















# from fastapi.responses import JSONResponse
# # Fetch subjects by class_id
# @app.get("/subjects/{class_id}", response_class=JSONResponse)
# async def get_subjects(class_id: int, db: Session = Depends(get_db)):
#     subjects = services.subjects.get_subjects_by_class(db=db, class_id=class_id)
#     return subjects

# # Fetch chapters by subject_id
# @app.get("/chapters/{subject_id}", response_class=JSONResponse)
# async def get_chapters(subject_id: int, db: Session = Depends(get_db)):
#     chapters = services.chapters.get_chapters_by_subject(db=db, subject_id=subject_id)
#     return chapters

# # Fetch topics by chapter_id
# @app.get("/topics/{chapter_id}", response_class=JSONResponse)
# async def get_topics(chapter_id: int, db: Session = Depends(get_db)):
#     topics = services.topics.get_topics_by_chapter(db=db, chapter_id=chapter_id)
#     return topics
