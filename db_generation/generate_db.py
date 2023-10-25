import pandas as pd
from tqdm import tqdm

from db_generation.generate_shema import generate_schema
from db_generation.tables.age_restriction import AgeRestriction
from db_generation.tables.cinema_user import CinemaUser
from db_generation.tables.language import Language
from db_generation.tables.movie import Movie
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.room import Room
from db_generation.tables.seat import Seat
from db_generation.tables.show import Show
from db_generation.tables.ticket import Ticket


def generate_db():
    number_of_rooms = 25
    number_of_movies = 900
    number_of_days_to_create_shows_for = 30 * 6
    number_of_users = 10000

    rooms = Room.get_all_objects(number_of_rooms)
    seats = Seat.get_all_objects(rooms)
    age_restrictions = AgeRestriction.get_all_objects()
    languages = Language.get_all_objects()
    movies = Movie.get_all_objects(number_of_movies, languages, age_restrictions)
    movie_versions = MovieVersion.get_all_objects(movies, languages)
    shows = Show.get_all_objects(number_of_days_to_create_shows_for, rooms, movie_versions)
    users = CinemaUser.get_all_objects(number_of_users)
    print("Creating tickets")
    tickets = Ticket.get_all_objects(seats, shows, users)

    all_object_tables = [
        age_restrictions,
        languages,
        rooms,
        seats,
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

    with open("output.csv", "w", encoding="utf8") as f:
        f.write("TableName,Count\n")
        for objs in all_object_tables:
            f.write(f"{objs[0].table_name},{len(objs)}\n")

    df = pd.read_csv("output.csv").sort_values("Count")
    print(df)

    print("\nSum: ", df["Count"].sum())

    with open("setup_rooms.txt", "w", encoding="utf8") as f:
        for room in rooms:
            f.write(room.get_room_schema(seats) + "\n")

    with open("setup_movie_versions.txt", "w", encoding="utf8") as f:
        for movie in movies:
            f.write(movie.get_movie_versions_summary(movie_versions) + "\n")

    with open("setup_shows_dates.txt", "w", encoding="utf8") as f:
        f.write(Show.get_dates_summary(shows))

    with open("setup_shows.txt", "w", encoding="utf8") as f:
        for show in tqdm(shows[:100:10]):
            f.write(show.get_show_schema(tickets, seats) + "\n")
        f.write("\n...")


if __name__ == '__main__':
    generate_db()
    generate_schema()
