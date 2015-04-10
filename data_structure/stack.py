#! /usr/bin/env python
# coding=utf-8

from linklist import SingleLinkList, Node


class Stack(object):
    """
    Simulate the stack data structure. The stack will use
    single linklist as its internal storage
    """
    def __init__(self, size=1024):
        self._size = size
        self._free = size
        self._linklist = SingleLinkList()
        self._base = self._linklist.rear
        self._top = self._linklist.head

    def push(self, data):
        if self._free == 0:
            raise Exception("Stack is full!")
        _node = Node(data)
        self._linklist.insert_node_head(_node)
        self._free -= 1
        self._base = self._linklist.rear
        self._top = self._linklist.head

    def pop(self):
        if self._base != self._top:
            data = self._linklist.head.data
            self._linklist.remove_node(0)
            self._free += 1
            self._top = self._linklist.head
        else:
            data = None
        return data
    
    def __str__(self):
        return "stack {}: size:{}, free:{}"\
                .format(id(self), self._size, self._free)

    def travel_stack(self):
        if self._base != self._top:
            self._linklist.travel_list()
