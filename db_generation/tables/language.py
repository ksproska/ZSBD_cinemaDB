from db_generation.parent_classes import AddableToDatabase, ObjectWithCounter
from db_generation.types import INTEGER, CHAR


class Language(AddableToDatabase, ObjectWithCounter):
    def __init__(self, language_name: str):
        self.id_language = INTEGER(Language.next())
        self.language_name = CHAR(language_name)

    @classmethod
    def get_all_objects(cls):
        language_names = ["polish", "english", "german", "czech", "slovene"]
        all_objects = []
        for name in language_names:
            all_objects.append(Language(name))
        return all_objects

    @property
    def primary_key_value(self):
        return self.id_language
