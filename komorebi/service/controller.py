from injector import Injector

from ..config import DBConfig
from ..domain import DBService

injector = Injector(DBConfig())
dbservice = injector.get(DBService)


def save_user(user):
    dbservice.save_user(user)


def update_user(user):
    dbservice.update_user(user)


def find_user(user_id):
    return dbservice.find_user(user_id)


def delete_user(user_id):
    dbservice.delete_user(user_id)


def create_club(club, owner_id):
    dbservice.create_club(club, owner_id)


def update_club(club):
    dbservice.update_club(club)


def delete_club(club_id):
    dbservice.delete_club(club_id)


def find_club_members(club_id):
    return dbservice.find_club_members(club_id)


def find_user_clubs(user_id):
    return dbservice.find_user_clubs(user_id)


def add_user_movie(user_id, movie):
    dbservice.add_user_movie(user_id, movie)


def find_user_movies(user_id):
    return dbservice.find_user_movies(user_id)


def rate_movie(user_id, movie):
    dbservice.rate_movie(user_id, movie)


def delete_user_movie(user_id, movie_id):
    dbservice.delete_user_movie(user_id, movie_id)


def persist_message(message):
    return dbservice.persist_message(message)
