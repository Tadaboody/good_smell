# flake8:noqa
try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata
__version__ = metadata.version("good-smell")

from .smell_warning import SmellWarning
from .lint_smell import LintSmell
from .ast_smell import AstSmell, LoggingTransformer
from .smells import implemented_smells
from .main import fix_smell, print_fixed_smell, main, smell_warnings
from . import smells  # Allow importing good_smell.smells
from .flake8_ext import LintingFlake8
