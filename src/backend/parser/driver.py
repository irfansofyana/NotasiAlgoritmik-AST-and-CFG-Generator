from notal_parser import NotalParser
from src.backend.parser.ast import AST
import json

if __name__ == "__main__":
    parser = NotalParser()

    input_directory_folder = 'input'
    input_file_name = 'dummy.in'
    with open(f'{input_directory_folder}/{input_file_name}', encoding='utf-8') as f:
        src_input = f.read()

        parsing_result = parser.parse(src_input)
        print(json.dumps(parsing_result.get_ast_in_json(), indent=2))
