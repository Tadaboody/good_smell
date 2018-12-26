import dataclasses

FLAKE8_FORMAT = "{path:s}:{row:d}:{col:d}:{code:s}{text:s}"
FLAKE8_FORMAT = "{path}:{row}:{col} {code} {msg}"


@dataclasses.dataclass(frozen=True)  # pylint: disable=too-few-public-methods
class SmellWarning:
    """Class to represent a warning message about a smell"""

    code: str
    row: int
    col: int
    path: str
    msg: str

    def warning_string(self, formatter: str = FLAKE8_FORMAT):
        return formatter.format(**dataclasses.asdict(self))
