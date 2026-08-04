# MSMS.py - The In-Memory Prototype

# --Data Models---
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

# --- In-Memory Databases --
#Global data stores and ID counters for session 
student_db = []
teacher_db = []
next_student_id = 1
next_teacher_id = 1


#-------------The Core Helper Functions---------------

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



# ---------The Front Desk Functions ------------


def find_student_by_id(student_id):
    """A new helper to find one student by their exact ID."""
    #Loop through student_db. If a student's ID matches student_id, return the student object.
    for student in student_db:
        if student.id == student_id:
            return student
    #If the loop finishes without finding a match, return None.
    return None

def front_desk_register(name, instrument):
    """High-level function to register a new student and enrol them."""
    global next_student_id
    #Create a new Student object, add it to student_db, and increment the ID.
    new_student = Student(next_student_id, name)
    student_db.append(new_student)
    next_student_id += 1
    
    #Immediately call front_desk_enrol() using the new student's ID and the provided instrument.
    front_desk_enrol(new_student.id, instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")

def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in a course."""
    # Use your new find_student_by_id() helper.
    student = find_student_by_id(student_id)
    #If the student is found, append the instrument to their 'enrolled_in' list.
    if student:
        student.enrolled_in.append(instrument)
        print(f"Front Desk: Enrolled student {student_id} in '{instrument}'.")
    else:
        #If the student is not found, print an error message like "Error: Student ID not found."
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)


# --- Main Application ---


def main():
    """Runs the main interactive menu for the receptionist."""
    # Pre-populate some data for easy testing
    add_teacher("Dr. Keys", "Piano")
    add_teacher("Ms. Fret", "Guitar")

    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Lookup Student or Teacher")
        print("4. (Admin) List all Students")
        print("5. (Admin) List all Teachers")
        print("q. Quit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            # Prompt for student name and instrument, then call front_desk_register.
            name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(name, instrument)
        elif choice == '2':
            # Prompt for student ID (as an int) and instrument, then call front_desk_enrol.
            try:
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ")
                front_desk_enrol(student_id, instrument)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '3':
            # Prompt for a search term, then call front_desk_lookup.
            term = input("Enter search term: ")
            front_desk_lookup(term)
        elif choice == '4':
            list_students()
        elif choice == '5':
            list_teachers()
        elif choice.lower() == 'q':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Program Start ---
if __name__ == "__main__":
    main()