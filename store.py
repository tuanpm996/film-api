import pandas as pd

auth_cache = None

def get_users():
    global auth_cache

    if auth_cache is None:
        # Load username and password from CSV file.
        df = pd.read_csv(
            './/auth.csv',
            sep='|',
            index_col=0,
            usecols=[1, 2, 3, 4],
            names=['username', 'password', 'age', 'gender']
        )
        auth_cache = df     # Cache username and password.
    return df

def exists_user(username):
    return (auth_cache['username'].isin([username])).any()

def df_height(df):
    return df.shape[0]

def add_user(username, password, user_info):
    global auth_cache

    age = user_info['age']
    gender = user_info['gender']

    # Reference safe guard.
    if auth_cache is None:
        auth_cache = pd.DataFrame(columns=['username', 'password', 'age', 'gender'])
    
    # Append item to cache.
    auth_cache = auth_cache.append(pd.DataFrame(
        data=[[username, password, age, gender]],
        columns=['username', 'password', 'age', 'gender'],
        index=[df_height(auth_cache)] # Increase the label by 1.
        ))

    # Save to file
    auth_cache.to_csv('.//auth.csv', sep='|')
    return

def get_user(user_id):
    global auth_cache

    if user_id in auth_cache.index:
        result = auth_cache.loc[0]
        
        if df_height(result) > 1:
            result.iloc[0].to_dict()
            return None

        return auth_cache.loc[0].to_dict()
    return None

def get_films():
    df = pd.read_csv(
        ".//items.csv",
        sep="|",
        usecols=[0, 1, 2, 4, 24],
        names=['id', 'name', 'date', 'link', 'image_url']
        )
    
    return df.to_json()