from src.backend.cfg_generator.cfg import *


class CFGGenerator:
    label = 0
    subprograms_ast = None
    visited_subprograms_ast = {}

    def __init__(self, algorithm_block_ast):
        # ast -> ASTParser, cfg -> CFG
        self.state = algorithm_block_ast
        self.cfg = None

        self.build_cfg()

    def get_cfg(self):
        return self.cfg

    def build_cfg(self):
        f = getattr(self, 'build_from_' + self.state.get_type())
        return f()

    def build_from_algorithm_block(self):
        children = self.state.get_children()
        child_builder = CFGGenerator(children[0])
        self.cfg = child_builder.get_cfg()

    def build_from_compound_statement(self):
        children = self.state.get_children()
        child_builder = CFGGenerator(children[0])
        self.cfg = child_builder.get_cfg()

    def build_from_statement_sequence(self):
        statements = self.state.get_children()
        for i in range(0, len(statements)):
            child = CFGGenerator(statements[i])
            if i == 0:
                self.cfg = child.get_cfg()
            else:
                self.cfg.merge_cfg(child.get_cfg())

    def get_label_now(self):
        self.__class__.label += 1
        return self.__class__.label

    @staticmethod
    def get_all_function_calls(expression_ast):
        if expression_ast.get_type() == "user_defined_function_call":
            function_call = expression_ast.get_notal_src()
            return [function_call]
        if len(expression_ast.get_children()) == 0:
            return []
        function_calls = []
        for child in expression_ast.get_children():
            target_block = CFGGenerator.get_all_function_calls(child)
            function_calls += [*target_block]
        return function_calls

    def connect_to_function_cfg(self, parent_node, expression_ast):
        function_calls = CFGGenerator.get_all_function_calls(expression_ast)

        for function_call in function_calls:
            function_name = self.get_subprogram_name(function_call)

            if 'function ' + function_name not in CFGGenerator.visited_subprograms_ast:
                if CFGGenerator.subprograms_ast is None:
                    raise Exception(f"Function {function_name} can't be found")
                if 'function ' + function_name not in CFGGenerator.subprograms_ast['function']:
                    raise Exception(f"Function {function_name} can't be found")
                function_declaration = CFGGenerator.subprograms_ast['function']['function ' + function_name][0]
                function_ast = CFGGenerator.subprograms_ast['function']['function ' + function_name][1]
                start_function_node = CFGNode(self.get_label_now(), [f'start: {function_declaration}'])
                end_function_node = CFGNode(self.get_label_now(), [f'end: {function_declaration}'])

                CFGGenerator.visited_subprograms_ast['function ' + function_name] = (
                    start_function_node,
                    end_function_node
                )

                function_cfg_generator = CFGGenerator(function_ast)
                function_cfg = function_cfg_generator.get_cfg()

                parent_node.add_adjacent(start_function_node)
                start_function_node.add_adjacent(function_cfg.get_entry_block())

                function_exit_blocks = function_cfg.get_exit_block()
                for exit_block in function_exit_blocks:
                    exit_block.add_adjacent(end_function_node)
                end_function_node.add_adjacent(parent_node)
            else:
                start_function_node, end_function_node = CFGGenerator.visited_subprograms_ast['function ' + function_name]
                parent_node.add_adjacent(start_function_node)
                end_function_node.add_adjacent(parent_node)

    def build_from_assignment_statement(self):
        children = self.state.get_children()
        expression = children[1]

        node_label = self.get_label_now()
        info = [self.state.get_notal_src()]
        node = CFGNode(node_label, info)

        self.connect_to_function_cfg(node, expression)
        self.cfg = CFG(node, [node])

    def build_from_function_returned_statement(self):
        children = self.state.get_children()
        expression = children[0]

        node_label = self.get_label_now()
        info = [self.state.get_notal_src()]
        node = CFGNode(node_label, info)

        self.connect_to_function_cfg(node, expression)
        self.cfg = CFG(node, [node])

    @staticmethod
    def get_subprogram_name(subprogram_call):
        open_bracket_pos = subprogram_call.find('(')
        if open_bracket_pos == -1:
            return subprogram_call
        return subprogram_call[:open_bracket_pos]

    def build_from_procedure_statement(self):
        children = self.state.get_children()
        if len(children) > 1:
            expression = children[1]
        else:
            expression = None

        node_label = self.get_label_now()
        info = [self.state.get_notal_src()]
        procedure_name = self.get_subprogram_name(self.state.get_notal_src())

        node = CFGNode(node_label, info)

        # Handle function call
        if expression is not None:
            self.connect_to_function_cfg(node, expression)

        # Subprogram_cfg
        if 'procedure ' + procedure_name not in CFGGenerator.visited_subprograms_ast:
            if CFGGenerator.subprograms_ast is None:
                raise Exception(f"Procedure {procedure_name} can't be found")
            if 'procedure ' + procedure_name not in CFGGenerator.subprograms_ast['procedure']:
                raise Exception(f"Procedure {procedure_name} can't be found")
            subprogram_declaration = CFGGenerator.subprograms_ast['procedure']['procedure ' + procedure_name][0]
            subprogram_ast = CFGGenerator.subprograms_ast['procedure']['procedure ' + procedure_name][1]
            start_procedure_node = CFGNode(self.get_label_now(), [f'start: {subprogram_declaration}'])
            end_procedure_node = CFGNode(self.get_label_now(), [f'end: {subprogram_declaration}'])

            CFGGenerator.visited_subprograms_ast['procedure ' + procedure_name] = (
                start_procedure_node,
                end_procedure_node
            )

            subprogram_generator = CFGGenerator(subprogram_ast)
            subprogram_cfg = subprogram_generator.get_cfg()

            node.add_adjacent(start_procedure_node)
            start_procedure_node.add_adjacent(subprogram_cfg.get_entry_block())

            subprogram_exit_blocks = subprogram_cfg.get_exit_block()
            for exit_block in subprogram_exit_blocks:
                exit_block.add_adjacent(end_procedure_node)
            end_procedure_node.add_adjacent(node)

        else:
            start_procedure_node, end_procedure_node = CFGGenerator.visited_subprograms_ast['procedure ' + procedure_name]
            node.add_adjacent(start_procedure_node)
            end_procedure_node.add_adjacent(start_procedure_node)

        self.cfg = CFG(node, [node])

    def build_from_output_statement(self):
        children = self.state.get_children()
        expression = children[0]

        node_label = self.get_label_now()
        info = [self.state.get_notal_src()]
        node = CFGNode(node_label, info)

        self.connect_to_function_cfg(node, expression)
        self.cfg = CFG(node, [node])

    def build_from_input_statement(self):
        node_label = self.get_label_now()
        info = [self.state.get_notal_src()]
        node = CFGNode(node_label, info)
        self.cfg = CFG(node, [node])

    @staticmethod
    def get_boolean_expression(parent_statement, ast):
        expression = ast.get_notal_src()
        boolean_expression = f'{parent_statement} ({expression})'
        return boolean_expression

    def build_from_if_statement(self):
        children = self.state.get_children()
        if len(children) == 3:
            self.build_from_if_else_statement()
            return

        # conditional node
        expression = children[0]
        node_label = self.get_label_now()
        info = [self.get_boolean_expression('if', expression)]
        node = CFGNode(node_label, info)

        # Handle function call
        self.connect_to_function_cfg(node, expression)
        self.cfg = CFG(node, [node])

        # statement nodes
        child = CFGGenerator(children[1])
        cfg_child = child.get_cfg()

        # merge the cfg
        self.cfg.merge_cfg(cfg_child)
        self.cfg.add_exit_block(node)

    def build_from_if_else_statement(self):
        children = self.state.get_children()

        # conditional node
        node_label = self.get_label_now()
        expression = children[0]
        info = [self.get_boolean_expression('if', expression)]
        node = CFGNode(node_label, info)

        # Handle function call
        self.connect_to_function_cfg(node, expression)

        # first statement nodes
        first_child = CFGGenerator(children[1])
        first_cfg_child = first_child.get_cfg()

        # second statement nodes
        second_child = CFGGenerator(children[2])
        second_cfg_child = second_child.get_cfg()

        # connect conditional node to first statement
        node.add_adjacent(first_cfg_child.get_entry_block())
        node.add_adjacent(second_cfg_child.get_entry_block())

        # Build the CFG
        self.cfg = CFG(node, [*first_cfg_child.get_exit_block(), *second_cfg_child.get_exit_block()])

    @staticmethod
    def get_depend_on_info(ast):
        return "DEPEND ON (" + ast.get_notal_src() + ")"

    def build_from_depend_on_statement(self):
        children = self.state.get_children()

        # depend on node
        node_label = self.get_label_now()
        info = [self.get_depend_on_info(children[0])]
        node = CFGNode(node_label, info)

        # depend on action list
        depend_on_actions = children[1].get_children()
        exit_blocks = []

        for i in range(len(depend_on_actions)):
            cfg_child = CFGGenerator(depend_on_actions[i]).get_cfg()
            exit_blocks += [*cfg_child.get_exit_block()]
            node.add_adjacent(cfg_child.get_entry_block())

        self.cfg = CFG(node, exit_blocks)

    @staticmethod
    def get_depend_on_action_expression(ast):
        return ast.get_notal_src()

    def build_from_depend_on_action(self):
        children = self.state.get_children()

        # expression node
        node_label = self.get_label_now()
        expression = children[0]
        info = [self.get_depend_on_action_expression(expression)]
        node = CFGNode(node_label, info)

        # Handle function call
        self.connect_to_function_cfg(node, expression)
        self.cfg = CFG(node, [node])

        # statement nodes
        child = CFGGenerator(children[1])
        cfg_child = child.get_cfg()

        # merge the cfg
        self.cfg.merge_cfg(cfg_child)

    def build_from_while_statement(self):
        children = self.state.get_children()

        # while conditional node
        node_label = self.get_label_now()
        expression = children[0]
        info = [self.get_boolean_expression('while', expression)]
        node = CFGNode(node_label, info)

        # Handle function call
        self.connect_to_function_cfg(node, expression)

        # statement nodes
        child = CFGGenerator(children[1])
        cfg_child = child.get_cfg()

        # connect while conditional node to statement nodes
        node.add_adjacent(cfg_child.get_entry_block())
        for exit_block in cfg_child.get_exit_block():
            exit_block.add_adjacent(node)

        # build the cfg
        self.cfg = CFG(node, [node])

    def build_from_repeat_until_statement(self):
        children = self.state.get_children()

        # statement nodes
        child = CFGGenerator(children[0])
        cfg_child = child.get_cfg()

        # until statement
        node_label = self.get_label_now()
        expression = children[1]
        info = [self.get_boolean_expression('until', expression)]
        node = CFGNode(node_label, info)

        # connect statement nodes to until node
        for exit_block in cfg_child.get_exit_block():
            exit_block.add_adjacent(node)
        node.add_adjacent(cfg_child.get_entry_block())

        # Handle function call
        self.connect_to_function_cfg(node, expression)

        # build the CFG
        self.cfg = CFG(cfg_child.get_entry_block(), [node])

    @staticmethod
    def get_traversal_statement_info(control_variable, range_value):
        control_variable = control_variable.get_notal_src()
        range_value = range_value.get_notal_src()
        info = f'{control_variable} traversal {range_value}'
        return info

    def build_from_traversal_statement(self):
        children = self.state.get_children()
        info = [self.get_traversal_statement_info(children[0], children[1])]

        # traversal node
        node_label = self.get_label_now()
        node = CFGNode(node_label, info)

        # statement nodes
        child = CFGGenerator(children[2])
        cfg_child = child.get_cfg()

        # connect traversal conditional node to statement nodes
        node.add_adjacent(cfg_child.get_entry_block())
        for exit_block in cfg_child.get_exit_block():
            exit_block.add_adjacent(node)

        # Handle function call
        self.connect_to_function_cfg(node, children[1])

        # build the cfg
        self.cfg = CFG(node, [node])

    @staticmethod
    def get_repeat_times_info(var):
        var = var.get_notal_src()
        info = f'repeat {var} times'
        return info

    def build_from_repeat_times_statement(self):
        children = self.state.get_children()

        # repeat node
        node_label = self.get_label_now()
        info = [self.get_repeat_times_info(children[0])]
        node = CFGNode(node_label, info)

        # Handle function call
        self.connect_to_function_cfg(node, children[0])

        # statement nodes
        child = CFGGenerator(children[1])
        cfg_child = child.get_cfg()

        # connect repeat node to its statement nodes
        node.add_adjacent(cfg_child.get_entry_block())
        for exit_block in cfg_child.get_exit_block():
            exit_block.add_adjacent(node)
        self.cfg = CFG(node, [node])

    def build_from_iterate_stop_statement(self):
        children = self.state.get_children()

        # first action nodes
        child = CFGGenerator(children[0])
        cfg_child = child.get_cfg()

        # conditional node
        node_label = self.get_label_now()
        info = [self.get_boolean_expression('stop', children[1])]
        node = CFGNode(node_label, info)

        # Handle function call
        self.connect_to_function_cfg(node, children[1])

        # second action nodes
        child_2 = CFGGenerator(children[2])
        cfg_child_2 = child_2.get_cfg()

        # connecting the nodes
        for exit_node in cfg_child.get_exit_block():
            exit_node.add_adjacent(node)
        node.add_adjacent(cfg_child_2.get_entry_block())
        for exit_node in cfg_child_2.get_exit_block():
            exit_node.add_adjacent(cfg_child.get_entry_block())

        self.cfg = CFG(cfg_child.get_entry_block(), [node])
