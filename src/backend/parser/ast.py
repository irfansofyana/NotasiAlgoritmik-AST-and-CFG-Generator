class AST:
    def __init__(self, type, children=None, parent=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.parent = parent


def get_ast_in_json(node):
    ast = {
        "type": node.type,
        "parent": node.parent
    }
    if len(node.children) == 0:
        return ast

    ast['children'] = []
    for child in node.children:
        ast_child = get_ast_in_json(child)
        ast['children'].append(ast_child)
    return ast
