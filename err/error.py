class Error(object):
    def __init__(self, pos_start, pos_end, error_name, details):
        """
        :param pos_start:
        :param pos_end:
        :param error_name:
        :param details:
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        res = f'{self.error_name}:{self.details}'
        res += f'File {self.pos_start.fn}, line {self.pos_end.ln + 1}'
        return res


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, detail):
        super().__init__(pos_start, pos_end, "IllegalCharError", detail)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, detail=''):
        super().__init__(pos_start, pos_end, "InvalidSyntaxError", detail)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, detail=''):
        super().__init__(pos_start, pos_end, "ExpectedCharError", detail)

