import random
import unittest

from db_generation.parent_classes import AddableToDatabase, ObjectWithCounter
from db_generation.types import INTEGER, CHAR


class Language(AddableToDatabase, ObjectWithCounter):
    language_names = ["polish", "english", "german", "czech", "slovene"]
    weights = [5, 10, 1, 1, 1]

    def __init__(self, language_name: str):
        self.id_language = INTEGER(Language.next())
        self.language_name = CHAR(language_name)

    @classmethod
    def get_all_objects(cls):
        return [Language(name) for name in cls.language_names]

    @property
    def primary_key_value(self):
        return self.id_language

    @classmethod
    def get_random_language(cls, languages):
        return random.choices(languages, weights=Language.weights)[0]


class TestLanguage(unittest.TestCase):
    def test_get_all_objects(self):
        languages = Language.get_all_objects()
        self.assertEqual(len(languages), 5)
        ids = [l.primary_key_value for l in languages]
        self.assertEqual(len(ids), len(set(ids)))

    def test_correct_number_of_weights(self):
        self.assertEqual(len(Language.language_names), len(Language.weights))

    def test_weights_work(self):
        languages = Language.get_all_objects()
        random_languages = [Language.get_random_language(languages) for x in range(100)]

        language_count_dict = {}
        for language in random_languages:
            language_count_dict[language] = language_count_dict.get(language, 0) + 1

        counts = language_count_dict.values()
        counts = sorted(counts, reverse=True)
        self.assertGreater(sum(counts[:2]), sum(counts[2:]))
