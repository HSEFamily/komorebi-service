import pprint
import unittest

import datetime

from injector import Injector
from komorebi.config import DBConfig
from komorebi.domain import DBService


class DomainTest(unittest.TestCase):

    def test_save_user(self):
        inj = Injector(DBConfig())
        user = {
            'first_name': 'Robert',
            'last_name': 'Smith',
            'email': 'disintegration@cure.com',
            'user_name': 'robert_smith',
            'password': 'lullaby'
        }
        dbs = inj.get(DBService)
        pprint.pprint(dbs.save_user(user))

    def test_update_user(self):
        inj = Injector(DBConfig())
        user = {
            'id': 1,
            'first_name': 'Robert',
            'last_name': 'Smith',
            'email': 'disintegration@cure.com',
            'user_name': 'robert_smith',
            'password': 'cold'
        }
        dbs = inj.get(DBService)
        pprint.pprint(dbs.update_user(user))

    def test_delete_user(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.delete_user(1)
        user = dbs.find_user(1)
        self.assertIsNone(user)

    def test_find_user(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        user = dbs.find_user(1)
        self.assertIsNotNone(user)
        pprint.pprint(user)

    def test_create_club(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        club = {
            'name': 'The Cure',
            'description': 'Most gothic band'
        }
        dbs.create_club(club, 2)
        members = dbs.find_club_members(club['id'])
        self.assertTrue(2 in [m['id'] for m in members])
        pprint.pprint(club)
        pprint.pprint(members)

    def test_update_club(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        club = {
            'id': 16,
            'name': 'The Cure',
            'description': 'Old school gothic'
        }
        dbs.update_club(club)

    def test_delete_club(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        dbs.delete_club(16)

    def test_persist_chat_message(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        message = {
            'from_id': 2,
            'to_id': 2,
            'date': datetime.datetime.now(),
            'message': 'Hello!'
        }
        pprint.pprint(dbs.persist_message(message))

