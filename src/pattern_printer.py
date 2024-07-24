#! /usr/bin/env python3

from copy import deepcopy


def _default_if_none(value, default):
    return value if value is not None else default


def reset_settings():
    global ALWAYS_RSTRIP
    ALWAYS_RSTRIP = True
    global INIT_EDITING_LIST
    INIT_EDITING_LIST = False
    global INIT_POSITION
    INIT_POSITION = [1, 1]
    global SPACE_CHAR
    SPACE_CHAR = " "


reset_settings()


class Paper:
    def __init__(
        self,
        paperdict={},
        paperlist=[],
        always_rstrip=None,
        init_position=None,
        is_editing_list=None,
        space_char=None,
    ):
        self.paperdict = paperdict
        self.paperlist = paperlist
        self.always_rstrip = _default_if_none(always_rstrip, ALWAYS_RSTRIP)
        self.init_position = _default_if_none(init_position, INIT_POSITION)
        self.is_editing_list = _default_if_none(is_editing_list, INIT_EDITING_LIST)
        self.space_char = _default_if_none(space_char, SPACE_CHAR)

    def clear(self):
        self.paperlist.clear()
        self.paperdict.clear()

    def sync_to_dict(self):
        self.paperdict.clear()
        for charpoint in self.paperlist:
            self.paperdict[tuple(charpoint[0])] = str(charpoint[1])
        if self.always_rstrip:
            while self.space_char in self.paperdict:
                self.paperdict.pop(self.space_char)

    def switch_to_dict(self, nosync=False, force=False):
        if (not nosync) and (self.is_editing_list or force):
            self.sync_to_dict()
        self.is_editing_list = False

    def sync_to_list(self, nosort=False):
        self.paperlist = [
            [list(key), self.paperdict[key]] for key in self.paperdict.keys()
        ]
        if not nosort:
            self.paperlist.sort()

    def switch_to_list(self, nosort=False, nosync=False, force=False):
        if (not nosync) and ((not self.is_editing_list) or force):
            self.sync_to_list(nosort=nosort)
        self.is_editing_list = True

    def refresh(self, editing_list=None):
        if self.is_editing_list:
            self.switch_to_dict()
            self.switch_to_list()
        else:
            self.switch_to_list()
            self.switch_to_dict()
        if editing_list is not None:
            self.is_editing_list = editing_list

    def edge(self, horizontal, fmm):
        generator_positions = (
            (self.paperlist[i][0] for i in range(len(self.paperlist)))
            if self.is_editing_list
            else self.paperdict.keys()
        )
        return fmm(
            (key[horizontal] for key in generator_positions),
            default=self.init_position[horizontal],
        )

    def right(self):  # used in the square option of sprint
        return self.edge(1, max)

    def left(self):
        return self.edge(1, min)

    def down(self):
        return self.edge(0, max)

    def up(self):
        return self.edge(0, min)

    def sprint(
        self,
        nochange=False,
        fill_right=False,
        right_min=0,
        down_min=0,
        stay_in_list=False,
        append_newline=True,
    ):
        if nochange:
            papertemp = deepcopy(self)
            return papertemp.sprint(
                nochange=False, fill_right=fill_right, right_min=right_min
            )
        was_editing_list = self.is_editing_list
        strout = ""
        position_now = self.init_position.copy()
        self.refresh(editing_list=True)
        if fill_right and right_min <= self.init_position[0]:
            right_min = self.right()
        for point in self.paperlist:
            k, charnow = point
            if k[0] < self.init_position[0] or k[1] < self.init_position[1]:
                continue
            if k[0] > position_now[0]:
                strout += self.space_char * max(right_min - position_now[0], 0) + "\n"
                position_now[0] += 1
                strout += (self.space_char * right_min + "\n") * (
                    k[0] - position_now[0]
                )
                position_now = [k[0], self.init_position[1]]
            if k[0] == position_now[0] and k[1] > position_now[1]:
                strout += self.space_char * (k[1] - position_now[1])
                position_now[1] = k[1]
            strout += str(charnow)
            position_now[1] += 1
        if position_now[0] < down_min:
            strout += (self.space_char * right_min + "\n") * (
                down_min - position_now[0]
            )
        if append_newline:
            strout += "\n"
        if stay_in_list and not was_editing_list:
            self.switch_to_dict()
        return strout

    # extra functions
    def translate(self, vector, stay_in_list=False):
        was_editing_list = self.is_editing_list
        self.switch_to_list(nosort=True)
        # self.paperlist = [
        #     [[point[0][0]+vector[0], point[0][1]+vector[1]],
        #      point[1]]
        #     for point in self.paperlist]
        for i in range(len(self.paperlist)):
            self.paperlist[i][0][0] += vector[0]
            self.paperlist[i][0][1] += vector[1]
        if not stay_in_list and not was_editing_list:
            self.switch_to_dict()


def translated(self, *args, **kwargs):
    paperout = deepcopy(self)
    paperout.translate(*args, **kwargs)
    return paperout
