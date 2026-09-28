# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "person_of_interest": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="person_of_interest",
                    input="What is the first name of Tom's mistress?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*Myrtle).*", ignore_case=True)],
    ),
    "specific_fact": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="specific_fact",
                    input="What university did Jay attend?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*Oxford).*", ignore_case=True)],
    ),
    "enumeration": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="enumeration",
                    input="What type of drink is served at Gatsby's parties?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [PatternMatchMetric(pattern="(?s)(?=.*cocktail).*", ignore_case=True)],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
