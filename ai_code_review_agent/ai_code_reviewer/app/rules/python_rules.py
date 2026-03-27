import re


class PythonRuleEngine:

    def __init__(self, structure, filename):
        self.structure = structure
        self.filename = filename
        self.issues = []

    # -------------------------------
    # NAMING (FUNCTIONS + VARIABLES)
    # -------------------------------
    def check_snake_case(self):

        pattern = r"^[a-z_][a-z0-9_]*$"

        # Functions
        for func in self.structure.get("functions", []):
            if not re.match(pattern, func["name"]):
                self._add_issue(
                    "Naming Convention",
                    func["line_start"],
                    f"Rename function '{func['name']}' to snake_case",
                    "low"
                )

        # Methods
        for cls in self.structure.get("classes", []):
            for method in cls.get("methods", []):
                if not re.match(pattern, method["name"]):
                    self._add_issue(
                        "Naming Convention",
                        method["line_start"],
                        f"Rename method '{method['name']}' to snake_case",
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
    # DOCSTRING
    # -------------------------------
    def check_docstrings(self):

        for func in self.structure.get("functions", []):
            if not func["has_docstring"]:
                self._add_issue(
                    "Docstring Missing",
                    func["line_start"],
                    "Add a docstring to this function",
                    "high"
                )

        for cls in self.structure.get("classes", []):
            for method in cls.get("methods", []):
                if not method["has_docstring"]:
                    self._add_issue(
                        "Docstring Missing",
                        method["line_start"],
                        "Add a docstring to this method",
                        "high"
                    )

    # -------------------------------
    # GLOBAL VARIABLES
    # -------------------------------
    def check_global_variables(self):

        for var in self.structure.get("globals", []):
            self._add_issue(
                "Global Variable",
                1,
                f"Avoid using global variable '{var}'",
                "medium"
            )

    # -------------------------------
    # TOO MANY PARAMETERS
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
                if method["num_params"] > 6:  # includes 'self'
                    self._add_issue(
                        "Too Many Parameters",
                        method["line_start"],
                        "Method has too many parameters (>5 excluding self)",
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
    # INTERNAL HELPER
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
    # RUN ALL RULES
    # -------------------------------
    def run(self):

        self.check_snake_case()
        self.check_function_length()
        self.check_docstrings()
        self.check_global_variables()
        self.check_parameters()
        self.check_class_length()

        return self.issues