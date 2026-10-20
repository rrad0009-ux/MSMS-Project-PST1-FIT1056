# app/user.py
"""Base User class for all users in the system."""

class User:
    """A base class for all users in the system."""
    def __init__(self, user_id=None, name="", id=None):
        # Support both 'user_id' and 'id' from JSON records
        self.id = user_id if user_id is not None else id
        self.name = name

    def to_dict(self):
        """Serializes base user attributes to a dictionary."""
        return {
            "id": self.id,
            "name": self.name
        }
    