#! /usr/bin/env python
# coding=utf-8

from uuid import uuid4
from linklist import SingleLinkList
from data_structure import debug


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
        self._verbose = kwargs.get('verbose', False)
        if self._verbose:
            debug("Building {}".format(self), "Info")
    
    @property
    def isEmpty(self):
        return self.free_space == self.size

    @property
    def top(self):
        if not self.isEmpty:
            return self._top.data
        else:
            raise Exception("Empty Stack!")

    @property
    def base(self):
        return self._base.data

    @property
    def size(self):
        return self._size

    @property
    def free_space(self):
        return self._free

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
        
    def __str__(self):
        return "Stack {}: size:{}, free:{}"\
                .format(self.name, self._size, self.free_space)

    def __len__(self):
        return self.size - self.free_space

    def push(self, data):
        if self.free_space == 0:
            raise Exception("Stack is full!")
        self._store.insert_node_head(data)
        self._free -= 1
        self._base = self._store.rear
        self._top = self._store.head

    def pop(self):
        if not self.isEmpty:
            data = self._store.head.data
            self._store.remove_node(0)
            self._free += 1
            self._top = self._store.head
        else:
            data = None
        return data

    def info(self):
        debug(str(self))
        if not self.isEmpty:
            self._store.travel_list()
