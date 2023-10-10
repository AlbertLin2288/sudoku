"""add more function for testing"""

import sudoku8

class Sudoku(sudoku8.Sudoku):
    def __str__(self):
        board = ""
        for i in self.board:
            for j in i:
                possible = "".join((str(k) for k in j.possible))
                board += "{:<12}".format(possible)
            board += "\n"
        groups = ""
        for i, j in self.groups.items():
            groups += "{:<3}: ".format(str(i))
            groups += "{:<12}".format("".join((str(k) for k in j[1])))
            groups += "  ".join(("ABCDEFGHIJ"[k.r] +\
                                 "abcdefghi"[k.c] for k in j[0]))+"\n"
        return board +"\n\n\n" + groups
