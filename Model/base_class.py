from datetime import datetime
import json
from uuid import uuid4
"""Base class for all classes in the project"""


class BaseClass:
    def __init__(self, created_at, updated_at, id):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    def save(self):
        self.updated_at = datetime.now()
        return str(self.updated_at)

    def update(self):
        self.updated_at = datetime.now()
        return str(self.updated_at)

    def to_json(self):
        """
        Return a JSON representation of the object
        after converting it to a dictionary.
        """
        dict_obj = self.__dict__.copy()
        dict_obj['created_at'] = self.created_at.isoformat()
        dict_obj['updated_at'] = self.updated_at.isoformat()
        dict_obj['id'] = str(self.id)
        return json.dumps(dict_obj)

    def save_to_file(self, filename):
        """Save the JSON representation of the object to a file"""
        with open(filename, 'a') as file:
            file.write(self.to_json())
            if file.closed:
                return ("Object saved to file")
