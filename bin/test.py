#!/usr/bin/env python
# coding=utf-8

import sys
import os
from optparse import OptionParser
os.path.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import sort
from data_structure import linklist, stack

Commands = ("sort", "singlelinklist", "stack")

USAGE = """
%prog <command> [options]
Commands:
""" + '\n'.join(["%10s: " % x for x in Commands])




def main():

    parser = OptionParser(USAGE)
    parser.add_option('-s', '--sort', type="string", dest="sort", default='qsort',
                      help="config which sort algorithm to run[bubble|insert|merge|heapsort|qsort]")
#    parser.add_option('-n', '--number', type="int", dest="number", default=50,
#                      help="config the number of records to show")
#    parser.add_option('-a', action="store_true", dest="asc", default=False,
#                      help="display the records in ascending or descending")
#    parser.add_option('-i', '--index', type='string', dest='idx', default='duration',
#                      help='display by which index[duration, latency]')
#    parser.add_option('-l', '--log', type='string', dest='log', default='celery.log',
#                      help='the log name which will be analyzed')
#    parser.add_option('-r', '--report', type='string', dest='report', default='celery.csv',
#                      help='the csv report to read')
#    parser.add_option('-b', action='store_false', dest='browser',
#                      default=False, help='Open report in browser or not')
#
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

    if cmd == 'sort':
        a = [40, 50, 20, 0, 1, 2, -1 ,30]
        x = sort.Sorter()
        if options.sort not in x.algorithms:
            print "No such sort algorithm:{}".format(options.sort)
            return 1

        if options.sort == 'bubble_recursion':
            x.run('bubble_recursion', a, len=len(a))
        elif options.sort == 'insert_recursion':
            x.run('insert_recursion', a, idx=1)
        elif options.sort == 'merge_recursion':
            x.run('merge_recursion', a, begin=0, rear=len(a)-1)
        elif options.sort == 'qsort':
            x.run('qsort', a, low=0, high=len(a)-1)
        else:
            x.run(options.sort, a)
            x.info()

    elif cmd == 'singlelinklist':
        link_list = linklist.SingleLinkList()
        data = ['a', 'b', 'c', 1, 2, 4, '0', 'anan', 'shanghai', 'rain']
        for i in xrange(len(data)):
            node = linklist.Node(data[i])
            link_list.insert_node_rear(node)
            #link_list.insert_node_head(node)
            print("list length: {}".format(link_list.info()))
            link_list.travel_list()
            link_list.reverse_list()
            link_list.travel_list()
            mid = link_list.seek_mid()
            print "middle node index {}, data: {}".format(mid.idx, mid.data)
            #link_list.remove_node(mid.idx)

    elif cmd == 'stack':
        s = stack.Stack(size=10)
        for i in xrange(10):
            s.push(i)
        s.travel_stack()


if __name__ == '__main__':
    sys.exit(main())
