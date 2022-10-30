from .trie_node import TrieNode

class Trie:
    def __init__(self):
        """This is the class for the trie datastructure.
        """
        self.nodes = {}

    def add_edge(self, color_a, color_b, direction):
        """This adds an edge to the trie.

        Args:
            color_a (int): The index of the start color.
            color_b (int): The index of the destination color.
            direction (int): The index of the direction.
        """
        for color in [color_a,color_b]:
            if color not in self.nodes:
                self.nodes[color] = TrieNode(color)
        self.nodes[color_a].add_node(self.nodes[color_b], direction)

    def color_frequency_list(self, color_a, direction):
        """Returns the frequency list

        Args:
            color_a (int): The start color.
            direction (int: The direction.

        Returns:
            The frequency list.
        """
        return self.nodes[color_a].color_frequency_list(direction)
