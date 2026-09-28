# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "person_extraction": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="person_extraction",
                    input="What is Einstein known for?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*Albert)(?=.*Einstein)(?=.*1879).*", ignore_case=True
            )
        ],
    ),
    "person_format": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="person_format",
                    input="Who was the first woman to be awarded a nobel prize?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*Marie)(?=.*Curie)(?=.*1867).*", ignore_case=True
            )
        ],
    ),
    "no_person": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="no_person",
                    input="Why did the Titanic sink?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*1912).*", ignore_case=True)],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
