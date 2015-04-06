#! /usr/bin/env python
# coding=utf-8

import sys
from time import time


def timeit(f, *args, **kwargs):
    def deco(*args, **kwargs):
        b = time()
        f(*args, **kwargs)
        e = time()
        print("Using {} seconds running {}".format(e - b, f.__name__))
    return deco

class Sorter:

    algorithms = ('bubble', 'bubble_recursion',
                  'insert', 'insert_recursion')

    def __init__(self, *args, **kwargs):
        self.count = 0
        self.cycle = 0

    def bubble(self, data, *args, **kwargs):
        _a = data
        for i in xrange(len(_a), 1, -1):
            for j in xrange(0, i - 1):
                if _a[j] > _a[j+1]:
                    _a[j], _a[j+1] = _a[j+1], _a[j]
                    self.count += 1
            self.cycle += 1
    def bubble_recursion(self, data, *args, **kwargs):
        def one_cycle(data, len):
            for i in xrange(0, len - 1):
                try:
                    if data[i] > data[i+1]:
                        data[i], data[i+1] = data[i+1], data[i]
                        self.count += 1
                except IndexError as e:
                    raise e
            self.cycle += 1

        _a = data
        len = kwargs['len']
        if len == 1:
            return
        else:
            one_cycle(_a, len)
            self.bubble_recursion(_a, len=len-1)

    def insert(self, data, *args, **kwargs):
        _a = data
        for i in xrange(1, len(_a)):
            for j in xrange(i, 0, -1):
                if _a[j] < _a[j-1]:
                    _a[j], _a[j-1] = _a[j-1], _a[j]
                    self.count += 1
            self.cycle += 1

    def insert_recursion(self, data, *args, **kwargs):
        def one_cycle(data, idx):
            for j in xrange(idx, 0, -1):
                try:
                    if data[j] < data[j-1]:
                        data[j], data[j-1] = data[j-1], data[j]
                        self.count += 1
                except IndexError:
                    raise
            self.cycle += 1

        _a = data
        idx = kwargs['idx']
        if idx == len(data):
            return
        else:
            one_cycle(_a, idx)
            self.insert_recursion(_a, idx=idx+1)

    @timeit
    def run(self, sort, data, *args, **kwargs):
        self.data = data
        self.sort = sort
        try:
            print("{} sorting".format(sort))
            print("original data:{}".format(data))
            getattr(self, sort)(data, *args, **kwargs)
            print("sorted data:{}".format(data))
        except Exception as e:
            print e
    
    def info(self):
        print("Total {} elements to sort".format(len(self.data)))
        print("Running {} cycle, {} times swap".format(self.cycle, self.count))

def main():
    x = Sorter()
    algorithm = sys.argv[1]
    a = [6, 3, 2, 1, -1, 5, 6, 7, -20, 10, 9, 8, 3]

    if algorithm not in x.algorithms:
        print "No {} implementation!".format(algorithm)
        sys.exit(1)

    if algorithm == 'bubble_recursion':
        x.run('bubble_recursion', a, len=len(a))
    elif algorithm == 'insert_recursion':
        x.run('insert_recursion', a, idx=1)
    else:
        x.run(algorithm, a)
    x.info()

if __name__ == '__main__':
    sys.exit(main())

