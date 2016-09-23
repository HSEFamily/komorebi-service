from injector import Module, singleton, provides
from ..domain import DBService, DBServiceImpl


class DBConfig(Module):

    @singleton
    @provides(DBService)
    def provide_db_service(self):
        return DBServiceImpl()

