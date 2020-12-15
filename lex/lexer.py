from lex.tokens import *
from lex.position import *
from err.error import *

"""
词法解析器
"""


class Lexer(object):
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None  # 当前访问的字符
        self.advance()

    # 预读 ：读取下一个
    def advance(self):
        self.pos.advance(self.current_char)  # 已经读取一次
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []
        """
        1.遍历text
        2.遍历过程中，分别判断获取的内容
        """
        while self.current_char is not None:
            if self.current_char in (' ', '\t', '\n'):
                self.advance()  # 空格，table, 换行 跳过
            elif self.current_char in DIGITS:  # 数字
                tokens.append(self.make_number())
                self.advance()
            elif self.current_char in LETTERS:  # 字符
                tokens.append(self.make_identifier())
            elif self.current_char == '=':  # =
                tokens.append(Token(TT_EQ, pos_start=self.pos))
                self.advance()
            elif self.current_char == '<':  # < <= <>
                tokens.append(self.make_less_than_not_eq())
            elif self.current_char == '>':  # > >=
                tokens.append(self.make_greater_than())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_L, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_R, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_DH, pos_start=self.pos))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_FH, pos_start=self.pos))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(TT_GH, pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_MH, pos_start=self.pos))
                self.advance()
            else:  # 没有匹配到
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        """
        整数，小数
        :return:
        """

        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_REAL, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        variable_str = ""
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            variable_str += self.current_char
            self.advance()

        if variable_str in KEYWORDS:
            tok_type = TT_KEYWORDS
        else:
            tok_type = TT_IDENTIFIER
        return Token(tok_type, variable_str, pos_start, self.pos)

    def make_less_than_not_eq(self):
        # < <= <>
        tok_type = TT_FL
        pop_start = self.pos.copy()

        self.advance()
        if self.current_char == '=':  # <=
            self.advance()
            tok_type = TT_FLE
        elif self.current_char == '>':  # <>
            self.advance()
            tok_type = TT_NE
        return Token(tok_type, pos_start=pop_start, pos_end=self.pos)

    def make_greater_than(self):
        # > >=
        tok_type = TT_FR
        pos_start = self.pos.copy()

        self.advance()
        if self.current_char == '=':  # >=
            self.advance()
            tok_type = TT_FRE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
