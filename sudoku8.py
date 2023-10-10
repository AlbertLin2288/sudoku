# going back to sudoku2
# based on sudoku7
# instead of 1 rule per ...
# use 9 different rules to allow easier check of relations

class Sudoku:
    """The board and rules."""
    def __init__(self, copy=None) -> None:
        """if copy, become a copy of copy""" 
        if copy is None:
            self.board = [[Number(self, r*9+c) for c in range(9)]
                           for r in range(9)]
            self.flat_board = [self.board[i//9][i%9] for i in range(81)]
            self.groups = {}
            self.id = 0
            for r in range(9):
                group = [self.flat_board[r*9:r*9+9], 
                         {i:9 for i in range(1,10)}]
                self.groups[self.id] = group
                for num in group[0]:
                    num.groups[self.id] = group
                self.id += 1
            for c in range(9):
                group = [self.flat_board[c::9],
                         {i:9 for i in range(1,10)}]
                self.groups[self.id] = group
                for num in group[0]:
                    num.groups[self.id] = group
                self.id += 1
            for block in range(9):
                group = [self.board[block//3*3][block%3*3:block%3*3+3]+\
                         self.board[block//3*3+1][block%3*3:block%3*3+3]+\
                         self.board[block//3*3+2][block%3*3:block%3*3+3],
                         {i:9 for i in range(1,10)}]
                self.groups[self.id] = group
                for num in group[0]:
                    num.groups[self.id] = group
                self.id += 1
        else:
                # make self a deepcopy of copy
            self.groups = {i:[[], copy.groups[i][1].copy()] for i in copy.groups}
            self.id = copy.id
            self.board = [[Number(self, copy = copy.board[r][c])
                            for c in range(9)] for r in range(9)]
            self.flat_board = [self.board[i//9][i%9] for i in range(81)]

    def error(self, info="Error"):
        """an error has occured"""
        raise ValueError(info)

    def set(self, pos, value):
        """set number at pos to value"""
        r, c = pos
        num1 = self.board[r][c]
        num1.set(value)


class Number:
    """The number"""
    def __init__(self, board:Sudoku, pos=None, copy=None) -> None:
        self.board = board
        if copy is None:
            self.pos = pos
            self.r, self.c = divmod(pos, 9)
            self.block = self.r//3, self.c//3
            self.block_pos = self.r%3, self.c%3
            self.possible = [1,2,3,4,5,6,7,8,9]
            self.groups = {}
        else:
            self.pos = copy.pos
            self.r = copy.r
            self.c = copy.c
            self.block = copy.block
            self.block_pos = copy.block_pos
            self.possible = copy.possible[:]
            self.groups = {}
            for i in copy.groups:
                self.groups[i] = self.board.groups[i]
                self.board.groups[i][0].append(self)

    def set(self, value):
        """set possible to value"""
        if value not in self.possible:
            self.board.error(f"{'ABCDEFGHI'[self.r]+'abcdefghi'[self.c]}" +\
                             f" can't be {str(value)}")
        removed = self.possible[:]
        removed.remove(value)
        for val in removed:
            self.remove(val)

    def remove(self, value):
        """remove value from possible
        if not in value, return false"""
        if len(self.possible) == 1 or value not in self.possible:
            return False
        self.possible.remove(value)
        for i in self.groups.values():
            val = i[1][value]
            if val>1:
                i[1][value] = val-1
            else:
                self.board.error(f"Removing {str(value)} from " +\
                                 f"{'ABCDEFGHI'[self.r]}"+\
                                 f"{'abcdefghi'[self.c]} cause group {i}" +\
                                  " to fail")

        if len(self.possible) == 1: # self is determinted
            for i, group in self.groups.items():
                group[0].remove(self)
                if not any((num.remove(self.possible[0]) for num in group[0])):
                    self.board.error(f"Removing {str(value)} from " +\
                                     f"{'ABCDEFGHI'[self.r]}"+\
                                     f"{'abcdefghi'[self.c]} cause group {i}"+\
                                      " to fail")

        # update related number
        return True
