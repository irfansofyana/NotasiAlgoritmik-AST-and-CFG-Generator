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
        f = getattr(self, 'on_' + self.get_type())
        return f()

    def on_notal_file(self):
        return self.get_children()[0].get_notal_code()

    def on_program_declaration(self):
        children = self.get_children()
        program = 'program ' + children[0].get_notal_code() + '\n'
        program += children[1].get_notal_code()
        return program

    def on_program_block(self):
        program_block = "KAMUS\n\t"
        for child in self.get_children():
            program_block += child.get_notal_code()
            program_block += "\n"
        return program_block

    def on_constant_declaration_block(self):
        constant_declaration_block = ''
        for child in self.get_children():
            constant_declaration_block += child.get_notal_code() + "\n"
        return constant_declaration_block

    def on_type_declaration_block(self):
        type_declaration_block = ''
        for child in self.get_children():
            type_declaration_block += child.get_notal_code() + "\n"
        return type_declaration_block

    def on_variable_declaration_block(self):
        variable_declaration_block = ''
        for child in self.get_children():
            variable_declaration_block += child.get_notal_code() + "\n"
        return variable_declaration_block

    def on_procedure_and_function_declaration_block(self):
        procedure_and_function_declaration_block = ''
        for child in self.get_children():
            procedure_and_function_declaration_block += child.get_notal_code() + "\n"
        return procedure_and_function_declaration_block

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

    def on_variable_declaration(self):
        children = self.get_children()
        variable_declaration = children[0].get_notal_code()
        variable_declaration += ': '
        variable_declaration += children[1].get_notal_code()
        return variable_declaration

    def on_attribute_declaration(self):
        attribute_declaration = ''
        for child in self.get_children():
            attribute = child.get_notal_code()
            if attribute_declaration == '':
                attribute_declaration += attribute
            else:
                attribute_declaration += f',{attribute}'
        return attribute_declaration

    def on_constant_declaration(self):
        children = self.get_children()
        constant_declaration = 'constant '
        constant_declaration += children[0].get_notal_code()
        constant_declaration += ' : '
        constant_declaration += children[1].get_notal_code()
        constant_declaration += ' = '
        constant_declaration += children[2].get_notal_code()
        return constant_declaration

    def on_type_declaration(self):
        children = self.get_children()
        type_declaration = 'type '
        type_declaration += children[0].get_notal_code()
        type_declaration += ' : '
        type_declaration += children[1].get_notal_code()
        return type_declaration

    def on_user_defined_type(self):
        user_defined_type = '<'
        user_defined_type += self.get_children()[0].get_notal_code()
        user_defined_type += '>'
        return user_defined_type

    def on_procedure_and_function_declaration(self):
        procedure_and_function_declaration = ''
        for child in self.get_children():
            procedure_and_function_declaration += child.get_notal_code() + '\n'
        return procedure_and_function_declaration

    def on_procedure_declaration(self):
        children = self.get_children()
        procedure_declaration = children[0].get_notal_code() + " " + children[1].get_notal_code()
        return procedure_declaration

    def on_procedure_identifier(self):
        procedure_identifier = 'procedure ' + self.get_children()[0].get_notal_code()
        return procedure_identifier

    def on_procedure_parameter_declaration(self):
        procedure_parameter_declaration = '('
        procedure_parameter_declaration += self.get_children()[0].get_notal_code()
        procedure_parameter_declaration += ')'
        return procedure_parameter_declaration

    def on_procedure_parameter_list(self):
        children = self.get_children()
        procedure_parameter_list = ''
        for child in children:
            parameter = child.get_notal_code()
            if procedure_parameter_list == '':
                procedure_parameter_list += parameter
            else:
                procedure_parameter_list += f';{parameter}'
        return procedure_parameter_list

    def on_procedure_parameter(self):
        children = self.get_children()
        return children[0].get_notal_code() + " " + children[1].get_notal_code()

    def on_procedure_parameter_type(self):
        return self.get_info()['type']

    def on_function_declaration(self):
        function_declaration = ''
        for child in self.get_children():
            function_declaration += child.get_notal_code()
        return function_declaration

    def on_function_identifier(self):
        function_identifier = 'function ' + self.get_children()[0].get_notal_code()
        return function_identifier

    def on_return_type(self):
        function_identifier = ' -> ' + self.get_children()[0].get_notal_code()
        return function_identifier

    def on_function_parameter_declaration(self):
        function_parameter_declaration = '('
        function_parameter_declaration += self.get_children()[0].get_notal_code()
        function_parameter_declaration += ')'
        return function_parameter_declaration

    def on_function_parameter_list(self):
        function_parameter_list = ''
        for child in self.get_children():
            function_parameter = child.get_notal_code()
            if function_parameter_list == '':
                function_parameter_list += function_parameter
            else:
                function_parameter_list += f',{function_parameter}'
        return function_parameter_list

    def on_function_parameter(self):
        return self.get_children()[0].get_notal_code()

    def on_operator(self):
        return self.get_info()['name']

    def on_sign_operator(self):
        return self.get_info()['value']

    def on_constant_value(self):
        if self.get_info() is not None:
            return str(self.get_info()['value'])
        else:
            constant_value = ""
            for child in self.get_children():
                constant_value += child.get_notal_code()
            return constant_value

    def on_variable(self):
        return self.get_children()[0].get_notal_code()

    def on_indexed_variable(self):
        children = self.get_children()
        indexed_var = children[0].get_notal_code() + '['
        indexed_var += children[1].get_notal_code()
        indexed_var += ']'
        return indexed_var

    def on_index_expression_list(self):
        index_expression_list = ''
        for child in self.get_children():
            expression = child.get_notal_code()
            if index_expression_list == '':
                index_expression_list += expression
            else:
                index_expression_list += f',{expression}'
        return index_expression_list

    def on_field_designator(self):
        children = self.get_children()
        field_designator = children[0].get_notal_code()
        field_designator += "."
        field_designator += children[1].get_notal_code()
        return field_designator

    def on_expression(self):
        children = self.get_children()
        expression = ''
        for child in children:
            expression += child.get_notal_code()
        return expression

    def on_additive_expression(self):
        return self.on_expression()

    def on_multiplicative_expression(self):
        return self.on_expression()

    def on_exponentiation_expression(self):
        children = self.get_children()
        expression = children[0].get_notal_code() + "^" + children[1].get_notal_code()
        return expression

    def on_unary_expression(self):
        return self.on_expression()

    def on_set_constructor(self):
        set_constructor = '['
        set_constructor += self.get_children()[0].get_notal_code()
        set_constructor += ']'

    def on_member_designator_list(self):
        children = self.get_children()
        member_designator_list = ''
        for child in children:
            member_designator = child.get_notal_code()
            if member_designator_list == '':
                member_designator_list += member_designator
            else:
                member_designator_list += f',{member_designator}'
        return member_designator_list

    def on_member_designator(self):
        children = self.get_children()
        member_designator = ''
        for child in children:
            designator = child.get_notal_code()
            if member_designator == '':
                member_designator += designator
            else:
                member_designator += f'..{designator}'
        return member_designator

    def on_user_defined_function_call(self):
        children = self.get_children()
        function_call = ''
        for child in children:
            function_call += child.get_notal_code()
        return children

    def on_math_function_call(self):
        return self.get_children()[0].get_notal_code()

    def on_function(self, func_name):
        function = f'{func_name}('
        function += self.get_children()[0].get_notal_code()
        function += ')'
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
    # notal_dict =
    parser = ASTParser(ast_dict=notal_dict)
    print(parser.get_notal_code())
    pass
