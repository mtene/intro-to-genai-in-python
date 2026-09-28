"""Run lesson-local DeepEval datasets against a chatbot."""

import os
import time
from collections.abc import Mapping, Sequence
from typing import Any, cast

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from rich.console import Console
from rich.table import Table

from chatbot.chat_context import ChatContext
from chatbot.chatbot_base import BaseChatBot

EvaluationSuites = Mapping[str, tuple[EvaluationDataset, Sequence[BaseMetric]]]


class ChatbotEvaluator:
    """Generate chatbot responses and apply directly declared DeepEval metrics."""

    def __init__(self, chatbot: BaseChatBot):
        self.chatbot = chatbot

    def run(
        self,
        suites: EvaluationSuites,
        console: Console,
        repetitions: int = 1,
        min_pass_rate: float = 0.8,
    ) -> bool:
        if not suites:
            console.print("[yellow]No test suite defined for this chatbot.[/yellow]")
            return False

        results: list[dict[str, Any]] = []
        self.chatbot.reset()
        for suite_name, (dataset, metrics) in suites.items():
            console.print(f"\n[bold cyan]Evaluating: {suite_name}[/bold cyan]")
            for repetition in range(repetitions):
                for golden in dataset.goldens:
                    if (golden.additional_metadata or {}).get("reset_chatbot", True):
                        self.chatbot.reset()
                    results.extend(
                        self._evaluate_golden(
                            suite_name,
                            cast(Golden, golden),
                            metrics,
                            console,
                            repetition + 1,
                        )
                    )

        self.chatbot.reset()
        self._print_results(results, console)
        passed = sum(result["passed"] for result in results)
        pass_rate = passed / len(results) if results else 0.0
        console.print(
            f"\n🎯 Evaluation summary: {passed} / {len(results)} metrics passed "
            f"({pass_rate:.0%}); required {min_pass_rate:.0%}."
        )
        return bool(results) and pass_rate >= min_pass_rate

    def _evaluate_golden(
        self,
        suite_name: str,
        golden: Golden,
        metrics: Sequence[BaseMetric],
        console: Console,
        repetition: int,
    ) -> list[dict[str, Any]]:
        console.print(f"[yellow]{golden.input}[/yellow]")
        start = time.perf_counter()
        try:
            answer = self.chatbot.get_answer(
                golden.input,
                ChatContext(status_update_func=lambda message: console.print(message)),
            )
            error = None
        except Exception as exception:
            answer = ""
            error = str(exception)
        latency = time.perf_counter() - start

        if error:
            return [
                {
                    "suite": suite_name,
                    "metric": type(metric).__name__,
                    "score": 0.0,
                    "threshold": metric.threshold,
                    "passed": False,
                    "reason": error,
                    "latency": latency,
                    "repetition": repetition,
                }
                for metric in metrics
            ]

        test_case = LLMTestCase(
            input=golden.input,
            actual_output=answer,
            expected_output=golden.expected_output,
            context=golden.context,
            retrieval_context=golden.retrieval_context,
            metadata=golden.additional_metadata,
        )
        results = []
        for metric in metrics:
            try:
                score = metric.measure(test_case)
                passed = bool(metric.is_successful())
                reason = metric.reason or ""
            except Exception as exception:
                score = 0.0
                passed = False
                reason = str(exception)
            results.append(
                {
                    "suite": suite_name,
                    "metric": type(metric).__name__,
                    "score": score,
                    "threshold": metric.threshold,
                    "passed": passed,
                    "reason": reason,
                    "latency": latency,
                    "repetition": repetition,
                }
            )
        return results

    @staticmethod
    def _print_results(results: list[dict[str, Any]], console: Console) -> None:
        table = Table(title="Evaluation results")
        table.add_column("Suite")
        table.add_column("Metric")
        table.add_column("Score", justify="right")
        table.add_column("Threshold", justify="right")
        table.add_column("Result")
        table.add_column("Latency", justify="right")
        table.add_column("Reason")
        for result in results:
            table.add_row(
                result["suite"],
                result["metric"],
                f"{result['score']:.2f}",
                f"{result['threshold']:.2f}"
                if result["threshold"] is not None
                else "-",
                "[green]pass[/green]" if result["passed"] else "[red]fail[/red]",
                f"{result['latency']:.2f}s",
                result["reason"],
            )
        console.print(table)
