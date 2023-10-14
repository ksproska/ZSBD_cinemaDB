from db_generation.tables.movie import Movie
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.room import Room
from db_generation.tables.language import Language
from db_generation.tables.seat import Seat
from db_generation.tables.show import Show
from db_generation.tables.ticket import Ticket
from db_generation.tables.user import User
from db_generation.tables.age_restriction import AgeRestriction


def main():
    rooms = Room.get_all_objects(3)
    seats = Seat.get_all_objects(rooms)
    age_restrictions = AgeRestriction.get_all_objects()
    languages = Language.get_all_objects()
    movies = Movie.get_all_objects(10, languages, age_restrictions)
    movie_versions = MovieVersion.get_all_objects(movies, languages)
    shows = Show.get_all_objects(2, rooms, movie_versions)
    users = User.get_all_objects(6)
    tickets = Ticket.get_all_objects(seats, shows, users)

    [print(x) for x in rooms]
    [print(x) for x in seats]

    [print(x) for x in age_restrictions]
    [print(x) for x in languages]
    [print(x) for x in movies]
    [print(x) for x in movie_versions]

    [print(x) for x in shows]
    [print(x) for x in tickets]


if __name__ == '__main__':
    main()
