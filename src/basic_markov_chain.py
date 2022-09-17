import random



class Node:
    def __init__(self, value):
        """This the class for the nodes used in the queue.

        Args:
            value (_type_): The value of the node.
            next (_type_): Points to the next node in the queue.
        """
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        """This is the class for the queue used in BFS.
        Args:
            f_node Node: Points to the first node in the queue.
            size int: Keeps track of the length of the queue.
            end Node: Points to the last node in the queue
        """
        self.f_node = None
        self.size = 0
        self.end = None
    def add(self, value):
        """Assign the value to a new node and adds it to the end of the queue

        Args:
            value (_type_): The value of the node.
        """
        if self.f_node == None:
            self.f_node = Node(value)
            self.end = self.f_node
        else:
            self.end.next = Node(value)
            self.end = self.end.next
        self.size += 1
    def pop(self):
        """Pops the first node from the queue and returns its value.

        Returns:
            value: The value of the popped node.
        """
        to_return = self.f_node.value
        self.f_node = self.f_node.next
        self.size -= 1
        return to_return

class Chain:
    def __init__(self, edges, n):
        """This is the class for the markov chain.

        Args:
            edges (_type_): A list of tuples, that contain edges and their weight.
            The weights are the frequency of the edges.
            n int: The number of rows in the image and the max number colors allowed in the image. 
            This will be changed later, so that more colors can be used in each image.
        """
        self.n = n
        self.adj = [None] * n
        self.lengths = [0] * n
        for i in range(n):
            self.adj[i] = [0] *n
            #print(i)
        
        for (a, b, w) in edges:
            self.adj[a][b] = w
            self.lengths[a] += w
        
        self.calculate_possibities()

    def calculate_possibities(self):
        """Redefines the weights of the edges to a percentage instead of frequency.
        """
        for a in range(self.n):
            for b in range(self.n):
                if self.lengths[a] == 0:
                    continue
                self.adj[a][b] /= self.lengths[a]

    def get_neighbors(self, pos):
        """Checks neighbors of the given position and returns their coordinates.

        Args:
            pos tuple: The coordinates for the position to check.

        Returns:
            list: A list of the neighbors coordinates.
        """
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
        """This function decides the color to be assigned to the current position based on the colors of the neighbors.

        Args:
            neighbors list: A list of the neighbors coordinates.
            image list: A 2d table representing the image to be generated.

        Returns:
            int: A color value.
        """
        possibilities = {}
        counter = {}
        count = 0
        #print(neighbors)
        for neighbor in neighbors:
            a = image[neighbor[0]][neighbor[1]]
            #print(a)
            if a == -1:
                continue
            
            count+=1
            for b in range(self.n):
                if (b not in counter):
                    counter[b] = 1
                else:
                    counter[b] += 1
                if (b not in possibilities):
                    possibilities[b] = self.adj[a][b]
                else:
                    possibilities[b] *= (self.adj[a][b]*counter[b])
        
    
        
        values = []
        probs = ()
        if len(possibilities) == 0:
            rand_val = random.randint(0,self.n-1)
        else:
            for a in possibilities.keys():
                values.append(a)
                probs+=(int(possibilities[a]*100) ,)
            
            rand_val = random.choices(values, weights=probs, k=1)[0]
            #print(rand_val)
        
        return rand_val

    def generate_image(self):
        """This is the main function for generating an image based on the chain.
        It uses BFS to traverse the image to be generated. The starting position is randomly picked.
        """
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
        """This function prints the image to the console.

        Args:
            image list: A 2d table representing the image to be printed.
        """
        for _, row in enumerate(image):
            for _, a in enumerate(row):
                print(a, end=", ")
            print()

    def print(self):
        for a in range(self.n):
            for b in range(self.n):
                w = self.adj[a][b]
                print("(" + str(a) + "," + str(b) + ")" + " : " + str(w))



def add_to_graph(key, weights):
    """This function makes sure each edge appears only once, and instead increments the weights if they appear multiple times.

    Args:
        key (_type_): The unique key for the current edge, to be used in a dictionary.
        weights (_type_): A dictionary containing the weights of each edge.

    Returns:
        _type_: _description_
    """
    if key in weights:
        weights[key] += 1
    else: 
        weights[key] = 1
    return weights

def collect_edges(image):
    """Collects the edges to be entered into the markov chain.

    Args:
        image list: A 2d table that represent the image to be analyzed.
    Returns:
        _type_: A list of edges.
    """
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

new_chain = Chain(graph, len(inp))
new_chain.print()
print()
new_chain.generate_image()