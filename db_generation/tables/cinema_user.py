import datetime
import unittest

from dateutil.relativedelta import relativedelta
from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.types import INTEGER, CHAR, DATE


class CinemaUser(ObjectWithCounter, AddableToDatabase):
    faker = Faker()
    min_age = '-18y'
    max_age = '-55y'

    def __init__(self):
        self.id_user = INTEGER(CinemaUser.next())
        self.name = CHAR(self.faker.first_name())
        self.surname = CHAR(self.faker.last_name())
        self.email = CHAR(self.faker.email())
        self.password = CHAR(f"{self.faker.word()}{self.faker.random_int()}")
        self.birth = DATE(self.faker.date_between(start_date=self.max_age, end_date=self.min_age))

    @classmethod
    def get_all_objects(cls, size):
        return [CinemaUser() for _ in range(size)]

    @property
    def primary_key_value(self):
        return self.id_user


class TestCinemaUser(unittest.TestCase):
    def test_get_all_objects(self):
        number_of_users = 100
        now = datetime.datetime.now().date()
        users = CinemaUser.get_all_objects(number_of_users)
        self.assertEqual(len(users), number_of_users)

        ids = [u.primary_key_value for u in users]
        self.assertEqual(len(ids), len(set(ids)))

        for user in users:
            self.assertIsNotNone(user.name.value)
            self.assertIsNotNone(user.surname.value)
            self.assertIsNotNone(user.email.value)
            self.assertIsNotNone(user.password.value)
            self.assertIsNotNone(user.birth.value)

            min_age = relativedelta(years=18)
            self.assertLessEqual(user.birth.value, now - min_age)
