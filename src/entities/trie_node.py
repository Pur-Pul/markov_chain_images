class TrieNode:
    def __init__(self, color):
        """This is the class for the nodes used in the trie datastructure.

        Args:
            color (int): The index of the color assigned to this node.
        """
        self.next = [{},{},{},{},{},{},{},{}]
        self.color = color
    def add_node(self, node, direction):
        """Adds the given node to the next list with the given direction
        or increments its frequency.

        Args:
            node (TrieNode): The TrieNode to add.
            direction (int): The directional index for the node to add.
        """
        if node not in self.next[direction]:
            self.next[direction][node] = 1
        else:
            self.next[direction][node] += 1
    def color_frequency_list(self, direction):
        """Returns the frequency list for the given direction.

        Args:
            direction (int): The direction to get the frequency list from

        Returns:
            The frequency list,
            containing the frequencies of the colors in the specified direction.
        """
        frequency_list = [[-1],[0]]
        for node in self.next[direction].items():
            frequency_list[0].append(node[0].color)
            frequency_list[1].append(node[1])
        return frequency_list
