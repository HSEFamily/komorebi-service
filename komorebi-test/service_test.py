import unittest

from injector import Injector
from komorebi.config import DBConfig
from komorebi.domain import DBService, DBServiceImpl
from komorebi.emdb_search import Parser, ParserImpl


class ServiceTest(unittest.TestCase):

    def test_di(self):
        injector = Injector(DBConfig())
        self.assertTrue(isinstance(injector.get(DBService), DBServiceImpl))
        self.assertEqual(isinstance(injector.get(Parser), ParserImpl))
