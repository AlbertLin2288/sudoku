# well well well we meet again
# Turns out the deadline is further than I expected
# With a test week coming on, I'll have a lot of free time(don't judge me
# on my lack of preparation)
# And another twist is VS code is extremely slow, so my estimation time
# of about 150 seconds per game(definately time out) turn into less than
# 5 seconds per game(on my computer, may be slower). This leave a lot of
# room for improvement
# Current play is to submit the sudokuh after some more testing, and try
# to work on improving it by adding a endgame feature.

# in order to detect endgame, we need a way of measuring freedom of movement
# we can also consider the time we have and work backward.
# one step before victory, solven can do that in little time
# three steps before, the best move is one allow no immediate win
# which is achieved in the program
# five steps before,
#
# Nevermind, the new stragety including a measurment of randomness and
# pure brute force.
# First we devise a way to roughly measure how many possiblities are left
# Then we calculate all possiblity
# Then we makes move with best outcome, with another unknow method of scoring
#
# The plan so far, now that there's only 2 and a half days left is the
# following:
# 1. Complete the method for the stragety
# 2. Since some constant will be required, conduct experiment to measure them
# 3. Test if the new version acturally have better score
# 4. Submit the improved version if not too late
# 5. Convert the improved version to C++
# 6. Measure new speed, thus changing the constant
# 7. Debug
# 8. Submit c++ version
#
# Note: the new version would be slower, hence a variable exist to measure time
# left and decide when to go into final phase. since c++ is proably faster,
# it would acturally be useful to use it.
#
#
# To measure number of possiblities, heres the data we can use:
# amount of determinated/undeterminated rows/columns/colhead sum
# number of solutions AFTER simpifly 22(hence less efficent)
#
# Brute force to get all possibilty is easy, just use solven(-1)
# But how do we find the best move?
#
# I have been reading old things I wrote in sudoku10d, something I
# forgot to commit to github.
# anyway here's some thought:
#
# Brute force best move:
# make a graph
# top row is all solution
# second row is all solution removing one row
# merge nodes that are the same
# keep doing this and you should have a complex graph
# now on the top row everyone get a name
# on the second and below row for every nodes:
#   for all above row nodes it's connected to:
#       if it's connected to a node that has a name
#           if it doesn't already has one, get the same name,
#               and mark this as win
#           else remove the name(unless the names are the same)
#       if there is one node that is marked as lost, also mark as winning node
#   if it's not marked as win, mark as lose.
#
# a scoring system can be added:
#   those with name has score set to 0,1 regardless
#   for every above node without name and marked as win, add their score,
#       but with win/lost reversed
#   that's all, good luck.
#
