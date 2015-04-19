#! /usr/bin/env python
# coding=utf-8

from linklist import SingleLinkList, Node
from uuid import uuid4


class Stack(object):
    """
    Simulate the stack data structure. The stack will use
    single linklist as its internal storage
    """
    store_cls = SingleLinkList
    def __init__(self, size=1024, *args, **kwargs):
        self._size = size
        self._free = size
        self._store = self.store_cls()
        self._base = self._store.rear
        self._top = self._store.head
        self._args = args
        self._kwargs = kwargs
        self._name = kwargs.get('name', str(uuid4()))

    @property
    def top(self):
        return self._top.data

    @property
    def base(self):
        return self._base.data

    @property
    def size(self):
        return self._size

    @property
    def free(self):
        return self._free

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def push(self, data):
        if self._free == 0:
            raise Exception("Stack is full!")
        _node = Node(data)
        self._store.insert_node_head(_node)
        self._free -= 1
        self._base = self._store.rear
        self._top = self._store.head

    def pop(self):
        if self._base != self._top:
            data = self._store.head.data
            self._store.remove_node(0)
            self._free += 1
            self._top = self._store.head
        else:
            data = None
        return data

    def empty(self):
        return self._base == self._top
    
    def __str__(self):
        return "stack {}: size:{}, free:{}"\
                .format(id(self), self._size, self._free)

    def __len__(self):
        return self.size - self.free

    def info(self):
        print "stack:{}:\n".format(self.name)
        if self._base != self._top:
            self._store.travel_list()
