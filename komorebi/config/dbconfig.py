from injector import Module, singleton, provides
from jujuq.jujuq import SQLDialect
from ..domain import DBService, DBServiceImpl


class DBConfig(Module):

    @singleton
    @provides(DBService)
    def provide_db_service(self):
        return DBServiceImpl(
            dialect=SQLDialect.postgres,
            db='komorebi',
            user='komorebi-psql',
            password='komorebi-password',
            conn='psycopg2'
        )

