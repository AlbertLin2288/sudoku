# I'm starting to do this too often
# this is a branch from sudoku6
# to test if a solution exist, just test it
# however, this will make it difficult to see
# if there's a reduction in possiblity
# so most of the code is similar
# I'm just not sure if this will work as thinking about sudoku has tire me out

# here we go again
# instead of rule, just make them constant and builtin
# the checking is done by number
# add group


class Sudoku:
    """The board and rules"""
    def __init__(self, copy=None) -> None:
        """if copy, become a copy of copy""" 
        if copy is None:
            self.board = [[Number(self, r*9+c) for c in range(9)]
                           for r in range(9)]
            self.flat_board = [self.board[i//9][i%9] for i in range(81)]
            self.groups = []
            for r in range(9):
                group = [self.flat_board[r*9:r*9+9], list(range(1,10))]
                self.groups.append(group)
                for num in group:
                    num.groups.append(group)
            for c in range(9):
                group = [self.flat_board[c::9], list(range(1,10))]
                self.groups.append(group)
                for num in group:
                    num.groups.append(group)
            for block in range(9):
                group = [self.board[block//3*3][block%3*3:block%3*3+3]+\
                         self.board[block//3*3+1][block%3*3:block%3*3+3]+\
                         self.board[block//3*3+2][block%3*3:block%3*3+3],
                           list(range(1,10))]
                self.groups.append(group)
                for num in group:
                    num.groups.append(group)
        else:
            # make self a deepcopy of copy
            self.init_as_copy(copy)
        
    def init_as_copy(self, copy):
        """init as a deepcopy of copy"""

    def error(self):
        """an error has occured"""

    def set(self, pos, value):
        """set number at pos to value"""
        r, c = pos
        num1 = self.board[r][c]
        num1.set(value)


class Number:
    """The number"""
    def __init__(self, board:Sudoku, pos) -> None:
        self.board = board
        self.pos = pos
        self.r, self.c = divmod(pos, 9)
        self.block = self.r//3, self.c//3
        self.block_pos = self.r%3, self.c%3
        self.possible = [1,2,3,4,5,6,7,8,9]
        self.groups = []

    def set(self, value):
        """set possible to value"""
        removed = self.possible[:]
        removed.remove(value)
        for val in removed:
            self.remove(val)

    def remove(self, value):
        """remove value from possible
        if not in value, return false"""
        if value not in self.possible:
            return False
        self.possible.remove(value)
        if len(self.possible) == 1: # self is determinted
            for group in self.groups:
                group[0].remove(self)
                group[1].remove(self.possible[0])
                if not any((num.remove(self.possible[0]) for num in group[0])):
                    pass
        # update related number
        return True

#     def set2(self, value):
#         """set self to value"""
#         self.possible = value
#         update_list = set() # don't ask me why this is a set
#         update_list2 = set()
#         for i, has_rule in self.has_rules.items():
#             if value == has_rule[0]: # has_rule satisified
#                 self.board.has_rule_true(i)
#             else:
#                 has_rule.remove(self)
#                 if len(has_rule) == 1:
#                     self.board.error()
#                     return
#                 if len(has_rule) == 2:
#                     update_list.add((has_rule[1], has_rule[0]))
#         for i, no_dupe_rule in self.no_dupe_rules.items():
#             if value in no_dupe_rule:
#                 self.board.error()
#                 return
#             for num in no_dupe_rule:
#                 if num != self:
#                     update_list2.add(num)
#         for num, value2 in update_list:
#             num.set2(value2)
