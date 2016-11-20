import hashlib

from injector import Injector

from config import DBConfig
from domain import DBService

injector = Injector(DBConfig())
dbservice = injector.get(DBService)


# User methods
def save_user(user):
    dbservice.save_user(user)


def auth_user(username, password):
    user = dbservice.find_user_by_username(username)
    if user['password'] == password:
        # Generate and return token
        return generate_token(username, password)
    else:
        # Authentication failed; no token
        return ''


def find_user(token, user_id):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        return user


def update_user(token, id, user_dict):
    user_dict['id'] = id
    username = user_dict['username']
    password = user_dict['password']
    real_token = generate_token(username, password)
    if token == real_token:
        dbservice.update_user(user_dict)


def delete_user(token, user_id):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        dbservice.delete_user(user_id)


def watch_movie(token, user_id, movie_id):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        dbservice.add_user_movie(user_id, movie_id)


def unwatch_movie(token, user_id, movie_id):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        dbservice.delete_user_movie(user_id, movie_id)


def set_review(token, user_id, movie_id, review_dict):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        dbservice.rate_movie(user_id, movie_id, movie_rate)


def get_user_movies(token, user_id):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        return dbservice.find_user_movies(user_id)


def create_club(token, user_id, club_dict):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        dbservice.create_club(club_dict, user_id)


def get_user_clubs(token, user_id):
    user = dbservice.find_user(user_id)
    username = user['username']
    password = user['password']
    real_token = generate_token(username, password)
    if token == real_token:
        return dbservice.find_user_clubs(user_id)


# Club methods
def update_club(id, club_dict):
    club_dict['id'] = id
    dbservice.update_club(club_dict)


def delete_club(id):
    dbservice.delete_user(id)


def add_club_member(club_id, member_id):
    dbservice.add_club_member(club_id, member_id)


def delete_club_member(club_id, member_id):
    dbservice.delete_club_member(club_id, member_id)


def get_club_members(id):
    return dbservice.find_club_members(id)


# Clubs methods
def find_clubs(sq):
    return dbservice.find_clubs(sq)


# Movies methods
def find_movies(sq):
    return dbservice.find_movies(sq)


def persist_message(message):
    # The fuck is that? oO
    pass


# Auth methods
def generate_token(username, password):
    h = hashlib.sha256()
    salt = 'correct horse battery staple'
    h.update(username.encode('utf-8'))
    h.update(salt.encode('utf-8'))
    h.update(password.encode('utf-8'))
    return h.hexdigest()
