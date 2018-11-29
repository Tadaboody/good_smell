from range_len_fix import RangeLenSmell
from lint_smell import LintSmell
from pathlib import Path
from fire import Fire
import astor


def lint_source(path: str, starting_line: int=0, end_line: int=None):
    path = Path(path)
    source = path.read_text()
    smell: LintSmell
    for smell in (RangeLenSmell,):
        source = smell(source, starting_line, end_line).fix_smell()
    print(astor.to_source(source))

if __name__ == '__main__':
    Fire(lint_source)