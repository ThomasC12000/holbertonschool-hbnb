import BaseClass
from users import Users

new_users = Users("Hadrien", "TAYAC", "test@gmail.com", "123456")
new_users.create_user()
print(new_users.get_user("0"))
