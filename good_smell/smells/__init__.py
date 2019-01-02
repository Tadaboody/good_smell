from .range_len_fix import RangeLenSmell
from .nested_for import NestedFor
from .filter import FilterIterator
from .missing_dropwhile import DropWhile

implemented_smells = (RangeLenSmell, NestedFor, FilterIterator, DropWhile)
