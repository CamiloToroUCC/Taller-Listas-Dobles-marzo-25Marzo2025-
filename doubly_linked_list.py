# doubly_linked_list.py

class Node:
    def __init__(self, data):
        self.data = data  #valor
        self.prev = None #
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_at_position(self, data, pos):
        if pos <= 0:
            self.insert_at_beginning(data)
        elif pos >= self.size:
            self.insert_at_end(data)
        else:
            new_node = Node(data)
            current = self.traverse_to_index(pos)
            prev_node = current.prev
            prev_node.next = new_node
            new_node.prev = prev_node
            new_node.next = current
            current.prev = new_node
            self.size += 1

    def delete_at_position(self, pos):
        if pos < 0 or pos >= self.size or not self.head:
            return
        if pos == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif pos == self.size - 1:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
        else:
            current = self.traverse_to_index(pos)
            current.prev.next = current.next
            current.next.prev = current.prev
        self.size -= 1

    def traverse_to_index(self, pos):
        current = self.head
        for _ in range(pos):
            current = current.next
        return current

    def get_node(self, pos):
        if pos < 0 or pos >= self.size:
            return None
        return self.traverse_to_index(pos)

    def move_to_beginning(self, pos):
        if pos <= 0 or pos >= self.size:
            return
        node = self.get_node(pos)
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node == self.tail:
            self.tail = node.prev
        node.prev = None
        node.next = self.head
        self.head.prev = node
        self.head = node

    def move_up(self, pos):
        if pos <= 0 or pos >= self.size:
            return
        node1 = self.get_node(pos)
        node2 = self.get_node(pos - 1)
        node1.data, node2.data = node2.data, node1.data

    def move_down(self, pos):
        if pos < 0 or pos >= self.size - 1:
            return
        node1 = self.get_node(pos)
        node2 = self.get_node(pos + 1)
        node1.data, node2.data = node2.data, node1.data

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
