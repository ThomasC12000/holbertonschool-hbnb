from Model.base_class import BaseClass
from Model.classes import Place, User, Review, Amenity, City, Country
from Persistence.persistence_manager import IPersistenceManager
import json

classes = {
    "Place": Place,
    "User": User,
    "Review": Review,
    "Amenity": Amenity,
    "City": City,
    "Country": Country
}

class DataManager(IPersistenceManager):
    def __init__(self, storage_file="data.json"):
        self.storage_file = storage_file
        self.data = self.load_data()

    def load_data(filename=None):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return {}

    def exists(self, entity_id, entity_type):
        cls_storage = self.data.get(entity_type)
        if (cls_storage):
            return cls_storage.get(entity_id) is not None
        return False

    def create(self, cls_name, *args, **kwargs):
        try:
            cls = classes[cls_name]
            entity = cls(*args, **kwargs)
            if (self.exists(entity.id, cls_name)):
                raise Exception("Entity already exists")
            if (self.data.get(cls_name) is None):
                self.data[cls_name] = {}
            self.data[cls_name][entity.id] = entity
            return entity
        except Exception as e:
            print(e)
            return None

    def save(self, entity):
        entity_type = type(entity).__name__
        entity_id = entity.id
        if (self.exists(entity_id, entity_type)):
            self.data[entity_type][entity_id].save()

    def get(self, entity_id, entity_type):
        if entity_type in self.data and entity_id in self.data[entity_type]:
            return self.data[entity_type][entity_id]
        return None

    def get_by_class(self, cls_name):
        return self.data.get(cls_name)

    def update(self, entity):
        entity_type = type(entity).__name__
        entity_id = entity.id
        self.data[entity_type][entity_id].update()

    def delete(self, entity_id, entity_type):
            del self.data[entity_type][entity_id]

data_manager = DataManager()

