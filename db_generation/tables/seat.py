import random

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.room import Room
from db_generation.types import INTEGER, BOOLEAN


class Seat(ObjectWithCounter, AddableToDatabase):
    rooms_seats = {}

    def __init__(self, room: Room, row, number):
        self.id_seat = INTEGER(Seat.next())
        self.row = INTEGER(row)
        self.number = INTEGER(number)
        self.is_vip_seat = BOOLEAN(bool(random.getrandbits(1)))
        self.fk_room = room.primary_key_value

    @classmethod
    def get_all_objects_single_room(cls, room: Room):
        rows_numb = 15
        seats_numb = 24
        all_objects = []
        for row in range(rows_numb):
            for seat in range(seats_numb):
                all_objects.append(Seat(room, row + 1, seat + 1))
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
