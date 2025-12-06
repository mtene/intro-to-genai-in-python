"""
Test cases for Exercise 2: System Instructions

These tests verify system prompt functionality. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="simple_factual",
        question="What is the capital of France?",
        expected_keywords=["Paris"],
    ),
    TestCase(
        id="explanation",
        question="Explain what Python is in one sentence",
        expected_keywords=["programming"],
    ),
    TestCase(
        id="system_prompt_adherence",
        question="Tell me about your personality",
        expected_keywords=["bubbly"],
    ),
]

# Define passing criteria
PASSING_CRITERIA = PassingCriteria(
    min_success_rate=0.8,
)

# Create the complete test suite
TEST_SUITE = TestSuite(
    test_cases=TEST_CASES, passing_criteria=PASSING_CRITERIA, repetitions=1
)
