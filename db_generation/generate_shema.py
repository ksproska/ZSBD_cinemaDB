from db_generation.tables_with_foreign_keys import Seat
from db_generation.tables_without_foreign_keys import AgeRestriction, Language, User, Room

age_restriction = AgeRestriction.get_all_objects()[0]
language = Language.get_all_objects()[0]
user = User.get_all_objects(1)[0]
room = Room.get_all_objects(1)[0]
seat = Seat.get_all_objects_single_room(room)[0]

all_tables = [
    AgeRestriction.get_all_objects()[0],
    Language.get_all_objects()[0],
    User.get_all_objects(1)[0],
    Room.get_all_objects(1)[0],
    Seat.get_all_objects_single_room(room)[0]
]

with open("db_init.sql", "w", encoding="utf8") as f:
    for table in all_tables:
        f.write(table.create_table())
