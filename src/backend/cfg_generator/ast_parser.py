from src.backend.parser.ast import AST
import re


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

    def get_notal_src(self):
        f = getattr(self, 'on_' + self.get_type())
        return f()

    def on_notal_file(self):
        return self.get_children()[0].get_notal_src()

    def on_program_declaration(self):
        children = self.get_children()
        program = 'program ' + children[0].get_notal_src() + '\n'
        program += children[1].get_notal_src()
        return program

    def on_program_block(self):
        program_block = "KAMUS\n\t"
        for child in self.get_children():
            program_block += child.get_notal_src()
            program_block += "\n"
        return program_block

    def on_constant_declaration_block(self):
        constant_declaration_block = ''
        for child in self.get_children():
            constant_declaration_block += child.get_notal_src() + "\n"
        return constant_declaration_block

    def on_type_declaration_block(self):
        type_declaration_block = ''
        for child in self.get_children():
            type_declaration_block += child.get_notal_src() + "\n"
        return type_declaration_block

    def on_variable_declaration_block(self):
        variable_declaration_block = ''
        for child in self.get_children():
            variable_declaration_block += child.get_notal_src() + "\n"
        return variable_declaration_block

    def on_procedure_and_function_declaration_block(self):
        procedure_and_function_declaration_block = ''
        for child in self.get_children():
            procedure_and_function_declaration_block += child.get_notal_src() + "\n"
        return procedure_and_function_declaration_block

    def on_procedure_and_function_implementation_block(self):
        procedure_and_function_implementation_block = ''
        for child in self.get_children():
            procedure_and_function_implementation_block += child.get_notal_src() + "\n"
        return procedure_and_function_implementation_block

    def on_procedure_implementation_list(self):
        procedure_implementation_list = ''
        for child in self.get_children():
            procedure_implementation_list += child.get_notal_src() + "\n"
        return procedure_implementation_list

    def on_procedure_implementation(self):
        children = self.get_children()
        procedure_implementation = children[0].get_notal_src() + " " + children[1].get_notal_src()
        return procedure_implementation

    def on_procedure_implementation_algorithm(self):
        procedure_implementation_algorithm = 'kamus lokal'
        procedure_implementation_algorithm += '\n\t'
        procedure_implementation_algorithm += self.get_children()[0].get_notal_src()
        return procedure_implementation_algorithm

    def on_function_implementation_list(self):
        function_implementation_list = ''
        for child in self.get_children():
            function_implementation_list += child.get_notal_src() + "\n"
        return function_implementation_list

    def on_function_implementation(self):
        children = self.get_children()
        function_implementation = children[0].get_notal_src() + " " + children[1].get_notal_src()
        return function_implementation

    def on_function_implementation_algorithm(self):
        function_implementation_algorithm = 'kamus lokal'
        function_implementation_algorithm += '\n\t'
        function_implementation_algorithm += self.get_children()[0].get_notal_src()
        return function_implementation_algorithm

    def on_algorithm_block(self):
        algorithm_block = "ALGORITMA\n" + self.get_children()[0].get_notal_src()
        return algorithm_block

    def on_type_denoter(self):
        if len(self.get_children()) == 0:
            return self.get_info()['type_name']
        else:
            return self.get_children()[0].get_notal_src()

    def on_ordinal_type(self):
        return self.get_children()[0].get_notal_src()

    def on_enumerated_type(self):
        return "(" + self.get_children()[0].get_notal_src() + ")"

    def on_subrange_type(self):
        children = self.get_children()
        return children[0].get_notal_src() + ".." + children[1].get_notal_src()

    def on_subrange_value(self):
        return self.get_children()[0].get_notal_src()

    def on_structured_type(self):
        return self.get_children()[0].get_notal_src()

    def on_array_type(self):
        children = self.get_children()
        return "array " + children[0].get_notal_src() + " of " + children[1].get_notal_src()

    def on_array_index(self):
        array_index = '['
        for child in self.get_children():
            array_index += child.get_notal_src() if array_index == '[' else f',{child.get_notal_src()}'
        array_index += ']'
        return array_index

    def on_identifier(self):
        return self.get_info()['identifier_name']

    def on_identifier_list(self):
        identifier_list = ''
        for child in self.get_children():
            identifier = child.get_notal_src()
            if identifier_list == '':
                identifier_list = identifier
            else:
                identifier_list += f',{identifier}'
        return identifier_list

    def on_variable_declaration(self):
        children = self.get_children()
        variable_declaration = children[0].get_notal_src()
        variable_declaration += ': '
        variable_declaration += children[1].get_notal_src()
        return variable_declaration

    def on_attribute_declaration(self):
        attribute_declaration = ''
        for child in self.get_children():
            attribute = child.get_notal_src()
            if attribute_declaration == '':
                attribute_declaration += attribute
            else:
                attribute_declaration += f',{attribute}'
        return attribute_declaration

    def on_constant_declaration(self):
        children = self.get_children()
        constant_declaration = 'constant '
        constant_declaration += children[0].get_notal_src()
        constant_declaration += ' : '
        constant_declaration += children[1].get_notal_src()
        constant_declaration += ' = '
        constant_declaration += children[2].get_notal_src()
        return constant_declaration

    def on_type_declaration(self):
        children = self.get_children()
        type_declaration = 'type '
        type_declaration += children[0].get_notal_src()
        type_declaration += ' : '
        type_declaration += children[1].get_notal_src()
        return type_declaration

    def on_user_defined_type(self):
        user_defined_type = '<'
        user_defined_type += self.get_children()[0].get_notal_src()
        user_defined_type += '>'
        return user_defined_type

    def on_procedure_and_function_declaration(self):
        procedure_and_function_declaration = ''
        for child in self.get_children():
            procedure_and_function_declaration += child.get_notal_src() + '\n'
        return procedure_and_function_declaration

    def on_procedure_declaration(self):
        children = self.get_children()
        procedure_declaration = children[0].get_notal_src() + " " + children[1].get_notal_src()
        return procedure_declaration

    def on_procedure_identifier(self):
        procedure_identifier = 'procedure ' + self.get_children()[0].get_notal_src()
        return procedure_identifier

    def on_procedure_parameter_declaration(self):
        procedure_parameter_declaration = '('
        procedure_parameter_declaration += self.get_children()[0].get_notal_src()
        procedure_parameter_declaration += ')'
        return procedure_parameter_declaration

    def on_procedure_parameter_list(self):
        children = self.get_children()
        procedure_parameter_list = ''
        for child in children:
            parameter = child.get_notal_src()
            if procedure_parameter_list == '':
                procedure_parameter_list += parameter
            else:
                procedure_parameter_list += f';{parameter}'
        return procedure_parameter_list

    def on_procedure_parameter(self):
        children = self.get_children()
        return children[0].get_notal_src() + " " + children[1].get_notal_src()

    def on_procedure_parameter_type(self):
        return self.get_info()['type']

    def on_function_declaration(self):
        function_declaration = ''
        for child in self.get_children():
            function_declaration += child.get_notal_src()
        return function_declaration

    def on_function_identifier(self):
        function_identifier = 'function ' + self.get_children()[0].get_notal_src()
        return function_identifier

    def on_return_type(self):
        function_identifier = ' -> ' + self.get_children()[0].get_notal_src()
        return function_identifier

    def on_function_parameter_declaration(self):
        function_parameter_declaration = '('
        function_parameter_declaration += self.get_children()[0].get_notal_src()
        function_parameter_declaration += ')'
        return function_parameter_declaration

    def on_function_actual_parameter(self):
        function_actual_parameter = '('
        function_actual_parameter += self.get_children()[0].get_notal_src()
        function_actual_parameter += ')'
        return function_actual_parameter

    def on_function_parameter_list(self):
        function_parameter_list = ''
        for child in self.get_children():
            function_parameter = child.get_notal_src()
            if function_parameter_list == '':
                function_parameter_list += function_parameter
            else:
                function_parameter_list += f',{function_parameter}'
        return function_parameter_list

    def on_function_parameter(self):
        return self.get_children()[0].get_notal_src()

    def on_compound_statement(self):
        children = self.get_children()
        compound_statement = children[0].get_notal_src()
        compound_statement = re.sub('\n', "\n\t", compound_statement)
        compound_statement = '\t' + compound_statement
        return compound_statement

    def on_statement_sequence(self):
        statement_sequence = ''
        for child in self.get_children():
            statement_sequence += child.get_notal_src() + '\n'
        return statement_sequence

    def on_assignment_statement(self):
        children = self.get_children()
        assignment_statement = children[0].get_notal_src()
        assignment_statement += ' <- '
        assignment_statement += children[1].get_notal_src()
        return assignment_statement

    def on_function_returned_statement(self):
        children = self.get_children()
        returned_statement = '->' + children[0].get_notal_src()
        return returned_statement

    def on_procedure_statement(self):
        children = self.get_children()
        procedure_statement = ''
        procedure_statement += children[0].get_notal_src()
        if len(children) == 2:
            procedure_statement += '('
            procedure_statement += children[1].get_notal_src()
            procedure_statement += ')'
        return procedure_statement

    def on_actual_parameter_list(self):
        actual_parameter_list = ''
        for child in self.get_children():
            actual_param = child.get_notal_src()
            if actual_parameter_list == '':
                actual_parameter_list += actual_param
            else:
                actual_parameter_list += f',{actual_param}'
        return actual_parameter_list

    def on_actual_parameter(self):
        return self.get_children()[0].get_notal_src()

    def on_input_statement(self):
        input_statement = 'input('
        input_statement += self.get_children()[0].get_notal_src()
        input_statement += ')'
        return input_statement

    def on_input_statement_parameter_list(self):
        input_statement_parameter_list = ''
        for child in self.get_children():
            input_statement_parameter = child.get_notal_src()
            if input_statement_parameter_list == '':
                input_statement_parameter_list += input_statement_parameter
            else:
                input_statement_parameter_list += f',{input_statement_parameter}'
        return input_statement_parameter_list

    def on_input_statement_parameter(self):
        return self.get_children()[0].get_notal_src()

    def on_output_statement(self):
        input_statement = 'output('
        input_statement += self.get_children()[0].get_notal_src()
        input_statement += ')'
        return input_statement

    def on_output_statement_parameter_list(self):
        output_statement_parameter_list = ''
        for child in self.get_children():
            output_statement_parameter = child.get_notal_src()
            if output_statement_parameter_list == '':
                output_statement_parameter_list += output_statement_parameter
            else:
                output_statement_parameter_list += f',{output_statement_parameter}'
        return output_statement_parameter_list

    def on_output_statement_parameter(self):
        return self.get_children()[0].get_notal_src()

    def on_depend_on_statement(self):
        children = self.get_children()
        depend_on_statement = 'depend on ('
        depend_on_statement += children[0].get_notal_src()
        depend_on_statement += ')\n\t'
        depend_on_statement += children[1].get_notal_src()
        depend_on_statement += '\n'
        return depend_on_statement

    def on_depend_on_action_list(self):
        depend_on_action_list = ''
        for child in self.get_children():
            depend_on_action = child.get_notal_src()
            if depend_on_action_list == '':
                depend_on_action_list += depend_on_action
            else:
                depend_on_action_list += f';\n{depend_on_action}'
        return depend_on_action_list

    def on_depend_on_action(self):
        children = self.get_children()
        depend_on_action = children[0].get_notal_src() + ": " + children[1].get_notal_src()
        return depend_on_action

    def on_if_statement(self):
        children = self.get_children()
        if_statement = 'if '
        if_statement += children[0].get_notal_src()
        if_statement += ' then '
        if_statement += children[1].get_notal_src()
        if len(children) == 3:
            if_statement += ' else '
            if_statement += children[2].get_notal_src()
        return if_statement

    def on_repeat_until_statement(self):
        children = self.get_children()
        repeat_until_statement = 'repeat '
        repeat_until_statement += children[0].get_notal_src()
        repeat_until_statement += ' until '
        repeat_until_statement += children[1].get_notal_src()
        return repeat_until_statement

    def on_repeat_times_statement(self):
        children = self.get_children()
        repeat_times_statement = 'repeat '
        repeat_times_statement += children[0].get_notal_src()
        repeat_times_statement += ' times\n'
        repeat_times_statement += children[1].get_notal_src()
        return repeat_times_statement

    def on_while_statement(self):
        children = self.get_children()
        while_statement = 'while '
        while_statement += children[0].get_notal_src()
        while_statement += ' do\n'
        while_statement += children[1].get_notal_src()
        return while_statement

    def on_iterate_stop_statement(self):
        children = self.get_children()
        iterate_statement = 'iterate '
        iterate_statement += children[0].get_notal_src()
        iterate_statement += ' stop '
        iterate_statement += children[1].get_notal_src()
        iterate_statement += children[2].get_notal_src()
        return iterate_statement

    def on_traversal_statement(self):
        children = self.get_children()
        traversal_statement = children[0].get_notal_src()
        traversal_statement += " traversal "
        traversal_statement += children[1].get_notal_src()
        traversal_statement += "\n"
        traversal_statement += children[2].get_notal_src()
        return traversal_statement

    def on_traversal_range_value(self):
        traversal_range_value = '['
        traversal_range_value += self.get_children()[0].get_notal_src()
        traversal_range_value += ']'
        return traversal_range_value

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
                constant_value += child.get_notal_src()
            return constant_value

    def on_boolean_constant(self):
        return self.on_constant_value()

    def on_integer_constant(self):
        return self.on_constant_value()

    def on_real_constant(self):
        return self.on_constant_value()

    def on_string_constant(self):
        return self.on_constant_value()

    def on_character_constant(self):
        return self.on_constant_value()

    def on_nil_constant(self):
        return self.on_constant_value()

    def on_variable(self):
        return self.get_children()[0].get_notal_src()

    def on_indexed_variable(self):
        children = self.get_children()
        indexed_var = children[0].get_notal_src() + '['
        indexed_var += children[1].get_notal_src()
        indexed_var += ']'
        return indexed_var

    def on_index_expression_list(self):
        index_expression_list = ''
        for child in self.get_children():
            expression = child.get_notal_src()
            if index_expression_list == '':
                index_expression_list += expression
            else:
                index_expression_list += f',{expression}'
        return index_expression_list

    def on_field_designator(self):
        children = self.get_children()
        field_designator = children[0].get_notal_src()
        field_designator += "."
        field_designator += children[1].get_notal_src()
        return field_designator

    def on_expression(self):
        children = self.get_children()
        expression = ''
        for child in children:
            if expression == '':
                expression += child.get_notal_src()
            else:
                expression += f' {child.get_notal_src()}'
        return expression

    def on_additive_expression(self):
        return self.on_expression()

    def on_multiplicative_expression(self):
        return self.on_expression()

    def on_exponentiation_expression(self):
        children = self.get_children()
        expression = children[0].get_notal_src() + "^" + children[1].get_notal_src()
        return expression

    def on_unary_expression(self):
        return self.on_expression()

    def on_set_constructor(self):
        set_constructor = '['
        set_constructor += self.get_children()[0].get_notal_src()
        set_constructor += ']'

    def on_member_designator_list(self):
        children = self.get_children()
        member_designator_list = ''
        for child in children:
            member_designator = child.get_notal_src()
            if member_designator_list == '':
                member_designator_list += member_designator
            else:
                member_designator_list += f',{member_designator}'
        return member_designator_list

    def on_member_designator(self):
        children = self.get_children()
        member_designator = ''
        for child in children:
            designator = child.get_notal_src()
            if member_designator == '':
                member_designator += designator
            else:
                member_designator += f'..{designator}'
        return member_designator

    def on_user_defined_function_call(self):
        children = self.get_children()
        function_call = ''
        for child in children:
            function_call += child.get_notal_src()
        return function_call

    def on_math_function_call(self):
        return self.get_children()[0].get_notal_src()

    def on_function(self, func_name):
        function = f'{func_name}('
        function += self.get_children()[0].get_notal_src()
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
        return self.get_children()[0].get_notal_src()

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
        return self.get_children()[0].get_notal_src()

    def on_integer_to_real_converter(self):
        return self.on_function('intToReal')

    def on_real_to_integer_converter(self):
        return self.on_function('realToInteger')

