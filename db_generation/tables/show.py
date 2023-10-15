import random
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.room import Room
from db_generation.types import INTEGER, DATE


class Show(ObjectWithCounter, AddableToDatabase):
    faker = Faker()
    oldest_date = (datetime.today() - relativedelta(years=5)).date()
    newest_date = (datetime.today() + relativedelta(months=1)).date()
    next_not_used_date = oldest_date
    movie_versions = set()
    rooms = set()

    def __init__(self, start_time: datetime, room: Room, movie_version: MovieVersion):
        self.id_show = INTEGER(Show.next())
        self.start_hour = INTEGER(start_time.hour)
        self.start_minute = INTEGER(start_time.minute)
        self.show_date = DATE(start_time.date())
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
        date_with_time = datetime(currently_used_date.year, currently_used_date.month, currently_used_date.day, 8, 0)
        while currently_used_date == date_with_time.date():
            movie_version: MovieVersion = random.choice(movie_versions)
            while not can_movie_version_be_shown_in_room(movie_version, room):
                movie_version: MovieVersion = random.choice(movie_versions)
            all_objects.append(Show(date_with_time, room, movie_version))
            movie = movie_version.get_movie()
            break_between_shows = 30 + random.choices([0, 60 * 3, 60 * 5], weights=[8, 4, 2])[0]
            date_with_time += relativedelta(minutes=round(movie.duration.value + break_between_shows, -1))
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


def can_movie_version_be_shown_in_room(movie_version: MovieVersion, room: Room):
    if movie_version.is_2d:
        return True
    if movie_version.is_3d and not room.capable_3D:
        return False
    if movie_version.get_movie().is_imax and not room.imax_capable:
        return False
    return True
