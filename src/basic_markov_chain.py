import random



class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.f_node = None
        self.size = 0
        self.end = None
    def add(self, value):
        if self.f_node == None:
            self.f_node = Node(value)
            self.end = self.f_node
        else:
            self.end.next = Node(value)
            self.end = self.end.next
        self.size += 1
    def pop(self):
        to_return = self.f_node.value
        self.f_node = self.f_node.next
        self.size -= 1
        return to_return

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

    def get_neighbors(self, pos):
        row_i, col_i = pos
        neighbors = []
        if row_i > 0:
            neighbors.append((row_i-1, col_i))
        if row_i < self.n-1:
            neighbors.append((row_i+1, col_i))
        if col_i > 0:
            neighbors.append((row_i, col_i-1))
        if col_i < self.n-1:
            neighbors.append((row_i, col_i+1))
        return neighbors

    def pick_color(self, neighbors, image):
        possibilities = {}
        count = 0
        #print(neighbors)
        for neighbor in neighbors:
            a = image[neighbor[0]][neighbor[1]]
            #print(a)
            if a == -1:
                continue
            
            count+=1
            for possibility in self.adj[a]:
                if (possibility[0] not in possibilities):
                    possibilities[possibility[0]] = possibility[1]
                else:
                    possibilities[possibility[0]] * (possibility[1]*2)
        
        values = []
        probs = ()
        if len(possibilities) == 0:
            rand_val = random.randint(0,self.n-1)
        else:
            for a in possibilities.keys():
                values.append(a)
                probs+=(int(possibilities[a]*100),)
                
            rand_val = random.choices(values, weights=probs, k=count)[0]
        
        return rand_val

    def generate_image(self):
        image = [None] * self.n
        for r in range(self.n):
            image[r] = [-1]*self.n

        start_pos = (random.randint(0, self.n-1), random.randint(0, self.n-1))
        visited = {}
        queue = Queue()
                
        #BFS
        visited[start_pos] = True
        queue.add(start_pos)
        while(queue.size>0):
            #print("queue_size: " + str(queue.size))
            #print("pop()")
            pos = queue.pop()
            neighbors = self.get_neighbors(pos)
            image[pos[0]][pos[1]] = self.pick_color(neighbors, image)

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited[neighbor] = True
                    #print("add: " + str(neighbor))
                    queue.add(neighbor)
        self.print_image(image)

    def print_image(self, image):
        for i, row in enumerate(image):
            for j, a in enumerate(row):
                print(a, end=", ")
            print()

    def print(self):
        for a in range(self.n):
            for j in range(len(self.adj[a])):
                b, w = self.adj[a][j]
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
        



inp = [[0, 1, 0, 1], [2, 0, 2, 0], [0, 1, 0, 3], [2, 0, 2, 3]]

graph = collect_edges(inp)

new_chain = chain(graph, len(inp))
new_chain.print()
print()
new_chain.generate_image()