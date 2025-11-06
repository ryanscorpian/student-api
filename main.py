from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import SQLModel, Session, select, create_engine
from models import Student

# -----------------------------
# Database setup
# -----------------------------
# Use /tmp for Render or SQLite locally
DATABASE_URL = "sqlite:///./students.db"  # Change to sqlite:////tmp/students.db on Render for ephemeral storage
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)

# -----------------------------
# FastAPI app and templates
# -----------------------------
app = FastAPI(title="Student API")
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Routes
# -----------------------------

# Display student list and form
@app.get("/", response_class=HTMLResponse)
def read_students(request: Request):
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
    return templates.TemplateResponse("students.html", {"request": request, "students": students})

# Add student from HTML form
@app.post("/student/form")
def create_student_form(
    name: str = Form(...),
    age: int = Form(...),
    student_class: str = Form(...)
):
    student = Student(name=name, age=age, student_class=student_class)
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
    return RedirectResponse(url="/", status_code=303)

# Delete student
@app.get("/student/delete/{roll_no}")
def delete_student(roll_no: int):
    with Session(engine) as session:
        student = session.get(Student, roll_no)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student)
        session.commit()
    return RedirectResponse(url="/", status_code=303)
