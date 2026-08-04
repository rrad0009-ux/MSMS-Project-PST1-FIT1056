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


# --- Quick Test Code ---
# Create a test student and teacher
s1 = Student(1, "Alice")
s1.enrolled_in.append("Piano")

t1 = Teacher(101, "Mr. Smith", "Guitar")

# Add them to your global databases
student_db.append(s1)
teacher_db.append(t1)

# Print them out to check if they work
print("Student Name:", student_db[0].name)
print("Enrolled In:", student_db[0].enrolled_in)
print("Teacher Name:", teacher_db[0].name, "| Speciality:", teacher_db[0].speciality)