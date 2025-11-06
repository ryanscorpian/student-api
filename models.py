from sqlmodel import SQLModel, Field
from typing import Optional

class Student(SQLModel, table=True):
    roll_no: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=50)
    age: int = Field(..., le=99)
    student_class: str = Field(..., max_length=50)
