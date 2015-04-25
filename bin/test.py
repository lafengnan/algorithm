#!/usr/bin/env python
# coding=utf-8

import sys
import os
import random
import traceback
from optparse import OptionParser
os.path.sys.path.append(os.path.dirname
                        (os.path.dirname(os.path.abspath(__file__))))

from algorithms import sort, polynomial
from data_structure import debug, linklist, stack, queue

Commands = ("sort", "singlelinklist", "doublelinklist",
            "search", "stack", 'poly', 'queue', 'pqueue')

USAGE = """
%prog <command> [options]
Commands:
""" + '\n'.join(["%10s: " % x for x in Commands])




def main():

    parser = OptionParser(USAGE)
    parser.add_option('-a', '--algorithm', type="string", dest="algorithm",
                      default='qsort',
                      help="config which sort algorithm to\
                      run[bubble|insert|merge|heapsort|qsort]")
    parser.add_option('-p', '--poly', type="string", dest="poly",
                      default='horner',
                      help="config the polynomial evaluation\
                      algorithm[horner|naive]")
    parser.add_option('-s', '--shardsize', type="int", dest="shard_size",
                      default=4,
                      help="config the shard size for merge_with_insert\
                      algorithm")
    parser.add_option('-v', action="store_true", dest="verbose", default=False,
                      help="verbose mode")

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
        b = range(1000, -1, -1)
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
            #c = [2, 3, 8, 6, 1, 5]
            #x.run(method, c, low=0, high=len(b)-1, shard_size=3)
            x.run(method, b, low=0, high=len(b)-1)
        else:
            x.run(options.sort, a)
            x.run(options.sort, b)
        x.info()

    elif cmd == 'singlelinklist':
        link_list = linklist.SingleLinkList()
        data = ['a', 'b', 'c', 1, 2, 4, '0', 'anan', 'shanghai', 'rain']
        for i in xrange(len(data)):
            node = linklist.Node(data[i])
            link_list.insert_node_rear(node)
            #link_list.insert_node_head(node)
        print link_list
        print "trave list:"
        link_list.travel_list()
        link_list.reverse_list()
        print "after reverse:"
        link_list.travel_list()
        mid = link_list.seek_mid()
        print "middle node index {}, data: {}".format(mid.idx, mid.data)
        link_list[mid.idx] = 'anan'
        link_list.travel_list()
        print link_list[0]
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
            dllist.insert_node('anan', 3)
        except IndexError as e:
            print e
        print dllist
        dllist.travel()
        for p in dllist:
            print p
        try:
            dllist.remove_node(2)
        except IndexError as e:
            print e
        print dllist
        dllist.travel()
        print "\n", dllist[4]
        dllist[0] = 'anan'
        print "\n"
        dllist.travel()

    elif cmd == 'stack':
        s = stack.Stack(size=15, verbose=options.verbose)
        for i in xrange(10):
            s.push(i)
        s.info()
        print "stack size:{}, active elements:{}, free_space:{}"\
                .format(s.size, len(s), s.free_space)

    elif cmd == 'poly':
        x = 5
        factors = range(1000)
        if options.poly == 'horner':
            print polynomial.horner(x, factors)
        else:
            print polynomial.naive(x, factors)

    elif cmd == 'search':
        a = [40, 50, 40, 20, 0, 1, 2, -1 ,30]
        b = range(1000,0,-1)
        search = sort.Search(options.algorithm, verbose=options.verbose)
        print search.search(1, a)
        #print search.search(0, a)
        #print search.search(2, a)
        #print search.search(40, a)
        #print search.search(60, a)
        print search.search(20, b)
        print search.search(90, b)
        print search.search(90, a)

    elif cmd == 'queue':
        a = [40, 50, 40, 20, 0, 1, 2, -1 ,30]
        q = queue.Queue(capacity=20, verbose=options.verbose)
        for x in a:
            q.enqueue(x)
        q.info()
        print q[3]
        q[3] = 'anan'
        q.info()
        print q.head, q.rear
        i = 0
        while i < len(a):
            try:
                print "dequeue: ", q.dequeue()
            except Exception as e:
                pass
            i += 1
        q.info()
        print q.head, q.rear

    elif cmd == 'pqueue':
        #a = [40, 50, 40, 20, 0, 1, 2, -1 ,30, 60]
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pf = lambda end: random.randint(0, end)
        q = queue.PQueue(20, verbose=options.verbose)
        try:
            for x in a:
                q.enqueue(x, pf(3))
        except Exception as e:
            debug(e, "exceptions")
            exc_type, exc_value, exc_tb = sys.exc_info()
            debug(traceback.print_tb(exc_tb, file=sys.stdout), "Exception")
        q.info()
        print q.head, q.rear
        print "dequeue: ", q.dequeue()
        q.info()
        print q.head, q.rear
        

if __name__ == '__main__':
    sys.exit(main())
