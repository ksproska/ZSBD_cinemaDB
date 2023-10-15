import random
import unittest

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.room import Room
from db_generation.types import INTEGER, BOOLEAN


class Seat(ObjectWithCounter, AddableToDatabase):
    numb_of_rows_min = 10
    numb_of_rows_max = 20
    numb_of_seats_in_row_min = 15
    numb_of_seats_in_row_max = 30
    rooms = set()

    def __init__(self, room: Room, row, number):
        self.id_seat = INTEGER(Seat.next())
        self.seat_row = INTEGER(row)
        self.seat_number = INTEGER(number)
        self.is_vip_seat = BOOLEAN(bool(random.getrandbits(1)))
        self.fk_room = room.primary_key_value

        self.rooms.add(room)

    @classmethod
    def get_all_objects_single_room(cls, room: Room):
        all_objects = []
        numb_of_rows = random.randint(cls.numb_of_rows_min, cls.numb_of_rows_max)
        numb_of_seats_in_row = random.randint(cls.numb_of_seats_in_row_min, cls.numb_of_seats_in_row_max)
        for row in range(numb_of_rows):
            row_numb = row + 1
            for seat in range(numb_of_seats_in_row):
                seat_numb = seat + 1
                seat = Seat(room, row_numb, seat_numb)
                all_objects.append(seat)
        return all_objects

    @classmethod
    def get_all_objects(cls, rooms: list[Room]):
        all_objects = []
        for room in rooms:
            seats = Seat.get_all_objects_single_room(room)
            all_objects.extend(seats)
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_seat

    def get_room(self) -> Room:
        for room in self.rooms:
            if room.primary_key_value == self.fk_room:
                return room
        return None


class TestSeat(unittest.TestCase):
    def test_get_all_objects(self):
        rooms = Room.get_all_objects(20)
        seats = Seat.get_all_objects(rooms)

        self.assertEqual(len(rooms) * Seat.numb_of_rows * Seat.numb_of_seats_in_row, len(seats))

        ids = [s.primary_key_value for s in seats]
        self.assertEqual(len(ids), len(set(ids)))

        for seat in seats:
            self.assertIsNotNone(seat.seat_row.value)
            self.assertIsNotNone(seat.seat_number.value)
            self.assertIsNotNone(seat.is_vip_seat.value)
            self.assertIsNotNone(seat.fk_room.value)

            self.assertIsNotNone(seat.get_room())
