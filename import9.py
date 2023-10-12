"""add more function for testing"""

import sudoku9

class Sudoku(sudoku9.Sudoku):
    def __str__(self):
        board = ""
        board2 = ""
        for i in self.board:
            for j in i:
                possible = "".join((str(k) for k in j.possible))
                board += "{:<12}".format(possible)
                dupe = " ".join((num.name for num in j.no_dupe_rule))
                board2 += f"{j.name}: {dupe:<80}\n"
            board += "\n"
        has_rules = ""
        for i, j in self.has_rules.items():
            has_rules += f"{str(i):<3}: {str(j[0])}: "
            has_rules += "  ".join((num.name for num in j[1:]))+"\n"
        return f"{board}\n\n\n{board2}\n\n\n{has_rules}"
