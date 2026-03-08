"""
Test cases for Exercise 4: Structured Outputs

These tests verify structured output functionality. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="person_extraction",
        question="What is Einstein known for?",
        expected_keywords=["Albert", "Einstein", "1879"],
    ),
    TestCase(
        id="person_format",
        question="Who was the first woman to be awarded a nobel prize?",
        expected_keywords=["Marie", "Curie", "1867"],
    ),
    TestCase(
        id="no_person",
        question="Why did the Titanic sink?",
        expected_keywords=["1912"],
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
