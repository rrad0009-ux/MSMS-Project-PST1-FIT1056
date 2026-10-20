**Music School Management System : Quality Assurance and Full Integration**

Application designed for student registration, instrument course enrolments, administrative data reporting, student and teacher lookup features, full CRUD data updates, attendance check-ins, physical ID card generation, graphical user interface (GUI), automated unit testing with pytest, system activity logging, automated JSON data backups, and financial payment processing. 
This was developed for FIT1056: Introduction to Software Engineering (PST5)

**What the system does**
The system is a fully upgraded digital management application for front desk receptionists and administrators of the school. It expands on the Streamlit graphical interface from PST4 by adding administrative quality assurance utilities (session logging, data backups) and a complete financial tracking engine to record payments and export transaction ledgers.
Its functions include: 

* Student registration: registers student and gives unique student id via sequential integers and enrols them in the course through the choice of instrument
* Course enrolment: enrols existing students to other/additional instrument courses using their student id
* Prevention of duplicate enrolments: checks existing enrolments to prevent enrolling a student in the same instrument course more than once
* Student/Teacher Lookup: uses keywords to look up student names, teacher names, and teacher speciality (case-insensitive)
* Administrative CRUD Operations: allows adding new teachers, updating student/teacher records dynamically via keyword arguments, and removing records safely
* Receptionist Check-in: records student attendance timestamps for courses and logs them to an attendance ledger
* Physical ID Badge Printing: exports formatted plain text student cards to local `.txt` files
* Interactive Streamlit GUI: provides a multi-page web dashboard with sidebar navigation for Student Management, Teacher Management, Daily Roster, and Payments
* Automated Data Backups: automatically creates timestamped JSON backups in `data/backups/` upon application startup
* System Session Logging: logs key business events (registrations, payments, cancellations) to `msms.log`
* Financial Payment Processing: records payments by student id with payment method tracking, displays transaction history, and exports financial CSV reports
* Automated Unit Testing: includes a pytest suite (`tests/test_schedule_manager.py`) to verify core backend business logic and financial reporting
* Catches non numeric id's without crashing the system using 'try-except'

**Major parts and functions**

*File persistence and data storage*
Uses a central controller class `ScheduleManager` containing lists for `students`, `teachers`, `courses`, `attendance_log`, and `finance_log`.
* _load_data(): reads data from `msms.json` into object instances. If file is not found, initializes a default starting structure
* _save_data(): serialises objects and writes state to `msms.json` with clean formatting

*Student and teacher management services*
* find_student_by_id(student_id): searches through student records to locate student object by id, returns None if not found
* register_student(name): registers new student using auto-incremented id and appends to student records
* add_teacher(name, speciality): creates teacher object with auto-incremented id and appends to teacher records
* update_teacher(teacher_id, **fields) and update_student(student_id, **fields): locates record by id and updates given fields
* remove_teacher(teacher_id) and remove_student(student_id): removes matching record from system lists

*Front desk, roster, and receptionist features*
* check_in(student_id, course_id, timestamp): logs student attendance with current iso timestamp string into `attendance_log`
* print_student_card(student_id): generates and saves a formatted text file (`<id>_card.txt`) containing student details and enrolled instruments
* front_desk_daily_roster(day): retrieves courses and enrolled students scheduled for a specific day

*Administrative and quality assurance utilities*
* init_logger(log_file): configures Python's logging module to record operational events in `msms.log`
* backup_data(data_path, backup_dir): copies `msms.json` to `data/backups/` with a timestamped filename on startup

*Financial engine and reporting*
* record_payment(student_id, amount, method): records a student financial transaction and logs it to `finance_log`
* get_payment_history(student_id): retrieves all payment transaction records for a given student id
* export_report(kind, out_path): exports attendance or financial transaction history to a CSV report file

*Graphical user interface and routing*
* main_dashboard.py: manages Streamlit session state, sidebar navigation, and routes across student, teacher, roster, and finance pages
* finance_pages.py: provides Streamlit forms to record payments, view student payment history tables, and trigger CSV report exports

**How to run the program**

*Prerequisites*
Python 3.10 Installed
Streamlit installed (`pip install streamlit pandas`)
Pytest installed (`pip install pytest`)
Terminal access

*Execution*
Navigate to project folder through terminal by opening it. Run application launcher as shown below

cd msms-project/PST5
streamlit run main.py

Now test out the program by interacting with the graphical interface in your browser

*Running automated tests*
Run the pytest test suite from the PST5 directory:

python -m pytest

**Testing out the program**

*Test 1: Registration of new Student*
* Open Student Management page in GUI
* Input name: rahul
* Expected output: confirmation that student rahul was registered with an assigned student id and saved to database

*Test 2: Record Financial Payment*
* Open Payments page in GUI
* Input student id: 1
* Input payment amount: 150.0
* Select payment method: Credit Card
* Expected output: confirmation message that payment was recorded, history table updated, and changes saved

*Test 3: Generate Financial CSV Report*
* Open Payments page in GUI
* Click "Export Financial Report (CSV)" button
* Expected output: "Report exported to data/finance_report.csv" and file created on disk

*Test 4: Check Automated Data Backups*
* Launch `streamlit run main.py`
* Expected output: timestamped backup file generated inside `data/backups/` (e.g., `msms_backup_YYYYMMDD_HHMMSS.json`)

*Test 5: Run Pytest Unit Tests*
* Execute `python -m pytest` in terminal
* Expected output: `3 passed in 0.14s` confirming all unit tests in `tests/test_schedule_manager.py` passed

**Assumptions, Design Choices, Extensions**

*Design Choices*
* Streamlit session state persistence: initialized `ScheduleManager` in `st.session_state` so in-memory records and JSON changes persist across menu navigation
* Model view controller pattern: kept GUI files in `gui/` focused strictly on rendering and input, delegating data logic and file saves to `ScheduleManager`
* Isolated test fixtures: pytest uses temporary directory fixtures (`tmp_path`) to run unit tests in isolation without altering live production data in `msms.json`
* Automated lifecycle backups: automated data backup runs on startup to safeguard database state before new session modifications take place
