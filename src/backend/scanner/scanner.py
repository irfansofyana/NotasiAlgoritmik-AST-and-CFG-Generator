import ply.lex as lex
import re
class NotalScanner(object):
    tokens = (
        'S_LESS_THAN_EQUAL',
        'S_GREATER_THAN_EQUAL',
        'S_NOT_EQUAL',
        'S_ASSIGNMENT',
        'S_UP_TO',
        'S_RETURN',
        'S_EQUAL',
        'S_PLUS_EQUAL',
        'S_MINUS_EQUAL',
        'S_TIMES_EQUAL',
        'S_DIVIDE_EQUAL',
        'S_PLUS',
        'S_MINUS',
        'S_TIMES',
        'S_DIVIDE',
        'S_LEFT_BRACKET',
        'S_RIGHT_BRACKET',
        'S_POWER',
        'S_LESS_THAN',
        'S_GREATER_THAN',
        'S_COLON',
        'S_SEMI_COLON',
        'S_DOUBLE_QUOTE',
        'S_SINGLE_QUOTE',
        'S_LEFT_SQUARE_BRACKET',
        'S_RIGHT_SQUARE_BRACKET',
        'S_LEFT_CURLY_BRACKET',
        'S_RIGHT_CURLY_BRACKET',
        'S_CONCATENATION',
        'S_ELEMENT_OF',
        'S_DOT'
    )

    t_S_LESS_THAN_EQUAL             = r'(\<\=|\≤)'
    t_S_GREATER_THAN_EQUAL          = r'(\>\=|\≥)'
    t_S_NOT_EQUAL                   = r'(\!\=|\≠)'
    t_S_ASSIGNMENT                  = r'(\:\=|\<\-|\←)'
    t_S_UP_TO                       = r'\.{2}'
    t_S_RETURN                      = r'(\-\>|\→)'
    t_S_EQUAL                       = r'\='
    t_S_PLUS_EQUAL                  = r'\+\='
    t_S_MINUS_EQUAL                 = r'\-\='
    t_S_DIVIDE_EQUAL                = r'\/\='
    t_S_PLUS                        = r'\+'
    t_S_MINUS                       = r'\-'
    t_S_TIMES                       = r'\*'
    t_S_DIVIDE                      = r'\/'
    t_S_LEFT_BRACKET                = r'\('
    t_S_RIGHT_BRACKET               = r'\)'
    t_S_POWER                       = r'\^'
    t_S_LESS_THAN                   = r'\<'
    t_S_GREATER_THAN                = r'\>'
    t_S_COLON                       = r'\:'
    t_S_SEMI_COLON                  = r'\;'
    t_S_DOUBLE_QUOTE                = r'\"' 
    t_S_SINGLE_QUOTE                = r"\'"
    t_S_LEFT_SQUARE_BRACKET         = r'\['
    t_S_RIGHT_SQUARE_BRACKET        = r'\]'
    t_S_LEFT_CURLY_BRACKET          = r'\{'
    t_S_RIGHT_CURLY_BRACKET         = r'\}'
    t_S_CONCATENATION               = r'\&'
    t_S_ELEMENT_OF                  = r'\∈'
    t_S_DOT                         = r'\.'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
        
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    def scan(self, data):
        self.lexer.input(data)
        while True:
            token = self.lexer.token()
            if not token:
                break
            print(token)

if __name__ == "__main__":
    scanner = NotalScanner()
    scanner.build()
    scanner.scan('(+-')