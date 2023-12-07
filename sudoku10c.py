# First test how fast it is at finding solution
# answer: 0.04s, 5 time as fast as sudoku9
#
# Step 2: Make a program for playing
import re
from time import time
P = re.compile("start(\n[1-9 ]{9}){9}")

def cal_col(row_num):
    """calculate which rules num is in"""
    rn = row_num//81
    cn = row_num//9%9
    nn = row_num%9
    r1 = rn*9 + cn
    r2 = rn*9 + nn + 81
    r3 = cn*9 + nn + 162
    r4 = rn//3*27 + cn//3*9 + nn + 243
    return r1,r2,r3,r4

def cal_row(col):
    """calculate which numbers rule col include"""
    if col<81:
        return (col*9+i for i in range(9))
    col -= 81
    if col<81:
        con = col//9*81 + col%9
        return (con+i*9 for i in range(9))
    col -= 81
    if col<81:
        return (col+81*i for i in range(9))
    col -= 81
    con = col//27*243+col//9%3*27+col%9
    return (con+i//3*81+i%3*9 for i in range(9))

def get_num(row_num):
    """return the location and value of the cell correspond to row row_num"""
    return row_num//81, row_num//9%9, row_num%9

def solven(rrows, rcolumns, col_head, sboard, row=None, n=1):
    """find if it has more or equal n solution"""
    if n == 0:
        print("Hi1") # shouldn't be called
        return 0
    if len(rcolumns) == 0:
        print("Hi2")
        return n-1
    if row is not None:
        pc = set()
        pr = set()
        sboard.append(row)
        for c1 in cal_col(row):
            if c1 in rcolumns:
                for r1 in cal_row(c1):
                    if r1 in rrows:
                        rrows.remove(r1)
                        pr.add(r1)
                        for c2 in cal_col(r1):
                            col_head[c2] -= 1
                rcolumns.remove(c1)
                pc.add(c1)
    if len(rcolumns) == 0:
        n = n-1
        if not check_error(sboard):
            raise ValueError("Board not possible")
        print_board(sboard)
        print("\n")
    else:
        mc = min(rcolumns, key=lambda c:col_head[c])
        if col_head[mc] != 0:
            col = mc
            for r1 in cal_row(col):
                if r1 in rrows:
                    n = solven(rrows, rcolumns,col_head, sboard, r1, n)
                    if n == 0:
                        break
    if row is not None:
        sboard.pop()
        for c1 in pc:
            rcolumns.add(c1)
        for r1 in pr:
            rrows.add(r1)
            for c2 in cal_col(r1):
                col_head[c2] += 1
    return n

def check_error(board1):
    """Check if the board is correct, return True if it's correct"""
    if len(board1) != 81:
        return False
    s1 = set()
    for i in board1:
        v = i//9
        if v in s1:
            return False
        s1.add(v)
    s1 = set()
    for i in board1:
        v = i//81*9+i%9
        if v in s1:
            return False
        s1.add(v)
    s1 = set()
    for i in board1:
        v = i%81
        if v in s1:
            return False
        s1.add(v)
    s1 = set()
    for i in board1:
        v = i//243*27+i%81//27*9+i%9
        if v in s1:
            return False
        s1.add(v)
    return True

def print_board(board1):
    """Print the board if it is completed"""
    if not check_error(board1):
        print("error")
    l1 = ["0" for i in range(81)]
    for i in board1:
        l1[i//9] = str(i%9+1)
    for i in range(9):
        print("".join(l1[i*9:i*9+9]))

# read board from file
board = []
with open("test3.txt", "r", encoding="utf-8") as file:
    text = file.read()
    m = re.search(P, text)
    if m is not None:
        b = m.group()[5:]
        for r in range(9):
            for c,j in enumerate(b[10*r+1:10*r+10]):
                if j!=" ":
                    board.append(r*81+c*9+int(j)-1)
print(board)

t1 = time()

rows = set(range(729))
columns = set(range(324))
columns_head = [9 for i in range(324)]
for nu in board:
    rc = cal_col(nu)
    for c in rc:
        if c in columns:
            columns.remove(c)
            for r in cal_row(c):
                if r in rows:
                    rows.remove(r)
                    for c3 in cal_col(r):
                        columns_head[c3] -= 1

print(solven(rows, columns, columns_head, board, None, -1))
print(f"Overall time: {time()-t1}s")
