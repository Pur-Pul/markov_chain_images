class chain:
    def __init__(self, edges, n):
        self.n = n
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
        for a in range(self.n):
            a_len = len(self.adj[a])
            for j in range(a_len):
                self.adj[a][j][1] /= self.lengths[a]

    def print(self):
        for a in range(self.n):
            for j in range(len(self.adj[a])):
                b = self.adj[a][j][0]
                w = self.adj[a][j][1]
                print("(" + str(a) + "," + str(b) + ")" + " : " + str(w))

def add_to_graph(key, weights):
    if key in weights:
        weights[key] += 1
    else: 
        weights[key] = 1
    return weights

def collect_edges(image):
    graph = []
    weights = {}
    for i, row in enumerate(image):
        for j, a in enumerate(row):
            if i > 0:               #check color above
                key = str(a)+" "+str(image[i-1][j])
                weights = add_to_graph(key, weights)

            if i < len(image)-1:    #check color below
                key = str(a)+" "+str(image[i+1][j])
                weights = add_to_graph(key, weights)
            
            if j > 0:               #check color left
                key = str(a)+" "+str(image[i][j-1])
                weights = add_to_graph(key, weights)
            
            if j < len(row) -1:     #check color right
                key = str(a)+" "+str(image[i][j+1])
                weights = add_to_graph(key, weights)
    for k in weights.keys():
        a, b = k.split(" ")
        graph.append((int(a), int(b), weights[k]))
    return graph
        



inp = [[0, 1, 2, 3], [1, 1, 0, 3], [0, 1, 3, 3], [2, 2, 2, 3]]

graph = collect_edges(inp)

new_chain = chain(graph, len(inp))
new_chain.print()