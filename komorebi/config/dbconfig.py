import psycopg2
import psycopg2.extras

from injector import Module, singleton, provides
from jujuq.jujuq import SQLDialect, ConnFactory
from ..domain import DBService, DBServiceImpl


class DBConfig(Module):

    @singleton
    @provides(DBService)
    def provide_db_service(self):
        # return DBServiceImpl(
        #     dialect=SQLDialect.postgres,
        #     db='komorebi_db',
        #     host='95.85.24.237',
        #     user='komorebi_psql',
        #     password='komorebi95root',
        #     conn_f=CF()
        # )
        return DBServiceImpl(
            dialect=SQLDialect.postgres,
            db='komorebi',
            host='localhost',
            user='egdeveloper-psql',
            password='komorebi95root',
            conn_f=CF()
        )


class CF(ConnFactory):

    def connect(self, conn_s):
        return psycopg2.connect(conn_s)

    def cursor(self, conn):
        return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

