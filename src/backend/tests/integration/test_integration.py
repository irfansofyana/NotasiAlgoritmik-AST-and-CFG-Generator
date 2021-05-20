import unittest
import os
import json
from src.api.functions import *
from src.api.visualize_cfg import convert_cfg_to_graphviz


class Integration(unittest.TestCase):
    @staticmethod
    def read_input(file_name):
        with open(file_name, encoding='utf-8') as f:
            input_src = f.read()
        return input_src

    @staticmethod
    def read_expected_ast(file_name):
        with open(file_name, encoding='utf-8') as f:
            expected_tokens = json.load(f)
        return expected_tokens

    @staticmethod
    def read_expected_cfg(file_name):
        with open(file_name, encoding='utf-8') as f:
            expected_cfg = f.read()
        return expected_cfg

    def test_ast(self):
        input_folder_dir = "input"
        output_folder_dir = "output-ast"

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            # Read generated AST
            generated_ast = get_ast(f'{input_folder_dir}/{input_file_name}')

            # Read expected AST
            output_file_name = f'{output_folder_dir}/{re.sub(".in", ".json", input_file_name)}'
            expected_result = self.read_expected_ast(output_file_name)

            self.assertEqual(generated_ast, expected_result)

    def test_cfg(self):
        input_folder_dir = "input"
        output_folder_dir = "output-cfg"

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            # Read generated CFG
            generated_cfg = get_cfg(f'{input_folder_dir}/{input_file_name}')
            generated_cfg = str(convert_cfg_to_graphviz(generated_cfg))

            # Read expected CFG
            output_file_name = f'{output_folder_dir}/{re.sub(".in", ".out", input_file_name)}'
            expected_result = self.read_expected_cfg(output_file_name)

            self.assertEqual(generated_cfg, expected_result)


if __name__ == '__main__':
    unittest.main()
