from base_class import BaseClass
from classes import User, Place, Review, Amenity, City, Country


lucas = User(first_name="Lucas", last_name="FEEDER", password="feed4ever", email="feed@feed.com")
thomas = User(first_name="Thomas", last_name="FEEDER", password="feed4ever", email="toto@toto.com")
print(lucas.first_name, lucas.id)
print(thomas.first_name, thomas.id)
thomas.save()