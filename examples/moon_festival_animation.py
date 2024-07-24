#! /usr/bin/env python3

#   Happy
#  Moon
# Festival

import pattern_printer
import time
import sys
import os
import math

pattern_printer.INIT_POSITION = [0, 0]

paper_string = pattern_printer.Paper()
paper_string.clear()
paper_string.update_from_string((-2, 3), "Happy")
paper_string.update_from_string((-1, 2), "Moon")
paper_string.update_from_string((0, 1), "Festival")

paper_circle = pattern_printer.Paper()
paper_circle.clear()
radius = 20
paper_circle.switch_to_dict()
star_circle = "*"
ratio_hwchar = 2
nslices_angle = radius * 4
is_clockwise = False
angle_start = math.pi / 2

for i in range(nslices_angle):
    angle = angle_start + math.pi * 2 * i / nslices_angle
    paper_circle.paperdict[
        (
            int(round(-math.sin(angle) * radius / ratio_hwchar)),
            int(round(math.cos(angle) * radius)),
        )
    ] = star_circle

center_of_circle = [math.ceil(radius / ratio_hwchar) + 1, radius]
paper_string.translate([center_of_circle[0], 0], stay_in_list=True)
paper_circle.translate(center_of_circle, stay_in_list=True)
down_full = paper_circle.down()

paper_presentation = pattern_printer.Paper(is_editing_list=True)
paper_presentation.clear()
to_clear_frame = True
clear_command = "clear" if os.name == "posix" else "cls"


def add_and_print(paperlist_extra, dt):
    paper_presentation.switch_to_list()
    for charpoint in paperlist_extra:
        paper_presentation.paperlist.append(charpoint)
        if to_clear_frame:
            os.system(clear_command)
        sys.stdout.write(paper_presentation.sprint(down_min=down_full))
        sys.stdout.flush()
        time.sleep(dt)


add_and_print(paper_string.paperlist, 0.1)
add_and_print(paper_circle.paperlist, 0.05)
