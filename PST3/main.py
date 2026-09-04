# ---------------------------------------
# main entry point and view layer
# ---------------------------------------

# handles user interactions and cli menu, passing commands to schedulemanager

from app.schedule import ScheduleManager


# -----------------------------
# ----------view functions-----
# -------------------------------

def front_desk_daily_roster(manager, day):
    """displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    found_any = False
    
    # iterate through courses in manager to find lessons matching the day
    for course in manager.courses:
        for lesson in course.lessons:
            if lesson.get("day", "").lower() == day.lower():
                print(f"Course: {course.name} | Instrument: {course.instrument} | Time: {lesson.get('start_time')} | Room: {lesson.get('room')}")
                found_any = True
                
    if not found_any:
        print(f"No lessons found for {day}.")


def switch_course(manager, student_id, from_course_id, to_course_id):
    """switches a student from one course to another and updates database."""
    student = manager.find_student_by_id(student_id)
    old_course = manager.find_course_by_id(from_course_id)
    new_course = manager.find_course_by_id(to_course_id)
    
    # validate that student and both courses exist
    if not student or not old_course or not new_course:
        print("Error: Invalid Student ID or Course ID.")
        return False
        
    if from_course_id not in student.enrolled_course_ids:
        print(f"Error: Student {student.name} is not enrolled in {old_course.name}.")
        return False
        
    # remove student from old course
    student.enrolled_course_ids.remove(from_course_id)
    if student_id in old_course.enrolled_student_ids:
        old_course.enrolled_student_ids.remove(student_id)
        
    # add student to new course
    if to_course_id not in student.enrolled_course_ids:
        student.enrolled_course_ids.append(to_course_id)
    if student_id not in new_course.enrolled_student_ids:
        new_course.enrolled_student_ids.append(student_id)
        
    # save updated records to persistent json storage
    manager._save_data()
    print(f"Success: Student {student.name} moved from {old_course.name} to {new_course.name}.")
    return True


def print_student_card(manager, student_id):
    """generates a text badge file for a student"""
    student = manager.find_student_by_id(student_id)
    if student:
        filename = f"{student_id}_card.txt"
        course_names = []
        for cid in student.enrolled_course_ids:
            c = manager.find_course_by_id(cid)
            if c:
                course_names.append(c.name)
                
        # write formatted id badge to local text file
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write("  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student.id}\n")
            f.write(f"Name: {student.name}\n")
            f.write(f"Enrolled In: {', '.join(course_names) if course_names else 'None'}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")


def front_desk_lookup(manager, term):
    """searches student and teacher records by keyword"""
    print(f"\n--- Performing lookup for '{term}' ---")
    term_lower = term.lower()
    
    # search matching student names
    print("Students:")
    s_matches = [s for s in manager.students if term_lower in s.name.lower()]
    if not s_matches:
        print("  No student matches found.")
    else:
        for s in s_matches:
            print(f"  ID: {s.id}, Name: {s.name}, Enrolled Courses: {s.enrolled_course_ids}")
            
    # search matching teacher names and specialities
    print("Teachers:")
    t_matches = [t for t in manager.teachers if term_lower in t.name.lower() or term_lower in t.speciality.lower()]
    if not t_matches:
        print("  No teacher matches found.")
    else:
        for t in t_matches:
            print(f"  ID: {t.id}, Name: {t.name}, Speciality: {t.speciality}")


# -----------------------------------
# ----------sub menus---------------
# ------------------------------------

# submenu loops grouping operations by category

def student_management_menu(manager):
    """menu handling student actions like add update and delete"""
    while True:
        print("\n--- Student Management ---")
        print("1. Register New Student")
        print("2. Update Student Info")
        print("3. Remove Student")
        print("4. List All Students")
        print("b. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        # register a fresh student profile
        if choice == '1':
            name = input("Enter student name: ").strip()
            if name:
                s = manager.register_student(name)
                print(f"Registered student {s.name} with ID {s.id}.")
            else:
                print("Error: Name cannot be blank.")
                
        # update existing student record
        elif choice == '2':
            try:
                sid = int(input("Enter student ID: "))
                new_name = input("Enter new name (leave blank to skip): ").strip()
                if new_name:
                    manager.update_student(sid, name=new_name)
                else:
                    print("No changes entered.")
            except ValueError:
                print("Error: Please enter a numerical ID.")
                
        # remove student and clear enrolments
        elif choice == '3':
            try:
                sid = int(input("Enter student ID to remove: "))
                manager.remove_student(sid)
            except ValueError:
                print("Error: Please enter a numerical ID.")
                
        # display all registered students
        elif choice == '4':
            print("\n--- All Registered Students ---")
            for s in manager.students:
                print(f"ID: {s.id}, Name: {s.name}, Courses: {s.enrolled_course_ids}")
                
        # return to primary menu
        elif choice.lower() == 'b':
            break


def teacher_management_menu(manager):
    """menu handling teacher actions like add edit and remove"""
    while True:
        print("\n--- Teacher Management ---")
        print("1. Add New Teacher")
        print("2. Update Teacher Info")
        print("3. Remove Teacher")
        print("4. List All Teachers")
        print("b. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        # add a new teacher profile
        if choice == '1':
            name = input("Enter teacher name: ").strip()
            speciality = input("Enter speciality: ").strip()
            if name and speciality:
                manager.add_teacher(name, speciality)
            else:
                print("Error: Fields cannot be blank.")
                
        # edit existing teacher fields
        elif choice == '2':
            try:
                tid = int(input("Enter teacher ID: "))
                new_name = input("Enter new name (blank to skip): ").strip()
                new_spec = input("Enter new speciality (blank to skip): ").strip()
                updates = {}
                if new_name:
                    updates['name'] = new_name
                if new_spec:
                    updates['speciality'] = new_spec
                if updates:
                    manager.update_teacher(tid, **updates)
                else:
                    print("No changes entered.")
            except ValueError:
                print("Error: Please enter a numerical ID.")
                
        # remove a teacher profile
        elif choice == '3':
            try:
                tid = int(input("Enter teacher ID to remove: "))
                manager.remove_teacher(tid)
            except ValueError:
                print("Error: Please enter a numerical ID.")
                
        # display all registered teachers
        elif choice == '4':
            print("\n--- All Registered Teachers ---")
            for t in manager.teachers:
                print(f"ID: {t.id}, Name: {t.name}, Speciality: {t.speciality}")
                
        # return to primary menu
        elif choice.lower() == 'b':
            break


def enrolment_and_roster_menu(manager):
    """menu handling course roster lookups enrolments and swaps"""
    while True:
        print("\n--- Course Enrolments & Rosters ---")
        print("1. View Daily Roster")
        print("2. Switch Student Course")
        print("3. Enrol Student into Course")
        print("4. List All Courses")
        print("b. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        # filter and print lessons by day
        if choice == '1':
            day = input("Enter day (e.g., Monday): ").strip()
            front_desk_daily_roster(manager, day)
            
        # swap courses for an existing student
        elif choice == '2':
            try:
                sid = int(input("Enter student ID: "))
                f_cid = int(input("Enter current course ID: "))
                t_cid = int(input("Enter target course ID: "))
                switch_course(manager, sid, f_cid, t_cid)
            except ValueError:
                print("Error: Please enter numerical IDs.")
                
        # enrol student into a course
        elif choice == '3':
            try:
                sid = int(input("Enter student ID: "))
                cid = int(input("Enter course ID: "))
                s = manager.find_student_by_id(sid)
                c = manager.find_course_by_id(cid)
                if s and c:
                    if cid not in s.enrolled_course_ids:
                        s.enrolled_course_ids.append(cid)
                    if sid not in c.enrolled_student_ids:
                        c.enrolled_student_ids.append(sid)
                    manager._save_data()
                    print(f"Enrolled {s.name} in {c.name}.")
                else:
                    print("Error: Student or Course not found.")
            except ValueError:
                print("Error: Please enter numerical IDs.")
                
        # list all available courses
        elif choice == '4':
            print("\n--- Courses ---")
            for c in manager.courses:
                print(f"ID: {c.id}, Name: {c.name}, Instrument: {c.instrument}, Teacher ID: {c.teacher_id}")
                
        # return to primary menu
        elif choice.lower() == 'b':
            break


def reception_attendance_menu(manager):
    """menu handling front desk checkins student badges and lookups"""
    while True:
        print("\n--- Reception & Attendance ---")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Search Lookup (Students & Teachers)")
        print("b. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        # log attendance checkin
        if choice == '1':
            try:
                sid = int(input("Enter student ID: "))
                cid = int(input("Enter course ID: "))
                manager.check_in(sid, cid)
            except ValueError:
                print("Error: Please enter numerical IDs.")
                
        # print text card file
        elif choice == '2':
            try:
                sid = int(input("Enter student ID: "))
                print_student_card(manager, sid)
            except ValueError:
                print("Error: Please enter a numerical ID.")
                
        # keyword search across records
        elif choice == '3':
            term = input("Enter search term: ").strip()
            if term:
                front_desk_lookup(manager, term)
            else:
                print("Error: Search term cannot be empty.")
                
        # return to primary menu
        elif choice.lower() == 'b':
            break


# ------------------------------------------------------
# ---------main application loop----------------------
# --------------------------------------------------------

# top level runtime menu loop

def main():
    """main function to run the msms application."""
    manager = ScheduleManager()

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("1. Student Management")
        print("2. Teacher Management")
        print("3. Course Enrolments & Rosters")
        print("4. Reception & Attendance")
        print("q. Quit")
        
        choice = input("Enter choice: ").strip()
        
        # navigate to category submenus
        if choice == '1':
            student_management_menu(manager)
        elif choice == '2':
            teacher_management_menu(manager)
        elif choice == '3':
            enrolment_and_roster_menu(manager)
        elif choice == '4':
            reception_attendance_menu(manager)
        elif choice.lower() == 'q':
            print("Exiting MSMS v3. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or q.")


# runtime entry point
if __name__ == "__main__":
    main()