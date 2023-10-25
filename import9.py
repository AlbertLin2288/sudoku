"""add more function for testing"""

import sudoku9
from time import time

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


if __name__ == "__main__":
    t1 = time()
    s1 = Sudoku()
    interface = False
##    IN_LIST = ["Aa1","Ab2","Ac3","Bd1","Be2","Bf3"]
##    for i in IN_LIST:
##        s2 = Sudoku(s1)
##        s2.input(i)
##        s1 = s2
##    print(1)
##    s2 = Sudoku(s1)
##    s2.input("Cg4")

    if False:
        move = input()
        while "q" not in move:
            if move[0] in "ABCDEFGHI" and move[1] in "abcdefghi" and \
                move[2] in "123456789":
                s2 = Sudoku(s1)
                s2.input(move)
                s1 = s2
            else:
                print("invalid input")
            move = input()
    
    if True:
        board1 = """
5 72   9 
  6 3 7 1
4      6 
1  49   7
   5 8   
8   27  5
 7      9
2 0 8 6  
 4   93 8"""[1:]
        for r,row in enumerate(board1.split("\n")):
            for c, n in enumerate(row):
                if n in "123456789":
                    s2 = Sudoku(s1)
                    s2.set_number((r,c),int(n))
                    s1 = s2
    if True:
        for i in range(81):
            if not s1.flat_board[i].isset:
                success = []
                for j in range(9):
                    try:
                        s2 = Sudoku(s1)
                        s2.set_number(i, j)
                        success.append(j)
                    except ValueError:
                        pass
                if len(success) == 1:
                    s1.set_number(i,success[0])
                else:
                    interface = True
                    break
        else:
            for r in range(9):
                for c in range(9):
                    print(s1.board[r][c].possible[0],end="")
                print()
    print(f"\n\nTime taken: {time()-t1}\n")
    
    if interface:
        cmd = input(">>>")
        while cmd:
            try:
                print(exec(cmd))
            except BaseException as e:
                print(e)
                input("Press enter to continue")
            cmd = input(">>>")
