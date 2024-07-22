#! /usr/bin/env python3

#   Happy
#  Moon
# Festival

import pattern_printer
import time
import sys
import os
import math

strings = ["Happy", "Moon", "Festival"]
nstrings = len(strings)
paper_strings = [pattern_printer.Paper() for i in range(nstrings)]

paper_circle = pattern_printer.Paper()
radius = max(len(string) for string in strings) + 3
# radius = int(math.ceil(radius * 0.75))
paper_circle.initial_position = [0, 0]
paper_circle.clear()
paper_circle.switch2dict()
star_circle = "*"
ratio_hwchar = 2
nslices_angle = radius * 4
is_clockwise = False
angle_start = math.pi / 2
get_position_circle = lambda angle: (int(round(-math.sin(angle) * radius / ratio_hwchar)), int(round(math.cos(angle) * radius)))
position_circle_start = get_position_circle(angle_start)
for i in range(nslices_angle):
    angle_current = angle_start + (2 * math.pi * i / nslices_angle) * ( -1 if is_clockwise else 1)
    position_current = get_position_circle(angle_current)
    if position_current == position_circle_start and i:
        continue
    paper_circle.paperdict[position_current] = star_circle
paper_circle.switch2list(nosort=True)
paper_circle.translate([math.ceil(radius/ratio_hwchar) + 1, radius])

for i in range(3):
    string_current = strings[i]
    paper_string_current = paper_strings[i]
    paper_string_current.clear()
    paper_string_current.initial_position = [0, 0]
    paper_string_current.switch2list()
    paper_string_current.paperlist = [ [[i, 2-i+j], star] for j, star in enumerate(string_current) ]
    paper_string_current.translate([math.ceil(radius / ratio_hwchar) -nstrings + 1, 1])

paperlist_strings = sum((paper.paperlist for paper in paper_strings), start=[])
paperlist_circle = paper_circle.paperlist

print(paper_circle.down())
down_full = max(paper.down() for paper in (paper_strings + [paper_circle]))
# down_full = 15

paper_presenting = pattern_printer.Paper()
paper_presenting.initial_position = [0, 0]
paper_presenting.clear()
paper_presenting.switch2list()

to_clear_frame = False
clear_command = "clear" if os.name == "posix" else "cls"

# paper_presenting.paperlist = paperlist_strings + paperlist_circle
# print(paper_presenting.sprint())

def add_and_print(paper, paperlist_extra, dt):
    for charpoint in paperlist_extra:
        paper.switch2list()
        paper.paperlist.append(charpoint)
        paper.refresh()
        if to_clear_frame:
            os.system(clear_command)
        sys.stdout.write(paper.sprint(down_min=down_full))
        sys.stdout.flush()
        time.sleep(dt)

add_and_print(paper_presenting, paperlist_strings, 0.1)
add_and_print(paper_presenting, paperlist_circle, 0.05)
