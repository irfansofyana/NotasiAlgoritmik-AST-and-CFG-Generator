import unittest
import os
import json
import re
from src.backend.scanner.notal_scanner import NotalScanner


class TestScanner(unittest.TestCase):
    def test_result_of_scanning(self):
        """
        Test the result of process scanning
        """

        input_folder_dir = "input"
        output_folder_dir = "output"

        input_files = os.listdir(input_folder_dir)
        for input_file_name in input_files:
            notal_scanner = NotalScanner()
            with open(f"{input_folder_dir}/{input_file_name}", encoding='utf-8') as f:
                input_src = f.read()
            notal_scanner.scan_for_tokens(input_src)
            generated_tokens = notal_scanner.get_tokens_in_json()

            output_file_name = re.sub(".in", ".json", input_file_name)
            with open(f"{output_folder_dir}/{output_file_name}", encoding='utf-8') as f:
                expected_tokens = json.load(f)

            self.assertEqual(generated_tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()
