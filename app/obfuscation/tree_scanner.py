import ast


class TreeScanner(ast.NodeVisitor):

    def __init__(self, *args, **kwargs):

        super(TreeScanner, self).__init__(*args, **kwargs)

        self.functions_names = set()
        self.classes_names = set()
        self.all_names = set()

    def visit_Module(self, node):

        self.root = node
        self.generic_visit(node)

    def visit_FunctionDef(self, node):

        self.functions_names.add(node.name)
        self.all_names.add(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):

        self.classes_names.add(node.name)
        self.all_names.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.ctx == ast.Store:
            self.all_names.add(node.id)
