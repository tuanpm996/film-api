from flask import Flask, g, session, request, redirect
from flask_cors import CORS
import numpy as np
import json
import base64
import pandas as pd
import math
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
import sys

import store
import authenticate as auth
import response as res

app = Flask(__name__)
CORS(app)


# Yhat = np.zeros((1,1))
@app.before_first_request
def start_app():
    print("start", file=sys.stderr)
    global Yhat, items
    u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
    users = pd.read_csv('data/u.user', sep='|', names=u_cols,
                        encoding='latin-1')

    n_users = users.shape[0]
    print('Number of users:', n_users, file=sys.stderr)
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

    ratings_base = pd.read_csv(
        'data/ua.base', sep='\t', names=r_cols, encoding='latin-1')
    ratings_test = pd.read_csv(
        'data/ua.test', sep='\t', names=r_cols, encoding='latin-1')

    rate_train = ratings_base.as_matrix()
    rate_test = ratings_test.as_matrix()

    print('Number of traing rates:', rate_train.shape[0], file=sys.stderr)
    print('Number of test rates:', rate_test.shape[0], file=sys.stderr)

    i_cols = [
        'id', 'name', 'release date', 'video release date', 'IMDb URL',
        'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy',
        'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
        'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
        'Thriller', 'War', 'Western', 'image_url'
    ]

    items = pd.read_csv('data/items.csv', sep='|', names=i_cols,
                        encoding='latin-1')

    n_items = items.shape[0]
    print('Number of items:', n_items, file=sys.stderr)

    X0 = items.as_matrix()
    X_train_counts = X0[:, 5:23]

    transformer = TfidfTransformer(smooth_idf=True, norm='l2')
    tfidf = transformer.fit_transform(X_train_counts.tolist()).toarray()

    Yhat = np.zeros((n_items, n_users))

    for n in range(n_users):
        ids, scores = get_items_rated_by_user(rate_train, n)
        Xhat = tfidf[ids, :]
        clf = SVC(kernel='rbf', C=7.4)
        svm_model_linear = clf.fit(Xhat, scores)
        Yhat[:, n] = svm_model_linear.predict(tfidf[:, :])
    print("Done", file=sys.stderr)


@app.route('/user', methods=['GET'])
def recommend():
    global Yhat, items

    id = request.args.get('id')
    top_6 = np.argpartition(Yhat[:, int(id)], -6)[-6:]

    return items.ix[top_6].to_json(orient='records')


def get_items_rated_by_user(rate_matrix, user_id):
    """
    in each line of rate_matrix, we have infor: user_id, item_id, rating (scores), time_stamp
    we care about the first three values
    return (item_ids, scores) rated by user user_id
    """
    y = rate_matrix[:, 0]  # all users
    # item indices rated by user_id
    # we need to +1 to user_id since in the rate_matrix, id starts from 1
    # while index in python starts from 0
    ids = np.where(y == user_id + 1)[0]
    item_ids = rate_matrix[ids, 1] - 1  # index starts from 0
    scores = rate_matrix[ids, 2]
    return (item_ids, scores)


def evaluate(Yhat, rates):
    se = 0
    cnt = 0
    for n in range(n_users):
        ids, scores_truth = get_items_rated_by_user(rates, n)
        scores_pred = Yhat[ids, n]
        e = scores_truth - scores_pred
        se += (e * e).sum(axis=0)
        cnt += e.size
    return math.sqrt(se / cnt)


@app.route('/signup', methods=['POST'])
def signup():
    print(request.get_json())
    data = request.get_json()

    # Store user information
    # TODO: Remove separators from username and password.
    username = data['username']
    password = data['password']
    age = data['age']
    gender = data['gender']

    print('{0} {1} {2} {3}'.format(username, password, age, gender))

    user_info = {}
    user_info['age'] = age
    user_info['gender'] = gender

    return auth.sign_up(username, password, user_info)


@app.route('/films', methods=['GET', 'POST'])
def get_films():
    return store.get_films()  \
        .loc[3:8]             \
        .to_json(orient='records')

@app.route('/film/<id>', methods=['GET', 'POST'])
def get_film(id):
    record = store.get_film_by_id(int(id))

    return json.dumps(record)

@app.route('/suggest', methods=['GET'])
def suggest_empty():
    films = store.get_films()

    return films.loc[3:8] \
        .to_json(orient='records')

@app.route('/suggest/<raw_string>', methods=['GET'])
def suggest(raw_string):
    decoded_string = base64.b64decode(raw_string).decode('UTF-8')

    films = store.get_films()

    return films.loc[films['name'].str          \
        .contains(decoded_string, na=False)]    \
        .to_json(orient='records')


@app.route('/search/<raw_string>', methods=['GET'])
def search(raw_string):
    decoded_string = base64.b64decode(raw_string).decode('UTF-8')

    films = store.get_films()

    return films.loc[
            films['name'].str
            .contains(decoded_string, na=False)
        ]           \
        .to_json(orient='records')
