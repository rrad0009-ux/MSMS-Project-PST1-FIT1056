# app/schedule.py
import json
import csv
import datetime
import logging  # Import logging module
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    # ... __init__, _load_data, _save_data ...

    def register_student(self, name):
        """Registers a new student and logs the event."""
        student_id = len(self.students) + 1
        new_student = StudentUser(student_id, name)
        self.students.append(new_student)
        self._save_data()
        
        # PST5: Log business event
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
        
        # PST5: Log financial transaction
        logging.info(f"Payment of ${amount:.2f} recorded for Student ID {student_id} via {method}.")
        return payment_record

    def cancel_lesson(self, lesson_id, reason="Unspecified"):
        """Cancels a scheduled lesson and logs a warning."""
        # PST5: Log business warning event
        logging.warning(f"Lesson ID {lesson_id} was cancelled. Reason: {reason}")
        self._save_data()
        