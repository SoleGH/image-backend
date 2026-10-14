import logging

logger = logging.getLogger("SOURCE")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def to_lower_camel_case(text, sep="_"):
    """translate "Hello World" to "hello_world" """
    mp = map(lambda x: sep + x.lower() if x.isupper() else x, text)
    return "".join(mp).removeprefix(sep)


def to_upper_camel_case(string, sep="_"):
    words = string.split(sep)
    capitalized_words = [word.capitalize() for word in words]
    return " ".join(capitalized_words)


class BaseCustomException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

class MessageException(BaseCustomException):
    def __init__(self, message):
        super().__init__(message, status_code=401)

class RecordNotFoundException(BaseCustomException):
    def __init__(self, message):
        super().__init__(message, status_code=404)

class RecordExistedException(BaseCustomException):
    def __init__(self, message):
        super().__init__(message, status_code=409)