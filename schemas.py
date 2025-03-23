from pydantic import BaseModel


class CodeReviewInput(BaseModel):
    code: str  # Raw Power Automate code as string


class CodeReviewOutput(BaseModel):
    review_status: bool  # True if code is acceptable, False otherwise
    problems_identified: list[str]  # List of issues found
    recommendations: list[str]  # Suggestions for improvement
