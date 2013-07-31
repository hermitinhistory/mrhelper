#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mrhelper import MRReducer


class RWC(MRReducer):
    def reducer(self, key, values):
        s = sum(map(int, values))
        self.emit(key, s)


if __name__ == '__main__':
    RWC.run()