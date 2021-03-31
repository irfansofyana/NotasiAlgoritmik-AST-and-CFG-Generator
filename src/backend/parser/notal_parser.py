import ply.yacc as yacc
from src.backend.scanner.notal_scanner import NotalScanner

class NotalParser(object):
    tokens = NotalScanner.tokens

    # grammar declaration here
    def p_relational_op(self, p):
        """relational_op: S_EQUAL
                | S_NOT_EQUAL
                | S_LESS_THAN_EQUAL
                | S_GREATER_THAN_REQUAL
                | S_LESS_THAN
                | S_GREATER_THAN
                | S_ELEMENT_OF
        """

    def p_multiplicative_op(self, p):
        """multiplicative_op: S_TIMES
                            | S_DIVIDE
                            | RW_DIV
                            | RW_MOD
                            | RW_AND
        """

    def p_additive_op(self, p):
        """additive_op: S_PLUS
                    | S_MINUS
                    | RW_OR
                    | RW_XOR
        """

    def p_unary_op(self, p):
        """unary_op: S_PLUS
            |   S_MINUS
            |   RW_NOT
        """

    def p_expression(self, p):
        """expression: expression relational_op additive_expression
                    |   additive_expression
        """

    # end of grammar declaration

    def p_error(self, p):
        print("Syntax error on input!")

    def __init__(self):
        self.lexer = NotalScanner()
        self.parser = yacc.yacc(module=self)

    def parse(self, source):
        self.source = source
        return self.parser.parse(source)