import random
from datetime import datetime

from dateutil.relativedelta import relativedelta

from db_generation.parent_classes import ObjectWithCounter, AddableToDatabase
from db_generation.tables.seat import Seat
from db_generation.tables.show import Show
from db_generation.tables.cinema_user import CinemaUser
from db_generation.common import get_primary_key_from_nullable
from db_generation.types import INTEGER, FLOAT, TIMESTAMP


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

    def __init__(self, seat: Seat, show: Show, user: CinemaUser | None):
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
            show.show_date.value.year,
            show.show_date.value.month,
            show.show_date.value.day,
            show.start_hour.value,
            show.start_minute.value
        ) - relativedelta(minutes=random.randint(0, 48 * 60))
        self.purchase = TIMESTAMP(purchase_timestamp)
        self.fk_seat = seat.primary_key_value
        self.fk_show = show.primary_key_value
        self.fk_user = get_primary_key_from_nullable(user)

    @classmethod
    def get_all_objects(cls, seats: list[Seat], shows: list[Show], users: list[CinemaUser]):
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
