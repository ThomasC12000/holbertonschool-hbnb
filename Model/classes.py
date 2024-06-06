from base_class import BaseClass


class User(BaseClass):
    def __init__(self, email, password, first_name='', last_name='', **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Place(BaseClass):
    def __init__(self, name, description, address, city_id, host_id, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.host_id = host_id

class Review(BaseClass):
    def __init__(self, user_id, place_id, rating, comment, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment

class Amenity(BaseClass):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

class City(BaseClass):
    def __init__(self, name, country_id, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.country_id = country_id

class Country(BaseClass):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name