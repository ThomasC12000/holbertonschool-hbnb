from uuid import uuid4
from datetime import datetime
from base_class import BaseClass

class Users(BaseClass):
    def __init__(self, first_name, last_name, email,
                 password, created_at = datetime.now(),
                 updated_at = datetime.now(), id = uuid4()):
        super().__init__(created_at, updated_at, id)
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    
    def get_user(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None
