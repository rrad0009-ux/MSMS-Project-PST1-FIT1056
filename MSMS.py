# MSMS.py - The In-Memory Prototype


#-----------------
# --Data Models---
#-----------------

class Student:
    """A blueprint for student objects. Storing student ID and name."""
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        # Store list of instruments that student is learning
        self.enrolled_in = []

class Teacher:
    """A blueprint for teacher objects. Storing teacher ID, name and specialty """
    def __init__(self, teacher_id, name, speciality):
        self.id = teacher_id
        self.name = name
        self.speciality = speciality

#---------------------------
# --- In-Memory Databases and Counters--
#---------------------------


#Global storage lists and incrementing ID counter
student_db = []
teacher_db = []
next_student_id = 1   
next_teacher_id = 1

#-----------------------------------------------------
#-------------Admin Functions---------------
#-----------------------------------------------------


def add_teacher(name, speciality):
    """
    Creates Teacher profile and adds it to the global database. Increments the
    global teacher ID after profile creation.
    """
    global next_teacher_id
    new_teacher = Teacher(next_teacher_id, name, speciality)
    teacher_db.append(new_teacher)
    next_teacher_id += 1
    return new_teacher

def list_students():
    """Shows registered students currently in the system"""
    print("\n--- All Registered Students ---")
    if not student_db:
        print("No students registered yet.")
        return
    for student in student_db:
        print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def list_teachers():
    """Shows registered teachers currently in the system"""
    print("\n--- All Registered Teachers ---")
    if not teacher_db:
        print("No teachers registered yet.")
        return
    for teacher in teacher_db:
        print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

def find_students(term):
    """Searches for students whos name contains the input-string (case insensitive)"""
    print(f"\n--- Finding Students matching '{term}' ---")
    results = []
    
    # Perform substring search across lowercase student names
    for student in student_db:
        if term.lower() in student.name.lower():
            results.append(student)
            
    # search results or 'not found' notice
    if not results:
        print("No match found.")
    else:
        for student in results:
            print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def find_teachers(term):
    """Perform search on teacher name or teacher specialty (case insensitive)"""
    print(f"\n--- Finding Teachers matching '{term}' ---")
    results = []
    
    # Perform substring search across lowercase teacher names and teacher specialty
    for teacher in teacher_db:
        if term.lower() in teacher.name.lower() or term.lower() in teacher.speciality.lower():
            results.append(teacher)
            
    # search results or 'not found' notice
    if not results:
        print("No match found.")
    else:
        for teacher in results:
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")


#-----------------------------------------------
#----User facing workflows and Front Desk  -----
#-----------------------------------------------

def find_student_by_id(student_id):

    """Looks up and returns student by their integer ID. Returns None if no matches"""
    
    for student in student_db:
        if student.id == student_id:
            return student
    
    return None

def front_desk_register(name, instrument):
    """Registers a new student, assigns a integer ID via auto-incrementation, enrolls student in instrument"""
    global next_student_id

    #Creates new student and append to database
    new_student = Student(next_student_id, name)
    student_db.append(new_student)
    next_student_id += 1
    
   #Enrolls student using their new ID
    front_desk_enrol(new_student.id, instrument)
    

def front_desk_enrol(student_id, instrument):
    """Enrollment of existing student to new instrument course via integer ID"""
    student = find_student_by_id(student_id)

#Checks existence of integer ID before appending instrument course data 
    if student:
        # To avoid duplicate entries for the same instrument
        if instrument not in student.enrolled_in:
            student.enrolled_in.append(instrument)
            print(f"Front Desk: Enrolled student {student.id} ('{student.name}') in '{instrument}'.")
        else:
            print(f"Front Desk: Student {student.id} is already enrolled in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term):
    """Lookup function for both student and teacher records"""
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)


#-------------------------
# --- Main Application ---
#-------------------------


def main():
    """Main interactive menu for the front desk interface"""
    # Pre-populate sample teacher data for session testing
    add_teacher("Dr. Keys", "Piano")
    add_teacher("Ms. Fret", "Guitar")


# starting menu 
    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. (Admin) List all Students")
        print("5. (Admin) List all Teachers")
        print("q. Quit")
        
        choice = input("Enter your choice: ").strip()

# option 1: register a new student and enroll them in instrument course
        if choice == '1':
            name = input("Enter student name: ").strip()
            instrument = input("Enter instrument to enrol in: ").strip()
            if name and instrument:
                front_desk_register(name, instrument)
            else:
                print("Error: Student name and instrument cannot be blank.")

# option 2: enroll existing student in a new instrument course using their integer ID           
        elif choice == '2':
            try: #safe conversion of input to integer for efficient ID lookup
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ").strip()
                if instrument:
                    front_desk_enrol(student_id, instrument)
                else:
                    print("Error: Instrument name cannot be blank.")
            except ValueError: #avoids programme from crashing from non numeric input and prints error friendly message
                print("Error: Invalid ID format. Please enter a numerical ID (e.g., 1, 2, 3).")

        # look up for students and teachers by keyword        
        elif choice == '3':
            term = input("Enter search term: ").strip()
            if term:
                front_desk_lookup(term)
            else:
                print("Error: Search term cannot be empty.")


        # display enrolled student records and teacher records        
        elif choice == '4':
            list_students()
            
        elif choice == '5':
            list_teachers()

        # Quit the application loop   
        elif choice.lower() == 'q':
            print("Exiting application. Goodbye!")
            break

        # Handle non-menu selection options    
        else:
            print("Invalid selection. Please enter a valid menu option (1-5 or q).")

#-----------------------
# - Program entry point -
#----------------------

if __name__ == "__main__":
    main()