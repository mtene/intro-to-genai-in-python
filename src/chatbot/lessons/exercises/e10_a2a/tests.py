"""
Test cases for Exercise 10: Agent-to-Agent Protocol (A2A)

These tests verify A2A multi-agent functionality. The exercise implementation
is intentionally incomplete and should fail these tests. The solution passes all tests.

The orchestrator automatically starts both expert agents as subprocesses when you
run the chatbot, so no manual setup is required.

You can extend these tests by appending additional test cases to the TEST_CASES list.
"""

from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


# Define test cases using TestCase objects
TEST_CASES = [
    TestCase(
        id="budget_expert_routing",
        question="What's a realistic daily budget for visiting Rome?",
        expected_keywords=["budget", "day", "accommodation", "food"],
    ),
    TestCase(
        id="destination_expert_routing",
        question="Recommend destinations for someone who loves beaches and diving",
        expected_keywords=["destination", "beach"],
    ),
    TestCase(
        id="multi_expert_coordination",
        question="I have $150 per day to spend in Asia. Where should I go?",
        expected_keywords=["budget", "destination"],
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
