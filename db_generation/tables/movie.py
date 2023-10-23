import random
import unittest
from datetime import datetime

from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.read_imdb_csv import get_movies_csv
from db_generation.tables.age_restriction import AgeRestriction
from db_generation.tables.language import Language
from db_generation.types import INTEGER, CHAR, DATE, BOOLEAN


class Movie(ObjectWithCounter, AddableToDatabase):
    imdb_df = get_movies_csv()
    faker = Faker()
    languages = set()

    def __init__(self, language: Language, age_restriction: AgeRestriction):
        self.id_movie = INTEGER(Movie.next())
        movie_df = self.imdb_df.iloc[self.id_movie.value]

        self.name = CHAR(movie_df["Name"])

        year = movie_df["Year"]
        first_day_of_a_year = datetime(year, 1, 1)
        last_day_of_a_year = datetime(year, 12, 31)
        self.premiere = DATE(self.faker.date_between_dates(date_start=first_day_of_a_year, date_end=last_day_of_a_year))

        self.duration = INTEGER(int(movie_df["Run_time"]))
        self.is_imax = BOOLEAN(bool(random.getrandbits(1)))
        self.fk_language = language.primary_key_value
        self.fk_age_restriction = age_restriction.primary_key_value

        self.languages.add(language)

    @classmethod
    def get_all_objects(cls, size: int, languages: list[Language], age_restrictions: list[AgeRestriction]):
        all_objects = []
        for i in range(size):
            language = Language.get_random_language(languages)
            age_restriction = random.choice(age_restrictions)
            all_objects.append(Movie(language, age_restriction))
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_movie

    def get_language(self) -> Language:
        for language in self.languages:
            if language.primary_key_value == self.fk_language:
                return language
        return None

    def get_movie_versions_summary(self, movie_versions):
        movie_versions_for_movie = [mv for mv in movie_versions if mv.get_movie().id_movie == self.id_movie]
        summary = f"{self.name.value}\nis IMAX: {self.is_imax.value}\n"
        for mv in movie_versions_for_movie:
            summary += mv.get_movie_version_details()
        return summary


class TestMovie(unittest.TestCase):
    def test_get_all_objects(self):
        languages = Language.get_all_objects()
        age_restrictions = AgeRestriction.get_all_objects()
        number_of_movies = 100

        movies = Movie.get_all_objects(number_of_movies, languages, age_restrictions)
        self.assertEqual(len(movies), number_of_movies)

        ids = [m.primary_key_value for m in movies]
        self.assertEqual(len(ids), len(set(ids)))
