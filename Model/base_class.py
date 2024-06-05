from datetime import datetime
import json
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

    def to_json(self):
        """Return a JSON representation of the object"""
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Return a dictionary representation of the object"""
        return self.__dict__

    def save_to_file(self, filename):
        """Save the JSON representation of the object to a file"""
        with open(filename, 'w') as file:
            file.write(self.to_json())
            if file.closed:
                return ("Object saved to file")
