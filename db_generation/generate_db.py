from db_generation.tables.movie import Movie
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.room import Room
from db_generation.tables.language import Language
from db_generation.tables.seat import Seat
from db_generation.tables.show import Show
from db_generation.tables.ticket import Ticket
from db_generation.tables.cinema_user import CinemaUser
from db_generation.tables.age_restriction import AgeRestriction


if __name__ == '__main__':
    rooms = Room.get_all_objects(3)
    seats = Seat.get_all_objects(rooms)
    age_restrictions = AgeRestriction.get_all_objects()
    languages = Language.get_all_objects()
    movies = Movie.get_all_objects(10, languages, age_restrictions)
    movie_versions = MovieVersion.get_all_objects(movies, languages)
    shows = Show.get_all_objects(2, rooms, movie_versions)
    users = CinemaUser.get_all_objects(6)
    tickets = Ticket.get_all_objects(seats, shows, users)

    all_object_tables = [
        rooms,
        seats,
        age_restrictions,
        languages,
        movies,
        movie_versions,
        shows,
        users,
        tickets
    ]

    with open("output.sql", "w", encoding="utf8") as f:
        for objs in all_object_tables:
            for obj in objs:
                f.write(obj.sql_addable + "\n")
        f.write('commit work;')
