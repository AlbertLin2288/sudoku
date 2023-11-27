"""add more function for testing"""

import sudoku9b
from time import time

class Sudoku(sudoku9b.Sudoku):
    def __str__(self):
        board = ""
        board2 = ""
        for i in self.board:
            for j in i:
                possible = "".join((str(k) for k in j.possible))
                board += "{:<12}".format(possible)
                dupe = " ".join((num.name for num in j.no_dupe_rule))
                if len(dupe) > 2:
                    board2 += f"{j.name}: {dupe:<80}\n"
            board += "\n"
        has_rules = ""
        for i, j in self.has_rules.items():
            has_rules += f"{str(i):<3}: {str(j[0])}: "
            has_rules += "  ".join((num.name for num in j[2:]))+"\n"
        return f"board:\n{board}\ndupe:\n{board2}\nhas\n{has_rules}"


if __name__ == "__main__":
    t1 = time()
    s1 = Sudoku()
    interface = True
##    IN_LIST = ["Aa1","Ab2","Ac3","Bd1","Be2","Bf3"]
##    for i in IN_LIST:
##        s2 = Sudoku(s1)
##        s2.input(i)
##        s1 = s2
##    print(1)
##    s2 = Sudoku(s1)
##    s2.input("Cg4")
    TEST1 = True
    # input moves and make them
    TEST2 = False
    # read sudoku question from file
    TEST3 = False
    # solve test2
    TEST4 = False
    # test if all number in file is useful
    TEST5 = False
    TEST6 = False

    if TEST1:
        move = input()
        while "q" not in move:
            for i in move.split(" "):
                if len(i)>2 and i[0] in "ABCDEFGHI" and i[1] in "abcdefghi" and\
                    i[2] in "123456789":
                    s2 = Sudoku(s1)
                    s2.input(i)
                    s1 = s2
            move = input()
    
    if TEST2:
        with open("test1.txt", encoding="UTF-8") as file:
            board1l = file.readlines()
            board1 = []
            for i in board1l:
                if i[0] != "#":
                    board1.append(i[:-1])
        for r,row in enumerate(board1[:9]):
            for c, n in enumerate(row[:9]):
                if n in "123456789":
                    s2 = Sudoku(s1)
                    s2.set_number((r,c),int(n))
                    s1 = s2
    if TEST3:
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

    if TEST4:
        g1 = sudoku9b.Game()
        with open("test1.txt", encoding="UTF-8") as file:
            board1l = file.readlines()
            board1 = []
            for i in board1l:
                if i[0] != "#":
                    board1.append(i[:-1])
        for r,row in enumerate(board1[:9]):
            for c, n in enumerate(row[:9]):
                if n in "123456789":
                    test = g1.set2((r,c),int(n))
                    if not test:
                        raise ValueError("Sudoku has a useless input")
                    g1.set1((r,c),int(n))

    if TEST5:
        s1 = sudoku9b.Sudoku()
        success = sudoku9b.check2(s1)
        if success[0]:
            print("Yay")
        else:
            print(success[1])
            s1 = success[2]
            # raise ValueError("Sudoku possible isn't possible")

    if TEST6:
        g1 = sudoku9b.Game()
        with open("test1.txt", encoding="UTF-8") as file:
            board1l = file.readlines()
            board1 = []
            for i in board1l:
                if i[0] != "#":
                    board1.append(i[:-1])
        for r,row in enumerate(board1[:9]):
            for c, n in enumerate(row[:9]):
                if n in "123456789":
                    test = g1.check1()
                    if not test:
                        raise ValueError("Sudoku couldn't tell if set")
                    g1.set1((r,c),int(n))
    
    if interface:
        cmd = input(">>>")
        while cmd:
            try:
                print(exec(cmd))
            except BaseException as e:
                print(e)
                input("Press enter to continue")
            cmd = input(">>>")
