# Music School Management System: Object Oriented and Graphical User Interface Application

Application built for student registration, course scheduling, teacher management, roster lookups, attendance check ins, student badge generation, interactive Streamlit GUI dashboards, and persistent json file storage. This was originally developed for FIT1056 PST3 and upgraded for PST4.

## What the system does

The system is an upgraded digital management application for front desk receptionists and school administrators. It refactors the earlier procedural code into a proper object oriented model view controller setup, keeping data safely stored across sessions in a central json file and providing a visual web dashboard via Streamlit.

* Student registration: registers student profiles with automatic id assignment and tracks enrolled course ids.
* Course enrolment and switching: enrols students into courses or swaps them between courses while updating student and course rosters.
* Daily roster viewing: filters scheduled lessons by weekday and displays times, room allocations, and instruments.
* Search and directory lookup: case insensitive keyword search across student and teacher records.
* Full administrative crud operations: lets admins add, update, and delete both student and teacher profiles.
* Attendance tracking: records student check ins with automatic iso timestamps into a persistent attendance log.
* Student id card printing: writes a formatted id badge text file directly to the folder for quick physical printing.
* Crash prevention: guards numerical id prompts using try except blocks so invalid inputs do not terminate the program.
* Central persistence: uses a schedule manager controller to load and dump state directly to msms json whenever data changes.
* Interactive GUI dashboard: presents an intuitive web interface built with Streamlit for managing students, teachers, and rosters.


## Major Parts and Functions

### Entity models (app folder)
* User: base class defining core user id and name properties.
* StudentUser: inherits from User, sets up an enrolled course ids list.
* TeacherUser: inherits from User, stores teacher speciality.
* Course: stores course details, assigned teacher id, student list, and lesson timetable.

### Controller and persistence engine
* ScheduleManager: main controller class managing system state and persistence.
* load data: parses msms json and reconstructs real class instances for students, teachers, and courses.
* save data: converts object instance properties using dict and writes clean formatted json to disk.
* find student by id: searches student objects and returns match or None.
* find teacher by id: searches teacher objects and returns match or None.
* find course by id: searches course objects and returns match or None.
* register student: creates new StudentUser with auto incremented id and saves.
* update student: updates valid attributes on a student object.
* remove student: deletes student and removes their id from enrolled courses.
* add teacher: creates new TeacherUser with auto incremented id and saves.
* update teacher: updates valid attributes on a teacher object.
* remove teacher: removes teacher record from the school.
* check in: validates student and course existence, saves timestamp to log.

### GUI view layer
* launch: configures top level window settings, handles sidebar routing, and maintains ScheduleManager in session state.
* show student management page: renders student search, directory listing, registration form, course enrolments, swaps, edits, and badge printing.
* show teacher management page: renders teacher addition form, directory, record updates, and removal options.
* show roster page: renders daily schedule filtering by day and handles interactive student check ins.
* main py: entry point that imports launch and starts the Streamlit dashboard app.
## How to Run the Program

* Prerequisites: Python 3.8 or above installed, Streamlit package installed via pip, and terminal access.
* Execution: Open your terminal, make sure you are in the PST4 project directory, and launch the Streamlit view layer using `streamlit run main.py`.


## Testing Out the Program

* Test 1 Student registration: Selected Student Management page, clicked Directory and Search tab. Input New Student Name as rahul, First Instrument as Guitar, and clicked Register Student. Expected output is a success banner confirming student rahul was registered with an assigned id.
* Test 2 Daily roster display: Selected Daily Roster page and chose Monday. Expected output displays data table schedule for Beginner Piano with time and room info.
* Test 3 Course switching: Selected Student Management page, clicked Enrol and Switch Courses tab. Selected student 1, current course 101, target course 102, and clicked Switch Course. Expected output shows success message confirming student moved between courses and updates saved.
* Test 4 Student check in: Selected Daily Roster page, selected student 1 and course 101 under Student Check in, and clicked Check in Student. Expected output displays success message and timestamp written to attendance log in msms json.
* Test 5 Student card badge export: Selected Student Management page, clicked Print ID Badge tab, selected student 1, and clicked Generate ID Badge File. Expected output confirms creation of the badge text file in the folder.
* Test 6 Teacher update: Selected Teacher Management page, clicked Update Teacher tab, selected teacher 1, entered new speciality as Keyboard, and clicked Update Teacher. Expected output confirms teacher updated and changes saved to msms json.
* Test 7 Input guardrail validation: Selected Student Management page, clicked Directory and Search tab, left student name blank, and submitted form. Expected output displays warning prompt asking for valid inputs without crashing the application.


## Assumptions and Design Choices

* Object oriented structure: used inheritance with User as a parent class to reuse code cleanly across student and teacher models.
* Model view controller pattern: kept entry points and GUI files focused only on visual rendering and inputs, delegating data validation, updates, and json file storage to ScheduleManager.
* Streamlit session state: initialized ScheduleManager once in session state so in memory records and JSON changes persist across page menu navigation.
* Categorized tabbed interfaces: organized multi feature administration into Streamlit tabs to prevent screen clutter and keep front desk workflows simple.
* File persistence: automatic json loading and saving on state changes so data stays saved between application runs.