"""
Test cases for Exercise 7: RAG

These tests verify RAG functionality. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="knowledge_retrieval",
        question="What university did Gatsby attend?",
        expected_keywords=["Oxford"],
    ),
    TestCase(
        id="specific_fact",
        question="What is the last name of the narrator?",
        expected_keywords=["Carraway"],
    ),
    TestCase(
        id="synthesis",
        question="In what year does the story take place?",
        expected_keywords=["1922"],
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
