#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class MRHelper(object):

    def __init__(self, sep):
        self.sep = sep


    def setup(self):
        return True


    def emit(self, key, value, sep=None):
        if key is None:
            print value
        else:
            sep = self.sep if sep is None else sep
            print '%s%s%s' % (key, sep, value)


    def execute(self):
        raise NotImplementedError


    @classmethod
    def run(cls, sep='\t'):
        mrjob = cls(sep)
        if not mrjob.setup():
            print >> sys.stderr, 'setup error, EXIT'
            sys.exit(1)
        mrjob.execute()


class MRMapper(MRHelper):
    """
    Mapper wrapper for hadoop streaming job
    """

    def __init__(self, sep='\t'):
        super(MRMapper, self).__init__(sep)


    def mapper(self, key, value):
        raise NotImplementedError


    def execute(self):
        k = 0
        for line in sys.stdin:
            self.mapper(k, line.strip())
            k += 1


class MRReducer(MRHelper):
    """
    Reducer wrapper for hadoop streaming job
    """

    def __init__(self, sep='\t'):
        super(MRReducer, self).__init__(sep)


    def reducer(self, key, values):
        raise NotImplementedError


    def execute(self):
        current_key, k = None, None
        values = []

        for line in sys.stdin:
            k, v = line.strip().split(self.sep, 1)

            if k == current_key:
                values.append(v)
            else:
                if current_key is not None:
                    self.reducer(current_key, values)
                current_key = k
                values = [v, ]

        assert(k == current_key)
        if current_key is not None:
            self.reducer(current_key, values)