"""
Test cases for Exercise 6: MCP

These tests verify MCP integration. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="currency_conversion",
        question="Is 100 USD enough to buy a 50 EUR present? Answer with just yes or no",
        expected_keywords=["yes"],
    ),
    TestCase(
        id="time_conversion",
        question="What is 4 PM Oslo time in New York?",
        expected_keywords=["10"],
    ),
    TestCase(
        id="mcp_search",
        question="What is the equivalent of GitHub Actions in Azure DevOps?",
        expected_keywords=["pipelines"],
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
