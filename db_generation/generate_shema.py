from db_generation.tables_without_foreign_keys import AgeRestriction, Language, User, Room

age_restriction = AgeRestriction.get_all_objects()[0]
language = Language.get_all_objects()[0]
user = User.get_all_objects(1)[0]
room = Room.get_all_objects(1)[0]

with open("db_init.sql", "w", encoding="utf8") as f:
    f.write(age_restriction.create_table())
    f.write(language.create_table())
    f.write(user.create_table())
    f.write(room.create_table())
