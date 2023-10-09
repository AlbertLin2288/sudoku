"""add more function for testing"""

import sudoku7

class Sudoku(sudoku7.Sudoku):
    def __str__(self):
        board = ""
        for i in self.board:
            for j in i:
                possible = "".join((str(k) for k in j.possible))
                board += "{:<12}".format(possible)
            board += "\n"
        groups = ""
        for i in self.groups.values():
            groups += "{:<12}".format("".join((str(k) for k in i[1])))
            groups += "  ".join(("ABCDEFGHIJ"[j.r] +\
                                 "abcdefghi"[j.c] for j in i[0]))+"\n"
        return board +"\n\n\n" + groups
