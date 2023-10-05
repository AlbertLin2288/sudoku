# idea:
# the same as sudoku2.py
# but two types of rule
# in a row/column/box: 1-9
# for each number: avilable slot

class Sudoku:
    """The board and rules"""
    def __init__(self, copy=None) -> None:
        """if copy, become a copy of copy"""
        if copy is None:
            self.board = [[Number(self, r, c) for c in range(9)]
                           for r in range(9)]
            self.has_rules = {} # {id:[value, Number...]}
                                # must have one number = value
            self.no_dupe_rules = {} # {id:[Number, Number..., int, int...]}
                                    # there can't be dupelicate in list
            self.id = 0 # largest unused id
            for r in range(9): # add rules to rows
                for i in range(9):
                    has_rule = [i]
                    self.has_rules[self.id] = has_rule
                    for c in range(9):
                        has_rule.append(self.board[r][c])
                        self.board[r][c].has_rules[self.id] = has_rule
                    self.id += 1
                no_dupe_rule = []
                self.no_dupe_rules[self.id] = no_dupe_rule
                for c in range(9):
                    no_dupe_rule.append(self.board[r][c])
                    self.board[r][c].no_dupe_rules[self.id] = no_dupe_rule
                self.id += 1
            for c in range(9): # add rules to columns
                for i in range(9):
                    has_rule = [i]
                    self.has_rules[self.id] = has_rule
                    for r in range(9):
                        has_rule.append(self.board[r][c])
                        self.board[r][c].has_rules[self.id] = has_rule
                    self.id += 1
                no_dupe_rule = []
                self.no_dupe_rules[self.id] = no_dupe_rule
                for r in range(9):
                    no_dupe_rule.append(self.board[r][c])
                    self.board[r][c].no_dupe_rules[self.id] = no_dupe_rule
                self.id += 1
            for block in range(9): # for each block
                for i in range(9):
                    has_rule = [i]
                    self.has_rules[self.id] = has_rule
                    for p in range(9): # the cord in the flattened block
                        number = self.board[block//3*3+p//3][block%3*3+p%3]
                        has_rule.append(number)
                        number.has_rules[self.id] = has_rule
                    self.id += 1
                no_dupe_rule = []
                self.no_dupe_rules[self.id] = no_dupe_rule
                for p in range(9):
                    number = self.board[block//3*3+p//3][block%3*3+p%3]
                    no_dupe_rule.append(number)
                    number.no_dupe_rules[self.id] = no_dupe_rule
                self.id += 1
        else:
            # make self a deepcopy of copy
            self.board = []
            self.has_rules = {}
            self.no_dupe_rules = {}
            self.id = copy.id
            for r in range(9):
                row = []
                for c,i in enumerate(copy.board[r]):
                    if type(i) == Number:
                        row.append(Number(self, r, c))
                    else:
                        row.append(i)
                self.board.append(row)
            for i in copy.has_rules:
                has_rule = [copy.has_rules[i][0]]
                for j in copy.has_rules[i][1:]:
                    has_rule.append(self.board[j.r][j.c])
                self.has_rules[i] = has_rule
            for i in copy.no_dupe_rules:
                no_dupe_rule = []
                for j in copy.no_dupe_rules[i]:
                    if type(j) == Number:
                        no_dupe_rule.append(self.board[j.r][j.c])
                    else:
                        no_dupe_rule.append(j)
                self.no_dupe_rules[i] = no_dupe_rule
            for r, i in enumerate(self.board):
                for c, j in enumerate(i):
                    for k in copy.board[r][c].has_rules:
                        j.has_rules[k] = self.has_rules[k]
                    for k in copy.board[r][c].no_dupe_rules:
                        j.no_dupe_rules[k] = self.no_dupe_rules[k]


class Number:
    """The number"""
    def __init__(self, board, r, c) -> None:
        self.board = board
        self.pos = (r,c)
        self.r, self.c = self.pos
        self.has_rules = {}
        self.no_dupe_rules = {}

