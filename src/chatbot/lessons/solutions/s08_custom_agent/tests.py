"""
Test cases for Exercise 8: Custom Agent

These tests verify custom agent functionality. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="letter_partner",
        question="Write a letter to my partner for our anniversary",
        expected_keywords=["love"],
    ),
    TestCase(
        id="telegram_dino",
        question="Write a a telegram describing dinosaur extinction",
        expected_keywords=["impact"],
    ),
    TestCase(
        id="postcard_cheese",
        question="Write a postcard about cheese from Greece",
        expected_keywords=["feta"],
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
