class CFGNode:
    def __init__(self, label, info=None, adjacent=None):
        self.info = []
        self.adjacent = []
        self.label = label
        if info and len(info) > 0:
            self.info = info
        if adjacent and len(adjacent) > 0:
            self.adjacent = adjacent

    def add_adjacent(self, node):
        if node not in self.adjacent:
            self.adjacent.append(node)

    def print_info(self):
        for info in self.info:
            print(info)

    def get_label(self):
        return self.label

    def get_info(self):
        return self.info

    def get_adjacent(self):
        return self.adjacent

    def traverse(self, is_visited, graph):
        is_visited[self.label] = True
        if self not in graph:
            graph[self] = self.adjacent
        for adj in self.adjacent:
            if not is_visited[adj.get_label()]:
                adj.traverse(is_visited, graph)


if __name__ == "__main__":
    a = CFGNode(label='1')
    b = CFGNode(label='2')
    a.add_adjacent(b)
    print(a.get_adjacent())
