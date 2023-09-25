# board:
#     a  b  c  d ...
# A [[0, 0, 0, 0 ... ]
# B  [0, 0, 0, 0 ... ]
# ... ...            ]]


board = [[0 for i in range(9)] for j in range(9)]

in1 = input()
if in1 == "start":
    print("Aa1", flush=True)
    board[0][0] = 1
    in2 = input()
else:
    in2 = in1

while in2!="Quit":
    # make moves
    pass
