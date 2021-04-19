from src.backend.parser.notal_parser import NotalParser


def read_src(file_path):
    with open(file_path, encoding='utf-8') as f:
        src_input = f.read()
    return src_input


def get_ast(file_path):
    parser = NotalParser()
    parse_result = parser.parse(read_src(file_path))
    return parse_result.get_ast_in_json()
