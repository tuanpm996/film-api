import pandas as pd

auth_cache = None

def get_users():
    global auth_cache

    if auth_cache is None:
        # Load username and password from CSV file.
        df = pd.read_csv(
            ".//auth.csv",
            sep="|",        # TODO: Remove separators from username and password.
            usecols=[0, 1],
            names=['username', 'password']
        )
        auth_cache = df     # Cache username and password.
    return df

def exists_user(username):
    if auth_cache.loc[auth_cache['username'] == username].shape[0] > 0:
        return true
    return false


def df_height(df):
    return df.shape[0]

def add_user(username, password):
    global auth_cache

    # Reference safe guard.
    if auth_cache is None:
        auth_cache = pd.DataFrame(columns=['username', 'password'])
    
    # Append item to cache.
    auth_cache = auth_cache.append(pd.DataFrame(
        data=[[username, password]],
        columns=['username', 'password']
        index=[df_height(auth_cache)] # Increase the label by 1.
        ))

    # Save to file
    auth_cache.to_csv('.//auth.csv')
    return


def get_films():
    df = pd.read_csv(
        ".//foo.csv",
        sep="|",
        usecols=[0, 1, 2, 4, 24],
        names=['id', 'name', 'date', 'link', 'image_url']
        )
    
    return df.to_json()