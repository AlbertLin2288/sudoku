# idea:
# the same as sudoku2.py
# but two types of rule
# in a row/column/box: 1-9
# for each number: avilable slot

class Sudoku:
    """The board and rules"""
    def __init__(self) -> None:
        self.board = [[Number() for c in range(9)] for r in range(9)]
        self.has_rules = [] # [value, Number...] must have one number = value
        self.no_dupe_rules = [] # [Number, Number..., int, int...] must not dupe

class Number:
    """The number"""
    def __init__(self) -> None:
        pass
