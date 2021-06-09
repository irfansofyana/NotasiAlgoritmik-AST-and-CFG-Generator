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


def get_ast_block(current_ast, target_type):
    if current_ast.get_type() == target_type:
        return current_ast
    if len(current_ast.get_children()) == 0:
        return None

    for child in current_ast.get_children():
        target_block = get_ast_block(child, target_type)
        if target_block is not None:
            return target_block


def get_cfg(file_path):
    try:
        ast = get_ast(file_path)
        return get_cfg_from_ast(ast)
    except Exception as err:
        raise err


def get_cfg_from_ast(ast_in_json):
    ast_parser = ASTParser(ast_dict=ast_in_json)
    main_program_ast = get_ast_block(ast_parser, 'algorithm_block')
    subprogram_implementation_block_ast = get_ast_block(ast_parser, "procedure_and_function_implementation_block")
    if subprogram_implementation_block_ast is not None:
        subprograms_ast = get_ast_of_the_subprograms(subprogram_implementation_block_ast)
    else:
        subprograms_ast = None

    try:
        CFGGenerator.label = 0
        CFGGenerator.subprograms_ast = subprograms_ast
        CFGGenerator.visited_subprograms_ast = {}

        cfg_builder = CFGGenerator(main_program_ast)
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


def get_ast_of_the_subprograms(procedure_and_function_implementation_block_ast):
    collected_ast = {'function': {}, 'procedure': {}}
    for child in procedure_and_function_implementation_block_ast.get_children():
        subprogram_name, ast_subprogram = get_ast_info(child)
        subprogram_type = 'function' if child.get_type() == 'function_implementation' else 'procedure'
        collected_ast[subprogram_type][subprogram_name] = ast_subprogram

    print(collected_ast)
    return collected_ast


def get_ast_info(subprogram_ast):
    subprogram_declaration = subprogram_ast.get_children()[0]
    subprogram_name = subprogram_declaration.get_children()[0].get_notal_src()
    subprogram_implementation = subprogram_ast.get_children()[1]
    collected_ast = (
            subprogram_declaration.get_notal_src(),
            get_ast_block(subprogram_implementation, 'algorithm_block')
    )
    return subprogram_name, collected_ast
