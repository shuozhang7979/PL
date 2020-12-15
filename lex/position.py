class Position(object):
    def __init__(self, idx, ln, col, fn, ftxt):
        """
        :param idx:索引
        :param ln:行号
        :param col:列好
        :param fn:文件名
        :param ftxt:内容
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        """
        获取下一个字符
        """
        self.idx += 1   # 索引加一
        self.col += 1   # 列号加一

        if current_char == '\n':    # 遇到换行符
            self.col = 0
            self.ln += 1

    def copy(self):     # 深拷贝
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

