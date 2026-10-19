# app/schedule.py
import json
import csv
import datetime
import logging
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    def __init__(self, data_file="data/msms.json"):
        self.data_file = data_file
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.finance_log = []
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON persistence file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.students = [StudentUser(**s) for s in data.get("students", [])]
                self.teachers = [TeacherUser(**t) for t in data.get("teachers", [])]
                self.courses = [Course(**c) for c in data.get("courses", [])]
                self.attendance_log = data.get("attendance_log", [])
                self.finance_log = data.get("finance_log", [])
        except (FileNotFoundError, json.JSONDecodeError):
            logging.info("Data file not found or empty. Initializing clean state.")
            self.students = []
            self.teachers = []
            self.courses = []
            self.attendance_log = []
            self.finance_log = []

    def _save_data(self):
        """Saves active state to JSON file."""
        data = {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses": [c.to_dict() for c in self.courses],
            "attendance_log": self.attendance_log,
            "finance_log": self.finance_log
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # --- PST5 Business Methods ---

    def register_student(self, name):
        """Registers a new student and logs the event."""
        student_id = len(self.students) + 1
        new_student = StudentUser(student_id, name)
        self.students.append(new_student)
        self._save_data()
        logging.info(f"Registered new student '{name}' with Assigned ID {student_id}.")
        return new_student

    def record_payment(self, student_id, amount, method):
        """Records a payment entry and logs the transaction."""
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
        """Exports logs to a CSV report."""
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]
        else:
            return False

        try:
            with open(out_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data_to_export)
            return True
        except Exception as e:
            logging.error(f"Failed to export report: {e}")
            return False

    def find_student_by_id(self, student_id):
        for s in self.students:
            if s.id == student_id:
                return s
        return None
    