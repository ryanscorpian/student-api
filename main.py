from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Session, select, create_engine
from models import Student, StudentUpdate  # ✅ Import models from separate file
from fastapi import Form
from fastapi.responses import RedirectResponse

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create DB tables
SQLModel.metadata.create_all(engine)

# FastAPI app
app = FastAPI(title="Student API")



@app.post("/student/", response_model=Student)
def create_student(student: Student):
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student


@app.get("/student/", response_model=list[Student])
def read_student():
    with Session(engine) as session:
        statement = select(Student)
        students = session.exec(statement).all()
        return students


@app.get("/student/{roll_no}", response_model=Student)
def get_student(roll_no: int):
    with Session(engine) as session:
        statement = select(Student).where(Student.roll_no == roll_no)
        student = session.exec(statement).first()  # fixed
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
    return templates.TemplateResponse("students.html", {"request": request, "students": students})


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

@app.get("/student/delete/{roll_no}")
def delete_student(roll_no: int):
    with Session(engine) as session:
        student = session.get(Student, roll_no)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student)
        session.commit()
    return RedirectResponse(url="/", status_code=303)

