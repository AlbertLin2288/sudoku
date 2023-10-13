# idea:
# the same as sudoku9.py
# except save no_dupe_rule to number
# note: no_dupe_rule include self
# within a has_rule theres many numbers
# however there are subset of has_rule that is other has_rule
# the number of different subset mustn't exceed number of numbers -1
# as a has_rule reduce size, it should update all it's children 
# and look for new parents
class Sudoku:
    """The board and rules"""
    def __init__(self, copy=None) -> None:
        """if copy, become a copy of copy""" 
        if copy is None:
            self.board = [[Number(self, r, c) for c in range(9)]
                           for r in range(9)]
            self.flat_board = [self.board[i//9][i%9] for i in range(81)]
            self.has_rules = {} # {id:[value, Number...]}
                                # must have one number = value
            self.id = 0 # largest unused id
            self.has_ids = []
            for r in range(9): # add rules to rows
                for i in range(1,10):
                    self.add_has_rule(i, zip([r]*9,range(9)))
                no_dupe = self.flat_board[r*9:r*9+9]
                for num in no_dupe:
                    num.no_dupe_rule.update(no_dupe)
            for c in range(9): # add rules to columns
                for i in range(1,10):
                    self.add_has_rule(i, zip(range(9),[c]*9))
                no_dupe = self.flat_board[c::9]
                for num in no_dupe:
                    num.no_dupe_rule.update(no_dupe)
            for block in range(9): # for each block
                for i in range(1,10):
                    has_rule = [i]
                    self.has_rules[self.id] = has_rule
                    self.has_ids.append(self.id)
                    for p in range(9): # the cord in the flattened block
                        number = self.board[block//3*3+p//3][block%3*3+p%3]
                        has_rule.append(number)
                        number.has_rules[self.id] = has_rule
                    self.id += 1
                no_dupe = [self.board[block//3*3+p//3][block%3*3+p%3]
                           for p in range(9)]
                for num in no_dupe:
                    num.no_dupe_rule.update(no_dupe)
        else:
            # make self a deepcopy of copy
            self.init_as_copy(copy)

    def init_as_copy(self, copy):
        """init as a deepcopy of copy"""
        self.board = []
        self.has_rules = {}
        self.id = copy.id
        self.has_ids = copy.has_ids[:]
        for r in range(9):
            row = []
            for c,i in enumerate(copy.board[r]):
                if isinstance(i, Number):
                    row.append(Number(self, r, c))
                else:
                    row.append(i)
            self.board.append(row)
        self.flat_board = [self.board[i//9][i%9] for i in range(81)]
        for i in copy.has_rules: # copy has_rules for board
            has_rule = [copy.has_rules[i][0]]
            for j in copy.has_rules[i][1:]:
                has_rule.append(self.flat_board[j.pos])
            self.has_rules[i] = has_rule
        for i,num in enumerate(self.flat_board):
            for j in copy.flat_board[i].has_rules: # copy has_rules for Number
                num.has_rules[j] = self.has_rules[j]
            for j in copy.flat_board[i].no_dupe_rule: # copy no_dupe rules
                num.no_dupe_rule.add(self.flat_board[j.pos])
            num.possible = copy.flat_board[i].possible[:]
        

    def set_number(self, pos, value):
        """set pos to value"""
        if isinstance(pos, str):
            self.board["ABCDEFGHI".index(pos[0])]\
                ["abcdefghi".index(pos[1])].set(value)
        elif isinstance(pos, int):
            self.flat_board[pos].set(value)
        elif isinstance(pos, tuple):
            self.flat_board[pos[0]*9+pos[1]].set(value)

    def add_has_rule(self, value, cords):
        """add has_rule value with numbers at cords"""
        has_rule = [value]
        self.has_rules[self.id] = has_rule
        self.has_ids.append(self.id)
        for r,c in cords:
            has_rule.append(self.board[r][c])
            self.board[r][c].has_rules[self.id] = has_rule
        self.id += 1

    def update_has_rules(self):
        """update the has_rules
        check if there is only one element in rule
            update: check this when removing element in rule
        check if there is parent/child of rule"""
        for i in self.has_ids:
            has_rule = self.has_rules[i]
            for has_rule2 in self.has_rules:
                if all((j in has_rule for j in has_rule2)): # rule2 is a child
                    if has_rule[0] == has_rule2[0]:
                        # remove has_rule
                        self.has_rule_true(i)
                        continue

    def has_rule_true(self, has_id):
        """has_rule is satisifled, so delete it"""
        self.has_ids.remove(has_id)
        has_rules = self.has_rules.pop(has_id)
        for i in has_rules[1:]:
            i.has_rules.pop(has_id)

    def error(self, message="Error"):
        """an error has occured"""
        raise ValueError(message)


class Number:
    """The number"""
    def __init__(self, board:Sudoku, r, c) -> None:
        self.board = board
        self.pos = r*9+c
        self.r, self.c = r, c
        self.name = "ABCDEFGHI"[r]+"abcdefghi"[c]
        self.has_rules = {}
        self.no_dupe_rule = set() # only Number
        self.possible = [1,2,3,4,5,6,7,8,9]

    def set(self, value):
        """replace self with int"""
        # to do: replace self with int
        self.set2(value)

    def remove(self, value):
        """remove value as a possibility
        used when set value(removing every other value) 
        and when conflicking"""
        if value not in self.possible:
            return False
        self.possible.remove(value)
        for i,has_rule in self.has_rules.copy().items():
            if has_rule[0] != value:
                continue
            has_rule.remove(self)
            self.has_rules.pop(i)
            if len(has_rule) == 1:
                self.board.error(f"Removing {str(value)} from " +\
                                 f"{self.name} cause " +\
                                 f"has_rule {i} to has fail.")
                continue
            if len(has_rule) == 2:
                self.board.has_rule_true(i)
                has_rule[1].set2(has_rule[0])
                continue
            
            # futher update group

        if len(self.possible) == 1: # self is determinted
            self._set3()
        return True

    def set2(self, value):
        """set self to value"""
        if value not in self.possible:
            self.board.error(f"can't set {self.name} to {value}")
        for i in self.possible[:]:
            if i == value:
                continue
            self.remove(i)
        # self.possible = value
        # update_list = set() # don't ask me why this is a set
        # for i, has_rule in self.has_rules.items():
        #     if value == has_rule[0]: # has_rule satisified
        #         self.board.has_rule_true(i)
        #     else:
        #         has_rule.remove(self)
        #         if len(has_rule) == 1:
        #             self.board.error()
        #             return
        #         if len(has_rule) == 2:
        #             update_list.add((has_rule[1], has_rule[0]))
        # for num, value2 in update_list:
        #     num.set2(value2)

    def _set3(self):
        """self has already only 1 possible"""
        value = self.possible[0]
        for i in self.no_dupe_rule:
            if i is self:
                continue
            i.no_dupe_rule.discard(self)
            i.remove(value)
        for i, has_rule in self.has_rules.copy().items():
            if has_rule[0] == value:
                self.board.has_rule_true(i)
                continue
            # i don't think it's possible
            raise ValueError("HI")
