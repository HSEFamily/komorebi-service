import psycopg2

from injector import Module, singleton, provides
from jujuq.jujuq import SQLDialect
from ..domain import DBService, DBServiceImpl


class DBConfig(Module):

    @singleton
    @provides(DBService)
    def provide_db_service(self):
        return DBServiceImpl(
            dialect=SQLDialect.postgres,
            db='komorebi_db',
            host='95.85.24.237',
            user='komorebi_psql',
            password='komorebi95root',
            conn=psycopg2
        )

