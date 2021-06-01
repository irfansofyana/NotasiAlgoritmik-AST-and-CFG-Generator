import ply.lex as lex
import copy


class NotalScanner(object):
    tokens = (
        "S_LESS_THAN_EQUAL",
        "S_GREATER_THAN_EQUAL",
        "S_NOT_EQUAL",
        "S_ASSIGNMENT",
        "S_UP_TO",
        "S_RETURN",
        "S_EQUAL",
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
        "S_COMMA",
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
        "RW_LOKAL",
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
        "RW_NOT",
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
        "RW_DEPEND",
        "RW_ON",
        "RW_REALTOINTEGER",
        "RW_INTEGERTOREAL",
        "RW_AWAL",
        "RW_AKHIR",
        "RW_FIRSTCHAR",
        "RW_LASTCHAR",
        "RW_LONG",
        "RW_ISKOSONG",
        "L_BOOLEAN_TRUE",
        "L_BOOLEAN_FALSE",
        "L_REAL_NUMBER",
        "L_INTEGER_NUMBER",
        "IDENTIFIER",
        "L_STRING",
        "L_CHARACTER",
        "L_NIL",
        "COMMENT",
        "WHITESPACE",
        "INDENT",
        "DEDENT"
    )

    t_ignore = " \t"
    t_S_LESS_THAN_EQUAL = r"(\<\=|\≤)"
    t_S_GREATER_THAN_EQUAL = r"(\>\=|\≥)"
    t_S_NOT_EQUAL = r"(\!\=|\≠)"
    t_S_ASSIGNMENT = r"(\:\=|\<\-|\←)"
    t_S_UP_TO = r"\.{2}"
    t_S_RETURN = r"(\-\>|\→)"
    t_S_EQUAL = r"\="
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
    t_S_COMMA = r"\,"
    t_S_DOUBLE_QUOTE = r"\""
    t_S_SINGLE_QUOTE = r"\'"
    t_S_LEFT_SQUARE_BRACKET = r"\["
    t_S_RIGHT_SQUARE_BRACKET = r"\]"
    t_S_LEFT_CURLY_BRACKET = r"\{"
    t_S_RIGHT_CURLY_BRACKET = r"\}"
    t_S_CONCATENATION = r"\&"
    t_S_ELEMENT_OF = r"\∈"
    t_S_DOT = r"\."

    states = (
        ('COMMENT', 'exclusive'),
    )

    def t_COMMENT(self, t):
        r'\{'
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.level = 1
        t.lexer.begin('COMMENT')

    def t_COMMENT_L_BRACE(self, t):
        r'\{'
        t.lexer.level += 1

    def t_COMMENT_R_BRACE(self, t):
        r'\}'
        t.lexer.level -= 1

        if t.lexer.level == 0:
            t.type = 'COMMENT'
            t.value = t.lexer.lexdata[t.lexer.code_start + 1: t.lexer.lexpos]
            t.lexer.lineno += t.value.count('\n')
            t.lexer.begin('INITIAL')

            # return t

    def t_COMMENT_NONSPACE(self, t):
        r'[^\s\{\}\'\"]+'

    t_COMMENT_ignore = " \t\n"

    def t_COMMENT_error(self, t):
        t.lexer.skip(1)

    def t_WHITESPACE(self, t):
        r"\n[ ]*"
        t.lexer.lineno += 1
        t.type = 'WHITESPACE'
        return t

    def t_error(self, t):
        print(
            f"Illegal character '{t.value[0]}' at line {t.lineno}"
        )
        t.lexer.skip(1)

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"

        reserved = {
            "judul": "RW_JUDUL",
            "kamus": "RW_KAMUS",
            "lokal": "RW_LOKAL",
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
            "depend": "RW_DEPEND",
            "on": "RW_ON",
            "realtointeger": "RW_REALTOINTEGER",
            "inttoreal": "RW_INTEGERTOREAL",
            "awal": "RW_AWAL",
            "akhir": "RW_AKHIR",
            "firstchar": "RW_FIRSTCHAR",
            "lastchar": "RW_LASTCHAR",
            "long": "RW_LONG",
            "iskosong": "RW_ISKOSONG",
            "true": "L_BOOLEAN_TRUE",
            "false": "L_BOOLEAN_FALSE",
            "nil": "L_NIL",
        }

        t.type = reserved.get(str(t.value).lower(), "IDENTIFIER")

        if t.type == "L_BOOLEAN":
            t.value = True if str(t.value).lower() == "true" else False

        return t

    def t_L_REAL_NUMBER(self, t):
        r"([0-9]*[.])[0-9]+"
        t.value = float(t.value)
        return t

    def t_L_INTEGER_NUMBER(self, t):
        r"([1-9][0-9]*)|([0])"
        t.value = int(t.value)
        return t

    def t_L_STRING(self, t):
        r'"[^\n"]*"'
        t.type = "L_STRING"
        return t

    def t_L_CHARACTER(self, t):
        r"'[^']{1}'"
        t.type = "L_CHARACTER"
        return t

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    def token(self):
        return self.lexer.token()


class IndentLexer(object):
    """
    A second lexing stage that interprets WHITESPACE
    Manages Off-Side Rule for indentation
    """

    def __init__(self, lexer):
        self.indents = [0]  # indentation stack
        self.tokens = []  # token queue
        self.lexer = lexer
        self.source = None
        self.notal_tokens = []

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    # Iterator interface
    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next

    def token(self):
        # empty our buffer first
        if self.tokens:
            return self.tokens.pop(0)

        # loop until we find a valid token
        while 1:
            # grab the next from first stage
            token = self.lexer.token()

            # we only care about whitespace
            if not token or token.type != 'WHITESPACE':
                return token

            # check for new indent/dedent
            whitespace = token.value[1:]  # strip \n
            change = self._calc_indent(whitespace, token)
            if change:
                break

        # indentation change
        if change == 1:
            token.type = 'INDENT'
            return token

        # dedenting one or more times
        assert change < 0
        change += 1
        token.type = 'DEDENT'

        # buffer any additional DEDENTs
        while change:
            self.tokens.append(copy.copy(token))
            change += 1

        return token

    def _calc_indent(self, whitespace, token):
        "returns a number representing indents added or removed"
        n = len(whitespace)  # number of spaces
        indents = self.indents  # stack of space numbers
        if n > indents[-1]:
            indents.append(n)
            return 1

        # we are at the same level
        if n == indents[-1]:
            return 0

        # dedent one or more times
        i = 0
        while n < indents[-1]:
            indents.pop()
            if n > indents[-1]:
                raise SyntaxError(f"Wrong indentation level at line: {token.lineno}")
            i -= 1
        return i

    def scan_for_tokens(self, source):
        self.source = source
        self.input(source)
        self.notal_tokens = []
        while True:
            token = self.token()
            if not token:
                break
            else:
                token.lexpos = (token.lexpos, self.find_column_position(token))
            self.notal_tokens.append(token)

    def find_column_position(self, token):
        start_line = self.source.rfind("\n", 0, token.lexpos) + 1
        return token.lexpos - start_line + 1

    def get_tokens_in_json(self):
        tokens_in_json = [
            {
                "type": token.type,
                "value": token.value,
                "line_position": token.lineno,
                "lex_position": token.lexpos[0],
                "column_position": token.lexpos[1],
            }
            for token in self.notal_tokens
        ]
        return tokens_in_json
