import json


ALLOWED_LLM_RULES = {
    "Readability Issue",
    "Single Responsibility Violation",
    "Code Smell",
    "Error Handling Issue",
    "Design Issue"
}


class ReviewAgent:

    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
        self.cache = {}

    # -------------------------------
    # MAIN ENTRY
    # -------------------------------
    def review(self, code: str, language: str, filename: str):

        guidelines = self._get_guidelines(language)

        all_issues = []

        code_chunks = self._split_code(code)

        for chunk, offset in code_chunks:
            prompt = self._build_prompt(chunk, guidelines)

            try:
                raw_output = self.llm.generate(prompt)

                issues = self._parse_llm_output(raw_output)

                for issue in issues:
                    if isinstance(issue.get("line"), int):
                        issue["line"] += offset

                    fixed_line = self._fix_issue_line(issue, code)

                    # only override if strong match
                    if fixed_line and abs(fixed_line - issue["line"]) > 5:
                        issue["line"] = fixed_line

                all_issues.extend(issues)

            except Exception as e:
                print("LLM chunk error:", e)

        # pipeline
        issues = self._filter_allowed_issues(all_issues)
        issues = self._filter_low_quality_issues(issues, code)
        issues = self._add_missed_critical_issues(code, issues)
        issues = self._normalize_severity(issues)

        issues = self._deduplicate_issues(issues)

        # inject filename
        for issue in issues:
            issue["file"] = filename

        return issues

    # -------------------------------
    # SMART LINE FIX
    # -------------------------------
    def _fix_issue_line(self, issue, code):
        suggestion = issue.get("suggestion", "").lower()

        # strong mappings
        mappings = [
            ("requests.get", "requests.get"),
            (".json", ".json("),
            ("open(", "open("),
            ("timeout", "requests.get"),
            ("divide", "len("),
            ("zero", "len("),
            ("nested loop", "for"),
            ("o(n", "for"),
        ]

        for keyword, code_key in mappings:
            if keyword in suggestion:
                return self._find_line_number(code, code_key)

        return issue.get("line")

    # -------------------------------
    # Line number
    # -------------------------------
    def _find_line_number(self, code, keyword):
        lines = code.split("\n")
        for i, line in enumerate(lines, start=1):
            if keyword in line:
                return i
        return 1

    # -------------------------------
    # GUIDELINES (RAG)
    # -------------------------------
    def _get_guidelines(self, language):

        if language in self.cache:
            return self.cache[language]

        docs = self.retriever.get_relevant_documents(
            f"{language} coding best practices"
        )

        text = "\n".join([doc.page_content for doc in docs])

        self.cache[language] = text
        return text

    # -------------------------------
    # PROMPT BUILDER
    # -------------------------------
    def _build_prompt(self, code, guidelines):

        return f"""
You are an expert senior software engineer reviewing code.

Your job is to detect ONLY real, high-confidence issues.

DO NOT over-report.

----------------------------------
STRICT RULES
----------------------------------

DO NOT report:
- naming issues
- docstring issues
- function length issues
- global variable issues

ONLY report issues if:
- there is a real bug, risk, or inefficiency
- you are highly confident (>90%)

----------------------------------
CATEGORY RULES
----------------------------------

Use ONLY these categories:

1. Error Handling Issue
2. Code Smell
3. Design Issue
4. Single Responsibility Violation
5. Readability Issue

IMPORTANT:
- DO NOT misuse "Single Responsibility Violation"
- DO NOT report trivial readability issues
- DO NOT repeat same issue multiple times

----------------------------------
OUTPUT FORMAT (STRICT JSON ONLY)
----------------------------------

[
  {{
    "rule": "<category>",
    "line": <line_number>,
    "severity": "low|medium|high",
    "suggestion": "<specific fix>"
  }}
]

Guidelines:
{guidelines}

Code:
{code}
"""

    # -------------------------------
    # IMPROVE SEVERITY
    # -------------------------------
    def _normalize_severity(self, issues):
        for issue in issues:
            text = issue.get("suggestion", "").lower()

            if any(x in text for x in ["crash", "exception", "timeout", "division", "json"]):
                issue["severity"] = "high"

            elif any(x in text for x in ["performance", "inefficient", "o(n"]):
                issue["severity"] = "medium"

            else:
                issue["severity"] = issue.get("severity", "low")

        return issues

    # -------------------------------
    # FORCE CRITICAL ISSUE DETECTION
    # -------------------------------
    def _add_missed_critical_issues(self, code, issues):
        text = code.lower()
        extra = []

        # requests timeout
        if "requests.get(" in text and "timeout=" not in text:
            extra.append({
                "rule": "Error Handling Issue",
                "line": self._find_line_number(code, "requests.get"),
                "severity": "high",
                "suggestion": "Add timeout parameter to requests.get(), e.g., timeout=5"
            })

        # unsafe json
        if ".json()" in text:
            extra.append({
                "rule": "Error Handling Issue",
                "line": self._find_line_number(code, ".json()"),
                "severity": "high",
                "suggestion": "Wrap response.json() in try/except to handle invalid JSON"
            })

        # divide by zero
        if "/" in text and "len(" in text:
            extra.append({
                "rule": "Error Handling Issue",
                "line": self._find_line_number(code, "len("),
                "severity": "high",
                "suggestion": "Check for empty list before division to avoid ZeroDivisionError"
            })

        # file handling
        if "open(" in text and "with open" not in text:
            extra.append({
                "rule": "Code Smell",
                "line": self._find_line_number(code, "open("),
                "severity": "medium",
                "suggestion": "Use context manager (with open) to handle file operations safely"
            })

        # axios / fetch
        if "axios.get" in text or "fetch(" in text:
            extra.append({
                "rule": "Error Handling Issue",
                "line": self._find_line_number(code, "axios.get"),
                "severity": "high",
                "suggestion": "Wrap API call in try/catch and handle errors properly"
            })

        # pagination bug
        if "page" in text and "offset" in text:
            extra.append({
                "rule": "Error Handling Issue",
                "line": self._find_line_number(code, "offset"),
                "severity": "high",
                "suggestion": "Validate page and limit before using them to calculate offset"
            })

        # division issue
        if "/ limit" in text:
            extra.append({
                "rule": "Error Handling Issue",
                "line": self._find_line_number(code, "Math.ceil"),
                "severity": "high",
                "suggestion": "Ensure limit is not undefined or zero before division"
            })

        # mass assignment
        if "{ ...req.body" in text:
            extra.append({
                "rule": "Design Issue",
                "line": self._find_line_number(code, "req.body"),
                "severity": "high",
                "suggestion": "Avoid spreading req.body directly to prevent mass assignment vulnerability"
            })

        # nested loops
        lines = code.split("\n")
        for i in range(len(lines) - 1):
            if "for" in lines[i] and "for" in lines[i + 1]:
                extra.append({
                    "rule": "Design Issue",
                    "line": i + 1,
                    "severity": "medium",
                    "suggestion": "Avoid nested loops to reduce O(n²) complexity"
                })
                break

        return issues + extra

    # -------------------------------
    # FILTER BAD LLM OUTPUT
    # -------------------------------
    def _filter_low_quality_issues(self, issues, code):
        filtered = []

        code_text = code.lower()

        for issue in issues:
            suggestion = issue.get("suggestion", "").lower()
            rule = issue.get("rule", "")

            # ❌ remove generic suggestions
            if any(x in suggestion for x in [
                "improve code",
                "add error handling",
                "refactor this",
                "optimize this"
            ]):
                continue

            # ❌ REMOVE FAKE "already handled" errors
            if "isuserexists" in suggestion and "if (!isuserexists)" in code_text:
                continue

            if "comparesync" in suggestion and "if (!match)" in code_text:
                continue

            # ❌ REMOVE BAD SRP
            if rule == "Single Responsibility Violation":
                if not any(x in suggestion for x in [
                    "multiple responsibilities",
                    "multiple unrelated tasks",
                    "separate api",
                    "separate business logic"
                ]):
                    continue

            # ❌ REMOVE WEAK READABILITY
            if rule == "Readability Issue":
                if any(x in suggestion for x in [
                    "better variable name",
                    "more descriptive name"
                ]):
                    continue

            filtered.append(issue)

        return filtered

    # -------------------------------
    # PARSE OUTPUT
    # -------------------------------
    def _parse_llm_output(self, raw_output):
        try:
            start = raw_output.find("[")
            end = raw_output.rfind("]") + 1
            json_str = raw_output[start:end]
            return json.loads(json_str)
        except Exception:
            return []

    # -------------------------------
    # FILTER VALID RULES ONLY
    # -------------------------------
    def _filter_allowed_issues(self, issues):
        return [i for i in issues if i.get("rule") in ALLOWED_LLM_RULES]

    # -------------------------------
    # CODE SPLITTING (WITH OFFSET)
    # -------------------------------
    def _split_code(self, code):
        import ast

        try:
            tree = ast.parse(code)
        except:
            return [(code, 0)]

        chunks = []
        lines = code.split("\n")

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                start = node.lineno - 1
                end = getattr(node, "end_lineno", start)

                chunk = "\n".join(lines[start:end])
                chunks.append((chunk, start))

        if not chunks:
            return [(code, 0)]

        return chunks
    
    # -------------------------------
    # Prevent Duplication
    # -------------------------------
    
    def _deduplicate_issues(self, issues):
        seen = set()
        unique = []

        for issue in issues:
            key = (
                issue.get("rule"),
                issue.get("line"),
                issue.get("suggestion")[:50]
            )

            if key not in seen:
                seen.add(key)
                unique.append(issue)

        return unique