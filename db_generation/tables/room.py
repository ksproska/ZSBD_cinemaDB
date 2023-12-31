import random
import unittest

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

    def get_room_schema(self, seats) -> str:
        seats_in_room = [s for s in seats if s.get_room().id_room == self.id_room]
        row_number = seats_in_room[0].seat_row.value
        schema = f"{self.__class__.__name__} {self.id_room} - "
        if self.capable_3D.value:
            schema += "3D "
        else:
            schema += "2D "
        if self.imax_capable.value:
            schema += "IMAX"
        schema += "\n"
        for inx, seat in enumerate(seats_in_room):
            seat_row = seat.seat_row.value
            br = "" if seat_row == row_number else "\n"
            s = "V" if seat.is_vip_seat.value else "_"
            c = "C" if seat.fk_connected_seat.value is not None \
                       or inx + 1 < len(seats_in_room) and seats_in_room[inx+1].fk_connected_seat.value is not None \
                else "_"
            schema += br + s + c + " "
            row_number = seat_row
        schema += "\n"
        return schema


class TestRoom(unittest.TestCase):
    def test_get_all_objects(self):
        number_of_rooms = 20
        rooms = Room.get_all_objects(number_of_rooms)
        self.assertEqual(len(rooms), number_of_rooms)

        ids = [r.primary_key_value for r in rooms]
        self.assertEqual(len(ids), len(set(ids)))

        for room in rooms:
            self.assertIsNotNone(room.room_sign.value)
            self.assertIsNotNone(room.floor_number.value)
            self.assertIsNotNone(room.imax_capable.value)
            self.assertIsNotNone(room.wheelchair_availability.value)
            self.assertIsNotNone(room.sponsor.value)
            self.assertIsNotNone(room.capable_3D.value)
