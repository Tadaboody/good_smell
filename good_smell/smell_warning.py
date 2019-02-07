from typing import NamedTuple

FLAKE8_FORMAT = "{path}:{row}:{col} {symbol} {msg}"
PYLINT_FORMAT = "{path}:{line}:{column}: {msg} ({symbol})"


def to_dict(namedtuple: NamedTuple) -> dict:
    return dict(zip(namedtuple._fields, list(namedtuple)))


class SmellWarning(NamedTuple):
    """Class to represent a warning message about a smell"""

    row: int
    col: int
    path: str
    msg: str
    symbol: str

    def warning_string(self, formatter: str = PYLINT_FORMAT):
        return formatter.format(**to_dict(self))
