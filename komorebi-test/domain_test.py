import pprint
import unittest

import datetime

from injector import Injector
from komorebi.config import DBConfig
from komorebi.domain import DBService


class DomainTest(unittest.TestCase):

    # 1
    def test_save_user(self):
        inj = Injector(DBConfig())
        user = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'disintegration@cure.com',
            'username': 'bragod1982',
            'password': 'bragod1982',
            'gender': 'male',
            'birthday': datetime.date(1982, 1, 1)
        }
        dbs = inj.get(DBService)
        pprint.pprint(dbs.save_user(user))

    # 2
    def test_update_user(self):
        inj = Injector(DBConfig())
        user = {
            'id': 25685,
            'first_name': 'Robert',
            'last_name': 'Smith',
            'email': 'disintegration@cure.com',
            'username': 'robert_smith',
            'password': 'cold'
        }
        dbs = inj.get(DBService)
        pprint.pprint(dbs.update_user(user))

    # 4
    def test_delete_user(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.delete_user(25685)
        user = dbs.find_user(25685)
        self.assertIsNone(user)

    # 3
    def test_find_user(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        user = dbs.find_user(12)
        self.assertIsNotNone(user)
        pprint.pprint(user)
        self.assertTrue(isinstance(user, dict))

    # 8
    def test_create_club(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        club = {
            'name': 'The Cure',
            'description': 'Most gothic band'
        }
        club = dbs.create_club(club, 9)
        members = dbs.find_club_members(club['id'])
        self.assertTrue(9 in [m['id'] for m in members])
        pprint.pprint(club)
        pprint.pprint(members)

    # 9
    def test_update_club(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        club = {
            'id': 8,
            'name': 'The Cure',
            'description': 'Old school amazing gothic'
        }
        dbs.update_club(club)

    # 10
    def test_delete_club(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.delete_club(8)

    # 11
    def test_persist_chat_message(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        message = {
            'from_id': 45,
            'to_id': 34,
            'date': datetime.datetime.now(),
            'message': 'Hello!'
        }
        pprint.pprint(dbs.persist_message(message))

    # 5
    def test_find_user_movies(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        pprint.pprint(dbs.find_user_movies(12))

    # 6
    def test_find_user_clubs(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        pprint.pprint(dbs.find_user_clubs(12))

    # 13
    def test_delete_user_movie(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.delete_user_movie(12, 1)

    # 7
    def test_rate_movie(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.rate_movie(12, 1, {
            'status': 'watched',
            'rating': 7,
            'comment': 'Super!'
        })

    # 14
    def test_add_movie(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.add_user_movie(12, {
            "id": 89,
            "name": "The Hunger",
            "year": datetime.date(1982, 1, 1),
            "description": "Gothic",
            "tagline": "Gothic",
            "duration": "92",
            "genre": [
                'gothic'
            ],
            "country": [
                'UK'
            ],
            "picture": "none",
            "director": {
                'id': 87,
                'name': 'Master'
            },
            "composer": {
                'id': 34,
                'name': 'Master'
            },
            "producers": [
                {
                    'id': 98,
                    'name': 'Master'
                }
            ],
            "script": [
                {
                'id': 58,
                'name': 'Master'
                }
            ],
            "editor": {
                'id': 45,
                'name': 'Master'
            },
            "operator": {
                'id': 92,
                'name': 'Master'
            },
            "cast": [{
                'id': 102,
                'name': 'Master'
            }]
        })

    # 15
    def test_find_clubs(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        pprint.pprint(dbs.find_clubs('Batcave'))

    # 16
    def test_add_club_member(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.add_club_member({
            'user_id': 17,
            'club_id': 1,
            'user_role': 'visitor'
        })
        pprint.pprint(dbs.find_club_members(1))

    # 17
    def test_delete_club_member(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.delete_club_member(1, 17)
        pprint.pprint(dbs.find_club_members(1))
