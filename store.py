import pandas as pd

def get_films():
    data = pd.read_csv(
        ".//foo.csv",
        sep="|",
        usecols=[0, 1, 2, 4, 24],
        names=['id', 'name', 'date', 'link', 'image_url']
        )

    return data.to_json()