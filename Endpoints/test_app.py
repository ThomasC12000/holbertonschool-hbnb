import unittest
import json
from app import app, users

class UserEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users.clear()  # Assurez-vous que l'état initial est vide

    def test_create_user(self):
        response = self.app.post('/users/', json={"email": "test@example.com", "first_name": "John", "last_name": "Doe"})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], "test@example.com")

    def test_create_user_invalid_email(self):
        response = self.app.post('/users/', json={"email": "testexample.com", "first_name": "John", "last_name": "Doe"})
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        self.app.post('/users/', json={"email": "test@example.com", "first_name": "John", "last_name": "Doe"})
        response = self.app.post('/users/', json={"email": "test@example.com", "first_name": "Jane", "last_name": "Smith"})
        self.assertEqual(response.status_code, 409)

    def test_get_user(self):
        # Créez un utilisateur d'abord
        create_response = self.app.post('/users/', json={"email": "test@example.com", "first_name": "John", "last_name": "Doe"})
        self.assertEqual(create_response.status_code, 201)
        user_id = json.loads(create_response.data)['id']

        # Récupérez l'utilisateur créé
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], "test@example.com")

    def test_update_user(self):
        # Créez un utilisateur d'abord
        create_response = self.app.post('/users/', json={"email": "test@example.com", "first_name": "John", "last_name": "Doe"})
        self.assertEqual(create_response.status_code, 201)
        user_id = json.loads(create_response.data)['id']

        # Mettez à jour l'utilisateur créé
        response = self.app.put(f'/users/{user_id}', json={"email": "new@example.com", "first_name": "John", "last_name": "Doe"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], "new@example.com")

    def test_delete_user(self):
        # Créez un utilisateur d'abord
        create_response = self.app.post('/users/', json={"email": "test@example.com", "first_name": "John", "last_name": "Doe"})
        self.assertEqual(create_response.status_code, 201)
        user_id = json.loads(create_response.data)['id']

        # Supprimez l'utilisateur créé
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
