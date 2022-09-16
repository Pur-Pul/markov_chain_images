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

        for a in range(self.n):
            for b in range(self.n):
                if (edge_count[a]) > 0:
                    self.assertEqual(self.new_chain.adj[a][b], frequency[(a,b)]/edge_count[a])
                else:
                    self.assertEqual(self.new_chain.adj[a][b], frequency[(a,b)])


