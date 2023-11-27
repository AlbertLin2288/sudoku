# restart again
# I think I could finished the previous one, but I'm out of brain cell
# to figure out how to check how many(I mean if) solutions are left.
# I know I said I can check it by setting every cell to possible number,
# but I perfer not wasting too much time on that, as dispite taking little
# time to solve a sudoku, victory rely on doing more calculation than
# you oppponante, so time is money.
# Therefore, I've been studing mathamatic of sudoku on wikipedia, and will
# be doing it this way unless time run out(for me, not the program).
# For now, this will just be my note, as I hope not to forget everything
# I've learned and having to restudy everytime.
#
#
#
# Exact cover problem is:
# S is a set of subsets of X, and X is just a set. find subset S* of S,
# such that S*, after flattening, is equal to X
# Exact hitting problem is:
# S is a set, X is a set of subsets of S, find subset S* of S, such that
# every elements in X include exact one element in S*
#
# Those two are the same because for exact hitting problem, let S' be
# S, but every element replaced with all elements in X that include it.
# Now stop viewing elements in X as set, and S' will be set of subsets
# of X. Now the problem become find subset S*' of S', such that
# (since every element in X include exact one element in S*, and S*'
# has elements replaced, include become included, so) every elements
# in X is included in exactly one element in S*'. And as all s*'ϵX,
# S*' is an exact cover of X.
#
# I used to love math before writing those
#
#
# For exact hitting, you(Yes, I use "you" when talking to myself) can imagine
# X as rules, where every element in x can appear only once in solution S*
# S = {Aa1, Aa2, Aa3 ... Aa9, Ab1, Ab2, ...}
# So we(Why did I use we this time? I don't know, this is just what I do when I
# sit in the corner talking to myself) need to find S* somewhat like this:
# (just an example) {Aa1, Ab2, Ac5, Ad3 ...}
# Rules include:
#   Include exactly one of Aa1, Aa2 ... (no dupe nor absent)
#   Include exactly one of Aa1, Ab1 ... (rules for rows)
#   Include exactly one of Aa1, Ba1 ... (rules for columns)
#   Include exactly one of Aa1, Ab1 ... (note: this is not for rows,
#                                        it's for blocks)
# And with them we can easily create X
#
