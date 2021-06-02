from graphviz import *
from src.backend.cfg_generator.ast_parser import *
import json


def visualize_ast(ast, output_path='rendered_ast.gv'):
    graph = convert_ast_to_graphviz(ast)
    graph.node_attr['fontname'] = 'consolas'
    graph.render(output_path, format='png', view=False)


def convert_ast_to_graphviz(ast):
    graph = Graph(comment="AST result")
    traverse_ast(ast, graph)
    return graph


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


def read_ast():
    with open('ast.json', encoding='utf-8') as f:
        ast = json.load(f)
    ast = ASTParser(ast_dict=ast)
    return ast


def get_ast_block(current_ast, target_type):
    if current_ast.get_type() == target_type:
        return current_ast
    if len(current_ast.get_children()) == 0:
        return None

    for child in current_ast.get_children():
        target_block = get_ast_block(child, target_type)
        if target_block is not None:
            return target_block


if __name__ == "__main__":
    ast = read_ast()
    user_input = input("What part of AST you want to render? ")
    desired_ast = get_ast_block(ast, user_input)
    visualize_ast(desired_ast.get_ast_in_json())
