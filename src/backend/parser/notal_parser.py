import ply.yacc as yacc
import re
from src.backend.scanner.notal_scanner import NotalScanner, IndentLexer


class NotalParser(object):
    tokens = NotalScanner.tokens
    start = 'file'

    def p_file(self, p):
        """file :   program
        """

    def p_program(self, p):
        """program  :   RW_PROGRAM IDENTIFIER block
        """

    def p_identifier_list(self, p):
        """identifier_list  : identifier_list S_COMMA IDENTIFIER
                            | IDENTIFIER
        """

    def p_block(self, p):
        """block    :   RW_KAMUS INDENT block_1
        """

    def p_block_1(self, p):
        """block_1  :   block_2
                    |   constant_declaration block_2
        """

    def p_block_2(self, p):
        """block_2  :   block_3
                    |   type_declaration block_3
        """

    def p_block_3(self, p):
        """block_3  :   block_4
                    |    variable_declaration block_4
        """

    def p_block_4(self, p):
        """block_4  :   DEDENT block_5
                    |   procedure_and_function_declaration DEDENT block_5
        """

    def p_block_5(self, p):
        """block_5  :   RW_ALGORITMA statement_part
        """

    def p_type_denoter(self, p):
        """type_denoter :   IDENTIFIER
                        |   ordinal_type
                        |   structured_type
                        |   RW_INTEGER
                        |   RW_REAL
                        |   RW_STRING
                        |   RW_CHARACTER
                        |   RW_BOOLEAN
        """

    def p_ordinal_type(self, p):
        """ordinal_type :   enumerated_type
                        |   subrange_type
        """

    def p_enumerated_type(self, p):
        """enumerated_type  :   S_LEFT_BRACKET identifier_list S_RIGHT_BRACKET
        """

    def p_subrange_type(self, p):
        """subrange_type    :   constant S_UP_TO constant
        """

    def p_structured_type(self, p):
        """structured_type  :   array_type
        """

    def p_array_type(self, p):
        """array_type   :   RW_ARRAY S_LEFT_SQUARE_BRACKET index_list S_RIGHT_SQUARE_BRACKET RW_OF component_type
        """

    def p_index_list(self, p):
        """index_list   :   index_list S_COMMA index_type
                        |   index_type
        """

    def p_index_type(self, p):
        """index_type   :   ordinal_type
                        |   IDENTIFIER
        """

    def p_component_type(self, p):
        """component_type   :   type_denoter"""

    def p_variable_declaration(self, p):
        """variable_declaration :  variable_declaration variable_sub_declaration
                                |   variable_sub_declaration
        """

    def p_variable_sub_declaration(self, p):
        """variable_sub_declaration :   identifier_list S_COLON type_denoter
        """

    def p_variable_declaration_comma(self, p):
        """variable_declaration_comma   :   variable_sub_declaration
                                        |   variable_sub_declaration S_COMMA variable_declaration_comma
        """

    def p_constant_declaration(self, p):
        """constant_declaration :   constant_declaration constant_sub_declaration
                                |   constant_sub_declaration
        """

    def p_constant_sub_declaration(self, p):
        """constant_sub_declaration :   RW_CONSTANT IDENTIFIER S_COLON type_denoter S_EQUAL constant
        """

    def p_type_declaration(self, p):
        """type_declaration :   type_declaration type_sub_declaration
                            |   type_sub_declaration
        """

    def p_type_sub_declaration(self, p):
        """type_sub_declaration :   RW_TYPE IDENTIFIER S_COLON type_variety
        """

    def p_type_variety(self, p):
        """type_variety :   type_denoter
                        |   type_user_defined
        """

    def p_type_user_defined(self, p):
        """type_user_defined    :   S_LESS_THAN variable_declaration_comma S_GREATER_THAN
        """

    def p_procedure_and_function_declaration(self, p):
        """procedure_and_function_declaration   :   procedure_and_function_declaration procedure_and_function_sub_declaration
                                                |   procedure_and_function_sub_declaration
        """

    def p_procedure_and_function_sub_declaration(self, p):
        """procedure_and_function_sub_declaration   :   procedure_declaration
                                                    |   function_declaration
        """

    def p_procedure_declaration(self, p):
        """procedure_declaration    :  procedure_identification formal_parameter_list
        """

    def p_procedure_identification(self, p):
        """procedure_identification :   RW_PROCEDURE IDENTIFIER
        """

    def p_formal_parameter_list(self, p):
        """formal_parameter_list    :   S_LEFT_BRACKET formal_parameter_section_list S_RIGHT_BRACKET
        """

    def p_formal_parameter_section_list(self, p):
        """formal_parameter_section_list    :   empty
                                            |   formal_parameter_section
        """

    def p_formal_parameter_section(self, p):
        """formal_parameter_section :   parameter_specification S_SEMI_COLON formal_parameter_section
                                    |   parameter_specification
        """

    def p_parameter_specification(self, p):
        """parameter_specification  :   procedure_parameter_type  variable_sub_declaration
        """

    def p_procedure_parameter_type(self, p):
        """procedure_parameter_type :   RW_INPUT
                                    |   RW_OUTPUT
                                    |   RW_INPUT S_DIVIDE RW_OUTPUT
        """

    def p_function_declaration(self, p):
        """function_declaration :   function_identification function_formal_parameter_list function_return_type
                                |   function_identification function_return_type
        """

    def p_function_identification(self, p):
        """function_identification  :   RW_FUNCTION IDENTIFIER
        """

    def p_function_return_type(self, p):
        """function_return_type :   S_RETURN type_denoter
        """

    def p_function_formal_parameter_list(self, p):
        """function_formal_parameter_list   :   S_LEFT_BRACKET function_parameter_list_option S_RIGHT_BRACKET
        """

    def p_function_parameter_list_option(self, p):
        """function_parameter_list_option   :   function_parameter_list
                                            |   empty
        """

    def p_function_parameter_list(self, p):
        """function_parameter_list  :   function_parameter_declaration S_SEMI_COLON function_parameter_list
                                    |   function_parameter_declaration
        """

    def p_function_parameter_declaration(self, p):
        """function_parameter_declaration   :   variable_sub_declaration
        """

    def p_statement_part(self, p):
        """statement_part   :   compound_statement
        """

    def p_compound_statement(self, p):
        """compound_statement   :   INDENT  statement_sequence  DEDENT
        """

    def p_statement_sequence(self, p):
        """statement_sequence   :   statement_sequence S_SEMI_COLON statement
                                |   statement_sequence statement
                                |   statement
        """

    def p_statement(self, p):
        """statement    :   simple_statement
                        |   structured_statement
        """

    def p_simple_statement(self, p):
        """simple_statement :   assignment_statement
                            |   procedure_statement
                            |   simple_if_statement
                            |   simple_while_statement
        """

    def p_assignment_statement(self, p):
        """assignment_statement :   variable_access S_ASSIGNMENT expression
        """

    def p_procedure_statement(self, p):
        """procedure_statement :   input_output_procedure_statement
                                |   IDENTIFIER S_LEFT_BRACKET actual_parameter_list S_RIGHT_BRACKET
                                |   IDENTIFIER
        """

    def p_actual_parameter_list(self, p):
        """actual_parameter_list    :   actual_parameter_list S_COMMA actual_parameter
                                    |   actual_parameter
        """

    def p_actual_parameter(self, p):
        """actual_parameter :   expression
        """

    def p_input_output_procedure_statement(self, p):
        """input_output_procedure_statement :   input_statement
                                            |   output_statement
        """

    def p_input_statement(self, p):
        """input_statement  :   RW_INPUT S_LEFT_BRACKET input_statement_parameter_list S_RIGHT_BRACKET
        """

    def p_input_statement_parameter_list(self, p):
        """input_statement_parameter_list   :   input_statement_parameter_list S_COMMA variable_access
                                            |   variable_access
        """

    def p_output_statement(self, p):
        """output_statement  :   RW_OUTPUT S_LEFT_BRACKET output_statement_parameter_list S_RIGHT_BRACKET
        """

    def p_output_statement_parameter_list(self, p):
        """output_statement_parameter_list  :   output_statement_parameter_list S_COMMA output_statement_parameter
                                            |   output_statement_parameter
        """

    def p_output_statement_parameter(self, p):
        """output_statement_parameter   :   expression
        """

    # TODO: ADD DEPEND ON statement
    def p_structured_statement(self, p):
        """structured_statement :   compound_statement
                                |   structured_if_statement
                                |   repeat_statement
                                |   structured_while_statement
        """

    def p_structured_if_statement(self, p):
        """structured_if_statement  : RW_IF boolean_expression RW_THEN structured_statement RW_ELSE structured_statement
        """

    def p_simple_if_statement(self, p):
        """simple_if_statement  :   RW_IF boolean_expression RW_THEN statement
                                |   RW_IF boolean_expression RW_THEN structured_statement RW_ELSE simple_statement
        """

    def p_boolean_expression(self, p):
        """boolean_expression   :   expression
        """

    def p_repeat_statement(self, p):
        """repeat_statement :   repeat_until_statement
                            |   repeat_times_statement
        """

    def p_repeat_until_statement(self, p):
        """repeat_until_statement   :   RW_REPEAT statement_sequence RW_UNTIL boolean_expression
        """

    def p_repeat_times_statement(self, p):
        """repeat_times_statement   :   RW_REPEAT IDENTIFIER RW_TIMES structured_statement
        """

    def p_structured_while_statement(self, p):
        """structured_while_statement   :   RW_WHILE boolean_expression RW_DO structured_statement
        """

    def p_simple_while_statement(self, p):
        """simple_while_statement   :   RW_WHILE boolean_expression RW_DO simple_statement
        """

    def p_unsigned_constant(self, p):
        """unsigned_constant :  non_string_constant
                            |   string_char_constant
                            |   boolean_constant
                            |   L_NIL
        """

    def p_constant(self, p):
        """constant :   string_char_constant
                    |   non_string_constant
                    |   sign non_string_constant
                    |   boolean_constant
                    |   L_NIL
        """

    def p_sign(self, p):
        """sign     :   S_PLUS
                    |   S_MINUS
        """

    def p_boolean_constant(self, p):
        """boolean_constant :   L_BOOLEAN_TRUE
                            |   L_BOOLEAN_FALSE
        """

    def p_non_string_constant(self, p):
        """non_string_constant  :    L_INTEGER_NUMBER
                                |    L_REAL_NUMBER
        """

    def p_string_char_constant(self, p):
        """string_char_constant :   L_STRING
                                |   L_CHARACTER
        """

    def p_variable_access(self, p):
        """variable_access : IDENTIFIER
                            | indexed_variable
                            | field_designator
        """

    def p_indexed_variable(self, p):
        """indexed_variable :   variable_access S_LEFT_SQUARE_BRACKET index_expression_list S_RIGHT_SQUARE_BRACKET
        """

    def p_index_expression_list(self, p):
        """index_expression_list    :   index_expression_list S_COMMA expression
                                    |   expression
        """

    def p_field_designator(self, p):
        """field_designator :   variable_access S_DOT IDENTIFIER
        """

    def p_expression(self, p):
        """expression : expression relational_op additive_expression
                    |   additive_expression
        """

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

    def p_additive_expression(self, p):
        """additive_expression : additive_expression additive_op multiplicative_expression
                            |   multiplicative_expression
        """

    def p_additive_op(self, p):
        """additive_op : S_PLUS
                    | S_MINUS
                    | RW_OR
                    | RW_XOR
        """

    def p_multiplicative_expression(self, p):
        """multiplicative_expression : multiplicative_expression multiplicative_op unary_expression
                                    |   unary_expression
        """

    def p_multiplicative_op(self, p):
        """multiplicative_op : S_TIMES
                            | S_DIVIDE
                            | RW_DIV
                            | RW_MOD
                            | RW_AND
        """

    def p_unary_expression(self, p):
        """unary_expression : unary_op unary_expression
                        |   exponentiation_expression
        """

    def p_exponentiation_expression(self, p):
        """exponentiation_expression    :   primary_expression
                                        |   primary_expression S_POWER exponentiation_expression
        """

    def p_unary_op(self, p):
        """unary_op : S_PLUS
            |   S_MINUS
            |   RW_NOT
        """

    # TODO: Add other necessary rule (related to function)
    def p_primary_expression(self, p):
        """primary_expression : variable_access
                            | unsigned_constant
                            | S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """

    def p_error(self, p):
        print("Syntax error on token: ", p)
        exit()

    def p_empty(self, p):
        """empty    :
        """
        pass

    def __init__(self):
        self.lexer = NotalScanner()
        self.lexer = IndentLexer(self.lexer)
        self.parser = yacc.yacc(module=self)

    def get_cleaner_source(self, source):
        return re.sub(r"\n{2,}", "\n", source)

    def parse(self, source):
        self.source = self.get_cleaner_source(source)
        return "Parsing Success!" if (self.parser.parse(self.source, self.lexer) is None) else "Parsing failed!"