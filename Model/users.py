from uuid import uuid4
from datetime import datetime
from base_class import BaseClass

class Users(BaseClass):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(created_at=datetime.now(), updated_at=datetime.now())
        self.users = []
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def create_user(self):
        user = {
            'id': uuid4(), # IT'S A STRING
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        self.users.append(user)
        return user
    
    def get_user(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None
