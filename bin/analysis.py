#!/usr/bin/env python
# coding=utf-8

import re
import sys
import csv
import time
import pandas as pd
import webbrowser

from optparse import OptionParser
from collections import OrderedDict

Commands = ("queue", "worker")

USAGE = """
%prog <command> [options]
Commands:
""" + '\n'.join(["%10s: " % x for x in Commands])



class Analyzer(object):
    """
    Analyzer is used to analyze the celery log by convert the
    key data to csv format, and then use pandas to analyze the
    data.
    @log: the log file to analyze
    @type: the report type:[csv]
    @out: the output format
    """
    _csv_execution_fields = ('start', 'end', 'queue', 'task_id',
                             'task_name', 'duration', 'retries')
    _csv_inqueue_fields = ('task_id', 'task_name', 'queue',
                           'inq', 'outq', 'duration', 'accept',
                           'delta', 'retries')


    def __init__(self, cmd, log, type="csv", *args, **kargs):
        super(Analyzer, self).__init__()
        self._cmd = cmd
        self._log = log
        self._type = type or "csv"
        self._name_format = "{name}.{type}" if cmd == 'worker' \
            else "{name}_inqueue.{type}"
        self._stat_report_name_format = "{name}_stat.{suffix}" if cmd== 'worker' \
            else "{name}_inqueue_stat.{suffix}"
        self._out_file = self._name_format.format(name=log.split(".")[0],
                                                           type=type)
        self._html_report = self._name_format.format(name=log.split(".")[0],
                                                     type="html")
        self._stat_report = self._stat_report_name_format.format(name=log.split(".")[0],
                                                     suffix="html")
        self.args = args
        self.kargs = kargs
        self._header = self._csv_inqueue_fields if self._cmd == 'queue' \
        else self._csv_execution_fields
        self._writer = self._build_csv_writer(self._out_file, self._header)

    @property
    def report(self):
        return self._html_report

    def _build_csv_writer(self, csv_f, header):
        def _build_csv_header():
            try:
                with open(csv_f, 'wb') as f:
                    w = csv.DictWriter(f, header)
                    w.writeheader()
            except IOError:
                raise
        try:
            _build_csv_header()
            try:
                fd = open(csv_f, 'a')
                return csv.DictWriter(fd, self._header)
            except IOError:
                raise
        except Exception:
            raise


    def _write_out(self, data):
        self._writer.writerow(data)

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
                # output the data and remove the item
                self._write_out(_tmp_lines[task_id])
                _tmp_lines.pop(task_id)
            else:
                # add to dict
                _tmp_lines[task_id] = _d

    def _queue(self, line, o_data):
        self._collect_in_queue_lines(line, o_data)

    def _worker(self, line, out_lines=None, pattern="spends", sep=' '):
        start_pattern = re.compile("starts executing")
        end_pattern = re.compile(pattern)
        end_mt = end_pattern.search(line)
        start_mt = start_pattern.search(line)
        if start_mt:
            data = line.rstrip('\n').split(sep)
            start, q, task_id, task_name, retries \
                = \
                "{} {}".format(data[0].lstrip('['), data[1].rstrip(':')), \
                data[9].split(':')[1].split('.')[0], \
                data[8].split(':')[1].rstrip(','), \
                data[9].split(':')[1].split('.')[-1].rstrip(','), \
                data[-1].split(':')[1].rstrip('}')

            _d = {'start': start, 'end': None, 'queue':q, 'task_id':task_id,
                  'task_name': task_name, 'duration': None, 'retries': retries}
            out_lines[task_id] = _d
        if end_mt:
            data = line.rstrip('\n').split(sep)
            end, q, task_id, task_name, tv, retries\
                = \
                "{} {}".format(data[0].lstrip('['), data[1].rstrip(':')),\
                data[11].split(':')[1].split('.')[0],\
                data[10].split(':')[1].rstrip(','), \
                data[11].split(':')[1].split('.')[-1].rstrip(','),\
                data[6], \
                data[-1].split(':')[1].rstrip('}')
            if task_id in out_lines:
                out_lines[task_id]['end'] = end
                out_lines[task_id]['duration'] = tv
                self._write_out(out_lines[task_id])
                out_lines.pop(task_id)
                #wd = {self._csv_execution_fields[i]:data_new[i] for i in xrange(len(data_new))}
            else:
                out_lines[task_id] = {'start': None, 'end': end, 'queue':q, 'task_id':task_id,
                  'task_name': task_name, 'duration': tv, 'retries': retries}

    def _build_report(self):
        """
        out_data = {
        'task_id': {'task_id':xxx, 'task_name':xxxx}
        }
        """

        func = getattr(self, "_%s"%self._cmd)
        out_data = OrderedDict()
        try:
            with open(self._log, 'r') as f:
                for l in f:
                    try:
                        func(l, out_data)
                    except Exception as e:
                         print("build report failed for {}".format(e))
                         raise
        except IOError as e:
            print("Open file:{} error {}".format(self._log, e))
            raise
        # Flush remainder items
        for v in out_data.values():
            self._write_out(v)

    def read_csv_report(self, idx, n, asc=False, bar_len=0):
        df = pd.read_csv(self._out_file)
        if idx == 'index':
            print df.sort(ascending=asc).head(n)
        else:
            print df.sort(idx, ascending=asc).head(n)
        print bar_len*"="
        print "%80s"%"Statistic Info"
        print bar_len*"="
        print df.describe()
        print bar_len*"="
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
            print("Starts analyzing...")
            self._build_report()
            print("Completes analyzing!")
        except:
            raise


def main():

    parser = OptionParser(USAGE)
    parser.add_option('-n', '--number', type="int", dest="number", default=50,
                      help="config the number of records to show")
    parser.add_option('-a', action="store_true", dest="asc", default=False,
                      help="display the records in ascending or descending")
    parser.add_option('-i', '--index', type='string', dest='idx', default='duration',
                      help='display by which index[duration, delta]')
    parser.add_option('-l', '--log', type='string', dest='log', default='celery.log',
                      help='the log name which will be analyzed')
    parser.add_option('-b', action='store_false', dest='browser',
                      default=False, help='Open report in browser or not')

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        print "Error: config the command"
        return 1

    cmd = args[0]
    if cmd not in Commands:
        parser.print_help()
        print "Error: Unkown command: ", cmd
        return 1

    BAR_LEN = 160 if cmd == 'queue' else 135 if cmd == 'worker' else 0

    analyzer = Analyzer(cmd, options.log)
    try:
        analyzer.run()
        print("Starts reading report...")
        print BAR_LEN*"="
        analyzer.read_csv_report(options.idx,
                                 options.number,
                                 options.asc,
                                 BAR_LEN)
        analyzer.create_html_report()
        analyzer.draw_duration_plot()
        print BAR_LEN*"="
        if options.browser:
            webbrowser.open(analyzer.report)
    except Exception as e:
        print("analyzing failed! Reason: {}".format(e))

if __name__ == '__main__':
    sys.exit(main())
