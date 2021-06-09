import ply.yacc as yacc
import re
from src.backend.scanner.notal_scanner import NotalScanner, IndentLexer
from src.backend.parser.ast import AST


class NotalParser(object):
    tokens = NotalScanner.tokens
    start = 'file'

    def p_file(self, p):
        """file :   program
        """
        p[0] = AST("notal_file", [p[1]])

    def p_program(self, p):
        """program  :   RW_PROGRAM identifier block
        """
        p[0] = AST("program_declaration", [p[2], p[3]])

    def p_identifier_list(self, p):
        """identifier_list  : identifier_list S_COMMA identifier
                            | identifier
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("identifier_list", [*curr_children, p[3]])

    def p_block(self, p):
        """block    :   RW_KAMUS INDENT constant_declaration_block type_declaration_block variable_declaration_block procedure_and_function_declaration_block algorithm_block procedure_and_function_implementation_block
                    | RW_KAMUS algorithm_block procedure_and_function_implementation_block
        """
        children = []
        start_index = 2 if len(p) == 4 else 3
        for i in range(start_index, len(p)):
            if p[i]:
                children.append(p[i])
        p[0] = AST("program_block", children)

    def p_constant_declaration_block(self, p):
        """constant_declaration_block  : empty
                    | constant_declaration
        """
        if p[1]:
            curr_children = p[1].get_children_or_itself()
            p[0] = AST("constant_declaration_block", [*curr_children])

    def p_type_declaration_block(self, p):
        """type_declaration_block  :   empty
                    |   type_declaration
        """
        if p[1]:
            curr_children = p[1].get_children_or_itself()
            p[0] = AST("type_declaration_block",[*curr_children])

    def p_variable_declaration_block(self, p):
        """variable_declaration_block  :   empty
                    |   variable_declaration
        """
        if p[1]:
            curr_children = p[1].get_children_or_itself()
            p[0] = AST("variable_declaration_block", [*curr_children])

    def p_procedure_and_function_declaration_block(self, p):
        """procedure_and_function_declaration_block  :   DEDENT
                    |   procedure_and_function_declaration DEDENT
        """
        if len(p) == 3:
            curr_children = p[1].get_children_or_itself()
            p[0] = AST("procedure_and_function_declaration_block", [*curr_children])

    def p_algorithm_block(self, p):
        """algorithm_block  :   RW_ALGORITMA statement_part
        """
        p[0] = AST("algorithm_block", [p[2]])

    def p_procedure_and_function_implementation_block(self, p):
        """procedure_and_function_implementation_block  :   empty
                    |   subprogram_implementation_list
        """
        if len(p) == 2:
            if p[1] is not None:
                p[0] = p[1]

    def p_subprogram_implementation_list(self, p):
        """subprogram_implementation_list : subprogram_implementation_list subprogram_implementation
                                        | subprogram_implementation
        """
        if len(p) == 2:
            p[0] = AST("procedure_and_function_implementation_block", [p[1]])
        else:
            curr_children = p[1].get_children_or_itself()
            p[0] = AST("procedure_and_function_implementation_block", [*curr_children, p[2]])

    def p_subprogram_implementation(self, p):
        """subprogram_implementation : procedure_implementation
                                     | function_implementation
        """
        p[0] = p[1]

    def p_procedure_implementation(self, p):
        """procedure_implementation :   procedure_declaration   procedure_implementation_block
        """
        p[0] = AST("procedure_implementation", [p[1], p[2]])

    def p_procedure_implementation_block(self, p):
        """procedure_implementation_block   :   RW_KAMUS RW_LOKAL INDENT constant_declaration_block type_declaration_block variable_declaration_block DEDENT algorithm_block
                                            | RW_KAMUS RW_LOKAL algorithm_block
        """
        children = []
        start_index = 3 if len(p) == 4 else 4
        for i in range(start_index, len(p)):
            if p[i] and i != 7:
                children.append(p[i])
        p[0] = AST("procedure_implementation_algorithm", children)

    def p_function_implementation(self, p):
        """function_implementation  :   function_declaration function_implementation_block
        """
        p[0] = AST("function_implementation", [p[1], p[2]])

    def p_function_implementation_block(self, p):
        """function_implementation_block    :   RW_KAMUS RW_LOKAL INDENT constant_declaration_block type_declaration_block variable_declaration_block DEDENT  algorithm_block
                                            | RW_KAMUS RW_LOKAL algorithm_block
        """
        children = []
        start_index = 3 if len(p) == 4 else 4
        for i in range(start_index, len(p)):
            if p[i] and i != 7:
                children.append(p[i])
        p[0] = AST("function_implementation_algorithm", children)

    def p_type_denoter(self, p):
        """type_denoter :   ordinal_type
                        |   structured_type
                        |   RW_INTEGER
                        |   RW_REAL
                        |   RW_STRING
                        |   RW_CHARACTER
                        |   RW_BOOLEAN
        """
        if isinstance(p[1], str):
            info = {
                'type_name': p[1]
            }
            p[0] = AST("type_denoter", None, info)
        else:
            p[0] = AST("type_denoter", [p[1]])

    def p_ordinal_type(self, p):
        """ordinal_type :   enumerated_type
                        |   subrange_type
                        |   identifier
        """
        p[0] = AST("ordinal_type", [p[1]])

    def p_enumerated_type(self, p):
        """enumerated_type  :   S_LEFT_BRACKET identifier_list S_RIGHT_BRACKET
        """
        p[0] = AST("enumerated_type", [p[2]])

    def p_subrange_type(self, p):
        """subrange_type    :  subrange_type_option
        """
        p[0] = p[1]

    def p_subrange_type_option(self, p):
        """subrange_type_option    :   subrange_option S_UP_TO subrange_option
        """
        p[0] = AST("subrange_type", [p[1], p[3]])

    def p_subrange_option(self, p):
        """subrange_option  :   identifier
                            |   constant
                            |   function_designator
        """
        p[0] = AST("subrange_value", [p[1]])

    def p_structured_type(self, p):
        """structured_type  :   array_type
        """
        p[0] = AST("structured_type", [p[1]])

    def p_array_type(self, p):
        """array_type   :   RW_ARRAY array_index RW_OF component_type
        """
        p[0] = AST("array_type", [p[2], p[4]])

    def p_array_index(self, p):
        """array_index  :   S_LEFT_SQUARE_BRACKET index_list S_RIGHT_SQUARE_BRACKET
        """
        p[0] = p[2]

    def p_index_list(self, p):
        """index_list   :   index_list S_COMMA index_type
                        |   index_type
        """
        if len(p) == 2:
            p[0] = AST("array_index", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("array_index", [*curr_children, p[3]])

    def p_index_type(self, p):
        """index_type   :   ordinal_type
        """
        p[0] = p[1]

    def p_component_type(self, p):
        """component_type   :   type_denoter"""
        p[0] = p[1]

    def p_variable_declaration(self, p):
        """variable_declaration :  variable_declaration variable_sub_declaration
                                |   variable_sub_declaration
        """
        if len(p) == 2:
            p[0] = AST("variable_declaration", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("variable_declaration", [*curr_children, p[2]])

    def p_variable_sub_declaration(self, p):
        """variable_sub_declaration :   identifier_list S_COLON type_denoter
        """
        p[0] = AST("variable_declaration", [p[1], p[3]])

    def p_variable_declaration_comma(self, p):
        """variable_declaration_comma   :   variable_sub_declaration
                                        |   variable_sub_declaration S_COMMA variable_declaration_comma
        """
        if len(p) == 2:
            p[0] = AST("attribute_declaration", [p[1]])
        else:
            curr_children = [] if p[3] is None else p[3].get_children_or_itself()
            p[0] = AST("attribute_declaration", [*curr_children, p[1]])

    def p_constant_declaration(self, p):
        """constant_declaration :   constant_declaration constant_sub_declaration
                                |   constant_sub_declaration
        """
        if len(p) == 2:
            p[0] = AST("constant_declaration", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("constant_declaration", [*curr_children, p[2]])

    def p_constant_sub_declaration(self, p):
        """constant_sub_declaration :   RW_CONSTANT identifier S_COLON type_denoter S_EQUAL constant
        """
        p[0] = AST("constant_declaration", [p[2], p[4], p[6]])

    def p_type_declaration(self, p):
        """type_declaration :   type_declaration type_sub_declaration
                            |   type_sub_declaration
        """
        if len(p) == 2:
            p[0] = AST("type_declaration", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("type_declaration", [*curr_children, p[2]])

    def p_type_sub_declaration(self, p):
        """type_sub_declaration :   RW_TYPE identifier S_COLON type_variety
        """
        p[0] = AST("type_declaration", [p[2], p[4]])

    def p_type_variety(self, p):
        """type_variety :   type_denoter
                        |   type_user_defined
        """
        p[0] = p[1]

    def p_type_user_defined(self, p):
        """type_user_defined    :   S_LESS_THAN variable_declaration_comma S_GREATER_THAN
        """
        p[0] = AST("user_defined_type", [p[2]])

    def p_procedure_and_function_declaration(self, p):
        """procedure_and_function_declaration   :   procedure_and_function_declaration procedure_and_function_sub_declaration
                                                |   procedure_and_function_sub_declaration
        """
        if len(p) == 2:
            p[0] = AST("procedure_and_function_declaration", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("procedure_and_function_declaration", [*curr_children, p[2]])

    def p_procedure_and_function_sub_declaration(self, p):
        """procedure_and_function_sub_declaration   :   procedure_declaration
                                                    |   function_declaration
        """
        p[0] = p[1]

    def p_procedure_declaration(self, p):
        """procedure_declaration    :  procedure_identifier formal_parameter_list
        """
        p[0] = AST("procedure_declaration", [p[1], p[2]])

    def p_procedure_identifier(self, p):
        """procedure_identifier :   RW_PROCEDURE identifier
        """
        p[0] = AST("procedure_identifier", [p[2]])

    def p_formal_parameter_list(self, p):
        """formal_parameter_list    :   S_LEFT_BRACKET formal_parameter_section_list S_RIGHT_BRACKET
        """
        p[0] = AST("procedure_parameter_declaration", [p[2]])

    def p_formal_parameter_section_list(self, p):
        """formal_parameter_section_list    :   empty
                                            |   formal_parameter_section
        """
        p[0] = p[1]

    def p_formal_parameter_section(self, p):
        """formal_parameter_section :   formal_parameter_section S_SEMI_COLON parameter_specification
                                    |   parameter_specification
        """
        if len(p) == 2:
            p[0] = AST("procedure_parameter_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("procedure_parameter_list", [*curr_children, p[3]])

    def p_parameter_specification(self, p):
        """parameter_specification  :   procedure_parameter_type  variable_sub_declaration
        """
        p[0] = AST("procedure_parameter", [p[1], p[2]])

    def p_procedure_parameter_type(self, p):
        """procedure_parameter_type :   RW_INPUT
                                    |   RW_OUTPUT
                                    |   RW_INPUT S_DIVIDE RW_OUTPUT
        """
        param_type = p[1] + p[2] + p[3] if len(p) == 4 else p[1]
        info = {'type': param_type}
        p[0] = AST("procedure_parameter_type", None, info)

    def p_function_declaration(self, p):
        """function_declaration :   function_identification function_formal_parameter_list function_return_type
                                |   function_identification function_return_type
        """
        children = [p[i] for i in range(1, len(p))]
        p[0] = AST("function_declaration", children)

    def p_function_identification(self, p):
        """function_identification  :   RW_FUNCTION identifier
        """
        p[0] = AST("function_identifier", [p[2]])

    def p_function_return_type(self, p):
        """function_return_type :   S_RETURN type_denoter
        """
        p[0] = AST("return_type", [p[2]])

    def p_function_formal_parameter_list(self, p):
        """function_formal_parameter_list   :   S_LEFT_BRACKET function_parameter_list_option S_RIGHT_BRACKET
        """
        p[0] = AST("function_parameter_declaration", [p[2]])

    def p_function_actual_parameter_list(self, p):
        """function_actual_parameter_list   :   S_LEFT_BRACKET actual_parameter_list S_RIGHT_BRACKET
        """
        p[0] = AST("function_actual_parameter", [p[2]])

    def p_function_parameter_list_option(self, p):
        """function_parameter_list_option   :   function_parameter_list
                                            |   empty
        """
        p[0] = p[1]

    def p_function_parameter_list(self, p):
        """function_parameter_list  :   function_parameter_list S_SEMI_COLON function_parameter_declaration
                                    |   function_parameter_declaration
        """
        if len(p) == 2:
            p[0] = AST("function_parameter_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("function_parameter_list", [*curr_children, p[3]])

    def p_function_parameter_declaration(self, p):
        """function_parameter_declaration   :   variable_sub_declaration
        """
        p[0] = AST("function_parameter", [p[1]])

    def p_statement_part(self, p):
        """statement_part   :   compound_statement
        """
        p[0] = p[1]

    def p_compound_statement(self, p):
        """compound_statement   :   INDENT  statement_sequence  DEDENT
        """
        p[0] = AST("compound_statement", [p[2]])

    def p_statement_sequence(self, p):
        """statement_sequence   :   statement_sequence S_SEMI_COLON statement
                                |   statement_sequence statement
                                |   statement
        """
        if len(p) == 2:
            p[0] = AST("statement_sequence", [p[1]])
        elif len(p) == 3:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("statement_sequence", [*curr_children, p[2]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("statement_sequence", [*curr_children, p[3]])

    def p_statement(self, p):
        """statement    : assignment_statement
                        | procedure_statement
                        | function_returned_statement
                        |   if_statement
                        | depend_on_statement
                        | while_statement
                        | traversal_statement
                        |   repeat_statement
                        |   iterate_stop_statement
        """
        p[0] = p[1]

    def p_assignment_statement(self, p):
        """assignment_statement :   variable_access S_ASSIGNMENT expression
        """
        p[0] = AST("assignment_statement", [p[1], p[3]])

    def p_procedure_statement(self, p):
        """procedure_statement :   input_output_procedure_statement
                                |   identifier S_LEFT_BRACKET actual_parameter_list S_RIGHT_BRACKET
                                |   identifier
        """
        if p[1].get_type() == "input_statement" or p[1].get_type() == "output_statement":
            p[0] = p[1]
        else:
            curr_children = [p[1]] if len(p) == 2 else [p[1], p[3]]
            p[0] = AST("procedure_statement", curr_children)

    def p_actual_parameter_list(self, p):
        """actual_parameter_list    :   actual_parameter_list S_COMMA actual_parameter
                                    |   actual_parameter
        """
        if len(p) == 2:
            p[0] = AST("actual_parameter_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("actual_parameter_list", [*curr_children, p[3]])

    def p_actual_parameter(self, p):
        """actual_parameter :   expression
        """
        p[0] = AST("actual_parameter", [p[1]])

    def p_input_output_procedure_statement(self, p):
        """input_output_procedure_statement :   input_statement
                                            |   output_statement
        """
        p[0] = p[1]

    def p_input_statement(self, p):
        """input_statement  :   RW_INPUT S_LEFT_BRACKET input_statement_parameter_list S_RIGHT_BRACKET
        """
        p[0] = AST("input_statement", [p[3]])

    def p_input_statement_parameter_list(self, p):
        """input_statement_parameter_list   :   input_statement_parameter_list S_COMMA input_statement_parameter
                                            |   input_statement_parameter
        """
        if len(p) == 2:
            p[0] = AST("input_statement_parameter_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("input_statement_parameter_list", [*curr_children, p[3]])

    def p_input_statement_parameter(self, p):
        """input_statement_parameter    :   variable_access
        """
        p[0] = AST("input_statement_parameter", [p[1]])

    def p_output_statement(self, p):
        """output_statement  :   RW_OUTPUT S_LEFT_BRACKET output_statement_parameter_list S_RIGHT_BRACKET
        """
        p[0] = AST("output_statement", [p[3]])

    def p_output_statement_parameter_list(self, p):
        """output_statement_parameter_list  :   output_statement_parameter_list S_COMMA output_statement_parameter
                                            |   output_statement_parameter
        """
        if len(p) == 2:
            p[0] = AST("output_statement_parameter_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("output_statement_parameter_list", [*curr_children, p[3]])

    def p_output_statement_parameter(self, p):
        """output_statement_parameter   :   expression
        """
        p[0] = AST("output_statement_parameter", [p[1]])

    def p_function_returned_statement(self, p):
        """function_returned_statement  :   S_RETURN expression
        """
        p[0] = AST("function_returned_statement", [p[2]])

    def p_depend_on_statement(self, p):
        """depend_on_statement  :   RW_DEPEND RW_ON S_LEFT_BRACKET input_statement_parameter_list S_RIGHT_BRACKET INDENT depend_on_action_list DEDENT
        """
        p[0] = AST("depend_on_statement", [p[4], p[7]])

    def p_depend_on_action_list(self, p):
        """depend_on_action_list    :   depend_on_action_list   depend_on_action
                                            |   depend_on_action
        """
        if len(p) == 2:
            p[0] = AST("depend_on_action_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("depend_on_action_list", [*curr_children, p[2]])

    def p_depend_on_action(self, p):
        """depend_on_action :   expression S_COLON INDENT statement_sequence DEDENT
        """
        p[0] = AST("depend_on_action", [p[1], p[4]])

    def p_if_statement(self, p):
        """if_statement : RW_IF boolean_expression RW_THEN compound_statement
                        | RW_IF boolean_expression RW_THEN compound_statement RW_ELSE compound_statement
        """
        if len(p) == 5:
            p[0] = AST("if_statement", [p[2], p[4]])
        else:
            p[0] = AST("if_statement", [p[2], p[4], p[6]])

    def p_boolean_expression(self, p):
        """boolean_expression   :   expression
        """
        p[0] = p[1]

    def p_repeat_statement(self, p):
        """repeat_statement :   repeat_until_statement
                            |   repeat_times_statement
        """
        p[0] = p[1]

    def p_repeat_until_statement(self, p):
        """repeat_until_statement   :   RW_REPEAT compound_statement RW_UNTIL boolean_expression
        """
        p[0] = AST("repeat_until_statement", [p[2], p[4]])

    def p_repeat_times_statement(self, p):
        """repeat_times_statement   :   RW_REPEAT variable_access RW_TIMES compound_statement
                                    |   RW_REPEAT integer_constant RW_TIMES compound_statement
                                    |   RW_REPEAT function_designator RW_TIMES compound_statement
        """
        p[0] = AST("repeat_times_statement", [p[2], p[4]])

    def p_while_statement(self, p):
        """while_statement   :   RW_WHILE boolean_expression RW_DO compound_statement
        """
        p[0] = AST("while_statement", [p[2], p[4]])

    def p_iterate_stop_statement(self, p):
        """iterate_stop_statement   :   RW_ITERATE compound_statement RW_STOP boolean_expression compound_statement
        """
        p[0] = AST("iterate_stop_statement", [p[2], p[4], p[5]])

    def p_traversal_statement(self, p):
        """traversal_statement  :   control_variable RW_TRAVERSAL traversal_range_value compound_statement
        """
        p[0] = AST("traversal_statement", [p[1], p[3], p[4]])

    def p_traversal_range_value(self, p):
        """traversal_range_value    :   S_LEFT_SQUARE_BRACKET subrange_type S_RIGHT_SQUARE_BRACKET
        """
        p[0] = AST("traversal_range_value", [p[2]])

    def p_control_variable(self, p):
        """control_variable :   identifier
        """
        p[0] = p[1]

    def p_unsigned_constant(self, p):
        """unsigned_constant :  non_string_constant
                            |   string_char_constant
                            |   boolean_constant
                            |   nil_constant
        """
        p[0] = AST("constant_value", [p[1]])

    def p_constant(self, p):
        """constant :   string_char_constant
                    |   non_string_constant
                    |   sign non_string_constant
                    |   boolean_constant
                    |   nil_constant
        """
        if len(p) == 2:
            p[0] = AST("constant_value", [p[1]])
        else:
            p[0] = AST("constant_value", [p[1], p[2]])

    def p_sign(self, p):
        """sign     :   S_PLUS
                    |   S_MINUS
        """
        info = {
            'value': p[1]
        }
        p[0] = AST("sign_operator", None, info)

    def p_boolean_constant(self, p):
        """boolean_constant :   L_BOOLEAN_TRUE
                            |   L_BOOLEAN_FALSE
        """
        info = {
            'value': p[1]
        }
        p[0] = AST("boolean_constant", None, info)

    def p_non_string_constant(self, p):
        """non_string_constant  :    integer_constant
                                |    real_constant
        """
        p[0] = p[1]

    def p_integer_constant(self, p):
        """integer_constant :   L_INTEGER_NUMBER
        """
        info = {'value': p[1]}
        p[0] = AST("integer_constant", None, info)

    def p_real_constant(self, p):
        """real_constant    :   L_REAL_NUMBER
        """
        info = {'value': p[1]}
        p[0] = AST("real_constant", None, info)

    def p_string_char_constant(self, p):
        """string_char_constant :   string_constant
                                |   char_constant
        """
        p[0] = p[1]

    def p_string_constant(self, p):
        """string_constant    :   L_STRING
        """
        info = {'value': p[1]}
        p[0] = AST("string_constant", None, info)

    def p_char_constant(self, p):
        """char_constant    :   L_CHARACTER
        """
        info = {'value': p[1]}
        p[0] = AST("character_constant", None, info)

    def p_nil_constant(self, p):
        """nil_constant :   L_NIL
        """
        info = {
            'value': p[1]
        }
        p[0] = AST("nil_constant", None, info)

    def p_variable_access(self, p):
        """variable_access : identifier
                            | indexed_variable
                            | field_designator
        """
        p[0] = AST("variable", [p[1]])

    def p_indexed_variable(self, p):
        """indexed_variable :   variable_access S_LEFT_SQUARE_BRACKET index_expression_list S_RIGHT_SQUARE_BRACKET
        """
        p[0] = AST("indexed_variable", [p[1], p[3]])

    def p_index_expression_list(self, p):
        """index_expression_list    :   index_expression_list S_COMMA expression
                                    |   expression
        """
        if len(p) == 2:
            p[0] = AST("index_expression_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("index_expression_list", [*curr_children, p[3]])

    def p_field_designator(self, p):
        """field_designator :   variable_access S_DOT identifier
        """
        p[0] = AST("field_designator", [p[1], p[3]])

    def p_expression(self, p):
        """expression : expression relational_op additive_expression
                    |   additive_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST("expression", [p[1], p[2], p[3]])

    def p_relational_op(self, p):
        """relational_op : S_EQUAL
                | S_NOT_EQUAL
                | S_LESS_THAN_EQUAL
                | S_GREATER_THAN_EQUAL
                | S_LESS_THAN
                | S_GREATER_THAN
                | S_ELEMENT_OF
                | RW_EQ
                | RW_NEQ
        """
        info = {
            'name': p[1]
        }
        p[0] = AST("operator", None, info)

    def p_additive_expression(self, p):
        """additive_expression : additive_expression additive_op multiplicative_expression
                            |   multiplicative_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST("additive_expression", [p[1], p[2], p[3]])

    def p_additive_op(self, p):
        """additive_op : S_PLUS
                    | S_MINUS
                    | RW_OR
                    | RW_XOR
        """
        info = {
            'name': p[1]
        }
        p[0] = AST("operator", None, info)

    def p_multiplicative_expression(self, p):
        """multiplicative_expression : multiplicative_expression multiplicative_op unary_expression
                                    |   unary_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST("multiplicative_expression", [p[1], p[2], p[3]])

    def p_multiplicative_op(self, p):
        """multiplicative_op : S_TIMES
                            | S_DIVIDE
                            | RW_DIV
                            | RW_MOD
                            | RW_AND
        """
        info = {
            'name': p[1]
        }
        p[0] = AST("operator", None, info)

    def p_unary_expression(self, p):
        """unary_expression : unary_op unary_expression
                        |   exponentiation_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST("unary_expression", [p[1], p[2]])

    def p_exponentiation_expression(self, p):
        """exponentiation_expression    :   primary_expression
                                        |   primary_expression S_POWER exponentiation_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST("exponentiation_expression", [p[1], p[3]])

    def p_unary_op(self, p):
        """unary_op : S_PLUS
            |   S_MINUS
            |   RW_NOT
        """
        info = {
            'name': p[1]
        }
        p[0] = AST("operator", None, info)

    def p_primary_expression(self, p):
        """primary_expression : variable_access
                            | unsigned_constant
                            | S_LEFT_BRACKET expression S_RIGHT_BRACKET
                            | set_constructor
                            | function_designator
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_set_constructor(self, p):
        """set_constructor  :   S_LEFT_SQUARE_BRACKET member_designator_list S_RIGHT_SQUARE_BRACKET
                            |   S_LEFT_SQUARE_BRACKET S_RIGHT_SQUARE_BRACKET
        """
        if len(p) == 4:
            p[0] = AST("set_constructor", [p[2]])

    def p_member_designator_list(self, p):
        """member_designator_list   :   member_designator_list  S_COMMA member_designator
                                    |   member_designator
        """
        if len(p) == 2:
            p[0] = AST("member_designator_list", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("member_designator_list", [*curr_children, p[3]])

    def p_member_designator(self, p):
        """member_designator    :   member_designator S_UP_TO   expression
                                |   expression
        """
        if len(p) == 2:
            p[0] = AST("member_designator", [p[1]])
        else:
            curr_children = [] if p[1] is None else p[1].get_children_or_itself()
            p[0] = AST("member_designator", [*curr_children, p[3]])

    def p_function_designator(self, p):
        """function_designator  :    user_defined_function_call
                                |   math_function_call
                                |   string_function_call
                                |   converter_function_call
        """
        p[0] = p[1]

    def p_user_defined_function_call(self, p):
        """user_defined_function_call    :   identifier function_actual_parameter_list
        """
        p[0] = AST("user_defined_function_call", [p[1], p[2]])

    def p_math_function_call(self, p):
        """math_function_call   :   abs_function
                                |   sin_function
                                |   cos_function
                                |   tan_function
                                |   succ_function
                                |   pred_function
        """
        p[0] = AST("math_function_call", [p[1]])

    def p_abs_function(self, p):
        """abs_function : RW_ABS S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("abs_function", [p[3]])

    def p_sin_function(self, p):
        """sin_function :   RW_SIN S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("sin_function", [p[3]])

    def p_cos_function(self, p):
        """cos_function :   RW_COS S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("cos_function", [p[3]])

    def p_tan_function(self, p):
        """tan_function :   RW_TAN S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("tan_function", [p[3]])

    def p_succ_function(self, p):
        """succ_function    :   RW_SUCC S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("succ_function", [p[3]])

    def p_pred_function(self, p):
        """pred_function    :   RW_PRED S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("pred_function", [p[3]])

    def p_string_function_call(self, p):
        """string_function_call :   awal_function
                                |   akhir_function
                                |   firstchar_function
                                |   lastchar_function
                                |   long_function
                                |   iskosong_function
        """
        p[0] = AST("string_function_call", [p[1]])

    def p_awal_function(self, p):
        """awal_function    :   RW_AWAL S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("awal_function", [p[3]])

    def p_akhir_function(self, p):
        """akhir_function    :   RW_AKHIR S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("akhir_function", [p[3]])

    def p_firstchar_function(self, p):
        """firstchar_function    :   RW_FIRSTCHAR S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("firstchar_function", [p[3]])

    def p_lastchar_function(self, p):
        """lastchar_function    :   RW_LASTCHAR S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("lastchar_function", [p[3]])

    def p_long_function(self, p):
        """long_function    :   RW_LONG S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("long_function", [p[3]])

    def p_iskosong_function(self, p):
        """iskosong_function    :   RW_ISKOSONG S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("iskosong_function", [p[3]])

    def p_converter_function_call(self, p):
        """converter_function_call  :   integer_to_real
                                    |   real_to_integer
        """
        p[0] = AST("converter_function_call", [p[1]])

    def p_integer_to_real(self, p):
        """integer_to_real  :   RW_INTEGERTOREAL S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("integer_to_real_converter", [p[3]])

    def p_real_to_integer(self, p):
        """real_to_integer  :   RW_REALTOINTEGER S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """
        p[0] = AST("real_to_integer_converter", [p[3]])

    def p_error(self, p):
        raise Exception(f"Syntax error at token: {p}")

    def p_empty(self, p):
        """empty    :
        """
        pass

    def p_identifier(self, p):
        """identifier   :   IDENTIFIER
        """
        info = {
            'identifier_name': p[1]
        }
        p[0] = AST("identifier", None, info)

    def __init__(self):
        self.parser = yacc.yacc(module=self)

    def get_cleaner_source(self, source):
        return re.sub(r"\n{2,}", "\n", source)

    def parse(self, source):
        source = self.get_cleaner_source(source)

        lexer = NotalScanner()
        lexer = IndentLexer(lexer)

        return self.parser.parse(source, lexer)
