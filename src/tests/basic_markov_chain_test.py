import unittest
from services import Chain
from main import Main

class TestChain(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        #Generates a list of weighted edges, where the weight corresponds to the frequency of said edge.
        graph = [
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7],
            [0,1,2,3,4,5,6,7]
        ]
        self.root = Main()
        self.edges = []
        self.edges = self.root.collect_edges(graph, self.edges)
        self.adj_template = [
            #a 0
            [
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 0
                [1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 1
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 2
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 3
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 4
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 5
                [1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 6
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0]  #dir 7
            ],
            #a 1
            [
                [1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 0
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 1
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 2
                [1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 3
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 4
                [1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 5
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 6
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0]  #dir 7
            ],
            #a 2
            [
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 0
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 1
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 2
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 3
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 4
                [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 5
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 6
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0]  #dir 7
            ],
            #a 3
            [
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 0
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 1
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 2
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 3
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 4
                [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0], #dir 5
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 6
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0]  #dir 7
            ],
            #a 4
            [
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 0
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 1
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 2
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 3
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 4
                [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0], #dir 5
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 6
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0]  #dir 7
            ],
            #a 5
            [
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 0
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 1
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 2
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 3
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 4
                [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0], #dir 5
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 6
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0]  #dir 7
            ],
            #a 6
            [
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 0
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 1
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0], #dir 2
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 3
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0], #dir 4
                [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0], #dir 5
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 6
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0]  #dir 7
            ],
            #a 7
            [
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 0
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0], #dir 1
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 2
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 3
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], #dir 4
                [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0], #dir 5
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0], #dir 6
                [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]  #dir 7
            ]
        ]

        #Generates a markov chain from the weighted edges.
        self.new_chain = Chain(self.edges, 8, self.root.direction_map)

    def test_possibilities_are_calculated_properly(self):
        self.assertEqual(self.adj_template, self.new_chain.adj)
    
    def test_neighbours_collected(self):
        ans = []
        ans.append(self.new_chain.get_neighbours((0,0), (8,8), True))
        ans.append(self.new_chain.get_neighbours((0,7), (8,8), True))
        ans.append(self.new_chain.get_neighbours((7,0), (8,8), True))
        ans.append(self.new_chain.get_neighbours((7,7), (8,8), True))
        ans.append(self.new_chain.get_neighbours((4,4), (8,8), True))

        template = [
            [(0,1),(1,0),(1,1)],
            [(0,6),(1,6),(1,7)],
            [(6,0),(6,1),(7,1)],
            [(6,6),(6,7),(7,6)],
            [(3,3),(3,4),(3,5),(4,3),(4,5),(5,3),(5,4),(5,5)]
        ]
            
        self.assertNotEqual(template, ans)
        for i in range(len(ans)): 
            ans[i].sort()
        self.assertEqual(template, ans)

    def test_color_selected_properly(self):
        ans = []
        c = self.new_chain.pick_color()
        ans.append((c in range(0, len(self.adj_template)), None, None, c))
        
        
        for i in range(0,7):
            for dir in range(0,7):
                c = self.new_chain.pick_color(i, dir)
                if c >= 0:
                    ans.append((self.adj_template[i][dir][c] > 0, i, dir, c))
        for a in ans:
            self.assertEqual((True, a[1], a[2], a[3]), a)

    def test_generated_image_is_correct_size(self):
        images = []
        template = []
        for i in range(50, 200, 50):
            for j in range(50, 200, 50):
                template.append((i,j))
                image = self.new_chain.generate_image((i,j), True)
                images.append((len(image[0]), len(image)))

        self.assertEqual(images, template)
