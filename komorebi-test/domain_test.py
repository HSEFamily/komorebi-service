import pprint
import unittest

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
            'id': 2,
            'first_name': 'Robert',
            'last_name': 'Smith',
            'email': 'disintegration@cure.com',
            'user_name': 'robert_smith',
            'password': 'cold'
        }
        dbs = inj.get(DBService)
        pprint.pprint(dbs.update_user(user))

    def test_find_user(self):
        inj = Injector(DBConfig())
        dbs = inj.get(DBService)
        user = dbs.find_user(2)
        self.assertIsNotNone(user)
        pprint.pprint(user)


