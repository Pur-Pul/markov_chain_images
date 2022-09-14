class chain:
    def __init__(self, edges, n):
        self.adj = [None] * n
        self.lengths = [0] * n
        for i in range(n):
            self.adj[i] = []
            #print(i)
        
        for (a, b, w) in edges:
            self.adj[a].append([b, w])
            self.lengths[a] += w
        
        self.calculate_possibities()

    def calculate_possibities(self):
        for a in range(n):
            a_len = len(self.adj[a])
            for j in range(a_len):
                self.adj[a][j][1] /= self.lengths[a]

    def print(self):
        for a in range(n):
            for j in range(len(self.adj[a])):
                b = self.adj[a][j][0]
                w = self.adj[a][j][1]
                print("(" + str(a) + "," + str(b) + ")" + " : " + str(w))


n = int(input())
graph = []
weights = {}
for i in range(n):
    key = input()
    if key in weights:
        weights[key] += 1
    else: 
        weights[key] = 1
for k in weights.keys():
    a, b = k.split(" ")
    graph.append((int(a), int(b), weights[k]))

new_chain = chain(graph, n)
new_chain.print()