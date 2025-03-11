from fastapi import APIRouter, Depends, Request
from StudentManager import StudentManager, StudentInput, Student

router = APIRouter()

async def get_StudentManager_obj(request: Request):
    return request.app.state.StudentManager

@router.get(
    "/students",
    summary="Get all students",
    description="Return all students from the external SQL database"        
    )
async def getAllStudents(
    student_manager: StudentManager = Depends(get_StudentManager_obj)
    ) -> list[Student]:
    return student_manager.getAllStudents()

@router.get(
    "/students/{student_id}",
    summary="Gey student by id",
    description="Find a specific student by their id"
    )
async def getStudentById(
    student_id: int,
    student_manager: StudentManager = Depends(get_StudentManager_obj)
    ) -> dict:
    return student_manager.getStudentById(student_id)

@router.post(
    "/students",
    summary="Add new student",
    description="Add a new student to the external SQL database"
    )
async def addNewStudent(
    student: StudentInput,
    student_manager: StudentManager = Depends(get_StudentManager_obj)
    ) -> dict:
    new_student = student_manager.addStudent(student)
    return {"Message": "Student created", "Student": new_student}

@router.put(
    "/students/{student_id}",
    summary="Update existing student",
    description="Update an existing student in the external SQL database"
    )
async def updateStudent(
    student_id: int,
    student: StudentInput,
    student_manager: StudentManager = Depends(get_StudentManager_obj)
    ) -> dict:
    try:
        updated_student = student_manager.updateStudent(student_id, student)
        return {"Message": "Student updated successfully", "Student": updated_student}
    except:
        return {"Message": "Error, invalid input"}
    
@router.delete(
    "/students/{student_id}",
    summary="Delete student",
    description="Delete a student from the external SQL database"
    )
async def deleteStudent(
    student_id: int,
    student_manager: StudentManager = Depends(get_StudentManager_obj)
    ) -> dict:
    deleted_student = student_manager.getStudentById(student_id)
    try:
        student_manager.deleteStudent(student_id)
        return {"Message": "Student deleted successfully", "Student": deleted_student["Student"]}
    except:
        return {"Message": "Error, student not found"}