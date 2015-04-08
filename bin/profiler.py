#!/usr/bin/env python
# coding=utf-8

import os
import sys
import resource
import time
import gc
import csv
import re
from functools import wraps
from collections import OrderedDict
from memory_profiler import profile
from wand.image import Image

target_dir = './photos'

def timeit(f, *args, **kwargs):
    @wraps(f)
    def deco(*args, **kwargs):
        b = time.time()
        f(*args, **kwargs)
        e = time.time()
        #if DEBUG:
        #    print("{0} seconds...".format(e-b))
    return deco

#@timeit
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

class TopLogAnalyzer(object):
    """
    Analyze the top command output for long time monitor
    Will create a csv report for graphic display
    @log: the top command output by using top -p [pid1, pid2, ...] -b > top.log
    @pids_num: the number of processes to monitor
    @user: the user of the pids

    """
    csv_header = ('timestamp', 'load_1', 'load_5', 'load_10',
                  'pid', 'virt', 'res', 'shr', '%cpu', '%mem'
                  )
    def __init__(self, log, pids, user, *args, **kwargs):
        super(TopLogAnalyzer, self).__init__()
        self._log = log
        self._pids = pids
        self._user = user
        self._args = args
        self._kwargs = kwargs
        self._csv = log.split('.')[0] + ".csv" if log else "top.csv"
        self._csv_writer = self._build_csv_writer()

    def _build_csv_writer(self):
        def _build_header():
            try:
                with open(self._csv, 'wb') as f:
                    w = csv.DictWriter(f, self.csv_header)
                    w.writeheader()
            except IOError:
                raise
        try:
            _build_header()
        except:
            raise
        try:
            fd = open(self._csv, 'a')
            w = csv.DictWriter(fd, self.csv_header)
        except IOError:
            raise
        return w

    def _collect_data(self):

        def _collect_top_line(line):
            words = line.rstrip('\n').split(' ')
            # timestamp, load_1, load_5, load_10
            headline_data = [words[2], words[-3].rstrip(','), words[-2].rstrip(','), words[-1]]
            return headline_data

        def _collect_stats(line):
            words = [x for x in line.rstrip('\n').rstrip(' ').lstrip(' ').split(' ') if x != '']
            # pid, virt, res, shr, %cpu, %mem
            pid = words[0]
            virt = words[4].rstrip('m')
            res = words[5].rstrip('m')
            shr = words[6]
            cpu = words[8]
            mem = words[9]
            return [pid, virt, res, shr, cpu, mem]

        _loads_pattern = re.compile("load")
        _stats_pattern = re.compile(self._user)

        try:
            with open(self._log, 'r') as f:
                _stats = list()
                for l in f:
                    if  _loads_pattern.search(l):
                        _stats = [] # reset _stats for new interval
                        _stats +=  _collect_top_line(l)
                    elif _stats_pattern.search(l):
                        pid_stat = _collect_stats(l)
                        _stats += pid_stat
                        data = dict(zip(self.csv_header, _stats))
                        self._csv_writer.writerow(data)
                        # Drain out pid_stat for next pid
                        for x in pid_stat:
                            _stats.remove(x)
        except IOError:
            raise

    def analyze(self, *args, **kwargs):
        print("Starts building csv report...")
        self._collect_data()
        print("Ends building csv report")


def profiler():
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

def analyze():
    # analysis cmd[analyze | profiler] options
    log = sys.argv[2]
    pids_num = int(sys.argv[3])
    user = sys.argv[-1]
    analyzer = TopLogAnalyzer(log, pids_num, user)
    analyzer.analyze()

if __name__ == "__main__":
    if sys.argv[1] == 'analyze':
        run = analyze
    elif sys.argv[1] == 'profiler':
        run = profiler
    sys.exit(run())

