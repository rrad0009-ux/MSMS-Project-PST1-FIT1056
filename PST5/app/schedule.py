# app/schedule.py
#---------------------------------------------------------
#------Schedule Manager Controller and Persistence Engine--
#---------------------------------------------------------

# central controller managing business logic, state, and JSON data serialization

import json
import csv
import datetime
import logging
from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_file="data/msms.json", data_path=None):
        # Support both data_file and data_path for backward compatibility
        self.data_file = data_path if data_path is not None else data_file
        self.data_path = self.data_file
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.finance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates object lists."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Reconstruct StudentUser object instances from JSON
                self.students = []
                for s in data.get("students", []):
                    s_id = s.get("id", s.get("user_id"))
                    student = StudentUser(user_id=s_id, name=s.get("name", ""))
                    student.enrolled_course_ids = s.get("enrolled_course_ids", [])
                    self.students.append(student)

                # Reconstruct TeacherUser object instances from JSON
                self.teachers = []
                for t in data.get("teachers", []):
                    t_id = t.get("id", t.get("user_id"))
                    teacher = TeacherUser(user_id=t_id, name=t.get("name", ""), speciality=t.get("speciality", ""))
                    self.teachers.append(teacher)

                # Reconstruct Course object instances from JSON
                self.courses = []
                for c in data.get("courses", []):
                    c_id = c.get("id", c.get("course_id"))
                    course = Course(
                        course_id=c_id,
                        name=c.get("name", ""),
                        instrument=c.get("instrument", ""),
                        teacher_id=c.get("teacher_id")
                    )
                    course.enrolled_student_ids = c.get("enrolled_student_ids", [])
                    course.lessons = c.get("lessons", [])
                    self.courses.append(course)

                # Load logs using .get() to handle missing keys gracefully
                self.attendance_log = data.get("attendance_log", data.get("attendance", []))
                self.finance_log = data.get("finance_log", [])

                # Calculate next IDs so new registrations do not overlap
                for s in self.students:
                    if s.id and s.id >= self.next_student_id:
                        self.next_student_id = s.id + 1
                for t in self.teachers:
                    if t.id and t.id >= self.next_teacher_id:
                        self.next_teacher_id = t.id + 1

        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("Data file not found or empty. Initializing clean state.")
            self.students = []
            self.teachers = []
            self.courses = []
            self.attendance_log = []
            self.finance_log = []

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.to_dict() if hasattr(s, 'to_dict') else s.__dict__ for s in self.students],
            "teachers": [t.to_dict() if hasattr(t, 'to_dict') else t.__dict__ for t in self.teachers],
            "courses": [c.to_dict() if hasattr(c, 'to_dict') else c.__dict__ for c in self.courses],
            "attendance_log": self.attendance_log,
            "finance_log": self.finance_log
        }

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)

    #-----------------------------------------
    #-----Helper Lookup Methods---------------
    #-----------------------------------------

    def find_student_by_id(self, student_id):
        """Looks up and returns student by their integer ID. Returns None if no matches."""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        """Looks up and returns course by their integer ID. Returns None if no matches."""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def find_teacher_by_id(self, teacher_id):
        """Looks up and returns teacher by their integer ID. Returns None if no matches."""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    #-----------------------------------------
    #---Attendance Check-in Workflow----------
    #-----------------------------------------

    def check_in(self, student_id, course_id, timestamp=None):
        """Records a student's attendance for a course after validation."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            logging.warning(f"Check-in failed: Invalid Student ID {student_id} or Course ID {course_id}.")
            return False

        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()

        check_in_record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": timestamp
        }

        self.attendance_log.append(check_in_record)
        self._save_data()
        logging.info(f"Student '{student.name}' (ID: {student_id}) checked into course '{course.name}' (ID: {course_id}).")
        return True

    #-----------------------------------------
    #---Student Management Methods------------
    #-----------------------------------------

    def register_student(self, name):
        """Creates new StudentUser with auto-increment ID and saves it."""
        new_student = StudentUser(user_id=self.next_student_id, name=name)
        self.students.append(new_student)
        self.next_student_id += 1
        self._save_data()
        logging.info(f"Registered new student '{name}' with Assigned ID {new_student.id}.")
        return new_student

    def enrol_student(self, student_id, course_id):
        """Enrols a student in a course and updates both student and course lists."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        if student and course:
            if course_id not in student.enrolled_course_ids:
                student.enrolled_course_ids.append(course_id)
            if student_id not in course.enrolled_student_ids:
                course.enrolled_student_ids.append(student_id)
            self._save_data()
            logging.info(f"Enrolled student ID {student_id} into course ID {course_id}.")
            return True
        return False

    def switch_course(self, student_id, from_course_id, to_course_id):
        """Switches a student from one course to another."""
        student = self.find_student_by_id(student_id)
        old_course = self.find_course_by_id(from_course_id)
        new_course = self.find_course_by_id(to_course_id)

        if not student or not old_course or not new_course:
            return False

        if from_course_id in student.enrolled_course_ids:
            student.enrolled_course_ids.remove(from_course_id)
        if student_id in old_course.enrolled_student_ids:
            old_course.enrolled_student_ids.remove(student_id)

        if to_course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(to_course_id)
        if student_id not in new_course.enrolled_student_ids:
            new_course.enrolled_student_ids.append(student_id)

        self._save_data()
        logging.info(f"Switched student ID {student_id} from course ID {from_course_id} to {to_course_id}.")
        return True

    def update_student(self, student_id, **fields):
        """Updates attributes for a student matching their ID."""
        student = self.find_student_by_id(student_id)
        if student:
            for key, val in fields.items():
                if hasattr(student, key):
                    setattr(student, key, val)
            self._save_data()
            logging.info(f"Updated student ID {student_id}.")
            return True
        logging.warning(f"Update student failed: Student ID {student_id} not found.")
        return False

    def remove_student(self, student_id):
        """Removes a student and takes them out of enrolled courses."""
        student = self.find_student_by_id(student_id)
        if student:
            self.students.remove(student)
            for course in self.courses:
                if student_id in course.enrolled_student_ids:
                    course.enrolled_student_ids.remove(student_id)
            self._save_data()
            logging.info(f"Removed student ID {student_id}.")
            return True
        logging.warning(f"Remove student failed: Student ID {student_id} not found.")
        return False

    #-----------------------------------------
    #---Teacher Management Methods------------
    #-----------------------------------------

    def add_teacher(self, name, speciality):
        """Creates a new TeacherUser profile with auto ID and saves it."""
        new_teacher = TeacherUser(user_id=self.next_teacher_id, name=name, speciality=speciality)
        self.teachers.append(new_teacher)
        self.next_teacher_id += 1
        self._save_data()
        logging.info(f"Added teacher '{name}' with Speciality '{speciality}'.")
        return new_teacher

    def update_teacher(self, teacher_id, **fields):
        """Updates fields for a teacher matching their ID."""
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher:
            for key, val in fields.items():
                if hasattr(teacher, key):
                    setattr(teacher, key, val)
            self._save_data()
            logging.info(f"Updated teacher ID {teacher_id}.")
            return True
        logging.warning(f"Update teacher failed: Teacher ID {teacher_id} not found.")
        return False

    def remove_teacher(self, teacher_id):
        """Removes a teacher record from the school."""
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher:
            self.teachers.remove(teacher)
            self._save_data()
            logging.info(f"Removed teacher ID {teacher_id}.")
            return True
        logging.warning(f"Remove teacher failed: Teacher ID {teacher_id} not found.")
        return False

    #-----------------------------------------
    #---Finance & Reporting Methods-----------
    #-----------------------------------------

    def record_payment(self, student_id, amount, method):
        """Records a payment entry into finance_log and saves data."""
        student = self.find_student_by_id(student_id)
        if not student:
            logging.warning(f"Payment failed: Student ID {student_id} not found.")
            return None

        payment_record = {
            "student_id": student_id,
            "amount": float(amount),
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.finance_log.append(payment_record)
        self._save_data()
        logging.info(f"Payment of ${amount:.2f} recorded for Student ID {student_id} via {method}.")
        return payment_record

    def get_payment_history(self, student_id):
        """Returns payment history list for a student."""
        return [p for p in self.finance_log if p.get("student_id") == student_id]

    def export_report(self, kind, out_path):
        """Exports finance or attendance logs to a CSV file."""
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]
        else:
            logging.warning(f"Export failed: Unknown report kind '{kind}'.")
            return False

        try:
            with open(out_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data_to_export)
            logging.info(f"Successfully exported {kind} report to {out_path}.")
            return True
        except Exception as e:
            logging.error(f"Failed to export CSV report: {e}")
            return False

    #-----------------------------------------
    #---Reception & Badge Utility Methods----
    #-----------------------------------------

    def print_student_card(self, student_id):
        """Generates a text ID badge file for a student."""
        student = self.find_student_by_id(student_id)
        if student:
            filename = f"{student_id}_card.txt"
            course_names = []
            for cid in student.enrolled_course_ids:
                c = self.find_course_by_id(cid)
                if c:
                    course_names.append(c.name)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("========================\n")
                f.write("  MUSIC SCHOOL ID BADGE\n")
                f.write("========================\n")
                f.write(f"ID: {student.id}\n")
                f.write(f"Name: {student.name}\n")
                f.write(f"Enrolled In: {', '.join(course_names) if course_names else 'None'}\n")
            logging.info(f"Generated student ID badge file '{filename}'.")
            return filename
        logging.warning(f"Badge generation failed: Student ID {student_id} not found.")
        return None
    