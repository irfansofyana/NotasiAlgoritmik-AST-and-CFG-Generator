import unittest
import os
import json
import re
from src.backend.scanner.notal_scanner import NotalScanner, IndentLexer


class TestScanner(unittest.TestCase):
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

    def test_result_of_scanning(self):
        """
        Test the result of process scanning
        """
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        input_folder_dir = os.path.join(parent_dir, "input")
        output_folder_dir = os.path.join(parent_dir, "output")

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            scanner = NotalScanner()
            scanner = IndentLexer(scanner)

            # Find generated tokens
            input_src = self.read_input(os.path.join(input_folder_dir, input_file_name))
            scanner.scan_for_tokens(input_src)
            generated_tokens = scanner.get_tokens_in_json()

            # Read expected tokens
            output_file_name = os.path.join(output_folder_dir, re.sub(".in", ".json", input_file_name))
            expected_tokens = self.read_expected_output(output_file_name)

            self.assertEqual(generated_tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
