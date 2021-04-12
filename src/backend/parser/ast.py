class AST:
    def __init__(self, type, children=None, parent=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.parent = parent

    def get_ast_in_json(self):
        ast = {
            "type": self.type,
            "parent": self.parent
        }
        if len(self.children) == 0:
            return ast

        ast['children'] = []
        for child in self.children:
            if child:
                ast_child = child.get_ast_in_json()
                ast['children'].append(ast_child)
        return ast
