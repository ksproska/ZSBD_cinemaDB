import pandas as pd


def get_movies_csv(path="./"):
    return pd.read_csv(path + 'regex_imdb.csv')
