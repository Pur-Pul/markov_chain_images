import random
from entities import Stack

class Chain:
    def __init__(self, graph, color_n, dir_map):
        """This is the class for the markov chain.

        Args:
            graph (_type_): A list of tuples, that contain edges and their weight.
            The weights are the frequency of the edges.
            color_n int: The number of colors to be used in the markov chain.
        """
        self.dir_map = dir_map
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
                dir = self.dir_map[neighbour[0]-pos[0]+1][neighbour[1]-pos[1]+1]
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