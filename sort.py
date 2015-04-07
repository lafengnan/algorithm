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
                  'insert', 'insert_recursion',
                  'merge_recursion',
                  'heap_sort',
                  'qsort',
                 )

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

    def merge_recursion(self, data, *args, **kwargs):
        def _merge(data, begin, mid, rear):

            L = data[begin:mid + 1]
            R = data[mid + 1:rear + 1]

            # Append a sentinel to the end
            L.append(0x7fffffff)
            R.append(0x7fffffff)

            i = j = 0
            self.count += 1
            for k in xrange(begin, rear + 1):
                if L[i] <= R[j]:
                    data[k] = L[i]
                    i += 1
                else:
                    data[k] = R[j]
                    j += 1


        b = kwargs['begin']
        r = kwargs['rear']
        m = (b + r)/2
        if b < r:
            self.merge_recursion(data, begin=b, rear=m)
            self.merge_recursion(data, begin=m+1, rear=r)
            _merge(data, b, m, r)
            self.cycle += 1

    def heap_sort(self, data, *args, **kwargs):

        def _left(idx):
            return idx << 1

        def _right(idx):
            return (idx << 1) + 1
        
        def _max_heapify(data, idx, heap_size):
            """
            Keep max heapify for the idxth node:
                     idx(p)
                     /   \
                2*idx(l) 2*idx+1(r)
                l < p, r < p
            """
            l = _left(idx)
            r = _right(idx)

            if l < heap_size and data[l] > data[idx]:
                max_idx = l
            else:
                max_idx = idx
            if r < heap_size and data[r] > data[max_idx]:
                max_idx = r

            if max_idx != idx:
                data[idx], data[max_idx] = data[max_idx], data[idx]
                _max_heapify(data, max_idx, heap_size)
        
        def _build_max_heap(data):
            for i in xrange(len(data)/2, -1, -1):
                try:
                    _max_heapify(data, i, len(data))
                except Exception as e:
                    print e
                    raise Exception("build heap failed!")

        try:
            _build_max_heap(data)
        except Exception:
            raise
        _heap_size = len(data)
        for i in xrange(_heap_size - 1, 0, -1):
            data[0], data[i] = data[i], data[0]
            _heap_size -= 1
            try:
                _max_heapify(data, 0, _heap_size)
            except Exception:
                raise
    
    def qsort(self, data, *args, **kwargs):
        """quick sort"""
        def _partition(data, low, high):
            pivot = data[low]
            while low < high:
                while low < high and data[high] >= pivot:
                    high -= 1
                    self.count += 1
                #data[low], data[high] = data[high], data[low]
                data[low] = data[high]
                while low < high and data[low] <= pivot:
                    low += 1
                    self.count += 1
                #data[low], data[high] = data[high], data[low]
                data[high] = data[low]
            data[low] = pivot
            self.cycle += 1
            return low

        L = kwargs['low']
        H = kwargs['high']
        if L < H:
            pivot_idx = _partition(data, L, H)
            self.qsort(data, low=L, high=pivot_idx-1)
            self.qsort(data, low=pivot_idx+1, high=H)

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
    elif algorithm == 'merge_recursion':
        x.run('merge_recursion', a, begin=0, rear=len(a)-1)
    elif algorithm == 'qsort':
        x.run('qsort', a, low=0, high=len(a)-1)
    else:
        x.run(algorithm, a)
    x.info()

if __name__ == '__main__':
    sys.exit(main())

