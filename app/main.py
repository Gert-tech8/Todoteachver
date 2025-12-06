from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .send_mail import send_otp_email
from . import models
from .database import engine, SessionLocal
from typing import List
from .schema import UserCreate, Task, TaskCreate, TaskUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo Application",
    description="A simple Todo application with user authentication and OTP verification.",
    version="1.0.0",
)

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to my todo application!"}

@app.post("/register/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # check duplicate email
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # validate password length in bytes (bcrypt limit is 72 bytes)
    pwd_bytes = user.password.encode("utf-8")
    if len(pwd_bytes) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long. When encoded to UTF-8 it exceeds 72 bytes; choose a shorter password."
        )

    # hash password
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # create otp
    code = 123456  # In real application, generate a random OTP and send via email/SMS
    otp = models.Otp(
        user_id=db_user.id,
        otp_code=code  # In real application, generate a random OTP and send via email/SMS
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)

    send_otp_email(to_email=db_user.email, otp_code=code)
    # return user without password
    return {
        "id": getattr(db_user, "id", None),
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "email": db_user.email
    }

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=task.owner_id,
        date=task.date,
        time=task.time,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[Task])
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}