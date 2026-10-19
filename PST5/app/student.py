# app/student.py
from app.user import User

class StudentUser(User):
    def __init__(self, user_id, name, enrolled_course_ids=None):
        super().__init__(user_id, name)
        self.enrolled_course_ids = enrolled_course_ids if enrolled_course_ids is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enrolled_course_ids": self.enrolled_course_ids
        }