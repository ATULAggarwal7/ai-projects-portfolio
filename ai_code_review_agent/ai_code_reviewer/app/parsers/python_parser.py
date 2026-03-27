import ast


class PythonParser:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)

        self.structure = {
            "functions": [],
            "classes": [],
            "globals": []
        }

    def parse(self):
        self._extract_globals()
        self._extract_functions_and_classes()
        return self.structure

    # -------------------------------
    # GLOBAL VARIABLES
    # -------------------------------
    def _extract_globals(self):
        for node in self.tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.structure["globals"].append(target.id)

    # -------------------------------
    # FUNCTIONS & CLASSES
    # -------------------------------
    def _extract_functions_and_classes(self):
        for node in self.tree.body:

            if isinstance(node, ast.FunctionDef):
                self.structure["functions"].append(
                    self._parse_function(node, is_method=False)
                )

            elif isinstance(node, ast.ClassDef):
                class_data = self._parse_class(node)
                self.structure["classes"].append(class_data)

    # -------------------------------
    # FUNCTION PARSER
    # -------------------------------
    def _parse_function(self, node, is_method=False):
        line_start = node.lineno
        line_end = getattr(node, "end_lineno", node.lineno)
        length = line_end - line_start + 1

        has_docstring = ast.get_docstring(node) is not None

        num_params = len(node.args.args)

        return {
            "name": node.name,
            "line_start": line_start,
            "line_end": line_end,
            "length": length,
            "has_docstring": has_docstring,
            "num_params": num_params,
            "is_method": is_method
        }

    # -------------------------------
    # CLASS PARSER
    # -------------------------------
    def _parse_class(self, node):
        line_start = node.lineno
        line_end = getattr(node, "end_lineno", node.lineno)

        methods = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._parse_function(item, is_method=True))

        return {
            "name": node.name,
            "line_start": line_start,
            "line_end": line_end,
            "methods": methods
        }