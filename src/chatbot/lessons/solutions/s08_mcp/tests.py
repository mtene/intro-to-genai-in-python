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
                    input=(
                        "Use convert_currency to convert 100 USD to EUR. "
                        "Reply with only the numeric EUR amount."
                    ),
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern=r"(?s)(?=.*\d+\.\d+).*")],
    ),
    "time_conversion": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="time_conversion",
                    input=(
                        "Use convert_time to convert 16:00 from Europe/Oslo to "
                        "America/New_York. Reply with only the tool output."
                    ),
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern=r"(?s).*\[America/New_York\].*")],
    ),
    "mcp_search": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="mcp_search",
                    input="What is the equivalent of GitHub Actions in Azure DevOps?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*Azure Pipelines).*", ignore_case=True
            )
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
