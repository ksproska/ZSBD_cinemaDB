import random
from faker import Faker
from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.types import INTEGER, CHAR, DATE, NUMBER, BOOLEAN


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


class Language(AddableToDatabase, ObjectWithCounter):
    def __init__(self, language_name: str):
        self.id_language = INTEGER(Language.next())
        self.language_name = CHAR(language_name)

    @classmethod
    def get_all_objects(cls):
        language_names = ["polish", "english", "german", "czech", "slovene"]
        all_objects = []
        for name in language_names:
            all_objects.append(Language(name))
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_language


class Room(ObjectWithCounter, AddableToDatabase):
    faker = Faker()

    def __init__(self):
        self.id_room = INTEGER(Room.next())
        self.room_sign = CHAR(chr(65 + self.id_room.value - 1))
        self.floor_number = NUMBER(self.faker.random_int(1, 3))
        self.imax_capable = BOOLEAN(bool(random.getrandbits(1)))
        self.wheelchair_availability = BOOLEAN(bool(random.getrandbits(1)))
        self.sponsor = CHAR(self.faker.company())
        self.capable_3D = BOOLEAN(bool(random.getrandbits(1)))

    @property
    def primary_key_value(self):
        return self.id_room

    @classmethod
    def get_all_objects(cls, size):
        return [Room() for _ in range(size)]


if __name__ == '__main__':
    age_restrictions = AgeRestriction.get_all_objects()
    languages = Language.get_all_objects()
    users = User.get_all_objects(6)
    rooms = Room.get_all_objects(4)

    [print(x) for x in age_restrictions]
    [print(x) for x in languages]
    [print(x) for x in users]
    [print(x) for x in rooms]
