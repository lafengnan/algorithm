#!/usr/bin/env python
# coding=utf-8

import sys
import os
from optparse import OptionParser
os.path.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import sort, polynomial
from data_structure import linklist, stack

Commands = ("sort", "singlelinklist", "doublelinklist", "stack", 'poly')

USAGE = """
%prog <command> [options]
Commands:
""" + '\n'.join(["%10s: " % x for x in Commands])




def main():

    parser = OptionParser(USAGE)
    parser.add_option('-a', '--algorithm', type="string", dest="algorithm", default='qsort',
                      help="config which sort algorithm to run[bubble|insert|merge|heapsort|qsort]")
    parser.add_option('-p', '--poly', type="string", dest="poly", default='horner',
                      help="config the polynomial evaluation algorithm[horner|naive]")
    parser.add_option('-s', '--shardsize', type="int", dest="shard_size", default=4,
                      help="config the shard size for merge_with_insert algorithm")
#    parser.add_option('-a', action="store_true", dest="asc", default=False,
#                      help="display the records in ascending or descending")

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
        if options.algorithm not in x.algorithms:
            print "No such sort algorithm:{}".format(options.algorithm)
            return 1

        method = options.algorithm

        if method == 'bubble_recursion':
            x.run(method, a, len=len(a))
        elif method == 'insert_recursion':
            x.run(method, a, idx=1)
        elif method.startswith('merge') or method == 'qsort':
            x.run(method, a, low=0, high=len(a)-1)
            # Below case is used for get reversion-pare numbers in one sequence
            # <<Introduction to Algorithms, page 24, 2-4>>, the reversion-pair
            # number equals to the swap times of insert sort
            b = [2, 3, 8, 6, 1, 5]
            x.run(method, b, low=0, high=len(b)-1, shard_size=3)
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
    elif cmd == 'doublelinklist':
        dllist = linklist.DoubleLinkList()
        try:
            for i in xrange(5):
                dllist.insert_node(i)
        except IndexError as e:
            print e
        print dllist
        dllist.travel()
        try:
            dllist.insert_node('anan', 4)
            dllist.insert_node('anan', 6)
        except IndexError as e:
            print e
        print dllist
        dllist.travel()

    elif cmd == 'stack':
        s = stack.Stack(size=10)
        for i in xrange(10):
            s.push(i)
        s.travel_stack()

    elif cmd == 'poly':
        x = 5
        factors = range(1000)
        if options.poly == 'horner':
            print polynomial.horner(x, factors)
        else:
            print polynomial.naive(x, factors)


if __name__ == '__main__':
    sys.exit(main())
