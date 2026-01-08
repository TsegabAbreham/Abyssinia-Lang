from node import * 

class ImportParser:
    def parse_import(self):
        self.eat("IMPORT")
        path = self.eat("STRING")
        alias = None
        if self.current()[0] == "AS":
            self.eat("AS")
            alias = self.eat("IDENTIFIER")
        return ImportStatement(path, alias)