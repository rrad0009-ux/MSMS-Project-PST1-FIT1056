# app/teacher.py
"""TeacherUser and Course models for the Music School Management System."""

from app.user import User

class TeacherUser(User):
    """Represents a teacher inheriting from User."""
    def __init__(self, user_id=None, name="", speciality="", id=None):
        super().__init__(user_id=user_id, name=name, id=id)
        self.speciality = speciality

    def to_dict(self):
        """Serializes TeacherUser to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "speciality": self.speciality
        }


class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id=None, name="", instrument="", teacher_id=None, enrolled_student_ids=None, lessons=None, id=None):
        self.id = course_id if course_id is not None else id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_student_ids = enrolled_student_ids if enrolled_student_ids is not None else []
        self.lessons = lessons if lessons is not None else []

    def to_dict(self):
        """Serializes Course to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "teacher_id": self.teacher_id,
            "enrolled_student_ids": self.enrolled_student_ids,
            "lessons": self.lessons
        }
    