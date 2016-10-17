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


def persist_message(message):
    # The fuck is that? oO
    pass
