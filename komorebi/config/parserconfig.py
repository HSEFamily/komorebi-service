from injector import Module, singleton, provides
from komorebi.emdb_search import Parser, ParserImpl


class ParserConfig(Module):

    @singleton
    @provides(Parser)
    def provide_parse(self):
        return ParserImpl()

