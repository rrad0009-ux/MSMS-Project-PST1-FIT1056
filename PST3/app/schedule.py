#---------------------------------------------------------
#------Schedule Manager Controller and Persistance Engine--
#---------------------------------------------------------

#central controller managing business logic, state and JSON data serialisation 

import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # attendance ledger holding checkin dictionaries
        self.attendance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)

                # reconstruct StudentUser object instances from JSON
                self.students = []
                for s_data in data.get("students", []):
                    student = StudentUser(s_data["id"], s_data["name"])
                    student.enrolled_course_ids = s_data.get("enrolled_course_ids", [])
                    self.students.append(student)

                # reconstruct TeacherUser object instances from JSON
                self.teachers = []
                for t_data in data.get("teachers", []):
                    teacher = TeacherUser(t_data["id"], t_data["name"], t_data.get("speciality", ""))
                    self.teachers.append(teacher)

                # reconstruct Course object instances from JSON
                self.courses = []
                for c_data in data.get("courses", []):
                    course = Course(
                        c_data["id"],
                        c_data["name"],
                        c_data["instrument"],
                        c_data.get("teacher_id")
                    )
                    course.enrolled_student_ids = c_data.get("enrolled_student_ids", [])
                    course.lessons = c_data.get("lessons", [])
                    self.courses.append(course)

                # load attendance log using .get() to handle missing keys gracefully
                self.attendance_log = data.get("attendance", [])

                # calculate next ids so new registrations don't overlap
                for s in self.students:
                    if s.id >= self.next_student_id:
                        self.next_student_id = s.id + 1
                for t in self.teachers:
                    if t.id >= self.next_teacher_id:
                        self.next_teacher_id = t.id + 1

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log
        }

        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    #-----------------------------------------
    #-----helper lookup methods---------------
    #-----------------------------------------

#helper functions to grab a student or course using their id

    def find_student_by_id(self, student_id):
        """Looks up and returns student by their integer ID. Returns None if no matches"""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        """Looks up and returns course by their integer ID. Returns None if no matches"""
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def find_teacher_by_id(self, teacher_id):
        """Looks up and returns teacher by their integer ID. Returns None if no matches"""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    #-----------------------------------------
    #---attendance check in Workflow--------
    #-----------------------------------------

#handles checking students into classes and saving to attendance log

    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": timestamp
        }
        
        self.attendance_log.append(check_in_record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    #-----------------------------------------
    #---student management methods------------
    #-----------------------------------------

#functions to add, update, and remove students

    def register_student(self, name):
        """Creates new StudentUser with auto-increment ID and saves it"""
        new_student = StudentUser(self.next_student_id, name)
        self.students.append(new_student)
        self.next_student_id += 1
        self._save_data()
        return new_student

    def update_student(self, student_id, **fields):
        """Updates attributes for a student matching their ID"""
        student = self.find_student_by_id(student_id)
        if student:
            for key, val in fields.items():
                if hasattr(student, key):
                    setattr(student, key, val)
            self._save_data()
            print(f"Student {student_id} updated.")
            return True
        print(f"Error: Student with ID {student_id} not found.")
        return False

    def remove_student(self, student_id):
        """Removes a student and takes them out of enrolled courses"""
        student = self.find_student_by_id(student_id)
        if student:
            self.students.remove(student)
            for course in self.courses:
                if student_id in course.enrolled_student_ids:
                    course.enrolled_student_ids.remove(student_id)
            self._save_data()
            print(f"Student {student_id} removed.")
            return True
        print(f"Error: Student with ID {student_id} not found.")
        return False

    #-----------------------------------------
    #---teacher management methods------------
    #-----------------------------------------

#functions to add, edit, and remove teachers

    def add_teacher(self, name, speciality):
        """Creates a new TeacherUser profile with auto ID and saves it"""
        new_teacher = TeacherUser(self.next_teacher_id, name, speciality)
        self.teachers.append(new_teacher)
        self.next_teacher_id += 1
        self._save_data()
        print(f"Core: Teacher '{name}' added.")
        return new_teacher

    def update_teacher(self, teacher_id, **fields):
        """Updates fields for a teacher matching their ID"""
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher:
            for key, val in fields.items():
                if hasattr(teacher, key):
                    setattr(teacher, key, val)
            self._save_data()
            print(f"Teacher {teacher_id} updated.")
            return True
        print(f"Error: Teacher with ID {teacher_id} not found.")
        return False

    def remove_teacher(self, teacher_id):
        """Removes a teacher record from the school"""
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher:
            self.teachers.remove(teacher)
            self._save_data()
            print(f"Teacher {teacher_id} removed.")
            return True
        print(f"Error: Teacher with ID {teacher_id} not found.")
        return False