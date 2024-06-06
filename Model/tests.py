from base_class import BaseClass
import classes

new_users = classes.Users("Lucas", "FEEDER", "feed4ever")
new_users.to_json()
new_users.save_to_file("users.json")
