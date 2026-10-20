# app/schedule.py
import json
import csv
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    def __init__(self, data_file="data/msms.json"):
        self.data_file = data_file
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        # PST5: Add self.finance_log list
        self.finance_log = []
        self._load_data()

    def _load_data(self):
        """Loads data from JSON file into memory."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
                # Reconstruct students, teachers, and courses
                self.students = [StudentUser(**s) for s in data.get("students", [])]
                self.teachers = [TeacherUser(**t) for t in data.get("teachers", [])]
                self.courses = [Course(**c) for c in data.get("courses", [])]
                self.attendance_log = data.get("attendance_log", [])
                # PST5: Load finance_log
                self.finance_log = data.get("finance_log", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
            self.students = []
            self.teachers = []
            self.courses = []
            self.attendance_log = []
            self.finance_log = []

    def _save_data(self):
        """Saves current state to JSON file."""
        data = {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses": [c.to_dict() for c in self.courses],
            "attendance_log": self.attendance_log,
            "finance_log": self.finance_log
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    # --- Fragment 5.1 Finance & Reporting Methods ---

    def record_payment(self, student_id, amount, method):
        """Records a payment entry into finance_log and saves data."""
        student = self.find_student_by_id(student_id)
        if not student:
            print(f"Error: Student ID {student_id} not found.")
            return None

        payment_record = {
            "student_id": student_id,
            "amount": float(amount),
            "method": method,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.finance_log.append(payment_record)
        self._save_data()
        print(f"Payment of ${amount:.2f} recorded for student ID {student_id}.")
        return payment_record

    def get_payment_history(self, student_id):
        """Returns a list of all payment records for a specific student."""
        return [p for p in self.finance_log if p.get('student_id') == student_id]

    def export_report(self, kind, out_path):
        """Exports finance or attendance logs to a CSV file."""
        print(f"Exporting {kind} report to {out_path}...")
        
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]
        else:
            print(f"Error: Unknown report type '{kind}'.")
            return False

        try:
            with open(out_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data_to_export)
            print(f"Successfully exported {kind} report to {out_path}.")
            return True
        except Exception as e:
            print(f"Error writing CSV report: {e}")
            return False

    # --- Helper Search Methods ---

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
        return None
    