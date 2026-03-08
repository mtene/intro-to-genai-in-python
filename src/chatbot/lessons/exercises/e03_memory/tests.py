"""
Test cases for Exercise 3: Conversation History

These tests verify conversation history tracking. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="simple_factual",
        question="What is the capital of Romania?",
        expected_keywords=["Bucharest"],
        reset_chatbot=False,
    ),
    TestCase(
        id="history_reference",
        question="What was my previous question?",
        expected_keywords=["capital", "Romania"],
        reset_chatbot=False,
    ),
    TestCase(
        id="multi_turn",
        question="Translate your first answer to German",
        expected_keywords=["Bukarest"],
        reset_chatbot=False,
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
