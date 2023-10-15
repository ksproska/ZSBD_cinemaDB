import datetime

from db_generation.tables.ticket import Ticket
from db_generation.tables.show import Show
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.movie import Movie
from db_generation.tables.seat import Seat
from db_generation.tables.room import Room
from db_generation.tables.language import Language
from db_generation.tables.cinema_user import CinemaUser
from db_generation.tables.age_restriction import AgeRestriction


def generate_schema():
    age_restriction = AgeRestriction.get_all_objects()[0]
    language = Language.get_all_objects()[0]
    user = CinemaUser()
    room = Room()
    seat = Seat.get_all_objects_single_room(room)[0]
    movie = Movie(language, age_restriction)
    movie_version = MovieVersion.get_all_objects_for_movie(movie, Language.get_all_objects())[0]
    show = Show(datetime.datetime.now(), room, movie_version)
    ticket = Ticket(seat, show, user)

    all_tables = [
        age_restriction,
        language,
        user,
        room,
        seat,
        movie,
        movie_version,
        show,
        ticket
    ]

    with open("db_init.sql", "w", encoding="utf8") as f:
        f.write("-- THIS SCHEMA IS NOT COMPLEAT, it does not cover constraints or foreign keys\n")
        f.write("-- Its purpose is only to gather all attributes in one place for easier further development\n\n")
        for table in all_tables:
            f.write(table.create_table() + "\n")


if __name__ == '__main__':
    generate_schema()
