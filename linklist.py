#! /usr/bin/env python
# coding=utf-8

class Node(object):
    """
    The Node object for link list
    @data: the data of one node
    """
    def __init__(self, data):
        self.data = data
        self.next = None


class SingleLinkList(object):
    """
    The single link list object
    """
    def __init__(self):
        self.len = 0
        self.head = None
        self.rear = None

    def insert_node(self, node):
        if isinstance(node, Node):
            # Head is None, means empty link list
            if not self.head:
                self.head = node
                self.rear = node
            else:
                p = self.rear
                self.rear = node
                p.next = node
            self.len += 1

    def seek_mid(self):
        slow = self.head
        quick = self.head
        while quick:
            slow = slow.next
            quick = quick.next.next
        print slow.data


    def travel_list(self):
        p = self.head
        while p:
            print p.data
            p = p.next

    def info(self):
        print("List length: {}".format(self.len))

def main():
    linkList = SingleLinkList()
    data = ['a', 'b', 'c', 1, 2, 4, '0', 'anan', 'shanghai', 'rain']
    for i in xrange(10):
        node = Node(data[i])
        linkList.insert_node(node)
    linkList.travel_list()
    linkList.info()
    linkList.seek_mid()

if __name__ == '__main__':
    main()
