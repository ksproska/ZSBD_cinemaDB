import datetime

from db_generation.tables_with_foreign_keys import Seat, Movie, MovieVersion, Show
from db_generation.tables_without_foreign_keys import AgeRestriction, Language, User, Room

age_restriction = AgeRestriction.get_all_objects()[0]
language = Language.get_all_objects()[0]
user = User()
room = Room()
seat = Seat.get_all_objects_single_room(room)[0]
movie = Movie(language, age_restriction)
movie_version = MovieVersion.get_all_objects_for_movie(movie, [language])[0]
show = Show(datetime.datetime.now(), room, movie_version)

all_tables = [
    age_restriction,
    language,
    user,
    room,
    seat,
    movie,
    movie_version,
    show
]

with open("db_init.sql", "w", encoding="utf8") as f:
    for table in all_tables:
        f.write(table.create_table())
