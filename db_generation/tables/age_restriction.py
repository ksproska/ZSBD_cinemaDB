from db_generation.parent_classes import AddableToDatabase
from db_generation.types import CHAR


class AgeRestriction(AddableToDatabase):
    def __init__(self, age_restriction_name: str):
        self.age_restriction_name = CHAR(age_restriction_name)

    @classmethod
    def get_all_objects(cls):
        age_restriction_names = ["PG", "PG-13", "R"]
        all_objects = []
        for name in age_restriction_names:
            all_objects.append(AgeRestriction(name))
        return all_objects

    @property
    def primary_key_value(self):
        return self.age_restriction_name
