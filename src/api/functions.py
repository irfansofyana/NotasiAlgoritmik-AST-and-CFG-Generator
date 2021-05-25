from src.backend.parser.notal_parser import NotalParser
from src.backend.cfg_generator.cfg_generator import *
from src.backend.cfg_generator.ast_parser import *


def read_src(file_path):
    with open(file_path, encoding='utf-8') as f:
        src_input = f.read()
    return src_input


def get_ast(file_path, src=None):
    try:
        parser = NotalParser()
        if file_path is not None:
            parse_result = parser.parse(read_src(file_path))
        else:
            parse_result = parser.parse(src)
        return parse_result.get_ast_in_json()
    except Exception as err:
        raise err


def get_algorithm_block(current_ast):
    if current_ast.get_type() == 'algorithm_block':
        return current_ast
    if len(current_ast.get_children()) == 0:
        return None

    for child in current_ast.get_children():
        algo_block = get_algorithm_block(child)
        if algo_block is not None:
            return algo_block


def get_cfg(file_path):
    try:
        ast = get_ast(file_path)
        return get_cfg_from_ast(ast)
    except Exception as err:
        raise err


def get_cfg_from_ast(ast_in_json):
    ast_parser = ASTParser(ast_dict=ast_in_json)
    algorithm_block = get_algorithm_block(ast_parser)

    try:
        CFGGenerator.label = 0
        cfg_builder = CFGGenerator(algorithm_block)
        generated_cfg = cfg_builder.get_cfg()

        generated_graph = generated_cfg.get_graph(CFGGenerator.label + 1)
        return generated_graph
    except Exception as err:
        raise err


def write_graph(graph):
    for node in graph:
        print('Node ', node.get_label(), node.get_info())
        print('\tadjacent nodes:')
        for i, adj_node in enumerate(node.get_adjacent()):
            print(f'\t\tlabel_node: ', adj_node.get_label())


if __name__ == "__main__":
    ast = get_ast('../backend/parser/input/6.in')
    graph = get_cfg_from_ast(ast)
    write_graph(graph)
