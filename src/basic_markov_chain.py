import random
import os
from PIL import Image

direction_map = [   [0, 1, 2],
                    [3, None, 4],
                    [5, 6, 7]
                ]

class Node:
    def __init__(self, value):
        """This the class for the nodes used in the Stack.

        Args:
            value (_type_): The value of the node.
            next (_type_): Points to the next node in the Stack.
        """
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        """This is the class for the Stack used in the depth-first traversal.
        """
        self.f_node = None
        self.size = 0
    def add(self, value):
        """This function adds a new Node to the top of the stack.

        Args:
            value: The value of the node added.
        """
        new_node = Node(value)
        if self.f_node is None:
            self.f_node = new_node
        else:
            new_node.next = self.f_node
            self.f_node = new_node
        self.size += 1
    def pop(self):
        """This function pops the top element from the stack.

        Returns:
            to_return: The value of the popped Node.
        """
        to_return = self.f_node.value
        self.f_node = self.f_node.next
        self.size -= 1
        return to_return

class Chain:
    def __init__(self, graph, color_n):
        """This is the class for the markov chain.

        Args:
            graph (_type_): A list of tuples, that contain edges and their weight.
            The weights are the frequency of the edges.
            color_n int: The number of colors to be used in the markov chain.
        """
        self.color_n = color_n
        self.adj = [None] * color_n
        self.lengths = [None] * color_n
        for i in range(color_n):
            self.lengths[i] = [0] * 8
            self.adj[i] = [None] * 8
            for dir in range(0, 8):
                self.adj[i][dir] = [0] * color_n

        for (color_a, color_b, dir, weight) in graph:
            self.adj[color_a][dir][color_b] = weight
            self.lengths[color_a][dir] += weight

        self.calculate_possibities()

    def calculate_possibities(self):
        """Redefines the weights of the edges to a percentage instead of frequency.
        """
        for color_a in range(self.color_n):
            for dir in range(0, 8):
                for color_b in range(self.color_n):
                    if self.lengths[color_a][dir] == 0:
                        self.adj[color_a][dir][color_b] = 0.0
                        continue
                    
                    self.adj[color_a][dir][color_b] /= self.lengths[color_a][dir]

    def get_neighbours(self, pos, image_size, eight_neighbours):
        """Checks neighbours of the given position and returns their coordinates.

        Args:
            pos tuple: The coordinates for the position to check.
            image_size: A tuple containg height and width of the image to be generated.
            eight_neighbours (Boolean): A boolean value that decides whether to only take the direct 4 neighbours into account
            or the surrounding 8.

        Returns:
            neighbours: A list containg coordinates for the neighbouring pixels to be processed.
            The list has been shuffled to avoid a clear directional pattern in the generated image.
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
        
        if(eight_neighbours):
            if row_i > 0 and col_i > 0:
                neighbours.append((row_i-1, col_i-1))
            if row_i > 0 and col_i < image_size[0]-1:
                neighbours.append((row_i-1, col_i+1))
            if row_i < image_size[1]-1 and col_i > 0:
                neighbours.append((row_i+1, col_i-1))
            if row_i < image_size[1]-1 and col_i < image_size[0]-1:
                neighbours.append((row_i+1, col_i+1))

        random.shuffle(neighbours)
        return neighbours

    def pick_color(self, color_a=None, dir=None):
        """This function decides the color for the next pixel based on the color of the current pixel
        and directional relation between the the two pixels.

        Args:
            color_a: The index of the color value of the current pixel.
            dir: The index of the direction of the next pixel from the current one.

        Returns:
            int: A color value that has been randomly selected based on the weights of a markov chain.
        """
        if color_a is None:
            return random.randint(0, self.color_n-1)

        colors = []
        possibilities = []
        largest=0
        for color_b, weight in enumerate(self.adj[color_a][dir]):
            largest = max(largest, weight)
            colors.append(color_b)
            possibilities.append(weight)
        
        if largest == 0:
            return -1

        rand_val = random.choices(colors, weights=possibilities, k=1)[0]
        return rand_val

    def generate_image(self, image_size, large_sample):
        """This is the main function for generating an image based on the chain.
        It uses DFS to traverse the image to be generated. The starting position is randomly picked.
        """
        image = [None] * image_size[1]
        for row in range(image_size[1]):
            image[row] = [-1]*image_size[0]

        start_pos = (random.randint(0, image_size[1]-1), random.randint(0, image_size[0]-1))
        #print(start_pos)
        image[start_pos[0]][start_pos[1]] = self.pick_color()

        stack = Stack()
        stack.add(start_pos)
        while stack.size>0:
            pos = stack.pop()
            neighbours = self.get_neighbours(pos, image_size, large_sample)
            for neighbour in neighbours:
                if image[neighbour[0]][neighbour[1]] != -1:
                    continue
                stack.add(neighbour)
                dir = direction_map[neighbour[0]-pos[0]+1][neighbour[1]-pos[1]+1]
                image[neighbour[0]][neighbour[1]] = self.pick_color(image[pos[0]][pos[1]], dir)

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
            for dir in range(0,8):
                for color_b in range(self.color_n):
                    weight = self.adj[color_a][dir][color_b]
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
            directions = []
            if i > 0:               #check color above
                directions.append((i-1,j,direction_map[0][1]))

            if i < len(image)-1:    #check color below
                directions.append((i+1,j,direction_map[2][1]))

            if j > 0:               #check color left
                directions.append((i,j-1,direction_map[1][0]))

            if j < len(row) -1:     #check color right
                directions.append((i,j+1,direction_map[1][2]))

            if i > 0 and j > 0:     #check color top left
                directions.append((i-1,j-1,direction_map[0][0]))
            
            if i > 0 and j < len(row) -1: #check color top right
                directions.append((i-1,j+1,direction_map[0][2]))
            
            if i < len(image) -1 and j > 0: #check color bottom left
                directions.append((i+1,j-1,direction_map[2][0])) 
            
            if i < len(image) -1 and j < len(row) -1: #check color bottom right
                directions.append((i+1,j+1,direction_map[2][2]))

            for direction in directions:
                key = str(color_a) + " " + str(image[direction[0]][direction[1]]) + " " + str(direction[2])
                #print(key)
                weights = add_to_graph(key, weights)

    for k in weights.keys():
        color_a, color_b, dir = k.split(" ")
        graph.append((int(color_a), int(color_b), int(dir), weights[k]))
    return graph

def read_image(file_name):
    """Reads an image from the input directory and returns a 2D table containing RGB values.

    Args:
        file_name String: The name of the file to bea read.

    Returns:
        inp: A 2d table conntaing color information about each pixel.
        The color values have been compressed to improve the runtime.
    """
    im = Image.open(os.path.join(directory, file_name)).convert('RGB')
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
    return inp

if __name__ == "__main__":
    directory = "src/input"
    edges=[]
    rgb_dict = {}
    rgb_list = []
    print("Number of input pictures: ", end="")
    picture_number = int(input())
    print()
    print("Pictures found: ")
    for file in os.listdir(directory):
        print(file)
    print()
    for i in range(picture_number):
        print("Enter picture name: ", end="")
        picture_name = input()
        edges = collect_edges(read_image(picture_name), edges)

    print("Color diversity: " + str(len(rgb_list)))

    print("Enter width of new image: ", end="")
    image_width = int(input())
    print("Enter height of new image: ", end="")
    image_height = int(input())
    print("Use 8 neighbours (Y/N): ", end="")
    if input().lower() == "y":
        eight = True
    else:
        eight = False
    
    new_chain = Chain(edges, len(rgb_list))

    print()
    table = new_chain.generate_image((image_width, image_height), eight)
    new_im = Image.new("RGB", (image_width, image_height))
    for x in range(0, len(table)):
        for y in range(0, len(table[x])):
            new_im.putpixel((y,x), rgb_list[table[x][y]])
    new_im.show()
