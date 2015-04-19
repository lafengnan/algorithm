from uuid import uuid4
from linklist import SingleLinkList
from data_structure import debug

class Queue(object):
    """
    Queue reprensts a FIFO queue. A single link list will be used as
    its internal storage.
    @size: the queue size
    @name: the queue name
    """
    store_cls = SingleLinkList

    def __init__(self, size=1024, *args, **kwargs):
        self._size = size
        self._free = size
        self._store = self.store_cls()
        self._head = self._store.head
        self._rear = self._store.rear
        self._name = kwargs.get('name', str(uuid4()))
        self._verbose = kwargs.get('verbose', False)
        if self._verbose:
            debug("Building {}".format(self), "Info")

    @property
    def head(self):
        return self._head.data if self._head else "None"

    @property
    def rear(self):
        return self._rear.data if self._rear else "None"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def size(self):
        return self._size

    @property
    def free_space(self):
        return self._free

    @property
    def isEmpty(self):
        return self.free_space == self.size
    
    @property
    def isFull(self):
        return self.free_space == 0

    def __len__(self):
        return self.size - self.free_space

    def __str__(self):
        return "Queue:{}, size:{}".format(self.name, self.size)

    def __getitem__(self, idx):
        if idx < self.size - self.free_space:
            return self._store[idx].data

    def __setitem__(self, idx, value):
        if idx < self.size - self.free_space:
            self._store[idx].data = value

    def enqueue(self, data):
        if self.isFull:
            raise Exception("Queue is Full!")
        try:
            self._store.insert_node_rear(data)
            self._free -= 1
            self._head = self._store.head
            self._rear = self._store.rear
        except Exception as e:
            debug(str(e), 'Exceptpion')

    def dequeue(self):
        if self.isEmpty:
            raise Exception("Queue is Empty!")
        try:
            # 0 means to remove the first node form linklist
            self._store.remove_node(0)
            self._free += 1
            self._head = self._store.head
            self._rear = self._store.rear
        except Exception as e:
            debug(str(e), "Exception")

    def info(self):
        if not self.isEmpty:
            debug("Queue: {}:".format(self.name), 
                  "Info", 
                  "None Empty",
                  size=self.size,
                 free=self.free_space)
            self._store.travel_list()
        else:
            debug("Queue: {}:".format(self.name), 
                  "Info", 
                  'Empty',
                  size=self.size,
                 free=self.free_space)
