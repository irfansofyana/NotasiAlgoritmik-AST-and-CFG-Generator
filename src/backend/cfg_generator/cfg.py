from src.backend.cfg_generator.cfg_node import *


class CFG:
    def __init__(self, entry_block, exit_block):
        # entry_block -> CFGNode, exit_block -> [CFGNode], entry_block -> exit_block must be connected
        self.entry_block = entry_block
        self.exit_block = exit_block

    def get_entry_block(self):
        return self.entry_block

    def get_exit_block(self):
        return self.exit_block

    def add_exit_block(self, node):
        self.exit_block.append(node)

    def merge_cfg(self, cfg):
        entry_block_next_cfg = cfg.get_entry_block()
        for exit_block in self.exit_block:
            exit_block.add_adjacent(entry_block_next_cfg)
        self.exit_block = cfg.get_exit_block()

    def get_graph(self, num_node):
        is_visited = [False for i in range(0, num_node + 3)]
        graph = {}
        self.entry_block.traverse(is_visited, graph)

        start_node = CFGNode(label=num_node, info=['start: main'])
        end_node = CFGNode(label=num_node+1, info=['end: main'])

        graph[start_node] = [self.entry_block]
        graph[end_node] = []
        for exit_node in self.exit_block:
            graph[exit_node].append(end_node)

        return graph
