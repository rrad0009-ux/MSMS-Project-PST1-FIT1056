# Music School Management System: Object Oriented, Quality Assurance, and Graphical User Interface Application

Application built for student registration, course scheduling, teacher management, roster lookups, attendance check ins, student badge generation, financial tracking, payment recording, CSV report exports, automated logging, timestamped data backups, interactive Streamlit GUI dashboards, automated pytest test suites, and persistent json file storage. This was originally developed for FIT1056 PST3, upgraded for PST4, and fully expanded for PST5.

## What the system does

The system is an upgraded digital management application for front desk receptionists and school administrators. It refactors the earlier procedural code into a proper object oriented model view controller setup, keeping data safely stored across sessions in a central json file, providing administrative logging and backup guardrails, verifying backend reliability through automated unit testing, and presenting a visual web dashboard via Streamlit.

* Student registration: registers student profiles with automatic id assignment and tracks enrolled course ids.
* Course enrolment and switching: enrols students into courses or swaps them between courses while updating student and course rosters.
* Daily roster viewing: filters scheduled lessons by weekday and displays times, room allocations, and instruments.
* Search and directory lookup: case insensitive keyword search across student and teacher records.
* Full administrative crud operations: lets admins add, update, and delete both student and teacher profiles.
* Attendance tracking: records student check ins with automatic iso timestamps into a persistent attendance log.
* Financial ledger management: records student payments with payment method tracking and retrieves historical payment logs per student.
* CSV report exports: exports financial transaction ledgers and attendance logs directly to structured csv files for administrative auditing.
* Application logging and backups: initializes session activity logging to a system log file and creates timestamped JSON data backups prior to GUI launch.
* Automated unit testing: validates core backend schedule manager logic, payment processing, and reporting using a pytest suite with isolated fixtures.
* Student id card printing: writes a formatted id badge text file directly to the folder for quick physical printing.
* Crash prevention: guards numerical id prompts using try except blocks so invalid inputs do not terminate the program.
* Central persistence: uses a schedule manager controller to load and dump state directly to msms json whenever data changes.
* Interactive GUI dashboard: presents an intuitive web interface built with Streamlit for managing students, teachers, rosters, and financial operations.


## Major Parts and Functions

### Entity models (app folder)
* User: base class defining core user id and name properties.
* StudentUser: inherits from User, sets up an enrolled course ids list.
* TeacherUser: inherits from User, stores teacher speciality.
* Course: stores course details, assigned teacher id, student list, and lesson timetable.

### Controller and persistence engine (app/schedule.py)
* ScheduleManager: main controller class managing system state, financial ledgers, and persistence.
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
* record payment: validates student id, records amount, method, and timestamp to finance log, and logs business event.
* get payment history: filters and returns all financial transaction records for a given student id.
* export report: writes attendance or financial transaction ledgers to designated csv file paths with dictionary headers.

### Quality assurance and administrative utilities (app/admin_utils.py)
* init logger: sets up system activity logging with formatted timestamps and log levels.
* backup data: generates a timestamped copy of the primary json database file in a dedicated backups directory.

### GUI view layer (gui folder and main.py)
* launch: configures top level window settings, handles sidebar routing, and maintains ScheduleManager in session state.
* show student management page: renders student search, directory listing, registration form, course enrolments, swaps, edits, and badge printing.
* show teacher management page: renders teacher addition form, directory, record updates, and removal options.
* show roster page: renders daily schedule filtering by day and handles interactive student check ins.
* show finance page: renders interactive payment forms, displays student transaction history tables, and triggers csv report exports.
* main py: application lifecycle entry point that initializes logging, triggers an automated startup backup, and launches the Streamlit dashboard.

### Automated testing suite (tests folder)
* test schedule manager py: pytest suite utilizing a fresh manager fixture backed by temporary file paths to independently verify student registration, payment logging, history retrieval, and csv exports.


## How to Run the Program

* Prerequisites: Python 3.8 or above installed, Streamlit and pytest packages installed via pip, and terminal access.
* Execution: Open your terminal, make sure you are in the PST5 project directory, and launch the Streamlit view layer using `streamlit run main.py`.
* Running Tests: Execute automated quality assurance tests in the PST5 directory using `python -m pytest`.


## Testing Out the Program

* Test 1 Student registration: Selected Student Management page, clicked Directory and Search tab. Input New Student Name as rahul, First Instrument as Guitar, and clicked Register Student. Expected output is a success banner confirming student rahul was registered with an assigned id.
* Test 2 Daily roster display: Selected Daily Roster page and chose Monday. Expected output displays data table schedule for Beginner Piano with time and room info.
* Test 3 Course switching: Selected Student Management page, clicked Enrol and Switch Courses tab. Selected student 1, current course 101, target course 102, and clicked Switch Course. Expected output shows success message confirming student moved between courses and updates saved.
* Test 4 Student check in: Selected Daily Roster page, selected student 1 and course 101 under Student Check in, and clicked Check in Student. Expected output displays success message and timestamp written to attendance log in msms json.
* Test 5 Record student payment: Selected Payments page, chose student 1, entered amount 150, selected Credit Card, and clicked Record Payment. Expected output displays success banner and appends payment entry to finance log.
* Test 6 Export financial report: Selected Payments page and clicked Export Finance Report CSV button. Expected output displays confirmation message that data was saved to CSV and creates finance_report.csv in data folder.
* Test 7 Automated unit test suite: Executed python -m pytest in terminal. Expected output confirms 3 passed tests verifying student registration, payment tracking, and report exports.
* Test 8 Input guardrail validation: Selected Student Management page, clicked Directory and Search tab, left student name blank, and submitted form. Expected output displays warning prompt asking for valid inputs without crashing the application.


## Assumptions and Design Choices

* Object oriented structure: used inheritance with User as a parent class to reuse code cleanly across student and teacher models.
* Model view controller pattern: kept entry points and GUI files focused only on visual rendering and inputs, delegating data validation, updates, and json file storage to ScheduleManager.
* Streamlit session state: initialized ScheduleManager once in session state so in memory records and JSON changes persist across page menu navigation.
* Lifecycle startup hooks: placed logging initialization and backup routines at the very start of main py so data safety and session tracking occur prior to GUI interaction.
* Isolated unit testing: designed a pytest fixture utilizing temporary directory paths to test backend methods independently without altering actual production JSON data.
* Categorized tabbed interfaces: organized multi feature administration into Streamlit tabs to prevent screen clutter and keep front desk workflows simple.
* File persistence: automatic json loading and saving on state changes so data stays saved between application runs.
