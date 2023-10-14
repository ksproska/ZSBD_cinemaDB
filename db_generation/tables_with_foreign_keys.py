import random
from datetime import datetime

from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables_without_foreign_keys import Room, AgeRestriction, Language
from db_generation.types import BOOLEAN, INTEGER, CHAR, DATE
import pandas as pd


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


class Movie(ObjectWithCounter, AddableToDatabase):
    df = pd.read_csv('regex_imdb.csv')
    faker = Faker()

    def __init__(self, language: Language, age_restriction: AgeRestriction):
        self.id_movie = INTEGER(Movie.next())
        movie_df = self.df.iloc[self.id_movie.value]
        self.name = CHAR(movie_df["Name"])
        year = movie_df["Year"]
        self.premiere = DATE(self.faker.date_between_dates(date_start=datetime(year, 1, 1), date_end=datetime(year, 12, 31)))
        self.duration = INTEGER(movie_df["Run_time"])
        self.is_imax = BOOLEAN(bool(random.getrandbits(1)))
        self.fk_language = language.primary_key_value
        self.fk_age_restriction = age_restriction.primary_key_value

    @classmethod
    def get_all_objects(cls, size: int, languages: list[Language], age_restrictions: list[AgeRestriction]):
        all_objects = []
        for i in range(size):
            language = random.choice(languages)
            age_restriction = random.choice(age_restrictions)
            all_objects.append(Movie(language, age_restriction))
        return all_objects


def main():
    rooms = Room.get_all_objects(2)
    room_seats = Seat.get_all_objects(rooms)
    age_restrictions = AgeRestriction.get_all_objects()
    languages = Language.get_all_objects()
    movies = Movie.get_all_objects(10, languages, age_restrictions)

    [print(x) for x in rooms]
    [print(x) for x in room_seats]

    [print(x) for x in age_restrictions]
    [print(x) for x in languages]
    [print(x) for x in movies]


if __name__ == '__main__':
    main()
