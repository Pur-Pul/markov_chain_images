class TrieNode:
    def __init__(self, color):
        self.next = [{},{},{},{},{},{},{},{}]
        self.color = color
    def add_node(self, node, direction):
        if node not in self.next[direction]:
            self.next[direction][node] = 1
        else:
            self.next[direction][node] += 1
    def color_frequency_list(self, direction):
        frequency_list = [[-1],[0]]
        for node in self.next[direction].items():
            frequency_list[0].append(node[0].color)
            frequency_list[1].append(node[1])
        return frequency_list
