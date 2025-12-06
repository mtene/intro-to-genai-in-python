"""
Test cases for Exercise 1: Prompting

These tests verify basic prompting functionality. The exercise implementation
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
        id="translation",
        question="Merry Christmas in German",
        expected_keywords=["Weihnachten"],
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
