import esprima


class JavaScriptParser:

    def __init__(self, code: str):
        self.code = code
        self.tree = None

        # 🔥 Try parsing safely (prevents crash)
        try:
            self.tree = esprima.parseScript(code, loc=True)
        except Exception as e:
            print("JS Parse Error:", e)

            # 🔥 TEMP FIX for modern JS (optional chaining etc.)
            try:
                safe_code = code.replace("?.", ".")
                self.tree = esprima.parseScript(safe_code, loc=True)
            except Exception as e2:
                print("JS Fallback Parse Failed:", e2)
                self.tree = None

        self.structure = {
            "functions": [],
            "classes": [],
            "globals": [],
            "parse_error": self.tree is None  # 🔥 important flag
        }

    # -------------------------------
    def analyze(self):

        # 🔥 If parsing failed → return minimal structure
        if not self.tree:
            return self.structure

        for node in self.tree.body:
            self._handle_node(node)

        return self.structure

    # -------------------------------
    def _handle_node(self, node):

        try:
            if node.type == "FunctionDeclaration":
                self.structure["functions"].append(
                    self._parse_function(node)
                )

            elif node.type == "VariableDeclaration":
                for decl in node.declarations:
                    if decl.id.type == "Identifier":
                        self.structure["globals"].append(decl.id.name)

            elif node.type == "ClassDeclaration":
                self.structure["classes"].append(
                    self._parse_class(node)
                )

        except Exception as e:
            print("Node parse error:", e)

    # -------------------------------
    def _parse_function(self, node):

        try:
            line_start = node.loc.start.line
            line_end = node.loc.end.line
            length = line_end - line_start + 1

            num_params = len(node.params)

            return {
                "name": node.id.name if node.id else "anonymous",
                "line_start": line_start,
                "line_end": line_end,
                "length": length,
                "has_docstring": False,
                "num_params": num_params,
                "is_method": False
            }

        except Exception as e:
            print("Function parse error:", e)
            return {}

    # -------------------------------
    def _parse_class(self, node):

        methods = []

        try:
            for element in node.body.body:
                if element.type == "MethodDefinition":

                    method_node = element.value

                    methods.append({
                        "name": element.key.name if hasattr(element.key, "name") else "unknown",
                        "line_start": method_node.loc.start.line,
                        "line_end": method_node.loc.end.line,
                        "length": method_node.loc.end.line - method_node.loc.start.line + 1,
                        "has_docstring": False,
                        "num_params": len(method_node.params),
                        "is_method": True
                    })

        except Exception as e:
            print("Class parse error:", e)

        return {
            "name": node.id.name if node.id else "anonymous_class",
            "line_start": node.loc.start.line,
            "line_end": node.loc.end.line,
            "methods": methods
        }