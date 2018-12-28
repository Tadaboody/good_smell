import dataclasses

FLAKE8_FORMAT = "{path}:{row}:{col} {symbol} {msg}"
PYLINT_FORMAT = "{path}:{line}:{column}: {msg} ({symbol})"


@dataclasses.dataclass(frozen=True)  # pylint: disable=too-few-public-methods
class SmellWarning:
    """Class to represent a warning message about a smell"""

    row: int
    col: int
    path: str
    msg: str
    symbol: str

    def warning_string(self, formatter: str = PYLINT_FORMAT):
        return formatter.format(**dataclasses.asdict(self))
