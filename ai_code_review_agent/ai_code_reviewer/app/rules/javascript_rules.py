import re


class JavaScriptRuleEngine:

    def __init__(self, structure, filename):
        self.structure = structure
        self.filename = filename
        self.issues = []

    # -------------------------------
    # NAMING
    # -------------------------------
    def check_naming(self):

        pattern = r"^[a-z_][a-z0-9_]*$"

        for func in self.structure.get("functions", []):
            if not re.match(pattern, func["name"]):
                self._add_issue(
                    "Naming Convention",
                    func["line_start"],
                    f"Rename function '{func['name']}' to camelCase or snake_case",
                    "low"
                )

        for cls in self.structure.get("classes", []):
            for method in cls.get("methods", []):
                if not re.match(pattern, method["name"]):
                    self._add_issue(
                        "Naming Convention",
                        method["line_start"],
                        f"Rename method '{method['name']}' properly",
                        "low"
                    )

    # -------------------------------
    # FUNCTION LENGTH
    # -------------------------------
    def check_function_length(self):

        for func in self.structure.get("functions", []):
            if func["length"] > 50:
                self._add_issue(
                    "Function Length",
                    func["line_start"],
                    "Function exceeds 50 lines",
                    "medium"
                )

        for cls in self.structure.get("classes", []):
            for method in cls.get("methods", []):
                if method["length"] > 50:
                    self._add_issue(
                        "Function Length",
                        method["line_start"],
                        "Method exceeds 50 lines",
                        "medium"
                    )

    # -------------------------------
    # FIXED GLOBAL CHECK (IMPORTANT)
    # -------------------------------
    def check_globals(self):

        SAFE_GLOBALS = {
            "require",
            "module",
            "exports",
            "__dirname",
            "__filename"
        }

        for var in self.structure.get("globals", []):

            var_name = var.get("name") if isinstance(var, dict) else var
            line = var.get("line", 1) if isinstance(var, dict) else 1
            code_line = var.get("code", "").strip() if isinstance(var, dict) else ""

            # ❌ Skip safe globals
            if var_name in SAFE_GLOBALS:
                continue

            # ❌ Skip imports (require / import)
            if "require(" in code_line or code_line.startswith("import"):
                continue

            # ❌ Skip constants (ALL CAPS usually config)
            if var_name.isupper():
                continue

            # ✅ Only flag mutable globals
            if any(keyword in code_line for keyword in ["let ", "var ", "= []", "= {}"]):
                self._add_issue(
                    "Global Variable",
                    line,
                    f"Avoid using mutable global variable '{var_name}'",
                    "medium"
                )

    # -------------------------------
    # PARAMETERS
    # -------------------------------
    def check_parameters(self):

        for func in self.structure.get("functions", []):
            if func["num_params"] > 5:
                self._add_issue(
                    "Too Many Parameters",
                    func["line_start"],
                    "Function has too many parameters (>5)",
                    "medium"
                )

        for cls in self.structure.get("classes", []):
            for method in cls.get("methods", []):
                if method["num_params"] > 5:
                    self._add_issue(
                        "Too Many Parameters",
                        method["line_start"],
                        "Method has too many parameters",
                        "medium"
                    )

    # -------------------------------
    # CLASS LENGTH
    # -------------------------------
    def check_class_length(self):

        for cls in self.structure.get("classes", []):
            length = cls["line_end"] - cls["line_start"] + 1

            if length > 200:
                self._add_issue(
                    "Class Length",
                    cls["line_start"],
                    "Class is too long (>200 lines)",
                    "medium"
                )

    # -------------------------------
    # ADD ISSUE
    # -------------------------------
    def _add_issue(self, rule, line, suggestion, severity):
        self.issues.append(
            {
                "rule": rule,
                "file": self.filename,
                "line": line,
                "severity": severity,
                "suggestion": suggestion
            }
        )

    # -------------------------------
    # RUN ENGINE
    # -------------------------------
    def run(self):

        self.check_naming()
        self.check_function_length()
        self.check_globals()
        self.check_parameters()
        self.check_class_length()

        return self.issues