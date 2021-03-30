import ply.yacc as yacc
from src.backend.scanner.notal_scanner import NotalScanner

class NotalParser(object):
    tokens = NotalScanner.tokens

    # grammar declaration here
    # TBA
    # end of grammar declaration

    def p_error(self, p):
        print("Syntax error on input!")

    def __init__(self):
        self.lexer = NotalScanner()
        self.parser = yacc.yacc(module=self)

    def parse(self, source):
        self.source = source
        return self.parser.parse(source)