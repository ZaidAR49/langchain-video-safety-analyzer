from pydantic import BaseModel


class ViolationItem(BaseModel):
    timestamp: str
    category: str
    description: str
    severity: str


class SafetyReport(BaseModel):
    overall_verdict: str
    safety_score: int
    summary: str
    violations: list[ViolationItem] = []
    recommended_edits: list[str] = []
