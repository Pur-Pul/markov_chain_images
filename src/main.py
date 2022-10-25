import os
import re
from PIL import Image
from services import Chain
from entities import Trie

class Main():
    """This is the main class that runs the program.
    """
    def __init__(self):
        """Initializes som variables used in the reading writing of the image files
        and training of the markov chain.
        """
        self.direction_map = [   
                                [0, 1, 2],
                                [3, None, 4],
                                [5, 6, 7]
                            ]
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.directory = "input"
        self.edges=[]
        self.rgb_dict = {}
        self.rgb_list = []
        self.neighbour_n = None
        self.compression = None
        self.use_trie = None
        self.trie = None
    
    def inp(self, prompt, regex):
        i = input(prompt)
        while not re.fullmatch(regex, i):
            print("Invalid input.")
            i = input(prompt)
        return i
        
    def run(self):
        """Collects inputs and calls the markovchain.
        Lastly it shows the generated image.
        """
        picture_number = int(self.inp("Number of input pictures: ", r"^[1-9]+\d*$"))
        self.neighbour_n = int(self.inp("Number of neighbours (8/4): ", r"^8|4$"))
        self.use_trie = (self.inp("Use trie? (Y/N): ", r"^[Yy]|[Nn]$").lower() == "y")
        if self.use_trie:
            self.trie = Trie()
        
        print("\nPictures found: ")
        files = "^"
        for file in os.listdir(self.directory):
            print(file)
            files+=re.escape(file)+"|"
        files = files[:-1]+"$"
        print(files)
        for _ in range(picture_number):
            picture_name = self.inp("Enter picture name: ", files)
            self.compression = int(self.inp("Color compression value (50 recomended): ", r"^[1-9]+\d*$"))
            if self.use_trie:
                self.train_trie(self.read_image(picture_name))
            else:
                self.edges = self.collect_edges(self.read_image(picture_name), self.edges)

        print("Color diversity: " + str(len(self.rgb_list)))

        image_width = int(self.inp("Enter width of new image: ", r"^[2-9]|[1-9]\d+$"))
        image_height = int(self.inp("Enter height of new image: ", r"^[2-9]|[1-9]\d+$"))
        
        new_chain = Chain(self.edges, len(self.rgb_list), self.direction_map, self.neighbour_n, self.trie)

        print()
        table = new_chain.generate_image((image_width, image_height))
        new_im = Image.new("RGB", (image_width, image_height))
        for x in range(0, len(table)):
            for y in range(0, len(table[x])):
                new_im.putpixel((y,x), self.rgb_list[table[x][y]])
        new_im.show()

    def add_to_graph(self, key, weights):
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

    def collect_edges(self, image, graph):
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
                    directions.append((i-1,j,self.direction_map[0][1]))

                if i < len(image)-1:    #check color below
                    directions.append((i+1,j,self.direction_map[2][1]))

                if j > 0:               #check color left
                    directions.append((i,j-1,self.direction_map[1][0]))

                if j < len(row) -1:     #check color right
                    directions.append((i,j+1,self.direction_map[1][2]))
                if self.neighbour_n == 8:
                    if i > 0 and j > 0:     #check color top left
                        directions.append((i-1,j-1,self.direction_map[0][0]))
                    
                    if i > 0 and j < len(row) -1: #check color top right
                        directions.append((i-1,j+1,self.direction_map[0][2]))
                    
                    if i < len(image) -1 and j > 0: #check color bottom left
                        directions.append((i+1,j-1,self.direction_map[2][0])) 
                    
                    if i < len(image) -1 and j < len(row) -1: #check color bottom right
                        directions.append((i+1,j+1,self.direction_map[2][2]))

                for direction in directions:
                    key = str(color_a) + " " + str(image[direction[0]][direction[1]]) + " " + str(direction[2])
                    #print(key)
                    weights = self.add_to_graph(key, weights)

        for k in weights.keys():
            color_a, color_b, dir = k.split(" ")
            graph.append((int(color_a), int(color_b), int(dir), weights[k]))
        return graph

    def train_trie(self, image):
        for i, row in enumerate(image):
            for j, color_a in enumerate(row):
                if i > 0:               #check color above
                    self.trie.add_edge(color_a, image[i-1][j], self.direction_map[0][1])

                if i < len(image)-1:    #check color below
                    self.trie.add_edge(color_a, image[i+1][j], self.direction_map[2][1])

                if j > 0:               #check color left
                    self.trie.add_edge(color_a, image[i][j-1], self.direction_map[1][0])

                if j < len(row) -1:     #check color right
                    self.trie.add_edge(color_a, image[i][j+1], self.direction_map[1][2])
                
                if self.neighbour_n == 8:
                    if i > 0 and j > 0:     #check color top left
                        self.trie.add_edge(color_a, image[i-1][j-1], self.direction_map[0][0])
                    
                    if i > 0 and j < len(row) -1: #check color top right
                        self.trie.add_edge(color_a, image[i-1][j+1], self.direction_map[0][2])
                    
                    if i < len(image) -1 and j > 0: #check color bottom left
                        self.trie.add_edge(color_a, image[i+1][j-1], self.direction_map[2][0])
                    
                    if i < len(image) -1 and j < len(row) -1: #check color bottom right
                        self.trie.add_edge(color_a, image[i+1][j+1], self.direction_map[2][2])

    def read_image(self, file_name):
        """Reads an image from the input directory and returns a 2D table containing RGB values.

        Args:
            file_name String: The name of the file to be read.

        Returns:
            inp: A 2d table conntaing color information about each pixel.
            The color values have been compressed to improve the runtime.
        """
        print(os.path)
        im = Image.open(os.path.join(self.directory, file_name)).convert('RGB')
        inp = [None]*im.size[1]
        for x in range(0,im.size[1]):
            inp[x] = [None]*im.size[0]
            for y in range(0,im.size[0]):
                temp = im.getpixel((y,x))
                rgb_val = (self.compression * round(temp[0]/self.compression), self.compression * round(temp[1]/self.compression), self.compression * round(temp[2]/self.compression))
                if rgb_val not in self.rgb_dict:
                    self.rgb_list.append(rgb_val)
                    self.rgb_dict[rgb_val] = len(self.rgb_list)-1

                inp[x][y] = self.rgb_dict[rgb_val]
        return inp

if __name__ == '__main__':
    new = Main()
    new.run()
