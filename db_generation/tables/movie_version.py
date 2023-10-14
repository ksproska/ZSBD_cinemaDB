import random

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.language import Language
from db_generation.tables.movie import Movie
from db_generation.common import get_primary_key_from_nullable
from db_generation.types import INTEGER, CHAR


class MovieVersion(ObjectWithCounter, AddableToDatabase):
    movies = set()

    def __init__(self, dubbing: Language | None, subtitles: Language | None, voice_over: Language | None, movie: Movie):
        self.id_movie_version = INTEGER(MovieVersion.next())
        self.dimension = CHAR(random.choice(['2D', '3D']))
        self.fk_dubbing_language = get_primary_key_from_nullable(dubbing)
        self.fk_subtitles_language = get_primary_key_from_nullable(subtitles)
        self.fk_voice_over_language = get_primary_key_from_nullable(voice_over)
        self.fk_movie = movie.primary_key_value
        self.movies.add(movie)

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

    @property
    def primary_key_value(self):
        return self.id_movie_version

    @property
    def is_3d(self):
        return self.dimension.value == '3D'

    @property
    def is_2d(self):
        return self.dimension.value == '2D'

    def get_movie(self) -> Movie:
        for movie in self.movies:
            if movie.primary_key_value == self.fk_movie:
                return movie
        return None
