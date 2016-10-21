from injector import Injector

from config import DBConfig
from domain import DBService

injector = Injector(DBConfig())
dbservice = injector.get(DBService)

# User methods
def save_user(user):
    dbservice.save_user(user)

def find_user(user_id):
    return dbservice.find_user(user_id)

def update_user(id, user_dict):
    user_dict['id'] = id
    dbservice.update_user(user_dict)

def delete_user(user_id):
    dbservice.delete_user(user_id)

def watch_movie(user_id, movie_id):
    dbservice.add_user_movie(user_id, movie_id)

def unwatch_movie(user_id, movie_id):
    dbservice.delete_user_movie(user_id, movie_id)

def set_review(user_id, movie_id, review_dict):
    dbservice.rate_movie(user_id, movie_id, movie_rate)

def get_user_movies(user_id):
    return dbservice.find_user_movies(user_id)

def create_club(user_id, club_dict):
    dbservice.create_club(club_dict, user_id)

def get_user_clubs(user_id):
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
