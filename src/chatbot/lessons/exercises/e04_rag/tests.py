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
        id="person_of_interest",
        question="What is the first name of Tom's mistress?",
        expected_keywords=["Myrtle"],
    ),
    TestCase(
        id="specific_fact",
        question="What university did Jay attend?",
        expected_keywords=["Oxford"],
    ),
    TestCase(
        id="enumeration",
        question="What type of drink is served at Gatsby's parties?",
        expected_keywords=["cocktail"],
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
