# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "currency_conversion": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="currency_conversion",
                    input="Is 100 USD enough to buy a 50 EUR present? Answer with just yes or no",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*yes).*", ignore_case=True)],
    ),
    "time_conversion": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="time_conversion",
                    input="What is 4 PM Oslo time in New York?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*10).*", ignore_case=True)],
    ),
    "microsoft_search": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="microsoft_search",
                    input="What is the equivalent of GitHub Actions in Azure DevOps?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*pipelines).*", ignore_case=True)],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
