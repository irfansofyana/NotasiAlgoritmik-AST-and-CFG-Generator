import ply.lex as lex
import re

class NotalScanner(object):
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
    