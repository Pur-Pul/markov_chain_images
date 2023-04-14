import os
import re
import time
from PIL import Image
from services import Chain
from entities import Trie

class Main():
    """This is the main class that runs the program.
    """
    def __init__(self):
        """Initializes som variables used in the reading writing of the image files
        and training of the markov chain.

            Variables:
                direction_map : A 3x3 table containing indices for each direction from the center.
                directory : A string containing the name of the folder to search for input images.
                edges : A list of tuples containing data for the markov chain.
                    This is only used when not using the trie.
                rgb_dict : Maps the colors from the input images to integer values.
                rgb_list : A list containg all unique color indices.
                neighbour_n : An integer either 8 or 4,
                    which defines how many neighbour nodes to take into account in the markov chain.
                compression : An integer value that is used to round the color values to.
                    Larger compression value, less unique colors. 1 means no compression.
                trie : This variable stores the trie object.

        """
        self.direction_map = [
                                [0, 1, 2],
                                [3, None, 4],
                                [5, 6, 7]
                            ]

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.directory = "static"
        self.edges=[]
        self.rgb_dict = {}
        self.rgb_list = []
        self.neighbour_n = None
        self.compression = None
        self.trie = None

    def inp(self, prompt, regex):
        """This function uses regular expression to filter the input.

        Args:
            prompt (string): This is the string to prompt the user for the input.
            regex (raw string): This string is the regular expression,
                which is used to check whether the input is allowed.

        Returns:
            string: A string which was appreoved by the reular expression.
        """
        i = input(prompt)
        while not re.fullmatch(regex, i):
            print("Invalid input.")
            i = input(prompt)
        return i

    def run(self):
        """
        Collects inputs and calls the markovchain.
        If use trie was set to True, a Trie will be used to train the markov chain.
        Lastly it shows the generated image.
        """
        self.neighbour_n = int(self.inp("Number of neighbours (8/4): ", r"^8|4$"))
        if self.inp("Use trie? (Y/N): ", r"^[Yy]|[Nn]$").lower() == "y":
            self.trie = Trie()

        print("\nPictures found: ")
        files = "^"
        for file in os.listdir(self.directory):
            print(file)
            files+=re.escape(file)+"|"
        files = files[:-1]+"$"
        training_time = self.read_images(files)
        start_time = time.time()
        new_chain = Chain(
            self.edges,
            len(self.rgb_list),
            self.direction_map,
            self.neighbour_n,
            self.trie
        )
        print(
            "Markov chain trained in " +
            str(training_time + (time.time()-start_time))+
            " seconds."
        )

        image_width, image_height = (
            int(self.inp("Enter width of new image: ", r"^[2-9]|[1-9]\d+$")),
            int(self.inp("Enter height of new image: ", r"^[2-9]|[1-9]\d+$"))
        )

        start_time = time.time()
        table = new_chain.generate_image((image_width, image_height))
        print("Image generated in " + str(time.time()-start_time)+" seconds.")
        self.generate_image(table, image_width, image_height)

    def generate_image(self, table, image_width, image_height):
        new_im = Image.new("RGB", (image_width, image_height))
        for i, row in enumerate(table):
            for j, col in enumerate(row):
                new_im.putpixel((j,i), self.rgb_list[col])
        new_im.show()

    def add_to_graph(self, color_a, color_b, direction, weights):
        """This function makes sure each edge appears only once,
        and instead increments the weights if they appear multiple times.

        Args:
            key (_type_): The unique key for the current edge, to be used in a dictionary.
            weights (_type_): A dictionary containing the weights of each edge.

        Returns:
            _type_: _description_
        """
        key = (
            str(color_a)+
            " "+
            str(color_b)+
            " "+
            str(direction)
        )
        if weights is None:
            weights = {}
        if key in weights:
            weights[key] += 1
        else:
            weights[key] = 1
        return weights

    def collect_edges(self, image, graph, weights = None):
        """Collects the edges to be entered into the markov chain.

        Args:
            image (list): A 2d table that represent the image to be analyzed.
            graph (list): A list of tuples containing the data for the markov chain.
        Returns:
            graph (list): A list of tuples containing the data for the markov chain.
        """
        for i, row in enumerate(image):
            for j, color_a in enumerate(row):
                if i > 0:               #check color above
                    weights = self.add_to_graph(
                        color_a,
                        image[i-1][j],
                        self.direction_map[0][1],
                        weights
                    )

                if i < len(image)-1:    #check color below
                    weights = self.add_to_graph(
                        color_a,
                        image[i+1][j],
                        self.direction_map[2][1],
                        weights
                    )

                if j > 0:               #check color left
                    weights = self.add_to_graph(
                        color_a,
                        row[j-1],
                        self.direction_map[1][0],
                        weights
                    )

                if j < len(row) -1:     #check color right
                    weights = self.add_to_graph(
                        color_a,
                        row[j+1],
                        self.direction_map[1][2],
                        weights
                    )

                if self.neighbour_n == 4:
                    continue

                if i > 0 and j > 0:     #check color top left
                    weights = self.add_to_graph(
                        color_a,
                        image[i-1][j-1],
                        self.direction_map[0][0],
                        weights
                    )

                if i > 0 and j < len(row) -1: #check color top right
                    weights = self.add_to_graph(
                        color_a,
                        image[i-1][j+1],
                        self.direction_map[0][2],
                        weights
                    )

                if i < len(image) -1 and j > 0: #check color bottom left
                    weights = self.add_to_graph(
                        color_a,
                        image[i+1][j-1],
                        self.direction_map[2][0],
                        weights
                    )

                if i < len(image) -1 and j < len(row) -1: #check color bottom right
                    weights = self.add_to_graph(
                        color_a,
                        image[i+1][j+1],
                        self.direction_map[2][2],
                        weights
                    )

        for k in weights.keys():
            color_a, color_b, direction = k.split(" ")
            graph.append((int(color_a), int(color_b), int(direction), weights[k]))
        return graph

    def train_trie(self, image):
        """This function trains the trie

        Args:
            image (_type_): _description_
        """
        for i, row in enumerate(image):
            for j, color_a in enumerate(row):
                if i > 0:               #check color above
                    self.trie.add_edge(color_a, image[i-1][j], self.direction_map[0][1])

                if i < len(image)-1:    #check color below
                    self.trie.add_edge(color_a, image[i+1][j], self.direction_map[2][1])

                if j > 0:               #check color left
                    self.trie.add_edge(color_a, row[j-1], self.direction_map[1][0])

                if j < len(row) -1:     #check color right
                    self.trie.add_edge(color_a, row[j+1], self.direction_map[1][2])

                if self.neighbour_n == 4:
                    continue

                if i > 0 and j > 0:     #check color top left
                    self.trie.add_edge(color_a, image[i-1][j-1], self.direction_map[0][0])

                if i > 0 and j < len(row) -1: #check color top right
                    self.trie.add_edge(color_a, image[i-1][j+1], self.direction_map[0][2])

                if i < len(image) -1 and j > 0: #check color bottom left
                    self.trie.add_edge(color_a, image[i+1][j-1], self.direction_map[2][0])

                if i < len(image) -1 and j < len(row) -1: #check color bottom right
                    self.trie.add_edge(color_a, image[i+1][j+1], self.direction_map[2][2])

    def read_images(self, files):
        """This function selects the images to read based on user input.
        It also initiates the training of the markov chain for each image.

        Args:
            files (list): A list containing the file names of the files in the input folder.

        Returns:
            time: The time it took to train the markov chain.
        """
        picture_number = int(self.inp("Number of input pictures: ", r"^[1-9]+\d*$"))
        total_time = 0
        for _ in range(picture_number):
            image = self.read_image(self.inp("Enter picture name: ", files))
            start_time = time.time()
            if self.trie is not None:
                self.train_trie(image)
            else:
                self.edges = self.collect_edges(image, self.edges)
            total_time+=time.time()-start_time
        return total_time

    def read_image(self, file_name):
        """Reads an image from the input directory and returns a 2D table containing RGB values.

        Args:
            file_name String: The name of the file to be read.

        Returns:
            inp: A 2d table conntaing color information about each pixel.
            The color values have been compressed to improve the runtime.
        """
        if self.trie is None:
            rec = "50"
        else:
            rec = "1"
        self.compression = int(self.inp(
                    "Color compression value ("+ rec +" recomended): ",
                    r"^[1-9]+\d*$")
                )
        start_time = time.time()
        image = Image.open(os.path.join(self.directory, file_name)).convert('RGB')
        inp = [None]*image.size[1]
        for i in range(0,image.size[1]):
            inp[i] = [None]*image.size[0]
            for j in range(0,image.size[0]):
                temp = image.getpixel((j,i))
                rgb_val = (
                    self.compression * round(temp[0]/self.compression),
                    self.compression * round(temp[1]/self.compression),
                    self.compression * round(temp[2]/self.compression)
                )
                if rgb_val not in self.rgb_dict:
                    self.rgb_list.append(rgb_val)
                    self.rgb_dict[rgb_val] = len(self.rgb_list)-1

                inp[i][j] = self.rgb_dict[rgb_val]
        print("Image file read in " + str(time.time()-start_time) + " seconds.")
        print("Color diversity: " + str(len(self.rgb_list)))
        return inp

if __name__ == '__main__':
    new = Main()
    new.run()
