#! /usr/bin/env python3
from pattern_printer import Paper
paperout = Paper()
paperout.switch2dict()
paperout.paperdict[(1, 1)] = 'a'
paperout.paperdict[(2, 2)] = 'b'
paperout.paperdict[(1, 3)] = 'c'
paperout.paperdict
paperout.switch2list()
paperout.paperlist
print(paperout.sprint())
