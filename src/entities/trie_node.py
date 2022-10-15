class TrieNode:
    def __init__(self, color):
        self.next = [{},{},{},{},{},{},{},{}]
        self.color = color
    def add_node(self, node, dir):
        if node not in self.next:
            self.next[dir][node] = 1
        else:
            self.next[dir][node] += 1
    def color_frequency_list(self, dir):
        frequency_list = [[-1],[0]]
        for node in self.next[dir].items():
            frequency_list[0].append(node[0].color)
            frequency_list[1].append(node[1])
        return frequency_list
