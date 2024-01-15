# Good news, 10g worked
# Well, almost
# this is the (hopefully) final draft of the python program
# Time to delete useless things and conduct more testing

from time import time
import sys

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

def hashable_board(sboard):
    """make the board hashable for easier reference
    simple join the number(1-9) together in string"""
    num_board = [0 for i in range(81)]
    for row in sboard:
        num_board[row//9] = row%9
    return "".join((str(i) for i in num_board))

def fast_int1(s):
    """translate 0-9 to int"""
    if s == "0":
        return 0
    if s == "1":
        return 1
    if s == "2":
        return 2
    if s == "3":
        return 3
    if s == "4":
        return 4
    if s == "5":
        return 5
    if s == "6":
        return 6
    if s == "7":
        return 7
    if s == "8":
        return 8
    if s == "9":
        return 9

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
                        if r in rrows:
                            row_nums.append(r)
                            # check dupe will come in next iter,
                            # as rrows get removed

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

def solvedif(rrows, rcolumns, col_head, sboard, boards, row=None, n=2):
    """find if it is possible to find more solutions not in boards
    so that len(boards) == n
    return the new solutions found in hashable form"""
    if n == 0:
        print("Hi1") # shouldn't be called
        return []
    if len(rcolumns) == 0:
        print("Hi2")
        no = len(boards)
        boards.update((hashable_board(sboard),))
        if len(boards) == no:
            return []
        return [hashable_board(sboard)]
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
        no = len(boards)
        boards.update((hashable_board(sboard),))
        if len(boards) == no:
            ret = []
        ret = [hashable_board(sboard)]
    else:
        ret = []
        mc = min(rcolumns, key=lambda c:col_head[c])
        if col_head[mc] != 0:
            col = mc
            for r1 in cal_row(col):
                if r1 in rrows:
                    dif = solvedif(rrows, rcolumns,col_head, sboard, boards, r1, n)
                    ret += dif
                    if len(boards) >= n:
                        break
    if row is not None:
        sboard.pop()
        for c1 in pc:
            rcolumns.add(c1)
        for r1 in pr:
            rrows.add(r1)
            for c2 in cal_col(r1):
                col_head[c2] += 1
    return ret

def simpify22(rrows, rcolumns, col_head, sboard):
    """Find a move that bring an instant win, or find one that isn't instant
    loses.
    check the number of solutions left for all move
    if it's 0, abandon it
    if it's 1, return True, move
    else, return False, best move
    to check number of solutions
    use solven with n=2 for a move
    save all the solution found
    if a new solution is found, add 1 solution to every move in the solution"""
    num_row = {0:rrows.copy()} # n:set pair indicate n solutions for
    # every row in set
    row_num = {i:0 for i in rrows}
    min_val = 0
    max_val = 0
    solutions = set() # all different found solutions in hashable
    while min_val<2:
        # check solven
        row = num_row[min_val].pop()
        if row == 110:
            pass
        num_row[min_val].update((row,))
        current = len(solutions)
        difs = solvedif(rrows, rcolumns, col_head, sboard, solutions,
                       row, n=current+2-min_val)
        new_val = len(solutions)-current + min_val
        if new_val == 1:
            #return solution
            return True, row
        for dif in difs:
            for p in range(81):
                r1 = p*9+fast_int1(dif[p])
                if r1 not in row_num:
                    continue
                n1 = row_num[r1]
                num_row[n1].remove(r1)
                if n1 == max_val:
                    max_val += 1
                    num_row[max_val] = {r1}
                num_row[n1+1].update((r1,))
                row_num[r1] = n1+1
        if new_val == 0:
            # remove row and make confirmed moves
            rrows.remove(row)
            for c1 in cal_col(row):
                col_head[c1] -= 1
                # assuming there is still a solution, col_head couldn't be zero
                # unless a row that is possible was removed, at which it will
                # be removed from rcolumns
                if col_head[c1] == 1:
                    for r2 in cal_row(c1):
                        if r2 in rrows:
                            set_values(rrows, rcolumns, col_head, [r2], sboard)
            if 110 not in rrows:
                pass
            row_num = {i:j for i,j in row_num.items() if i in rrows}
            num_row = {i:j.intersection(rrows) for i,j in num_row.items()}
            max_val = max(row_num.values())
        while len(num_row[min_val]) == 0:
            min_val += 1
    return False, num_row[max_val].pop()


t1 = time()
ttotal = 0
rows = set(range(729))
columns = set(range(324))
columns_head = [9 for i in range(324)]
board = []
ttotal += time() - t1
print(f"init took {str(time()-t1)} seconds, totaling " +
    f"{str(ttotal)} seconds,", file=sys.stderr)
step = 1
while True:
    ins = input()
    t1 = time()
    if ins == "Quit":
        break
    if ins == "Start":
        set_values(rows, columns, columns_head, [0], board)
        print("Aa1", flush=True)
        continue
    move = to_int(ins)
    set_values(rows, columns, columns_head, [move], board)
    win = solven(rows, columns, columns_head, board, n=2) == 1
    if win:
        print("!",flush=True)
    win, move = simpify22(rows, columns, columns_head, board)
    if win:
        print(from_int(move)+"!", flush=True)
        continue
    set_values(rows, columns, columns_head, [move], board)
    # do something
    ttotal += time() - t1
    print(f"step {str(step)} took {str(time()-t1)} seconds, totaling " +
          f"{str(ttotal)} seconds,", file=sys.stderr)
    step += 1
    print(from_int(move), flush=True)
