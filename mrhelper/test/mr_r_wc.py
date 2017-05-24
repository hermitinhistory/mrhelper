#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('./')
from mrhelper import MRReducer


class RWC(MRReducer):
    def cleanup(self):
        self.emit('xxxx_from_cleanup', 1)

    def reducer(self, key, values):
        s = sum(map(int, values))
        self.emit(key, s)


if __name__ == '__main__':
    RWC.run()
