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
            'identifier': self.on_identifier,
            'identifier_list': self.on_identifier_list,
            'operator': self.on_operator,
            'sign_operator': self.on_sign_operator,
            'boolean_constant': self.on_constant_value,
            'integer_constant': self.on_constant_value,
            'real_constant': self.on_constant_value,
            'string_constant': self.on_constant_value,
            'char_constant': self.on_constant_value,
            'nil_constant': self.on_constant_value
        }
        f = node_type_handler[self.get_type()]
        return f()

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
        return self.get_info()['value']


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
