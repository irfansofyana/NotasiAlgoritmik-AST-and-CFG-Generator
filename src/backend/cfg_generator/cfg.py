class CFG:
    def __init__(self, entry_block, exit_block):
        # entry_block -> CFGNode, exit_block -> [CFGNode], entry_block -> exit_block must be connected
        self.entry_block = entry_block
        self.exit_block = exit_block

        self.connect_entry_and_exit_block()

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

    def connect_entry_and_exit_block(self):
        for exit_block in self.exit_block:
            if self.entry_block.get_label() != exit_block.get_label():
                self.entry_block.add_adjacent(exit_block)

    def get_graph(self, num_node):
        is_visited = [False for i in range(0, num_node + 1)]
        graph = {}
        self.entry_block.traverse(is_visited, graph)
        return graph
