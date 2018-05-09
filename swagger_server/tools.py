import hashlib
import os
import errno


def hashpasswd(passwd):
    return hashlib.sha512(passwd.encode('utf-8')).hexdigest()


def create_path(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


class EvalBuilder:

    _expressions = None

    def __init__(self):
        self._expressions = []

    def append(self, expression):
        self._expressions.append(expression)

    def __str__(self):
        if len(self._expressions) == 0:
            return "True"
        eval_string = "and_(True"
        for expression in self._expressions:
            eval_string += ","+expression
        eval_string += ")"
        return eval_string

    def getEvalStr(self):
        return self.__str__()
