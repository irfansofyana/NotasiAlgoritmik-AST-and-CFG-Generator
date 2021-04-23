from src.backend.parser.ast import AST


class ASTParser(AST):
    def __init__(self, ast_dict=None):
        super().__init__()
        self.built_from_dict(ast_dict=ast_dict)

    def built_from_dict(self, ast_dict):
        self.type = ast_dict['type']
        self.info = ast_dict['info']
        self.children = []

        if 'children' not in ast_dict:
            return

        for child in ast_dict['children']:
            ast_child = ASTParser(ast_dict=child)
            self.children.append(ast_child)

    def get_notal_code(self):
        node_type_handler = {
            'algorithm_block': self.on_algorithm_block,
            'type_denoter': self.on_type_denoter,
            'ordinal_type': self.on_ordinal_type,
            'enumerated_type': self.on_enumerated_type,
            'subrange_type': self.on_subrange_type,
            'subrange_value': self.on_subrange_value,
            'structured_type': self.on_structured_type,
            'array_type': self.on_array_type,
            'array_index': self.on_array_index,
            'identifier': self.on_identifier,
            'identifier_list': self.on_identifier_list,
            'operator': self.on_operator,
            'sign_operator': self.on_sign_operator,
            'boolean_constant': self.on_constant_value,
            'integer_constant': self.on_constant_value,
            'real_constant': self.on_constant_value,
            'string_constant': self.on_constant_value,
            'char_constant': self.on_constant_value,
            'nil_constant': self.on_constant_value,
            'constant_value': self.on_constant_value,
            'math_function_call': self.on_math_function_call,
            'abs_function': self.on_abs_function,
            'sin_function': self.on_sin_function,
            'cos_function': self.on_cos_function,
            'tan_function': self.on_tan_function,
            'succ_function': self.on_succ_function,
            'pred_function': self.on_pred_function,
            'string_function_call': self.on_string_function_call,
            'awal_function': self.on_awal_function,
            'akhir_function': self.on_akhir_function,
            'firstchar_function': self.on_firstchar_function,
            'lastchar_function': self.on_lastchar_function,
            'long_function': self.on_long_function,
            'iskosong_function': self.on_iskosong_function,
            'converter_function_call': self.on_converter_function_call,
            'integer_to_real_converter': self.on_integer_to_real_converter,
            'real_to_integer_converter': self.on_real_to_integer_converter,
        }
        f = node_type_handler[self.get_type()]
        return f()

    def on_algorithm_block(self):
        child = self.get_children()
        algorithm_block = "ALGORITMA\n" + child.get_notal_code()
        return algorithm_block

    def on_type_denoter(self):
        if len(self.get_children()) == 0:
            return self.get_info()['type_name']
        else:
            return self.get_children()[0].get_notal_code()

    def on_ordinal_type(self):
        return self.get_children()[0].get_notal_code()

    def on_enumerated_type(self):
        return "(" + self.get_children()[0].get_notal_code() + ")"

    def on_subrange_type(self):
        children = self.get_children()
        return children[0].get_notal_code() + ".." + children[1].get_notal_code()

    def on_subrange_value(self):
        return self.get_children()[0].get_notal_code()

    def on_structured_type(self):
        return self.get_children()[0].get_notal_code()

    def on_array_type(self):
        children = self.get_children()
        return "array " + children[0].get_notal_code() + " of " + children[1].get_notal_code()

    def on_array_index(self):
        array_index = '['
        for child in self.get_children():
            array_index += child.get_notal_code() if array_index == '[' else f',{child.get_notal_code()}'
        array_index += ']'
        return array_index

    def on_identifier(self):
        return self.get_info()['identifier_name']

    def on_identifier_list(self):
        identifier_list = ''
        for child in self.get_children():
            identifier = child.get_notal_code()
            if identifier_list == '':
                identifier_list = identifier
            else:
                identifier_list += f',{identifier}'
        return identifier_list

    def on_operator(self):
        return self.get_info()['name']

    def on_sign_operator(self):
        return self.get_info()['value']

    def on_constant_value(self):
        if self.get_info() is not None:
            return self.get_info()['value']
        else:
            constant_value = ""
            for child in self.get_children():
                constant_value += child.get_notal_code()
            return constant_value

    def on_math_function_call(self):
        return self.get_children()[0].get_notal_code()

    def on_function(self, func_name):
        function = f"{func_name}("
        function += self.get_children()[0].get_notal_code()
        function += ")"
        return function

    def on_abs_function(self):
        return self.on_function('abs')

    def on_sin_function(self):
        return self.on_function('sin')

    def on_cos_function(self):
        return self.on_function('cos')

    def on_tan_function(self):
        return self.on_function('tan')

    def on_succ_function(self):
        return self.on_function('succ')

    def on_pred_function(self):
        return self.on_function('pred')

    def on_string_function_call(self):
        return self.get_children()[0].get_notal_code()

    def on_awal_function(self):
        return self.on_function('awal')

    def on_akhir_function(self):
        return self.on_function('akhir')

    def on_firstchar_function(self):
        return self.on_function('firstchar')

    def on_lastchar_function(self):
        return self.on_function('lastchar')

    def on_long_function(self):
        return self.on_function('long')

    def on_iskosong_function(self):
        return self.on_function('iskosong')

    def on_converter_function_call(self):
        return self.get_children()[0].get_notal_code()

    def on_integer_to_real_converter(self):
        return self.on_function('intToReal')

    def on_real_to_integer_converter(self):
        return self.on_function('realToInteger')


if __name__ == "__main__":
    notal_dict = {
        "type": "identifier_list",
        "info": None,
        "children": [
            {
                "type": "identifier",
                "info": {
                    "identifier_name": "x"
                }
            },
            {
                "type": "identifier",
                "info": {
                    "identifier_name": "y"
                }
            }
        ]
    }
    parser = ASTParser(ast_dict=notal_dict)
    print(parser.get_notal_code())
    pass
