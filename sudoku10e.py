# Just a example program for checking if it could work

# to do: add a way to not delete certainty
# Failed misreablely

from time import time
ttotal = 0
t1 = time()

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

def to_int(move):
    """translate a move to row"""
    return "ABCDEFGHI".index(move[0])*81+"abcdefghi".index(move[1])*9+\
    int(move[2])-1

def from_int(row_num):
    """generate Aa1... from row num"""
    return "ABCDEFGHI"[row_num//81]+"abcdefghi"[row_num//9%9]+str(row_num%9+1)

def solvenc(rrows, rcolumns, col_head, sboard, cboard, row=None, n=1):
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
    certain = 0 # 0: no solution sofar, >1: solution row
    if len(rcolumns) == 0:
        n = n-1
    #     if not check_error(sboard):
    #         raise ValueError("Board not possible")
    #     print_board(sboard)
    #     print("\n")
    else:
        mc = min(rcolumns, key=lambda c:col_head[c])
        if col_head[mc] != 0:
            col = mc
            for r1 in cal_row(col):
                if r1 in rrows:
                    total = n
                    cboard2 = []
                    n = solvenc(rrows, rcolumns,col_head, sboard, cboard2, r1, n)
                    if n == 0:
                        certain = -1
                        break
                    if certain != -1 and total != n:
                        if certain == 0:
                            certain = r1
                            cboard3 = cboard2[:]
                        else:
                            certain = -1
        if certain>0:
            cboard.append(certain)
            for i in cboard3:
                cboard.append(i)
    if row is not None:
        sboard.pop()
        for c1 in pc:
            rcolumns.add(c1)
        for r1 in pr:
            rrows.add(r1)
            for c2 in cal_col(r1):
                col_head[c2] += 1
    return n

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

def set_values(rrows, rcolumns, col_head, row_nums):
    """set the row_nums to true"""
    for nu in row_nums:
        if nu in rrows:
            rc = cal_col(nu)
            for c in rc:
                if c in rcolumns:
                    rcolumns.remove(c)
                    for r in cal_row(c):
                        if r in rrows:
                            rrows.remove(r)
                            for c3 in cal_col(r):
                                col_head[c3] -= 1

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

rows = set(range(729))
columns = set(range(324))
columns_head = [9 for i in range(324)]
board = []

running = True
length = 0
while running:
    ttotal += time() - t1
    ins = input()
    t1 = time()
    if ins == "Quit":
        running = False
        break
    if ins == "start":
        m = 0
        print(from_int(m),flush=True)
        length = 1
        board.append(m)
        set_values(rows, columns, columns_head, (m,))
        solvenc(rows, columns, columns_head, board[:], board)
        set_values(rows, columns, columns_head, board[length:])
        continue
    ins = to_int(ins)
    board.append(ins)
    length = len(board)
    set_values(rows, columns, columns_head, (ins,))
    solvenc(rows, columns, columns_head, board[:], board)
    set_values(rows, columns, columns_head, board[length:])
    good = False
    for r5 in range(729):
        if r5 in rows:
            rem = solven(rows, columns, columns_head, board, r5, 2)
            if rem == 1: # there is only one unique solution left
                m = r5
                break
            if not good and rem == 0: # more than one solution down that road
                # step one: check for reduction of possibility
                cm = min(cal_col(r5),
                         key=lambda x:rows.intersection(cal_row(x)))
                for r6 in cal_row(cm):
                    if not solven(rows, columns, columns_head, board, r6):
                        break
                else:
                    m = r5

    print(from_int(m),flush=True)
    board.append(m)
    set_values(rows, columns, columns_head, (m,))
    length = len(board)
    solvenc(rows, columns, columns_head, board[:], board)
    set_values(rows, columns, columns_head, board[length:])



print(f"Overall time: {ttotal}s")
