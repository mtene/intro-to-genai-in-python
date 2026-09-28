# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "simple_factual": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="simple_factual",
                    input="What is the capital of Romania?",
                    additional_metadata={"reset_chatbot": False},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*Bucharest).*", ignore_case=True)],
    ),
    "history_reference": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="history_reference",
                    input="What was my previous question?",
                    additional_metadata={"reset_chatbot": False},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*capital)(?=.*Romania).*", ignore_case=True
            )
        ],
    ),
    "multi_turn": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="multi_turn",
                    input="Translate your first answer to German",
                    additional_metadata={"reset_chatbot": False},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*Bukarest).*", ignore_case=True)],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
