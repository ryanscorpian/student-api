from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, select, create_engine, Field
from typing import Optional

templates = Jinja2Templates(directory="templates")

#Database setup

DATABASE_URL = "sqlite:///./students.db"  # SQLite file
engine = create_engine(DATABASE_URL, echo=True)

#student model

class Student(SQLModel,table = True):
    roll_no : Optional[int] = Field(default = None , primary_key=True )
    name : str = Field(...,max_length =50)
    age : int = Field(...,le = 99)
    student_class : str = Field(...,max_length=50)

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    student_class: Optional[str] = None

 # Create the table in the database

SQLModel.metadata.create_all(engine)   

# FastAPI app

app = FastAPI(title="student API")

@app.post("/student/",response_model=Student)
def create_student(student: Student):
    with Session(engine)as session:
        session.add(student)
        session.commit()
        session.refresh(student) # get auto-generated roll_no
        return student

@app.get("/student/", response_model=list[Student])
def read_student():
    with Session(engine) as session:
        statement = select(Student)
        students = session.exec(statement).all()
        return students

@app.get("/student/{roll_no}", response_model=str)
def get_student(roll_no: int):
    with Session(engine) as session:
        statement = select(Student).where(Student.roll_no == roll_no)
        student = session.exec(statement).first()
        if not student:
         raise HTTPException(status_code=404, detail="Student not found")
        return  student

@app.patch("/student/{roll_no}", response_model=Student)
def update_student(roll_no : int , updates : StudentUpdate):
     with Session(engine) as session:
        statement = select(Student).where(Student.roll_no == roll_no)
        student = session.exec(statement).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        for key,value in updates.dict(exclude_unset=True).items():
            setattr(student,key,value)

        session.add(student)
        session.commit()
        session.refresh(student)
        return student

@app.delete("/student/{roll_no}")
def delete_student(roll_no: str):
    with Session(engine) as session:
        statement = select(Student).where(Student.roll_no == roll_no)
        student = session.exec(statement).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
    
        session.delete(student)
        session.commit()
        return {"message": f"Student with roll no {roll_no} deleted successfully"}
    
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    print("➡️ Home route called")  # Add this line
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
    return templates.TemplateResponse("index.html", {"request": request, "students": students})








    
           
    



    

     











    

