import ply.lex as lex

class TMPScanner(object):
    tokens = (
        "S_LESS_THAN_EQUAL",
        "S_GREATER_THAN_EQUAL",
        "S_NOT_EQUAL",
        "S_EQUAL",
        "S_PLUS",
        "S_MINUS",
        "S_TIMES",
        "S_DIVIDE",
        "S_LEFT_BRACKET",
        "S_RIGHT_BRACKET",
        "S_LESS_THAN",
        "S_GREATER_THAN",
        "S_ELEMENT_OF",
        "RW_AND",
        "RW_OR",
        "RW_XOR",
        "RW_NOT",
        "RW_EQ",
        "RW_NEQ",
        "RW_DIV",
        "RW_MOD",
        "L_BOOLEAN_TRUE",
        "L_BOOLEAN_FALSE",
        "L_REAL_NUMBER",
        "L_INTEGER_NUMBER",
        "IDENTIFIER",
        "L_STRING",
        "L_CHARACTER",
    )

    t_ignore = " \t"
    t_S_LESS_THAN_EQUAL = r"(\<\=|\≤)"
    t_S_GREATER_THAN_EQUAL = r"(\>\=|\≥)"
    t_S_NOT_EQUAL = r"(\!\=|\≠)"
    t_S_EQUAL = r"\="
    t_S_PLUS = r"\+"
    t_S_MINUS = r"\-"
    t_S_TIMES = r"\*"
    t_S_DIVIDE = r"\/"
    t_S_LEFT_BRACKET = r"\("
    t_S_RIGHT_BRACKET = r"\)"
    t_S_LESS_THAN = r"\<"
    t_S_GREATER_THAN = r"\>"
    t_S_ELEMENT_OF = r"\∈"

    # states = (
    #     ('COMMENT', 'exclusive'),
    # )
    #
    # def t_COMMENT(self, t):
    #     r'\{'
    #     t.lexer.code_start = t.lexer.lexpos
    #     t.lexer.level = 1
    #     t.lexer.begin('COMMENT')
    #
    # def t_COMMENT_L_BRACE(self, t):
    #     r'\{'
    #     t.lexer.level += 1
    #
    # def t_COMMENT_R_BRACE(self, t):
    #     r'\}'
    #     t.lexer.level -= 1
    #
    #     if t.lexer.level == 0:
    #         t.type = 'COMMENT'
    #         t.value = t.lexer.lexdata[t.lexer.code_start + 1: t.lexer.lexpos]
    #         t.lexer.lineno += t.value.count('\n')
    #         t.lexer.begin('INITIAL')
    #
    #         return t
    #
    # def t_COMMENT_NONSPACE(self, t):
    #     r'[^\s\{\}\'\"]+'
    #
    # t_COMMENT_ignore = " \t\n"
    #
    # def t_COMMENT_error(self, t):
    #     t.lexer.skip(1)

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(
            f"Illegal character '{t.value[0]}' at line {t.lineno} column {self.find_column_position(t)}"
        )
        t.lexer.skip(1)

    def t_IDENTIFIER(self, t):
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
            "not": "RW_NOT",
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
            "true": "L_BOOLEAN_TRUE",
            "false": "L_BOOLEAN_FALSE"
        }

        t.type = reserved.get(str(t.value).lower(), "IDENTIFIER")

        if t.type == "L_BOOLEAN":
            t.value = True if str(t.value).lower() == "true" else False

        return t

    def t_L_REAL_NUMBER(self, t):
        r"[-]?([0-9]*[.])[0-9]*"
        t.value = float(t.value)
        return t

    def t_L_INTEGER_NUMBER(self, t):
        r"[-]?([1-9][0-9]*)|([0])"
        t.value = int(t.value)
        return t

    def t_L_STRING(self, t):
        r'"[^"]*"'
        t.type = "L_STRING"
        return t

    def t_L_CHARACTER(self, t):
        r"'[^']{1}'"
        t.type = "L_CHARACTER"
        return t

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def find_column_position(self, token):
        start_line = self.source.rfind("\n", 0, token.lexpos) + 1
        return token.lexpos - start_line + 1

    def scan_for_tokens(self, source):
        self.source = source
        self.lexer.input(source)
        self.tokens = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            else:
                token.lexpos = (token.lexpos, self.find_column_position(token))
            self.tokens.append(token)

    def get_tokens_in_json(self):
        tokens_in_json = [
            {
                "type": token.type,
                "value": token.value,
                "line_position": token.lineno,
                "lex_position": token.lexpos[0],
                "column_position": token.lexpos[1],
            }
            for token in self.tokens
        ]
        return tokens_in_json