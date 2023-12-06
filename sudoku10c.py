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
        return n-1
    mc = min(rcolumns, key=lambda c:col_head[c])
    if col_head[mc] != 0:
        col = mc
        for r1 in cal_row(col):
            if r1 in rrows:
                n = solven(rrows, rcolumns,col_head, sboard, r1, n)
                if n == 0:
                    return 0
    if row is not None:
        sboard.pop()
        for c1 in pc:
            rcolumns.add(c1)
        for r1 in pr:
            rrows.add(r1)
            for c2 in cal_col(r1):
                col_head[c2] += 1
    return n


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
                    if r==11:
                        pass
                    for c3 in cal_col(r):
                        columns_head[c3] -= 1

print(solven(rows, columns, columns_head, board, 1))
print(f"Overall time: {time()-t1}s")
