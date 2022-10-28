from .trie_node import TrieNode

class Trie:
    def __init__(self):
        self.nodes = {}

    def add_edge(self, color_a, color_b, direction):
        for color in [color_a,color_b]:
            if color not in self.nodes:
                self.nodes[color] = TrieNode(color)
        self.nodes[color_a].add_node(self.nodes[color_b], direction)

    def color_frequency_list(self, color_a, direction):
        return self.nodes[color_a].color_frequency_list(direction)
