import random
import unittest

from db_generation.common import get_primary_key_from_nullable
from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.room import Room
from db_generation.types import INTEGER, BOOLEAN


class Seat(ObjectWithCounter, AddableToDatabase):
    numb_of_rows_min = 10
    numb_of_rows_max = 20
    numb_of_seats_in_row_min = 15
    numb_of_seats_in_row_max = 30
    rooms = set()

    def __init__(self, room: Room, row, number, is_vip_seat=False, seat=None):
        self.id_seat = INTEGER(Seat.next())
        self.seat_row = INTEGER(row)
        self.seat_number = INTEGER(number)
        self.is_vip_seat = BOOLEAN(is_vip_seat)
        self.fk_room = room.primary_key_value
        self.fk_connected_seat = get_primary_key_from_nullable(seat)

        self.rooms.add(room)

    @classmethod
    def get_all_objects_single_room(cls, room: Room):
        all_objects = []
        numb_of_rows = random.randint(cls.numb_of_rows_min, cls.numb_of_rows_max)
        numb_of_seats_in_row = random.randint(cls.numb_of_seats_in_row_min, cls.numb_of_seats_in_row_max)
        vip_seat_rows = [numb_of_rows - 4, numb_of_rows - 3, numb_of_rows - 2]
        connected_seat_rows = [numb_of_rows - 5, numb_of_rows - 4, numb_of_rows - 3]
        middle_seat = int(numb_of_seats_in_row/2)
        numb_of_vip_in_row = 8
        numb_of_connected_in_row = 4
        vip_seats_in_row = [middle_seat - x + (numb_of_vip_in_row/2) - 1 for x in range(numb_of_vip_in_row)]
        connected_seats_in_row = [middle_seat - x + (numb_of_connected_in_row/2) for x in range(numb_of_connected_in_row)]
        for row in range(numb_of_rows):
            row_numb = row + 1
            for seat in range(numb_of_seats_in_row):
                seat_numb = seat + 1
                is_vip_seat = row in vip_seat_rows and seat in vip_seats_in_row
                seat = Seat(room, row_numb, seat_numb, is_vip_seat)
                all_objects.append(seat)
        connected_seats = [x for x in all_objects if x.seat_row.value in connected_seat_rows and x.seat_number.value in connected_seats_in_row]
        for i in range(int(len(connected_seats) / 2)):
            s1 = connected_seats[int(i * 2)]
            s2 = connected_seats[int(i * 2 + 1)]
            # s1.fk_connected_seat = s2.id_seat
            s2.fk_connected_seat = s1.id_seat
        return all_objects

    @property
    def get_modifier_for_connected_seat(self):
        if self.fk_connected_seat.value is None:
            return ""
        return f"\nUPDATE Seats SET fk_connected_seat = {self.id_seat} WHERE id_seat = {self.fk_connected_seat};"

    @property
    def sql_addable(self):
        return f"{super().sql_addable}{self.get_modifier_for_connected_seat}"

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

        self.assertLessEqual(len(rooms) * Seat.numb_of_rows_min * Seat.numb_of_seats_in_row_min, len(seats))
        self.assertGreaterEqual(len(rooms) * Seat.numb_of_rows_max * Seat.numb_of_seats_in_row_max, len(seats))

        ids = [s.primary_key_value for s in seats]
        self.assertEqual(len(ids), len(set(ids)))

        for seat in seats:
            self.assertIsNotNone(seat.seat_row.value)
            self.assertIsNotNone(seat.seat_number.value)
            self.assertIsNotNone(seat.is_vip_seat.value)
            self.assertIsNotNone(seat.fk_room.value)

            self.assertIsNotNone(seat.get_room())
