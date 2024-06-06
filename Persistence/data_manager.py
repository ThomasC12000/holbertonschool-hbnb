from Model.base_class import BaseClass
from Model.places import Places
from persistence_manager import IPersistenceManager
from typing import Dict

class DataManager(IPersistenceManager):
    def __init__(self):
            self.storage: Dict[str, Dict[str, BaseClass | Places]] = {}

    def save(self, entity):
        entity_type = type(entity).__name__
        entity_id = entity["id"]
        self.storage[entity_type][entity_id].save()

    def get(self, entity_id, entity_type):
        if entity_type in self.storage and entity_id in self.storage[entity_type]:
            return self.storage[entity_type][entity_id]
        return None

    def update(self, entity):
        entity_type = type(entity).__name__
        entity_id = entity["id"]
        self.storage[entity_type][entity_id].update()

    def delete(self, entity_id, entity_type):
        if entity_type in self.storage and entity_id in self.storage[entity_type]:
             del self.storage[entity_type][entity_id]