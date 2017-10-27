import pandas as pd


auth_cache = null

def get_users():
    if auth_cache == null:
        # Load username and password from CSV file.
        df = pd.read_csv(
            ".//auth.csv",
            sep="|",        # TODO: Remove separators from username and password.
            usecols=[0, 1],
            names=['username', 'password']
        )
        auth_cache = df     # Cache username and password.
    return df


def get_films():
    df = pd.read_csv(
        ".//foo.csv",
        sep="|",
        usecols=[0, 1, 2, 4, 24],
        names=['id', 'name', 'date', 'link', 'image_url']
        )
    return df.to_json()
