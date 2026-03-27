from pydantic import BaseModel
from typing import List


class Issue(BaseModel):
    rule: str
    file: str
    line: int
    severity: str
    suggestion: str


class ReviewResponse(BaseModel):
    score: int
    issues: List[Issue]
    summary: str