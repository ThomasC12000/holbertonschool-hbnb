from base_class import BaseClass
from users import Users

new_users = Users("Lucas", "FEEDER", "feed@gmail.com", "feed4ever")
new_users.to_json()
new_users.save_to_file("users.json")
