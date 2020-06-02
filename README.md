# pattern-printer
A python program to create and transform character patterns without counting spaces.

## Structure
This program contains a class `Paper` to accept characters and their positions. Inside `Paper` there is a dictioary `paperdict` and a list `paperlist`. `paperdict` contains the characters and use their position as the keys, and `paperlist` is made up of lists made up of the list of `[<position>, <character>]`. Characters can be added to `paperdict` and transformed in `paperlist` a function `sprint` will produce the strings from these characters.
For example,
```
>>> from pattern_printer import Paper
>>> paperout = Paper()
>>> paperout.switch2dict()
>>> paperout.paperdict[(1, 1)] = 'a'
>>> paperout.paperdict[(2, 2)] = 'b'
>>> paperout.paperdict[(1, 3)] = 'c'
>>> paperout.paperdict
{(1, 1): 'a', (2, 2): 'b', (1, 3): 'c'}
>>> paperout.switch2list()
>>> paperout.paperlist
[[[1, 1], 'a'], [[1, 3], 'c'], [[2, 2], 'b']]
>>> print(paperout.sprint())
a c
 b
```

It was my first little repo, created when I was trying git and GitHub for the first time.
It was not something practical, but a little Python module to deal with the pattern-printing exercises in the programming course I had be enrolled. 
Any advice is welcome, and please feel tell me if there is anything wrong or improper here.
