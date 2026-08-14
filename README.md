**Music school management system : Persistent application**

Application designed for student registration, instrument course enrolments, administrative data reporting, student and teacher lookup features, attendance tracking, and student badge generation with json file persistence. 
This was developed for FIT1056 (PST2)

**What the system does**
The system is a digital prototype for front desk receptionists and administrators of the school and replaces manual record keeping by giving an interface to manage student and teacher profiles with data saved to a json file.


- Student registration: Registers student and gives unique student id via sequential integers and enrols them in the course through the choice of instrument
- Course enrolment: Enrols existing students to other/additional instrument courses using their student id
- Prevention of duplicate enrolments: Checks existing enrolments to prevent enrolling a student in the same instrument course more than once
- Student/teacher lookup: Uses keywords to look up student names, teacher names, teacher speciality (case insensitive)
- Attendance check in: Records student attendance with an iso timestamp into the persistent ledger
- ID badge printing: Generates a plain text id badge file for any registered student
- Full administrative crud operations: Allows adding, updating, and removing both teacher and student records
- Displays overview of all registered students and teaching staff
- Catches non numeric ids without crashing the system using try except blocks
- Automatic persistence: Saves changes directly to the json data file upon any modification

**Major parts and functions**

*File persistence and data storage*
global app_data dictionary holds all persistent application data, containing lists for students, teachers, attendance, and counter integers next_student_id and next_teacher_id
load_data(path): loads data from msms.json into app_data or initializes default empty structure if file does not exist
save_data(path): serializes and writes app_data to the json file with indentation

*Admin functions*
add_teacher(name, speciality): creates a teacher record with an auto incremented id and adds it to the list
update_teacher(teacher_id, **fields): updates fields for a teacher matching the given id
remove_teacher(teacher_id): removes a teacher from the data store via id filtering
update_student(student_id, **fields): updates fields for a student matching the given id
remove_student(student_id): removes a student from the data store via id filtering
list_students() and list_teachers(): prints formatted listings of all registered students and teachers respectively

*Front desk functions*
find_student_by_id(student_id): looks up and returns a student dictionary by integer id or none if not found
front_desk_register(name, instrument): registers a new student with next_student_id and immediately calls front_desk_enrol to assign an initial instrument
front_desk_enrol(student_id, instrument): checks student existence and appends the new instrument to enrolled_in if not already present
front_desk_lookup(term): performs a case insensitive search across student names, teacher names, and teacher specialities
check_in(student_id, course_id, timestamp): records student check in with an iso timestamp into the attendance list
print_student_card(student_id): generates a formatted text file badge for the specified student

*Application loop*
main(): manages the interactive loop, loads data on startup, displays a 12 option menu

**How to run the program**

*Prerequisites*
Python 3.8 installed
Terminal access

*Execution*
Navigate to project folder through terminal by opening it. Run application through scripts as shown below

cd msms-project
python pst2_main.py

Now test out the program by interacting with the start menu 

**Testing out the program**

*Test 1 Registration of new student* 
- Chose menu option 1
- Input name: Rahul
- Input instrument: Guitar
- Expected output: Confirmation that student 1 was enrolled in Guitar

*Test 2 Enrolment of existing student in another instrument course*
- Chose menu option 2
- Input student id: 1
- Input instrument: Piano 
- Expected output: Confirms student 1 is enrolled in Piano 

*Test 3 Verify duplicate course enrolment*
- Chose menu option 2
- Input student id: 1
- Input instrument: Piano 
- Expected output: Confirms that student 1 is already enrolled in Piano 

*Test 4 Student check in*
- Chose menu option 3
- Input student id: 1
- Input course name/id: Guitar
- Expected output: Confirms student 1 checked into Guitar

*Test 5 Print student badge card*
- Chose menu option 4
- Input student id: 1
- Expected output: Confirmation message indicating printed student card to 1_card.txt

*Test 6 Search records*
- Chose menu option 5
- Enter search name: rahul
- Expected output: Returns matching student details for Rahul

*Test 7 Add and update teacher info*
- Chose menu option 6, enter name Dr. Keys and speciality Piano
- Chose menu option 7, input teacher id 1, enter new speciality Keyboard
- Expected output: Confirms teacher added and updated successfully

*Test 8 View student/teacher list for admin purposes*
- Chose option 11 to view all registered students 
- Chose option 12 to view all registered teachers

*Test 9 Error guardrails*
- Chose menu option 2
- Type abc when asked for id
- Expected output: Error: Invalid ID format. Please enter a numerical ID.
- Guardrail protects the application from crashing

**Assumptions, Design Choices, Extensions**

*Design choices* 
- Case insensitive searching: applied lower method to search properties and queries to return consistent results across names and specialities
- Sequential auto incrementation: uses integer counters for students and teachers to ensure lookups are easy and unique
- File persistence: uses json serialization to automatically save application state between runs without losing data
- Text badge export: outputs student details directly to plain text card files for front desk use
