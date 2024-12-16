import requests

def getServerUrl():
    SERVER_URL = input("Enter the host address: ")
    SERVER_PORT = input("Enter the port: ")
    API_STUDENTS = "students"
    students_url = "http://" + SERVER_URL + ":" + SERVER_PORT + "/" + API_STUDENTS
    return students_url

def printMenu():
    print("What do you want to do?")
    print("1.Get students list")
    print("2.Get a specific student information")
    print("3.Save a new student")
    print("4.Change student name")
    print("5.Change student age")
    print("6.Delete student")
    print("7.Exit")
    choice = input("Enter your choice: ")
    return choice

def notNumError(choice, data):
    print("\n" + str(data) + " must be a digit, '" + str(choice) + "' is not a digit, Please try again.")

def choiceIsDiget(choice):
    if choice.isdigit():
        return True
    return False

def choiceIsValid(choice):
    if choiceIsDiget:
        if choice > 0 and choice < 8:
            return True
        else:
            return False
    else:
        return False

def printStudent(student_info):
    print("ID: " + str(student_info["id"]))
    print("Name: " + student_info["name"])
    print("Age: " + str(student_info["age"]))
    print("---------------") 

def printStudentsList():
    students_list = requests.get(students_full_url)
    if students_list.status_code == 200:
        students = students_list.json()["students"]
        print("\n-----students list-----")
        for student in students:
            printStudent(student)   
    else:
        print("\nError")

def printStudentInfo():
    student_id = input("Enter the student ID: ")
    if not choiceIsDiget(student_id):
        notNumError(student_id, "ID")
        return
    student_info = requests.get(students_full_url + "/" + student_id)
    status_code = student_info.status_code
    if status_code == 200:
        print("\n-----student info-----")
        printStudent(student_info.json())
    else:
        print("\nError: Student not found")

def saveNewStudent():
    student_name = input("Enter student name: ")
    student_age = input("Enter student age: ")
    if not choiceIsDiget(student_age):
        notNumError(student_age, "Age")
        return
    student_data = {"name": student_name, "age": student_age}
    new_student = requests.post(students_full_url, json=student_data)
    if new_student.status_code == 201:
        print("\nStudent created successfully:")
        printStudent(new_student.json())
    else:
        print("\nError")

def getStudentById():
    student_id = input("Enter the student ID: ")
    if not choiceIsDiget(student_id):
        notNumError(student_id, "ID")
        return False
    student_info = requests.get(students_full_url + "/" + student_id)
    return student_info.json()

def changeStudentName():
    student_info = getStudentById()
    if not student_info:
        return
    student_info["name"] = input("Enter new student name: ")
    student_new_name = requests.put(students_full_url + "/" + str(student_info["id"]), json=student_info)
    if student_new_name.status_code == 200:
        print("\nChanged Successfully")
    else:
        print("\nError: Change failed")

def changeStudentAge():
    student_info = getStudentById()
    if not student_info:
        return
    student_info["age"] = input("Enter new student age: ")
    student_new_name = requests.put(students_full_url + "/" + str(student_info["id"]), json=student_info)
    if student_new_name.status_code == 200:
        print("\nChanged Successfully")
    else:
        print("\nError: Change failed")

def deleteStudent():
    student_id = input("Enter the student ID: ")
    if not getStudentById():
        return
    delete_student = requests.delete(students_full_url + "/" + student_id)
    if delete_student.status_code == 200:
        print("\nDeleted Successfully")
    else:
        print("\nError: Delete failed")

students_full_url = getServerUrl()

try:
    while True:
        print()
        choice = printMenu()
        if choiceIsDiget(choice):
            choice = int(choice)
        if not choiceIsValid(choice):
            continue
        if choice == 1:
            printStudentsList()
        elif choice == 2:
            printStudentInfo()
        elif choice == 3:
            saveNewStudent()
        elif choice == 4:
            changeStudentName()
        elif choice == 5:
            changeStudentAge()
        elif choice == 6:
            deleteStudent()
        else:
            print("Exiting the program.")
            break
except Exception as e:
    print("Error: an error has accrued, please try again.")