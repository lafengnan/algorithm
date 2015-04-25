from uuid import uuid4
from linklist import SingleLinkList
from data_structure import debug

class Queue(object):
    """
    Queue reprensts a FIFO queue. A single link list will be used as
    its internal storage.
    @capacity: the queue capacity
    @name: the queue name
    """
    store_cls = SingleLinkList

    def __init__(self, capacity=1024, *args, **kwargs):
        self._capacity = capacity
        self._free = capacity
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
    def capacity(self):
        return self._capacity

    @property
    def free_space(self):
        return self._free

    @property
    def isEmpty(self):
        return self.free_space == self.capacity
    
    @property
    def isFull(self):
        return self.free_space == 0

    def __len__(self):
        return self.capacity - self.free_space

    def __str__(self):
        return "Queue:{}, capacity:{}".format(self.name, self.capacity)

    def __getitem__(self, idx):
        if idx < self.capacity - self.free_space:
            return self._store[idx].data

    def __setitem__(self, idx, value):
        if idx < self.capacity - self.free_space:
            self._store[idx].data = value

    def enqueue(self, data):
        if self.isFull:
            raise Exception("Queue is Full!")
        try:
            self._store.insert_node_rear(data)
            self._head = self._store.head
            self._rear = self._store.rear
            self._free -= 1
        except Exception:
            raise

    def dequeue(self):
        if self.isEmpty:
            raise Exception("Queue is Empty!")
        try:
            # 0 means to remove the first node form linklist
            element = self[0]
            self._store.remove_node(0)
            self._head = self._store.head
            self._rear = self._store.rear
            self._free += 1
            return element
        except Exception:
            raise

    def info(self):
        debug("Queue: {}:".format(self.name),
              "Info",
              empty=self.isEmpty,
              capacity=self.capacity,
              free=self.free_space)

        if not self.isEmpty:
            self._store.travel_list()

class PQueue(Queue):
    """
    Priority Queue
    The priority queue id different from a FIFO queue, it will pop the elementa
    according to user defined priority.
    The data in PQueue should conform with the following format:

        data = {'priority': 0, 'data': 'anan'},

    the priority number SHOULD be a none-negative interge.
    """
    store_cls = SingleLinkList
    MIN_PRI = -0x7fffffff #Represents infinity 

    def __init__(self, capacity=1024, *args, **kwargs):
        super(PQueue, self).__init__(capacity, *args, **kwargs)
        self._heap_size = 0
           
    def _max_heap_insert(self, data):
        def _heap_increase_key(q, idx, data):
            _parent = lambda x: x >> 1 if x % 2 else (x >> 1) - 1

            if data['priority'] < q[idx].get('priority', 0):
                raise Exception("New priority is smaller than current \
                                priority!")
           
            q[idx]['priority'] = data['priority']
            while idx > 0 and q[_parent(idx)]['priority'] < q[idx]['priority']:
                q[idx], q[_parent(idx)] = q[_parent(idx)], q[idx]
                idx = _parent(idx)

        q = self
        if 'priority' not in data.keys():
            raise Exception("Data:{} missing priority info".format(data))
        q._heap_size += 1
        #q[q._heap_size - 1] = {'priority':q.MIN_PRI, 'data':"xxx"}
        _heap_increase_key(q, q._heap_size - 1, data)

    def _heap_extract_max(self):
        _left = lambda x: (x << 1) + 1
        _right = lambda x: (x << 1) + 2
        def _max_heapify(q, idx):
            l = _left(idx)
            r = _right(idx)

            if l <= q._heap_size and q[l]['priority'] > q[idx]['priority']:
                largest = l
            else:
                largest = idx
            if r <= q._heap_size and q[r]['priority'] > q[largest]['priority']:
                largest = r
            if largest != idx:
                q[idx], q[largest] = q[largest], q[idx]
                _max_heapify(q, largest)

        if self._heap_size < 1:
            raise Exception("Heap underflow!")

        q = self
        q._heap_size -= 1
        _max_heapify(q, 0)

    def enqueue(self, data, priority):
        if self.isFull:
            raise Exception("Queue is full!")
        try:
            # Encapluse the data into a dict
            data = {'priority':priority, 'data':data}
            self._store.insert_node_rear(data)
            self._head = self._store.head
            self._rear = self._store.rear
            self._free -= 1
            # Invoke _max_heap_insert to keep heap stable
            self._max_heap_insert(data)
        except Exception:
            raise

    def dequeue(self):
        if self.isEmpty:
            raise Exception("Empty Queue!")
        try:
            data = self[0]
            self._store.remove_node(0)
            self._head = self._store.head
            self._rear = self._store.rear
            self._free += 1
            self._heap_extract_max()
            return data
        except Exception:
            raise

    def info(self):
        debug("PQueue: {}:".format(self.name),
              "Info",
              empty=self.isEmpty,
              capacity=self.capacity,
              free=self.free_space)

        if not self.isEmpty:
            self._store.travel_list()
