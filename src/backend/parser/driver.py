from notal_parser import NotalParser

if __name__=="__main__":
    parser = NotalParser()

    input_directory_folder = 'input'
    input_file_name = '1.in'
    with open(f'{input_directory_folder}/{input_file_name}', encoding='utf-8') as f:
        src_input = f.read()

        parsing_result = parser.parse(src_input)
        print(parsing_result)