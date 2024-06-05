from datetime import datetime
"""abstract base class for all classes"""


class BaseClass:
    def __init__(self, created_at, updated_at):
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        self.updated_at = datetime.now()
        return self.updated_at

    def update(self):
        self.updated_at = datetime.now()
        return self.updated_at

