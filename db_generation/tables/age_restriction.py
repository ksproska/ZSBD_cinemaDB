import unittest

from db_generation.parent_classes import AddableToDatabase
from db_generation.types import CHAR


class AgeRestriction(AddableToDatabase):
    age_restriction_names = ["PG", "PG-13", "R"]

    def __init__(self, age_restriction_name: str):
        self.age_restriction_name = CHAR(age_restriction_name)

    @classmethod
    def get_all_objects(cls):
        return [AgeRestriction(name) for name in cls.age_restriction_names]

    @property
    def primary_key_value(self):
        return self.age_restriction_name


class TestAgeRestriction(unittest.TestCase):
    def test_get_all_objects(self):
        age_restrictions = AgeRestriction.get_all_objects()
        self.assertEqual(len(age_restrictions), 3)
        ids = [ar.primary_key_value for ar in age_restrictions]
        self.assertEqual(len(ids), len(set(ids)))
