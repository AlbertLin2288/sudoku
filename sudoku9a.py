"""The 9th attmpt in this"""
# to test if it works
import random
P = 0.2
# has_rule: [value, {child_value:{children id...}...} Numbers...]

VALUES = (1, 2, 3, 4, 5, 6, 7, 8, 9)

class Sudoku:
    """The board and rules"""
    def __init__(self, copy=None) -> None:
        """if copy, become a copy of copy""" 
        if copy is None:
            self.board = [[Number(self, r, c) for c in range(9)]
                           for r in range(9)]
            self.flat_board = [self.board[i//9][i%9] for i in range(81)]
            self.has_rules = {} # {id:[value, children_ids, Number...]}
                                # must have one number = value
            self.id = 0 # largest unused id
            self.has_ids = []
            for r in range(9): # add rules to rows
                has_rules = {} # group of same has_rules
                for i in VALUES: # add rules to group, Numbers done
                    has_rules[self.id] = \
                        [i, {j:set() for j in VALUES if j!=i}] +\
                            self.flat_board[r*9:r*9+9]
                    self.id += 1
                for i, has_rule in has_rules.items():
                    self.has_rules[i] = has_rule # add rule to self
                    for j,k in has_rules.items():
                        if k[0] != has_rule[0]:
                            has_rule[1][k[0]].add(j)
                    for num in has_rule[2:]:
                        num.has_rules[i] = has_rule
                no_dupe = self.flat_board[r*9:r*9+9]
                for num in no_dupe:
                    num.no_dupe_rule.update(no_dupe)
            for c in range(9): # add rules to columns
                has_rules = {}
                for i in VALUES:
                    has_rules[self.id] =\
                        [i, {j:set() for j in VALUES if j!=i}] +\
                            self.flat_board[c::9]
                    self.id += 1
                for i, has_rule in has_rules.items():
                    self.has_rules[i] = has_rule
                    for j,k in has_rules.items():
                        if k[0] != has_rule[0]:
                            has_rule[1][k[0]].add(j)
                    for num in has_rule[2:]:
                        num.has_rules[i] = has_rule
                no_dupe = self.flat_board[c::9]
                for num in no_dupe:
                    num.no_dupe_rule.update(no_dupe)
            for block in range(9): # for each block
                has_rules = {}
                for i in VALUES:
                    has_rule = [i, {j:set() for j in VALUES if j!=i}]
                    has_rules[self.id] = has_rule
                    self.has_rules[self.id] = has_rule
                    for p in range(9): # the cord in the flattened block
                        number = self.board[block//3*3+p//3][block%3*3+p%3]
                        has_rule.append(number)
                        number.has_rules[self.id] = has_rule
                    self.id += 1
                for i, has_rule in has_rules.items():
                    for j,k in has_rules.items():
                        if k[0] != has_rule[0]:
                            has_rule[1][k[0]].add(j)
                no_dupe = [self.board[block//3*3+p//3][block%3*3+p%3]
                           for p in range(9)]
                for num in no_dupe:
                    num.no_dupe_rule.update(no_dupe)
        else:
            # make self a deepcopy of copy
            self.init_as_copy(copy)

    def init_as_copy(self, copy):
        """init as a deepcopy of copy"""
        self.board = []
        self.has_rules = {}
        self.id = copy.id
        self.has_ids = copy.has_ids[:]
        for r in range(9):
            row = []
            for c,i in enumerate(copy.board[r]):
                num = Number(self, r, c)
                num.isset = i.isset
                row.append(num)
            self.board.append(row)
        self.flat_board = [self.board[i//9][i%9] for i in range(81)]
        for i in copy.has_rules: # copy has_rules for board
            has_rule = [copy.has_rules[i][0]]
            children = {j:k.copy() for j,k in copy.has_rules[i][1].items()}
            has_rule.append(children)
            for j in copy.has_rules[i][2:]:
                has_rule.append(self.flat_board[j.pos])
            self.has_rules[i] = has_rule
        for i,num in enumerate(self.flat_board):
            for j in copy.flat_board[i].has_rules: # copy has_rules for Number
                num.has_rules[j] = self.has_rules[j]
            for j in copy.flat_board[i].no_dupe_rule: # copy no_dupe rules
                num.no_dupe_rule.add(self.flat_board[j.pos])
            num.possible = copy.flat_board[i].possible[:]

    def set_number(self, pos, value):
        """set pos to value"""
        if isinstance(pos, str):
            self.board["ABCDEFGHI".index(pos[0])]\
                ["abcdefghi".index(pos[1])].set(value)
        elif isinstance(pos, int):
            self.flat_board[pos].set(value)
        elif isinstance(pos, tuple):
            self.flat_board[pos[0]*9+pos[1]].set(value)

    def input(self, value):
        """used in game"""
        self.set_number(value[:2], int(value[2]))

    def has_rule_true(self, has_id):
        """has_rule is satisifled, so delete it"""
        if has_id in self.has_rules:
            if has_id == 90:
                pass
            has_rules = self.has_rules.pop(has_id)
            for i in has_rules[2:]:
                i.has_rules.pop(has_id)

    def error(self, message="Error"):
        """an error has occured"""
        raise ValueError(message)
    
    def __eq__(self, value) -> bool:
        if isinstance(value, Sudoku):
            if any((not i.eq(j)
                     for i,j in zip(self.flat_board,value.flat_board))):
                return False
            if len(self.has_rules) != len(value.has_rules):
                return False
            hr1 = list(self.has_rules.values())
            hr2 = list(value.has_rules.values())
            for i in hr1:
                for j in hr2:
                    if i[0] == j[0] and len(i) == len(j) and\
                        all((hr1[k].pos == hr2[k].pos for k in range(len(i)-2))):
                        break
                else:
                    return False
            for i in hr2:
                for j in hr1:
                    if i[0] == j[0] and len(i) == len(j) and\
                        all((hr1[k].pos == hr2[k].pos for k in range(len(i)-2))):
                        break
                else:
                    return False
            return True
        return False


class Number:
    """The number"""
    def __init__(self, board:Sudoku, r, c) -> None:
        self.board = board
        self.pos = r*9+c
        # self.r, self.c = r, c
        # unused
        self.name = "ABCDEFGHI"[r]+"abcdefghi"[c]
        self.has_rules = {}
        self.no_dupe_rule = set() # only Number now
        self.possible = [1,2,3,4,5,6,7,8,9]
        self.isset = False

    def set(self, value):
        """replace self with int"""
        # to do: replace self with int
        if self.isset:
            if self.possible[0] != value:
                self.board.error(f"Can't set {self.name} to {value},"+\
                                 f" it's already set to {self.possible[0]}")
        else:
            self.set2(value)

    def remove(self, value):
        """remove value as a possibility
        used when set value(removing every other value) 
        and when conflicking"""
        if value not in self.possible:
            return False
        self.possible.remove(value)
        if len(self.possible) == 0:
            self.board.error(f"removing {str(value)} from {self.name} "+\
                             "when it's the only possibility.")
            # don't think this is going to happen
        for i,has_rule in self.has_rules.copy().items():
            if has_rule[0] != value:
                continue
            # has_rule without value won't be affected
            has_rule.remove(self)
            self.has_rules.pop(i)
            if i in self.has_rules:
                self.has_rules.pop(i)
            if len(has_rule) == 2:
                self.board.error(f"Removing {str(value)} from " +\
                                 f"{self.name} cause " +\
                                 f"has_rule {i} to has fail.")
                continue
            if len(has_rule) == 3:
                self.board.has_rule_true(i)
                has_rule[2].set2(has_rule[0])
                continue
            has_rules = self.has_rules.keys()
            for j in has_rule[1].copy().keys(): # update has_rule's child
                # if removal of self cause a child of has_rule to
                # no longer be a child, there must be a value in child that
                # is no longer in has_rule.
                # the only value removed from has_rule is self
                # therefore child must include self and isn't removed
                # since child has different value, that is garunteened
                # but child, since it include self, must be in self.has_rules
                for has_rule2_id in has_rule[1][j].intersection(has_rules):
                    has_rule[1][j].discard(has_rule2_id)
                if len(has_rule[1][j]) == 0: # no longer has child has_rule j
                    has_rule[1].pop(j)
            parents = set(has_rule[2].has_rules.keys()) # update parents
            for num in has_rule[3:]: # parents must be in all has_rules number
                parents.intersection_update(num.has_rules.keys())
            for has_rule2_id in parents: # add has_rule to parent
                if has_rule2_id == i:# the parent happen to be itself
                    continue
                if has_rule[0] in self.board.has_rules[has_rule2_id][1]:
                    self.board.has_rules[has_rule2_id][1][has_rule[0]].add(i)
                elif has_rule[0] == self.board.has_rules[has_rule2_id][0]:
                    self.board.has_rule_true(has_rule2_id)
                else:
                    self.board.has_rules[has_rule2_id][1][has_rule[0]] = {i}
            # check if number of child values exceed number of Number
            if len(has_rule[1]) > len(has_rule) - 2:
                self.board.error(f"More children of rule {i} than its Number"+\
                                 f" when {value} is removed from {self.name}")
            # futher update rule

        if len(self.possible) == 1: # self is determinted
            self._set3()
        return True

    def set2(self, value):
        """set self to value"""
        if value not in self.possible:
            self.board.error(f"can't set {self.name} to {value}")
        for i in self.possible[:]:
            if i == value:
                continue
            self.remove(i)

    def _set3(self):
        """self has already only 1 possible"""
        self.isset = True
        # print(f"{self.name} is set")
        value = self.possible[0]
        for i in self.no_dupe_rule.copy(): # handeling those that conflic with self
            # they no longer need to worry about duping with self
            # and no longer can be value
            if i is self:
                continue
            i.no_dupe_rule.discard(self)
            i.remove(value)
            self.no_dupe_rule.discard(i)
        for i, has_rule in self.has_rules.copy().items():
            # satisifling has_rules
            if has_rule[0] == value:
                self.board.has_rule_true(i)
                continue
            # I don't think it's possible
            # as has_rules should be removed when possible is reduced
            # so I'll leave it here for easier discovery of bugs
            raise ValueError("HI")
    
    def eq(self, value) -> bool:
        if isinstance(value, Number):
            if self.possible != value.possible:
                return False
            return True
        return False


class Game:
    """a class to test if Sudoku is good enough"""
    def __init__(self) -> None:
        self.s1 = Sudoku()

    def set1(self, pos, value):
        """just set a value"""
        s2 = Sudoku(self.s1)
        s2.set_number(pos, value)
        self.s1 = s2

    def check1(self):
        """check if isset is always interexchangable to no other solution
        isset => 1 solve(easier) <==> more solve => not isset: True as 
            isset is only True from _set3, from set2, when len(possible)==1
        1 solve => isset <==> not isset => more solve(easier)"""
        for i in range(81):# do check2 first
            if not self.s1.flat_board[i].isset:
                possible = 0
                for j in VALUES:
                    try:
                        s2 = Sudoku(self.s1)
                        s2.set_number(i, j)
                        if possible:
                            possible = 2
                            break
                        possible = 1
                    except ValueError:
                        pass
                if possible == 1:
                    return False
                if possible == 0:
                    raise ValueError("Why?")
        return True


    def set2(self, pos, value):
        """check if possibiliy decrease
        and if sudoku change
        petty sure if sudoku doesn't change per check1 possiblity stay"""
        s2 = Sudoku(self.s1)
        s2.set_number(pos, value)
        if s2 == self.s1:
            return False
        if look_for_dif(self.s1, s2):
            return True
        raise ValueError("different result")

def check2(s1):
    """check if all possible are indeed possible
    to much to try, so random"""
    for i in range(81):
        if random.random()<P and not s1.flat_board[i].isset:
            try:
                s2 = Sudoku(s1)
                choice = random.choice(s2.flat_board[i].possible)
                s2.set_number(i, choice)
                success = check2(s2)
                if not success[0]:
                    return False, "ABCDEFGHI"[i//9]+"abcdefghi"[i%9]+\
                        str(choice)+" "+ success[1], success[2]
            except ValueError as e:
                print(e)
                print(f"set {str(i)} to {choice}")
                return False, "ABCDEFGHI"[i//9]+"abcdefghi"[i%9]+str(choice), s1
    return (True,)

def look_for_dif(s1, s2):
    """return if s1 has more solve than s2
    assume it's impossible to be reverse"""
    for i in range(81):
        if len(s1.flat_board[i].possible) > len(s2.flat_board[i].possible):
            # more possible in s1 than s2 at i
            return True
        if not s1.flat_board[i].isset:
            # the same and not isset
            for j in s1.flat_board[i].possible:
                s3 = Sudoku(s1)
                s4 = Sudoku(s2)
                try:
                    s3.set_number(i,j)
                    try:
                        s4.set_number(i,j)
                    except ValueError:
                        return True
                except ValueError:
                    continue
                dif = look_for_dif(s3, s4)
                if dif:
                    return True
    return False
