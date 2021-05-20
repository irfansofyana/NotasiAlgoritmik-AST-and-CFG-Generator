import unittest
import os
import json
import re
from src.backend.parser.notal_parser import NotalParser


class Integration(unittest.TestCase):
    @staticmethod
    def read_input(file_name):
        with open(file_name, encoding='utf-8') as f:
            input_src = f.read()
        return input_src

    @staticmethod
    def read_expected_output(file_name):
        with open(file_name, encoding='utf-8') as f:
            expected_tokens = json.load(f)
        return expected_tokens

    def test_ast(self):
        input_folder_dir = "input"
        output_folder_dir = "output"

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            parser = NotalParser()

            # Read generated AST
            input_src = self.read_input(f'{input_folder_dir}/{input_file_name}')
            parsing_result = parser.parse(input_src)
            generated_ast = parsing_result.get_ast_in_json()

            # Read expected AST
            output_file_name = f'{output_folder_dir}/{re.sub(".in", ".json", input_file_name)}'
            expected_result = self.read_expected_output(output_file_name)

            self.assertEqual(generated_ast, expected_result)

    def test_cfg(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()