# pyright: reportCallIssue=false
"""Evaluation smoke checks for this lesson."""

from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import PatternMatchMetric

EVAL_SUITES = {
    "budget_expert_routing": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="budget_expert_routing",
                    input="What's a realistic daily budget for visiting Rome?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*budget)(?=.*day)(?=.*accommodation)(?=.*food).*",
                ignore_case=True,
            )
        ],
    ),
    "destination_expert_routing": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="destination_expert_routing",
                    input="Recommend destinations for someone who loves beaches and diving",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*destination)(?=.*beach).*", ignore_case=True
            )
        ],
    ),
    "multi_expert_coordination": (
        EvaluationDataset(
            goldens=[
                Golden(
                    name="multi_expert_coordination",
                    input="I have $150 per day to spend in Asia. Where should I go?",
                    additional_metadata={"reset_chatbot": True},
                )
            ]
        ),
        [
            PatternMatchMetric(
                pattern="(?s)(?=.*budget)(?=.*destination).*", ignore_case=True
            )
        ],
    ),
}

EVAL_REPETITIONS = 1
EVAL_MIN_PASS_RATE = 0.8
