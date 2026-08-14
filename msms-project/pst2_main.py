# pst2_main.py - The Persistent Application

#----------------------------------------
# Global dictionary holding all persistent data
#-----------------------------------------

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will be holding all the application data

#-----------------------------------------
# File persistence and data storage 
#-----------------------------------------


def load_data(path=DATA_FILE):
    """Loads data from JSON file into the global app_data dictionary. Makes default structure if file doesnt exist """
    global app_data
    try:
        with open(path, 'r') as f:
            # Load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # dictionary structure for starting fresh lists
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Serialises and writes global app_data dictionary to JSON file"""
    # open file in write mode and format output with indent = 4 
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

#-------------------------------------
#Student registration and lookup services
#-------------------------------------

def find_student_by_id(student_id):
    """Looks up and returns student dictionary by integer ID or None if not found"""
    for student in app_data['students']:
        if student['id'] == student_id:
            return student
    return None

def front_desk_register(name, instrument):
    """Registers a new student, assigns a unique integer ID, and enrols them in an initial instrument."""
    student_id = app_data['next_student_id']
    new_student = {
        "id": student_id,
        "name": name,
        "enrolled_in": []
    }
    app_data['students'].append(new_student)
    app_data['next_student_id'] += 1
    
    # Immediately enrol student in their first instrument
    front_desk_enrol(student_id, instrument)

def front_desk_enrol(student_id, instrument):
    """Enrols an existing student's course list into a new instrument course. Prevents duplicate enrolment for same instrument"""
    student = find_student_by_id(student_id)
    if student:
        if instrument not in student['enrolled_in']:
            student['enrolled_in'].append(instrument)
            print(f"Front Desk: Enrolled student {student['id']} ('{student['name']}') in '{instrument}'.")
        else:
            print(f"Front Desk: Student {student['id']} is already enrolled in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def list_students():
    """Displays all registerd students their assigned integer ID and enrolled instrument course"""
    print("\n--- All Registered Students ---")
    if not app_data['students']:
        print("No students registered yet.")
        return
    for student in app_data['students']:
        print(f"  ID: {student['id']}, Name: {student['name']}, Enrolled in: {student.get('enrolled_in', [])}")

def list_teachers():
    """Shows all registered teachers their assigned integer ID and specialities"""
    print("\n--- All Registered Teachers ---")
    if not app_data['teachers']:
        print("No teachers registered yet.")
        return
    for teacher in app_data['teachers']:
        print(f"  ID: {teacher['id']}, Name: {teacher['name']}, Speciality: {teacher.get('speciality', 'N/A')}")

def front_desk_lookup(term):
    """Performs a case-insensitive search across student names, teacher names and teacher specialities"""
    print(f"\n--- Performing lookup for '{term}' ---")
    term_lower = term.lower()
    
    print("Students:")
    student_matches = [s for s in app_data['students'] if term_lower in s['name'].lower()]
    if not student_matches:
        print("  No student matches found.")
    else:
        for s in student_matches:
            print(f"  ID: {s['id']}, Name: {s['name']}, Enrolled in: {s.get('enrolled_in', [])}")
            
    print("Teachers:")
    teacher_matches = [t for t in app_data['teachers'] if term_lower in t['name'].lower() or term_lower in t.get('speciality', '').lower()]
    if not teacher_matches:
        print("  No teacher matches found.")
    else:
        for t in teacher_matches:
            print(f"  ID: {t['id']}, Name: {t['name']}, Speciality: {t.get('speciality', 'N/A')}")



#--------------------------------
# Administrative data management (CRUD OPERATIONS) 
#-------------------------------


def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store with auto incremented ID"""
    teacher_id = app_data['next_teacher_id']
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Updates field for a teacher matching with ID"""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return True
    print(f"Error: Teacher with ID {teacher_id} not found.")
    return False

def remove_teacher(teacher_id):
    """Removes a teacher from the data store via ID by list filtering"""
    initial_count = len(app_data['teachers'])
    app_data['teachers'] = [t for t in app_data['teachers'] if t['id'] != teacher_id]
    
    if len(app_data['teachers']) < initial_count:
        print(f"Teacher {teacher_id} removed.")
        return True
    else:
        print(f"Error: Teacher with ID {teacher_id} not found.")
        return False

def update_student(student_id, **fields):
    """Updates field for a student matching with ID"""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return True
    print(f"Error: Student with ID {student_id} not found.")
    return False

def remove_student(student_id):
    """Removes a student from the data store via ID by list filtering"""
    initial_count = len(app_data['students'])
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    
    if len(app_data['students']) < initial_count:
        print(f"Student {student_id} removed.")
        return True
    else:
        print(f"Error: Student with ID {student_id} not found.")
        return False


#-----------------------------
# Front desk and badge generation
#------------------------------

def check_in(student_id, course_id, timestamp=None):
    """Records attendence check in with an ISO timestamp and appends it the persistent attendance ledger"""
    if timestamp is None:
        # Get the current time as an ISO formatted string
        timestamp = datetime.datetime.now().isoformat()
    
    # Create a check-in record dictionary
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    
    # Append this new record to the global attendance list
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    """Generates and saves student ID badge file locally. Formatted to plain text"""
    # Find the student dictionary in app_data['students']
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # Create a filename based on the student's ID
        filename = f"{student_id}_card.txt"
        
        # Open and write the student card details in a clean format
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write("  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
            
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")


#------------------------------
# User interface and Interactive loop
#------------------------------

def main():
    """Main application controller loop managing user interaction and trigger persistence saves"""
    load_data() # Load all data from JSON file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Check-in Student")
        print("4. Print Student Card")
        print("5. Lookup Student or Teacher")
        print("6. Add New Teacher")
        print("7. Update Teacher Info")
        print("8. Remove Teacher")
        print("9. Update Student Info")
        print("10. Remove Student")
        print("11. List All Students")
        print("12. List All Teachers")
        print("q. Quit and Save")
        
        choice = input("Enter your choice: ").strip()
        made_change = False # A flag to track if we need to save changes

        # option 1:Register new student 
        if choice == '1':
            name = input("Enter student name: ").strip()
            instrument = input("Enter instrument to enrol in: ").strip()
            if name and instrument:
                front_desk_register(name, instrument)
                made_change = True
            else:
                print("Error: Name and instrument cannot be blank.")

        # option 2: enroll existing student
        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ").strip()
                if instrument:
                    front_desk_enrol(student_id, instrument)
                    made_change = True
                else:
                    print("Error: Instrument name cannot be blank.")
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        # option 3: check in student
        elif choice == '3':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = input("Enter course name/ID: ").strip()
                if course_id:
                    check_in(student_id, course_id)
                    made_change = True
                else:
                    print("Error: Course ID cannot be empty.")
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        #option 4: print student card badge 
        elif choice == '4':
            try:
                student_id = int(input("Enter student ID: "))
                print_student_card(student_id)
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        # option 5: search and lookup 
        elif choice == '5':
            term = input("Enter search term: ").strip()
            if term:
                front_desk_lookup(term)
            else:
                print("Error: Search term cannot be empty.")

        #option 6: add a new teacher 
        elif choice == '6':
            name = input("Enter teacher name: ").strip()
            speciality = input("Enter teacher speciality (e.g. Piano, Guitar): ").strip()
            if name and speciality:
                add_teacher(name, speciality)
                made_change = True
            else:
                print("Error: Teacher name and speciality cannot be blank.")

        # option 7: update teacher info 
        elif choice == '7':
            try:
                teacher_id = int(input("Enter teacher ID: "))
                new_speciality = input("Enter new speciality (leave blank to skip): ").strip()
                new_name = input("Enter new teacher name (leave blank to skip): ").strip()
                
                updates = {}
                if new_speciality:
                    updates['speciality'] = new_speciality
                if new_name:
                    updates['name'] = new_name
                
                if updates:
                    if update_teacher(teacher_id, **updates):
                        made_change = True
                else:
                    print("No updates provided.")
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        # option 8: remove teacher
        elif choice == '8':
            try:
                teacher_id = int(input("Enter teacher ID to remove: "))
                if remove_teacher(teacher_id):
                    made_change = True
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        # option 9: update student info
        elif choice == '9':
            try:
                student_id = int(input("Enter student ID: "))
                new_name = input("Enter new student name (leave blank to skip): ").strip()
                
                updates = {}
                if new_name:
                    updates['name'] = new_name
                
                if updates:
                    if update_student(student_id, **updates):
                        made_change = True
                else:
                    print("No updates provided.")
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        #option 10: remove student
        elif choice == '10':
            try:
                student_id = int(input("Enter student ID to remove: "))
                if remove_student(student_id):
                    made_change = True
            except ValueError:
                print("Error: Invalid ID format. Please enter a numerical ID.")

        #option 11: list students
        elif choice == '11':
            list_students()

        #option 12: list teachers
        elif choice == '12':
            list_teachers()

        #option quit application 
        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break

        else:
            print("Invalid choice. Please select a valid menu option (1-12 or q).")
            
        # save data after modifying action 
        if made_change:
            save_data()

    save_data() # Save one final time on exit

#-----------------------
# Application runtime entry 
#-----------------------

if __name__ == "__main__":
    main()