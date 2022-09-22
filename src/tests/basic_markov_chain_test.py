import unittest
import random
from basic_markov_chain import Chain
from basic_markov_chain import collect_edges

class TestChain(unittest.TestCase):
    def setUp(self):
        #Generates a list of weighted edges, where the weight corresponds to the frequency of said edge.
        self.n = random.randint(2,10)
        graph = [None]*self.n
        for  i in range(self.n):
            graph[i] = [random.randint(0,self.n-1)]*self.n
        self.edges = collect_edges(graph)

        #Generates a markov chain from the weighted edges.
        self.new_chain = Chain(self.edges, self.n)

    def test_possibilities_are_calculated_properly(self):
        edge_count = {}
        frequency = {}
        for i in range(self.n):
            edge_count[i] = 0
            for j in range(self.n):
                frequency[(i,j)] = 0
        for i in self.edges:
            frequency[(i[0],i[1])] = i[2]
            if i[0] in edge_count:
                edge_count[i[0]] += i[2]
            else:
                edge_count[i[0]] = i[2]
        
        adj_template = [None]*self.n
        for a in range(self.n):
            adj_template[a] = [None]*self.n
            for b in range(self.n):
                if (edge_count[a]) > 0:
                    adj_template[a][b] = frequency[(a,b)]/edge_count[a]
                else:
                    adj_template[a][b] = frequency[(a,b)]
        self.assertEqual(adj_template, self.new_chain.adj)
    
    def test_neighbours_collected(self):
        image_size = (100, 100)
        
        template = []
        ans = []
        i=0
        while(True):
            pos = (random.randint(0, image_size[0]), random.randint(0, image_size[1]))
            ans = self.new_chain.get_neighbours(pos, image_size)
            row_i, col_i = pos
            template = []
            if row_i > 0:
                template.append((row_i-1, col_i))
            if row_i < image_size[1]-1:
                template.append((row_i+1, col_i))
            if col_i > 0:
                template.append((row_i, col_i-1))
            if col_i < image_size[0]-1:
                template.append((row_i, col_i+1))
            if (template != ans or i > 10):
                break
            i+=1
        
        self.assertNotEqual(template, ans)
        
        
        ans.sort()
        template.sort()
        self.assertEqual(template, ans)




