from notal_scanner import NotalScanner
import json

if __name__ == "__main__":
    scanner = NotalScanner()

    input_directory_folder = 'input'
    input_file_name = '1.in'
    with open(f'{input_directory_folder}/{input_file_name}', encoding='utf-8') as f:
        src_input = f.read()

        scanner.scan_for_tokens(src_input)
        tokens = scanner.get_tokens_in_json()
        print(json.dumps(tokens, indent=2))