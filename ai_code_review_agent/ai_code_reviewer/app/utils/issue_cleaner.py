def clean_duplicate_issues(issues):

    seen = set()
    cleaned = []

    for issue in issues:

        key = (
            issue.get("file"),
            issue.get("line"),
            issue.get("rule")
        )

        if key not in seen:

            seen.add(key)
            cleaned.append(issue)

    return cleaned