# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "letter_partner": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="letter_partner",
                    input="Write a letter to my partner for our anniversary",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*love).*", ignore_case=True)],
    ),
    "telegram_dino": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="telegram_dino",
                    input="Write a a telegram describing dinosaur extinction",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(
            pattern=(
                r"(?s)(?!.*(?:\S+\s+){30}\S)"
                r"(?=.*(?:impact|asteroid|extinct|collision|catastroph)).*"
            ),
            ignore_case=True,
        )],
    ),
    "postcard_cheese": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="postcard_cheese",
                    input="Write a haiku about cheese from Greece",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern=r"(?s)(?=.*(?:feta|cheese)).*\n.*\n.*",
                ignore_case=True,
            )
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
