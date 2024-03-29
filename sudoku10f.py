# 10 started from scratch for competetion
# only efficency is considered

from time import time

def cal_col(rp):
    """calculate which rules num is in"""
    rn = rp//81
    cn = rp//9%9
    nn = rp%9
    r1 = rn*9 + cn
    r2 = rn*9 + nn + 81
    r3 = cn*9 + nn + 162
    r4 = rn//3*27 + cn//3*9 + nn + 243
    return r1,r2,r3,r4

def cal_row(rc):
    """calculate which numbers rule col include"""
    if rc<81:
        return (rc*9+i for i in range(9))
    rc -= 81
    if rc<81:
        con = rc//9*81 + rc%9
        return (con+i*9 for i in range(9))
    rc -= 81
    if rc<81:
        return (rc+81*i for i in range(9))
    rc -= 81
    con = rc//27*243+rc//9%3*27+rc%9
    return (con+i//3*81+i%3*9 for i in range(9))

def to_int(movep):
    """translate a move to row"""
    return "ABCDEFGHI".index(movep[0])*81+"abcdefghi".index(movep[1])*9+\
    int(movep[2])-1

def from_int(rp):
    """generate Aa1... from row num"""
    return "ABCDEFGHI"[rp//81]+"abcdefghi"[rp//9%9]+str(rp%9+1)

def set_values(rrows, rcolumns, col_head, row_nums, sboard):
    """set the row_nums to true
    new: also make moves that are certain
    assume no prior certain(col_head=1) exist"""
    while row_nums:
        nu = row_nums.pop(0)
        if nu in rrows:
            sboard.append(nu)
            rc = cal_col(nu)
            redcol = set()
            for c in rc:
                if c in rcolumns:
                    rcolumns.remove(c)
                    for r in cal_row(c):
                        if r in rrows:
                            rrows.remove(r)
                            for c3 in cal_col(r):
                                col_head[c3] -= 1
                                redcol.add(c3)
            # col_head=1 mean it's not remove(no row added to solution)
            # and that the remaining row is True. So as long as col_head -=1
            # is together with col remove, we should be fine
            for c in redcol:
                if col_head[c] == 1:# certain
                    for r in cal_row(c):
                        row_nums.append(r)
                        # check in rrows will come in next iter,
                        # so does check dupe as rrows get removed

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

def solve2(rrows, rcolumns, col_head, sboard, row=None, n=2):
    """find if it has 0,1 or 2 or more solution"""
    if n == 0:
        print("Hi1") # shouldn't be called
        return 0,[]
    if len(rcolumns) == 0:
        print("Hi2")
        return n-1,[]
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
        twos = []
    else:
        no = n
        mc = min(rcolumns, key=lambda c:col_head[c])
        if col_head[mc] != 0:
            col = mc
            for r1 in cal_row(col):
                if r1 in rrows:
                    n, twos = solve2(rrows, rcolumns,col_head, sboard, r1, n)
                    if n == 0:
                        break
            if no-n == 2:
                # This row has 2 solution
                twos.append(row)
        else:
            twos = []
    if row is not None:
        sboard.pop()
        for c1 in pc:
            rcolumns.add(c1)
        for r1 in pr:
            rrows.add(r1)
            for c2 in cal_col(r1):
                col_head[c2] += 1
    return n, twos

def simpifle1(rrows, rcolumns, col_head, sboard):
    """simpily check for those columns with only one elements"""
    while True:
        if len(rcolumns) == 0:
            return
        mc = min(rcolumns, key=lambda c:col_head[c])
        if col_head[mc] == 1:
            col = mc
            for r1 in cal_row(col):
                if r1 in rrows:# There should be only one
                    sboard.append(r1)
                    for c1 in cal_col(r1):
                        if c1 in rcolumns:
                            for r2 in cal_row(c1):
                                if r2 in rrows:
                                    rrows.remove(r2)
                                    for c2 in cal_col(r2):
                                        col_head[c2] -= 1
                            rcolumns.remove(c1)
        else:
            break

def simpifle2(rrows, rcolumns, col_head, sboard):
    """check if all move has two solutions
    if not, delete the row and solven, but only when mc=1(simpifle1)
    require there to be no mc=1 beforehand"""
    unchecked = rrows.copy()
    while unchecked:
        # check solven
        row = unchecked.pop()
        n, twos = solve2(rrows, rcolumns, col_head, sboard, row, n=2)
        if n == 0: # ok
            for r in twos:
                if r in unchecked:
                    unchecked.remove(r)
            continue
        if n == 1:
            #return solution
            return row
        # remove row and make confirmed moves
        rrows.remove(row)
        for c1 in cal_col(row):
            col_head[c1] -= 1
            # assuming there is still a solution, col_head couldn't be zero
            # unless a row that is possible was removed, at which it will be
            # removed from rcolumns
            if col_head[c1] == 1:
                set_values(rrows, rcolumns, col_head, [c1], sboard)
    return None

# def check_solutions(rrows, rcolumns, col_head, check_vals, sboard, row=None):
#     """Check if all move grant two solutions
#     Method one: check if all rows appears twice in a non-repeating search
#     solven's argithrim is non-repeating, but that only allow branch at the
#     branch with least branches"""
#     # Is it possible to do it faster?
#     # for some combination 1,2,3,4 and check if there is a number that appeared only
#     # once at a position, at most need 24 check
#     # test case: 124 132 122 243 233 231 234 213 334 222
#     # solven: 122 124 132 213 222 231 233 234 243 334
#     # 301 602 103 004 111 312 513 114 121 322 323 324
#     # for soduko that is 9**3*2=1458
#     # let's just try solven
#     # check_vals is dict with keys being to_check
#     #
#     # if n == 0:
#     #     print("Hi1") # shouldn't be called
#     #     return 0
#     # if len(rcolumns) == 0:
#     #     print("Hi2")
#     #     return n-1
#     if row is not None:
#         pc = set()
#         pr = set()
#         sboard.append(row)
#         for c1 in cal_col(row):
#             if c1 in rcolumns:
#                 for r1 in cal_row(c1):
#                     if r1 in rrows:
#                         rrows.remove(r1)
#                         pr.add(r1)
#                         for c2 in cal_col(r1):
#                             col_head[c2] -= 1
#                 rcolumns.remove(c1)
#                 pc.add(c1)
#     if len(rcolumns) == 0:
#         # n = n-1
#         for r1 in sboard:
#             if r1 in check_vals:
#                 check_vals[r1] += 1
#     else:
#         mc = min(rcolumns, key=lambda c:col_head[c])
#         if col_head[mc] != 0:
#             col = mc
#             for r1 in cal_row(col):
#                 if r1 in rrows:
#                     check_solutions(rrows, rcolumns,col_head, check_vals, sboard, r1)
#     if row is not None:
#         sboard.pop()
#         for c1 in pc:
#             rcolumns.add(c1)
#         for r1 in pr:
#             rrows.add(r1)
#             for c2 in cal_col(r1):
#                 col_head[c2] += 1



t1 = time()
rows = set(range(729))
columns = set(range(324))
columns_head = [9 for i in range(324)]
board = []
while True:
    ins = input()
    if ins == "Quit":
        break
    if ins == "start":
        set_values(rows, columns, columns_head, [0], board)
        print("Aa1", flush=True)
        continue
    move = to_int(ins)
    set_values(rows, columns, columns_head, [move], board)
    # Simplify
    # 1.Check if all elements in rows has 1 solutions
    # remove those that are not
    # remove rules with only one element as well
    # check if they have two solutions
    # if not, do it and win
    # if a location has only one solution, steps should remove them
    win = simpifle2(rows, columns, columns_head, board)
    if win is not None:
        if win in rows:
            print(from_int(win)+"!", flush=True)
        else:
            print("!")
        continue
    move = rows.pop()
    rows.update((move,))
    print(from_int(move))
    set_values(rows, columns, columns_head, [move], board)
    # do something


# first game played against me(I had sudoku10c)

# start
# Aa1
# Ab2
# Bh1
# Ac3
# Ad4
# Ae5
# Fa9
# Af6
# Bi5
# Ag9
# Ca6
# Af6
# Ba8
# Gc6
# Cb5
# Ga3
# Fe2
# Hh4
# Cd7
# Ei1
# Ce1
# Ie9
# Ff1
# Dd6
# Cg4
# Ge7
# Ch2
# Id1
# Fb3
# Ic2
# Gb4
# Dg3
# Dc7!
# Quit
