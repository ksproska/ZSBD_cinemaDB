import random

from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.types import INTEGER, CHAR, NUMBER, BOOLEAN


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
