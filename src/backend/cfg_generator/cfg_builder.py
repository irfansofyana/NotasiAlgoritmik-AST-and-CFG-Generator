from src.backend.cfg_generator.parse_ast import *
from src.backend.cfg_generator.cfg_node import *
from src.backend.cfg_generator.cfg import *

label = 0


class CFGBuilder:
    def __init__(self, ast):
        # ast -> ASTParser, cfg -> CFG
        self.state = ast
        self.cfg = None

        self.build_cfg()

    def get_cfg(self):
        return self.cfg

    def build_cfg(self):
        f = getattr(self, 'on_' + self.state.get_type())
        return f()

    def on_algorithm_block(self):
        children = self.state.get_children()
        child_builder = CFGBuilder(children[0])
        self.cfg = child_builder.get_cfg()

    def on_compound_statement(self):
        children = self.state.get_children()
        child_builder = CFGBuilder(children[0])
        self.cfg = child_builder.get_cfg()

    def on_statement_sequence(self):
        statements = self.state.get_children()
        for i in range(0, len(statements)):
            child = CFGBuilder(statements[i])
            if i == 0:
                self.cfg = child.get_cfg()
            else:
                self.cfg.merge_cfg(child.get_cfg())

    @staticmethod
    def get_label_now():
        global label
        label += 1
        return label

    def on_assignment_statement(self):
        node_label = self.get_label_now()
        info = [self.state.get_notal_code()]
        node = CFGNode(node_label, info)
        self.cfg = CFG(node, [node])

    def on_procedure_statement(self):
        node_label = self.get_label_now()
        info = [self.state.get_notal_code()]
        # TODO: Connect it to the implementation of the procedure itself
        node = CFGNode(node_label, info)
        self.cfg = CFG(node, [node])

    def on_output_statement(self):
        node_label = self.get_label_now()
        info = [self.state.get_notal_code()]
        node = CFGNode(node_label, info)
        self.cfg = CFG(node, [node])

    def on_input_statement(self):
        node_label = self.get_label_now()
        info = [self.state.get_notal_code()]
        node = CFGNode(node_label, info)
        self.cfg = CFG(node, [node])

    @staticmethod
    def get_boolean_expression(parent_statement, ast):
        expression = ast.get_notal_code()
        boolean_expression = f'{parent_statement} {expression}'
        return boolean_expression

    def on_if_statement(self):
        children = self.state.get_children()
        if len(children) == 3:
            self.on_if_else_statement()
            return

        # conditional node
        node_label = self.get_label_now()
        info = [self.get_boolean_expression('if', children[0])]
        node = CFGNode(node_label, info)
        self.cfg = CFG(node, [node])

        # statement nodes
        child = CFGBuilder(children[1])
        cfg_child = child.get_cfg()

        # merge the cfg
        self.cfg.merge_cfg(cfg_child)
        self.cfg.add_exit_block(node)

    def on_if_else_statement(self):
        children = self.state.get_children()

        # conditional node
        node_label = self.get_label_now()
        info = [self.get_boolean_expression('if', children[0])]
        node = CFGNode(node_label, info)

        # first statement nodes
        first_child = CFGBuilder(children[1])
        first_cfg_child = first_child.get_cfg()

        # second statement nodes
        second_child = CFGBuilder(children[2])
        second_cfg_child = second_child.get_cfg()

        # connect conditional node to first statement
        node.add_adjacent(first_cfg_child.get_entry_block())
        node.add_adjacent(second_cfg_child.get_entry_block())

        # Build the CFG
        self.cfg = CFG(node, [*first_cfg_child.get_exit_block(), *second_cfg_child.get_exit_block()])

    def on_while_statement(self):
        children = self.state.get_children()

        # while conditional node
        node_label = self.get_label_now()
        info = [self.get_boolean_expression('while', children[0])]
        node = CFGNode(node_label, info)

        # statement nodes
        child = CFGBuilder(children[1])
        cfg_child = child.get_cfg()

        # connect while conditional node to the fg
        node.add_adjacent(cfg_child.get_entry_block())
        for exit_block in cfg_child.get_exit_block():
            exit_block.add_adjacent(node)

        # build the cfg
        self.cfg = CFG(node, [node])


def write_graph(graph):
    for node in graph:
        print('Node ', node.get_label(), node.get_info())
        print('\tadjacent nodes:')
        for i, adj_node in enumerate(node.get_adjacent()):
            print(f'\t\tlabel_node: ', adj_node.get_label())


if __name__ == "__main__":
    notal_dict = {}
    ast_parser = ASTParser(ast_dict=notal_dict)
    builder = CFGBuilder(ast_parser)
    cfg = builder.get_cfg()
    graph = cfg.get_graph(label)
    write_graph(graph)