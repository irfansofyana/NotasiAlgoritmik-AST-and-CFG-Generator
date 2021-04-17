from graphviz import Digraph
from notal_parser import NotalParser
import json

# dot = Digraph(comment='The Round Table')
# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')
#
# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')
#
# dot.render('test-output/round-table.gv', format='png')


def read_src(file_path):
    with open(file_path, encoding='utf-8') as f:
        src_input = f.read()
    return src_input


def get_ast(file_path):
    parser = NotalParser()
    parse_result = parser.parse(read_src(file_path))
    return parse_result.get_ast_in_json()


def visualize_ast(ast, output_path='test-output/result.gv'):
    graph = Digraph(comment="AST result")
    traverse_ast(ast, graph)
    graph.render(output_path, format='png', view=True)


def get_node_label(node):
    label = node['type']
    infos = node['info']
    if infos is not None:
        for info in infos:
            label = label + "\n" + str(info) + ": " + str(infos[info])
    return label


node_counter = 0


def traverse_ast(ast, graph, parent_counter=None):
    global node_counter
    node_counter += 1
    node_label = get_node_label(ast)
    now_counter = node_counter

    graph.node(str(now_counter), node_label)
    if parent_counter is not None:
        graph.edge(str(parent_counter), str(now_counter))

    if 'children' not in ast:
        return

    for i, child in enumerate(ast['children']):
        traverse_ast(child, graph, now_counter)


if __name__ == "__main__":
    file_path = 'input/4.in'
    ast = get_ast(file_path)
    visualize_ast(ast)
