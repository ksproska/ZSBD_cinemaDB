import random
import unittest
from datetime import datetime

from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.age_restriction import AgeRestriction
from db_generation.tables.language import Language
from db_generation.tables.movie import Movie
from db_generation.tables.movie_version import MovieVersion
from db_generation.tables.room import Room
from db_generation.tables.seat import Seat
from db_generation.tables.show import Show
from db_generation.tables.cinema_user import CinemaUser
from db_generation.common import get_primary_key_from_nullable
from db_generation.types import INTEGER, FLOAT, TIMESTAMP


class Ticket(ObjectWithCounter, AddableToDatabase):
    min_advance_of_purchase = -30
    max_advance_of_purchase = 60 * 48

    probability_of_user_purchase = 0.75

    discounts = {
        ("normal", None): 0.1,
        ("student", None): 0.2,
        ("normal", "vip"): 0,
        ("student", "vip"): 0.15,
    }
    prices = {
        ("2D", False): 30,
        ("2D", True): 33,
        ("3D", False): 37,
        ("3D", True): 34
    }
    seats = set()

    def __init__(self, seat: Seat, show: Show, user: CinemaUser | None):
        self.id_ticket = INTEGER(Ticket.next())

        self.discount = FLOAT(self.get_discount(seat))
        self.base_price = FLOAT(self.get_price(show))
        self.purchase = TIMESTAMP(self.get_purchase(show))

        self.fk_seat = seat.primary_key_value
        self.fk_show = show.primary_key_value
        self.fk_user = get_primary_key_from_nullable(user)

        self.seats.add(seat)

    def get_discount(self, seat: Seat):
        if seat.is_vip_seat.value:
            return random.choice([v for k, v in self.discounts.items() if "vip" == k[1]])
        return random.choice([v for k, v in self.discounts.items() if k[1] is None])

    def get_price(self, show: Show):
        dimension, is_imax = self.get_dimension_and_is_imax(show)
        price = self.prices[(dimension, is_imax)]
        return price

    def get_dimension_and_is_imax(self, show: Show) -> (str, bool):
        movie_version = show.get_movie_version()
        dimension = movie_version.dimension.value
        is_imax = movie_version.get_movie().is_imax.value
        return dimension, is_imax

    def get_purchase(self, show: Show):
        show_date = show.show_date.value
        show_timestamp = datetime(
            show_date.year,
            show_date.month,
            show_date.day,
            show.start_hour.value,
            show.start_minute.value
        )
        advance_of_ticket_purchase = self.get_random_purchase_advantage_in_minutes()
        return show_timestamp - advance_of_ticket_purchase

    @classmethod
    def get_random_purchase_advantage_in_minutes(cls):
        return relativedelta(
            minutes=random.randint(cls.min_advance_of_purchase, cls.max_advance_of_purchase)
        )

    @classmethod
    def get_all_objects(cls, seats: list[Seat], shows: list[Show], users: list[CinemaUser]):
        all_objects = []
        for show in tqdm(shows):
            room = show.get_room()
            seats_in_room = [s for s in seats if s.fk_room == room.primary_key_value]
            numb_of_rows = seats_in_room[-1].seat_row.value
            numb_of_columns = seats_in_room[-1].seat_number.value
            show_fillup_probability = random.random() * 0.75
            for seat in seats_in_room:
                rowprob = (1 - seat.seat_row.value / numb_of_rows)
                colprob = abs(seat.seat_number.value - (numb_of_columns/2))/(numb_of_columns/2)
                base = (rowprob + colprob)
                if base - show_fillup_probability < random.random():
                    if random.random() < cls.probability_of_user_purchase:
                        user = random.choice(users)
                        all_objects.append(Ticket(seat, show, user))
                    else:
                        all_objects.append(Ticket(seat, show, None))
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_ticket

    def get_seat(self) -> Seat:
        for seat in self.seats:
            if seat.primary_key_value == self.fk_seat:
                return seat
        return None


class TestTicket(unittest.TestCase):
    def test_get_all_objects(self):
        rooms = Room.get_all_objects(3)
        seats = Seat.get_all_objects(rooms)
        age_restrictions = AgeRestriction.get_all_objects()
        languages = Language.get_all_objects()
        movies = Movie.get_all_objects(10, languages, age_restrictions)
        movie_versions = MovieVersion.get_all_objects(movies, languages)
        shows = Show.get_all_objects(5, rooms, movie_versions)
        users = CinemaUser.get_all_objects(5)
        tickets = Ticket.get_all_objects(seats, shows, users)

        ids = [t.primary_key_value for t in tickets]
        self.assertEqual(len(ids), len(set(ids)))

        all_possible_seats_to_buy = 0
        for show in shows:
            room = show.get_room()
            seats_in_room = [s for s in seats if s.fk_room == room.primary_key_value]
            all_possible_seats_to_buy += len(seats_in_room)

        # actual_overall_fill_up = len(tickets) / all_possible_seats_to_buy
        # self.assertLessEqual(abs(actual_overall_fill_up - Ticket.overall_fill_up), 0.05)

    def test_purchase_advantage(self):
        min_val, max_val = None, None
        for _ in range(100):
            delta_time = Ticket.get_random_purchase_advantage_in_minutes().minutes
            if min_val is None or delta_time < min_val:
                min_val = delta_time
            if max_val is None or delta_time > max_val:
                max_val = delta_time
        self.assertLessEqual(Ticket.min_advance_of_purchase, min_val)
        self.assertLessEqual(max_val, Ticket.max_advance_of_purchase)
