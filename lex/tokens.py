import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
#   token_type => TT
TT_INT = "INT"
TT_REAL = "REAL"

TT_PLUS = "PLUS"    # +
TT_MUL = "MUL"      # *
TT_MINUS = "MINUS"  # -
TT_DIV = "DIV"      # /

TT_EOF = "EOF"      # end_inputs
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORDS = "KEYWORDS"

TT_EQ = "EQ"    # =
TT_NE = "NE"    # <>
TT_FL = "FL"    # <
TT_FR = "FR"    # >
TT_FLE = "FLE"  # <=
TT_FRE = "FRE"  # >=

TT_L = "L"      # (
TT_R = "R"      # )

TT_DH = "DH"    # ,
TT_FH = "FH"    # ;
TT_GH = "GH"    # .
TT_MH = "MH"    # :
KEYWORDS = [
    'program',
    'type', 'integer', 'real',
            'class', 'public', 'private', 'protected',
            'virtual', 'override', 'overload',
    "var",
    'begin', 'end', 'return',
    "and", "or", "not",
    "if", "then", "else",
    'while',
    'function', 'procedure'
]


class Token(object):
    # <token-name, attribute-value>
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            # Token 单个字符串， pos_start = pos_end
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance(self.value)    # 下一个token
        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        # 判断token 是否一致
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'
