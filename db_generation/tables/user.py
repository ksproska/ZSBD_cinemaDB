from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.types import INTEGER, CHAR, DATE


class User(ObjectWithCounter, AddableToDatabase):
    faker = Faker()

    def __init__(self):
        self.id_user = INTEGER(User.next())
        self.name = CHAR(self.faker.first_name())
        self.surname = CHAR(self.faker.last_name())
        self.email = CHAR(self.faker.email())
        self.password = CHAR(f"{self.faker.word()}{self.faker.random_int()}")
        self.birth = DATE(self.faker.date_of_birth())

    @classmethod
    def get_all_objects(cls, size):
        return [User() for _ in range(size)]

    @property
    def primary_key_value(self):
        return self.id_user
