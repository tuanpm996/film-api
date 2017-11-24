import pandas as pd

auth_cache = pd.read_csv(
    './/auth.csv',
    sep='|',
    index_col=0,
    usecols=[0, 1, 2, 3, 4],
)

def get_users():
    global auth_cache
    
    return auth_cache

def exists_user(username):
    global auth_cache

    return (auth_cache['username'].isin([username])).any()

def df_height(df):
    return df.shape[0]

def add_user(username, password, user_info):
    global auth_cache

    age = user_info['age']
    gender = user_info['gender']

    # Append item to cache.
    auth_cache = auth_cache.append(pd.DataFrame(
        data=[[username, password, age, gender]],
        columns=['username', 'password', 'age', 'gender'],
        index=[df_height(auth_cache) + 1] # Increase the label by 1.
        ))

    # Save to file
    auth_cache.to_csv('.//auth.csv', sep='|', encoding='utf-8')
    return

def get_user(user_id):
    global auth_cache
    has_id = auth_cache.index.isin([user_id])   # Vector contains boolean values.

    if has_id.any():
        user_info = auth_cache.loc[has_id]
        
        print(user_info)

        return user_info.iloc[0].to_dict()
    return None

def get_films():
    df = pd.read_csv(
        './/items.csv',
        sep="|",
        usecols=[0, 1, 2, 4, 24],
        names=['id', 'name', 'date', 'link', 'image_url']
        )

    return df.loc[3:8].to_json(orient='records')


def get_film_by_id(id):
    df = pd.read_csv(
        './/items.csv',
        sep="|",
        usecols=[0, 1, 2, 4, 24],
        names=['id', 'name', 'date', 'link', 'image_url']
    )

    return df.loc[df['id'] == id].to_dict(orient='records')[0]
