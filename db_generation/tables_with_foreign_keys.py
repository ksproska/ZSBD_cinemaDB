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
        self.premiere = DATE(
            self.faker.date_between_dates(date_start=datetime(year, 1, 1), date_end=datetime(year, 12, 31)))
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

    @property
    def primary_key_value(self):
        return self.id_movie


def get_primary_key_from_nullable(x):
    return INTEGER(None) if x is None else x.primary_key_value


class MovieVersion(ObjectWithCounter, AddableToDatabase):
    def __init__(self, dubbing: Language | None, subtitles: Language | None, voice_over: Language | None, movie: Movie):
        self.id_movie_version = INTEGER(MovieVersion.next())
        self.dimension = CHAR(random.choice(['2D', '3D']))
        self.fk_dubbing_language = get_primary_key_from_nullable(dubbing)
        self.fk_subtitles_language = get_primary_key_from_nullable(subtitles)
        self.fk_voice_over_language = get_primary_key_from_nullable(voice_over)
        self.fk_movie = movie.primary_key_value

    @classmethod
    def get_all_objects_for_movie(cls, movie: Movie, languages: list[Language]):
        all_objects = [MovieVersion(random.choice(languages), None, None, movie),
                       MovieVersion(None, random.choice(languages), None, movie),
                       MovieVersion(None, None, random.choice(languages), movie)]
        return all_objects

    @classmethod
    def get_all_objects(cls, movies: list[Movie], languages: list[Language]):
        all_objects = []
        for movie in movies:
            movie_versions_for_movie = cls.get_all_objects_for_movie(movie, languages)
            all_objects.extend(movie_versions_for_movie)
        return all_objects


def main():
    rooms = Room.get_all_objects(2)
    room_seats = Seat.get_all_objects(rooms)
    age_restrictions = AgeRestriction.get_all_objects()
    languages = Language.get_all_objects()
    movies = Movie.get_all_objects(10, languages, age_restrictions)
    movie_versions = MovieVersion.get_all_objects(movies, languages)

    [print(x) for x in rooms]
    [print(x) for x in room_seats]

    [print(x) for x in age_restrictions]
    [print(x) for x in languages]
    [print(x) for x in movies]
    [print(x) for x in movie_versions]


if __name__ == '__main__':
    main()
