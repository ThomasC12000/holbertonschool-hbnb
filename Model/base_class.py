from uuid import uuid4
from datetime import datetime
import json
import os
"""Parent class with shared methods"""

class BaseClass:
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid4())
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def save(self):
        """Save the current instance to a file."""
        data = self.__dict__
        all_data = self._load_all()
        existing = next((item for item in all_data if item['id'] == self.id), None)
        if existing:
            all_data = [item if item['id'] != self.id else data for item in all_data]
        else:
            all_data.append(data)
        self._save_all(all_data)

    def delete(self):
        """Delete the current instance from the file."""
        all_data = self._load_all()
        all_data = [item for item in all_data if item['id'] != id]
        self._save_all(all_data)

    def update(self, **kwargs):
        """Update the attributes of the current instance."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
        self.save()


