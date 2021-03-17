import ply.lex as lex
import re


class NotalScanner(object):
    tokens = (
        "S_LESS_THAN_EQUAL",
        "S_GREATER_THAN_EQUAL",
        "S_NOT_EQUAL",
        "S_ASSIGNMENT",
        "S_UP_TO",
        "S_RETURN",
        "S_EQUAL",
        "S_PLUS_EQUAL",
        "S_MINUS_EQUAL",
        "S_TIMES_EQUAL",
        "S_DIVIDE_EQUAL",
        "S_PLUS",
        "S_MINUS",
        "S_TIMES",
        "S_DIVIDE",
        "S_LEFT_BRACKET",
        "S_RIGHT_BRACKET",
        "S_POWER",
        "S_LESS_THAN",
        "S_GREATER_THAN",
        "S_COLON",
        "S_SEMI_COLON",
        "S_DOUBLE_QUOTE",
        "S_SINGLE_QUOTE",
        "S_LEFT_SQUARE_BRACKET",
        "S_RIGHT_SQUARE_BRACKET",
        "S_LEFT_CURLY_BRACKET",
        "S_RIGHT_CURLY_BRACKET",
        "S_CONCATENATION",
        "S_ELEMENT_OF",
        "S_DOT",
        "RW_JUDUL",
        "RW_KAMUS",
        "RW_ALGORITMA",
        "RW_TYPE",
        "RW_CONSTANT",
        "RW_FUNCTION",
        "RW_PROCEDURE",
        "RW_PROGRAM",
        "RW_MODUL",
        "RW_AND",
        "RW_OR",
        "RW_XOR",
        "RW_EQ",
        "RW_NEQ",
        "RW_INPUT",
        "RW_OUTPUT",
        "RW_IF",
        "RW_THEN",
        "RW_ELSE",
        "RW_DIV",
        "RW_MOD",
        "RW_ABS",
        "RW_SUCC",
        "RW_PRED",
        "RW_SIN",
        "RW_COS",
        "RW_TAN",
        "RW_REPEAT",
        "RW_TIMES",
        "RW_UNTIL",
        "RW_WHILE",
        "RW_DO",
        "RW_TRAVERSAL",
        "RW_ITERATE",
        "RW_STOP",
        "RW_REAL",
        "RW_ARRAY",
        "RW_OF",
        "RW_SEQFILE",
        "RW_OPEN",
        "RW_READ",
        "RW_REWRITE",
        "RW_CLOSE",
        "RW_CHARACTER",
        "RW_INTEGER",
        "RW_BOOLEAN",
        "RW_STRING",
        "L_TRUE",
        "L_FALSE",
        "L_REAL_NUMBER",
        "L_INTEGER_NUMBER",
        "L_IDENTIFIER",
    )

    t_ignore = " \t"
    t_S_LESS_THAN_EQUAL = r"(\<\=|\≤)"
    t_S_GREATER_THAN_EQUAL = r"(\>\=|\≥)"
    t_S_NOT_EQUAL = r"(\!\=|\≠)"
    t_S_ASSIGNMENT = r"(\:\=|\<\-|\←)"
    t_S_UP_TO = r"\.{2}"
    t_S_RETURN = r"(\-\>|\→)"
    t_S_EQUAL = r"\="
    t_S_PLUS_EQUAL = r"\+\="
    t_S_MINUS_EQUAL = r"\-\="
    t_S_DIVIDE_EQUAL = r"\/\="
    t_S_PLUS = r"\+"
    t_S_MINUS = r"\-"
    t_S_TIMES = r"\*"
    t_S_DIVIDE = r"\/"
    t_S_LEFT_BRACKET = r"\("
    t_S_RIGHT_BRACKET = r"\)"
    t_S_POWER = r"\^"
    t_S_LESS_THAN = r"\<"
    t_S_GREATER_THAN = r"\>"
    t_S_COLON = r"\:"
    t_S_SEMI_COLON = r"\;"
    t_S_DOUBLE_QUOTE = r"\""
    t_S_SINGLE_QUOTE = r"\'"
    t_S_LEFT_SQUARE_BRACKET = r"\["
    t_S_RIGHT_SQUARE_BRACKET = r"\]"
    t_S_LEFT_CURLY_BRACKET = r"\{"
    t_S_RIGHT_CURLY_BRACKET = r"\}"
    t_S_CONCATENATION = r"\&"
    t_S_ELEMENT_OF = r"\∈"
    t_S_DOT = r"\."
    t_L_REAL_NUMBER = r"[+-]?([0-9]*[.])[0-9]*"
    t_L_INTEGER_NUMBER = r"([1-9][0-9]*)|([0])"

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def t_L_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"

        reserved = {
            "judul": "RW_JUDUL",
            "kamus": "RW_KAMUS",
            "algoritma": "RW_ALGORITMA",
            "type": "RW_TYPE",
            "constant": "RW_CONSTANT",
            "function": "RW_FUNCTION",
            "procedure": "RW_PROCEDURE",
            "program": "RW_PROGRAM",
            "modul": "RW_MODUL",
            "and": "RW_AND",
            "or": "RW_OR",
            "xor": "RW_XOR",
            "eq": "RW_EQ",
            "neq": "RW_NEQ",
            "input": "RW_INPUT",
            "output": "RW_OUTPUT",
            "if": "RW_IF",
            "then": "RW_THEN",
            "else": "RW_ELSE",
            "div": "RW_DIV",
            "mod": "RW_MOD",
            "abs": "RW_ABS",
            "succ": "RW_SUCC",
            "pred": "RW_PRED",
            "sin": "RW_SIN",
            "cos": "RW_COS",
            "tan": "RW_TAN",
            "repeat": "RW_REPEAT",
            "times": "RW_TIMES",
            "until": "RW_UNTIL",
            "while": "RW_WHILE",
            "do": "RW_DO",
            "traversal": "RW_TRAVERSAL",
            "iterate": "RW_ITERATE",
            "stop": "RW_STOP",
            "real": "RW_REAL",
            "array": "RW_ARRAY",
            "of": "RW_OF",
            "seqfile": "RW_SEQFILE",
            "open": "RW_OPEN",
            "read": "RW_READ",
            "rewrite": "RW_REWRITE",
            "close": "RW_CLOSE",
            "character": "RW_CHARACTER",
            "integer": "RW_INTEGER",
            "boolean": "RW_BOOLEAN",
            "string": "RW_STRING",
        }

        t.type = reserved.get(t.value.lower(), "L_IDENTIFIER")
        return t

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def scan_for_tokens(self, data):
        self.lexer.input(data)
        self.tokens = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            self.tokens.append(token)

    def get_tokens_in_json(self):
        tokens_in_json = [
            {
                "type": token.type,
                "value": token.value,
                "lineno": token.lineno,
                "lexpos": token.lexpos,
            }
            for token in self.tokens
        ]
        return tokens_in_json


if __name__ == "__main__":
    scanner = NotalScanner()
    scanner.scan_for_tokens("10 10.0")
    tokens = scanner.get_tokens_in_json()
    print(tokens)
