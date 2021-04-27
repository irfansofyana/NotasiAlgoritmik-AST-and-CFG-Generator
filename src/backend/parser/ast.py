class AST:
    def __init__(self, type=None, children=None, info=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.info = info

    def get_ast_in_json(self):
        ast = {
            "type": self.type,
            "info": self.info
        }
        if len(self.children) == 0:
            return ast

        ast['children'] = []
        for child in self.children:
            if child:
                ast_child = child.get_ast_in_json()
                ast['children'].append(ast_child)
        return ast

    def get_children(self):
        return self.children

    def get_children_or_itself(self):
        if len(self.children) > 0:
            return self.get_children()
        else:
            return [self]

    def get_type(self):
        return self.type

    def get_info(self):
        return self.info
