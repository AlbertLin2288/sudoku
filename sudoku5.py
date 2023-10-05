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
            self.has_ids = []
            self.no_dupe_ids = []
            for r in range(9): # add rules to rows
                for i in range(9):
                    self.add_has_rule(i, zip([r]*9,range(9)))
                self.add_no_dupe_rule([], zip([r]*9,range(9)))
            for c in range(9): # add rules to columns
                for i in range(9):
                    self.add_has_rule(i, zip(range(9),[c]*9))
                self.add_no_dupe_rule([], zip(range(9),[c]*9))
            for block in range(9): # for each block
                for i in range(9):
                    has_rule = [i]
                    self.has_rules[self.id] = has_rule
                    self.has_ids.append(self.id)
                    for p in range(9): # the cord in the flattened block
                        number = self.board[block//3*3+p//3][block%3*3+p%3]
                        has_rule.append(number)
                        number.has_rules[self.id] = has_rule
                    self.id += 1
                no_dupe_rule = []
                self.no_dupe_rules[self.id] = no_dupe_rule
                self.no_dupe_ids.append(self.id)
                for p in range(9):
                    number = self.board[block//3*3+p//3][block%3*3+p%3]
                    no_dupe_rule.append(number)
                    number.no_dupe_rules[self.id] = no_dupe_rule
                self.id += 1
        else:
            # make self a deepcopy of copy
            self.init_as_copy(copy)
        
    def init_as_copy(self, copy):
        """init as a deepcopy of copy"""
        self.board = []
        self.has_rules = {}
        self.no_dupe_rules = {}
        self.id = copy.id
        self.has_ids = copy.has_ids
        self.no_dupe_ids = copy.no_dupe_ids
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

    def set_number(self, pos, value):
        pass

    def add_has_rule(self, value, cords):
        has_rule = [value]
        self.has_rules[self.id] = has_rule
        self.has_ids.append(self.id)
        for r,c in cords:
            has_rule.append(self.board[r][c])
            self.board[r][c].has_rules[self.id] = has_rule
        self.id += 1

    def add_no_dupe_rule(self, values, cords):
        no_dupe_rule = list(values)
        self.no_dupe_rules[self.id] = no_dupe_rule
        self.no_dupe_ids.append(self.id)
        for r,c in cords:
            no_dupe_rule.append(self.board[r][c])
            self.board[r][c].no_dupe_rules[self.id] = no_dupe_rule
        self.id += 1

    def update_has_rules(self):
        """update the has_rules
        check if there is only one element in rule
            update: check this when removing element in rule
        check if there is child of rule"""
        for i in self.has_ids:
            has_rule = self.has_rules[i]

    def update_do_dupe_rules(self, ids):
        """update the no_dupe_rules
        check if there is child has_rule"""

    def has_rule_true(self, has_id):
        """has_rule is satisifled, so delete it"""
        self.has_ids.remove(has_id)
        has_rules = self.has_rules.pop(has_id)
        for i in has_rules[1:]:
            i.has_rules.pop(has_id)

    def error(self):
        """an error has occured"""


class Number:
    """The number"""
    def __init__(self, board:Sudoku, r, c) -> None:
        self.board = board
        self.pos = (r,c)
        self.r, self.c = self.pos
        self.has_rules = {}
        self.no_dupe_rules = {}
        self.possible = [1,2,3,4,5,6,7,8,9]

    def set(self):
        """replace self with int"""

    def set2(self, value):
        """set self to value"""
        self.possible = value
        update_list = set() # don't ask me why this is a set
        for i in self.has_rules:
            if value == self.has_rules[i][0]: # has_rule satisified
                self.board.has_rule_true(i)
            else:
                has_rule = self.has_rules[i]
                has_rule.remove(self)
                if len(has_rule) == 1:
                    self.board.error()
                    return None
                elif len(has_rule) == 2:
                    update_list.add(has_rule[1])
