from fastapi import APIRouter, UploadFile, File

from app.models.schemas import ReviewResponse
from app.utils.file_loader import detect_language, read_code_file
from app.utils.repo_scanner import scan_repository

from app.parsers.python_parser import PythonParser
from app.parsers.javascript_parser import JavaScriptParser

from app.rules.python_rules import PythonRuleEngine
from app.rules.javascript_rules import JavaScriptRuleEngine

from app.agents.review_agent import ReviewAgent
from app.scoring.scoring_engine import ScoringEngine

from app.llm.local_llm import LocalLLM
from app.rag.vector_store import load_vector_store


router = APIRouter()

# Initialize dependencies (once)
llm = LocalLLM()
vector_store = load_vector_store()
retriever = vector_store.as_retriever()

review_agent = ReviewAgent(llm, retriever)


# -----------------------------
# MERGE + DEDUP (CORE FIX)
# -----------------------------
def merge_issues(rule_issues, llm_issues):
    """
    Merge issues with priority:
    Rule Engine > LLM
    """

    seen = set()
    final = []

    def make_key(issue):
        suggestion = issue.get("suggestion", "").lower()

        # normalize similar issues
        if "requests.get" in suggestion:
            return ("requests_issue", issue.get("line"))

        if "json()" in suggestion:
            return ("json_issue", issue.get("line"))

        if "file" in suggestion and "context manager" in suggestion:
            return ("file_issue", issue.get("line"))

        return (
            issue.get("rule"),
            issue.get("line"),
            suggestion[:50]
        )

    # Rule issues first (HIGH PRIORITY)
    for issue in rule_issues:
        key = make_key(issue)
        if key not in seen:
            seen.add(key)
            final.append(issue)

    # LLM issues second
    for issue in llm_issues:
        key = make_key(issue)
        if key not in seen:
            seen.add(key)
            final.append(issue)

    return final


@router.get("/")
def health_check():
    return {"status": "AI Code Reviewer Running"}


# -----------------------------
# SINGLE FILE REVIEW
# -----------------------------
@router.post("/review-code", response_model=ReviewResponse)
async def review_code(file: UploadFile = File(...)):

    file_bytes = await file.read()
    code = read_code_file(file_bytes)
    language = detect_language(file.filename)

    structure = {}
    rule_issues = []

    # -----------------------------
    # PYTHON ANALYSIS
    # -----------------------------
    if language == "python":

        parser = PythonParser(code)
        structure = parser.parse()

        rule_engine = PythonRuleEngine(
            structure,
            file.filename
        )

        rule_issues = [
        issue for issue in rule_engine.run()
        if issue["rule"] != "Docstring Missing"
        ]

    # -----------------------------
    # JAVASCRIPT ANALYSIS
    # -----------------------------
    elif language == "javascript":

        parser = JavaScriptParser(code)
        structure = parser.analyze()

        rule_engine = JavaScriptRuleEngine(
            structure,
            file.filename
        )

        rule_issues = [
            issue for issue in rule_engine.run()
            if issue["rule"] != "Docstring Missing"
        ]

    # -----------------------------
    # AI REVIEW
    # -----------------------------
    ai_issues = review_agent.review(
        code,
        language,
        file.filename
    )

    # -----------------------------
    # MERGE (NO OVERLAP)
    # -----------------------------
    all_issues = merge_issues(rule_issues, ai_issues)

    # -----------------------------
    # SCORING
    # -----------------------------
    scoring_engine = ScoringEngine(all_issues)
    score = scoring_engine.calculate()

    return {
        "score": score,
        "issues": all_issues,
        "summary": ""
    }


# -----------------------------
# REPOSITORY REVIEW
# -----------------------------
@router.post("/review-repository")
async def review_repository(folder_path: str):

    files = scan_repository(folder_path)

    all_issues = []

    for file_path in files:

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        language = detect_language(file_path)

        structure = {}
        rule_issues = []

        # PYTHON
        if language == "python":

            parser = PythonParser(code)
            structure = parser.parse()

            rule_engine = PythonRuleEngine(
                structure,
                file_path
            )

            rule_issues = [
                issue for issue in rule_engine.run()
                if issue["rule"] != "Docstring Missing"
            ]

        # JAVASCRIPT
        elif language == "javascript":

            parser = JavaScriptParser(code)
            structure = parser.analyze()

            rule_engine = JavaScriptRuleEngine(
                structure,
                file_path
            )

            rule_issues = [
                issue for issue in rule_engine.run()
                if issue["rule"] != "Docstring Missing"
            ]

        # AI REVIEW
        ai_issues = review_agent.review(
            code,
            language,
            file_path
        )

        issues = merge_issues(rule_issues, ai_issues)

        all_issues.extend(issues)

    # FINAL DEDUP (ACROSS FILES)
    all_issues = merge_issues([], all_issues)

    # SCORING
    scoring_engine = ScoringEngine(all_issues)
    score = scoring_engine.calculate()

    return {
        "score": score,
        "issues": all_issues,
        "total_files": len(files)
    }