#! /usr/bin/env python3

from copy import copy, deepcopy
from dataclasses import dataclass

class Paper:
    @dataclass
    class Setting:
        blank_char = " "
        line_sep_char = "\n"
        end_with_sep = False
        initial_position = [1, 1]
        is_editing_list = False
        auto_clean_blank = True

    _default_original = Setting()
    
    default = Setting()

    def reset_default(cls):
        cls.default = cls._default_original

    def __init__(self,
                 paperdict=None,
                 paperlist=None,
                 blank_char=None,
                 line_sep_char=None,
                 end_with_sep=None,
                 initial_position=None,
                 is_editing_list=None,
                 auto_clean_blank=None,
                 settings=None,
                 use_original_default=False):
        if use_original_default:
            self.apply_setting(self._original_default)
        else:
            self.apply_setting()
        for key_local, val_local in locals().items(): 
            if key_local[0] != "_" and val_local is not None:
                 setattr(self, key_local, val_local)
        self.paperdict = dict() if paperdict is None else paperdict
        self.paperlist = list() if paperlist is None else paperlist
        # self.refresh()
        # print(self, "initialized")

    def apply_setting(self, setting=None):
        if setting is None:
            setting = self.default
        for attrname in setting.__dir__():
            if attrname[0] != "_":
                setattr(self, attrname, getattr(setting, attrname))

    def clear(self):
        self.paperlist.clear()
        self.paperdict.clear()

    def sync2dict(self):
        self.paperdict.clear()
        for charpoint in self.paperlist:
            self.paperdict[tuple(charpoint[0])] = str(charpoint[1])
        if self.auto_clean_blank:
            while self.blank_char in self.paperdict:
                self.paperdict.pop(self.blank_char)

    def switch2dict(self, nosync=False, force=False):
        if (not nosync) and (self.is_editing_list or force):
            self.sync2dict()
        self.is_editing_list = False

    def sync2list(self, nosort=False):
        self.paperlist = [
            [list(key), self.paperdict[key]]
            for key in self.paperdict.keys()]
        if not nosort:
            self.paperlist.sort()

    def switch2list(self, nosort=False, nosync=False, force=False):
        if (not nosync) and ((not self.is_editing_list) or force):
            self.sync2list(nosort=nosort)
        self.is_editing_list = True

    def refresh(self, editing_list = None):
        if self.is_editing_list:
            self.switch2dict()
            self.switch2list()
        else:
            self.switch2list()
            self.switch2dict()
        if editing_list is not None:
            self.is_editing_list = editing_list

    def edge(self, horizontal, fmm):
        generator_positions = (
                (self.paperlist[i][0] for i in range(len(self.paperlist)))
                if self.is_editing_list
                else self.paperdict.keys())
        return fmm((key[horizontal] for key in generator_positions), default=self.initial_position[horizontal])

    def right(self):  # used in the square option of sprint
        return self.edge(1, max)

    def left(self):
        return self.edge(1, min)

    def down(self):
        return self.edge(0, max)

    def up(self):
        return self.edge(0, min)

    def sprint(self, nochange=False, fill_right=False, right_min=0, down_min=0, stay_in_list=False):
        if nochange:
            from copy import deepcopy
            papertemp = deepcopy(self)
            return papertemp.sprint(nochange=False,
                                    fill_right=fill_right,
                                    right_min=right_min)
        was_editing_list = self.is_editing_list
        strout = ""
        # ADDRESS PROBLEM, A MATTER OF SAFTY
        position_now = self.initial_position.copy()
        # self.refresh()
        # self.switch2dict()
        self.refresh(editing_list = True)
        if fill_right and right_min <= self_initial_position[0]:
            right_min = self.right()
        # for k in self.paperdict.keys():
        for point in self.paperlist:
            k, charnow = point
            if k[0] < self.initial_position[0] or k[1] < self.initial_position[1]:
                continue
            if k[0] > position_now[0]:
                strout += (self.blank_char *
                           max(right_min - position_now[0], 0) +
                           self.line_sep_char)
                position_now[0] += 1
                strout += ((self.blank_char*right_min +
                            self.line_sep_char) *
                           (k[0]-position_now[0]))
                position_now = [k[0], self.initial_position[1]]
            if k[0] == position_now[0] and k[1] > position_now[1]:
                strout += self.blank_char*(k[1]-position_now[1])
                position_now[1] = k[1]
            # strout += str(self.paperdict[k])
            strout += str(charnow)
            position_now[1] += 1
        if position_now[0] < down_min:
            strout += (self.blank_char*right_min + self.line_sep_char) * (down_min - position_now[0])
        if self.end_with_sep:
            strout += self.line_sep_char
        if stay_in_list and not was_editing_list:
            self.switch2dict()
        return strout

    # extra functions
    def translate(self, vector, stay_in_list=False):
        was_editing_list = self.is_editing_list
        self.switch2list(nosort=True)
        # self.paperlist = [
        #     [[point[0][0]+vector[0], point[0][1]+vector[1]],
        #      point[1]]
        #     for point in self.paperlist]
        for i in range(len(self.paperlist)):
            self.paperlist[i][0][0] += vector[0]
            self.paperlist[i][0][1] += vector[1]
        if not stay_in_list and not was_editing_list:
            self.switch2dict()

def translated(self, *args, **kwargs):
    from copy import deepcopy
    paperout = deepcopy(self)
    paperout.translate(*args, **kwargs)
    return paperout


if __name__ == "__main__":
    paper1 = Paper()
    paper1.paperdict[(4, 5)] = "3"
    #paper1.translate([-1, -3])
    print(paper1.sprint())
    print("-----")
    import example_abc
    print("-----")
    import example_xes
    print("-----")
