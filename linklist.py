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
        print("\nTraveling list...")
        while p:
            print p
            p = p.next

    def info(self):
        return self.len

def main():
    link_list = SingleLinkList()
    data = ['a', 'b', 'c', 1, 2, 4, '0', 'anan', 'shanghai', 'rain']
    for i in xrange(len(data)):
        node = Node(data[i])
        link_list.insert_node_rear(node)
        #link_list.insert_node_head(node)
    print("list length: {}".format(link_list.info()))

    link_list.travel_list()
    link_list.reverse_list()
    link_list.travel_list()
    mid = link_list.seek_mid()
    print "middle node index {}, data: {}".format(mid.idx, mid.data)
    #link_list.remove_node(mid.idx)

if __name__ == '__main__':
    main()
