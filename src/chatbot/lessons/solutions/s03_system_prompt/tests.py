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
                    input="What is the capital of France?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*Paris).*", ignore_case=True)],
    ),
    "explanation": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="explanation",
                    input="Explain what Python is in one sentence",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*programming).*", ignore_case=True)],
    ),
    "system_prompt_adherence": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="system_prompt_adherence",
                    input="Tell me about your personality",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern=(
                    "(?s)(?=.*(?:bubbl|enthusias|positiv|joy|excit|cheerful|sunshine)).*"
                ),
                ignore_case=True,
            )
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
