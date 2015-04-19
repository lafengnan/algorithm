#! /usr/bin/env python
# coding=utf-8

from time import time
from data_structure import stack

def timeit(f, *args, **kwargs):
    def deco(*args, **kwargs):
        b = time()
        r = f(*args, **kwargs)
        e = time()
        print("Using {} seconds running {}".format(e - b, f.__name__))
        return r
    return deco

class Sorter(object):

    algorithms = ('bubble', 'bubble_recursion',
                  'insert_exchange', 'insert_recursion',
                  'insert_shift', 'merge_recursion',
                  'merge_with_insert','merge_none_recursion',
                  'heap_sort','select_sort',
                  'qsort','qsort_none_recursion'
                 )

    def __init__(self, *args, **kwargs):
        super(Sorter, self).__init__()
        self.count = 0
        self.cycle = 0
        self._args = args
        self._kwargs = kwargs
        self._verbose= kwargs.get('verbose', False)

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

    def insert_exchange(self, data, *args, **kwargs):
        _a = data
        for i in xrange(1, len(_a)):
            for j in xrange(i, 0, -1):
                if _a[j] < _a[j-1]:
                    _a[j], _a[j-1] = _a[j-1], _a[j]
                    self.count += 1
            self.cycle += 1

    def insert_shift(self, data, *args, **kwargs):
        _a = data
        for i in xrange(1, len(_a)):
            key = _a[i]
            j = i - 1
            while key < _a[j] and j >= 0:
                _a[j+1] = _a[j] # right shift _a[j]
                j -= 1
                self.count += 1
            _a[j+1] = key
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

    def select_sort(self, data, *args, **kwargs):
        _a = data
        for i in xrange(len(_a) - 1):
            key = min = _a[i]
            sentinel = i
            for j in xrange(i+1, len(_a)):
                if min > _a[j]:
                    min = _a[j]
                    sentinel = j
                    self.count += 1
            # sentinel has changed, means has data swaped
            if sentinel != i:
                _a[i] = min
                _a[sentinel] = key
            self.cycle += 1
            print _a

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

        l = kwargs.get('low', 0)
        h = kwargs.get('high', -1)
        if l < h:
            m = (l + h) >> 1
            self.merge_recursion(data, low=l, high=m)
            self.merge_recursion(data, low=m+1, high=h)
            _merge(data, l, m, h)
            self.cycle += 1

    def merge_none_recursion(self, data, *args, **kwargs):
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

        l = kwargs.get('low', 0)
        h = kwargs.get('high', -1)
        if l < h:
            mid = (l + h) >> 1
            stk = stack.Stack()
            if l < mid:
                stk.push(l)
                stk.push(mid)
            if mid + 1 < h:
                stk.push(mid+1)
                stk.push(h)
            _merge(data, l, mid, h)
            while not stk.isEmpty:
                sh = stk.top
                stk.pop()
                sl = stk.top
                stk.pop()
                smid = (sl + sh) >> 1
                if sl < smid:
                    stk.push(sl)
                    stk.push(smid)
                if smid + 1 < sh:
                    stk.push(smid+1)
                    stk.push(sh)
                _merge(data, sl, smid, sh)
            _merge(data, l, mid, h)

    def merge_with_insert(self, data, *args, **kwargs):
        def _insert(data, low, high):
            _new = data[low:high+1]
            self.insert_shift(_new)

            k = low
            j = 0
            while k <= high:
                data[k] = _new[j]
                k += 1
                j += 1

        l = kwargs.get('low', 0)
        h = kwargs.get('high', -1)
        shard_size = kwargs.get('shard_size', 4)

        if h -l > shard_size - 1:
            m = (l + h)/2
            self.merge_with_insert(data, low=l, high=m)
            self.merge_with_insert(data, low=m+1, high=h)
            _insert(data, l, h)
        else:
            _insert(data, l, h)

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

        def _partition2(data, low, high):
            x = data[high]
            i = low - 1
            j = low
            while j < high:
                if data[j] <= x:
                    i += 1
                    data[i], data[j] = data[j], data[i]
                j += 1
            data[i+1], data[high] =  data[high], data[i+1]
            return i + 1
        
        L = kwargs.get('low', 0)
        H = kwargs.get('high', -1)
        if L < H:
            pivot_idx = _partition2(data, L, H)
            self.qsort(data, low=L, high=pivot_idx-1)
            self.qsort(data, low=pivot_idx+1, high=H)

    def qsort_none_recursion(self, data, *args, **kwargs):
        def _partition(data, low, high):
            x = data[high]
            i = low - 1
            j = low
            while j < high:
                if data[j] <= x:
                    i += 1
                    data[i], data[j] = data[j], data[i]
                    self.count += 1
                j += 1
            data[i+1], data[high] = data[high], data[i+1]
            return i + 1

        l = kwargs.get('low', 0)
        h = kwargs.get('high', -1)
        stk = stack.Stack()
        if l < h:
            mid = _partition(data, l, h)
            if l < mid - 1:
                stk.push(l)
                stk.push(mid-1)
            if mid + 1 < h:
                stk.push(mid+1)
                stk.push(h)
            while not stk.isEmpty:
                if self._verbose:
                    stk.travel_stack()
                sh = stk.top
                stk.pop()
                sl = stk.top
                stk.pop()
                mid = _partition(data, sl, sh)
                if sl < mid -1:
                    stk.push(sl)
                    stk.push(mid-1)
                if mid + 1 < sh:
                    stk.push(mid+1)
                    stk.push(sh)

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

class Search(object):
    """
    Search class defines the method about how to search a specified key in one
    sequence.
    """
    algorithms = ("bisearch", "bisearch_none_recursion", "bisearch_loop")

    def __init__(self, algorithm='bisearch', *args, **kwargs):
        assert algorithm in self.algorithms
        self._algorithm = algorithm
        self._args = args
        self._kwargs = kwargs
        self._verbose = kwargs.get('verbose', False)

    def _bisearch(self, key, seq, **kwargs):
        if len(seq) == 0:
            return False, -1
        else:
            l = kwargs.get('low', 0)
            h = kwargs.get('high', -1)
            mid = (l + h) >> 1
            div = key - seq[mid]
            if self._verbose:
                print "compare in [%d - %d] @%d" % (l, h, mid)
            if div == 0:
                return True, mid
            elif l < h and div < 0:
                return self._bisearch(key, seq, low=l, high=mid-1)
            elif l < h and div > 0:
                return self._bisearch(key, seq, low=mid+1, high=h)
            return False, -1

    def _bisearch_none_recursion(self, k, seq, **kwargs):
        assert len(seq) != 0

        l = kwargs.get('low', 0)
        h = kwargs.get('high', -1)
        mid = (l+h) >> 1
        div = k - seq[mid]
        stk = stack.Stack()

        if div == 0:
            return True, mid
        else:
            stk.push(l)
            stk.push(h)
            while not stk.isEmpty:
                sh = stk.top
                stk.pop()
                sl = stk.top
                stk.pop()
                mid = (sl + sh) >> 1
                if k == seq[mid]:
                    return True, mid
                elif k < seq[mid]:
                    stk.push(sl)
                    stk.push(mid-1)
                else:
                    stk.push(mid+1)
                    stk.push(sh)
        return False, -1

    def _bisearch_loop(self, k, seq, **kwargs):
        assert len(seq) != 0
        l = kwargs.get('low', 0)
        h = kwargs.get('high', -1)
        if l < h:
            mid = (l + h) >> 1
            while k != seq[mid] and mid >= 0:
                mid = (l + h) >> 1
                if k < seq[mid]:
                    h = mid - 1
                else:
                    l = mid + 1
                if mid == h or mid == l:
                    break

            return (True, mid) if k == seq[mid] else (False, -1)


    def search(self, key, seq):
        sorter = Sorter(verbose=False)
        if self._verbose:
            print "Before sort: %r" % seq
        sorter.qsort_none_recursion(seq, low=0, high=len(seq)-1)
        if self._verbose:
            print "After sorted: %r" % seq
        return getattr(self, "_%s"%self._algorithm)(key, seq, low=0, high=len(seq)-1)
