from db_generation.types import INTEGER


def get_primary_key_from_nullable(x):
    return INTEGER(None) if x is None else x.primary_key_value
