#---------------------------------------------------------
#------Main entry point and view layer-----------------
#---------------------------------------------------------

#handles user interactions and CLI menu, passing commands to ScheduleManager

from app.schedule import ScheduleManager

#-----------------------------------------
#-----view functions----------------------
#-----------------------------------------

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
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
        
    # remove from old course
    student.enrolled_course_ids.remove(from_course_id)
    if student_id in old_course.enrolled_student_ids:
        old_course.enrolled_student_ids.remove(student_id)
        
    # add to new course
    if to_course_id not in student.enrolled_course_ids:
        student.enrolled_course_ids.append(to_course_id)
    if student_id not in new_course.enrolled_student_ids:
        new_course.enrolled_student_ids.append(student_id)
        
    manager._save_data()
    print(f"Success: Student {student.name} moved from {old_course.name} to {new_course.name}.")
    return True

#-----------------------------------------
#-----main application loop---------------
#-----------------------------------------

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager()  # create ONE instance of the application brain

    while True:
        print("\n MSMS v3 (Object-Oriented) ")
        print("1.View Daily Roster")
        print("2.Switch Student Course")
        print("3.Check in Student")
        print("q.Quit")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            day = input("Enter day : ").strip()
            front_desk_daily_roster(manager, day)
            
        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                from_course = int(input("Enter current course ID: "))
                to_course = int(input("Enter new course ID: "))
                switch_course(manager, student_id, from_course, to_course)
            except ValueError:
                print("Error: Please enter valid numerical IDs.")
                
        elif choice == '3':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = int(input("Enter course ID: "))
                manager.check_in(student_id, course_id)
            except ValueError:
                print("Error: Please enter valid numerical IDs.")
                
        elif choice.lower() == 'q':
            print("Exiting")
            break
            
        else:
            print("Invalid choice. Please select 1, 2, 3, or q.")

if __name__ == "__main__":
    main()