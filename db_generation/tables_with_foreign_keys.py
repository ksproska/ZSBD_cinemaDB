import random
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from faker import Faker

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables_without_foreign_keys import Room, AgeRestriction, Language, User
from db_generation.types import BOOLEAN, INTEGER, CHAR, DATE, FLOAT, TIMESTAMP
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

    @property
    def primary_key_value(self):
        return self.id_seat


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


def get_primary_key_from_nullable(x):
    return INTEGER(None) if x is None else x.primary_key_value


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


def can_movie_version_be_shown_in_room(movie_version: MovieVersion, room: Room):
    if movie_version.is_2d:
        return True
    if movie_version.is_3d and not room.capable_3D:
        return False
    if movie_version.get_movie().is_imax and not room.imax_capable:
        return False
    return True


class Show(ObjectWithCounter, AddableToDatabase):
    faker = Faker()
    oldest_date = (datetime.today() - relativedelta(years=5)).date()
    newest_date = (datetime.today() + relativedelta(months=1)).date()
    next_not_used_date = oldest_date
    movie_versions = set()
    rooms = set()

    def __init__(self, start_time: datetime, room: Room, movie_version: MovieVersion):
        self.id_show = INTEGER(Show.next())
        self.start_hour = INTEGER(start_time.hour)
        self.start_minute = INTEGER(start_time.minute)
        self.date = DATE(start_time.date())
        self.fk_room = room.primary_key_value
        self.fk_movieVersion = movie_version.primary_key_value

        self.rooms.add(room)
        self.movie_versions.add(movie_version)

    @classmethod
    def get_all_objects(cls, number_of_days: int, rooms: list[Room], movie_versions: list[MovieVersion]):
        all_objects = []
        for i in range(number_of_days):
            shows_for_single_day = cls.get_all_objects_for_single_day(cls.next_not_used_date, rooms, movie_versions)
            all_objects.extend(shows_for_single_day)
            cls.next_not_used_date += relativedelta(days=1)
        return all_objects

    @classmethod
    def get_all_objects_for_single_day(cls, currently_used_date: date, rooms: list[Room],
                                       movie_versions: list[MovieVersion]):
        all_objects = []
        for room in rooms:
            shows = cls.set_program_for_room_for_date(currently_used_date, movie_versions, room)
            all_objects.extend(shows)
        return all_objects

    @classmethod
    def set_program_for_room_for_date(cls, currently_used_date: date, movie_versions, room):
        all_objects = []
        date_with_time = datetime(currently_used_date.year, currently_used_date.month, currently_used_date.day, 8, 0)
        while currently_used_date == date_with_time.date():
            movie_version: MovieVersion = random.choice(movie_versions)
            while not can_movie_version_be_shown_in_room(movie_version, room):
                movie_version: MovieVersion = random.choice(movie_versions)
            all_objects.append(Show(date_with_time, room, movie_version))
            movie = movie_version.get_movie()
            date_with_time += relativedelta(minutes=round(movie.duration.value + 30, -1))
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_show

    def get_movie_version(self) -> MovieVersion:
        for movie_version in self.movie_versions:
            if movie_version.primary_key_value == self.fk_movieVersion:
                return movie_version
        return None

    def get_room(self) -> Room:
        for room in self.rooms:
            if room.primary_key_value == self.fk_room:
                return room
        return None


class Ticket(ObjectWithCounter, AddableToDatabase):
    discounts = {
        "vip": 0,
        "normal": 0.1,
        "vip_student": 0.15,
        "student": 0.2
    }
    prices = {
        "2D_imax_False": 30,
        "2D_imax_True": 33,
        "3D_imax_False": 37,
        "3D_imax_True": 34
    }

    def __init__(self, seat: Seat, show: Show, user: User | None):
        self.id_ticket: int = INTEGER(Ticket.next())
        if seat.is_vip_seat:
            available_discount_types = [v for k, v in self.discounts.items() if "vip" in k]
        else:
            available_discount_types = [v for k, v in self.discounts.items() if "vip" not in k]
        self.discount = FLOAT(random.choice(available_discount_types))

        movie_version = show.get_movie_version()
        dimension = movie_version.dimension.value
        is_imax = movie_version.get_movie().is_imax.value
        if is_imax and random.random() < 0.4:
            is_imax = False

        price = self.prices[f"{dimension}_imax_{is_imax}"]

        self.base_price = FLOAT(price)
        purchase_timestamp = datetime(
            show.date.value.year,
            show.date.value.month,
            show.date.value.day,
            show.start_hour.value,
            show.start_minute.value
        ) - relativedelta(minutes=random.randint(0, 48 * 60))
        self.purchase = TIMESTAMP(purchase_timestamp)
        self.fk_seat = seat.primary_key_value
        self.fk_show = show.primary_key_value
        self.fk_user = get_primary_key_from_nullable(user)

    @classmethod
    def get_all_objects(cls, seats: list[Seat], shows: list[Show], users: list[User]):
        all_objects = []
        for show in shows:
            room = show.get_room()
            seats_in_room = [s for s in seats if s.fk_room == room.primary_key_value]
            for seat in seats_in_room:
                user = None
                if random.random() > 0.4:
                    user = random.choice(users)
                if random.random() > 0.3:
                    all_objects.append(Ticket(seat, show, user))
        return all_objects


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
