from pydantic import BaseModel
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class EvaluationType(str, Enum):
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    REGEX = "regex"
    LENGTH_MIN = "length_min"
    LENGTH_MAX = "length_max"
    MANUAL = "manual"

class Expectation(BaseModel):
    type: EvaluationType
    value: Any
    description: Optional[str] = None

class TestCase(BaseModel):
    id: str
    name: str
    prompt: str
    provider: Literal["claude", "openai", "goose"] = "claude"
    model: str = "claude-sonnet-4-20250514"
    expectations: List[Expectation] = []
    system_prompt: Optional[str] = None
    temperature: float = 1.0
    max_tokens: int = 1024
    created_at: datetime = datetime.now()
    tags: List[str] = []

class TestResult(BaseModel):
    test_id: str
    test_name: str
    prompt: str
    response: str
    provider: str
    model: str
    passed: Optional[bool] = None
    evaluation_results: List[Dict[str, Any]] = []
    execution_time: float
    timestamp: datetime = datetime.now()
    error: Optional[str] = None