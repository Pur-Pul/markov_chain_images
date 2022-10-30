import unittest
from entities import TrieNode

class TestTrieNode(unittest.TestCase):
    def setUp(self):
        self.node = TrieNode(1)
        one = TrieNode(1)
        two = TrieNode(2)
        three = TrieNode(3)
        four = TrieNode(4)
        five = TrieNode(5)
        six = TrieNode(6)
        seven = TrieNode(7)
        eight = TrieNode(8)
        nine = TrieNode(9)
        ten = TrieNode(10)

        self.node.add_node(one,0)
        self.node.add_node(two,1)
        self.node.add_node(three,2)
        self.node.add_node(four,3)
        self.node.add_node(five,4)
        self.node.add_node(six,5)
        self.node.add_node(seven,6)
        self.node.add_node(eight,7)
        self.node.add_node(nine,0)
        self.node.add_node(ten,1)
        self.node.add_node(one,2)
        self.node.add_node(two,3)
        self.node.add_node(three,4)
        self.node.add_node(four,5)
        self.node.add_node(five,6)
        self.node.add_node(six,7)
        self.node.add_node(seven,0)
        self.node.add_node(eight,1)
        self.node.add_node(nine,2)
        self.node.add_node(ten,3)
        self.node.add_node(one,0)
        self.node.add_node(two,1)
        self.node.add_node(three,2)
    
    def test_color_is_correct(self):
        self.assertEqual(1, self.node.color)
    
    def text_nodes_are_added_properly(self):
        template = [
            {1 : 2, 9 : 1, 7 : 1},
            {2 : 2, 10 : 1, 8 : 1},
            {3 : 2, 1 : 1, 9 : 1},
            {4 : 1, 2 : 1, 10 : 1},
            {5 : 1, 3 : 1},
            {6 : 1, 4 : 1},
            {7 : 1, 5 : 1},
            {8 : 1, 6 : 1}
        ]
        self.assertEqual(template, self.node.next)
    
    def test_color_frequency_list_is_constructed_correctly(self):
        template = [
            [
                [-1,1,9,7],
                [0,2,1,1]
            ],
            [
                [-1,2,10,8],
                [0,2,1,1]
            ],
            [
                [-1,3,1,9],
                [0,2,1,1]
            ],
            [
                [-1,4,2,10],
                [0,1,1,1]
            ],
            [
                [-1,5,3],
                [0,1,1]
            ],
            [
                [-1,6,4],
                [0,1,1]
            ],
            [
                [-1,7,5],
                [0,1,1]
            ],
            [
                [-1,8,6],
                [0,1,1]
            ]
        ]
        ans = [
            self.node.color_frequency_list(0),
            self.node.color_frequency_list(1),
            self.node.color_frequency_list(2),
            self.node.color_frequency_list(3),
            self.node.color_frequency_list(4),
            self.node.color_frequency_list(5),
            self.node.color_frequency_list(6),
            self.node.color_frequency_list(7)
        ]
        self.assertEqual(template, ans)
