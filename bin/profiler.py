#!/usr/bin/env python
# coding=utf-8

import os
import sys
import resource
import time
import gc
import csv
from functools import wraps
from collections import OrderedDict
from memory_profiler import profile
from wand.image import Image


def timeit(f, *args, **kwargs):
    @wraps(f)
    def deco(*args, **kwargs):
        b = time.time()
        f(*args, **kwargs)
        e = time.time()
        #if DEBUG:
        #    print("{0} seconds...".format(e-b))
    return deco

@timeit
@profile
def profile_wand(*args, **kwargs):
    path = kwargs['path']
    with Image(filename=path) as original:
        with original.clone() as resized:
            resized.transform(resize=("256x256"))
            resized.format='jpeg'

class Profiler(object):
    """
    Profiling wand memory usage
    """
    csv_header = ('count', 'memory')

    def __init__(self, csv, dir, callback=profile_wand, *args, **kwargs):
        super(Profiler, self).__init__()
        self._csv_file = csv
        self._test_dir = dir
        self._callback = callback
        self._args = args
        self._kwargs = kwargs
        self._mem_stats = OrderedDict()
        self._count = 0
        self.does_info = kwargs['info'] or False
        self._w = self._build_csv_writer()

    def _mem_usage_kb(self):
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    def _build_csv_header(self):
        try:
            with open(self._csv_file, 'wb') as f:
                w = csv.DictWriter(f, self.csv_header)
                w.writeheader()
        except IOError as e:
            raise

    def _build_csv_writer(self):
        self._build_csv_header()
        try:
            self.csv_fd = open(self._csv_file, 'a')
            w = csv.DictWriter(self.csv_fd, self.csv_header)
        except IOError:
            raise
        return w

    def travel_path(self):
        for f in os.listdir(self._test_dir):
            f_path = os.path.join(self._test_dir, f)
            print "{0} starts processing {1}".format(self._callback.__name__, f_path)
            self._callback(path=f_path)
            self._w.writerow({'count':str(self._count), 'memory':self._mem_usage_kb()})
            if self.does_info:
                print "Memory is used: %d KB" % self._mem_usage_kb()
            self._count += 1

    def info(self):
        print "%d file are handled." % self._count
        gc.collect()
        print("garbage stats:{}".format(gc.garbage))


def main():
    #dir = sys.argv[3] or './photos'
    #loops = int(sys.argv[4])
    dir = './1000_pics'
    #dir = './photos'
    loops = 30

    p = Profiler('report.csv', dir, info=False)

    for i in xrange(1, loops + 1):
        print("Round {0}......".format(i))
        p.travel_path()
        if p.does_info:
            p.info()
    print("Test Done! Building Report......")

if __name__ == "__main__":
    sys.exit(main())

