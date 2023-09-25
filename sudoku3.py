# board:
#     a  b  c  d ...
# A [[0, 0, 0, 0 ... ]
# B  [0, 0, 0, 0 ... ]
# ... ...            ]]
# pos:[r,c]

# ideas
# allow and deny list
# remember relation between grids
# for example, a row must have all of 1-9, and each pair can't have the same
# and it must be able to split

# to do:
# stdrule
# how to split rule

# idea 2:
# variable
# for instance, Aa can be x1 = [1,2,3...]
# Ab = [1,2,3,4...] - x1  --> x2
# Ba = [1,2,3...] -x1 -x2 -->x3
# make it so that no loop exist in defination of xn
# when x2 change, for example set to 1
# first solve x1!=1, and update it
# and then update x3, so it can update it's parents





# class Grid:
#     """each place in sudoku"""
#     def __init__(self, pos, value=0):
#         self.pos = pos
#         self.value = value
#         self.rules = []
#         self.moved = False
    
#     def set(self, value):
#         """change the value and updating all the rules"""
#         self.value = value
#         for i in self.rules:
#             i.update(self, value)

#     def __str__(self):
#         return "ABCDEFGHI"[self.pos[0]] + "abcdefghi"[self.pos[1]] +\
#                str(self.value)

# class Board:
#     """a collection of Grid objects"""
#     def __init__(self) -> None:
#         self.grids = [[Grid((r,c)) for c in range(9)] for r in range(9)]
#         self.rules = []
#         for r in self.grids:
#             self.rules.append(Rule(r, list(range(1,10))))
#         for c in zip(*self.grids):
#             self.rules.append(Rule(list(c), list(range(1,10))))
#         for i in range(9):
#             rgrids = []
#             for j in range(9):
#                 rgrids.append(self.grids[i//3*3+j//3][i%3*3+j%3])
#             self.rules.append(Rule(rgrids, list(range(1,10))))

#     def set(self, pos, value):
#         self.grids[pos[0]][pos[1]].set(value)
#         self.grids[pos[0]][pos[1]].moved = True

class Variable:
    def __init__(self) -> None:
        pass

# Test = True
# if not Test:
#     board = Board()

#     in1 = input()
#     if in1 == "start":
#         print("Aa1", flush=True)
#         board.set((0,0), 1)
#         in2 = input()
#     else:
#         in2 = in1

#     while in2!="Quit":
#         # make moves
#         pass
