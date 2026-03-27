class ScoringEngine:

    def __init__(self, issues):

        self.issues = issues
        self.base_score = 100

    def calculate(self):

        score = self.base_score

        for issue in self.issues:

            severity = issue.get("severity", "low").lower()

            if severity == "high":
                score -= 5

            elif severity == "medium":
                score -= 3

            elif severity == "low":
                score -= 1

        # Prevent negative score
        if score < 20:
            score = 20

        return score