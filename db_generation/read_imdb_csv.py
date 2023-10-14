from os.path import exists

import pandas as pd


def get_movies_csv():
    filename = 'regex_imdb.csv'
    filepath = f"./{filename}"
    if exists(filepath):
        return pd.read_csv(filepath)
    return pd.read_csv(f"./../{filename}")
