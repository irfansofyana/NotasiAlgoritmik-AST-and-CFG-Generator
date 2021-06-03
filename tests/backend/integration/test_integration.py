import unittest
import os
import json
from src.api.functions import *
from src.api.visualize_cfg import convert_cfg_to_graphviz, convert_cfg_json_to_graphviz


class Integration(unittest.TestCase):
    @staticmethod
    def read_input(file_name):
        with open(file_name, encoding='utf-8') as f:
            input_src = f.read()
        return input_src

    @staticmethod
    def read_output(file_name):
        with open(file_name, encoding='utf-8') as f:
            expected_output = json.load(f)
        return expected_output

    def test_ast_resurrected_successfully(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        input_folder_dir = os.path.join(parent_dir, "input-valid")
        output_folder_dir = os.path.join(parent_dir, "output-ast-valid")

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            # Read generated AST
            generated_ast = get_ast(os.path.join(input_folder_dir, input_file_name))

            # Read expected AST
            output_file_name = os.path.join(output_folder_dir, re.sub(".in", ".json", input_file_name))
            expected_result = self.read_output(output_file_name)

            self.assertEqual(generated_ast, expected_result)

    def test_cfg_resurrected_successfully(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        input_folder_dir = os.path.join(parent_dir, "input-valid")
        output_folder_dir = os.path.join(parent_dir, "output-cfg-valid")

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            # Read generated CFG
            generated_cfg = get_cfg(os.path.join(input_folder_dir, input_file_name))
            generated_cfg_in_graphviz = convert_cfg_to_graphviz(generated_cfg).source

            # Read expected CFG
            output_file_name = os.path.join(output_folder_dir, re.sub(".in", ".json", input_file_name))
            expected_cfg_in_json = self.read_output(output_file_name)
            expected_cfg_in_graphviz = convert_cfg_json_to_graphviz(expected_cfg_in_json).source

            self.assertEqual(generated_cfg_in_graphviz, expected_cfg_in_graphviz)

    def test_ast_failed_to_resurrect(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        invalid_input_dir = os.path.join(parent_dir, "input-ast-failed-to-resurrect")

        invalid_input_files = os.listdir(invalid_input_dir)
        for invalid_input_file in invalid_input_files:
            with self.assertRaises(Exception):
                get_ast(os.path.join(invalid_input_dir, invalid_input_file))

    def test_cfg_failed_to_resurrect(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        invalid_input_dir = os.path.join(parent_dir, "input-cfg-failed-to-resurrect")

        invalid_input_files = os.listdir(invalid_input_dir)
        for invalid_input_file in invalid_input_files:
            with self.assertRaises(Exception):
                get_cfg(os.path.join(invalid_input_dir, invalid_input_file))


if __name__ == '__main__':
    unittest.main()
