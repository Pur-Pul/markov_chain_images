import random
import os
from PIL import Image

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
        new_node = Node(value)
        if self.f_node is None:
            self.f_node = self.end = new_node
        else:
            self.end.next = new_node
            self.end = new_node
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

class Stack:
    def __init__(self):
        self.f_node = None
        self.size = 0
    def add(self, value):
        new_node = Node(value)
        if self.f_node is None:
            self.f_node = new_node
        else:
            new_node.next = self.f_node
            self.f_node = new_node
        self.size += 1
    def pop(self):
        to_return = self.f_node.value
        self.f_node = self.f_node.next
        self.size -= 1
        return to_return

class Chain:
    def __init__(self, graph, color_n):
        """This is the class for the markov chain.

        Args:
            edges (_type_): A list of tuples, that contain edges and their weight.
            The weights are the frequency of the edges.
            n int: The number of rows in the image and the max number colors allowed in the image.
            This will be changed later, so that more colors can be used in each image.
        """
        self.color_n = color_n
        self.adj = [None] * color_n
        self.lengths = [0] * color_n
        for i in range(color_n):
            self.adj[i] = [0] * color_n
            #print(i)

        for (color_a, color_b, weight) in graph:
            self.adj[color_a][color_b] = weight
            self.lengths[color_a] += weight

        self.calculate_possibities()

    def calculate_possibities(self):
        """Redefines the weights of the edges to a percentage instead of frequency.
        """
        for color_a in range(self.color_n):
            for color_b in range(self.color_n):
                if self.lengths[color_a] == 0:
                    continue
                self.adj[color_a][color_b] /= self.lengths[color_a]

    def get_neighbours(self, pos, image_size):
        """Checks neighbours of the given position and returns their coordinates.

        Args:
            pos tuple: The coordinates for the position to check.

        Returns:
            list: A list of the neighbours coordinates.
        """
        row_i, col_i = pos
        neighbours = []
        if row_i > 0:
            neighbours.append((row_i-1, col_i))
        if row_i < image_size[1]-1:
            neighbours.append((row_i+1, col_i))
        if col_i > 0:
            neighbours.append((row_i, col_i-1))
        if col_i < image_size[0]-1:
            neighbours.append((row_i, col_i+1))
        random.shuffle(neighbours)
        return neighbours

    def pick_color(self, color_a=None):
        """This function decides the color to be assigned to the current position,
        based on the colors of the neighbours.

        Args:
            neighbours list: A list of the neighbours coordinates.
            image list: A 2d table representing the image to be generated.

        Returns:
            int: A color value.
        """
        if color_a is None:
            return random.randint(0, self.color_n-1)

        colors = []
        possibilities = []
        for color_b, weight in enumerate(self.adj[color_a]):
            colors.append(color_b)
            possibilities.append(weight)

        rand_val = random.choices(colors, weights=possibilities, k=1)[0]
        return rand_val

    def generate_image(self, image_size):
        """This is the main function for generating an image based on the chain.
        It uses BFS to traverse the image to be generated. The starting position is randomly picked.
        """
        image = [None] * image_size[1]
        for row in range(image_size[1]):
            image[row] = [-1]*image_size[0]

        start_pos = (random.randint(0, image_size[0]-1), random.randint(0, image_size[1]-1))
        #print(start_pos)
        image[start_pos[0]][start_pos[1]] = self.pick_color()

        stack = Stack()
        stack.add(start_pos)
        while stack.size>0:
            pos = stack.pop()
            neighbours = self.get_neighbours(pos, image_size)
            for neighbour in neighbours:
                if image[neighbour[0]][neighbour[1]] != -1:
                    continue
                stack.add(neighbour)
                image[neighbour[0]][neighbour[1]] = self.pick_color(image[pos[0]][pos[1]])

        return image

    def print_image(self, image):
        """This function prints the image to the console.

        Args:
            image list: A 2d table representing the image to be printed.
        """
        for _, row in enumerate(image):
            for _, color in enumerate(row):
                print(color, end=", ")
            print()

    def print(self):
        for color_a in range(self.color_n):
            for color_b in range(self.color_n):
                weight = self.adj[color_a][color_b]
                print("(" + str(color_a) + "," + str(color_b) + ")" + " : " + str(weight))



def add_to_graph(key, weights):
    """This function makes sure each edge appears only once,
    and instead increments the weights if they appear multiple times.

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

def collect_edges(image, graph):
    """Collects the edges to be entered into the markov chain.

    Args:
        image list: A 2d table that represent the image to be analyzed.
    Returns:
        _type_: A list of edges.
    """
    weights = {}
    for i, row in enumerate(image):
        for j, color_a in enumerate(row):
            if i > 0:               #check color above
                key = str(color_a)+" "+str(image[i-1][j])
                weights = add_to_graph(key, weights)

            if i < len(image)-1:    #check color below
                key = str(color_a)+" "+str(image[i+1][j])
                weights = add_to_graph(key, weights)

            if j > 0:               #check color left
                key = str(color_a)+" "+str(row[j-1])
                weights = add_to_graph(key, weights)

            if j < len(row) -1:     #check color right
                key = str(color_a)+" "+str(row[j+1])
                weights = add_to_graph(key, weights)
    for k in weights.keys():
        color_a, color_b = k.split(" ")
        graph.append((int(color_a), int(color_b), weights[k]))
    return graph


if __name__ == "__main__":
    directory = "src/input"
    edges=[]
    rgb_dict = {}
    rgb_list = []
    print("Number of pictures: ", end="")
    m_pictures = int(input())
    print()
    for file in os.listdir(directory):
        if m_pictures == 0:
            break
        m_pictures-=1
        im = Image.open(os.path.join(directory, file)).convert('RGB')
        inp = [None]*im.size[1]

        for x in range(0,im.size[1]):
            inp[x] = [None]*im.size[0]
            for y in range(0,im.size[0]):
                temp = im.getpixel((y,x))
                rgb_val = (50 * round(temp[0]/50), 50 * round(temp[1]/50), 50 * round(temp[2]/50))
                if rgb_val not in rgb_dict:
                    rgb_list.append(rgb_val)
                    rgb_dict[rgb_val] = len(rgb_list)-1

                inp[x][y] = rgb_dict[rgb_val]

        edges = collect_edges(inp, edges)

    print("Color diversity: " + str(len(rgb_list)))
    new_chain = Chain(edges, len(rgb_list))
    #new_chain.print()
    print()
    table = new_chain.generate_image(im.size)
    new_im = Image.new("RGB", im.size)
    for x in range(0, len(table)):
        for y in range(0, len(table[x])):
            new_im.putpixel((y,x), rgb_list[table[x][y]])
    new_im.show()
