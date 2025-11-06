from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


# Student Table Model
class Student(SQLModel, table=True):
    roll_no: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=50)
    age: int = Field(..., le=99)
    student_class: str = Field(..., max_length=50)


# Model for Partial Update (PATCH)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    student_class: Optional[str] = None
