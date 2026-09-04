**Music School Management System : Object Oriented Application**

Application built for student registration, course scheduling, teacher management, roster lookups, attendance check ins, student badge generation, and persistent json file storage. 
This was developed for FIT1056 (PST3)

**What the system does**
The system is an upgraded digital management application for front desk receptionists and school administrators. It refactors the earlier procedural code into a proper object oriented model view controller setup, keeping data safely stored across sessions in a central json file.
Its functions include:

* Student registration: registers student profiles with automatic id assignment and tracks enrolled course ids
* Course enrolment and switching: enrols students into courses or swaps them between courses while updating student and course rosters
* Daily roster viewing: filters scheduled lessons by weekday and displays times, room allocations, and instruments
* Search and directory lookup: case insensitive keyword search across student and teacher records
* Full administrative crud operations: lets admins add, update, and delete both student and teacher profiles
* Attendance tracking: records student check ins with automatic iso timestamps into a persistent attendance log
* Student id card printing: writes a formatted id badge text file directly to the folder for quick physical printing
* Crash prevention: guards numerical id prompts using try except blocks so invalid inputs do not terminate the program
* Central persistence: uses a schedule manager controller to load and dump state directly to msms.json whenever data changes

**Differences from PST2 and Architectural Decisions**

* How it differs from PST2
PST2 relied on raw dictionaries stored in a global app_data dictionary and ran mostly procedural functions. In PST3, all entities are upgraded into true object oriented classes. StudentUser and TeacherUser now inherit shared identity attributes directly from a base User parent class using super().__init__(). We also introduced a dedicated Course class to keep track of lesson schedules and enrolled student ids separately. Instead of saving loose dictionaries directly, a central ScheduleManager controller handles all the business logic, lookup helpers, and json file serialization.

* Why the sub menu design was chosen
In PST2, the main menu displayed a flat list of 10 options, which felt crowded and cluttered for the user. For PST3, the interface was reorganized into categorized sub menus (Student Management, Teacher Management, Course Enrolments and Rosters, and Reception and Attendance). This keeps the home screen clean with just 4 main categories, groups related workflows together so front desk staff do not have to scan past administrative options, and makes the terminal navigation feel much easier to use.

**Major parts and functions**

*Entity models (app folder)*
* User (user.py): base class defining core user id and name properties
* StudentUser (student.py): inherits from User, sets up an enrolled course ids list
* TeacherUser (teacher.py): inherits from User, stores teacher speciality
* Course (teacher.py): stores course details, assigned teacher id, student list, and lesson timetable

*Controller and persistence engine (app/schedule.py)*
* ScheduleManager: main controller class managing system state and persistence
* _load_data(): parses msms.json and reconstructs real class instances for students, teachers, and courses
* _save_data(): converts object instance properties using __dict__ and writes clean formatted json to disk
* find_student_by_id(student_id): searches student objects and returns match or None
* find_teacher_by_id(teacher_id): searches teacher objects and returns match or None
* find_course_by_id(course_id): searches course objects and returns match or None
* register_student(name): creates new StudentUser with auto incremented id and saves
* update_student(student_id, **fields): dynamically updates valid attributes on a student object
* remove_student(student_id): deletes student and removes their id from enrolled courses
* add_teacher(name, speciality): creates new TeacherUser with auto incremented id and saves
* update_teacher(teacher_id, **fields): dynamically updates valid attributes on a teacher object
* remove_teacher(teacher_id): removes teacher record from the school
* check_in(student_id, course_id): validates student and course existence, saves timestamp to log

*View layer and sub menus (main.py)*
* front_desk_daily_roster(manager, day): prints pretty table of classes happening on a chosen weekday
* switch_course(manager, student_id, from_course_id, to_course_id): moves student between courses
* print_student_card(manager, student_id): writes formatted badge card to text file
* front_desk_lookup(manager, term): runs case insensitive search on students and teachers
* student_management_menu(manager): sub menu handling student registration, edits, removals, and listings
* teacher_management_menu(manager): sub menu handling teacher additions, edits, removals, and listings
* enrolment_and_roster_menu(manager): sub menu handling daily rosters, swaps, and enrolments
* reception_attendance_menu(manager): sub menu handling student check ins, badge exports, and search
* main(): top level loop showing 4 categories and routing commands to sub menus

**How to run the program**

*Prerequisites*
Python 3.8 or above installed
Terminal or command line access

*Execution*
Open your terminal, make sure you are in the PST3 project directory, and launch the view layer:

python main.py

**Testing out the program**

*Test 1: Student registration*
* Chose menu option 1, then option 1 for registration
* Input name: rahul
* Expected output: confirmation that student rahul was registered with an assigned id

*Test 2: Daily roster display*
* Chose menu option 3, then option 1 for roster
* Input day: monday
* Expected output: displays lesson schedule for Beginner Piano with time and room info

*Test 3: Course switching*
* Chose menu option 3, then option 2 to switch course
* Input student id 1, old course 101, new course 102
* Expected output: confirms student moved between courses and updates course lists

*Test 4: Student check in*
* Chose menu option 4, then option 1 for check in
* Input student id 1, course id 101
* Expected output: success message and timestamp written to attendance log in msms.json

*Test 5: Student card badge export*
* Chose menu option 4, then option 2 to print card
* Input student id: 1
* Expected output: prints card confirmation and creates 1_card.txt in the folder

*Test 6: Teacher update*
* Chose menu option 2, then option 2 to update teacher
* Input teacher id 1, enter new speciality Keyboard
* Expected output: confirms teacher updated and changes saved to file

*Test 7: Input guardrail validation*
* Chose menu option 1, then option 2
* Enter invalid input abc when asked for id
* Expected output: error message prompting for a numerical id without crashing the program

**Assumptions and Design Choices**

* Design choices
* Object oriented structure: used inheritance with User as a parent class to reuse code cleanly across student and teacher models
* Model view controller pattern: kept main.py focused only on inputs and printing, leaving data validation, updates, and json file storage to ScheduleManager
* Dynamic updates: used hasattr and setattr inside update methods so user fields can be edited dynamically without tons of hardcoded if statements
* Categorized sub menus: grouped 12+ operations into 4 logical sub menus to prevent long confusing terminal menus
* File persistence: automatic json loading and saving on every state change so data stays saved between terminal runs
