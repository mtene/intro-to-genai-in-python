from dataclasses import dataclass, field
from typing import List


@dataclass
class TestCase:
    """
    Defines a single test case for chatbot testing.

    Attributes:
        id: Unique identifier for the test
        question: The question to ask the chatbot
        expected_keywords: Keywords that should appear in the answer (case-insensitive)
        reset_chatbot: Whether to reset chatbot state before running this test (default: True)
    """

    id: str
    question: str
    expected_keywords: List[str] = field(default_factory=list)
    reset_chatbot: bool = True


@dataclass
class PassingCriteria:
    """
    Defines criteria that must be met for tests to pass.

    Attributes:
        min_success_rate: Minimum fraction of tests that must succeed (0.0-1.0)
        max_avg_time: Maximum average execution time in seconds
    """

    min_success_rate: float = 0.8
    max_avg_time: float | None = None


@dataclass
class TestSuite:
    """
    Complete test suite for a chatbot implementation.

    Attributes:
        test_cases: List of test cases to run
        passing_criteria: Criteria for determining overall pass/fail
        repetitions: Number of times to run each test case (default: 1)
    """

    test_cases: List[TestCase]
    passing_criteria: PassingCriteria
    repetitions: int = 1

    def __len__(self) -> int:
        """Returns the number of test cases."""
        return len(self.test_cases)
