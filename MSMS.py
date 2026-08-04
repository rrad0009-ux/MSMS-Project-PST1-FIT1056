# MSMS.py - The In-Memory Prototype

# --- Data Models ---
class Student:
    """A blueprint for student objects. Holds their info."""
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        # Initialised an empty list called 'enrolled_in' to store instrument names.
        self.enrolled_in = []

class Teacher:
    """A blueprint for teacher objects."""
    def __init__(self, teacher_id, name, speciality):
        # Assign all three parameters to independant variable
        self.id = teacher_id
        self.name = name
        self.speciality = speciality

# --- In-Memory Databases ---
#Global data stores and ID counters for session 
student_db = []
teacher_db = []
next_student_id = 1
next_teacher_id = 1


#The Core Helper Functions 

def find_students(term):
    """Finds students by name."""
    print(f"\n--- Finding Students matching '{term}' ---")
    results = []
    
    # Loop through student_db. If the search 'term' (case-insensitive) is in the student's name,
    for student in student_db:
        name_in_lower = student.name.lower()
        term_in_lower = term.lower()
        if term_in_lower in name_in_lower:
            results.append(student)        # add them to your results list.
            
    # Check if we found any matching students
    if len(results) == 0:
        #After the loop, if the results list is empty, print "No match found."
        print("No match found.")
    else:
        # Otherwise, print the details for each student in the results list.
        for student in results:
            print(f"  ID: {student.id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

def find_teachers(term):
    """Finds teachers by name or speciality."""
    print(f"\n--- Finding Teachers matching '{term}' ---")
    results = []
    
    # Similar loop to student function,  for the term in BOTH the teacher's name AND their speciality.
    for teacher in teacher_db:
        name_in_lower = teacher.name.lower()
        speciality_in_lower = teacher.speciality.lower()
        term_in_lower = term.lower()
        
        if term_in_lower in name_in_lower or term_in_lower in speciality_in_lower:
            results.append(teacher)
            
    # Check if we found any matching teachers
    if len(results) == 0:
        #After the loop, if the results list is empty, print "No match found."
        print("No match found.")
    else:
        # Otherwise, print the details for each student in the results list.
        for teacher in results:
            print(f"  ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")