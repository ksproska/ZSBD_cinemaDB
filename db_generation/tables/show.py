import random
import unittest
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.age_restriction import AgeRestriction
from db_generation.tables.language import Language
from db_generation.tables.movie import Movie
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.room import Room
from db_generation.tables.seat import Seat
from db_generation.types import INTEGER, DATE


class Show(ObjectWithCounter, AddableToDatabase):
    min_break_between_movies = 30
    additional_break = [0, 60 * 3, 60 * 5]
    additional_break_weights = [8, 4, 2]

    earliest_show_hour = 8
    earliest_show_minute = 0

    faker = Faker()
    oldest_date = (datetime.today() - relativedelta(months=3)).date()
    newest_date = (datetime.today() + relativedelta(months=1)).date()
    next_not_used_date = oldest_date
    movie_versions = set()
    rooms = set()

    def __init__(self, start_datatime: datetime, room: Room, movie_version: MovieVersion):
        self.id_show = INTEGER(Show.next())
        self.start_hour = INTEGER(start_datatime.hour)
        self.start_minute = INTEGER(start_datatime.minute)
        self.show_date = DATE(start_datatime.date())

        self.fk_room = room.primary_key_value
        self.fk_movie_version = movie_version.primary_key_value

        self.rooms.add(room)
        self.movie_versions.add(movie_version)

    @classmethod
    def get_all_objects(cls, number_of_days: int, rooms: list[Room], movie_versions: list[MovieVersion]):
        all_objects = []
        for i in range(number_of_days):
            shows_for_single_day = cls.get_all_objects_for_single_day(cls.next_not_used_date, rooms, movie_versions)
            all_objects.extend(shows_for_single_day)
            cls.next_not_used_date += relativedelta(days=1)
        return all_objects

    @classmethod
    def get_all_objects_for_single_day(cls, currently_used_date: date, rooms: list[Room],
                                       movie_versions: list[MovieVersion]):
        all_objects = []
        for room in rooms:
            shows = cls.set_program_for_room_for_date(currently_used_date, movie_versions, room)
            all_objects.extend(shows)
        return all_objects

    @classmethod
    def set_program_for_room_for_date(cls, currently_used_date: date, movie_versions, room):
        all_objects = []
        next_available_datetime = datetime(
            currently_used_date.year,
            currently_used_date.month,
            currently_used_date.day,
            cls.earliest_show_hour,
            cls.earliest_show_minute
        )
        while currently_used_date == next_available_datetime.date():
            movie_version: MovieVersion = MovieVersion.get_movie_version_that_can_be_shown_in_room(movie_versions, room)
            all_objects.append(Show(next_available_datetime, room, movie_version))

            movie_duration = movie_version.get_movie().duration.value
            break_between_shows = cls.min_break_between_movies \
                                  + random.choices(cls.additional_break, weights=cls.additional_break_weights)[0]
            next_available_datetime += relativedelta(minutes=round(movie_duration + break_between_shows, -1))
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_show

    def get_movie_version(self) -> MovieVersion:
        for movie_version in self.movie_versions:
            if movie_version.primary_key_value == self.fk_movie_version:
                return movie_version
        return None

    def get_room(self) -> Room:
        for room in self.rooms:
            if room.primary_key_value == self.fk_room:
                return room
        return None

    def get_show_schema(self, tickets, seats: list[Seat]):
        discounts = {
            0.1: "N-",
            0.2: "S-",
            0: "NV",
            0.15: "SV",
        }
        room = self.get_room()
        tickets_for_show = [t for t in tickets if t.fk_show == self.id_show]
        seats_for_room = [s for s in seats if s.fk_room == room.id_room]
        row_number = seats_for_room[0].seat_row.value
        schema = f"{self.__class__.__name__} {self.id_show} ({int(100 * (len(tickets_for_show) / len(seats_for_room)))}%)\n"
        for seat in seats_for_room:
            seat_row = seat.seat_row.value
            br = "" if seat_row == row_number else "\n"
            t = "_"
            d = "__"
            for ticket in tickets_for_show:
                if ticket.get_seat().id_seat == seat.id_seat:
                    t = "X" if ticket.fk_user.value is None else "U"
                    d = discounts[ticket.discount.value]
                    break
            schema += br + t + d + " "
            row_number = seat_row
        return schema + "\n"

    @classmethod
    def get_dates_summary(cls, shows):
        last_date = shows[0].show_date.value
        counter = 0
        summary = ""
        for show in shows:
            if last_date == show.show_date.value:
                counter += 1
            else:
                summary += f"{last_date}\t{counter}\n"
                counter = 0
                last_date = show.show_date.value
        return summary


class TestShow(unittest.TestCase):
    def test_get_all_objects(self):
        rooms = Room.get_all_objects(3)
        age_restrictions = AgeRestriction.get_all_objects()
        languages = Language.get_all_objects()
        movies = Movie.get_all_objects(10, languages, age_restrictions)
        movie_versions = MovieVersion.get_all_objects(movies, languages)
        shows = Show.get_all_objects(5, rooms, movie_versions)

        ids = [s.primary_key_value for s in shows]
        self.assertEqual(len(ids), len(set(ids)))

        for show in shows:
            room = show.get_room()
            self.assertEqual(show.get_room().id_room, room.id_room)
            movie_version = show.get_movie_version()
            if movie_version.is_3d:
                self.assertTrue(room.capable_3D.value)
            if movie_version.get_movie().is_imax.value:
                self.assertTrue(room.imax_capable.value)
