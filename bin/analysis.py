#!/usr/bin/env python
# coding=utf-8

import re
import os, sys
import csv
from collections import OrderedDict
import pandas as pd
from pylab import *
import time
import webbrowser

BAR_LEN = 160 if sys.argv[1] == 'in_queue' else 135 if sys.argv[1] == 'in_worker' \
    else 0

class Analyzer(object):
    """
    Analyzer is used to analyze the celery log by convert the
    key data to csv format, and then use pandas to analyze the
    data.
    @log: the log file to analyze
    @type: the report type:[csv]
    @out: the output format
    """
    _csv_execution_fields = ('timestamp', 'queue', 'task_id',
                             'task_name', 'duration', 'retries')
    _csv_inqueue_fields = ('task_id', 'task_name', 'queue',
                           'inq', 'outq', 'duration', 'accept',
                           'delta', 'retries')


    def __init__(self, opt, log, type="csv", *args, **kargs):
        super(Analyzer, self).__init__()
        self._opt = opt
        self._log = log
        self._type = type or "csv"
        self._name_format = "{name}.{type}" if opt == 'in_worker' \
            else "{name}_inqueue.{type}"
        self._stat_report_name_format = "{name}_stat.{suffix}" if opt == 'in_worker' \
            else "{name}_inqueue_stat.{suffix}"
        self._out_file = self._name_format.format(name=log.split(".")[0],
                                                           type=type)
        self._html_report = self._name_format.format(name=log.split(".")[0],
                                                     type="html")
        self._stat_report = self._stat_report_name_format.format(name=log.split(".")[0],
                                                     suffix="html")
        self.args = args
        self.kargs = kargs
        _header = self._csv_inqueue_fields if self._opt == 'in_queue' \
        else self._csv_execution_fields
        self._build_csv_writer(self._out_file, _header)

    @property
    def report(self):
        return self._html_report

    def _build_csv_writer(self, csv_f, header):
        try:
            with open(csv_f, 'wb') as f:
                w = csv.DictWriter(f, header)
                w.writeheader()
        except IOError as e:
            print("build csv writer failed! Reason:{}".format(e))
            raise

    def _write_out(self, csv_f, data):
        fields = self._csv_execution_fields if self._opt == 'in_worker' \
            else self._csv_inqueue_fields
        try:
            with open(csv_f, 'a') as f:
                w = csv.DictWriter(f, fields)
                w.writerow(data)
        except Exception as e:
            print("Open file:{} error {}".format(self._out_file, e))
            raise

    def _collect_in_queue_lines(self, line, out_lines, pattern_tx="publishing",
                               pattern_rx="(anan)+.*Received", sep=' '):
        _tmp_lines = out_lines
        prog_tx = re.compile(pattern_tx)
        prog_rx = re.compile(pattern_rx)
        prog_accept = re.compile("(anan)+.*task-accepted")

        mt_tx = prog_tx.search(line)
        mt_rx = prog_rx.search(line)
        mt_accept = prog_accept.search(line)

        if mt_tx:
            data = line.rstrip('\n').split(sep)
            date, ts, q, task_id, task_name, retries = \
                data[0].lstrip('['),\
                data[1].rstrip(':'), \
                data[-2].split(':')[1].split('.')[0], \
                data[-3].split(':')[1].rstrip(','), \
                data[-2].split(':')[1].split('.')[-1].rstrip(','),\
                data[-1].split(':')[1].rstrip('}')
            _d = dict({'task_id':task_id, 'task_name':task_name,
                       'queue':q, 'inq':"{} {}".format(date, ts),
                       'outq':None, 'duration':None, 'accept':None,
                       'delta':None, 'retries':retries
                       })
            if task_id in _tmp_lines:
                for k in _d:
                    if _d[k] != _tmp_lines[task_id][k] and _d[k]:
                        _tmp_lines[task_id][k] = _d[k]
            else:
                # add to dict
                _tmp_lines[task_id] = _d
        if mt_rx:
            data = line.rstrip('\n').split(sep)
            date, ts, q, task_id, task_name, retries = \
                data[0].lstrip('['), \
                data[1].rstrip(':'), \
                data[-2].split(':')[1].split('.')[0], \
                data[-3].split(':')[1].rstrip(','), \
                data[-2].split(':')[1].split('.')[-1].rstrip(','),\
                0

            _d = dict({'task_id':task_id, 'task_name':task_name,
                       'queue':q, 'inq':None,
                       'outq':"{} {}".format(date, ts),
                       'duration': 0,
                       'accept':None,
                       'delta': 0, 'retries':retries})

            if task_id in _tmp_lines:
                _tmp_lines[task_id]['outq'] = _d['outq']

                if _tmp_lines[task_id]['inq']:
                    in_time_str = _tmp_lines[task_id]['inq']
                    o_time_str = _d['outq']
                    in_time = time.mktime(time.strptime(in_time_str.split(',')[0],
                                                        "%Y-%m-%d %H:%M:%S")) + \
                        float('0.%s'%in_time_str.split(',')[1])
                    o_time = time.mktime(time.strptime(o_time_str.split(',')[0],
                                                       "%Y-%m-%d %H:%M:%S")) + \
                        float('0.%s'%o_time_str.split(',')[1])
                    _tmp_lines[task_id]['duration'] = _d['duration'] = o_time - in_time
            else:
                # add to dict
                _tmp_lines[task_id] = _d
        if mt_accept:
            data = line.rstrip('\n').split(sep)
            date, ts, q, task_id, task_name, retries = \
                data[0].lstrip('['), \
                data[1].rstrip(':'), \
                data[-1].split(':')[1].split('.')[0], \
                data[-2].split(':')[1].rstrip(','), \
                data[-1].split(':')[1].split('.')[-1].rstrip('}'),\
                0

            _d = dict({'task_id':task_id, 'task_name':task_name,
                       'queue':q, 'inq':None, 'outq':None,
                       'duration': 0,
                       'accept':"{} {}".format(date, ts),
                       'delta': 0, 'retries':retries})

            if task_id in _tmp_lines:
                _tmp_lines[task_id]['accept'] = _d['accept']

                if _tmp_lines[task_id]['outq']:
                    in_time_str = _tmp_lines[task_id]['outq']
                    o_time_str = _d['accept']
                    in_time = time.mktime(time.strptime(in_time_str.split(',')[0],
                                                        "%Y-%m-%d %H:%M:%S")) + \
                        float('0.%s'%in_time_str.split(',')[1])
                    o_time = time.mktime(time.strptime(o_time_str.split(',')[0],
                                                       "%Y-%m-%d %H:%M:%S")) + \
                        float('0.%s'%o_time_str.split(',')[1])
                    _tmp_lines[task_id]['delta'] = _d['delta'] = o_time - in_time
            else:
                # add to dict
                _tmp_lines[task_id] = _d

    def _in_queue(self, line, o_data):
        self._collect_in_queue_lines(line, o_data)

    def _in_worker(self, line, out_lines=None, pattern="spends", sep=' '):
        prog = re.compile(pattern)
        mt = prog.search(line)
        if mt:
            data = line.rstrip('\n').split(sep)
            data_new = ts, q, task_id, task_name, tv, retries\
                = \
                "{} {}".format(data[0].lstrip('['), data[1].rstrip(':')),\
                data[11].split(':')[1].split('.')[0],\
                data[10].split(':')[1].rstrip(','), \
                data[11].split(':')[1].split('.')[-1].rstrip(','),\
                data[6], \
                data[-1].split(':')[1].rstrip('}')
            wd = {self._csv_execution_fields[i]:data_new[i] for i in xrange(len(data_new))}
            out_lines[task_id] = wd

    def _build_report(self):
        """
        out_data = {
        'task_id': {'task_id':xxx, 'task_name':xxxx}
        }
        """

        func = getattr(self, "_%s"%self._opt)
        out_data = OrderedDict()
        try:
            with open(self._log, 'r') as f:
                while True:
                    l = f.readline()
                    if not l:
                        break
                    try:
                        func(l, out_data)
                    except Exception as e:
                         print("build report failed for {}".format(e))
                         raise
            try:
                for v in out_data.values():
                    self._write_out(self._out_file, v)
            except Exception:
                raise
        except IOError as e:
            print("Open file:{} error {}".format(self._log, e))
            raise

    def read_csv_report(self, idx, n):
        df = pd.read_csv(self._out_file)
        print df.sort(idx, ascending=False).head(n)
        print BAR_LEN*"="
        print "%80s"%"Statistic Info"
        print BAR_LEN*"="
        print df.describe()
        print BAR_LEN*"="
        print df.task_name.describe()

    def create_html_report(self):
        pf = pd.read_csv(self._out_file)
        try:
            with open(self._html_report, 'wb') as f:
                f.writelines(pf.to_html())
        except IOError:
            raise

    def draw_duration_plot(self):
        pass


    def run(self):
        try:
            self._build_report()
        except:
            raise


def main():
    if len(sys.argv) < 3:
        print("Missing report type:[in_queue, in_worker]")
        sys.exit(1)
    analyzer = Analyzer(*sys.argv[1:3])
    try:
        analyzer.run()
        print BAR_LEN*"="
        analyzer.read_csv_report(sys.argv[-2], int(sys.argv[-1]))
        analyzer.create_html_report()
        analyzer.draw_duration_plot()
        print BAR_LEN*"="
        #webbrowser.open(analyzer.report)
    except Exception as e:
        print("analyzing failed! Reason: {}".format(e))

if __name__ == '__main__':
    sys.exit(main())
