from Model.base_class import BaseClass
"""Classes for the different models in the application."""

class User(BaseClass):
    def __init__(self, email, password, first_name='', last_name='', **kwargs):
        super().__init__(**kwargs)
        assert email, "User: email missing"
        assert password, "User: password missing"
        assert first_name, "User: first_name missing"
        assert last_name, "User: last_name missing"
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Place(BaseClass):
    def __init__(self, name='', location='', description='', address='', city_id='', host_id='', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.host_id = host_id
        self.location = location

class Review(Place, User):
    def __init__(self, user_id, id, place_id='', rating='', comment='', **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment

class Amenity(BaseClass):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

class City(BaseClass):
    def __init__(self, name, id, country, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.id = id
        self.country = country

class Country(BaseClass):
    def __init__(self, name, country_code, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code
