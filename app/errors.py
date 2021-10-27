class Error(Exception):
    pass


class NotInteger(Error):
    pass


class Unavailable(Error):
    pass


class InvalidResponseData(Error):
    pass


class InvalidRequestData(Error):
    pass


class ValueTooSmall(Error):
    pass


class ValueTooBig(Error):
    pass


class InvalidValueType(Error):
    pass
