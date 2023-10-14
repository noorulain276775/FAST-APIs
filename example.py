from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {
        "name": "noor",
        "age": 15,
        "year": "9th B"
    },

    2: {
        "name": "fatima",
        "age": 15,
        "year": "9th B"
    }
}


class Students(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None



@app.get('/')
def home():
    return {"message": "Your fast api is working"}


@app.get('/student/{id}')
def get_student(id: int = Path(..., description="Type ID of the tsudent you want to view", ge=0)):
    student_info = students.get(id) 
    if student_info is not None:
        return student_info
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@app.get('/student-name')
def get_student_name(*, name: Optional[str]= None, age: int):
    for student_id in students:
        if (students[student_id]["name"] == name) and (students[student_id]["age"] == age):
            return students[student_id]
        else:
            raise HTTPException(status_code=404, detail=f"Student with this {name} and {age} not found ")
        

@app.post('/create_students/{id}')
def create_students(id: int, student: Students):
    if id in students:
        raise HTTPException(status_code=500, detail=f"Student with this {id} already exist")
    students[id] = student
    return students[id]


@app.put('/update_students/{id}')
def update_students(id: int, student : UpdateStudent):
    if id in students:
        if student.name != None:
            students[id].name = student.name
        if student.age != None:
            students[id].age = student.age
        if student.name != None:
            students[id].year = student.year

        return students[id]
    raise HTTPException(status_code=500, detail=f"Student with this {id} already exist")
    