from injector import Module, singleton, provides


class ParserConfig(Module):

    @singleton
    def provide_parse(self):
        pass

