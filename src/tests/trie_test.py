import unittest
from entities import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.trie.add_edge(1, 10, 0)
        self.trie.add_edge(2, 9, 1)
        self.trie.add_edge(3, 8, 2)
        self.trie.add_edge(4, 7, 3)
        self.trie.add_edge(5, 6, 4)
        self.trie.add_edge(1, 10, 5)
        self.trie.add_edge(2, 9, 6)
        self.trie.add_edge(3, 8, 7)
        self.trie.add_edge(4, 7, 0)
        self.trie.add_edge(5, 6, 1)
        self.trie.add_edge(1, 10, 2)
        self.trie.add_edge(2, 9, 3)
        self.trie.add_edge(3, 8, 4)
        self.trie.add_edge(1, 10, 5)
        self.trie.add_edge(2, 9, 6)
        self.trie.add_edge(3, 8, 7)
        self.trie.add_edge(4, 7, 0)
        self.trie.add_edge(5, 6, 1)
        self.trie.add_edge(1, 10, 2)
        self.trie.add_edge(2, 9, 3)
        self.trie.add_edge(3, 8, 4)
        self.trie.add_edge(4, 7, 5)
        self.trie.add_edge(5, 6, 6)
        self.trie.add_edge(1, 10, 7)
        self.trie.add_edge(2, 9, 0)
        self.trie.add_edge(3, 8, 1)
    
    def test_node_dict_is_constructed_properly(self):
        template = [1,2,3,4,5,6,7,8,9,10]
        
        trie_list = [key for key in self.trie.nodes]
        trie_list.sort()
        self.assertEqual(template, trie_list)
    
    def test_color_frequency_list_returns_correct_value(self):
        ans = [
            self.trie.color_frequency_list(1, 0),
            self.trie.color_frequency_list(2, 1),
            self.trie.color_frequency_list(3, 2),
            self.trie.color_frequency_list(4, 3),
            self.trie.color_frequency_list(5, 4),
            self.trie.color_frequency_list(6, 5),
            self.trie.color_frequency_list(7, 6),
            self.trie.color_frequency_list(8, 7),
            self.trie.color_frequency_list(9, 0),
            self.trie.color_frequency_list(10, 1),
            self.trie.color_frequency_list(1, 2),
            self.trie.color_frequency_list(2, 3),
            self.trie.color_frequency_list(3, 4),
            self.trie.color_frequency_list(4, 5),
            self.trie.color_frequency_list(5, 6),
            self.trie.color_frequency_list(6, 7),
            self.trie.color_frequency_list(7, 0),
            self.trie.color_frequency_list(8, 1),
            self.trie.color_frequency_list(9, 2),
            self.trie.color_frequency_list(10, 3)
        ]
        template = [
            self.trie.nodes[1].color_frequency_list(0),
            self.trie.nodes[2].color_frequency_list(1),
            self.trie.nodes[3].color_frequency_list(2),
            self.trie.nodes[4].color_frequency_list(3),
            self.trie.nodes[5].color_frequency_list(4),
            self.trie.nodes[6].color_frequency_list(5),
            self.trie.nodes[7].color_frequency_list(6),
            self.trie.nodes[8].color_frequency_list(7),
            self.trie.nodes[9].color_frequency_list(0),
            self.trie.nodes[10].color_frequency_list(1),
            self.trie.nodes[1].color_frequency_list(2),
            self.trie.nodes[2].color_frequency_list(3),
            self.trie.nodes[3].color_frequency_list(4),
            self.trie.nodes[4].color_frequency_list(5),
            self.trie.nodes[5].color_frequency_list(6),
            self.trie.nodes[6].color_frequency_list(7),
            self.trie.nodes[7].color_frequency_list(0),
            self.trie.nodes[8].color_frequency_list(1),
            self.trie.nodes[9].color_frequency_list(2),
            self.trie.nodes[10].color_frequency_list(3),
        ]
        self.assertEqual(template, ans)
