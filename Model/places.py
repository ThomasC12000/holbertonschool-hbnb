from uuid import uuid4
from datetime import datetime
from base_class import BaseClass

class Places(BaseClass):
    def __init__(self, ):
        self.users = []
        self.name = name
        self.email = email
        self.password = password

    def create_user(self):
        user = {
            'id': str(uuid4()), # IT'S A STRING
            'name': self.name,
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
