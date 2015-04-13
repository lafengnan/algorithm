#! /usr/bin/env python
# coding=utf-8

class Node(object):
    """
    The Node class for link list
    @data: the data of one node
    """
    def __init__(self, data):
        super(Node, self).__init__()
        self._idx = 0
        self._data = data
        self.next = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, value):
        self._idx = value

    def __str__(self):
        return "\tindex:{}, data: {}".format(self._idx, self._data)

class SingleLinkList(object):
    """
    The SingleLinkList class represents a single link list. In the
    list each node is an instance of Node class. The link list is shown
    as below example (3 data nodes).
    @kwargs: opts for link list creation. TBD

      List
    .------.
    | len  |
    .------.
    | opts |
    .------.       Node 0           Node 1           Node 2
    | head | ---->.------.   .---->.------.   .---->.------.
    .------.      | idx  |   |     | idx  |   |     | idx  |
    | rear | --.  .------.   |     .------.   |     .------.
    *------*   |  | data |   |     | data |   |     | data |
               |  .------.   |     .------.   |     .------.
               |  | next |---*     | next |---*     | next |---> None
               |  *------*         *------*         *------*
               |                                       ^
               |                                       |
               *---------------------------------------*

    """
    def __init__(self, **kwargs):
        super(SingleLinkList, self).__init__()
        self.len = 0
        self.opts = kwargs
        self.head = None
        self.rear = None

    def __str__(self):
        return "List:{}\n\tlen = {}\n\thead = {}\n\trear ={}"\
                .format(hex(id(self)), self.len, self.head, self.rear)

    def insert_node_head(self, node):
        if isinstance(node, Node):
            # Head is None, means empty link list
            if not self.head:
                self.head = node
                self.rear = node
            else:
                p = self.head
                self.head = node
                node.next = p
                # Increase all the following nodes' index value
                while p:
                    p.idx += 1
                    p = p.next
            self.len += 1
        else:
            raise Exception("Wrong type node!")

    def insert_node_rear(self, node):
        if isinstance(node, Node):
            # Head is None, means empty link list
            if not self.head:
                self.head = node
                self.rear = node
                node.idx = 0
            else:
                p = self.rear
                self.rear = node
                p.next = node
                node.idx = p.idx + 1
            self.len += 1
        else:
            raise Exception("Wrong type node!")

    def remove_node(self, idx):
        """
        Remove the idxth node from link list
        """
        if self.len == 0:
            raise Exception("try to remove node from empty list")
        if idx >= self.len:
            raise IndexError("idx:{} is out of range".format(idx))

        p = q = self.head

        # Delete first node
        if idx == 0:
            self.head = p.next
            p.next = None
        else:
            while idx:
                q = p
                p = p.next
                idx -= 1
            # 1. The idxth node is rear node
            if not p.next:
                # 1.1 Only one node
                if p == q:
                    self.head = self.rear = None
                else:
                    self.rear = q
                    q.next = None
            # 2. The idxth node is not rear node
            else:
                q.next = p.next
                p.next = None
                tmp = q.next
                # Decrease the index value for the rest nodes
                while tmp:
                    tmp.idx -= 1
                    tmp = tmp.next
        del p
        self.len -= 1

    def seek_mid(self):
        """
        Using quick pointer and slow pointer to seek the middle node
        """
        slow = quick = self.head
        if not slow:
            return None
        while quick.next:
            quick = quick.next.next
            slow = slow.next
            if not quick:
                break
        return slow

    def reverse_list(self):
        """
        Reverse a single link list:
        a -> b -> c -> d becomes:
        d -> c -> b -> a
        """
        # Empty list equals to reversed empty list
        # One node list equals to reversed one node list
        if self.len == 0 or self.len == 1:
            return
        else:
            p = self.head
            q = self.head.next
            s = self.head.next.next
            # Only two nodes
            if not s:
                # Two node, just swap data
                p.data, q.data = q.data, p.data

                # Anoher way is operate next pointer
                #self.head = q
                #self.rear = p
                #q.next = p
                #p.next = None
            else:
                new_rear = p # save the new rear
                while s:
                    q.next = p
                    p = q
                    q = s
                    s = s.next
                q.next  = p
                # Rebuild head and rear
                self.rear = new_rear
                new_rear.next = None
                self.head = q
                # Reset index value
                p = self.head
                new_idx = 0
                while p:
                    p.idx = new_idx
                    p = p.next
                    new_idx += 1

    def travel_list(self):
        p = self.head
        while p:
            print p
            p = p.next

class DoubleLinkList(object):
    """
    Represents a double link list object. A double link list looks like the
    example below.(Has 3 data nodes)

     DBList
    .------.
    | len  |
    .------.                .------------------------------------.
    | opts |                |                                    |
    .------.       Node 0   |        Node 1           Node 2     |
    | head |----->.------.  | .--->.------.    .---->.------.    |
    .------.      | idx  |<-* |     | idx  |   |     | idx  |    |
    | rear |      .------.    |     .------.   |     .------.    |
    *------*      | data |    |     | data |   |     | data |    |
       |          .------.    |     .------.   |     .------.    |
       |          | next |----*     | next |---*     | next |----*
       *--------->*------*          *------*         *------*
                  | prev |<---------| prev |<--------| prev |
                  *------*          *------*         *------*
                     |                                  ^
                     |                                  |
                     *----------------------------------*

    """
    class _Node(object):
        """
        _Node represents a node in one double link list. It looks like the
        below figure.
        @idx: the index of the node in one double link list
        @data: the data stored in the node
        @prev: the previos potiner of a node, it points to its previos node
        @next: the next pointer of a node, it points to the next node

        .------.
        | idx  |
        *------*
        | data |
        *------*
        | prev |
        *------*
        | next |
        *------*
        """
        def __init__(self, data, *args, **kwargs):
            super(DoubleLinkList._Node, self).__init__()
            self._idx = 0
            self._data = data
            self.next = self.prev = None
            self._args = args
            self._kwargs = kwargs

        @property
        def index(self):
            return self._idx

        @index.setter
        def index(self, value):
            self._idx = value

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, value):
            self._data = value

        def __str__(self):
            return "\tindex:{}, data:{}, prev:{}, next:{}"\
                .format(self.index,
                        self.data,
                        self.prev.index,
                        self.next.index)

    def __init__(self, *args, **kwargs):
        super(DoubleLinkList, self).__init__()
        self._len = 0
        self.args = args
        self.node_cls = kwargs.get('node', None) or self._Node
        self.head = self.rear = None
        self.kwargs = kwargs

    @property
    def len(self):
        return self._len

    def inc_len(self):
        self._len += 1

    def dec_len(self):
        self._len -= 1

    def __str__(self):
        return "DoubleLinkList: {}, length: {}".format(hex(id(self)), self.len)

    def insert_node(self, data, pos=-1, *args, **kwargs):
        """
        Insert a node into the list after the specified postion.
        """
        _node = self.node_cls(data)
        # 1. Insert into an empty double link list
        if self._len == 0:
            self.head = self.rear = _node
            _node.prev = _node.next = _node
        # 2. Insert into a nonempty double link list
        else:
            # 2.1 In default insert the node from the begining
            if pos == -1:
                _node.next = self.head
                self.head.prev = _node
                self.head = _node
                self.rear = _node
                # Update index value
                p = self.head.next
                count = 0
                while p and count < self.len:
                    p.index += 1
                    count += 1
                    p = p.next
                    # Rebuild last node and head node relaion:
                    # tail->next = head
                    # head->prev = tail
                    if count == self.len - 1:
                        p.next = self.head
                        self.head.prev = p
            # 2.2  pos represents the node to insert after
            elif pos >= 0:
                if pos >= self.len:
                    raise IndexError("position:{} is over list length: {}"\
                                     .format(pos, self.len))
                if pos < len:
                    p = self.head
                    cur = pos
                    while cur:
                        p = p.next
                        cur -= 1
                    # Insert
                    _node.next = p.next
                    p.next.prev = _node
                    p.next = _node
                    _node.prev = p

                    # Increase index for the following nodes
                    # Firtly Init new node index to p's index
                    _node.index = p.index
                    p = p.next
                    cur = 0
                    while p and cur < self.len - pos:
                        p.index += 1
                        p = p.next
                        cur += 1
        self.inc_len()

    def remove_node(self, pos):
        """
        Remove the node @pos
        """
        # 1. Empty list, return
        if self.len == 0:
            return
        else:
            if pos < self.len:
                cur = pos
                p = self.head
                # Remove the first node
                if cur == 0:
                    self.head = p.next
                    p.prev.next = p.next
                    p.next.prev = p.prev
                    p.prev = p.next = None
                else:
                    while cur:
                        p = p.next
                        cur -= 1
                    p.prev.next = p.next
                    p.next.prev = p.prev
                    p.next = p.prev = None
                del p
                self.dec_len()
                # Update index
                cur = pos
                p = self.head
                while cur:
                    p = p.next
                    cur -= 1
                update = 0
                while update < self.len - pos:
                    p.index -= 1
                    p = p.next
                    update += 1
            else:
                raise IndexError("Position:{} is over list range:{}"\
                                 .format(pos, self.len))

    def travel(self):
        p = self.head
        cur = 0
        while p and cur < self.len:
            print p
            p = p.next
            cur += 1
