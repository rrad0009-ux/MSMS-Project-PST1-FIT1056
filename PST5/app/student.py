# app/student.py
"""StudentUser model inheriting from the base User class."""

from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id=None, name="", enrolled_course_ids=None, id=None):
        super().__init__(user_id=user_id, name=name, id=id)
        self.enrolled_course_ids = enrolled_course_ids if enrolled_course_ids is not None else []

    def to_dict(self):
        """Serializes StudentUser to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "enrolled_course_ids": self.enrolled_course_ids
        }