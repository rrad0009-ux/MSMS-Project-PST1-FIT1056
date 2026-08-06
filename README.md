**Music School Management System : In Memory Prototype**

Application designed for student registration, instrument course enrolments, administrative data reporting, student and teacher lookup features. 
This was developed for FIT1056: Introduction to Software Engineering (PST1)

**What the system does**
The system is a digital prototype for front desk receptionists and administrators of the school and replaces manual record-keeping by giving an interface to manage student and teacher profiles.
Its functions include: 

- Student registration: Registers student and gives unique student ID via sequential integers and enrolls them in the course through the choice of instrument
- Course enrolment: Enrolls existing students to other/additional instrument courses using their student ID.
- Prevention of duplicate students: Checks existing enrollments to prevent enrolling a student in the same instrument course more than once
- Student/Teacher Lookup: Uses keywords to look up student names, teacher names, teacher specialty (case-insensitive)
- Displays overview of all registered students and teaching staff
- Catches non numeric ID's without crashing the system using 'try-except'

**Major parts and functions**

*In memory storage*
'class Student' is used as a blueprint to store student objects  (id, name, instrument enrollment)
'class Teacher' is used as a blueprint for teacher objects (id, name, specialty)
Contains global storage and counters, where 'student_db' and 'teacher_db' are the temporary global lists and 'next_student_id' and 'next_teacher_id' are incrementing integer key counters

*admin functions*
add_teacher(name, specialty) : creates a Teacher profile and appends it to teacher_db and increments the global ID counter
list_students() and list_teachers(): prints formatted listings of student_db and teacher_db records respecitvely 
find_student(term) : searches matching names of students (case-insensitive)
find_teachers(term) : searches teacher_db for teachers whos names matches or specialty matches (case-insensitive) 

*front desk functions*
find_student_by_id(student_id) : searches through student_db to locate student by ID, returns None if not found
front_desk_register(name,instrument) : registers new student via next_student_id, increments counter and summons front_desk_enrol to assign course
front_desk_enrol(student_id, instrument): checks student existence and appends the new instrument to enrolled_in if not already present
front_desk_lookup(term) : combines find_students and find_teachers to create search across both databases 

*application loop*
main() : manages the 'while' and 'True' application loop, pre-populates sample teacher names, displays menu, collects user input and routes choice

**How to run the program**

*Prerequisites*
Python 3.8 Installed
Terminal access

*Execution*
Navigate to project folder through terminal by opening it. Run application through scripts as shown below

cd msms-project
python MSMS.py

Now Test out the program by interacting with the start menu 

**Testing out the program**

*Test 1 Registration of new Student* 
- Chose menu option 1
- Input Name: Rahul
- Input Instrument: Guitar
- Expected output: Confirmation that student Rahul was registered and enrolled in Guitar with ID 1

*Test 2 Enrollment of existing student in another instrument course*
- Chose menu option 2
- Input student ID: 1 (as newly registered student Rahul from the previous test)
- Input instrument: Piano 
- Expected output: Confirms student 1 is enrolled in Piano 

*Test 3: Verify duplicate course enrollment *
- Chose menu option 2
- Input student ID: 1
- Input instrument: Piano 
- Expected output: Confirms that student 1 is already enrolled in Piano 

*Test 4: Search Records*
- Chose menu option 3
- Enter search name: "key"
- Expected output: Returns "Dr.Keys" as existing/matching teacher

*Test 5: View student/teacher list for admin purposes*
- Chose option 4: to view all registered students 
- Chose option 5: to view all registered teachers

*Test 6: Error Guardrails*
- Chose menu option 2
- Type "abc" when asked for ID
- Expected output: "Error: Invalid ID format. Please enter numberical ID" 
- Guardrail protects the application from crashing

**Assumptions, Design Choices, Extensions**

*Design Choices* 
- Case-insensitive searching: applied .lower() to search properties and queries to return same results (for e.g. "PIANO", "Piano" would still be returned as "piano")

- Sequential auto-incrementation: Uses simple integer counter to ensure lookups are easy and straight forward


