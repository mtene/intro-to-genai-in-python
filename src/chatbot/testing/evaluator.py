"""
Chatbot testing framework for systematic testing and benchmarking.
"""

from typing import List, Dict, Any
import time
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


class ChatbotEvaluator:
    """Framework for evaluating chatbot performance."""

    def __init__(self, chatbot: BaseChatBot):
        self.chatbot = chatbot
        self.results: List[Dict[str, Any]] = []

    def run_test_case(self, test_case: TestCase) -> Dict[str, Any]:
        """Run a single test case and collect metrics."""

        # Reset chatbot state before test if requested
        if test_case.reset_chatbot:
            self.chatbot.reset()

        start_time = time.time()

        try:
            answer = self.chatbot.get_answer(test_case.question, ctx=ChatContext())
            success = True
            error = None
        except Exception as e:
            answer = None
            success = False
            error = str(e)

        end_time = time.time()

        # Validate answer and collect metrics
        metrics = {}
        if success and answer:
            # Check keyword presence
            if test_case.expected_keywords:
                keywords_found = [
                    kw
                    for kw in test_case.expected_keywords
                    if kw.lower() in answer.lower()
                ]
                metrics["keyword_match"] = {
                    "found": keywords_found,
                    "total": len(test_case.expected_keywords),
                    "score": len(keywords_found) / len(test_case.expected_keywords),
                }

                if metrics["keyword_match"]["score"] < 1.0:
                    success = False
                    error = f"Keywords missing: expected {len(test_case.expected_keywords)}, found {len(keywords_found)}"

        # Collect metrics
        result = {
            "test_id": test_case.id,
            "question": test_case.question,
            "answer": answer,
            "success": success,
            "error": error,
            "execution_time": end_time - start_time,
            "answer_length": len(answer) if answer else 0,
            "metrics": metrics,
        }

        return result

    def run_test_suite(self, test_suite: TestSuite) -> List[Dict]:
        """Run all test cases from a TestSuite and return results."""
        self.results = []

        total_runs = len(test_suite) * test_suite.repetitions
        if test_suite.repetitions > 1:
            print(
                f"Running {len(test_suite)} test cases × {test_suite.repetitions} repetitions = {total_runs} total runs..."
            )
        else:
            print(f"Running {len(test_suite)} test cases...")

        for test_case in test_suite.test_cases:
            test_results = []

            for rep in range(test_suite.repetitions):
                if test_suite.repetitions > 1:
                    print(
                        f"[{test_case.id}] {test_case.question[:50]} (run {rep + 1}/{test_suite.repetitions})"
                    )
                else:
                    print(f"[{test_case.id}] {test_case.question[:50]}")

                result = self.run_test_case(test_case)
                result["repetition"] = rep + 1
                self.results.append(result)
                test_results.append(result)

                if result["success"]:
                    print(f"  ✔️  Success ({result['execution_time']:.2f}s)")
                    if "metrics" in result and "keyword_match" in result["metrics"]:
                        km = result["metrics"]["keyword_match"]
                        print(f"    Keywords: {km['found']} ({km['score'] * 100:.0f}%)")
                else:
                    print(f"  ❌ Failed: {result['error']}")

            # Show per-test summary if multiple repetitions
            if test_suite.repetitions > 1:
                successes = sum(1 for r in test_results if r["success"])
                print(
                    f"  → {successes}/{test_suite.repetitions} runs passed ({successes / test_suite.repetitions * 100:.0f}%)"
                )

            print()

        return self.results

    def print_summary(self):
        """Print summary statistics."""
        if not self.results:
            print("No results to summarize")
            return

        total = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        avg_time = sum(r["execution_time"] for r in self.results) / total

        print(
            f"Results: {successful}/{total} passed ({successful / total * 100:.1f}%) | Avg time: {avg_time:.2f}s"
        )

    def check_passing_criteria(
        self, results: List[Dict], criteria: PassingCriteria
    ) -> bool:
        """
        Check if test results meet passing criteria.

        Args:
            results: List of test results from run_test_suite()
            criteria: PassingCriteria object with:
                - min_success_rate (float): Minimum success rate (0.0-1.0)
                - max_avg_time (float, optional): Maximum average execution time

        Returns:
            True if all criteria are met, False otherwise
        """
        if not results:
            print("No results to check")
            return False

        all_passed = True

        # Check success rate
        success_count = sum(1 for r in results if r["success"])
        success_rate = success_count / len(results)
        passed = success_rate >= criteria.min_success_rate

        if not passed:
            print(
                f"❌ Success rate {success_rate * 100:.1f}% below required {criteria.min_success_rate * 100:.1f}%"
            )
            all_passed = False

        # Check average execution time
        if criteria.max_avg_time is not None:
            avg_time = sum(r["execution_time"] for r in results) / len(results)
            passed = avg_time <= criteria.max_avg_time

            if not passed:
                print(
                    f"❌ Average time {avg_time:.2f}s exceeds maximum {criteria.max_avg_time:.2f}s"
                )
                all_passed = False

        if all_passed:
            print("✔️  All criteria passed")

        return all_passed
