#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from mrhelper import MRMapper


class MWC(MRMapper):
    def setup(self):
        c = os.environ.get('name')
        if c is not None:
            self.emit(c, 1)


    def mapper(self, _, value):
        for a in value.split():
            self.emit(a, 1)


if __name__ == '__main__':
    MWC.run()
