from .trie_node import TrieNode

class Trie:
    def __init__(self):
        self.nodes = {}

    def add_edge(self,a,b,dir):
        for color in [a,b]:
            if color not in self.nodes:
                self.nodes[color] = TrieNode(color)
        self.nodes[a].add_node(self.nodes[b], dir)

    def color_frequency_list(self,a,dir):
        return self.nodes[a].color_frequency_list(dir)
