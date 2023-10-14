import random
from datetime import datetime

import pandas as pd
from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.age_restriction import AgeRestriction
from db_generation.tables.language import Language
from db_generation.types import INTEGER, CHAR, DATE, BOOLEAN


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
        self.duration = INTEGER(int(movie_df["Run_time"]))
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
