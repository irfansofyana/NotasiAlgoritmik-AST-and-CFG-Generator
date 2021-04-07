import ply.yacc as yacc
from src.backend.scanner.notal_scanner import NotalScanner


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
        """block    :   RW_KAMUS block_1
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
        """block_4  :   block_5
                    |   procedure_and_function_declaration block_5
        """

    def p_block_5(self, p):
        """block_5  :   RW_ALGORITMA statement_list
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
        """procedure_declaration    :   RW_PROCEDURE IDENTIFIER
                                    |   RW_PROCEDURE IDENTIFIER S_LEFT_BRACKET procedure_parameter_list_option S_RIGHT_BRACKET
        """

    def p_procedure_parameter_list_option(self, p):
        """procedure_parameter_list_option  :   procedure_parameter_list
                                            |   empty
        """

    def p_procedure_parameter_list(self, p):
        """procedure_parameter_list :   procedure_parameter_declaration S_SEMI_COLON procedure_parameter_list
                                    |   procedure_parameter_declaration
        """

    def p_procedure_parameter_declaration(self, p):
        """procedure_parameter_declaration  :   procedure_parameter_type  variable_sub_declaration
        """

    def p_procedure_parameter_type(self, p):
        """procedure_parameter_type :   RW_INPUT
                                    |   RW_OUTPUT
                                    |   RW_INPUT S_DIVIDE RW_OUTPUT
        """

    def p_function_declaration(self, p):
        """function_declaration :   RW_FUNCTION IDENTIFIER S_LEFT_BRACKET function_parameter_list_option S_RIGHT_BRACKET S_RETURN type_denoter
                                |   RW_FUNCTION IDENTIFIER S_RETURN type_denoter
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

    def p_statement_list(self, p):
        """statement_list   :   empty
        """

    def p_unsigned_constant(self, p):
        """unsigned_constant :  numerical_constant
                            |   string_char_constant
                            |   boolean_constant
                            |   L_NIL
        """

    def p_constant(self, p):
        """constant :   string_char_constant
                    |   numerical_constant
                    |   sign numerical_constant
                    |   boolean_constant
                    |   variable
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

    def p_numerical_constant(self, p):
        """numerical_constant  :   L_INTEGER_NUMBER
                                |   L_REAL_NUMBER
        """

    def p_string_char_constant(self, p):
        """string_char_constant :   L_STRING
                                |   L_CHARACTER
        """

    def p_variable(self, p):
        """variable : IDENTIFIER
                    | variable S_DOT field_id
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

    def p_primary_expression(self, p):
        """primary_expression : variable
                            | unsigned_constant
                            | S_LEFT_BRACKET expression S_RIGHT_BRACKET
        """

    def p_field_id(self, p):
        """field_id : IDENTIFIER
        """

    def p_error(self, p):
        print(p)
        print("Syntax error on input!")

    def p_empty(self, p):
        """empty    :
        """
        pass

    def __init__(self):
        self.lexer = NotalScanner()
        self.parser = yacc.yacc(module=self)

    def parse(self, source):
        self.source = source
        return self.parser.parse(source)