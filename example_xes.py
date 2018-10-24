from copy import copy, deepcopy
from pattern_printer import Paper, translated

# def xcross(n, char="*"):
#     """Generate Paper with a big X with size n*n made up with char"""
#     paperout = Paper() # generate a blank Paper
#     paperout.switch2dict() # start working with paperdict
#     for i in range(n):
#         for j in range(n):
#             if i == j or i + j == n - 1: 
#                 paperout.paperdict[(i+1, j+1)] = char # add char to paperdict to form the X
#     paperout.refresh() # sort and synchronize contents inside paperdict and paperlist
#     return paperout


# equivalent to
def xcross(n, char="*"):
    """Generate Paper with a big X with size n*n made up with char"""
    paperout = Paper() # generate a blank Paper
    paperout.switch2list() # start working with paperdict
    paperout.paperlist = [ [[i+1, j+1], char]
    for i in range(n)
    for j in range (n)
    if i == j or i + j == n - 1]
    paperout.refresh() # sort and synchronize contents inside paperdict and paperlist
    return paperout


paperout = Paper()
m = 5
paperout.switch2list()
paperout.paperlist = xcross(m*2-1, char='a').paperlist # add the 1st X
paperout.paperlist+=translated(xcross(m, char='b'), [0, m*2-2]).paperlist # add the 2nd X
paperout.paperlist+=translated(xcross(m, char='c'), [m-1, m*2-2]).paperlist # add the 3rd X
paperout.paperlist+=translated(xcross(m*2-1, char='d'), [0, m*3-3]).paperlist # add the 4th X
# print(paperout.paperlist) # just for testing (print paperlist)
# paperout.refresh() # for testings below (print paperdict and paperlist)
# print()
# print(paperout.paperlist) # just for testing
print(paperout.sprint(fill_right=True)) #print them all out
# fill_right=True is additional, it is used to test the fill_right code.
