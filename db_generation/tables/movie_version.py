import random
import unittest

from db_generation.common import get_primary_key_from_nullable
from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.age_restriction import AgeRestriction
from db_generation.tables.language import Language
from db_generation.tables.movie import Movie
from db_generation.tables.room import Room
from db_generation.types import INTEGER, CHAR


class MovieVersion(ObjectWithCounter, AddableToDatabase):
    dimension2d = '2D'
    dimension3d = '3D'
    dimensions = [dimension2d, dimension3d]
    weights = [7, 3]
    movies = set()

    def __init__(self, movie: Movie,
                 dubbing: Language | None = None,
                 subtitles: Language | None = None,
                 voice_over: Language | None = None):
        self.id_movie_version = INTEGER(MovieVersion.next())

        self.dimension = CHAR(random.choices(self.dimensions, weights=self.weights)[0])

        self.fk_dubbing_language = get_primary_key_from_nullable(dubbing)
        self.fk_subtitles_language = get_primary_key_from_nullable(subtitles)
        self.fk_voice_over_language = get_primary_key_from_nullable(voice_over)
        self.fk_movie = movie.primary_key_value

        self.movies.add(movie)

    @classmethod
    def get_all_objects_for_movie(cls, movie: Movie, languages: list[Language]):
        original_language = movie.get_language()
        if random.random() < 0.6:
            all_objects = [MovieVersion(movie, dubbing=Language.get_random_language_different_than(languages, original_language)),
                           MovieVersion(movie, subtitles=Language.get_random_language_different_than(languages, original_language))]
        elif random.random() < 0.8:
            all_objects = [MovieVersion(movie, voice_over=Language.get_random_language_different_than(languages, original_language))]
        else:
            all_objects = [MovieVersion(movie)]
        return all_objects

    @classmethod
    def get_all_objects(cls, movies: list[Movie], languages: list[Language]):
        all_objects = []
        for movie in movies:
            movie_versions_for_movie = cls.get_all_objects_for_movie(movie, languages)
            all_objects.extend(movie_versions_for_movie)
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_movie_version

    @property
    def is_3d(self):
        return self.dimension.value == self.dimension3d

    @property
    def is_2d(self):
        return self.dimension.value == self.dimension2d

    def get_movie(self) -> Movie:
        for movie in self.movies:
            if movie.primary_key_value == self.fk_movie:
                return movie
        return None

    @classmethod
    def get_movie_version_that_can_be_shown_in_room(cls, movie_versions, room: Room):
        movie_version: MovieVersion = random.choice(movie_versions)
        while not can_movie_version_be_shown_in_room(movie_version, room):
            movie_version: MovieVersion = random.choice(movie_versions)
        return movie_version


def can_movie_version_be_shown_in_room(movie_version: MovieVersion, room: Room):
    if movie_version.is_3d and not room.capable_3D.value:
        return False
    if movie_version.get_movie().is_imax.value and not room.imax_capable.value:
        return False
    return True


class TestMovieVersion(unittest.TestCase):
    def test_get_all_objects(self):
        age_restrictions = AgeRestriction.get_all_objects()
        languages = Language.get_all_objects()
        number_of_movies = 100
        movies = Movie.get_all_objects(number_of_movies, languages, age_restrictions)
        movie_versions = MovieVersion.get_all_objects(movies, languages)

        self.assertGreater(len(movie_versions), number_of_movies)

        for movie_version in movie_versions:
            is_dubbing = movie_version.fk_dubbing_language.value is not None
            is_voice_over = movie_version.fk_voice_over_language.value is not None
            self.assertTrue(not (is_dubbing and is_voice_over))

            original_language = movie_version.get_movie().get_language().id_language.value
            self.assertNotEquals(original_language, movie_version.fk_dubbing_language.value)
            self.assertNotEquals(original_language, movie_version.fk_voice_over_language.value)
            self.assertNotEquals(original_language, movie_version.fk_subtitles_language.value)
