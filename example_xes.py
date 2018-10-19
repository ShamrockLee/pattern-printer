from copy import copy, deepcopy
from pattern_printer import Paper
def xcross(n, char="*"):
    paperout = Paper()
    paperout.switch2dict()
    for i in range(n):
        for j in range(n):
            if i == j or i + j == n - 1: 
                paperout.paperdict[(i+1, j+1)] = char
    paperout.refresh()
    return paperout
paperout = Paper()
m = 5
paperout.switch2list()
paperout.paperlist = xcross(m*2-1, char='a').paperlist
paperout.paperlist+=Paper.translated(xcross(m, char='b'), [0, m*2-2]).paperlist
paperout.paperlist+=deepcopy(Paper.translated(xcross(m, char='c'), [m-1, m*2-2])).paperlist
paperout.paperlist+= deepcopy(Paper.translated(xcross(m*2-1, char='d'), [0, m*3-3])).paperlist
#print(paperout.paperlist)
paperout.refresh()
#print()
#print(paperout.paperlist)
print(paperout.sprint(fill_right=True))
