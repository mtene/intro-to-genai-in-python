import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from typing import List, Dict, Any
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.testing.test_suite import TestSuite, TestCase, PassingCriteria


class ChatbotEvaluator:
    """Framework for evaluating chatbot performance."""

    def __init__(self, chatbot: BaseChatBot):
        self.chatbot = chatbot
        self.results: List[Dict[str, Any]] = []

    def run_test_suite(self, test_suite: TestSuite, rich_console: Console) -> bool:
        """Run all test cases from a TestSuite and return results."""

        if not test_suite.test_cases or test_suite.repetitions <= 0:
            rich_console.print("⚠️  [yellow]No tests to run![/yellow]")
            return False

        self.results = []
        for repetition in range(test_suite.repetitions):
            for test_idx, test_case in enumerate(test_suite.test_cases):
                # Reset chatbot state: before each test suite starts or if test requires it
                if test_idx == 0 or test_case.reset_chatbot:
                    rich_console.print("[dim]Chatbot state reset[/dim]")
                    self.chatbot.reset()

                if test_suite.repetitions > 1:
                    rich_console.print(
                        f"⏩ Running {len(test_suite)} test cases (repetition {repetition + 1} / {test_suite.repetitions}) ..."
                    )
                else:
                    rich_console.print(f"⏩ Running {len(test_suite)} test cases ...")

                # Run test
                result = self._run_test_case(test_case, rich_console)
                result["repetition"] = repetition + 1
                self.results.append(result)


        # Show per-test summary
        for test_case in test_suite.test_cases:
            successes = sum(
                1
                for result in self.results
                if result["test_id"] == test_case.id and result["success"]
            )
            rich_console.print(
                f"⭐ Test [yellow]{test_case.id}[/yellow]: {successes} / {test_suite.repetitions} runs passed ({successes / test_suite.repetitions * 100:.0f}%)"
            )

        # Show global summary
        success = self._check_passing_criteria(
            test_suite.passing_criteria, rich_console
        )
        total = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        avg_time = sum(r["execution_time"] for r in self.results) / total
        rich_console.print(
            f"🎯 Testing summary: {successful} / {total} passed ({successful / total * 100:.1f}%) | Avg time: {avg_time:.2f}s"
        )

        # Reset chatbot state after all tests complete
        rich_console.print("[dim]Chatbot state reset[/dim]")
        self.chatbot.reset()

        return success

    def _run_test_case(
        self, test_case: TestCase, rich_console: Console
    ) -> Dict[str, Any]:
        """Run a single test case and collect metrics."""

        # Run case, tracking execution time
        rich_console.print(f"[[yellow]{test_case.id}[/yellow]] {test_case.question}")
        start_time = time.time()
        try:
            answer = self.chatbot.get_answer(
                test_case.question,
                ctx=ChatContext(
                    status_update_func=lambda msg: rich_console.print(Text(msg))
                ),
            )
            error = None
            rich_console.print(Panel(Markdown(answer)))
            success = True
        except Exception as e:
            error = str(e)
            answer = None
            rich_console.print(f"[bold_red]{error}[/bold_red]")
            success = False
        end_time = time.time()
        execution_time = end_time - start_time

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
                rich_console.print(
                    f"     Keywords: found {metrics['keyword_match']['found']} expected {test_case.expected_keywords} ({metrics['keyword_match']['score'] * 100:.0f}%)"
                )

                if metrics["keyword_match"]["score"] < 1.0:
                    success = False
                    error = f"Keywords missing: expected {len(test_case.expected_keywords)}, found {len(keywords_found)}"

        # Print outcome
        if success:
            rich_console.print(f"  ✔️  Success ({execution_time:.2f}s)")
        else:
            rich_console.print(f"  ❌ Failed: {error}")

        return {
            "test_id": test_case.id,
            "question": test_case.question,
            "answer": answer,
            "success": success,
            "error": error,
            "execution_time": execution_time,
            "metrics": metrics,
        }

    def _check_passing_criteria(
        self, criteria: PassingCriteria, rich_console: Console
    ) -> bool:
        """Check if test results meet passing criteria."""

        all_passed = True

        # Check success rate
        success_count = sum(1 for r in self.results if r["success"])
        success_rate = success_count / len(self.results) if self.results else 0.0
        passed = success_rate >= criteria.min_success_rate

        if not passed:
            rich_console.print(
                f"❌ Success rate {success_rate * 100:.1f}% below required {criteria.min_success_rate * 100:.1f}%"
            )
            all_passed = False

        # Check average execution time
        if criteria.max_avg_time is not None:
            avg_time = (
                sum(r["execution_time"] for r in self.results) / len(self.results)
                if self.results
                else 0.0
            )
            passed = avg_time <= criteria.max_avg_time

            if not passed:
                rich_console.print(
                    f"❌ Average time {avg_time:.2f}s exceeds maximum {criteria.max_avg_time:.2f}s"
                )
                all_passed = False

        if all_passed:
            rich_console.print("✔️  All criteria passed")

        return all_passed
