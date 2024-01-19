# Just a tool to check if output are error
# allow use of solven with board generated from raw move
TOBYTES = bytes.maketrans(b"",b"")
from time import time

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

def to_int(movep):
    """translate a move to row"""
    return "ABCDEFGHI".index(movep[0])*81+"abcdefghi".index(movep[1])*9+\
    int(movep[2])-1

def from_int(rp):
    """generate Aa1... from row num"""
    return "ABCDEFGHI"[rp//81]+"abcdefghi"[rp//9%9]+str(rp%9+1)

def solven(rrows, rcolumns, col_head, sboard, row=None, n=1, save=None):
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
                rcolumns.remove(c1)
                for r1 in cal_row(c1):
                    if r1 in rrows:
                        rrows.remove(r1)
                        pr.add(r1)
                        for c2 in cal_col(r1):
                            col_head[c2] -= 1
                pc.add(c1)
    if len(rcolumns) == 0:
        n = n-1
        if save is not None:
            save.append(sboard[:])
        else:
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
                    n = solven(rrows, rcolumns,col_head, sboard, r1, n, save)
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

def make_boardr(moves):
    """make a board based on moves(in row form)
    return a turple of rows, columns, columns_head and board"""
    rows = set(range(729))
    columns = set(range(324))
    columns_head = [9 for i in range(324)]
    board = moves[:]
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
    return rows, columns, columns_head, board

def make_boardm(moves):
    """make a board, but in raw game form"""
    move = [to_int(i) for i in moves]
    return make_boardr(move)

def solven2(board, n):
    """a shell for solven (row=None)"""
    save = []
    n = solven(board[0], board[1], board[2], board[3], None, n, save)
    return n, save

def force1(board, timelim=100):
    """brute force the best move
    return a complex and messy graph like list for moving
    or return None if timelim is reached"""
    # store it with minimal info required
    # make a list noting all the rows that exist.
    # actually, traditional method in expressing sudoku is more efficent
    # because they had builtin info regarding rule1
    # if a data type can enforce all 4 rules, that would reach the
    # theroatical limit, but for now, let's settle with this.
    # first note all rrows that is certain(union)
    # then every layer is a dictionary with key being hash of current
    # and value is a list with win/lose, score and parent
    #
    # if there are n block with total of m rows
    # a subset with length k(k<n) of m rrows can be expressed
    # with(if m<256) k char.
    # hence that's a better hash
    maxtime = time()+timelim
    all_solution = solven2(board, -1)[1]
    all_row = set.union(set(),*all_solution)
    same = set.intersection(set(range(729)),*all_solution)
    difference = all_row.difference(same)
    to_real = list(difference)
    from_real = {j:i for i,j in enumerate(to_real)}
    def hash2(rows):
        """hash a subset
        rows is list"""
        return b''.join((TOBYTES[i:i+1] for i in rows))
    all_solution_li = [[from_real[i] for i in j if i in to_real]
                        for j in all_solution]
    for i in all_solution_li:
        i.sort()
    if len({len(i) for i in all_solution_li}) != 1:
        raise ValueError("Error")
    l1 = len(all_solution_li[0])
    row1 = {hash2(i):[hash2(i),(0,1)] for i in all_solution_li}
    rows=[row1]
    for i in range(l1-1):
        t=time()
        if t>maxtime:
            print("Timeout")
            return None
        prv_row = rows[i]
        row = {}
        rows.append(row)
        # hash: win/lose, score
        for sol,sol_val in prv_row.items():
            for j in range(l1-i):
                new_sol = sol[:j]+sol[j+1:]
                if new_sol in row:
                    # add a node to nodelist
                    # win/lose score
                    new_sol_val = row[new_sol]
                    winlose = new_sol_val[0]
                    winlose_prv = sol_val[0]
                    if type(winlose) == bytes:
                        if type(winlose_prv) == bytes:
                            if winlose != sol:
                                new_sol_val[0] = 1
                                new_sol_val[1] = (1,0)
                        else:
                            new_sol_val[0] = 1
                            new_sol_val[1] = (1,0)
                    else:
                        if winlose == 0:
                            if type(winlose_prv) == bytes or winlose_prv==0:
                                new_sol_val[0] = 1
                        new_sol_val[1] = (new_sol_val[1][0]+sol_val[1][1],
                                          new_sol_val[1][1]+sol_val[1][0])
                    new_sol_val[2].append(sol)
                else:
                    # win/lose score
                    winlose_prv = sol_val[0]
                    if type(winlose_prv) == bytes:
                        winlose = winlose_prv
                        score = (0,1)
                    else:
                        winlose = 1 - winlose_prv
                        score = sol_val[1][1], sol_val[1][0]
                    row[new_sol] = [winlose, score, [sol]]
    return rows
# force1 was way toooooo slow
# the complexity was low in the beginning and end
# but it expand in the middle, slowing down.
#
#
# Please, god, bless me with the will to study
# https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem
# Ok let S0* be all solutions
# S0*' = {X/⋂S0*|XϵS0*}
# S0 = ⋃S0*'
# then a move mϵS0 is made
# S1* = {X|mϵX, XϵS0*'}
# and so on until one player made a move m that cause S*' to be empty and win
# Thus the last player to make a move win, so it's normal play

if __name__ == "__main__":
    a=['Aa1', 'Ha9', 'Id9', 'Gg9', 'Ff9', 'Ei9', 'Db9', 'Ch9', 'Ac9', 'Hb8',
       'Eb1', 'Gc1', 'Hc2', 'Da2', 'Ab2', 'Cg1', 'Bd1', 'Hf1', 'De1', 'Ii1',
       'Hi7', 'Hh6', 'Ci2', 'Ge2', 'Ih2', 'Ed2', 'Hd3', 'Ig3', 'Ga3', 'Hg5',
       'Ic7', 'Ie8', 'Ia4', 'If6', 'Gf7', 'Gh4', 'Dd7', 'Dh5', 'Fa7', 'Fd8',
       'Dg8', 'Cd6', 'Ec3']
    b=a[:-3]
    board2 = make_boardm(b)
    #result = force(board2, 20)
    print("",end="")
