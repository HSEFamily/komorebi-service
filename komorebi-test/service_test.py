import unittest

import psycopg2

from injector import Injector
from jujuq import Query, SQLDialect
from komorebi.config import DBConfig
from komorebi.domain import DBService, DBServiceImpl


class ServiceTest(unittest.TestCase):

    def test_di(self):
        injector = Injector(DBConfig())
        self.assertTrue(isinstance(injector.get(DBService), DBServiceImpl))

    def test_db_connection(self):
        q = Query.construct(dialect=SQLDialect.postgres,
                            tb='users',
                            db='komorebi_db',
                            host='95.85.24.237',
                            user='komorebi_psql',
                            password='komorebi95root',
                            conn=psycopg2
                            )
        print(q.table('users').raw('SELECT 1 + 1').fetch_one())

