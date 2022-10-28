from .node import Node
class Stack:
    def __init__(self):
        """This is the class for the Stack used in the depth-first traversal.
        """
        self.f_node = None
        self.size = 0
    def add(self, value):
        """This function adds a new Node to the top of the stack.

        Args:
            value: The value of the node added.
        """
        new_node = Node(value)
        if self.f_node is None:
            self.f_node = new_node
        else:
            new_node.next = self.f_node
            self.f_node = new_node
        self.size += 1
    def pop(self):
        """This function pops the top element from the stack.

        Returns:
            to_return: The value of the popped Node.
        """
        to_return = self.f_node.value
        self.f_node = self.f_node.next
        self.size -= 1
        return to_return
